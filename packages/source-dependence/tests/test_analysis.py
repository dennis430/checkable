"""Synthetic tests with known generation processes."""

import json
from pathlib import Path

import pytest

from source_dependence.graph import analyze, build_graph
from source_dependence.models import Claim, Observation, Relationship, Source


def test_duplicates_do_not_increase_independent_support():
    data = json.loads(Path("examples/duplicate.json").read_text())
    claims = [Claim(**c) for c in data["claims"]]
    observations = [Observation(**o) for o in data["observations"]]
    sources = [Source(**s) for s in data["sources"]]
    relationships = [Relationship(**r) for r in data["relationships"]]
    g = build_graph(claims, observations, sources, relationships)
    profile = analyze(g, "c1")
    assert profile.observations_counted == 2
    assert "group1" in profile.documented_origin_groups
    # Under declared duplicate model, does not claim additional independent support
    assert any("not a count of statistically independent" in n for n in profile.notes)


def test_unknown_lineage_remains_unknown():
    claims = [Claim(id="c1", text="test")]
    observations = [Observation(id="o1", claim_id="c1", type="reported_assertion", content="x")]
    sources = []
    relationships = []
    g = build_graph(claims, observations, sources, relationships)
    profile = analyze(g, "c1")
    assert any("No source" in u or "Unknown" in u for u in profile.unknowns)
