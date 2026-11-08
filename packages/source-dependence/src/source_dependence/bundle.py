"""Portable reconciliation bundles. Integrity verification independent of analytical engine.

Uses maintained crypto libraries. Specifies exact bytes hashed. Does not invent cryptography.
Successful verification of integrity does not imply lineage independently established.
Reproducibility requires actual re-execution of a supported engine version; it is not inferred from hash match.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

BUNDLE_VERSION = "reconciliation.bundle.v1"


def _canonical(obj: Any) -> bytes:
    """Deterministic JSON canonicalization for hashing."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def write_bundle(
    manifest: dict,
    report: dict,
    assumptions: list,
    analytical_version: str,
    integrity_material: dict | None = None,
) -> dict:
    bundle = {
        "version": BUNDLE_VERSION,
        "manifest": manifest,
        "assumptions": assumptions,
        "analytical_version": analytical_version,
        "report": report,
        "integrity": integrity_material or {},
    }
    content_hash = hashlib.sha256(_canonical({k: v for k, v in bundle.items() if k != "integrity"})).hexdigest()
    bundle["integrity"]["content_sha256"] = content_hash
    return bundle


def verify_bundle(path: Path | dict) -> dict:
    """Verify and label each property separately.

    Statuses: PASS, FAIL, NOT_PRESENT, NOT_CHECKED, UNSUPPORTED, MISSING_INPUT.
    analysis_reproducible is NOT_RUN until an explicit re-execution path succeeds.
    """
    if isinstance(path, Path):
        bundle = json.loads(path.read_text())
    else:
        bundle = path

    result = {
        "schema_version_valid": bundle.get("version") == BUNDLE_VERSION,
        "envelope_commitment_consistent": False,
        "artifact_bytes_verified": "NOT_CHECKED",
        "signature_verified": "NOT_CHECKED",
        "timestamp_verified": "NOT_PRESENT",
        "analysis_reproducible": "NOT_RUN",
        "lineage_independently_established": False,
        "notes": [],
        "exit_code_recommended": 0,
    }

    expected = bundle.get("integrity", {}).get("content_sha256")
    content = {k: v for k, v in bundle.items() if k != "integrity"}
    actual = hashlib.sha256(_canonical(content)).hexdigest()
    result["envelope_commitment_consistent"] = expected == actual
    if not result["envelope_commitment_consistent"]:
        result["notes"].append("Envelope content hash mismatch.")
        result["exit_code_recommended"] = 1
    else:
        result["notes"].append("Envelope hash matches; this is self-consistency only, not origin authentication.")

    if "signature" in bundle.get("integrity", {}):
        result["signature_verified"] = "NOT_CHECKED"
        result["notes"].append("Signature material present but no trust policy applied in this verifier version.")

    result["analysis_reproducible"] = "NOT_RUN"
    result["notes"].append("Analysis re-execution not performed; status is NOT_RUN until a supported engine is invoked and report compared.")

    result["notes"].append("No check above establishes independent lineage or real-world claim truth.")
    return result
