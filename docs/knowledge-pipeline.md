# Knowledge ingestion and retrieval

[Overview](../README.md) · [Local AI detail](https://github.com/soonerbear22-ux/local-ai-lab/blob/main/docs/knowledge.md)

## Implemented path

Windows mapped Samba inbox → systemd watcher → document extraction and chunking → Qwen3-Embedding-4B on ai-worker → Qdrant on core-services → Homelab API semantic search.

The inspected ingester accepts Markdown, text, PDF, and DOCX. It uses heading-aware sections, a 1400-character target, 200-character overlap for long sections, stable source filenames, and SHA-256 tracking. PDF extraction does not perform OCR; the inspected DOCX path does not extract table cells.

## Recorded expansion and current discrepancy

At 08:57 UTC on September 26, the expansion report recorded 27 added documents / 135 chunks, removal of one test point, 235 total points, and 28/28 expected-source retrieval checks passing in the top five.

At 21:42 UTC, a fresh audit observed 101 points with successful embedding and semantic search. A direct source inventory then found only `homelab-master.md` (19 points) and `homelab-operations.md` (82 points). The 27 runbook files remain in the processed folder but are not in the current indexed-source inventory.

Both observations are retained. The intervening change and whether it was intentional have not been established. The earlier retrieval results are historical, not proof that those runbooks are currently searchable.

## Operational limits

The watcher remains active. Its three-second pre-start delay followed a successful Samba test, but is not a universal transfer-completion guarantee.

Replacement embeds new chunks before deleting the old source, then performs a separate upsert. Failure after deletion can leave the previous source absent. Reconcile source files, state, database payloads, and actual retrieval before corrective action. No reingestion, deletion, or infrastructure change was performed for this portfolio refresh.
