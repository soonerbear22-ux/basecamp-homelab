# Architecture

[Overview](../README.md) · [Diagram](../diagrams/basecamp-architecture.md) · [Rebuild](rebuild.md)

Basecamp V1 separates application services, DNS, and GPU embeddings across three guests on one Proxmox host. Installed versions and immutable image references are in the [manifest](../release/manifest.json).

| Location | Responsibility | Dependency |
| --- | --- | --- |
| Proxmox host | Guest lifecycle, storage, scheduled backups | Physical host, SSD and bulk HDD |
| VM 100 core-services | Interfaces, monitoring, API, Qdrant, ingestion, Samba inbox | Guest disk and network; ai-worker for embeddings |
| LXC 101 Pi-hole | DNS filtering and site-specific DHCP | Host and LAN; independent of the application VM |
| VM 102 ai-worker | Qwen/Qwen3-Embedding-4B through TEI, float16, 2560 dimensions | Passed-through RTX 3060, driver, container runtime, model cache |
| Main PC | Ollama response generation and ComfyUI images | Separate Windows runtime and models |

The capture records pve-manager 9.2.20, Ubuntu 24.04.5 LTS on core-services, Docker 29.8.1 and Compose 5.5.1. These are observed versions, not claims about the newest upstream releases.

## Data flow and boundaries

The authenticated Samba inbox feeds a systemd watcher and a locked ingestion process. Text extraction and chunking run on core-services; ai-worker generates vectors. Qdrant persists vectors and source metadata. The API embeds queries and returns scored chunks to its clients, including Open WebUI tools.

The API also reads Docker, Prometheus, Proxmox, and embedding health. Its full audit collects seven component groups independently. Successful collection is different from every component being healthy.

Pi-hole is separate from Docker maintenance, but all guests share a physical host. Monitoring observes infrastructure on which it also depends. Backup and bulk storage share one HDD. This is not host-level high availability.

Chat and images depend on the main PC; embeddings depend on the Basecamp GPU. A responsive WebUI proves neither backend is available. Recovery follows dependency order.

## Public adaptations

The live installation uses several Compose projects. The public recipe consolidates core services under `basecamp-v1`, preserves service names/data paths, adds digest pins and explicit bindings, and supplies site settings through environment variables. The API uses its published certificate-verifying source. A dedicated `basecamp` ingestion account replaces a personal account. Production was not migrated during packaging.
