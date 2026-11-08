#!/usr/bin/env python3
"""Write examples/sample.bundle.json from the duplicate example.

The bundle commits to this run's report. Verification of the file checks the
envelope hash. It does not re-run analysis and does not establish lineage.
"""
from __future__ import annotations

import json
from pathlib import Path

from source_dependence import __version__
from source_dependence.bundle import write_bundle
from source_dependence.graph import analyze, build_graph
from source_dependence.models import Claim, Observation, Relationship, Source

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples" / "duplicate.json"
DEST = ROOT / "examples" / "sample.bundle.json"


def main() -> None:
    data = json.loads(SOURCE.read_text())
    claims = [Claim(**c) for c in data["claims"]]
    observations = [Observation(**o) for o in data["observations"]]
    sources = [Source(**s) for s in data["sources"]]
    relationships = [Relationship(**r) for r in data["relationships"]]
    graph = build_graph(claims, observations, sources, relationships)
    profile = analyze(graph, claims[0].id)
    bundle = write_bundle(
        manifest={"inputs": ["examples/duplicate.json"], "claim_id": claims[0].id},
        report=json.loads(profile.model_dump_json()),
        assumptions=[],
        analytical_version=__version__,
    )
    DEST.write_text(json.dumps(bundle, indent=2) + "\n")
    print(DEST)


if __name__ == "__main__":
    main()
