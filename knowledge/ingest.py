#!/usr/bin/env python3

import os
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import requests
from pypdf import PdfReader
from docx import Document

BASE = Path(os.environ.get("KNOWLEDGE_BASE", "/opt/basecamp/knowledge"))
INBOX = BASE / "inbox"
PROCESSED = BASE / "processed"
STATE_FILE = BASE / "state" / "ingested.json"

EMBED_URL = os.environ["EMBEDDING_URL"]
QDRANT_URL = os.environ["QDRANT_URL"].rstrip("/")
COLLECTION = "homelab_knowledge"

SUPPORTED = {".txt", ".md", ".pdf", ".docx"}

TARGET_CHARS = 1400
OVERLAP_CHARS = 200


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state):
    STATE_FILE.write_text(
        json.dumps(state, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def file_hash(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def clean_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_txt(path):
    return clean_text(path.read_text(encoding="utf-8", errors="replace"))


def extract_pdf(path):
    reader = PdfReader(str(path))
    pages = []

    for number, page in enumerate(reader.pages, start=1):
        text = clean_text(page.extract_text() or "")
        if text:
            pages.append(f"## Page {number}\n\n{text}")

    return "\n\n".join(pages)


def extract_docx(path):
    doc = Document(str(path))
    parts = []

    for paragraph in doc.paragraphs:
        text = clean_text(paragraph.text)
        if not text:
            continue

        style = (paragraph.style.name or "").lower()

        if style.startswith("heading"):
            match = re.search(r"(\d+)", style)
            level = min(int(match.group(1)), 6) if match else 2
            parts.append(f"{'#' * level} {text}")
        else:
            parts.append(text)

    return "\n\n".join(parts)


def extract_text(path):
    suffix = path.suffix.lower()

    if suffix in {".txt", ".md"}:
        return extract_txt(path)
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix == ".docx":
        return extract_docx(path)

    raise ValueError(f"Unsupported file type: {suffix}")


def split_sections(text):
    sections = []
    current_heading = "Document"
    buffer = []

    def flush():
        nonlocal buffer
        body = clean_text("\n\n".join(buffer))
        if body:
            sections.append((current_heading, body))
        buffer = []

    for line in text.splitlines():
        stripped = line.strip()

        if re.match(r"^#{1,6}\s+\S", stripped):
            flush()
            current_heading = re.sub(r"^#{1,6}\s+", "", stripped).strip()
        else:
            buffer.append(line)

    flush()

    if not sections and clean_text(text):
        sections.append(("Document", clean_text(text)))

    return sections


def chunk_body(body):
    body = clean_text(body)

    if len(body) <= TARGET_CHARS:
        return [body] if body else []

    chunks = []
    start = 0

    while start < len(body):
        end = min(start + TARGET_CHARS, len(body))

        if end < len(body):
            candidates = [
                body.rfind("\n\n", start, end),
                body.rfind(". ", start, end),
                body.rfind("\n", start, end),
                body.rfind(" ", start, end),
            ]
            split_at = max(candidates)

            if split_at > start + 400:
                if body[split_at:split_at + 2] == ". ":
                    end = split_at + 1
                else:
                    end = split_at

        chunk = body[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(body):
            break

        start = max(end - OVERLAP_CHARS, start + 1)

    return chunks


def make_chunks(text):
    chunks = []

    for section, body in split_sections(text):
        for piece in chunk_body(body):
            chunks.append({
                "section": section,
                "text": piece,
            })

    return chunks


def embed(text):
    r = requests.post(
        EMBED_URL,
        json={"inputs": text},
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()

    if not data or not isinstance(data[0], list):
        raise RuntimeError("Unexpected embedding response")

    if len(data[0]) != 2560:
        raise RuntimeError(
            f"Unexpected embedding dimension: {len(data[0])}"
        )

    return data[0]


def qdrant_put(points):
    r = requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION}/points?wait=true",
        json={"points": points},
        timeout=120,
    )
    r.raise_for_status()


def delete_document(source):
    r = requests.post(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/delete?wait=true",
        json={
            "filter": {
                "must": [
                    {
                        "key": "source",
                        "match": {"value": source},
                    }
                ]
            }
        },
        timeout=120,
    )
    r.raise_for_status()


def point_id(source, digest, chunk_number):
    raw = f"{source}:{digest}:{chunk_number}".encode()
    value = hashlib.sha256(raw).hexdigest()
    return int(value[:15], 16)


def ingest_file(path, state):
    digest = file_hash(path)
    previous = state.get(path.name)

    if previous and previous.get("sha256") == digest:
        print(f"SKIP: {path.name} (identical version already ingested)")
        destination = PROCESSED / path.name
        if destination.exists():
            destination.unlink()
        shutil.move(str(path), str(destination))
        return

    print(f"READ: {path.name}")
    text = extract_text(path)

    if not text:
        print(f"SKIP: {path.name} (no extractable text)")
        return

    chunks = make_chunks(text)

    if not chunks:
        print(f"SKIP: {path.name} (no chunks produced)")
        return

    print(f"INGEST: {path.name} ({len(chunks)} chunks)")

    # Embed everything first. The existing indexed document remains intact
    # if extraction or embedding fails partway through.
    points = []

    for number, chunk in enumerate(chunks, start=1):
        print(
            f"  embedding {number}/{len(chunks)} "
            f"[{chunk['section']}]"
        )

        embedding_input = (
            f"Document: {path.name}\n"
            f"Section: {chunk['section']}\n\n"
            f"{chunk['text']}"
        )

        points.append({
            "id": point_id(path.name, digest, number),
            "vector": embed(embedding_input),
            "payload": {
                "text": chunk["text"],
                "source": path.name,
                "file_type": path.suffix.lower().lstrip("."),
                "section": chunk["section"],
                "chunk": number,
                "total_chunks": len(chunks),
                "sha256": digest,
                "ingested_at": utc_now(),
            },
        })

    # Replace the old version only after the new version is fully prepared.
    if previous:
        print(f"REPLACE: removing previous index for {path.name}")
        delete_document(path.name)

    qdrant_put(points)

    state[path.name] = {
        "sha256": digest,
        "chunks": len(chunks),
        "file_type": path.suffix.lower().lstrip("."),
        "ingested_at": utc_now(),
    }

    save_state(state)

    destination = PROCESSED / path.name

    if destination.exists():
        destination.unlink()

    shutil.move(str(path), str(destination))

    print(f"DONE: {path.name}")


def main():
    state = load_state()

    files = sorted(
        p for p in INBOX.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED
    )

    if not files:
        print("No supported files found in inbox.")
        return

    for path in files:
        try:
            ingest_file(path, state)
        except Exception as exc:
            print(f"ERROR: {path.name}: {exc}")
            print("  File left in inbox; verify index/state before retrying.")


if __name__ == "__main__":
    main()
