# Review Findings Disposition (updated)

Baseline after corrective: source-dependence @ 9ead1c22..., model-evidence-archive @ 2646fe55...

## Accepted prior fixes (preserved)
- R04: analysis_reproducible = NOT_RUN. Commit c5ec4e25.
- R13: explicit command names. Commit 9582dd8f.
- Partial R06: nonzero exit on envelope mismatch.

## R01 - PARTIAL
- Controller now loads prior state and preserves terminal statuses (FROZEN_* etc.). Fails closed if pyproject.toml missing.
- Still no full Day-3/7/30/90 machine, no artifact download/restore across runs, no budget reservation.
- Commit 8165ea49.

## R02 - PARTIAL
- OpenAIAdapter with injectable Transport and MockTransport added. Offline tests prove request construction, response parsing, hash of actual bytes, is_historical flag.
- Live workflow still dry-run; no secret wiring; no persistence of real records yet.
- Commit f930034e / cf62c882.

## R07-R11 - Partial progress
- Graph switched to MultiDiGraph; duplicate IDs rejected; multi-edges preserved; SCC-based cycle detection; order-invariant test added.
- Public synthetic examples now cover shared origin, same-text distinct origins, circular support, unknown lineage, contradiction, inferred edges, and disputed edges. See examples/ and docs/BASELINES.md.
- Full sensitivity re-run (analyze again after removing disputed edges) and automated constraint reconciliation are still not implemented.
- Commit 3d535ad8 / 8cac7823, plus the v0.1.2 adoption commit.

## R03 - Unresolved
- Runs 40060747386 and 40060747765 failed with runner ID 0, no steps. Cause not established from available metadata. New changes not yet re-dispatched.

## R12 - Release cut, registry still closed
- Tag v0.1.2 is the GitHub release. Independent of PyPI.
- Trusted publishing in publish.yml is still not configured. pip install source-dependence remains a 404.

## R14 - Open
- Full gate enforcement is still open. v0.1.2 does not declare Gate B or Gate C passed. Maintainer-authored examples do not count.

## 2026-11-08 — adoption drop, gates unchanged

- The quick start commands in the README now resolve to files in the tree.
- analyze reports the contrast with naive counting. It still does not deduplicate text, does not apply assumptions, and does not re-run sensitivity after deleting disputed edges.
- Archive R02 persistence is tracked in the model-evidence-archive repository, not by this file's older "no persistence" sentence.
