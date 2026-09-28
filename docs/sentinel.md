# Sentinel independent recovery node

[Overview](../README.md) · [Current state](current-state.md) · [Backups](backup-recovery.md)

Sentinel is a Raspberry Pi outside the Basecamp virtualization host. It provides Pi-hole DNS, Uptime Kuma, Tailscale administration, diagnostics and a self-contained emergency status page. Core-services Kuma and Sentinel Kuma are distinct monitoring instances; Homepage links distinguish both and the emergency page.

## Completed controls and checks

- Key-only SSH, no root SSH or X11 forwarding, and targeted host firewall rules while preserving Docker and Tailscale networking.
- Docker administration requires elevated privileges; the normal operator was removed from the Docker group.
- Debian security updates are automatic without automatic reboot. Pi-specific packages, Pi-hole and container updates remain controlled maintenance.
- Kuma was pinned to the existing 2.5.5 image digest without recreating the running container.
- Health checks run every two minutes for DNS, services, temperature, storage, power warnings and backup age. Backup freshness threshold is 36 hours.
- Emergency status has no external asset dependency; its health endpoint returns an unhealthy response for degraded or stale state.
- Persistent journals have bounded size/retention. Recovery and diagnostic tools are available locally.

## Backup and recovery contract

The daily schedule is 03:30 America/Chicago with up to ten minutes of jitter and persistent catch-up. Three local snapshots and thirty successful Basecamp snapshots are retained. Captures include live SQLite snapshots, the Pi-hole export, Kuma data/Compose, selected configuration and recovery inventory.

The destination uses a restricted backup account and forced receiver. Receiver checks include storage identity, capacity and checksum. Staged validation checked five SQLite databases, the Pi-hole archive and Kuma contents after downloading a backup. This was not a production overwrite, an SD-card image, or a bare-metal restoration. Tailscale node identity is excluded; total loss requires enrollment again.

Basecamp receives Sentinel backups. That direction does not protect Basecamp's own guest archives from loss of Basecamp or its backup disk. Router/DHCP settings were not changed in the Sentinel setup; verify client resolver selection before claiming DNS redundancy.

## Recovery acceptance

After maintenance, check local DNS, emergency health freshness, Kuma, private SSH, backup age and destination storage. Test an uncached name lookup and the intended client DNS path. During a Basecamp outage, expect the remote backup to fail visibly while Sentinel continues local service; confirm a new successful backup after recovery.

The recorded controlled network-isolation test passed these independence checks. Real UPS power-loss testing, automatic low-battery shutdown and independent phone alerts remain outside that acceptance.
