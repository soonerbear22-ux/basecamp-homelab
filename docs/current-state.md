# Current state — October 3, 2026

[Overview](../README.md) · [Change and incident record](changes/2026-09-27.md) · [Sentinel](sentinel.md)

This combines September 27 operating records, September 29 media checks, and October 3 Arda/knowledge-pipeline maintenance. See the [Jellyfin runbook](jellyfin.md) and [dated update](changes/2026-09-29.md). It is not a new simultaneous health check of every device. The immutable **v1.0.0** tag remains the September 26 reference package; its version manifest, validation evidence and release notes describe that freeze. Current documentation on main can advance independently.

| Area | Latest supported state | Evidence limit |
| --- | --- | --- |
| Basecamp | Five running guests: two VMs and three LXCs; Jellyfin and media automation extend the original three workloads | V1 reboot acceptance still covers the original baseline |
| Jellyfin / media automation | Guests 103 / 104 running; Jellyfin health passes; five media containers running; saved refresh triggers verified | Full request-to-playback acceptance and guest-104 scheduled backup coverage remain outstanding |
| Arda | VM 105 hosts a private AzerothCore WotLK realm; autostart, MySQL/auth/world service health and daily local database/configuration backup automation were verified October 3 | Local backup integrity was tested; an isolated database restore drill remains separate work |
| Citadel | Main Windows workstation, renamed; hosts Ollama and ComfyUI | Chat and image generation still depend on this separate machine |
| Open WebUI | Runs on Basecamp; saved Ollama connection repaired after workstation changes | Six models and custom assistants returned; 99 chats and the account matched the pre-change backup |
| Sentinel | Independent Raspberry Pi running DNS, monitoring, private access and emergency status | Client DNS selection determines whether independent DNS helps each client |
| Physical installation | Gateway/modem, Basecamp, Sentinel and CyberPower moved from living room to closet; five labeled, verified cable runs | One demarcation-to-closet run via attic, four Cat6 runs from closet to Citadel's bedroom; first run's medium unspecified; JDSU testing and 1,000 Mbps link rate confirmed by operator |
| Remote administration | Samsung and iPad key-based SSH tested; Samsung also has a separate Termux path | Successful tested paths are not a complete access-policy audit |
| Sentinel backups | Scheduled backups to Basecamp with retention and staged integrity/restore checks | This is not an off-host backup of Basecamp itself or a bare-metal Sentinel restore |

## Remaining acceptance work

- Preserve cable-label/termination mapping privately and confirm battery-backed outlet assignments. All five runs were labeled and operator-verified with a JDSU, with a confirmed 1,000 Mbps link rate. Formal certification level and measured application throughput were not supplied.
- Confirm UPS USB telemetry on Basecamp before configuring or claiming NUT-driven shutdown. Do not cut power as an informal test.
- Verify an independent copy and isolated restore of Basecamp guest backups; bulk data and guest archives still share a disk.
- Configure and test independent alert delivery. Local monitoring and status pages do not prove phone notifications work.
- Revalidate full voice recovery separately. Prior voice use is not a current end-to-end acceptance test.

The [automatic inventory process](documentation-sync.md) covers a deliberately narrow set of core container facts. It cannot infer equipment moves, root causes, or user-visible acceptance from a container inventory.
