# Service inventory

[Overview](../README.md) · [Configuration](configuration.md) · [Operations](operations.md)

## Current infrastructure observation — October 6

Core-services remains VM 100 on Hornburg. The canonical monitoring audit confirms Kuma, Prometheus, Grafana, node exporter, Beszel hub and agent, all with `unless-stopped`, and enabled Docker. Later core inventory has twelve containers (the former eleven plus Varda); this is not a refreshed application/model inventory. Sentinel has independent Kuma, DNS and host-health; Elros has Windows exporter plus the lightweight Local Service observer. [Monitoring](monitoring.md) records the verified triangle and alert limits.

The table below describes the frozen V1 reference recipe and ports. Registry pins/container counts in that release are historical, not a complete current deployment inventory.

All eleven core containers were running with `unless-stopped` in the final capture. Ports below describe the reference recipe; access policy and bind interfaces are local inputs.

| Service | Port | Role/state |
| --- | --- | --- |
| Open WebUI | 3002 | AI interface; persisted application database |
| Open Terminal | 8000 | Execution capability; separate key and persistent home |
| Homepage | 3003 | Dashboard configuration and images |
| Homelab API | 8091 | Thirteen diagnostic/retrieval GET operations |
| Qdrant | 6333 | Vectors, text and provenance |
| Prometheus | 9090 | Metrics data and generated scrape configuration |
| Node Exporter | 9100 | Host metrics; host network/PID context |
| Grafana | 3000 | Dashboards and settings |
| Uptime Kuma | 3001 | Availability checks/settings |
| Beszel | 8090 | Monitoring hub and shared agent socket |
| Beszel Agent | Unix socket | Host monitoring and Docker access |

The separate `qwen3-embedding` container on ai-worker serves port 8080 and persists its model cache. It is outside the eleven-container core count. The ingestion watcher is a systemd unit, not a container.

Pi-hole runs in LXC 101; its recorded versions are core 6.4.3, web 6.6 and FTL 6.7.1. A local DNS query succeeded during packaging. This does not verify filtering or DHCP lease delivery for every client. QEMU Guest Agent is active and responsive on ai-worker.

Installed digests are in the [manifest](../release/manifest.json). Main-PC Ollama and ComfyUI are external dependencies documented in [Local AI Lab](https://github.com/soonerbear22-ux/local-ai-lab). Alert delivery and full voice recovery are outside V1 acceptance.

## Post-V1 operating record

See the [September 27 current state](current-state.md), [incident resolutions](changes/2026-09-27.md), and [Sentinel runbook](sentinel.md) for workstation naming, physical power work, independent DNS/monitoring, mobile access and backup validation. The V1 measurements above remain dated evidence. Sentinel backups to Basecamp do not establish off-host protection for Basecamp guest backups.

## Historical September 29 media addition (coverage superseded by current state)

[Jellyfin and media automation](jellyfin.md) add unprivileged guests 103 and 104. Today's read-only checks confirm Jellyfin health, five running media containers, and saved Radarr/Sonarr import/upgrade refresh hooks. The enabled backup job includes guest 103 but excludes guest 104; externally mounted library data needs separate protection. See the [dated evidence and remaining acceptance work](changes/2026-09-29.md). These services are outside the immutable V1 rebuild package and the core-only automatic inventory.


## October 3 Arda services

VM 105 `arda` is a dedicated AzerothCore WotLK guest outside the eleven-container core-services count.

Verified production service units:

- `mysql`
- `arda-auth.service`
- `arda-world.service`
- `arda-backup.timer`

Arda's game services are not Docker containers and should not be interpreted through the core-services container inventory. See the [Arda runbook](arda.md) for the documented worldserver logging workaround and backup behavior.
