# Hornburg rename and recovery record - October 3, 2026

[Current state](current-state.md) · [Backup and recovery](backup-recovery.md)

## Completed status

The native Linux/Proxmox node is now **hornburg**, with FQDN **hornburg.home**. The operator approved the six-guest maintenance outage after isolated recovery tests. All six guests were stopped with normal guest shutdown commands, their definitions were moved with hashes unchanged, and the operator issued the single host reboot through Termius because Remote Desktop Commander blocks host reboot commands.

The host returned at approximately **01:50 America/Chicago / 06:50 UTC**. All six guests started automatically. Final application/API checks passed at approximately **01:57 / 06:57 UTC**. The API node reference is deployed, the obsolete empty node directory is removed, and daily backups are enabled again.

## Preserved inventory

| ID | Type | Live guest name | Configured RAM | Root disk |
| --- | --- | --- | --- | --- |
| 100 | VM | core-services | 8 GiB | 100 GiB, local-lvm |
| 101 | LXC | pihole | 1 GiB | 8 GiB, local-lvm |
| 102 | VM | ai-worker | 12 GiB | 100 GiB, local-lvm; GPU passthrough |
| 103 | LXC | jellyfin | 2 GiB | 24 GiB, local-lvm |
| 104 | LXC | media-automation | 4 GiB | 16 GiB, local-lvm |
| 105 | VM | arda | 8 GiB | 64 GiB, basecamp-storage |

All original guest-config hashes, network/storage configuration hashes and SSH public host-key hashes matched after the rename. Guest IDs, guest names, disks, permissions, network addresses, bridge configuration and physical storage paths were preserved. Only guest-definition ownership moved from the old node directory to the new one.

## Compatibility names intentionally retained

| Area | Current choice |
| --- | --- |
| Tailscale | The existing device registration, address and advertised name `basecamp` remain; native Linux/Proxmox is `hornburg` |
| Samba | NetBIOS name remains `BASECAMP`; `HORNBURG` is an additional alias; the share remains `Basecamp` |
| Storage | `basecamp-storage`, `basecamp-backups`, and existing mount paths remain |
| SSH clients | Existing aliases and IP-based connections remain usable; SSH host keys were preserved |
| API | `PVE_NODE` is `hornburg`; existing `/basecamp/*` paths and operation IDs remain compatible |
| Monitoring | Existing IP targets and Prometheus job labels remain, preserving query/history compatibility |
| Guest application paths | Existing `/opt/basecamp` paths and backup/service prefixes remain |

Homepage's Proxmox, backup, primary Pi-hole and related host descriptions now use Hornburg. Older monitor display labels may still use Basecamp; they were not globally rewritten.

## Post-reboot acceptance

- Hornburg is the only node returned by the Proxmox node list and reports online.
- All six guests are running and all four configured storage entries are active.
- Proxmox cluster filesystem, API proxy, API daemon, status daemon and scheduler are active.
- The regenerated TLS certificate names hornburg/hornburg.home and retains the existing IP SAN. The management page returned HTTP 200 with its existing Proxmox CA validated.
- SSH key hashes matched the checkpoint and strict IP-based SSH continued working.
- Primary Pi-hole and independent Sentinel DNS answered direct queries from the workstation.
- Existing Basecamp and knowledge mapped drives remained accessible.
- Jellyfin and all five media automation endpoints returned HTTP 200.
- Arda database, auth, world and backup timer were active; database/auth/world ports were listening.
- The scoped API deployment changed only its node assignment in the private source. Live source/container hashes matched; the ten other core containers were not recreated by that deployment.
- Final API health returned OK, all seven audit components were retrieved, all six expected guests and eleven expected core containers were running, and embeddings/Qdrant/semantic retrieval passed.
- Daily snapshot/Zstandard/keep-last=7 backups are enabled for 100-105. The next scheduled successful run is still to be observed.
- Backup-health HTTP returned OK. Its newest-archive check remains insufficient to establish freshness for every guest.

### Prometheus recovery

Prometheus had exited cleanly during the guest shutdown, with exit code 0 and no OOM indication, but did not restart automatically with the other core containers. Starting the existing container restored readiness. All four configured monitoring targets subsequently reported up with no scrape errors. The reason its restart policy did not bring it back is not established; do not describe that cause as diagnosed.

## Isolated recovery tests completed before cutover

**Media automation:** Its new archive was restored to unused test LXC 9104 on a fresh root disk, with autostart disabled, no external bind mounts and networking removed before first boot. Docker and all five local application endpoints passed. External library recovery and indexer integration were outside this test.

**Arda:** Its new archive was restored to unused test VM 9105 on a separate local-lvm volume, with autostart disabled and its network interface removed before boot. MySQL/auth/world/timer health, all three database schemas and application listeners passed. The disk restore took approximately 19 minutes on this host.

Both test guests were normally shut down and removed; their temporary volumes were verified absent. Production guest definitions were never overwritten by a restore.

## Recovery material and limits

Selected identity, network, storage, backup, Samba and six-guest configuration checkpoints are retained privately, with a checksum-verified selected-config copy on the workstation. Consistent pmxcfs database checkpoints passed SQLite integrity checking. The prior API source/image and the deployed candidate are retained for rollback.

The old node directory was removed only after confirming that it held no guest definitions and after verifying the six new-node configs against their original hashes. Rollback must coordinate native identity, definition ownership and the API node reference; disk restoration is not part of an ordinary hostname rollback.

The complete guest archives and media/data still share the host's HDD/filesystem. Independent full-disk backups, the other four guest restore drills, a separate SQL-dump import, game-client recovery login and full external-media workflows remain outside this acceptance. Configured RAM is not measured consumption. No existing disk was reformatted and no SSH private key was copied.
