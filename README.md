# Basecamp Homelab

Basecamp is my self-hosted homelab built to develop hands-on experience with virtualization, Linux administration, containerized services, networking, monitoring, DNS, secure remote access, and local AI infrastructure.

Rather than building the environment as a single finished system, I have expanded it incrementally as new requirements and projects have emerged. The lab serves both as production infrastructure for my home environment and as a platform for learning, testing, troubleshooting, and systems integration.

## Current Architecture

Basecamp is a dedicated Proxmox VE virtualization host.

### Physical Host

- Intel Core i7-9700K — 8 cores / 8 threads
- 32 GB DDR4 memory
- NVIDIA GeForce RTX 3060 — 12 GB VRAM
- 1 TB SSD
- 4 TB HDD
- Proxmox VE hypervisor

The RTX 3060 is currently installed but is not assigned to a production workload. Future GPU passthrough, AI, or other accelerated workloads may be explored as the lab evolves.

## Virtualization

### `core-services`

Ubuntu Server 24.04 LTS virtual machine used as the primary Docker application host.

Current services include:

- Docker Engine
- Open WebUI
- Homepage
- Uptime Kuma
- Beszel monitoring
- Prometheus/Grafana-related monitoring components
- Additional internal homelab services

### LXC 101 — Pi-hole

Pi-hole runs in a dedicated Proxmox LXC container and provides network-level DNS filtering for the home network.

## Networking & Remote Access

The homelab uses both the local network and a Tailscale overlay network.

Tailscale provides secure remote connectivity between authorized devices without directly exposing homelab management services to the public internet.

Remote administration has been tested from multiple device types, including:

- Windows workstation
- Laptop
- iPhone
- iPad
- Raspberry Pi-based Outpost workstation

Selected services are available through Tailscale HTTPS endpoints, allowing the same service addresses to be used both at home and remotely.

## Monitoring

The environment includes multiple monitoring tools serving different purposes:

- **Uptime Kuma** — service availability monitoring
- **Beszel** — lightweight host and system monitoring
- **Prometheus/Grafana components** — metrics collection and visualization experiments

Monitoring has been used not only for dashboards but also to validate service health during configuration changes and troubleshooting.

## Problems Solved

Building Basecamp has required troubleshooting across multiple layers of the infrastructure stack.

Examples include:

- Configuring Proxmox repositories and completing host updates
- Deploying and managing Docker Compose application stacks
- Configuring persistent network addressing
- Deploying Pi-hole in an LXC container
- Establishing Tailscale connectivity between physical hosts, virtual machines, Raspberry Pis, mobile devices, and workstations
- Converting LAN-only services to securely accessible remote services
- Configuring HTTPS access for internal applications
- Resolving host restrictions affecting Homepage access
- Validating service availability with command-line network testing
- Implementing system and service monitoring
- Troubleshooting container health and application configuration

## Skills Demonstrated

This project currently demonstrates hands-on experience with:

- Proxmox VE
- Linux administration
- Ubuntu Server
- Virtual machines and LXC containers
- Docker and Docker Compose
- TCP/IP networking
- DNS
- SSH
- Tailscale
- Reverse proxy / HTTPS service access
- Service monitoring
- Infrastructure troubleshooting
- Raspberry Pi integration
- Self-hosted applications

## Project Goals

Basecamp continues to serve as a platform for developing practical infrastructure engineering skills.

Planned areas of development include:

- Automated backups and recovery testing
- Improved infrastructure documentation
- Network segmentation and VLANs
- Managed switching
- Centralized storage / NAS services
- Infrastructure automation using Bash and Python
- Configuration management
- UPS integration and graceful shutdown
- Improved observability
- Rack-mounted infrastructure
- Additional security hardening

## Related Projects

Basecamp provides infrastructure and connectivity for several additional projects that will be documented separately:

- **Outpost** — portable Raspberry Pi edge workstation
- **Private 5G SA Lab** — Open5GS and UERANSIM test environment
- **Local AI Infrastructure** — self-hosted LLM and AI services

---

This repository documents the continued development of the Basecamp homelab, including architecture decisions, implementation, troubleshooting, and lessons learned.
