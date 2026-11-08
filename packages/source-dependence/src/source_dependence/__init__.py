"""Source-dependence: analytical core and portable reconciliation bundles."""

__version__ = "0.1.2"

from .models import (
    Claim,
    Observation,
    Source,
    Relationship,
    Assumption,
    SupportProfile,
)
from .graph import build_graph, analyze
from .bundle import write_bundle, verify_bundle

__all__ = [
    "Claim",
    "Observation",
    "Source",
    "Relationship",
    "Assumption",
    "SupportProfile",
    "build_graph",
    "analyze",
    "write_bundle",
    "verify_bundle",
]
