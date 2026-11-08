# Changelog

## 0.1.2 - 2026-11-08

First tagged release. v0.1.1 was described below while `pyproject.toml` was still `0.1.0`; that version was not tagged.

- Ten public synthetic examples and `examples/sample.bundle.json`, which the quick start already named.
- `sensitivity` now states the naive observation count, the documented origin-group count, whether a shared origin collapses that naive count, circular components, and contradiction edges.
- A documented `contradiction` relationship is listed. It is not reconciled.
- Assumptions passed to `analyze` are recorded and marked not applied.
- `scripts/compare_baselines.py` regenerates `docs/BASELINES.md`.
- Install instructions no longer tell a new user to `pip install` a name that is not on PyPI.

These examples were written by the maintainer. They do not close Gate B or Gate C.

## 0.1.1 - 2026-10-24 (corrective)

- Removed false analysis_reproducible success assertion (R04). Status is now NOT_RUN until explicit re-execution.
- Explicit Click command names (analyze, verify-bundle) and non-zero exit on verification failure.
- Replaced echo-only daily workflow with controller that performs integrity check and persists state/ledger.
- Archive collector implemented with offline fixtures and PAUSED_ACCESS reporting; workflow invokes it.
- Findings ledger added at docs/review/findings.md.

Original 0.1.0 release remains the first public snapshot. These changes are prospective repairs, not backdated observations.

## 0.1.0 - 2026-10-23

- Initial experimental release (scaffolding).
