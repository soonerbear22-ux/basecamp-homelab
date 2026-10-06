# Backup and recovery

[Overview](../README.md) · [Storage](storage.md) · [Operations](operations.md)

## Current protection — canonical state through October 6

Configured Proxmox policy is daily snapshot, Zstandard, keep-last=7 for guests **100–105**. Current logical inventory includes `hornburg-backups` (about 1833 GiB, 2 TB class). Physical device/mount separation and newer scheduled-success readback remain unresolved in the supplied canonical package. Use the actual configured target privately; do not rely on the old `basecamp-backups` example as a current deployment instruction.

Selected 104/105 archives passed integrity checks and isolated whole-guest restores; test guests/volumes were removed. External media, independent/off-host copies, other four guest restores, separate SQL import/client recovery and consistent knowledge-data restoration remain separate limits. A newest-archive health page is not proof every expected guest is fresh.

The historical records below retain former backup scopes and shared-HDD placement. They do not override this current logical inventory or selected restore acceptance. No backup runtime changes or new scheduled verification were performed during repository synchronization.

## V1 coverage — September 26, 2026

The enabled Proxmox job runs **daily**, in **snapshot** mode, with **Zstandard** compression and **keep-last=7**. Its explicit guest list is **100, 101, 102**. Archives exist for all three, including the first ai-worker backup from the completion session. The [reference stanza](../config/proxmox-backup.example.cfg) omits the private job identity.

VM 100's disk includes application data, Qdrant and knowledge state; LXC 101 contains Pi-hole; VM 102 contains the embedding runtime and model cache. The observed VM 100/Pi-hole archives predate the final evening changes. Verify the next successful scheduled run before relying on an archive for that exact final state.

`basecamp-storage` and `basecamp-backups` share one HDD/filesystem. They are not independent copies. Off-host protection, recovery-time objectives and an isolated restore test remain unverified.

## Before maintenance

Check enabled status, guest scope, available capacity, last successful task, and archive timestamps through Proxmox or `pvesm list <CONFIGURED_BACKUP_STORAGE>`. Keep final private environment/CA settings, Pi-hole exports, WebUI settings and knowledge source/state backups outside GitHub.

Preserve Qdrant storage or a validated snapshot **together with** knowledge sources, processed files and `state/ingested.json`. Pause ingestion for an application-consistent copy. A filesystem copy of a running database is not automatically consistent. A successful guest snapshot job proves an archive exists; it does not prove restoration.

## Isolated restore procedure

1. Select a successful archive and an unused test guest ID with sufficient storage. Never restore over a live guest as a test.
2. Restore with networking disconnected or isolated and autostart disabled.
3. Remove duplicate addressing/identities before connecting a test network. Keep restored Pi-hole DHCP isolated from the production LAN. Review GPU passthrough so two guests cannot claim the same device.
4. Boot and check filesystems, application login and data. Restore a consistent Qdrant/knowledge pair and run a known query. Test embeddings only with a compatible available GPU/runtime.
5. Record archive/date, recovery time, results and discrepancies privately; publish sanitized conclusions. Keep production running until a deliberate cutover.

## Rollback

Record deployed commits/digests and preserve pre-change data before updates. Roll back code/configuration only when the previous version supports the current data format. For a database migration, first restore matching pre-change data in isolation. Changing an image tag alone is not a safe database downgrade.

Host reboot recovery passed in the completion session. That is distinct from restoring a lost or damaged guest from backup.

## Historical post-V1 operating record

See the [September 27 current state](current-state.md), [incident resolutions](changes/2026-09-27.md), and [Sentinel runbook](sentinel.md) for workstation naming, physical power work, independent DNS/monitoring, mobile access and backup validation. The V1 measurements above remain dated evidence. Sentinel backups to Basecamp do not establish off-host protection for Basecamp guest backups.

## September 29 media addition

[Jellyfin and media automation](jellyfin.md) add unprivileged guests 103 and 104. Today's read-only checks confirm Jellyfin health, five running media containers, and saved Radarr/Sonarr import/upgrade refresh hooks. The enabled backup job includes guest 103 but excludes guest 104; externally mounted library data needs separate protection. See the [dated evidence and remaining acceptance work](changes/2026-09-29.md). These services are outside the immutable V1 rebuild package and the core-only automatic inventory.


## October 3 Arda backup path

Arda (VM 105) has a separate application-level backup path inside the guest. A persistent daily systemd timer runs `/usr/local/bin/arda-backup`, producing compressed dumps of `acore_auth`, `acore_characters`, and `acore_world` plus configuration files.

A manual October 3 backup completed and all three compressed SQL archives passed gzip integrity checks.

This is application-level protection only. It does not prove:

- VM 105 is included in the Proxmox guest-backup job;
- the backup is off-host;
- a database restore has been completed successfully;
- the VM itself can be reconstructed from this backup without the documented runtime/configuration steps.

Keep the [Arda runbook](arda.md) with the backup artifacts so source revision, runtime layout, service units and the worldserver stdin workaround are available during recovery.


## Historical October 3 Proxmox coverage

During the Hornburg rename preflight, live inspection found the enabled daily job included 100–103 and excluded 104/105. It was expanded to **100,101,102,103,104,105**, preserving the existing schedule, snapshot mode, Zstandard compression, storage and keep-last=7 retention.

First full backups of media-automation (104) and Arda (105) completed successfully. Both passed Zstandard integrity tests; the media archive contains its rootfs/media-stack configuration, and Arda's archive passed VMA block-integrity verification. Archives and matching successful completion logs were observed for all six guests. Only the new 104/105 archives were integrity-tested in this session.

The host's selected configuration and all six guest definitions were preserved in a protected checkpoint, with a checksum-verified copy on Elros. Guest archives remain on the same HDD/filesystem; this checkpoint does not establish off-host protection for the full guest disks. Media/data bind mounts need separate backups. Isolated whole-guest restoration now passed for 104 and 105; the other four guest restores, a separate SQL-dump import and a consistent Qdrant/knowledge restore remain untested.

The existing backup-health page checks only the newest guest archive, not freshness for every expected guest. Its OK status cannot substitute for the per-guest checks above.

The native Proxmox/Linux name is now `hornburg`. After the selected recovery checks passed, the approved maintenance outage and operator-issued reboot completed successfully. All six guests started automatically and the daily backup job was re-enabled for 100–105. Existing storage IDs and paths remain unchanged. The next successful scheduled backup remains to be observed. See the [completed maintenance record](hornburg-rename-preflight.md).

## October 3 isolated restore results

The new media archive was restored into an unused test LXC with a fresh root disk, no bind mounts, no network interface and autostart disabled. Docker and all five application endpoints passed local checks. External media-library recovery and external service integration were outside this test.

The new Arda VMA archive was restored into an unused test VM on a separate volume, with networking removed and autostart disabled before boot. MySQL, auth, world and the backup timer started; all three database schemas were queried successfully and the expected application ports listened. This tests whole-VM recovery, not a separate database-dump import or game-client login.

Both test guests and their temporary volumes were removed after graceful shutdown. Production guests stayed running, and their config hashes remained unchanged. The daily snapshot/zstd/keep-last=7 job was paused during the drill and re-enabled for 100–105. Its next successful scheduled run remains to be observed.

Selected config rollback material has a checksum-verified off-host copy. The complete guest archives and external media/data still require independent protection. A consistent pmxcfs database checkpoint also passed SQLite integrity checking and is retained privately.
