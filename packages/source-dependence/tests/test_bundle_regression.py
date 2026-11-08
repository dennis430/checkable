"""Regression: analysis_reproducible must not be inferred from envelope hash."""
import hashlib
import json
from source_dependence.bundle import verify_bundle

def test_r04_not_run():
    bad = {
        "version": "reconciliation.bundle.v1",
        "manifest": {},
        "assumptions": [],
        "analytical_version": "nonexistent-999",
        "report": {"fake": True},
        "integrity": {},
    }
    content = {k: v for k, v in bad.items() if k != "integrity"}
    h = hashlib.sha256(json.dumps(content, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    bad["integrity"]["content_sha256"] = h
    result = verify_bundle(bad)
    assert result["analysis_reproducible"] == "NOT_RUN"
    assert result["envelope_commitment_consistent"] is True
    assert result["lineage_independently_established"] is False
