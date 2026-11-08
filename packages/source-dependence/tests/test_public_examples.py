"""Public examples must keep the distinctions the README states."""
import json
from pathlib import Path

from source_dependence.bundle import verify_bundle
from source_dependence.graph import analyze, build_graph
from source_dependence.models import Claim, Observation, Relationship, Source

EX = Path("examples")


def _profile(name: str):
    data = json.loads((EX / name).read_text())
    graph = build_graph(
        [Claim(**c) for c in data.get("claims", [])],
        [Observation(**o) for o in data.get("observations", [])],
        [Source(**s) for s in data.get("sources", [])],
        [Relationship(**r) for r in data.get("relationships", [])],
    )
    return analyze(graph, data["claims"][0]["id"], None), data


def test_shared_origin_is_not_exact_dedup():
    profile, data = _profile("duplicate.json")
    texts = {str(o["content"]) for o in data["observations"]}
    assert profile.observations_counted == 2
    assert len(texts) == 2
    assert profile.sensitivity["distinct_documented_origin_group_count"] == 1
    assert profile.sensitivity["shared_origin_collapses_naive_count"] is True


def test_same_text_distinct_origins_are_not_collapsed():
    profile, data = _profile("same_text_distinct_origins.json")
    texts = {str(o["content"]) for o in data["observations"]}
    assert len(texts) == 1
    assert profile.sensitivity["distinct_documented_origin_group_count"] == 2
    assert profile.sensitivity["shared_origin_collapses_naive_count"] is False


def test_circular_support_is_reported():
    profile, _ = _profile("circular.json")
    assert profile.sensitivity["circular_component_count"] >= 1
    assert any("circular" in item for item in profile.unknowns)


def test_contradiction_is_listed():
    profile, _ = _profile("contradiction.json")
    assert profile.sensitivity["contradiction_edge_count"] == 1
    assert profile.contradictions


def test_unknown_lineage_is_not_a_shared_origin():
    profile, _ = _profile("unknown_lineage.json")
    assert profile.unknowns
    assert profile.sensitivity["shared_origin_collapses_naive_count"] is False
    assert profile.sensitivity["distinct_documented_origin_group_count"] == 0


def test_inferred_edge_stays_unresolved():
    profile, _ = _profile("inferred_not_documented.json")
    assert any("inferred" in item for item in profile.unresolved_relationships)
    assert profile.sensitivity["shared_origin_collapses_naive_count"] is False


def test_assumption_is_recorded_not_applied():
    data = json.loads((EX / "missing_source_and_one_documented.json").read_text())
    from source_dependence.models import Assumption

    graph = build_graph(
        [Claim(**c) for c in data["claims"]],
        [Observation(**o) for o in data["observations"]],
        [Source(**s) for s in data["sources"]],
        [],
    )
    profile = analyze(graph, "c1", [Assumption(**a) for a in data["assumptions"]])
    assert profile.assumption_conditioned_results["applied"] is False
    assert profile.assumption_conditioned_results["assumption_ids"] == ["a1"]


def test_sample_bundle_envelope_only():
    result = verify_bundle(EX / "sample.bundle.json")
    assert result["envelope_commitment_consistent"] is True
    assert result["analysis_reproducible"] == "NOT_RUN"
    assert result["lineage_independently_established"] is False
    assert result["exit_code_recommended"] == 0
