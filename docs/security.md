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
- Add backup and recovery evidence, including protection of backup data.
- Validate alert delivery and the limits of monitoring on shared infrastructure.

Record implemented controls with date, scope, expected behavior, observed behavior, and remaining limitations. Keep sensitive evidence private and publish only the sanitized conclusion.

## Reporting an issue

Do not put credentials, private endpoints, or sensitive logs in a public issue. A public documentation correction can identify the affected file and describe the problem without disclosing operational details.
