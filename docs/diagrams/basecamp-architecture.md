# Basecamp Infrastructure Diagram

```mermaid
flowchart TB

    Internet([Internet])
    Gateway["AT&T BGW320<br/>Home Gateway"]

    Internet --> Gateway

    subgraph LAN["Home Network"]
        direction TB

        Basecamp["BASECAMP<br/>Proxmox VE<br/>i7-9700K | 32 GB RAM"]

        subgraph Proxmox["Virtualized Infrastructure"]
            direction LR

            Core["core-services<br/>Ubuntu Server 24.04 LTS<br/>Docker Host"]
            PiHole["LXC 101<br/>Pi-hole<br/>DNS Filtering"]
        end

        subgraph Docker["Docker Services"]
            direction LR
            WebUI["Open WebUI"]
            Homepage["Homepage"]
            Kuma["Uptime Kuma"]
            Beszel["Beszel"]
            Monitoring["Monitoring<br/>Components"]
        end

        Gateway --> Basecamp
        Basecamp --> Core
        Basecamp --> PiHole

        Core --> WebUI
        Core --> Homepage
        Core --> Kuma
        Core --> Beszel
        Core --> Monitoring
    end

    subgraph Tailnet["Tailscale Overlay Network"]
        direction LR
        Windows["Windows<br/>Workstation"]
        Outpost["OUTPOST<br/>Raspberry Pi 4"]
        Mobile["iPhone / iPad"]
        Laptop["Laptop"]
    end

    Windows -. Secure Remote Access .-> Basecamp
    Outpost -. Secure Remote Access .-> Core
    Mobile -. Secure Remote Access .-> Core
    Laptop -. Secure Remote Access .-> Basecamp
```

## Architecture Summary

Basecamp acts as the primary virtualization host for the homelab.

Proxmox VE separates infrastructure workloads into virtual machines and Linux containers. The `core-services` Ubuntu Server VM hosts containerized applications through Docker, while Pi-hole operates independently in an LXC container.

Local services communicate across the home LAN, while Tailscale provides authenticated remote connectivity for authorized endpoints without requiring management services to be directly exposed to the public internet.
