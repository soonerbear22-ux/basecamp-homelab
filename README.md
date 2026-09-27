# Basecamp Homelab — V1

A working infrastructure lab built and operated by Logan: Proxmox virtualization, Linux services, DNS, GPU embeddings, a searchable operations knowledge base, observability, and private remote access.

**V1 freezes the completed September 26, 2026 baseline.** A final read-only capture at **01:13 UTC on September 27** confirmed three running guests, eleven running core-services containers, thirteen documented API operations, a complete seven-component audit, and a healthy knowledge pipeline. The completion session recorded recovery after a real host reboot and automatic ingestion through a single-instance lock.

## Engineering focus

- Separate application, DNS, and GPU workloads with explicit dependencies and persistence boundaries.
- Run GPU embeddings on Basecamp while the main PC handles chat and images.
- Ingest documents automatically and return source-aware semantic search through a diagnostic API.
- Diagnose ambiguous metrics using guest evidence, preserve partial audit results, and verify recovery beyond container startup.
- Freeze working versions and document rebuild, backup, rollback, and private configuration boundaries.

## V1 deployment

| Component | Frozen role |
| --- | --- |
| Basecamp | Proxmox; i7-9700K, 32 GB RAM, 1 TB SSD, 4 TB HDD |
| VM 100 — core-services | 4 cores, 8 GiB RAM, 100 GiB disk; eleven Docker services and ingestion |
| LXC 101 — Pi-hole | Unprivileged Debian; 1 core, 1 GiB RAM, 8 GiB root filesystem; DNS and site-configured DHCP |
| VM 102 — ai-worker | 4 cores, 12 GiB RAM, 100 GiB disk; RTX 3060 12 GB, Qwen3-Embedding-4B, 2560 dimensions |
| Main Windows PC | External dependency for Ollama chat and ComfyUI images |
| Backups | Daily snapshot job, Zstandard compression, last seven archives retained for guests 100, 101, 102 |

All guests have autostart enabled; all eleven core containers use `unless-stopped`. The index contains **34 distinct sources / 244 points**, including retained validation documents. These are dated measurements, not uptime or corpus-quality guarantees.

## Reproduce and operate

Start with the [V1 rebuild guide](docs/rebuild.md). The package includes [core Compose](deploy/core-services/compose.yaml), [worker Compose](deploy/ai-worker/compose.yaml), a [version manifest](release/manifest.json), [local configuration template](config/site.env.example), [ingestion source](knowledge/ingest.py), systemd units, synthetic retrieval content, regression tests, and a runtime verifier.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-validation.txt
python scripts/fetch_api.py
python scripts/validate_repository.py --history
python -m pytest -q tests vendor/homelab-api/tests
```

These commands validate the public package without deploying services. Deployment steps target a fresh, isolated environment.

## Documentation

| Read this | To understand |
| --- | --- |
| [Architecture](docs/architecture.md) · [diagram](diagrams/basecamp-architecture.md) | Placement and dependencies |
| [Rebuild](docs/rebuild.md) · [configuration](docs/configuration.md) | Reproduction inputs and version pins |
| [Operations](docs/operations.md) · [troubleshooting](docs/troubleshooting.md) | Acceptance, maintenance, and failure modes |
| [Services](docs/services.md) · [networking](docs/networking.md) | Roles, ports, and access paths |
| [Knowledge](docs/knowledge-pipeline.md) | Extraction, locking, embeddings, and retrieval |
| [Storage](docs/storage.md) · [backup and recovery](docs/backup-recovery.md) | Persistence and final backup coverage |
| [Security](docs/security.md) | Trust boundaries and publication rules |
| [V1 validation](docs/validation-v1.md) · [release notes](release/NOTES-v1.0.0.md) | Results and remaining limits |

## Scope and limits

This is a reproducible reference package with documented manual provisioning and site inputs. A clean-room rebuild has not been performed. Operators supply their own private databases, corpus, credentials, device identities and dashboards.

Guest archives exist for all three guests; independent off-host copies and an isolated restore drill remain unverified. Bulk storage and backups share one disk. VLANs, UPS integration, alert delivery, and the full current voice path are outside V1 acceptance. The public API trust configuration and consolidated Compose layout were validated as release artifacts, not deployed over the frozen lab.

Related projects: [Homelab API](https://github.com/soonerbear22-ux/homelab-api) and [Local AI Lab](https://github.com/soonerbear22-ux/local-ai-lab).
