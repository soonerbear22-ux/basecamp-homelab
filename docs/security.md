# Security and Public Documentation

[Overview](../README.md) · [Architecture](architecture.md) · [Networking](networking.md)

## Scope

This page records the documented access model and the controls that still need evidence. It is not a security audit or a claim of production hardening.

## Documented baseline

| Area | What is supported by the project record | What is not established |
| --- | --- | --- |
| Remote access | Tailscale connectivity between authorized devices | Detailed access rules, device lifecycle, and negative access tests |
| HTTPS | Selected services use Tailscale HTTPS endpoints | Complete certificate/access review for every application |
| Workload separation | Applications in a VM; Pi-hole in a separate LXC | Complete isolation, least-privilege configuration, or host redundancy |
| Maintenance | Proxmox repository configuration and host updates listed as prior work | A current patch audit or scheduled maintenance process |
| Monitoring | Service and system monitoring tools documented | Security alerting coverage and tested notification delivery |

The documented design avoids requiring public management endpoints. Actual gateway forwarding, firewall rules, and application exposure must be verified before claiming there is no unintended public access. Encryption and network reachability do not replace application authorization.

## Public repository rules

Publish architecture, design reasoning, sanitized evidence, and generic procedures. Do not commit:

- Passwords, access tokens, API keys, private keys, session cookies, or recovery codes.
- Private IP addresses, Tailscale addresses, tailnet identifiers, or private endpoint URLs.
- Real environment files, credential-bearing configuration, database exports, or backups.
- Unreviewed logs and screenshots containing account details or sensitive configuration.

Use descriptive placeholders such as `<SERVICE_ENDPOINT>` in future examples. Review the entire file and commit diff, including screenshots and metadata, before publication. Redaction must remove the value rather than merely hide it visually.

If a credential is ever committed, treat it as exposed: revoke or rotate it through the issuing service and assess where it was used. Deleting the latest copy does not remove it from Git history. No credential exposure is asserted by this page.

## Planned hardening and validation

- Review administrative access, account privileges, and authentication settings.
- Document and test intended Tailscale and application access boundaries.
- Verify gateway forwarding and service exposure.
- Establish a repeatable update and rollback process.
- Design segmentation before marking VLAN isolation implemented.
- Complete an isolated restore drill and independent off-host backup protection; V1 now has scheduled coverage and archives for all three guests.
- Validate alert delivery and the limits of monitoring on shared infrastructure.

Record implemented controls with date, scope, expected behavior, observed behavior, and remaining limitations. Keep sensitive evidence private and publish only the sanitized conclusion.

## Reporting an issue

Do not put credentials, private endpoints, or sensitive logs in a public issue. A public documentation correction can identify the affected file and describe the problem without disclosing operational details.

## Current AI and knowledge boundaries

The API now uses a Proxmox token for infrastructure reads and reaches Docker, Prometheus, ai-worker, and Qdrant. Its public source takes endpoints and credentials from environment variables; private values and raw audit output are excluded. The API itself has no inbound authentication. GET-only routes do not constrain the privileges of a compromised process or prove that the upstream token has read-only permissions.

The published API copy enables Proxmox certificate verification and supports a private CA bundle. This publication adaptation has not been deployed; live trust configuration remains private. Review that boundary separately from Tailscale HTTPS access.

Knowledge results can contain sensitive operational facts and untrusted document text. Treat retrieval as evidence with a date and source, not as executable instructions. Database health does not prove source completeness; see the [final pipeline contract](knowledge-pipeline.md).

## V1 release controls

Public inputs use reserved example names or explicit placeholders. Environment files, certificates, databases, model weights, generated scrape targets and downloaded dependencies are excluded from Git. The API build context is restricted by `.dockerignore`; private site files cannot be copied by its Dockerfile.

The repository gate scans current public files and reachable historical text blobs for address, credential, private-key and identity patterns without echoing matched values. This is a bounded check, not proof that an arbitrary future secret will be detected. Review the entire diff before regenerating release checksums.

Docker socket access remains powerful even with a read-only mount; it does not restrict Docker API operations. Host PID/root mounts and Open Terminal are separate privilege boundaries. Keep unauthenticated API/Qdrant/metrics endpoints on restricted private paths. A `GET`-only API schema does not constrain a compromised process. The loopback defaults in the public templates must be deliberately adjusted for required private reachability.

The public package was validated without replacing live trust settings, credentials, access rules or application state. No fresh exposure/least-privilege audit is claimed by the release.

## Post-V1 operating record

See the [September 27 current state](current-state.md), [incident resolutions](changes/2026-09-27.md), and [Sentinel runbook](sentinel.md) for workstation naming, physical power work, independent DNS/monitoring, mobile access and backup validation. The V1 measurements above remain dated evidence. Sentinel backups to Basecamp do not establish off-host protection for Basecamp guest backups.
