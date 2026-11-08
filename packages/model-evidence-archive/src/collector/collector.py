"""Executable collector.

Offline fixtures are for tests. They are not historical observations.
A live call is persisted only when the adapter marked it historical and the
stored hash matches the captured response bytes. Existing files are not rewritten.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PANEL_PATH = Path("probes/panel_v1.json")


def load_panel() -> dict:
    return json.loads(PANEL_PATH.read_text())


def collect_offline_fixture() -> dict:
    """Quarantined synthetic response for testing only. Never treated as historical."""
    text = "Under declared copy model, one independent observation."
    return {
        "probe_id": "p1_duplicate",
        "model": "synthetic-fixture",
        "response_text": text,
        "raw_response": text,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "method": "offline_fixture",
        "hash": hashlib.sha256(text.encode()).hexdigest(),
        "is_historical": False,
        "notes": "Quarantined test fixture; not a real provider response.",
    }


def check_access() -> dict:
    """Report access status without making requests if no secrets."""
    has_openai = bool(os.environ.get("OPENAI_API_KEY"))
    has_anthropic = bool(os.environ.get("ANTHROPIC_API_KEY"))
    has_google = bool(os.environ.get("GOOGLE_API_KEY"))
    return {
        "openai": "AVAILABLE" if has_openai else "MISSING_SECRET",
        "anthropic": "AVAILABLE" if has_anthropic else "MISSING_SECRET",
        "google": "AVAILABLE" if has_google else "MISSING_SECRET",
        "overall": "PAUSED_ACCESS" if not (has_openai or has_anthropic or has_google) else "PARTIAL",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def verify_record(record: dict) -> dict:
    """Check a stored record. A fixture is not promoted by a matching hash."""
    if record.get("is_historical") is not True:
        return {
            "historical": False,
            "hash_ok": "NOT_APPLICABLE",
            "note": "Not an archive record. Hash is not treated as provenance.",
        }
    raw = record.get("raw_response")
    if not isinstance(raw, str) or not record.get("hash"):
        return {"historical": True, "hash_ok": False, "note": "Historical flag set without raw_response and hash."}
    actual = hashlib.sha256(raw.encode()).hexdigest()
    return {
        "historical": True,
        "hash_ok": actual == record.get("hash"),
        "actual": actual,
        "claimed": record.get("hash"),
        "note": "Hash covers the captured response bytes only. It does not authenticate the provider.",
    }


def persist_historical(results: list[dict], write_dir: Path) -> list[str]:
    """Write historical rows. Refuse to replace a file with different bytes."""
    write_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for row in results:
        if row.get("is_historical") is not True:
            continue
        check = verify_record(row)
        if check.get("hash_ok") is not True:
            row["status"] = "HASH_MISMATCH"
            row["is_historical"] = False
            continue
        stamp = str(row.get("collected_at", "undated")).replace(":", "")
        raw_name = f"{stamp}_{row.get('model', 'model')}_{row.get('probe_id', 'probe')}.json"
        safe = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in raw_name)
        path = write_dir / safe
        payload = json.dumps(row, indent=2) + "\n"
        if path.exists():
            existing = json.loads(path.read_text())
            if existing.get("raw_response") != row.get("raw_response") or existing.get("hash") != row.get("hash"):
                raise RuntimeError(f"refusing to rewrite {path}")
        else:
            path.write_text(payload)
        written.append(str(path))
    return written


def _live_results(panel: dict, access: dict, adapter: Any) -> list[dict]:
    results: list[dict] = []
    if adapter is not None:
        for probe in panel.get("probes", []):
            results.append(adapter.collect(probe))
    elif access.get("openai") == "AVAILABLE":
        from .adapters import OpenAIAdapter, UrllibTransport

        built = OpenAIAdapter(UrllibTransport(), os.environ.get("OPENAI_API_KEY"))
        for probe in panel.get("probes", []):
            results.append(built.collect(probe))
    for provider in ("anthropic", "google"):
        if access.get(provider) == "AVAILABLE":
            results.append(
                {
                    "provider": provider,
                    "status": "ADAPTER_NOT_IMPLEMENTED",
                    "is_historical": False,
                    "note": "Secret is present. This version has no adapter. No response was invented.",
                }
            )
    return results


def run_collection(dry_run: bool = True, adapter: Any = None, write_dir: Path | None = None) -> dict:
    panel = load_panel()
    access = check_access()
    if dry_run or access["overall"] == "PAUSED_ACCESS":
        return {
            "panel_version": panel.get("version"),
            "access": access,
            "results": [collect_offline_fixture()],
            "records_written": [],
            "note": "No live provider calls made. Offline fixture only for testing. The fixture is not a historical record.",
        }

    results = _live_results(panel, access, adapter)
    written: list[str] = []
    if write_dir is not None:
        written = persist_historical(results, write_dir)
    return {
        "panel_version": panel.get("version"),
        "access": access,
        "results": results,
        "records_written": written,
        "note": "Only rows with is_historical true and a matching raw_response hash are written. Failures are kept in results and are not archive records.",
    }
