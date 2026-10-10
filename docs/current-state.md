# Current state — October 10, 2026

[Overview](../README.md) · [Change and incident record](changes/2026-09-27.md) · [Sentinel](sentinel.md)

## Verified public projection — October 10, 2026

The latest saved private Homelab canonical package is authoritative; this is its sanitized public projection, not a fresh infrastructure audit. E10 monitoring observations were collected October 6; the recovered backup/storage evidence dates to October 5, Gwaihir to October 8, and endpoint/access checkpoints to October 10. This documentation update makes no runtime changes. Private addresses, identities, notification destinations and corpus content are excluded.

| Component | Current supported role/state | Limit |
| --- | --- | --- |
| Hornburg | Native Proxmox/Linux name `hornburg`; formerly Basecamp | Compatibility storage/share/API names remain; repository not renamed |
| Elros | Windows workstation display identity; native hostname Citadel; workstation workloads and host telemetry | No native Elros OS rename claimed |
| Sentinel | Independent Raspberry Pi, secondary Pi-hole/DNS, Kuma and self-contained host-health/status | Client DNS selection still matters; no dependency on Hornburg for local watcher health |
| Core monitoring | Kuma, Prometheus, Grafana, Beszel and agents in VM 100 | Monitoring guest shares Hornburg's failure domain |
| Monitoring triangle | All six directed peer relationships runtime-verified; Local Service observer on Elros | Reboot/device/full alert acceptance remains follow-up, not an implementation blocker |
| Backup policy | Enabled daily snapshot/zstd/keep-last=7 for 100–105 targeting `hornburg-backups`; October 4 TASK OK/all six operator-reported; six archives observed October 5 | Original task log and later complete set, retention/integrity and recovery remain separate |
| Backup storage | October 5 physical chain proves Seagate Expansion USB 2 TB-class ext4 backup disk separate from WD bulk storage | Same-host media is not off-host protection; dated device evidence needs current inspection before operations |
| Backup health | Deployed per-guest checker plus retained host check; syntax/service/JSON/HTTP/isolated fixtures passed; fresh corrected HTTP OK October 10 | Timer provenance, current source/set and Homepage tile/core-fetch acceptance remain open |
| Gwaihir | October 8 local SSH/dashboard active, dashboard enabled, listener 8088 and local HTTP 200 | Remote route, guest-query key authentication and full dashboard source correspondence unresolved |
| Beszel media coverage | October 10 hub/core agent healthy and media endpoints reachable | 103/104 registrations, agent metrics/startup/restart acceptance blocked by administrative/dashboard access (H17) |

### Hornburg guests

| ID / type | Native name / display role | vCPU / RAM | Root disk / storage | Infrastructure function |
| --- | --- | --- | --- | --- |
| 100 VM | core-services | 4 / 8 GiB | 100 GiB, local-lvm | Shared Docker applications and monitoring |
| 101 LXC | pihole | 1 / 1 GiB | 8 GiB, local-lvm | Primary DNS |
| 102 VM | ai-worker / Bombadil | 4 / 12 GiB | 100 GiB, local-lvm | GPU workload substrate |
| 103 LXC | jellyfin / Palantír | 2 / 2 GiB | 24 GiB, local-lvm | Media server; mounted library separate from root disk |
| 104 LXC | media-automation | 2 / 4 GiB | 16 GiB, local-lvm | Five media automation containers |
| 105 VM | arda / Arda | 4 / 8 GiB | 64 GiB, local-lvm | Dedicated Ubuntu 24.04 LTS application substrate |

All six were running in the October 3 canonical inventory; autostart and successful cutover reboot are recorded. E10 confirms live core monitoring and peer endpoint state; it does not re-audit every application. VM 105's newer local-lvm configuration supersedes old qcow2/bulk-storage notes. Core inventory later includes twelve containers (the prior eleven plus Varda); application details and Local AI lifecycle remain with their owning projects.

See [monitoring](monitoring.md) for the six directions and exact acceptance limits, [storage](storage.md) for persistence boundaries, and [backups](backup-recovery.md) for restore scope. H01/H02 narrow the dated disk/target and scheduled/archive portions; current retention/checkpoints, direct task/timer evidence and Homepage acceptance remain. Other work includes planned Prometheus restart, independent recovery, notification/device acceptance, UPS, media workflow and access policy. Local AI public synchronization completed at its October 6 owner checkpoint; runtime/ingestion remains owner work. The existing 44-test closeout toolkit is implemented; durable receipts, ownership routing and drift integration are the Software & Codex handoff. See the [dated reconciliation](changes/2026-10-10.md).

## Historical operating records through October 3

The following dated records are preserved for provenance. Their older backup-disk, container-count and workstation descriptions are superseded by the current projection above where they differ.

The sections below retain September 27 operating records, September 29 media checks, and October 3 maintenance history. The [October 3 final health sweep](homelab-health-sweep-2026-10-03.md) adds dated live checks, supplemented by local operator evidence for Gwaihir and Sentinel. See the [Jellyfin runbook](jellyfin.md) and [dated update](changes/2026-09-29.md). The immutable **v1.0.0** tag remains the September 26 reference package; its version manifest, validation evidence and release notes describe that freeze. Current documentation on main can advance independently.

