# Keeping documentation current

[Overview](../README.md) · [Current state](current-state.md) · [Operations](operations.md)

## Installation status — September 28, 2026

The reviewed collector and publisher are installed on core-services. A manual collection and publisher dry run passed. The existing user crontab now runs the collector daily at **09:00 UTC** (04:00 Central daylight time / 03:00 Central standard time), using a non-overlapping lock and owner-private state directory. Existing schedule entries were preserved. Cron is active and does not require the operator to remain logged in. Cron does not catch up a run missed while the host is off; the first unattended scheduled execution remains to be observed.

**Automatic uploads are not enabled.** No GitHub credential was installed or extracted from the interactive connection. The validated first inventory is included in this repository; future local captures stay on the host until the separately scoped credential and first draft-PR check are completed. Its file contains no observation timestamp; this dated installation record establishes the initial capture, not continuing freshness.

The systemd units below are an alternative installation method, not a second active scheduler. The current host has user lingering disabled, so the existing cron service was used. Do not enable both schedules.

## Scope and publication boundary

The collector records only eleven explicitly named core containers' immutable **local image IDs** and restart policies. Image IDs identify local image content; they are not pullable registry digests and do not replace V1's registry pins. It does not read environment variables, logs, addresses, bind mounts, databases or arbitrary container names. Missing expected containers fail the capture, preserving the previous complete file. It deliberately excludes running state and volatile timestamps: this is configuration drift documentation, not availability monitoring.

The optional publisher validates the entire allowlist before any network request. It creates a draft pull request changing only `inventory/core-services.json` and that file's checksum entry. It never writes main, merges, or alters V1 pins. An unchanged observation makes no proposal. An existing inventory PR pauses further proposals; a previously closed proposal for identical content is not reopened. Review or merge pending changes before expecting newer observations to appear. If a proposal was declined in error, reopen it manually.

PR branches are public immediately. Review this projection and approve its fields before enabling publication. Repository privacy-pattern checks are an additional bounded safeguard, not a substitute for the allowlist or human review. No public-repository self-hosted Actions runner is installed in the lab.

## Local collector installation

Use the existing core-services operator account that already has Docker access. These are user systemd units; do not grant a new account Docker access solely for this task. Install only the reviewed collector, not a periodically auto-updated checkout:

```bash
install -d -m 700 ~/.local/lib/basecamp-inventory ~/.local/state/basecamp-inventory ~/.config/systemd/user
install -m 600 scripts/collect_inventory.py ~/.local/lib/basecamp-inventory/
install -m 600 deploy/systemd/basecamp-inventory.service deploy/systemd/basecamp-inventory.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user start basecamp-inventory.service
systemctl --user enable --now basecamp-inventory.timer
```

The timer runs daily at 09:00 in the host's timezone, with up to ten minutes jitter and catch-up after downtime. For operation after logout, an administrator must enable lingering for the selected account. Check `loginctl show-user "$USER" -p Linger` and the next trigger with `systemctl --user list-timers basecamp-inventory.timer`. A user timer without lingering is not guaranteed to run while logged out.

## Optional GitHub publisher

Publication requires a separately supplied credential. The connected interactive GitHub account is not exported into the homelab. Use an expiring fine-grained token limited to this repository with Contents write and Pull requests write, or an equivalently scoped GitHub App installation token maintained by a separate credential manager. Never paste credentials into chat, commit them, or place them in command arguments. Store the token in an owner-only regular file outside Git; on Linux the publisher enforces owner and mode checks.

Copy `scripts/propose_inventory.py` beside the reviewed collector. First run without credentials to validate the local file; this makes no network request:

```bash
python3 ~/.local/lib/basecamp-inventory/propose_inventory.py --inventory ~/.local/state/basecamp-inventory/core-services.json
```

After placing the credential locally, run once with `--credential-file` pointing to that private file. Review the resulting draft PR and confirm CI before scheduling uploads. Add an `ExecStartPost` command to a user service override using those same paths only after that check. Keep the collector and publisher installation pinned until their updates are separately reviewed; do not fetch and execute main during a scheduled run.

If main advances while a PR is open, resolve its checksum manifest against current main, run the repository validator, and review the inventory before merge. A failed API operation exits without printing raw request/response details; an interrupted branch creation can resume on the next run. Errors never trigger a forced update. Only one local service instance should publish at a time. The account credential has more authority than the script uses; keep it protected and revoke it when retiring the task.

## Physical work and incidents

Record date, purpose, general equipment placement, cable category/termination, verification, observed failure, root cause, correction and recovery test. Do not publish home addresses, detailed floor plans or private network endpoints. Configuration collection cannot infer a wall drop, tell which UPS outlet was used, or explain why a repair worked. Add a reviewed note under `docs/changes/` and link it from current state.

## Disable and recover

Disable the user timer with `systemctl --user disable --now basecamp-inventory.timer`. This does not stop lab services. Preserve the last inventory for diagnosis; remove any publication override and revoke its credential if compromised. Check the last collector service result before relying on the saved inventory: old output is deliberately retained on failure.

For the installed cron variant, use `crontab -e` and remove only the line marked `basecamp-inventory-managed`; preserve unrelated jobs. The most recent scheduled run's safe summary is in `~/.local/state/basecamp-inventory/last-run.log`. The cron line uses a lock; retain that lock if extending it to invoke publication after a successful collection. Do not run the publisher after a failed collection, because the saved file then represents an older observation.

References: [GitHub pull request API](https://docs.github.com/en/rest/pulls/pulls), [fine-grained permissions](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens), and [self-hosted runner security](https://docs.github.com/en/actions/reference/security/secure-use).
