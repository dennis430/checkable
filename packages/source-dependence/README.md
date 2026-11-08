# source-dependence

Source-dependence and evidential reconciliation methodology with reference implementation and portable bundle verifier.

This package provides:

- Structured models for claims, observations, sources, derivation relationships, assumptions, and acquisition metadata, aligned with W3C PROV concepts where useful.
- Local analysis that traces shared origins, circular support, unknown lineage, and documented contradictions. Outputs a support/dependence profile. Does not manufacture a universal truth score.
- Portable reconciliation bundles (experimental spec) with integrity verification that remains usable independently of the analytical engine.
- CLI and library for offline use. No accounts, no hosted upload service.

## Status

Experimental v0.1.2. The gates in `KILL_CRITERIA.md` are not declared passed. Maintainer-written examples do not count as external use. See `LIMITATIONS.md`, `KILL_CRITERIA.md`, and `VALUE_CAPTURE.md`.

## Install

Clone, then install. The examples are files in the checkout, not files inside the wheel.

```bash
git clone https://github.com/dennis430/source-dependence.git
cd source-dependence
pip install -e .
```

The tag `v0.1.2` is the same tree plus the release notes. The wheel and sdist on that release install the library only.

PyPI publishing is prepared in `.github/workflows/publish.yml` and is not live. `pip install source-dependence` will 404 until that publisher is configured.

## Quick start

From the checkout:

```bash
source-dependence analyze examples/duplicate.json
source-dependence analyze examples/same_text_distinct_origins.json
source-dependence verify-bundle examples/sample.bundle.json
```

`duplicate.json` is two different wordings and one documented origin. Counting reports says 2. Exact text deduplication also says 2. Documented origin groups say 1.

`same_text_distinct_origins.json` is the same text from two documented origins. Exact text deduplication says 1. Origin groups say 2. This package does not collapse them.

`verify-bundle` checks the envelope hash. A match does not re-run the analysis and does not establish lineage. `analysis_reproducible` stays `NOT_RUN`.

The other eight cases, and the command that regenerates the comparison table, are in `examples/README.md` and `docs/WALKTHROUGH.md`. The generated table is `docs/BASELINES.md`.

## Companions

These three repositories are one set. They do not import each other.

- [genesis-verifier](https://github.com/dennis430/genesis-verifier) recomputes a receipt against the file it cites. A pass is not authorization and not authenticity.
- [model-evidence-archive](https://github.com/dennis430/model-evidence-archive) holds the frozen probe panel. Authentic model responses are stored only when a collector captured them. None are in the tree yet.

## What this does not do

- Does not claim a claim is true or assign calibrated real-world probabilities in v0.1.
- Successful bundle verification does not establish that lineage is independently authenticated or that a real-world claim is true.
- Not a substitute for qualified judgment.
- Not a paid product, a consulting funnel, or a standard. Contact is GitHub issues.

License: MIT. Copyright 2026 Dennis Liu.
