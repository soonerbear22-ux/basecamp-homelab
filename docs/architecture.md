# Basecamp Architecture

## Overview

Basecamp is a Proxmox VE virtualization host that provides the core compute platform for my homelab.

The architecture separates the physical hypervisor from application workloads by running services inside virtual machines and containers rather than directly on the Proxmox host.

This design allows individual workloads to be maintained, restarted, backed up, modified, or replaced without treating the physical host as a single monolithic server.

## Physical Architecture

### Basecamp

**Role:** Proxmox VE Hypervisor

Hardware:

- Intel Core i7-9700K
- 32 GB DDR4 RAM
- NVIDIA GeForce RTX 3060 12 GB
- 1 TB SSD
- 4 TB HDD

The physical host runs Proxmox VE and provides compute resources to virtualized workloads.

The RTX 3060 is currently installed but is not assigned to a production workload.

## Virtualized Infrastructure

### core-services

**Type:** Virtual Machine  
**Operating System:** Ubuntu Server 24.04 LTS  
**Primary Role:** Docker application host

The `core-services` VM provides an isolated Linux environment for containerized applications.

Docker services currently include:

- Open WebUI
- Homepage
- Uptime Kuma
- Beszel
- Monitoring components
- Supporting homelab services

Application workloads are intentionally kept off the Proxmox host whenever practical.

### LXC 101

**Type:** Linux Container  
**Primary Role:** DNS filtering

LXC 101 hosts Pi-hole, which provides network-level DNS filtering.

Running Pi-hole separately from the main Docker host reduces dependency between DNS infrastructure and application services.

## Network Architecture

Basecamp participates in both the local home network and a Tailscale overlay network.

The local network provides normal LAN connectivity between infrastructure and client devices.

Tailscale provides authenticated remote connectivity between authorized devices without requiring homelab management interfaces to be directly exposed to the public internet.

Connected systems include:

- Basecamp
- core-services
- Outpost
- Windows workstation
- Mobile devices
- Other authorized endpoints

## Design Principles

The Basecamp architecture is being developed around several principles:

1. **Separation of responsibilities**  
   Hypervisor, application, and DNS workloads are separated where practical.

2. **Remote manageability**  
   Infrastructure should remain securely accessible from authorized devices when away from the local network.

3. **Observability**  
   Service and host health should be measurable rather than assumed.

4. **Recoverability**  
   Future development will include automated backups and documented recovery procedures.

5. **Incremental improvement**  
   New technologies are introduced when they solve an actual problem or provide useful hands-on experience.

6. **Documentation**  
   Architecture decisions, troubleshooting, and major configuration changes are documented so the environment can be understood and reproduced.

## Future Architecture Work

Planned improvements include:

- Backup and restore infrastructure
- VLAN-based network segmentation
- Managed switching
- Centralized storage
- UPS monitoring and graceful shutdown
- Infrastructure automation
- Configuration management
- Additional security hardening
- Physical rack integration
