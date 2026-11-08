"""Regression: multiple relationship assertions between same endpoints are preserved and order-invariant."""
from source_dependence.graph import analyze, build_graph
from source_dependence.models import Claim, Observation, Relationship, Source

def test_multi_relationship_preserved():
    claims = [Claim(id="c1", text="test")]
    observations = [
        Observation(id="o1", claim_id="c1", type="reported_assertion", content="a"),
        Observation(id="o2", claim_id="c1", type="reported_assertion", content="b"),
    ]
    sources = []
    rels = [
        Relationship(id="r1", from_id="o2", to_id="o1", label="documented", kind="derivation"),
        Relationship(id="r2", from_id="o2", to_id="o1", label="disputed", kind="derivation"),
    ]
    g = build_graph(claims, observations, sources, rels)
    assert g.number_of_edges("o2", "o1") == 2
    p1 = analyze(g, "c1")
    g2 = build_graph(claims, observations, sources, list(reversed(rels)))
    p2 = analyze(g2, "c1")
    assert len(p1.unresolved_relationships) == len(p2.unresolved_relationships)
    assert any("disputed" in u for u in p1.unresolved_relationships)