| Area | Latest supported state | Evidence limit |
| --- | --- | --- |
| Hornburg | Native Linux/Proxmox rename completed; all six guests started automatically after the reboot; eleven core containers running after Prometheus recovery | [Completed rename and recovery record](hornburg-rename-preflight.md); service, DNS, share, certificate and API checks passed |
| Jellyfin / media automation | Guests 103 / 104 running; Jellyfin health passes; five media containers running; saved refresh triggers verified | Full request-to-playback acceptance remains outstanding; guest 104 now has a validated first archive and daily scheduled coverage |
| Arda | VM 105 hosts a private AzerothCore WotLK realm; autostart, MySQL/auth/world service health and daily local database/configuration backup automation were verified October 3 | Local SQL/archive integrity and isolated whole-VM restoration passed; separate SQL-dump import and game-client recovery login remain untested |
| Citadel | Main Windows workstation, renamed; hosts Ollama and ComfyUI | Chat and image generation still depend on this separate machine |
| Open WebUI | Runs on Basecamp; saved Ollama connection repaired after workstation changes | Six models and custom assistants returned; 99 chats and the account matched the pre-change backup |
| Sentinel | Independent Raspberry Pi running DNS, monitoring, private access and emergency status | Client DNS selection determines whether independent DNS helps each client |
| Physical installation | Gateway/modem, Basecamp, Sentinel and CyberPower moved from living room to closet; five labeled, verified cable runs | One demarcation-to-closet run via attic, four Cat6 runs from closet to Citadel's bedroom; first run's medium unspecified; JDSU testing and 1,000 Mbps link rate confirmed by operator |
| Remote administration | Samsung and iPad key-based SSH tested; Samsung also has a separate Termux path | Successful tested paths are not a complete access-policy audit |
| Sentinel backups | Scheduled backups to Basecamp with retention and staged integrity/restore checks | This is not an off-host backup of Basecamp itself or a bare-metal Sentinel restore |

## Remaining acceptance work

- Preserve cable-label/termination mapping privately and confirm battery-backed outlet assignments. All five runs were labeled and operator-verified with a JDSU, with a confirmed 1,000 Mbps link rate. Formal certification level and measured application throughput were not supplied.
- Confirm UPS USB telemetry on Basecamp before configuring or claiming NUT-driven shutdown. Do not cut power as an informal test.
- Verify independent copies and the remaining four guest restores; isolated restores of 104/105 passed. That was the historical shared-disk layout; October 5 inspection proves a separate attached backup disk, still without off-host recovery acceptance.
- Configure and test independent alert delivery. Local monitoring and status pages do not prove phone notifications work.
- Revalidate full voice recovery separately. Prior voice use is not a current end-to-end acceptance test.

The [automatic inventory process](documentation-sync.md) covers a deliberately narrow set of core container facts. It cannot infer equipment moves, root causes, or user-visible acceptance from a container inventory.


## October 3 completed Hornburg rename and backup coverage

The daily Proxmox job now includes all six guests, 100–105. New full archives for 104 and 105 passed compression integrity testing; Arda's archive also passed VMA block verification. The live six-guest audit and semantic retrieval remained healthy after these backups.

Selected configuration rollback material is retained on the host and as a checksum-verified copy on Elros. A consistent pmxcfs database checkpoint passed integrity checking. Isolated recovery passed for media automation and Arda, and both test guests/volumes were removed. During the isolated drills the six production guests stayed running. Their config hashes also remained unchanged through the subsequent approved rename; daily six-guest backups are re-enabled. The final live API audit retrieved all seven components and confirmed operational semantic retrieval.

The native node is now `hornburg` / `hornburg.home`. After the selected restores passed, the approved guest shutdown and rename were completed, and the operator issued the host reboot through Termius. All six guests started automatically. The Hornburg API candidate is deployed; the final audit found all six guests and eleven core containers running. Prometheus required a manual start and all four targets are now up; the missed automatic restart remains a follow-up. DNS, mapped shares, media services, Arda, certificate validation and semantic retrieval passed. Samba's BASECAMP identity/share, the old Tailscale name, storage IDs and API route names remain for compatibility. See the [completed cutover and recovery record](hornburg-rename-preflight.md).


## October 3 final health sweep

Live checks collected at 15:07-15:23 UTC, local operator checks at approximately 15:39-15:40 UTC, and approved cleanup verification at 16:35-16:38 UTC passed for all six guests, storage, core services, monitoring, DNS, Sentinel, Palantir/Jellyfin, media automation, Arda, knowledge retrieval, Gwaihir and Elros. The [full dated record](homelab-health-sweep-2026-10-03.md) gives PASS/WARNING results and exact evidence for each component.

Hornburg's OpenIPMI startup failure was traced to no discovered local IPMI system interface. After explicit approval, only its boot entry was disabled and the failed state cleared. Zero failed host units, active Proxmox/HA units, the live Software Watchdog, all six running guests and a complete seven-component API audit were verified afterward. No reboot or service stop occurred.

The next automatic six-guest Proxmox backup after cutover has not yet been observed; its next run is October 4 00:00 CDT (05:00 UTC). Prometheus is ready with all four targets up, but its single earlier missed automatic restart remains unexplained. Do not change it unless the issue reproduces. Compatibility names in Tailscale, Samba, storage IDs, API routes, paths and monitoring labels intentionally remain where integrations require them.

The immutable V1 package and its evidence remain historical. Health/reachability checks do not establish new restore, playback, client-login, voice/streaming or independent alert-delivery acceptance.
