"""Validate public files, immutable dependencies, links, checksums and Git blobs.

This is a deterministic publication gate, not a complete secret-detection service.
It never prints a matched value. Review the final diff as well.
"""
import argparse
import ast
import hashlib
import io
import ipaddress
import json
from pathlib import Path
import re
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHECKSUMS = ROOT / "release/CHECKSUMS.sha256"
SKIP_DIRS = {".git", ".venv", "vendor", "__pycache__", ".pytest_cache", "private", "secrets", "data", "models"}
ERRORS = []

def git(*args, input=None):
    # This exact checkout was chosen by the caller; no global Git settings change.
    return subprocess.check_output(["git", "-c", "safe.directory=" + ROOT.as_posix(), "-C", str(ROOT), *args], input=input)

def public_files():
    if (ROOT / ".git").exists():
        names = git("ls-files", "--cached", "--others", "--exclude-standard", "-z").decode().split("\0")
        return sorted({ROOT / name for name in names if name and (ROOT / name).is_file()}, key=lambda p: p.relative_to(ROOT).as_posix())
    return sorted((p for p in ROOT.rglob("*") if p.is_file() and not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts)), key=lambda p: p.relative_to(ROOT).as_posix())

def error(name, message):
    ERRORS.append(f"{name}: {message}")

def privacy(name, text, *, source_path=None):
    rules = {
        "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        "GitHub credential": r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})\b",
        "tailnet address": r"\b[\w.-]+\.ts\.net\b",
        "hardware address": r"\b(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\b",
        "SSH identity": r"ssh-(?:rsa|ed25519)\s+AAAA[A-Za-z0-9+/=]{20,}",
        "personal home path": r"(?:[A-Za-z]:[\\/]Users[\\/][^\s/\\]+|/home/(?!user\b|basecamp\b)[A-Za-z0-9_-]+)",
    }
    for kind, pattern in rules.items():
        if re.search(pattern, text): error(name, kind + " pattern found")
    for match in re.finditer(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])", text):
        try: address = ipaddress.ip_address(match.group())
        except ValueError: continue
        if not address.is_loopback and str(address) != "0.0.0.0":
            error(name, "numeric network address found")
            break
    if re.search(r"\b(?:fc|fd)[0-9a-f]{2}(?::[0-9a-f]{0,4}){2,7}\b", text, re.I):
        error(name, "private IPv6 address pattern found")
    for match in re.finditer(r"(?im)^\s*(?:-\s*)?(?:[A-Z0-9_]*(?:TOKEN|PASSWORD|SECRET|API_KEY)[A-Z0-9_]*)\s*[:=]\s*([^\n]+)", text):
        value = match.group(1).strip().strip("\"'")
        # A known filename-filter pattern set is code, not a credential.
        if (source_path or name) == "knowledge/ingest.py" and match.group(0).strip() == "SECRET_NAME_PATTERNS = {":
            continue
        if value and not any(x in value for x in ("${", "REPLACE_ME", "example", "test-only", "os.environ", "env(")):
            error(name, "non-placeholder credential assignment")

def history_reviews():
    """Only exact reviewed infrastructure blobs; credentials cannot be exempted."""
    path = ROOT / "release/history-privacy-review.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    allowed = {"personal home path pattern found", "numeric network address found"}
    reviews = {}
    if data.get("version") != 1:
        raise ValueError("unsupported history review version")
    for item in data["findings"]:
        key = (item["blob"], item["path"], item["category"])
        if (not re.fullmatch(r"[0-9a-f]{40}", item["blob"])
                or item["category"] not in allowed or not item.get("review")
                or key in reviews):
            raise ValueError("invalid or duplicate history review")
        reviews[key] = item["review"]
    return reviews

