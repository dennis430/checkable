# Walkthrough

Checkout, then:

```bash
pip install -e .
source-dependence analyze examples/duplicate.json
```

Read `sensitivity` in the JSON:

- `naive_observation_count` is how many observations bear on the claim.
- `distinct_documented_origin_group_count` is how many origin groups the caller already wrote down.
- `shared_origin_collapses_naive_count` is true only when two of those observations carry the same documented origin group.

Then:

```bash
source-dependence analyze examples/same_text_distinct_origins.json
source-dependence analyze examples/circular.json
source-dependence analyze examples/contradiction.json
source-dependence analyze examples/unknown_lineage.json
python scripts/compare_baselines.py
```

`docs/BASELINES.md` is the output of that script. If you edit an example, regenerate the table and commit both.

Bundle round trip:

```bash
python scripts/write_sample_bundle.py
source-dependence verify-bundle examples/sample.bundle.json
```

Change one byte inside `report` and leave `integrity.content_sha256` alone. `verify-bundle` exits non-zero. Putting the hash back does not mean the analysis was run again, and it does not mean the stated lineage is true.

Library:

```python
import json
from source_dependence.graph import analyze, build_graph
from source_dependence.models import Claim, Observation, Relationship, Source

data = json.load(open("examples/duplicate.json"))
graph = build_graph(
    [Claim(**c) for c in data["claims"]],
    [Observation(**o) for o in data["observations"]],
    [Source(**s) for s in data["sources"]],
    [Relationship(**r) for r in data["relationships"]],
)
print(analyze(graph, "c1").model_dump_json(indent=2))
```

A third-party integration is a program that calls `analyze` or `verify_bundle` on records that this repository did not ship. Opening an issue with that use, or a link to the calling code, is the signal this project is set up to receive.
