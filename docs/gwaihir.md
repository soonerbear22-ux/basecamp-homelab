# Gwaihir — portable homelab operations console

Gwaihir is the Chromebook-based portable administration and recovery endpoint for the homelab.

## Platform

- ChromeOS Chromebook
- Debian 13 Crostini Linux environment
- Linux hostname: `gwaihir`
- Operator account and private endpoint values are configured locally

## Purpose

Gwaihir provides an independent management path into the homelab when another workstation or management endpoint is unavailable.

Current capabilities include:

- Tailscale remote connectivity
- SSH/Termius administration
- Moonlight remote access to Elros
- Git and GitHub repository access
- Network diagnostics
- Homelab reachability and service checks

## Installed diagnostic tools

- git
- ssh
- curl
- wget
- dig
- traceroute
- iperf3
- nmap

## Repository

A working clone of the homelab repository is maintained at:

`~/homelab/basecamp-homelab`

GitHub authentication uses a dedicated Gwaihir SSH key. Private key material is not stored in this repository.

## Local workspace

`~/gwaihir`

Subdirectories:

- `bin` — administration utilities
- `logs` — diagnostic output
- `backups` — temporary recovery/configuration copies
- `notes` — working notes

## homelab-status

The public script uses reserved example hostnames by default. Supply `HORNBURG`, `CORE`, `PIHOLE`, `SENTINEL`, `PALANTIR`, `MEDIA`, `ELROS` and optionally `SSH_KEY` in the local environment; do not commit private values. This sanitization changes the public recipe only, not the commissioned installation.

The `homelab-status` utility performs non-destructive network and TCP service checks from Gwaihir.

The initial verified checks include:

- Hornburg / Proxmox
- Pi-hole
- Sentinel / Uptime Kuma
- Palantir / Jellyfin
- media-automation
- Radarr
- Sonarr
- Prowlarr
- qBittorrent
- Elros service reachability
- Elros Ollama
- Elros ComfyUI
- Elros Kokoro TTS
- Elros Sunshine

Elros is monitored at an operator-configured private endpoint. Because Elros does not respond to ICMP ping from Gwaihir, its online state is determined from verified service reachability rather than ping alone.

All initial host and service checks passed during Gwaihir commissioning on October 2, 2026.

## Security

No passwords, API keys, private SSH keys, authentication tokens, or other secrets should be committed to this repository.

## Incident snapshots

Gwaihir can capture a timestamped homelab status report for troubleshooting:

```bash
homelab-status --save
```

Snapshots are stored locally under:

```text
~/gwaihir/logs/homelab-status-YYYY-MM-DD_HH-MM-SS.log
```

The snapshot records host reachability, Proxmox guest state, core services,
media services, infrastructure checks, and external-system status at the
time the command is run. External-system status includes Elros and its
verified Ollama, ComfyUI, Kokoro TTS, and Sunshine service checks.

Normal `homelab-status` operation remains unchanged.