def scan_history():
    if git("rev-parse", "--is-shallow-repository").decode().strip() == "true":
        error("history", "full clone required")
        return
    reviews = history_reviews()
    seen = set()
    privacy("historical commit messages", git("log", "--all", "--format=%B").decode())
    # rev-list supplies only one representative path. Enumerate trees so an
    # identical blob at an unreviewed path does not inherit an exemption.
    paths = {}
    for commit in git("rev-list", "--all").decode().splitlines():
        for row in git("ls-tree", "-r", "-z", commit).decode().split("\0"):
            if not row:
                continue
            metadata, path = row.split("\t", 1)
            _, kind, sha = metadata.split()
            if kind == "blob":
                paths.setdefault(sha, set()).add(path)
    objects = git("rev-list", "--objects", "--all").decode().splitlines()
    ids = [line.split(" ", 1)[0] for line in objects]
    metadata = git("cat-file", "--batch-check=%(objectname) %(objecttype)", input=("\n".join(ids)+"\n").encode()).decode().splitlines()
    blobs = [line.split()[0] for line in metadata if line.endswith(" blob")]
    stream = io.BytesIO(git("cat-file", "--batch", input=("\n".join(blobs)+"\n").encode()))
    scanned = 0
    for _ in blobs:
        sha, kind, size = stream.readline().decode().strip().split()
        content = stream.read(int(size)); stream.read(1)
        try: text = content.decode("utf-8")
        except UnicodeDecodeError: continue
        name = "history blob " + sha[:12]
        blob_paths = paths.get(sha, set())
        before = len(ERRORS)
        source_path = "knowledge/ingest.py" if blob_paths == {"knowledge/ingest.py"} else None
        privacy(name, text, source_path=source_path)
        findings = ERRORS[before:]
        del ERRORS[before:]
        for finding in findings:
            category = finding[len(name) + 2:]
            keys = {(sha, path, category) for path in blob_paths}
            if keys and keys <= reviews.keys():
                seen.update(keys)
                print(f"REVIEWED: {name}: {category}; exact historical path/blob disposition")
            else:
                ERRORS.append(finding)
        scanned += 1
    for sha, path, category in reviews.keys() - seen:
        error("history review " + sha[:12], "stale or unmatched disposition")
    print(f"Scanned {scanned} unique text blobs reachable from local Git refs.")

def validate(files):
    for path in files:
        name = path.relative_to(ROOT).as_posix()
        if any(part in {"private", "secrets", "data", "models"} for part in Path(name).parts) or path.name in {"site.env", ".env"}:
            error(name, "private/runtime path included")
        try: text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            error(name, "binary artifact needs explicit manual review"); continue
        privacy(name, text)
        try:
            if path.suffix == ".py": ast.parse(text)
            if path.suffix == ".json": json.loads(text)
            if path.suffix in {".yaml", ".yml"}: yaml.safe_load(text)
        except Exception as exc: error(name, "parse failure: " + type(exc).__name__)
        if path.suffix == ".md":
            if len(re.findall(r"^```", text, re.M)) % 2: error(name, "unbalanced code fence")
            for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if re.match(r"(?:https?://|mailto:|#)", link): continue
                target = link.split("#")[0]
                if target and not (path.parent / target).exists(): error(name, "broken relative link: " + target)
    manifest = json.loads((ROOT / "release/manifest.json").read_text())
    for relative in ["deploy/core-services/compose.yaml", "deploy/ai-worker/compose.yaml"]:
        config = yaml.safe_load((ROOT / relative).read_text())
        for name, service in config["services"].items():
            if service.get("restart") != "unless-stopped": error(relative, name + " lacks restart policy")
            if "build" not in service and service["image"] != manifest["images"].get(name): error(relative, name + " digest differs from manifest")
            if "build" not in service and not re.search(r"@sha256:[0-9a-f]{64}$", service["image"]): error(relative, name + " has unpinned image")
    if not re.fullmatch(r"[0-9a-f]{40}", manifest["embedding"]["revision"]): error("manifest", "model revision is not immutable")
    if not re.fullmatch(r"[0-9a-f]{40}", manifest["api_source"]["commit"]): error("manifest", "API commit is not immutable")
    for name, expected in manifest["api_source"]["files"].items():
        path = ROOT / "vendor/homelab-api" / name
        if not path.exists(): error(name, "run scripts/fetch_api.py before validation")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected["sha256"]: error(name, "API dependency checksum mismatch")
        else: privacy("API dependency " + name, path.read_text())
    if (ROOT / "docs/diagrams/basecamp-architecture.md").exists(): error("diagram", "misplaced duplicate")

def checksum_lines(files):
    return [hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.relative_to(ROOT).as_posix() for p in files if p != CHECKSUMS]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--write-checksums", action="store_true", help="Release maintainer: regenerate reviewed file checksums")
    args = parser.parse_args()
    if args.write_checksums and not CHECKSUMS.exists():
        CHECKSUMS.touch()
    files = public_files()
    validate(files)
    if args.history: scan_history()
    lines = checksum_lines(files)
    if args.write_checksums and not ERRORS:
        CHECKSUMS.write_text("\n".join(lines)+"\n", encoding="utf-8", newline="\n")
    elif not CHECKSUMS.exists() or CHECKSUMS.read_text().splitlines() != lines:
        error("release checksums", "missing, changed or incomplete; regenerate only after reviewing changes")
    for message in ERRORS: print("FAIL:", message)
    if ERRORS: raise SystemExit(1)
    print(f"PASS: {len(files)} public files; syntax, links, privacy patterns, pinned dependencies and checksums.")

if __name__ == "__main__":
    main()
