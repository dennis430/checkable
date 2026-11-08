"""Provider adapters. Transport is injectable so tests never hit the network.

Synthetic transports are not a source of historical records. The caller decides
is_historical. This module sets it true only after a transport returned bytes.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Protocol
from urllib.request import Request, urlopen


class Transport(Protocol):
    def post(self, url: str, headers: dict, json: dict) -> dict: ...


class UrllibTransport:
    """Real HTTP transport. Used only when a live collection is requested."""

    def post(self, url: str, headers: dict, json: dict) -> dict:
        body = json_dumps(json)
        req = Request(
            url,
            data=body,
            headers={**headers, "Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(req, timeout=60) as resp:
            return json_loads(resp.read().decode())


def json_dumps(payload: dict) -> bytes:
    return json.dumps(payload).encode()


def json_loads(payload: str) -> dict:
    return json.loads(payload)


class OpenAIAdapter:
    def __init__(self, transport: Transport, api_key: str | None = None):
        self.transport = transport
        self.api_key = api_key

    def collect(self, probe: dict) -> dict:
        if not self.api_key:
            return {"status": "MISSING_SECRET", "probe_id": probe.get("id"), "is_historical": False}
        payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": probe.get("text", "")}]}
        try:
            resp = self.transport.post(
                "https://api.openai.com/v1/chat/completions",
                {"Authorization": f"Bearer {self.api_key}"},
                payload,
            )
            raw = resp.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {
                "probe_id": probe.get("id"),
                "model": "gpt-4o-mini",
                "raw_response": raw,
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "method": "openai_adapter",
                "hash": hashlib.sha256(raw.encode()).hexdigest() if isinstance(raw, str) else None,
                "is_historical": True,
                "status": "success",
            }
        except Exception as exc:
            return {"status": "error", "error": str(exc), "probe_id": probe.get("id"), "is_historical": False}


class MockTransport:
    """Synthetic transport for tests only. Never used for historical records by itself."""

    def post(self, url: str, headers: dict, json: dict) -> dict:
        return {"choices": [{"message": {"content": "Mock response: one independent observation under declared copy."}}]}
