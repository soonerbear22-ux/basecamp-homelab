# Arda — private World of Warcraft server

[Overview](../README.md) · [Current state](current-state.md) · [Backup and recovery](backup-recovery.md)

Current Homelab scope is VM 105 placement/resources, guest agent/autostart, six-guest Proxmox backup participation and selected isolated whole-VM restore acceptance. Separate SQL import/game-client recovery, application source revisions, accounts and gameplay belong to Arda. This pass does not synchronize Arda application behavior.

Arda is a dedicated Ubuntu Server virtual machine hosting an AzerothCore Wrath of the Lich King 3.3.5a realm. This runbook records the public, sanitized operating facts and excludes private addresses, credentials, tokens and player data.

## Placement

- Proxmox VM: 105
- Guest name: `arda`
- vCPU: 4
- RAM: 8 GiB
- Virtual disk: 64 GiB on local-lvm (newer canonical operator evidence supersedes the earlier qcow2/bulk-storage placement)
- Autostart: enabled
- Guest agent: enabled
- OS: Ubuntu Server 24.04 LTS

Arda is separate from the core-services, media and embedding workloads.

## Historical October 3 application record

Application-specific facts below are retained as dated history, not refreshed by this infrastructure synchronization. Home-directory paths use a generic placeholder; use the Arda canonical package for current application operation.

### AzerothCore layout

Source repository:

`/home/user/azerothcore-wotlk`

Installed runtime:

`/home/user/azerothcore`

These paths have different roles. Git operations belong in the source tree; runtime binaries and configuration are under the installed tree.

The verified source revision during the October 3 maintenance session was commit `950684036946011c3d597382b3cfb5de99f7adbc` on `master`.

Runtime configuration includes:

- `/home/user/azerothcore/etc/authserver.conf`
- `/home/user/azerothcore/etc/worldserver.conf`

## Databases and services

MySQL 8.4 is used for the standard AzerothCore databases:

- `acore_auth`
- `acore_characters`
- `acore_world`

Production services:

- `arda-auth.service`
- `arda-world.service`

The realm uses the normal AzerothCore authentication and world-server TCP ports. Private network addresses are intentionally omitted from this public repository.

## Backups

A local backup script at `/usr/local/bin/arda-backup` creates timestamped compressed dumps of all three AzerothCore databases plus configuration files.

The corresponding systemd timer runs daily and is persistent across downtime. A manual October 3 backup completed successfully and its gzip archives passed integrity testing.

This proves local backup creation and archive integrity, not full disaster recovery. An isolated database restore drill remains a separate acceptance item.

## Known incident: repeated `AC>` prompt logging

On October 3, 2026, `worldserver` generated a severe repeated-console-prompt log storm. Symptoms included high worldserver, journald and rsyslog CPU use and several gigabytes of journal growth.

Setting `AC_DISABLE_INTERACTIVE=1`, including through the AzerothCore wrapper path, did not suppress the behavior for the deployed build.

The working systemd approach keeps stdin open and non-terminating:

```bash
/bin/bash -c 'exec 0< <(tail -f /dev/null); exec /home/user/azerothcore/bin/worldserver -c /home/user/azerothcore/etc/worldserver.conf'
```

After the change, worldserver remained available and the repeated `AC>` prompt output stopped.

Treat this as a known production workaround. Any replacement should be tested for service availability, journal growth and prompt recurrence before it is accepted.

## Journal safeguards

Persistent journal limits were added after the incident:

```ini
[Journal]
SystemMaxUse=500M
SystemKeepFree=2G
RuntimeMaxUse=100M
```

Unexpected journal growth should be investigated at the source rather than handled by simply increasing these limits.

## Operating rules

Before material changes:

1. inspect live service, database, resource and log state;
2. preserve relevant configuration and logs;
3. verify a usable backup when data is at risk;
4. change one major variable at a time;
5. re-check services, ports, logs and realm behavior afterward.

Do not publish credentials, database passwords, recovery material, private addresses or player data.
