# Backup and recovery

[Overview](../README.md) · [Storage](storage.md) · [Operations](operations.md)

## Final coverage

The enabled Proxmox job runs **daily**, in **snapshot** mode, with **Zstandard** compression and **keep-last=7**. Its explicit guest list is **100, 101, 102**. Archives exist for all three, including the first ai-worker backup from the completion session. The [reference stanza](../config/proxmox-backup.example.cfg) omits the private job identity.

VM 100's disk includes application data, Qdrant and knowledge state; LXC 101 contains Pi-hole; VM 102 contains the embedding runtime and model cache. The observed VM 100/Pi-hole archives predate the final evening changes. Verify the next successful scheduled run before relying on an archive for that exact final state.

`basecamp-storage` and `basecamp-backups` share one HDD/filesystem. They are not independent copies. Off-host protection, recovery-time objectives and an isolated restore test remain unverified.

## Before maintenance

Check enabled status, guest scope, available capacity, last successful task, and archive timestamps through Proxmox or `pvesm list basecamp-backups`. Keep final private environment/CA settings, Pi-hole exports, WebUI settings and knowledge source/state backups outside GitHub.

Preserve Qdrant storage or a validated snapshot **together with** knowledge sources, processed files and `state/ingested.json`. Pause ingestion for an application-consistent copy. A filesystem copy of a running database is not automatically consistent. A successful guest snapshot job proves an archive exists; it does not prove restoration.

## Isolated restore drill — not yet completed

1. Select a successful archive and an unused test guest ID with sufficient storage. Never restore over a live guest as a test.
2. Restore with networking disconnected or isolated and autostart disabled.
3. Remove duplicate addressing/identities before connecting a test network. Keep restored Pi-hole DHCP isolated from the production LAN. Review GPU passthrough so two guests cannot claim the same device.
4. Boot and check filesystems, application login and data. Restore a consistent Qdrant/knowledge pair and run a known query. Test embeddings only with a compatible available GPU/runtime.
5. Record archive/date, recovery time, results and discrepancies privately; publish sanitized conclusions. Keep production running until a deliberate cutover.

## Rollback

Record deployed commits/digests and preserve pre-change data before updates. Roll back code/configuration only when the previous version supports the current data format. For a database migration, first restore matching pre-change data in isolation. Changing an image tag alone is not a safe database downgrade.

Host reboot recovery passed in the completion session. That is distinct from restoring a lost or damaged guest from backup.

## Post-V1 operating record

See the [September 27 current state](current-state.md), [incident resolutions](changes/2026-09-27.md), and [Sentinel runbook](sentinel.md) for workstation naming, physical power work, independent DNS/monitoring, mobile access and backup validation. The V1 measurements above remain dated evidence. Sentinel backups to Basecamp do not establish off-host protection for Basecamp guest backups.
