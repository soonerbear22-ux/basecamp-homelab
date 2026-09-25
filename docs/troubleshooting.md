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
