#!/usr/bin/env python3
"""Stateful daily controller. Loads prior state if present; preserves terminal states; fails closed on missing required files for integrity."""
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

STATE_PATH = Path("state/daily_state.json")
LEDGER_PATH = Path("state/decision_ledger.jsonl")

def load_prior() -> dict | None:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            return None
    return None

def main():
    now = datetime.now(timezone.utc).isoformat()
    prior = load_prior()
    if prior and prior.get("status") in ("FROZEN_UNPROVEN", "FROZEN_NO_ADVANTAGE", "ARCHIVED", "INVALID_METHOD"):
        state = prior.copy()
        state["last_check"] = now
        state["notes"] = state.get("notes", []) + ["Terminal state preserved; no re-activation"]
        result_ok = True
    else:
        state = prior.copy() if prior else {"status": "LIVE_TRIAL", "notes": []}
        state["last_check"] = now
        state["status"] = state.get("status", "LIVE_TRIAL")
        py_path = Path("pyproject.toml")
        if not py_path.exists():
            state["notes"] = state.get("notes", []) + ["integrity_fail: pyproject.toml missing"]
            state["status"] = "INTEGRITY_FAIL"
            result_ok = False
        else:
            state["pyproject_sha256"] = hashlib.sha256(py_path.read_bytes()).hexdigest()[:16]
            result_ok = True
    STATE_PATH.parent.mkdir(exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))
    with LEDGER_PATH.open("a") as f:
        f.write(json.dumps({"ts": now, "action": "daily_status", "status": state["status"], "ok": result_ok}) + "\n")
    print(json.dumps({"ok": result_ok, "status": state["status"], "state_written": str(STATE_PATH), "ts": now}))

if __name__ == "__main__":
    main()
