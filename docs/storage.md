# Storage and persistence

[Overview](../README.md) · [Backups](backup-recovery.md)

## Observed layout

The large Basecamp disk has approximately 3.6 TB formatted capacity. The Proxmox storage IDs `basecamp-storage` and `basecamp-backups` point to locations on the same ext4 filesystem and physical disk. They are not independent copies.

VM 100 and VM 102 each have a 100 GB system disk on local-lvm. Pi-hole LXC 101 has an 8 GB root filesystem. The knowledge tree resides within core-services' guest filesystem.

## Application data boundaries

Persisted data includes Open WebUI, Grafana, Prometheus, Uptime Kuma, Beszel, Homepage configuration/images, Qdrant, and the knowledge source/state tree.

The inspected Qdrant storage is outside the common application-data directory. Backing up only that common directory would omit Qdrant and the knowledge tree. Public documentation identifies these boundaries by purpose without publishing the host's private layout.

## Remaining work

A named storage destination and a persistent mount do not establish backup consistency or tested restoration. Centralized NAS service, independent off-host copies, and isolated restore validation are not claimed by this inventory.
