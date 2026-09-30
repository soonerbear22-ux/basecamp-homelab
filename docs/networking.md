# Networking and Remote Access

[Overview](../README.md) · [Architecture](architecture.md) · [Diagram](../diagrams/basecamp-architecture.md) · [Security](security.md)

## Documented topology

| Component | Role in the baseline |
| --- | --- |
| AT&T BGW320 | Home gateway shown in the original diagram |
| Home LAN | Local connectivity for infrastructure and clients |
| BASECAMP | Proxmox host connected to the home network |
| core-services | Application VM participating in LAN and Tailscale connectivity |
| ai-worker | Separate LAN and Tailscale reachability; embedding dependency for ingestion/search |
| Pi-hole in LXC 101 | Network-level DNS filtering |
| Tailscale | Authenticated overlay connectivity for authorized endpoints |

The diagram is logical: it does not specify physical ports, subnet routes, firewall rules, or a complete traffic matrix.

## Access paths

**Local access:** clients reach local infrastructure through the home network. Pi-hole provides DNS filtering and its DHCP feature is enabled in the final capture. Lease ranges, reservations, upstream resolvers and client fallback behavior remain private and are not reproduced by this repository.

**Remote access:** Tailscale connects authorized devices to homelab endpoints. The original project record reports administration from Windows, a laptop, iPhone, iPad, and Outpost. Selected services use Tailscale HTTPS endpoints to provide consistent service addresses at home and away.

This describes the intended access model. It does not prove that every endpoint is reachable, that every client uses Pi-hole, or that all public exposure has been audited.

## Addressing and DNS documentation

Persistent network addressing is listed as prior completed work. The mechanism, lease/reservation arrangement, and complete address plan remain undocumented. Private addresses and tailnet names belong in private operational records, not this public repository.

Use logical roles such as `BASECAMP`, `core-services`, and `DNS service` in public diagrams. Avoid publishing actual endpoint URLs in screenshots or copied command output.

## Additional access validation

V1 recorded DNS recovery after reboot and a successful local DNS query during packaging. The following broader access checks remain a proposed plan, not completed test results:

| Check | Evidence to capture privately | Public summary |
| --- | --- | --- |
| LAN application access | Client context, target, and response | Which service was reachable and when |
| DNS filtering | Client resolver selection and a controlled query | Resolution/filtering behavior observed |
| Remote access | An authorized client away from the LAN and target response | Device category and successful/failed access |
| HTTPS | Certificate and application response | Validation outcome without endpoint names |
| Access restrictions | Allowed and denied client/service combinations | Policy behavior without identities or addresses |
| DNS dependency | Behavior during controlled Docker-VM maintenance | Whether DNS remained available |

Record observations separately from assumptions. An application response, successful name lookup, and overlay connectivity each validate different parts of the path.

## Planned changes

VLANs, network segmentation, and managed switching are planned. No implemented VLAN IDs, subnet design, subnet router, exit node, or firewall policy is asserted here.

Before a network change, record the working baseline and a recovery access path privately. Change one layer at a time, verify the intended paths, and use the [troubleshooting record](troubleshooting.md) to document the outcome.

## September 26 additions

The knowledge inbox is available through an authenticated Samba share mapped on Windows. Tailscale Serve mappings were inspected for production WebUI, dashboard, and monitoring access. The old voice-test mapping remains configured even though its historical container was absent from the morning inventory; a saved route is not evidence of an available backend.

The latest combined audit checks ai-worker TCP reachability and the embedding HTTP health route separately. A TCP connection does not establish authenticated SSH access, and LAN HTTP health does not independently test the overlay HTTP path.

## Public rebuild bindings

The reference core Compose project gives containers service-name DNS. Host-side ingestion uses the loopback-published Qdrant port; container clients use `qdrant:6333`. TEI remains on the separate worker. Node Exporter's host-network listener must be reachable from Prometheus, and its target label must match the API's `PROMETHEUS_INSTANCE` input.

Published ports default to loopback; choose required private interfaces and review host/firewall policy before enabling remote access. Configure Tailscale identities and HTTPS routes locally. Never copy the live installation's private address plan into Git. See the [rebuild order](rebuild.md).

## Post-V1 operating record

The physical installation now places the gateway/modem, Basecamp, Sentinel and CyberPower UPS together in a closet. Five labeled runs were installed and operator-verified: one from the exterior demarcation through the attic to the closet (medium unspecified), and four Cat6 runs from the closet to Citadel's bedroom. The operator tested with a JDSU and confirmed a 1,000 Mbps connection rate. This is link-speed evidence, not an application throughput benchmark or an assertion of a particular cable-certification standard. Private label-to-port mappings belong in the local inventory.

See the [September 27 current state](current-state.md), [incident resolutions](changes/2026-09-27.md), and [Sentinel runbook](sentinel.md) for workstation naming, physical power work, independent DNS/monitoring, mobile access and backup validation. The V1 measurements above remain dated evidence. Sentinel backups to Basecamp do not establish off-host protection for Basecamp guest backups.

## September 29 media addition

[Jellyfin and media automation](jellyfin.md) add unprivileged guests 103 and 104. Today's read-only checks confirm Jellyfin health, five running media containers, and saved Radarr/Sonarr import/upgrade refresh hooks. The enabled backup job includes guest 103 but excludes guest 104; externally mounted library data needs separate protection. See the [dated evidence and remaining acceptance work](changes/2026-09-29.md). These services are outside the immutable V1 rebuild package and the core-only automatic inventory.
