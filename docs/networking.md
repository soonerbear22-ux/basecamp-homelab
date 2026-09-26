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

**Local access:** clients reach local infrastructure through the home network. Pi-hole provides DNS filtering, but exact client DNS distribution, upstream resolvers, and fallback behavior are not captured in the repository.

**Remote access:** Tailscale connects authorized devices to homelab endpoints. The original project record reports administration from Windows, a laptop, iPhone, iPad, and Outpost. Selected services use Tailscale HTTPS endpoints to provide consistent service addresses at home and away.

This describes the intended access model. It does not prove that every endpoint is reachable, that every client uses Pi-hole, or that all public exposure has been audited.

## Addressing and DNS documentation

Persistent network addressing is listed as prior completed work. The mechanism, lease/reservation arrangement, and complete address plan remain undocumented. Private addresses and tailnet names belong in private operational records, not this public repository.

Use logical roles such as `BASECAMP`, `core-services`, and `DNS service` in public diagrams. Avoid publishing actual endpoint URLs in screenshots or copied command output.

## Validation to record next

The following is a proposed validation plan, not a test result:

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
