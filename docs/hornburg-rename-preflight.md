# Hornburg rename preflight — October 3, 2026

[Current state](current-state.md) · [Backup and recovery](backup-recovery.md)

## Execution status

Target role/name: Hornburg. The actual Linux/Proxmox node is still `basecamp`, with FQDN `basecamp.home`. No hostname, node configuration ownership, Tailscale identity, Samba identity, guest name, storage path, or IP was changed during this preflight. No reboot or guest shutdown was performed.

A native node rename is not cleared for automatic execution. The official [Proxmox rename page](https://pve.proxmox.com/wiki/Renaming_a_PVE_node) specifies an empty node. This host is populated. [Proxmox staff guidance](https://forum.proxmox.com/threads/changing-hostname-and-ip-of-non-empty-pve-host.112068/) also describes configuration preservation, guest-config moves, and reboot considerations. This is a maintenance procedure requiring an explicit outage boundary and a validated recovery path, not a display-label edit.

## Verified host and guest baseline

Standalone Proxmox host: one node directory, no Corosync configuration, Proxmox manager 9.2.20, kernel 7.0.14-19-pve, Intel i7-9700K, approximately 32 GB RAM. All six guests were running and configured for autostart.

| ID | Type | Live name | Configured RAM | Root disk |
| --- | --- | --- | --- | --- |
| 100 | QEMU VM | core-services | 8 GiB | 100 GiB, local-lvm |
| 101 | LXC | pihole | 1 GiB | 8 GiB, local-lvm |
| 102 | QEMU VM | ai-worker | 12 GiB | 100 GiB, local-lvm; GPU passthrough |
| 103 | LXC | jellyfin | 2 GiB | 24 GiB, local-lvm |
| 104 | LXC | media-automation | 4 GiB | 16 GiB, local-lvm |
| 105 | QEMU VM | arda | 8 GiB | 64 GiB, basecamp-storage |

Configured RAM is not measured consumption. Guest 103 and 104 external bind mounts are not included in their rootfs archives. Their media/data directories require separate protection.

## Dependencies and preservation plan

| Dependency | Verified state | Requirement for a native rename |
| --- | --- | --- |
| Proxmox guest ownership | Six configs under the existing node directory | Preserve all IDs/configs; use the appropriate pmxcfs guest-config move procedure with guests stopped |
| Homelab API | Live `PVE_NODE` is hard-coded to `basecamp` | Update the node reference in coordination with the native change, then repeat the full six-guest audit |
| Proxmox TLS | Current certificate names the old short name and FQDN | Regenerate/validate the node certificate and check clients' trust/URLs |
| Tailscale | Existing device advertises the old name | Preserve its registration/IP; keep the legacy name during initial recovery, then migrate client references deliberately |
| Samba | Effective NetBIOS name is BASECAMP, inherited from the hostname; share is Basecamp | Preserve the existing share/path and pin a compatibility identity before the native hostname changes |
| Elros mapped drive | Existing Basecamp share works through an IP-based mapping | Keep the share name, address and underlying paths |
| Windows SSH | Existing alias points to the node's overlay IP; strict checking succeeds by IP | Preserve public host identity, authorized keys and existing client aliases |
| Storage | Existing storage IDs and mounts contain the old name; no node restriction was observed | Keep `basecamp-storage`, `basecamp-backups` and their physical paths |
| Prometheus | Existing job label is `basecamp` | Preserve label continuity and IP target; change display labels separately |
| Homepage / Uptime Kuma | Node and backup-health targets use IP addresses | Keep working endpoints; update titles after technical verification |
| DNS continuity | Independent Sentinel DNS answered a direct query | Verify affected clients actually use a working fallback before planned Pi-hole downtime |
| Backup health | Existing page checks the newest guest archive and newest host archive | Do not treat its OK status as proof of per-guest coverage |

## Backup changes completed

The enabled daily Proxmox backup job was expanded from guests 100–103 to all six guests, 100–105. Snapshot mode, compression, schedule, storage, and retention were preserved.

First full backups of guests 104 and 105 completed successfully. Both passed Zstandard integrity tests. Guest 104 archive structure contains the rootfs and media-stack configuration. Arda's archive also passed the VMA internal block-integrity check.

All six guests have an observed archive and matching successful completion log. Only the two new archives received integrity testing in this session. No isolated restoration drill has been completed.

Selected host identity, network, storage, backup-job, Samba, and all six guest configuration files were preserved in a protected checkpoint. A checksum-verified copy is also on Elros. This is an off-host configuration checkpoint, not an off-host copy of every guest archive or a complete bare-metal backup.

## Proposed maintenance sequence — approval and recovery gates

1. Recheck active backup tasks, config hashes, available capacity and all six guests. Validate the chosen recovery path in isolation and make a local console available.
2. Confirm independent administration by IP and DNS continuity. Prepare compatibility settings for legacy Tailscale/SMB/client references.
3. Preserve updated configs and evidence. Gracefully stop guests during an agreed maintenance window, checking service/player impact first.
4. Apply the Proxmox node-identity and guest-config migration procedure. Preserve disks, IDs, mounts, permissions and SSH keys. Handle the TLS certificate and reboot as required.
5. Recover the host by its existing IP. Verify storage, networking, node ownership and all six guests. Bring services back in dependency order; validate Pi-hole, core services, embeddings, media services and Arda.
6. Coordinate the API node reference and validate health, discovery, seven-component audit and semantic retrieval. Check monitoring, shares, client access and guest/application logs.
7. Update client-facing names and documentation incrementally after technical verification. Retain rollback material and legacy compatibility until acceptance is complete.

Rollback must restore the old identity and config ownership coherently; a partial reversal can strand guest definitions. Disk restoration is a separate recovery action and is not part of an ordinary hostname rollback.

## Acceptance limits

The native rename has not been executed or rehearsed against this populated host. Archive integrity is not proof of successful restoration. Sentinel's direct DNS response is not proof that every client will automatically fail over. No zero-risk or zero-downtime guarantee is made.
