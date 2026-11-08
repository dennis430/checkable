"""Graph construction using MultiDiGraph to preserve multiple relationship assertions.
Traces documented derivation paths. Bounded cycle detection via strongly connected components.
"""

from __future__ import annotations

from typing import Any

import networkx as nx

from .models import (
    Assumption,
    Claim,
    Observation,
    Relationship,
    Source,
    SupportProfile,
)


def build_graph(
    claims: list[Claim],
    observations: list[Observation],
    sources: list[Source],
    relationships: list[Relationship],
) -> nx.MultiDiGraph:
    g = nx.MultiDiGraph()
    seen_ids = set()
    for c in claims:
        if c.id in seen_ids:
            raise ValueError(f"Duplicate claim ID: {c.id}")
        seen_ids.add(c.id)
        g.add_node(c.id, kind="claim", data=c)
    for o in observations:
        if o.id in seen_ids:
            raise ValueError(f"Duplicate observation ID: {o.id}")
        seen_ids.add(o.id)
        g.add_node(o.id, kind="observation", data=o)
        g.add_edge(o.id, o.claim_id, kind="bears_on", key="bears_on")
    for s in sources:
        if s.id in seen_ids:
            raise ValueError(f"Duplicate source ID: {s.id}")
        seen_ids.add(s.id)
        g.add_node(s.id, kind="source", data=s)
    for r in relationships:
        g.add_edge(r.from_id, r.to_id, key=r.id, data=r, label=r.label.value, kind=r.kind)
    return g


def analyze(
    graph: nx.MultiDiGraph,
    claim_id: str,
    assumptions: list[Assumption] | None = None,
) -> SupportProfile:
    """Produce support/dependence profile. Trace documented relationships."""
    if claim_id not in graph:
        raise ValueError(f"Claim {claim_id} not in graph")

    obs_nodes = [
        u for u, v, k, d in graph.edges(keys=True, data=True)
        if v == claim_id and graph.nodes[u].get("kind") == "observation"
    ]
    obs_ids = set(obs_nodes)
    origin_groups = set()
    unresolved = []
    contradictions = []
    unknowns = []
    group_members: dict[str, list[str]] = {}

    for oid in obs_ids:
        obs = graph.nodes[oid]["data"]
        if obs.source_id and obs.source_id in graph:
            src = graph.nodes[obs.source_id]["data"]
            if src.origin_group:
                origin_groups.add(src.origin_group)
                group_members.setdefault(src.origin_group, []).append(oid)
            else:
                unknowns.append(f"Unknown origin for source {obs.source_id} of {oid}")
        else:
            unknowns.append(f"No source for observation {oid}")

        for _, _, k, edata in graph.edges(oid, keys=True, data=True):
            if edata.get("kind") == "contradiction":
                contradictions.append(f"{oid} key={k} contradicts {edata.get('label')}")
            if edata.get("label") in ("unknown", "disputed", "inferred"):
                unresolved.append(f"{oid} key={k} label={edata.get('label')}")

    sccs = [c for c in nx.strongly_connected_components(graph) if len(c) > 1]
    circular_count = len(sccs)
    if circular_count:
        unknowns.append(f"Potential circular support in SCCs of size >1: {circular_count} component(s)")

    disputed_count = sum(1 for _, _, _, d in graph.edges(keys=True, data=True) if d.get("label") == "disputed")
    shared_origin_collapses = any(len(members) > 1 for members in group_members.values())
    sensitivity = {
        "naive_observation_count": len(obs_ids),
        "distinct_documented_origin_group_count": len(origin_groups),
        "shared_origin_collapses_naive_count": shared_origin_collapses,
        "circular_component_count": circular_count,
        "contradiction_edge_count": len(contradictions),
        "disputed_edge_count": disputed_count,
        "note": (
            "shared_origin_collapses_naive_count is true only when two observations "
            "carry the same documented origin group. Unknown lineage is not treated as shared origin. "
            "Exact text deduplication is not performed here."
        ),
    }
    assumption_conditioned: dict[str, Any] = {}
    if assumptions:
        assumption_conditioned = {
            "assumption_ids": [a.id for a in assumptions],
            "applied": False,
            "note": "Assumptions are recorded. This version does not recompute the profile with them removed.",
        }

    profile = SupportProfile(
        claim_id=claim_id,
        observations_counted=len(obs_ids),
        documented_origin_groups=sorted(origin_groups),
        unresolved_relationships=unresolved,
        assumption_conditioned_results=assumption_conditioned,
        sensitivity=sensitivity,
        contradictions=contradictions,
        unknowns=unknowns,
        notes=[
            "Root count is not a count of statistically independent observations.",
            "Documented derivation paths are traced separately from caller-supplied origin groups.",
            "Multiple relationship assertions between the same endpoints are preserved.",
        ],
    )
    return profile
