# Service inventory

[Overview](../README.md) · [Configuration](configuration.md) · [Operations](operations.md)

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
