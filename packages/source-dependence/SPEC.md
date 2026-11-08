# Experimental Specification Notes

## Data model

See `src/source_dependence/models.py`. Aligns with PROV-DM Entity (observations/claims), Activity (derivations), Agent (sources) without incompatible duplicates. Relationships labeled documented/declared/inferred/disputed/unknown/synthetic_ground_truth. `kind` may be `derivation`, `shared_origin`, `citation`, `infrastructure`, `contradiction`, or `other`. A `contradiction` edge is copied into `SupportProfile.contradictions`. It is not resolved.

## Bundle format `reconciliation.bundle.v1`

JSON object with version, manifest (inputs), assumptions, analytical_version, report, integrity (content_sha256 of canonical form excluding integrity field, plus optional signature/timestamp under explicit policy).

Canonicalization: sorted keys, compact separators, UTF-8.

Verification reports separately:
- bytes match commitment
- signature under selected trust policy
- timestamp/transparency under documented assumptions
- analysis reproducible from available inputs and version
- lineage independently established (always false unless separate evidence)

## Analysis

`analyze()` returns SupportProfile. `observations_counted` is the raw count. `sensitivity.naive_observation_count` repeats that count under an explicit name. `sensitivity.distinct_documented_origin_group_count` counts caller-supplied origin groups. `sensitivity.shared_origin_collapses_naive_count` is true only when one documented origin group covers more than one observation. Unknown lineage is not treated as shared origin. Exact text deduplication is not part of `analyze`. Circular components and contradiction edges are counted. Assumptions, when passed in, are recorded with `applied: false`. Unknowns and unresolved relationships are preserved. Notes state that a root count is not a count of statistically independent observations.
