#!/usr/bin/env python3
"""Recompute the response hash of one JSON record. Exit 1 on a failed historical record."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.collector.collector import verify_record  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python scripts/verify_record.py <record.json>", file=sys.stderr)
        sys.exit(64)
    record = json.loads(Path(sys.argv[1]).read_text())
    result = verify_record(record)
    print(json.dumps(result, indent=2))
    if result.get("historical") is True and result.get("hash_ok") is not True:
        sys.exit(1)


if __name__ == "__main__":
    main()
