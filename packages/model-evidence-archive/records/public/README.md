# records/public

No authentic provider responses are stored here.

When a live collection has produced a file under `records/incoming/`:

1. Run `python scripts/verify_record.py` on it.
2. Copy the file here without changing `raw_response` or `hash`.
3. Update `COVERAGE.md` with the new count in the same commit.

Do not add a response that was typed, paraphrased, or reconstructed from memory.
