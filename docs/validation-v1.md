# V1 validation record

[Overview](../README.md) · [Release notes](../release/NOTES-v1.0.0.md) · [Machine-readable evidence](../release/evidence.json)

**Freeze date:** September 26, 2026, America/Chicago. The final live capture began at 01:13 UTC on September 27. The [earlier September 26 observation](validation-2026-09-26.md) is retained as history and is superseded where the completion work changed the state.

## Live and recorded acceptance

| Check | Result | Evidence boundary |
| --- | --- | --- |
| Proxmox guests | Three expected guests running; autostart enabled on all three | Read-only API/configuration capture |
| Core Docker | Eleven expected containers running; all use `unless-stopped` | Live Docker inspection |
| Host reboot recovery | All three guests, core services and DNS recovered | Recorded completion session; not repeated during packaging |
| ai-worker guest agent | Active; Proxmox ping succeeded | Guest and host read-only checks |
| API schema/runtime | Thirteen GET operations; all thirteen returned JSON in the release verifier | Does not prove every response field is correct |
| Full audit | Seven requested / seven retrieved; complete | Collection success is distinct from health |
| Embeddings/retrieval | 2560-dimensional response; successful semantic query | Functional sample, not a quality benchmark |
| Knowledge inventory | Qdrant green; 34 source names, 244 points | Includes retained validation files; private contents excluded |
| Automatic ingestion/lock | Successful test via watcher and writable `flock` path; temporary lock test removed | Completion-session output; packaging checked active watcher/current state |
| Worker memory | About 10 GiB available; zero swap use | Guest reading supports treating Proxmox's anomalous percentage cautiously |
| DNS | Local Pi-hole query resolved; versions captured | Does not validate all client filtering/DHCP behavior |
| Backup scope/artifacts | Enabled daily snapshot/zstd job for 100, 101, 102; last seven retained; archives for each | Existing core/Pi-hole archives predate final evening changes; no restore drill |

## Repository validation

- **23 tests passed:** ingestion failure/idempotence/replacement, collection initialization safety, environment parsing, and the pinned API's eleven contract/regression tests. All external dependencies in these tests are mocked.
- Both sanitized Compose definitions parsed successfully with the installed Compose CLI; no services were deployed.
- Generated Prometheus configuration passed `promtool check config` without changing the running configuration.
- Python, JSON and YAML syntax, Markdown relative links, code fences, immutable image/model/API references and dependency file hashes passed the repository gate.
- Public-file privacy patterns and all 28 unique existing reachable text blobs plus commit messages were checked before publication. The workflow repeats the check including the release commit's files/history. Matched values are never printed.
- Release file SHA-256 checksums are in [CHECKSUMS.sha256](../release/CHECKSUMS.sha256). They exclude downloaded API files, which have separate hashes in the manifest, and the checksum file itself.

The test run emitted one upstream Starlette/httpx deprecation warning. Assertions passed; the pinned test dependencies remain unchanged for this release.

The [validation workflow](../.github/workflows/validate.yml) reruns repository checks, tests and Compose parsing on pushes and pull requests. GitHub's Actions page is the authoritative record for each hosted run.

## Not claimed

A fresh end-to-end rebuild, an isolated backup restore, an off-host backup, exhaustive secret detection, firewall/least-privilege verification, all-client DHCP/DNS acceptance, alert delivery and complete current voice recovery were not tested by packaging. Private data and customized app state must be supplied by the operator. The production infrastructure was not redeployed, reindexed or rebooted during this release work.
