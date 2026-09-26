# Backup coverage and recovery

[Overview](../README.md) · [Storage](storage.md)

## Implemented and observed September 26

The inspected enabled Proxmox job runs daily in snapshot mode, retains the last seven backups, and explicitly includes core-services VM 100 and Pi-hole LXC 101. Archives dated September 22–26 were listed at the configured destination.

VM 102 ai-worker is absent from this job, and no ai-worker archive appeared in that destination's listing. Backups elsewhere have not been established.

## Limits

- The backup destination shares Basecamp's large physical disk with the other named storage destination.
- An archive existing does not prove that it restores successfully.
- The inspected September 26 core-services archive predates the morning knowledge expansion.
- GPU-worker recovery needs VM configuration, EFI state, system disk, passthrough settings, and the embedding deployment materials.
- Current whole-lab reboot recovery and voice-service startup remain unverified.

## Proposed restore acceptance

Restore to an isolated target. Validate application data, guest startup, DNS behavior, a real embedding request, semantic search, and a controlled ingestion against the isolated database. Record the archive used and any manual intervention.

This procedure is a plan, not a completed restore test. Earlier Raspberry Pi/Windows power-recovery observations do not validate today's three-guest Basecamp topology.
