# Storage and persistence

[Overview](../README.md) · [Backups](backup-recovery.md)

## Current logical layout — canonical evidence through October 6

Canonical inventory reports `basecamp-storage` about 3666 GiB, `hornburg-backups` about 1833 GiB (2 TB class), `local` about 94 GiB and `local-lvm` about 794 GiB. The old `basecamp-backups` ID is absent from that returned inventory. Storage IDs retain their independent compatibility meaning; do not rename them with the host.

The changed backup pool is verified logically. A dedicated physical 2 TB device, its mount chain and independence from bulk storage are **not yet verified by the supplied canonical package**. The earlier same-ext4/HDD statement describes the former layout. Neither pool capacity nor name establishes physical separation or off-host protection.

All six current guest root volumes are documented on local-lvm; [current state](current-state.md) has capacities. Arda VM 105's newer 64 GiB local-lvm configuration supersedes the old qcow2-on-bulk-storage record. Resolve exact backing devices privately before disk work.

## Application data boundaries

Persisted data includes Open WebUI, Grafana, Prometheus, Uptime Kuma, Beszel, Homepage configuration/images, Qdrant, and the knowledge source/state tree.

The inspected Qdrant storage is outside the common application-data directory. Backing up only that directory would omit Qdrant and the knowledge tree. The public templates use generic reproducible paths: `/opt/basecamp/data`, `/opt/basecamp/compose/qdrant/storage`, `/opt/basecamp/knowledge`, and the worker's model cache. No private storage identities or device serials are included.

## Remaining work

The configured daily snapshot/zstd/keep-last=7 policy covers all six guests. Selected whole-guest restores of 104/105 passed; the others and external data remain open. A named destination, mount or successful archive still does not establish application consistency or tested restoration. Independent off-host protection and newer scheduled-success/physical-target readback remain unverified.

## Historical September 29 media addition (coverage superseded)

[Jellyfin and media automation](jellyfin.md) add unprivileged guests 103 and 104. Today's read-only checks confirm Jellyfin health, five running media containers, and saved Radarr/Sonarr import/upgrade refresh hooks. The enabled backup job includes guest 103 but excludes guest 104; externally mounted library data needs separate protection. See the [dated evidence and remaining acceptance work](changes/2026-09-29.md). These services are outside the immutable V1 rebuild package and the core-only automatic inventory.


## October 3 Arda storage

The earlier VM 105 qcow2/bulk-storage note is superseded: latest canonical operator configuration records a 64 GiB disk on local-lvm. Inside the guest, the AzerothCore runtime and local timestamped database/configuration backups reside on that VM's storage path.

Arda's daily in-guest backup timer is distinct from Proxmox guest-archive protection. A verified local SQL/configuration backup does not establish VM-level, off-host, or bare-metal recovery. Current host-level policy includes VM 105 and a selected isolated VM restore passed; separate database import/client recovery and off-host protection remain open.
