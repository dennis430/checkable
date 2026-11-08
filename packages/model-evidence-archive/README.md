# model-evidence-archive

Cryptographically anchored longitudinal archive of model responses to synthetic evidential-reasoning probes.

Records authentic collector-observed responses. Does not invent historical observations. A hash of response bytes is not provider-origin authentication.

## Status

Experimental. The frozen panel is `probes/panel_v1.json` (12 probes, frozen 2026-10-23).

Authentic records in this tree: **none**. Coverage on 2026-11-08 is `PAUSED_ACCESS` until an operator configures `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GOOGLE_API_KEY`. See `COVERAGE.md`.

Anthropic and Google secrets are detected and reported. This version has an adapter only for OpenAI. A missing adapter is `ADAPTER_NOT_IMPLEMENTED`. No substitute answer is written.

## What is actually in the repository

- The frozen probe panel.
- A collector that dry-runs without secrets and, with a secret, calls the adapter it has.
- `scripts/verify_record.py`, which recomputes the SHA-256 of `raw_response`.
- No public model responses. The weekly workflow uploads an artifact. It does not commit one.

## Run it

Dry run, no network:

```bash
python scripts/collect.py --status status/coverage.json
```

Live, only if you accept the provider's terms and the spend:

```bash
OPENAI_API_KEY=... python scripts/collect.py --live
python scripts/verify_record.py records/incoming/<file>.json
```

`records/incoming/` is gitignored. A record belongs in `records/public/` only after a person has checked that `is_historical` is true and the bytes were not edited. Do not hand-write a model answer into that directory.

## Companions

- [source-dependence](https://github.com/dennis430/source-dependence) is the analytical core and the bundle verifier.
- [genesis-verifier](https://github.com/dennis430/genesis-verifier) recomputes a receipt against a cited file. It is not this collector.

## What this does not do

- Does not fill a missing week with a plausible answer.
- Does not treat a signature-free hash as proof of which provider produced the text.
- Does not score the answers. That would be a later, separate analysis, and only on records that were actually captured.

License: MIT for original code and probes. Provider outputs, when they exist, stay subject to the provider's terms.

Contact: GitHub issues.
