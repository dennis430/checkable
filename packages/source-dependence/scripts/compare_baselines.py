#!/usr/bin/env python3
"""Compare naive counting and exact-text dedup against documented origin groups.

Writes docs/BASELINES.md. Synthetic fixtures only. This does not declare a gate passed.
"""
from __future__ import annotations

import json
from pathlib import Path

from source_dependence.graph import analyze, build_graph
from source_dependence.models import Claim, Observation, Relationship, Source

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
OUT = ROOT / "docs" / "BASELINES.md"
SKIP = {"sample.bundle.json", "README.md"}


def load(path: Path):
    data = json.loads(path.read_text())
    claims = [Claim(**c) for c in data.get("claims", [])]
    observations = [Observation(**o) for o in data.get("observations", [])]
    sources = [Source(**s) for s in data.get("sources", [])]
    relationships = [Relationship(**r) for r in data.get("relationships", [])]
    return data, claims, observations, sources, relationships


def rows() -> list[dict]:
    found = []
    for path in sorted(EXAMPLES.iterdir()):
        if path.name in SKIP or path.suffix != ".json":
            continue
        data, claims, observations, sources, relationships = load(path)
        graph = build_graph(claims, observations, sources, relationships)
        profile = analyze(graph, claims[0].id)
        texts = [str(o.content) for o in observations]
        found.append(
            {
                "file": path.name,
                "naive": profile.observations_counted,
                "exact_text": len(set(texts)),
                "origin_groups": profile.sensitivity["distinct_documented_origin_group_count"],
                "collapses": profile.sensitivity["shared_origin_collapses_naive_count"],
                "circular": profile.sensitivity["circular_component_count"],
                "contradictions": profile.sensitivity["contradiction_edge_count"],
                "unresolved": len(profile.unresolved_relationships),
            }
        )
    return found


def render(found: list[dict]) -> str:
    lines = [
        "# Baselines on the public examples",
        "",
        "Synthetic fixtures. A smaller number is not a truth score.",
        "Exact-text dedup collapses identical `content` strings and ignores documented origins.",
        "`origin_groups` counts distinct documented `origin_group` values. Unknown lineage stays out of that count.",
        "",
        "This table does not declare Gate B passed. The examples were written by the maintainer.",
        "",
        "| Example | Naive count | Exact-text unique | Documented origin groups | Shared origin collapses naive count | Circular components | Contradictions | Unresolved edges |",
        "|---|---:|---:|---:|---|---:|---:|---:|",
    ]
    for row in found:
        lines.append(
            "| `{file}` | {naive} | {exact_text} | {origin_groups} | {collapses} | {circular} | {contradictions} | {unresolved} |".format(
                **row
            )
        )
    lines.append("")
    lines.append("Regenerate with `python scripts/compare_baselines.py` from a checkout with the package installed.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    found = rows()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(render(found))
    print(OUT)
    for row in found:
        print(row)


if __name__ == "__main__":
    main()
