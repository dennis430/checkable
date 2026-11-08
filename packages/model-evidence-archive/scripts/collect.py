#!/usr/bin/env python3
"""Run the collector.

Default is dry-run: write a coverage status and no archive records.
--live calls configured adapters. Historical rows go to --records-dir
(default records/incoming), which is gitignored. Copy reviewed files into
records/public without editing response bytes.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.collector.collector import run_collection  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--records-dir", default="records/incoming")
    parser.add_argument("--status", default="status/coverage.json")
    args = parser.parse_args()
    status_path = ROOT / args.status
    write_dir = ROOT / args.records_dir if args.live else None
    # load_panel reads a relative path, so run from the repo root.
    import os

    os.chdir(ROOT)
    result = run_collection(dry_run=not args.live, write_dir=write_dir)
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status_path": str(status_path), "records_written": result.get("records_written", []), "access": result["access"]["overall"]}, indent=2))


if __name__ == "__main__":
    main()
