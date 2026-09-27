# Basecamp V1 — reproducible infrastructure baseline

V1 freezes the completed September 26, 2026 homelab and packages its configuration, source dependencies, validation and operating procedures for review and reproduction.

## Included

- Three-guest Proxmox reference architecture and corrected root-level diagram.
- Eleven core services and a separate GPU embedding worker, with captured image digests and an immutable Qwen3 model revision.
- Environment-based site configuration, checksum-verified API source, pinned Python dependencies, ingestion source, systemd locking and Samba/backup examples.
- Rebuild, operations, backup/restore, rollback, networking and troubleshooting runbooks.
- Sanitized final evidence, release checksums and continuous repository validation.

## Acceptance

The final capture confirmed all guests/containers running, thirteen responding API operations, a seven-of-seven audit, healthy 2560-dimensional embeddings and semantic retrieval, and 34 indexed sources / 244 points including retained test sources. The completion session passed host reboot recovery and locked automatic ingestion. Daily backups now cover all three guests, with archives observed for each.

Twenty-three mocked regression tests passed. Both Compose files and generated Prometheus configuration passed their native parsers. Repository syntax, relative links, pins, checksums and bounded privacy/history checks passed. See the [validation record](../docs/validation-v1.md) for exact scope.

## Reproduction and limits

Follow the [rebuild guide](../docs/rebuild.md). This is a reference package with manual platform provisioning and private operator inputs. It was not clean-room deployed or substituted for the working lab. Public adaptations include a consolidated Compose project, explicit bindings and certificate-verifying API configuration.

Private knowledge, app databases, credentials, addresses, dashboard state and model weights are not distributed. Archives are on the same bulk disk; off-host copies and isolated restores remain unverified. Some observed archives predate the final evening changes. Voice, VLANs, UPS and alert-delivery validation are outside V1 acceptance.

The API dependency is fixed at commit `13e8d5cd4bae0fe06087cdf161c720f6aef8848f`; the release manifest records its file hashes and all image/model pins. Future changes should use a new reviewed version and preserve V1 as the reproducible reference.
