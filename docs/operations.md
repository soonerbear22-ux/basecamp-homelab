# Operations runbook

[Overview](../README.md) · [Rebuild](rebuild.md) · [Backups](backup-recovery.md) · [Troubleshooting](troubleshooting.md)

## Routine read-only checks

On Proxmox, inspect host/storage health, guest state and recent backup task outcomes. In core-services, inspect Docker state and the ingestion watcher. In ai-worker, inspect guest memory, GPU availability and embedding service health.

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}'
systemctl is-active homelab-knowledge-ingest.path
journalctl -u homelab-knowledge-ingest.service -n 30 --no-pager
python scripts/verify_runtime.py --env-file site.env
```

The runtime verifier calls all thirteen documented API routes, requires JSON responses, checks knowledge health/dimensions and audit completeness, and prints aggregate results only. It does not prove every component or API value is correct. Raw journal/API output can contain private data; keep it local.

For the frozen private corpus only, add `--expected-points 244`. For a different installation, use its own known baseline. Verify source inventory/provenance separately; point count alone cannot detect missing sources with equal replacement counts.

## Fresh-corpus ingestion acceptance

1. Start with an empty test collection and active embedding dependency; verify dimensions are 2560 and distance is Cosine.
2. Copy `knowledge/samples/retrieval-check.md` to a staging directory on the knowledge filesystem, finish writing, then move it into `inbox`.
3. Check that the watcher triggers, the service exits successfully, the file moves to `processed`, and the state entry matches its digest. An inactive oneshot after successful completion is normal; the path unit should remain active.
4. Query for workload placement or recovery order through `/knowledge/search.json`. Confirm the returned source/section belongs to the sample. Do not paste private result text into public logs.
5. Repeat the same file/content and confirm it is skipped without duplicate points. Keep this synthetic source as an identified test fixture, or remove its points/state/source consistently under controlled maintenance. Do not perform partial cleanup.

Manual ingestion should use `systemctl start homelab-knowledge-ingest.service` so it receives the same environment and lock. Direct invocations without that lock can race. Before changing state or doing database maintenance, stop the watcher and wait for the service to finish; preserve source/state/database backups.

## Recovery order

1. Recover Proxmox and storage; inspect the host before changing guests.
2. Verify Pi-hole/DNS and all three guest states. Confirm ai-worker's guest agent.
3. Check Docker startup, Qdrant, Prometheus and GPU/TEI readiness.
4. Check embeddings, retrieval and the full audit, then the WebUI and other interfaces.
5. Check the inbox watcher, scheduled backup scope and application-specific functions. Main-PC inference/image availability is separate from Basecamp recovery.

All three guests and eleven containers recovered in the recorded V1 reboot test. That observation does not justify unattended repeat reboots while users depend on the lab.

## Maintenance and rollback

Record the current release/digests, verify backup timestamps and preserve private inputs. Update one dependency at a time in a test environment; do not use unreviewed floating image updates. Re-run repository checks, affected regression tests and runtime acceptance. Apply only after checking schema/data compatibility. Follow the [backup runbook](backup-recovery.md) for rollback; a database downgrade may require matched data restoration.

The reference Compose file uses the same container names as the live lab. It is a rebuild artifact, not an instruction to start a second copy on the frozen host.
