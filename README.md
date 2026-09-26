# Basecamp Homelab

A Proxmox-based infrastructure lab built and operated by Logan: Linux guests, Docker services, DNS filtering, GPU-backed embeddings, semantic knowledge retrieval, monitoring, and private remote access.

**Updated September 26, 2026.** A live audit at 21:42 UTC retrieved all seven component groups, reported all three expected guests running, and found all eleven expected core-services containers running. These are dated observations, not an uptime guarantee.

## Current implementation

| Layer | Implemented |
| --- | --- |
| Physical host | Intel Core i7-9700K, 32 GB RAM, 1 TB SSD, 4 TB HDD |
| VM 100 — core-services | 8 GB allocated RAM, 100 GB virtual system disk; Docker applications and knowledge infrastructure |
| LXC 101 — Pi-hole | Separate DNS filtering guest |
| VM 102 — ai-worker | 12 GB allocated RAM, 100 GB virtual system disk; RTX 3060 12 GB passed through for Qwen3-Embedding-4B |
| Applications | Open WebUI, Open Terminal, Homepage, Homelab API |
| Knowledge | Samba inbox, systemd ingestion watcher, GPU embeddings, Qdrant, semantic search API |
| Monitoring | Prometheus, Node Exporter, Grafana, Uptime Kuma, Beszel and its agent |
| Backups | Inspected daily snapshot job covers VM 100 and LXC 101, with retention set to the last seven backups |
| Remote access | Tailscale and selected private HTTPS routes |

Ollama chat inference and ComfyUI image generation run on the main Windows PC. Basecamp's GPU serves the separate embedding workload.

## Documentation

| Document | Purpose |
| --- | --- |
| [Architecture](docs/architecture.md) · [diagram](diagrams/basecamp-architecture.md) | Placement, dependencies, and GPU role |
| [Services](docs/services.md) | Current service inventory and evidence limits |
| [Networking](docs/networking.md) | Connectivity and private access boundaries |
| [Storage](docs/storage.md) · [backup and recovery](docs/backup-recovery.md) | Persistence, scheduled coverage, shared failure domains |
| [Knowledge pipeline](docs/knowledge-pipeline.md) | Ingestion, retrieval, and the current corpus discrepancy |
| [September 26 validation](docs/validation-2026-09-26.md) | Dated evidence and unresolved observations |
| [Security](docs/security.md) · [troubleshooting](docs/troubleshooting.md) | Privilege boundaries and incident lessons |

## Related projects

- [Local AI Lab](https://github.com/soonerbear22-ux/local-ai-lab): Ollama, Open WebUI, ComfyUI/FLUX, voice history, assistant profiles, and knowledge retrieval.
- [Homelab API](https://github.com/soonerbear22-ux/homelab-api): thirteen OpenAPI operations, sanitized source, and mocked regression tests.

## Current limits and next work

GPU passthrough, embeddings, and scheduled guest backups are implemented. The inspected backup job does not cover ai-worker; off-host copies and isolated restores remain unverified. Two Proxmox storage names share one physical disk.

The morning knowledge expansion passed its checks, but the later live index contains only the two baseline sources. Reconcile that discrepancy before claiming the added runbooks remain searchable. Current voice recovery, full-topology reboot recovery, monitoring alert delivery, VLANs, UPS integration, and complete deployment reproduction remain follow-up work.

Public files omit private addresses, tailnet names, credentials, raw telemetry, and private knowledge content. Updates preserve Git history and separate historical tests from current observations.
