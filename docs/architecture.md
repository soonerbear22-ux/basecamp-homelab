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

## Post-V1 operating record

See the [September 27 current state](current-state.md), [incident resolutions](changes/2026-09-27.md), and [Sentinel runbook](sentinel.md) for workstation naming, physical power work, independent DNS/monitoring, mobile access and backup validation. The V1 measurements above remain dated evidence. Sentinel backups to Basecamp do not establish off-host protection for Basecamp guest backups.

## September 29 media addition

[Jellyfin and media automation](jellyfin.md) add unprivileged guests 103 and 104. Today's read-only checks confirm Jellyfin health, five running media containers, and saved Radarr/Sonarr import/upgrade refresh hooks. The enabled backup job includes guest 103 but excludes guest 104; externally mounted library data needs separate protection. See the [dated evidence and remaining acceptance work](changes/2026-09-29.md). These services are outside the immutable V1 rebuild package and the core-only automatic inventory.


## October 3 current topology additions

Current role names used operationally are:

- Proxmox host role: **Hornburg**; the underlying host OS hostname remains `basecamp`.
- Main Windows workstation role: **Elros**; historical documentation may still refer to Citadel.
- VM 102 AI worker role: **Bombadil**; the guest remains the dedicated embedding worker.
- VM 105 **Arda** hosts the private AzerothCore WotLK realm.

Arda is a dedicated 4-vCPU / 8 GiB VM with autostart enabled. Its MySQL, authentication and world services are separate from the core-services Docker stack. Arda uses its own daily in-guest database/configuration backup timer and is also included in the daily Proxmox backup job covering guests 100-105.

These names are presentation/role names. Where operating-system hostnames differ, live hostnames should be preserved until a deliberate rename is completed and verified.
