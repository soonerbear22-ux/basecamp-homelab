# Operations runbook

[Overview](../README.md) · [Rebuild](rebuild.md) · [Backups](backup-recovery.md) · [Troubleshooting](troubleshooting.md)

## Current monitoring operation

Use [monitoring](monitoring.md) for the verified six-direction triangle. Inspect Elros task `Elros-Homelab-Watcher`, Local Service principal, boot/minute triggers, last result and advancing JSON status under `C:\ProgramData\MiddleEarthMonitoring\data`. A registered task alone is not execution evidence. Source under `bin` must remain protected; service write access belongs only in data. Status older than three minutes is stale.

Inspect peer Kuma heartbeats and Prometheus targets independently. Core's new Sentinel checks have no notifications; Elros has local output only. Planned reboot and full notification acceptance remain follow-ups. Use disposable fixtures for recovery, not production shutdowns. Reference V1 Compose is not a second production deployment. Six-guest host autostart was observed during October 3 cutover, but the prior Prometheus restart miss still requires planned maintenance acceptance.

## Current backup-health operation

Use the [backup runbook](backup-recovery.md) for the deployed per-guest checker, retained host rule and unchanged JSON interface. Inspect the UUID-backed backup mount, current job target and each expected guest archive before maintenance. Check `basecamp-backup-health.service` result/journal and `basecamp-backup-health.timer` enablement, activity and actual subsequent invocation independently. Enabled status and next due time alone are not invocation proof.

Acceptance proceeds through syntax, controlled checker/service result, all six guest log lines, JSON, existing HTTP endpoint, core-services fetch and Homepage tile, then normal scheduled generation. Use disposable redirected fixtures for failure cases; do not modify production archive mtimes or rerun a full backup to fix the page. Keep private endpoints, device identifiers, raw logs and rollback paths outside public Git. Current source/hash, timer provenance and Homepage acceptance remain unresolved in the dated evidence.

Gwaihir's commissioned dashboard listener is 8088. Inspect existing service/source before changes; local service health, remote route, guest-query authentication and source publication are different checks. See [Gwaihir](gwaihir.md).

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
2. Verify Pi-hole/DNS and all six current guest states. Confirm ai-worker's guest agent.
3. Check Docker startup, Qdrant, Prometheus and GPU/TEI readiness.
4. Check embeddings, retrieval and the full audit, then the WebUI and other interfaces.
5. Check the inbox watcher, scheduled backup scope and application-specific functions. Main-PC inference/image availability is separate from Hornburg recovery.

All three guests and eleven containers recovered in the recorded V1 reboot test. That observation does not justify unattended repeat reboots while users depend on the lab.

## Maintenance and rollback

Record the current release/digests, verify backup timestamps and preserve private inputs. Update one dependency at a time in a test environment; do not use unreviewed floating image updates. Re-run repository checks, affected regression tests and runtime acceptance. Apply only after checking schema/data compatibility. Follow the [backup runbook](backup-recovery.md) for rollback; a database downgrade may require matched data restoration.

The reference Compose file uses the same container names as the live lab. It is a rebuild artifact, not an instruction to start a second copy on the frozen host.

## Post-V1 operating record

See the [September 27 current state](current-state.md), [incident resolutions](changes/2026-09-27.md), and [Sentinel runbook](sentinel.md) for workstation naming, physical power work, independent DNS/monitoring, mobile access and backup validation. The V1 measurements above remain dated evidence. Sentinel backups to Basecamp do not establish off-host protection for Basecamp guest backups.

## Historical September 29 media addition (coverage superseded by current state)

[Jellyfin and media automation](jellyfin.md) add unprivileged guests 103 and 104. Today's read-only checks confirm Jellyfin health, five running media containers, and saved Radarr/Sonarr import/upgrade refresh hooks. The enabled backup job includes guest 103 but excludes guest 104; externally mounted library data needs separate protection. See the [dated evidence and remaining acceptance work](changes/2026-09-29.md). These services are outside the immutable V1 rebuild package and the core-only automatic inventory.


## October 3 current-recovery additions

The immutable V1 reboot evidence covers only the original three guests. Current operations now also include media guests 103/104 and Arda VM 105.

For current-topology recovery:

1. recover the Proxmox host and storage first;
2. verify the original infrastructure guests;
3. verify Jellyfin/media guests separately;
4. verify Arda VM 105, then MySQL, `arda-auth.service`, `arda-world.service`, and the realm listeners;
5. check Arda journal growth for recurrence of the documented `AC>` prompt storm;
6. verify application-level backup timers independently from Proxmox guest-backup coverage.

Do not infer current six-guest recovery from the historical three-guest V1 reboot test.
