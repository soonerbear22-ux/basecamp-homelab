# Storage and persistence

[Overview](../README.md) · [Backups](backup-recovery.md)

## Observed layout

The large Basecamp disk has approximately 3.6 TB formatted capacity. The Proxmox storage IDs `basecamp-storage` and `basecamp-backups` point to locations on the same ext4 filesystem and physical disk. They are not independent copies.

VM 100 and VM 102 each have a 100 GB system disk on local-lvm. Pi-hole LXC 101 has an 8 GB root filesystem. The knowledge tree resides within core-services' guest filesystem.

## Application data boundaries

Persisted data includes Open WebUI, Grafana, Prometheus, Uptime Kuma, Beszel, Homepage configuration/images, Qdrant, and the knowledge source/state tree.

The inspected Qdrant storage is outside the common application-data directory. Backing up only that directory would omit Qdrant and the knowledge tree. The public templates use generic reproducible paths: `/opt/basecamp/data`, `/opt/basecamp/compose/qdrant/storage`, `/opt/basecamp/knowledge`, and the worker's model cache. No private storage identities or device serials are included.

## Remaining work

A daily job and observed archives now cover all three guests. A named destination, mount or successful archive still does not establish application consistency or tested restoration. Independent off-host copies and isolated restore validation are not claimed by this inventory.

## September 29 media addition

[Jellyfin and media automation](jellyfin.md) add unprivileged guests 103 and 104. Today's read-only checks confirm Jellyfin health, five running media containers, and saved Radarr/Sonarr import/upgrade refresh hooks. The enabled backup job includes guest 103 but excludes guest 104; externally mounted library data needs separate protection. See the [dated evidence and remaining acceptance work](changes/2026-09-29.md). These services are outside the immutable V1 rebuild package and the core-only automatic inventory.


## October 3 Arda storage

VM 105 `arda` has a 64 GB qcow2 virtual disk on `basecamp-storage`. Inside the guest, the AzerothCore runtime and local timestamped database/configuration backups reside on that VM's storage path.

Arda's daily in-guest backup timer is distinct from Proxmox guest-archive protection. A verified local SQL/configuration backup does not establish VM-level, off-host, or bare-metal recovery. Proxmox backup coverage for VM 105 is not claimed without a separate host-level verification.
