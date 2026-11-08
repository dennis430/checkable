"""Versioned structured records for claims, observations, sources, and relationships.

User-supplied lineage is an assertion, not authenticated fact. Inferred edges are reviewable.
Maps to PROV-DM Entity/Activity/Agent where useful without inventing incompatible duplicates.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class ObservationType(str, Enum):
    DIRECT = "direct_observation"
    REPORTED = "reported_assertion"
    TRANSFORMATION = "transformation"
    INFERENCE = "inference"
    SYNTHETIC = "synthetic_fixture"


class RelationLabel(str, Enum):
    DOCUMENTED = "documented"
    DECLARED = "declared"
    INFERRED = "inferred"
    DISPUTED = "disputed"
    UNKNOWN = "unknown"
    SYNTHETIC_GT = "synthetic_ground_truth"


class Claim(BaseModel):
    id: str
    text: str
    hypothesis: Optional[str] = None


class Source(BaseModel):
    id: str
    name: Optional[str] = None
    origin_group: Optional[str] = None  # documented shared origin if known
    infrastructure: Optional[str] = None
    rights: Optional[str] = None


class Observation(BaseModel):
    id: str
    claim_id: str
    type: ObservationType
    content: Any  # structured or text; treated as data
    source_id: Optional[str] = None
    times: dict[str, Optional[datetime]] = Field(default_factory=dict)  # observation, publication, acquisition, anchor
    uncertainty: Optional[dict] = None
    coverage: Optional[str] = None
    missingness: Optional[str] = None


class Relationship(BaseModel):
    id: str
    from_id: str  # observation or source
    to_id: str
    label: RelationLabel
    kind: Literal[
        "derivation",
        "shared_origin",
        "citation",
        "infrastructure",
        "contradiction",
        "other",
    ] = "other"
    supporting_refs: list[str] = Field(default_factory=list)
    asserted_by: Optional[str] = None  # who declared/inferred


class Assumption(BaseModel):
    id: str
    text: str
    conditioned_on: list[str] = Field(default_factory=list)


class SupportProfile(BaseModel):
    """Structured support/dependence profile. No universal truth score."""
    claim_id: str
    observations_counted: int
    documented_origin_groups: list[str]
    unresolved_relationships: list[str]
    assumption_conditioned_results: dict[str, Any] = Field(default_factory=dict)
    sensitivity: dict[str, Any] = Field(default_factory=dict)  # what changes if disputed removed, etc.
    contradictions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    # Explicitly: root_count is not independent observations count
    version: str = "0.1.0"
