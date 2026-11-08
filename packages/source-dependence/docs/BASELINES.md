# Baselines on the public examples

Synthetic fixtures. A smaller number is not a truth score.
Exact-text dedup collapses identical `content` strings and ignores documented origins.
`origin_groups` counts distinct documented `origin_group` values. Unknown lineage stays out of that count.

This table does not declare Gate B passed. The examples were written by the maintainer.

| Example | Naive count | Exact-text unique | Documented origin groups | Shared origin collapses naive count | Circular components | Contradictions | Unresolved edges |
|---|---:|---:|---:|---|---:|---:|---:|
| `circular.json` | 2 | 2 | 2 | False | 1 | 0 | 0 |
| `contradiction.json` | 2 | 2 | 2 | False | 0 | 1 | 0 |
| `disputed_derivation.json` | 2 | 2 | 2 | False | 0 | 0 | 1 |
| `duplicate.json` | 2 | 2 | 1 | True | 0 | 0 | 0 |
| `independent.json` | 2 | 2 | 2 | False | 0 | 0 | 0 |
| `inferred_not_documented.json` | 2 | 2 | 2 | False | 0 | 0 | 1 |
| `missing_source_and_one_documented.json` | 1 | 1 | 1 | False | 0 | 0 | 0 |
| `same_text_distinct_origins.json` | 2 | 1 | 2 | False | 0 | 0 | 0 |
| `single_origin_three_reports.json` | 3 | 3 | 1 | True | 0 | 0 | 0 |
| `unknown_lineage.json` | 3 | 3 | 0 | False | 0 | 0 | 0 |

Regenerate with `python scripts/compare_baselines.py` from a checkout with the package installed.
