# Service Inventory

[Overview](../README.md) · [Architecture](architecture.md) · [Networking](networking.md) · [Troubleshooting](troubleshooting.md)

## Documented services

“Documented” means present in the existing project record, not independently health-checked during this documentation update.

| Service | Placement | Purpose | Status and limits |
| --- | --- | --- | --- |
| Proxmox VE | BASECAMP | Virtual machine and LXC hosting | Documented hypervisor; exact version and guest allocations not recorded |
| Docker Engine / Compose | core-services, Ubuntu Server 24.04 LTS VM | Containerized application stacks | Documented; sanitized stack definitions are not yet published |
| Pi-hole | LXC 101 | DNS filtering | Documented; resolver distribution and redundancy are not established |
| Open WebUI | Docker on core-services | Self-hosted AI web interface | Documented application; model backend, inference performance, and GPU use are not established |
| Homepage | Docker on core-services | Homelab dashboard | Documented; prior host-restriction troubleshooting is recorded at summary level |
| Uptime Kuma | Docker on core-services | Service availability monitoring | Documented; target coverage and alert delivery are not recorded |
| Beszel | Docker on core-services | Host/system monitoring | Documented; monitored inventory and agent placement need detail |
| Prometheus/Grafana-related components | core-services monitoring environment | Metrics collection and visualization experiments | Experimental; no complete production monitoring stack is claimed |
| Tailscale | Documented infrastructure and authorized endpoints | Remote connectivity and selected HTTPS access | Per-device installation details and policy validation remain private or undocumented |

Unnamed “supporting services” in the original notes are not expanded into invented inventory entries.

## Operational dependencies

The application services share core-services and BASECAMP. Pi-hole is outside the Docker VM but still shares the physical host. Monitoring located on the system it observes can disappear during that system's outage; the repository does not demonstrate an independent alerting path.

Availability checks should distinguish a running container from a usable application. Record both the service response and the relevant dependency when validating a change.

## Information to capture for each service

Before treating this repository as a reproducible operations guide, add a sanitized record of:

- Installed version and deployment method.
- Persistent data locations described by purpose, with sensitive paths omitted.
- Dependencies, intended access scope, and authentication requirements.
- Health-check method and expected result.
- Upgrade procedure, pre-change backup needs, and rollback method.
- Backup scope and a successful recovery test.
- A dated validation result and known limitations.

These are documentation requirements for future work, not claims that backup, rollback, or recovery has been tested.

## Change record convention

For a service change, record the reason, affected workload, prior state, action, validation, and rollback outcome. Update this inventory only after verifying the implementation. Keep credentials and private endpoints out of commits; see [security](security.md).
