# Validation record — September 26, 2026

[Overview](../README.md)

| Evidence | Result | Interpretation |
| --- | --- | --- |
| Live combined audit, 21:42 UTC | 7/7 component groups retrieved | Telemetry collected successfully; not a full security or recovery audit |
| Proxmox API | Host, guests, and storage reads succeeded | Authenticated access worked for those operations |
| Expected guests | VM 100, LXC 101, VM 102 running | Dated guest state |
| Expected Docker containers | 11 present and running | Does not prove every application workflow |
| Embedding request | 2560 dimensions returned | Embedding generation worked |
| Qdrant and semantic query | Green, 101 points, one query result returned | Search worked against the current collection |
| Direct source inventory | Two baseline sources, 19 + 82 points | Earlier 27 runbooks absent from the live index |
| Morning corpus report | 27 added documents, 135 chunks, 28/28 targeted retrieval checks | Historical successful expansion; later discrepancy unresolved |
| Public API regression tests | Mocked contract and failure-behavior checks | Separate from live deployment validation |

## Findings requiring follow-up

The processed runbooks and morning manifests survive, but the live source set differs. Preserve both evidence sets before deciding whether to reingest. A green collection and a successful query do not prove corpus completeness.

The combined API distinguishes unusual metrics from confirmed faults. Its `complete` flag counts retrieved groups; callers must inspect dependency health inside those groups. The audit does not establish image currency, off-host backup, restore readiness, or voice recovery.
