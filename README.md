# Basecamp Homelab

A practical infrastructure portfolio documenting my Proxmox-based home lab: Linux administration, virtualization, Docker services, DNS filtering, monitoring, and remote access.

**Stage: early implementation and documentation.** This repository describes the existing lab and the reasoning behind its design. It is not yet a complete deployment or recovery package. Current-state statements reflect the documented baseline, not a live availability audit.

## Start here

| Document | What it covers |
| --- | --- |
| [Architecture](docs/architecture.md) | Hardware, workload boundaries, decisions, and failure dependencies |
| [Infrastructure diagram](diagrams/basecamp-architecture.md) | Logical placement and remote-access relationships |
| [Networking](docs/networking.md) | LAN, DNS, Tailscale, and validation gaps |
| [Services](docs/services.md) | Service roles, placement, and operational documentation |
| [Security](docs/security.md) | Documented controls, public-data handling, and planned hardening |
| [Troubleshooting](docs/troubleshooting.md) | Prior work, evidence limits, and a repeatable incident record |

## Current implementation

| Layer | Documented implementation |
| --- | --- |
| Compute | BASECAMP running Proxmox VE |
| Hardware | Intel Core i7-9700K; 32 GB DDR4; 1 TB SSD; 4 TB HDD |
| Application host | `core-services`, an Ubuntu Server 24.04 LTS VM running Docker and Docker Compose stacks |
| DNS | Pi-hole in dedicated Proxmox LXC 101 |
| Applications | Open WebUI and Homepage |
| Monitoring | Uptime Kuma, Beszel, and Prometheus/Grafana-related experiments |
| Remote access | Tailscale between authorized devices; selected services use Tailscale HTTPS endpoints |
| GPU | RTX 3060 with 12 GB VRAM installed; not assigned to a production workload |

The existing project record reports remote administration from Windows, a laptop, iPhone, iPad, and the Raspberry Pi-based Outpost workstation. It also records work on host updates, persistent addressing, Docker Compose, HTTPS access, and Homepage host restrictions. [Troubleshooting](docs/troubleshooting.md) separates these summaries from fully evidenced case studies.

## Engineering decisions

Application workloads live in a VM rather than being installed directly on the hypervisor. Pi-hole lives in a separate LXC so Docker-VM maintenance need not also stop DNS. Both guests still depend on the same physical host: this is **not a highly available design**.

Monitoring tools serve different purposes, but their presence does not establish complete alert coverage or an uptime guarantee. Open WebUI on Basecamp connects to Ollama on the main Windows PC. The owner confirms working local AI, image generation, voice, and purpose-built assistant profiles. Recovered project records also document tested live diagnostic tools. Basecamp GPU passthrough remains separate planned work; inference depends on the main PC.

## Planned work

- **Recovery:** automated backups and a documented restore exercise.
- **Network:** segmentation, VLANs, and managed switching.
- **Operations:** improved observability, tested automation, and configuration management.
- **Infrastructure:** centralized storage, UPS integration, and physical rack organization.
- **Security:** additional hardening with recorded validation.
- **Optional exploration:** GPU passthrough and accelerated workloads.

These are future directions from the project baseline, not completed capabilities or purchase commitments. Each should be marked complete only with implementation details and a sanitized validation record.

## Repository layout

```text
basecamp-homelab/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── networking.md
│   ├── services.md
│   ├── security.md
│   └── troubleshooting.md
└── diagrams/
    └── basecamp-architecture.md
```

## Documentation and privacy

Public documentation uses logical names and omits private addresses, tailnet identifiers, credentials, and sensitive configuration. No deployable configuration or automation is claimed until reviewed examples are actually added.

The baseline for this documentation is the original README, architecture notes, and infrastructure diagram. Git history preserves the initial work and subsequent cleanup. Future changes should update the affected document and diagram together, with a meaningful commit explaining the outcome.
