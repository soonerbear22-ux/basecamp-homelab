# Troubleshooting and Engineering Evidence

[Overview](../README.md) · [Architecture](architecture.md) · [Networking](networking.md) · [Services](services.md)

## Evidence status

The original README lists the work below as completed. It does not include incident timelines, exact commands, before/after outputs, or detailed root-cause analyses. These are **historical summaries**, not reconstructed incident reports.

| Recorded work | Evidence needed for a full case study |
| --- | --- |
| Proxmox repository configuration and host updates | Original symptom, repository change, and update result |
| Docker Compose deployment and container troubleshooting | Affected stack, observed failure, change, and application validation |
| Persistent network addressing | Addressing method and verification after restart |
| Pi-hole deployment in LXC | Resolver path and controlled filtering test |
| Tailscale connectivity and remote HTTPS access | Client context, intended path, and sanitized result |
| Homepage host-restriction issue resolved | Exact error, relevant setting, reason for the change, and access test |
| Command-line network testing and monitoring | Test purpose, expected result, observed result, and interpretation |

No exact commands or root causes are invented to fill these gaps.

## Confirmed repository correction

**Problem:** the architecture diagram existed in both `docs/diagrams/basecamp-architecture.md` and root-level `diagrams/basecamp-architecture.md`.

**Action:** retained the root-level file as the canonical diagram and removed the misplaced duplicate in [commit 993bd62](https://github.com/soonerbear22-ux/basecamp-homelab/commit/993bd62687270a2594f1572cc4fb289f55ebf09f).

**Validation:** the GitHub deletion result confirmed success and the docs directory listed architecture.md without the duplicate subdirectory. Existing commits were retained.

**Prevention:** link to the canonical diagram from the README and architecture document; review the repository-relative path before committing a new file.

## September 26 engineering evidence

- **Docker image metadata failure:** the deployed API now retains a container result using its configured image when an image metadata lookup fails, and includes a warning instead of losing the entire inventory. The public regression test covers this fallback.
- **Broad homelab audits:** a combined endpoint retrieves seven component groups and retains partial results when a component raises an error. Derived fields keep ambiguous memory or vector-index readings separate from confirmed faults.
- **Knowledge freshness discrepancy, resolved before V1:** the morning expansion passed 28 targeted retrieval checks at 235 points; a later observation showed two baseline sources/101 points. The completion work restored the corpus, and the final direct inventory now has 34 source names/244 points, including retained validation documents. The earlier observation remains in the historical record; it is no longer the release state.
- **Samba ingestion race:** a three-second pre-start delay followed a successful transfer/ingestion test. It is a mitigation for that observed case, not a general file-completion protocol.
- **Ingestion lock permissions:** a lock under `/run` could not be opened by the service user. Moving it to the writable knowledge state directory allowed the locked service to ingest its test file successfully. The temporary lock-test source was removed afterward.
- **Misleading ai-worker memory percentage:** Proxmox reported a value slightly above allocated memory. Guest inspection showed about 10 GiB available, zero swap use and no reported OOM events; no RAM change was justified. V1 keeps this ambiguous metric separate from a confirmed memory fault.
- **Recovery validation:** the completion session passed a real host reboot with all three guests and eleven core containers recovering. The final packaging capture confirmed the running state and ai-worker guest-agent response without repeating a disruptive reboot.

See the [final V1 validation](validation-v1.md), [historical observation](validation-2026-09-26.md), and [knowledge pipeline](knowledge-pipeline.md).

## Suggested diagnostic workflow

This is a workflow for future incidents, not a report of tests run against the lab.

1. **Define the symptom and scope.** Record what fails, from which client context, when it began, and whether other services are affected.
2. **Check dependencies.** Separate physical host, guest, container, network, DNS, TLS, and application observations.
3. **Form a testable hypothesis.** State what result would support or reject it.
4. **Make the smallest justified change.** Record the previous state and a rollback path before modifying it.
5. **Validate the user-visible result.** A running process alone is insufficient; verify the intended application behavior.
6. **Check for regression.** Recheck related access paths and dependencies.
7. **Document the result.** Preserve sanitized evidence and distinguish confirmed cause from unresolved suspicion.

| Symptom | First distinction to establish |
| --- | --- |
| Multiple services unavailable | Shared host/VM/network dependency versus separate application failures |
| Name fails but service is otherwise reachable | DNS resolution versus transport/application failure |
| LAN works but remote access fails | Remote client authorization, overlay path, and endpoint selection |
| HTTPS endpoint fails | Connectivity, certificate validation, and application response |
| Homepage rejects access | Application host validation versus network reachability |
| Monitoring looks healthy but a user cannot connect | Monitoring vantage point and what the check actually measures |

## Incident record template

Copy this structure for a future evidence-backed case study:

```markdown
## Short incident title
- Date and scope:
- Symptom and impact:
- Expected behavior:
- Observed behavior:
- Evidence collected (sanitized):
- Hypothesis and test:
- Change made and reason:
- Validation result:
- Rollback plan and whether it was used:
- Confirmed cause, or remaining uncertainty:
- Prevention / follow-up:
```

A useful case study explains why the evidence justified the change. Omit sensitive values rather than publishing raw logs; follow the [public-documentation rules](security.md).

## Post-V1 operating record

See the [September 27 current state](current-state.md), [incident resolutions](changes/2026-09-27.md), and [Sentinel runbook](sentinel.md) for workstation naming, physical power work, independent DNS/monitoring, mobile access and backup validation. The V1 measurements above remain dated evidence. Sentinel backups to Basecamp do not establish off-host protection for Basecamp guest backups.

## September 29 media addition

[Jellyfin and media automation](jellyfin.md) add unprivileged guests 103 and 104. Today's read-only checks confirm Jellyfin health, five running media containers, and saved Radarr/Sonarr import/upgrade refresh hooks. The enabled backup job includes guest 103 but excludes guest 104; externally mounted library data needs separate protection. See the [dated evidence and remaining acceptance work](changes/2026-09-29.md). These services are outside the immutable V1 rebuild package and the core-only automatic inventory.
