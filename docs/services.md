# Service inventory

[Overview](../README.md) · [Architecture](architecture.md)

The September 26 live audit reported all eleven expected core-services containers running. Container state alone does not establish every feature's health.

| Service | Placement | Role and evidence |
| --- | --- | --- |
| Proxmox | Basecamp | API status, guest inventory, and storage reads succeeded |
| Pi-hole | LXC 101 | DNS guest running; morning record confirmed DNS service active |
| Open WebUI | core-services | AI interface; prior owner-confirmed chat/image integrations |
| Open Terminal | core-services | Separate execution capability for selected assistants |
| Homelab API | core-services | Thirteen GET operations covering diagnostics, retrieval, and infrastructure audit |
| Qdrant | core-services | Green; 2560-dimensional Cosine collection; live source inventory checked |
| Homepage | core-services | Dashboard container running |
| Prometheus / Node Exporter / Grafana | core-services | Established metrics collection and visualization stack |
| Uptime Kuma | core-services | Availability monitoring; alert delivery coverage unverified |
| Beszel / Beszel Agent | core-services | System monitoring; full monitored-host inventory not audited here |
| Qwen3-Embedding-4B / TEI | ai-worker | Real embedding request succeeded with 2560 dimensions |
| Ollama | Main Windows PC | Owner-confirmed chat backend; current preference recorded as local tag `qwen3.6:35b` |
| ComfyUI / FLUX | Main Windows PC | Saved workflows, installed model files, and successful-generation logs inspected |
| Kokoro / Faster-Whisper | Main Windows PC, historical voice setup | Kokoro observed running in the morning; full current voice path and startup remain unverified |

The eleven-container count includes the separate monitoring components and excludes services outside core-services. The ingestion watcher is a systemd unit, not another Docker container.

VM 100, VM 102, and LXC 101 had onboot enabled in the morning audit. Eight inspected application containers used `unless-stopped`. Those settings do not prove a successful recovery of the current topology.

Version tags such as `main` and `latest` do not establish that installed images are current upstream. Secrets and deployment-specific configuration remain outside this repository.
