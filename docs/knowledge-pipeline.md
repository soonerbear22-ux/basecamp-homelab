# Knowledge pipeline

[Overview](../README.md) · [Rebuild](rebuild.md) · [Operations](operations.md)

The final direct inventory contains **34 distinct source names and 244 points**, including retained validation documents. This supersedes the earlier two-source/101-point observation. Private source names and content are not distributed.

## Processing contract

1. Place a completed document in the authenticated inbox.
2. A `DirectoryNotEmpty` path unit activates a oneshot service after a three-second delay.
3. `flock -n` acquires the writable state-directory lock before ingestion.
4. Extract `.md`, `.txt`, `.pdf` or `.docx`; heading-aware chunks target 1400 characters with 200-character overlap.
5. Generate 2560-dimensional embeddings and store them in Qdrant's `homelab_knowledge` Cosine collection.
6. Persist provenance, update filename/SHA-256 state, and move the successful source to `processed`.

Payloads contain text, source, section, chunk ordinal/count, file type, digest and timestamp. Identical content under the same filename is skipped. Changed documents are fully embedded before replacement begins.

Delete and upsert are separate database requests. Failure between them can remove an old index without completing the replacement. State writes are not transactional with Qdrant. Compare state, processed files and database inventory before retrying. The public source retains this behavior and corrects an error message that previously overclaimed preservation.

## Locking and transfer completion

The final lock is `/opt/basecamp/knowledge/state/ingest.lock`. An earlier lock under `/run` failed under the service user; moving it to the writable state directory fixed the permission failure. The completion session tested automatic ingestion with the lock and removed its temporary test document afterward.

Every manual ingest must acquire the same lock. This does not serialize unrelated database maintenance or Samba writes. The three-second delay is a mitigation, not a transfer-completion protocol: finish writing outside the watched inbox, then move the file into it on the same filesystem. Quarantine failing/unsupported files outside the inbox to avoid repeated path activation; preserve the source.

## Acceptance and limits

Use the synthetic [retrieval sample](../knowledge/samples/retrieval-check.md) in a fresh test corpus. A public rebuild has its own point count; it does not inherit the private 244-point corpus.

Check actual embeddings, collection dimensions/distance, source provenance, semantic retrieval and source inventory. A green small collection can return results with `indexed_vectors_count: 0`; that field alone does not prove failure. A passing health query does not prove corpus completeness or answer quality.

PDF extraction has no OCR; DOCX extraction reads paragraphs/headings, not tables. Empty or failed documents may remain in the inbox. Invalid state JSON currently falls back to an empty state: preserve and repair it before another ingest. These are documented V1 limitations.


## October 3 hardening and recovery

A maintenance session identified that the inbox is actively watched by `homelab-knowledge-ingest.path`; files placed there can be consumed within seconds. Recovery or editing work should therefore stage documents outside the inbox, pause the path unit when necessary, and only move completed files into the inbox for deliberate ingestion.

A secret-bearing filename guard was added after recovery material was found in the private corpus. The ingester now rejects filenames containing common password, credential, recovery-code, private-key and environment-file indicators before extraction or embedding. This is a preventive filename heuristic, not a substitute for content-level secret scanning.

The same session repaired the Arda knowledge document by staging it outside the watched inbox, reingesting once, and verifying that the processed file hash, state metadata and exact Qdrant source count agreed. See the [October 3 change record](changes/2026-10-03.md).
