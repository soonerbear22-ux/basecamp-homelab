# Rebuild Basecamp V1

[Overview](../README.md) · [Configuration](configuration.md) · [Operations](operations.md) · [Backups](backup-recovery.md)

This procedure targets **fresh, isolated guests**. The working lab was frozen, not redeployed during packaging. The public core Compose project consolidates several live projects and reuses their container names: do not run it beside the existing installation on the same Docker host. Follow [rollback guidance](backup-recovery.md) before any migration.

## 1. Provision the platform

Use the [guest reference](../config/proxmox-guests.example.json) for sizing and roles. Create the application VM, unprivileged Debian Pi-hole LXC, and embedding VM with unused IDs if your host already has guests. Configure private addressing, storage, bridge and autostart locally. Preserve independent access to the Proxmox console.

For ai-worker, enable IOMMU in firmware/host configuration, identify the actual GPU/IOMMU group, assign the RTX 3060 to the guest, and install a compatible NVIDIA driver. PCI IDs, firmware flags and device groups depend on the machine; never copy another machine's device address. Install QEMU Guest Agent in the Ubuntu guests and enable its Proxmox option. The frozen worker uses fixed 12 GiB RAM with ballooning disabled.

Install Docker Engine with Compose on both Ubuntu guests. On ai-worker, install/configure the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html), then verify GPU visibility before starting TEI. The observed driver is recorded in the manifest; do not treat it as a hardware-independent requirement.

