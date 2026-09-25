# Basecamp Architecture

[Overview](../README.md) · [Diagram](../diagrams/basecamp-architecture.md) · [Networking](networking.md) · [Services](services.md)

## Scope and status

Basecamp is an early-stage, single-host homelab. Current implementation below reflects the existing repository baseline. Documentation review is not a live infrastructure audit; future work is labeled separately.

## Physical host

| Component | Documented configuration |
| --- | --- |
| Host | BASECAMP, running Proxmox VE |
| CPU | Intel Core i7-9700K, 8 cores / 8 threads |
| Memory | 32 GB DDR4 |
| Storage | 1 TB SSD and 4 TB HDD |
| GPU | NVIDIA GeForce RTX 3060, 12 GB VRAM |

The GPU is installed but is not assigned to a production workload. Storage pool layout, redundancy, guest resource allocations, and GPU passthrough are not documented as implemented.

## Workload boundaries

| Workload | Placement | Responsibility |
| --- | --- | --- |
| core-services | Ubuntu Server 24.04 LTS VM | Docker Engine and Docker Compose application stacks |
| Pi-hole | Dedicated Proxmox LXC 101 | Network-level DNS filtering |
| Applications and monitoring | Docker on core-services | Open WebUI, Homepage, Uptime Kuma, Beszel, and monitoring experiments |

The [service inventory](services.md) records each service's role and the evidence still needed.

## Decisions and tradeoffs

| Decision | Reason | Limitation |
| --- | --- | --- |
| Place application workloads in a VM | Separate application maintenance from the hypervisor | The VM still depends on BASECAMP |
| Run Pi-hole outside the Docker VM | Reduce coupling between DNS and application maintenance | Both guests share one physical host |
| Use Tailscale for remote access | Connect authorized devices without requiring public management endpoints | Actual access policy and exposure still need documented validation |
| Use multiple monitoring tools | Observe service availability and host health separately | Tool deployment alone does not demonstrate alert delivery or complete coverage |
| Grow incrementally | Introduce changes as requirements emerge | Reproducibility depends on continuing to record configuration and recovery steps |

## Dependencies and failure boundaries

A BASECAMP outage affects both the Docker VM and Pi-hole. A core-services outage affects its applications and any monitoring hosted there. Guest separation does not remove shared power, storage, or host dependencies. The gateway and network remain connectivity dependencies.

Pi-hole separation is not DNS redundancy. The repository does not demonstrate automatic failover, high availability, independent monitoring, or a tested recovery path.

## Planned architecture work

| Area | Evidence needed before marking complete |
| --- | --- |
| Backups and recovery | Backup scope, retention, and a successful restore exercise |
| Segmentation and managed switching | Implemented boundaries and allowed/denied path tests |
| Centralized storage | Storage design and recovery dependencies |
| UPS integration | Monitoring and graceful shutdown validation |
| Automation and configuration management | Sanitized, tested automation with rollback guidance |
| Security hardening | Recorded controls and validation results |
| Rack integration | Implemented physical layout |

See [security](security.md) for control gaps and [troubleshooting](troubleshooting.md) for the evidence format.

## Local AI dependency

Open WebUI on core-services connects to Ollama on the main Windows PC. This separates the application host from inference: a healthy WebUI does not guarantee that the inference PC is awake or reachable. The Basecamp RTX 3060 is not the documented inference device. Voice testing used an isolated development WebUI; its results should not be treated as a production upgrade.
