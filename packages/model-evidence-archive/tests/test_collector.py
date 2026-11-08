from src.collector.collector import check_access, collect_offline_fixture, run_collection

def test_access_missing():
    status = check_access()
    assert status["overall"] == "PAUSED_ACCESS"

def test_fixture_not_historical():
    fix = collect_offline_fixture()
    assert fix["is_historical"] is False
    assert "synthetic" in fix["model"]

def test_run_dry():
    out = run_collection(dry_run=True)
    assert out["access"]["overall"] == "PAUSED_ACCESS"
    assert any(not r.get("is_historical", True) for r in out["results"])
