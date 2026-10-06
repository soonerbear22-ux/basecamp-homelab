# H16 — historical privacy disposition (October 6, 2026)

## Root cause and classification

GitHub workflow `Validate V1 package`, job `validate`, failed in run
`37459896935` at `python scripts/validate_repository.py --history` on main
`73cc6a34dc9236b36a03fbbc3609cf55423b28bc`. The scanner applied the current
publication rules to every historical blob, without carrying the source path
needed for its existing filename-filter constant exception.

Seven blob/category findings were reproduced across 168 unique reachable text
blobs. Six are historical private infrastructure information; one is a validator
false positive. None is a sanitized numeric example or an exposed credential.

| Blob (unique prefix) | Path | Category | Introduced | Replaced/removed |
| --- | --- | --- | --- | --- |
| `7c5ea80d0215` | `knowledge/ingest.py` | False positive: filename-filter set constant | `679a1bb6bbb6` | Still current; code is safe |
| `777548971059` | `docs/arda.md` | Personal home paths | `bb114fbeae6a` | `73cc6a34dc92` |
| `de2c8c51dd35` | `scripts/gwaihir/homelab-status` | Private LAN addresses | `b22cd51a8043` | `3ada38735ad1` |
| `b524d4182d97` | `scripts/gwaihir/homelab-status` | Private LAN addresses | `3ada38735ad1` | `836c40d2adc7` |
| `75607f190af5` | `scripts/gwaihir/homelab-status` | Private LAN addresses | `836c40d2adc7` | `554964bc984e` |
| `9e2f6880a2a0` | `scripts/gwaihir/homelab-status` | Private LAN addresses | `554964bc984e` | `73cc6a34dc92` |
| `93d629dc252b` | `docs/gwaihir.md` | Private LAN address | `554964bc984e` | `73cc6a34dc92` |

The underlying infrastructure values entered on October 3 UTC; the last current
copies were sanitized October 6 UTC. These were actual operational identifiers,
not examples. Their removal from main does not remove old copies from history.
They reveal internal topology/account naming but provide no authentication
capability. No credential usability probe or account/service change was needed.
No rotation/revocation requirement was identified from these findings.

## Scope and limits

All advertised branch/tag refs were cloned for basecamp-homelab, homelab-api and
local-ai-lab: only main in each, plus basecamp-homelab's V1 tag. The six private
blobs remain reachable through main history; none occurs in V1's reachable
objects. The constant remains current on main. Related repositories contain
neither these blobs nor the same private values in their reachable text history.
GitHub release listings show one V1 release, with no attached assets, and no
releases in either related repository. The V1 release predates these findings.

Supplementary private-key, GitHub-token, AWS access-key, credential-webhook and
JWT pattern searches found no matches across 168/36/45 reachable text blobs in
the three repositories. The full repository validator also found no genuine
credential assignments after correcting the constant false positive. These are
bounded heuristic checks, not a guarantee about arbitrary unknown secret
formats, unreachable GitHub objects, external clones/forks, or deleted refs.
No sensitive values or raw historical content appear in this report.

## Accepted non-destructive treatment

Retain the six exact old infrastructure blobs, with explicit review entries in
[history-privacy-review.json](../release/history-privacy-review.json), rather
than rewriting public history solely to remove private LAN/account identifiers.
This dispositions the historical risk; it does not claim that exposure was erased
or that these internal values are obsolete/unusable. Current publication remains
strict. Any future stronger removal request requires a separately approved
history-rewrite plan; no such action is necessary for this disposition.

Each review binds a full Git blob ID, actual path and infrastructure finding
category. A changed blob, copied blob at a different path, new category or stale
entry fails. Credential categories cannot be placed in the review list. The
scanner enumerates all commit trees to check every path and requires a full
clone. It continues scanning all reachable text blobs and commit messages;
reviewed findings remain visible as `REVIEWED`, rather than disappearing.

The existing filename-filter set exception now receives the actual historical
source path and remains restricted to the exact constant line in
`knowledge/ingest.py`. Neither other paths nor real assignments gain an exception.

The workflow still invokes `--history` as a blocking check. No workflow step was
skipped, made advisory, or given continue-on-error. V1 pins/tag/release evidence
were untouched. Rollback is a normal revert of this change, restoring the prior
failing gate without altering public history. No runtime deployment occurred.

## Acceptance

The current-tree syntax/link/privacy/pin/checksum gate, full history scan and
53 repository/API tests passed locally, including 15 new privacy regressions.
Regressions cover copied/changed historical blobs, new historical secrets,
branch/tag-only findings, commit messages, current-tree protection, prohibited
credential exemptions, stale reviews, shallow clones and redacted output.
Native Compose parsing is left to the unchanged GitHub CI job because Docker
CLI is absent from the task environment. Publication and resulting CI are
recorded in the private canonical Homelab package after actual observation.
