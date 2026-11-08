# Public examples

Synthetic records. No customer evidence. Each file is one claim and the relationships a caller already wrote down. The analyzer does not decide that those relationships are true.

| File | What a stranger should notice |
|---|---|
| `duplicate.json` | Two wordings, one documented origin. Counting reports says 2. Exact text dedup also says 2. Origin groups say 1. |
| `same_text_distinct_origins.json` | Same text, two documented origins. Exact text dedup says 1. Origin groups say 2. This package does not collapse them. |
| `independent.json` | Different text, two documented origins. Naive count and origin groups agree at 2. |
| `single_origin_three_reports.json` | Three reports, one origin group. Naive count says 3. |
| `circular.json` | Each report cites the other. A cycle is reported. It is not converted into independent support. |
| `unknown_lineage.json` | Missing sources stay unknown. They are not filled in and not treated as a shared origin. |
| `contradiction.json` | A documented contradiction is listed. It is not averaged away. |
| `inferred_not_documented.json` | An inferred derivation stays unresolved. It is not upgraded to documented. |
| `disputed_derivation.json` | A disputed edge stays unresolved and is counted in sensitivity. |
| `missing_source_and_one_documented.json` | One documented observation. The coverage assumption is recorded and not applied. |
| `sample.bundle.json` | A portable bundle. `verify-bundle` checks the envelope hash only. |

Regenerate the comparison table with `python scripts/compare_baselines.py`.
