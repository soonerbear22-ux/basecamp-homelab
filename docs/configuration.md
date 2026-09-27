# Configuration inventory

[Overview](../README.md) · [Rebuild](rebuild.md) · [Security](security.md)

The release separates observed production settings from public rebuild adaptations. The [manifest](../release/manifest.json) is the machine-readable version record; the [evidence file](../release/evidence.json) contains aggregate observations.

| Artifact | What it fixes | Operator supplies |
| --- | --- | --- |
| Core/worker Compose | Service topology, mount destinations, image digests, restart policy, TEI options | Bind addresses, storage paths, private endpoints and credentials |
| Guest reference | IDs/roles, CPU/RAM/disk sizing, autostart and GPU role | Installation media, unused IDs, bridge, MAC/UUID, PCI device and addressing |
| Backup reference | Daily snapshot, zstd, keep-last 7, three-guest scope | Existing storage destination, schedule/timezone and capacity checks |
| API dependency | Exact Git commit plus file SHA-256 values | Proxmox identity/token, trusted CA and private service endpoints |
| Ingestion/systemd | Source, Python pins, watcher and shared flock path | Service account, permissions and private environment |
| Samba example | Authenticated inbox share and masks | Local account/password and network restrictions |

## Version policy

All third-party service containers use digests captured from installed images. The embedding model uses cached revision `5cf2132abc99cad020ac570b19d031efec650f2b`, with float16, 8192 maximum batch tokens, and client batch size 8. The live tag was `86-1.9`; the public recipe pins its image digest and the model revision. TEI supports revision selection through its [documented CLI](https://huggingface.co/docs/text-embeddings-inference/cli_arguments).

The API's original Python base-image digest was unavailable, so the rebuild Dockerfile pins the official `python:3.12-slim` digest resolved during packaging. API and ingestion Python dependencies are pinned to captured installed versions. The OS package installation of `procps`, installation media, drivers, Pi-hole installer and Docker host installation are not fully locked artifacts; this is functional reproducibility, not a byte-identical OS/image build.

## Private inputs and application setup

Copy [site.env.example](../config/site.env.example) to ignored `site.env`. Replace every `REPLACE_ME` and `.invalid` value. Never print rendered secrets in a public log. `render_config.py` writes an ignored local Prometheus file and refuses placeholder settings by default.

The API container and host ingestion use different Qdrant addresses: Compose service DNS inside the container; loopback for host ingestion. The Proxmox node name and expected guest/container names in the pinned API reflect Basecamp. A differently named installation must adapt and retest that dependency.

Open WebUI accounts, tools, model connections, image/voice settings, Homepage content, Grafana dashboards, Uptime Kuma checks, Beszel pairing, Pi-hole lists/leases and Tailscale routes live in private application state. A fresh deployment requires those setup steps; container startup does not reproduce personalized settings. No model weights, private corpus, database export, token or certificate private key is included.

The repository contains no new blanket license grant. Dependencies and model downloads retain their upstream licenses and terms.