Install Pi-hole in its isolated LXC following the [official installation documentation](https://docs.pi-hole.net/main/basic-install/). Restore a reviewed private export or configure upstream DNS/filtering anew. The existing lab has DHCP enabled; a fresh instance must remain isolated until its range, gateway, reservations and responsibility relative to any other DHCP server are explicitly settled. Private DNS/DHCP settings are not in this release.

## 2. Obtain and validate the package

On the Linux build/deployment guest, check out `v1.0.0` and work from the repository root:

```bash
git clone --branch v1.0.0 https://github.com/soonerbear22-ux/basecamp-homelab.git
cd basecamp-homelab
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-validation.txt
python scripts/fetch_api.py
python scripts/validate_repository.py --history
python -m pytest -q tests vendor/homelab-api/tests
```

The API download is locked to a Git commit and SHA-256 checksums. Existing changed dependency files are never overwritten. Image/model downloads require registry access and disk capacity; no model weights are bundled.

## 3. Supply private configuration

Copy `config/site.env.example` to ignored `site.env` and restrict it to its operator (`chmod 600 site.env`). Replace every `.invalid` endpoint and `REPLACE_ME` value. Generate independent application secrets and use an appropriately restricted Proxmox read identity. Store the trusted Proxmox CA as `ca.crt` in the configured CA directory; the public API verifies certificates.

Choose private bind interfaces deliberately. The safe examples bind published ports to loopback. TEI must be reachable from core-services. Node Exporter uses host networking, so its listen address and Prometheus target must be reachable from the Prometheus container. `localhost` inside a container is that container, not its host. Configure the Basecamp host's Node Exporter separately for the additional host target, or remove that scrape job if intentionally outside your rebuild.

Create the data/cache directories referenced by Compose on the correct guest. Verify required UID/GID and permissions for each pinned image before first startup; inspect its configured user and application documentation. In particular, Grafana and Prometheus must be able to write their data directories. Never make the entire data tree world-writable. The Qdrant, knowledge and model-cache paths are separate from the common data root.

A new Beszel installation needs hub setup before an agent token/key exists: start only `beszel`, create the local account/system entry privately, then supply its key/token. Temporary example values must not reach a running agent. Similarly, existing application databases may override environment defaults; verify settings in each application after a restore.

Render and validate once all inputs are complete:

```bash
python scripts/render_config.py --env-file site.env
docker compose --env-file site.env -f deploy/core-services/compose.yaml config --quiet
docker compose --env-file site.env -f deploy/ai-worker/compose.yaml config --quiet
```

`config --quiet` validates configuration without deploying it. Avoid printing full resolved configuration because it includes secrets. See [Docker's configuration reference](https://docs.docker.com/reference/cli/docker/compose/config/).

## 4. Start dependencies on their respective guests

On **ai-worker**, copy the package and a worker-specific private environment (do not distribute the core Proxmox/app credentials to this guest). Supply only `AI_WORKER_BIND_ADDRESS` and `EMBEDDING_MODEL_CACHE` for its Compose file:

```bash
docker compose --env-file site.env -f deploy/ai-worker/compose.yaml pull
docker compose --env-file site.env -f deploy/ai-worker/compose.yaml up -d
```

Wait for model loading and verify TEI health and an actual 2560-element embedding using your private endpoint. GPU access is declared through a [Compose device reservation](https://docs.docker.com/compose/how-tos/gpu-support/).

On **core-services**:

```bash
docker compose --env-file site.env -f deploy/core-services/compose.yaml pull --ignore-buildable
docker compose --env-file site.env -f deploy/core-services/compose.yaml build homelab-api
docker compose --env-file site.env -f deploy/core-services/compose.yaml up -d qdrant prometheus node-exporter
python scripts/init_collection.py --env-file site.env
docker compose --env-file site.env -f deploy/core-services/compose.yaml up -d
```

Collection initialization creates a missing collection only; it rejects incompatible existing dimensions/distance and never drops data. `depends_on` establishes startup order, not readiness. Inspect failures before starting user traffic.

Complete private application setup: WebUI administrator and Ollama connection, API tool endpoint, Terminal connection for specifically authorized assistants, dashboard links, Grafana data source/dashboards, Kuma checks, Beszel pairing and private access routes. Use `http://homelab-api:8091` and `http://open-terminal:8000` for clients inside the same Compose network. Main-PC Ollama/image services must be reachable through the intended private path. Tailnet routes, model presets and application databases are not recreated automatically.

## 5. Install knowledge ingestion on core-services

For a **new** service account and empty knowledge tree:

```bash
sudo adduser --system --group --home /opt/basecamp/knowledge basecamp
sudo install -d -o basecamp -g basecamp /opt/basecamp/knowledge/{inbox,processed,state,scripts}
sudo install -o basecamp -g basecamp -m 0644 knowledge/ingest.py /opt/basecamp/knowledge/scripts/ingest.py
sudo -u basecamp python3 -m venv /opt/basecamp/knowledge/.venv
sudo /opt/basecamp/knowledge/.venv/bin/pip install -r knowledge/requirements.txt
sudo install -d -m 0750 -g basecamp /etc/basecamp
sudo install -m 0640 -g basecamp config/knowledge.env.example /etc/basecamp/knowledge.env
```

Edit `/etc/basecamp/knowledge.env` privately to replace its endpoint. Confirm the service account can write the state/processed/inbox directories and read the environment. For an existing tree, back it up and inspect ownership rather than recursively changing unrelated data.

Create the Qdrant collection before enabling the watcher. Install the units:

```bash
sudo install -m 0644 deploy/systemd/homelab-knowledge-ingest.* /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now homelab-knowledge-ingest.path
```

For optional Windows file submission, install Samba, merge the [share example](../config/samba-knowledge.conf.example), set the local Samba password interactively with `sudo smbpasswd -a basecamp`, validate with `testparm`, and restrict access to intended private clients. Stage complete files outside the watched inbox before moving them in. The delay is not a guarantee that a large network transfer is finished.

## 6. Acceptance and backups

Run the [operations acceptance procedure](operations.md). Start with the synthetic sample, check retrieval/provenance, then supply your own reviewed corpus. Do not expect the private lab's 244-point count from one public sample.

Create the Proxmox backup job using the [reference scope](../config/proxmox-backup.example.cfg), verify archives for every guest and schedule a future isolated restore drill. Set autostart only after validating guest behavior. A controlled host reboot requires a maintenance window and console access; record guest, DNS, container, embedding and API recovery separately.

Repository validation and Compose parsing passed for V1. An end-to-end fresh installation, database restore, gateway exposure audit and client-wide DNS/DHCP validation remain separate acceptance work for each deployment.
