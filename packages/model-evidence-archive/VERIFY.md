# Verifying a record

A record is a JSON object written by `src/collector/collector.py`.

Historical records have:

- `is_historical: true`
- `raw_response`: the response text the adapter captured
- `hash`: hex SHA-256 of the UTF-8 bytes of `raw_response`
- `probe_id`, `model`, `collected_at`, `method`

Check one file:

```bash
python scripts/verify_record.py records/public/some-record.json
```

`hash_ok: true` means the hash matches those bytes. It does not mean the provider signed the response, and it does not mean the answer is right.

`historical: false` means the file is not an archive record. The offline fixture is in that class even if its hash matches its own text.

If `is_historical` is true and the hash does not match, the script exits 1. Do not "fix" that by editing `raw_response` or by recalculating the hash over a revised text. Keep the failure.
