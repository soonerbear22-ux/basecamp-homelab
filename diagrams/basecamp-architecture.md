# Basecamp infrastructure diagram

[Overview](../README.md) · [Architecture](../docs/architecture.md)

Logical deployment as reviewed September 26, 2026. Lines express dependencies, not firewall policy or physical cabling.

```mermaid
flowchart TB
    Clients["Authorized clients"] --> Access["Private Tailscale access"]
    Access --> WebUI
    Access --> Dashboard
    subgraph Basecamp["BASECAMP - Proxmox"]
        subgraph Core["VM 100 - core-services"]
            WebUI["Open WebUI"]
            Terminal["Open Terminal"]
            Dashboard["Homepage"]
            API["Homelab API - 13 operations"]
            Monitor["Prometheus / Grafana / Kuma / Beszel"]
            Inbox["Samba knowledge inbox"]
            Ingest["systemd ingestion"]
            Qdrant["Qdrant"]
            Inbox --> Ingest
            WebUI --> API
            WebUI --> Terminal
            API --> Qdrant
            API --> Monitor
            Ingest --> Qdrant
        end
        subgraph Worker["VM 102 - ai-worker"]
            GPU["RTX 3060 passthrough"]
            Embed["Qwen3-Embedding-4B / TEI"]
            GPU --- Embed
        end
        DNS["LXC 101 - Pi-hole"]
        Backup["Daily backups: VM 100 and LXC 101"]
        Disk["Large HDD - shared storage and backup filesystem"]
        Backup --> Disk
        API --> Embed
        Ingest --> Embed
    end
    subgraph PC["Main Windows PC"]
        Ollama["Ollama chat inference"]
        Comfy["ComfyUI / FLUX image generation"]
    end
    WebUI --> Ollama
    WebUI --> Comfy
    Clients --> Inbox
```

The Basecamp GPU now serves embeddings. Voice is omitted from the current deployment diagram because its earlier test environment has not been revalidated. ai-worker is absent from the inspected backup job. No addresses, credentials, or private service URLs are shown.
