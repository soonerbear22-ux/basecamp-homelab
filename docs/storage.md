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
