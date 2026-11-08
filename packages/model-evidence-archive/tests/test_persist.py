import hashlib
import json
from pathlib import Path

from src.collector.adapters import MockTransport, OpenAIAdapter
from src.collector.collector import persist_historical, run_collection, verify_record


def test_dry_run_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    out = run_collection(dry_run=True, write_dir=tmp_path)
    assert out["records_written"] == []
    assert list(tmp_path.iterdir()) == []
    assert out["results"][0]["is_historical"] is False


def test_live_mock_persists_and_refuses_rewrite(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    adapter = OpenAIAdapter(MockTransport(), api_key="test-key")
    first = run_collection(dry_run=False, adapter=adapter, write_dir=tmp_path)
    assert first["records_written"]
    assert all(item["is_historical"] is True for item in first["results"] if item.get("status") == "success")
    saved = json.loads(Path(first["records_written"][0]).read_text())
    assert verify_record(saved)["hash_ok"] is True
    again = run_collection(dry_run=False, adapter=adapter, write_dir=tmp_path)
    assert again["records_written"]
    # same captured text may differ in collected_at, so a second file is allowed
    # a rewrite of an existing path with different bytes is not
    target = Path(first["records_written"][0])
    mutated = dict(saved)
    mutated["raw_response"] = "changed"
    mutated["hash"] = hashlib.sha256(b"changed").hexdigest()
    try:
        persist_historical([mutated], tmp_path)
    except RuntimeError as exc:
        assert "refusing to rewrite" in str(exc)
    else:
        # persist uses collected_at in the filename; force the collision
        mutated["collected_at"] = saved["collected_at"]
        try:
            persist_historical([mutated], tmp_path)
            raise AssertionError("rewrite was accepted")
        except RuntimeError as exc:
            assert "refusing to rewrite" in str(exc)
    assert target.read_text() == Path(first["records_written"][0]).read_text()


def test_unimplemented_provider_is_not_a_record(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "present")
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    out = run_collection(dry_run=False, write_dir=tmp_path)
    assert any(row.get("status") == "ADAPTER_NOT_IMPLEMENTED" for row in out["results"])
    assert out["records_written"] == []
    assert not any(row.get("is_historical") for row in out["results"])
