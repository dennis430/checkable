from src.collector.adapters import OpenAIAdapter, MockTransport

def test_adapter_with_mock_transport():
    adapter = OpenAIAdapter(transport=MockTransport(), api_key="dummy")
    probe = {"id": "p1", "text": "test probe"}
    result = adapter.collect(probe)
    assert result["status"] == "success"
    assert result["is_historical"] is True
    assert "Mock response" in result["raw_response"]
    assert result["hash"] is not None

def test_adapter_missing_key():
    adapter = OpenAIAdapter(transport=MockTransport(), api_key=None)
    result = adapter.collect({"id": "p1"})
    assert result["status"] == "MISSING_SECRET"
    assert result["is_historical"] is False
