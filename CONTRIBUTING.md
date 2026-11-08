# Contributing

This is a side project. A session can be an hour. The subject can be anything you have a file for.

## Run

```bash
git clone https://github.com/dennis430/checkable.git
cd checkable
pip install pytest pydantic networkx click cryptography
./checkable test
./checkable demo
```

Node 20 or newer. Python 3.10 or newer.

## While you change it

- Keep a check strict. Do not loosen a verifier so a demo passes.
- A new example can be about any subject. Put it in `playground/` or in the package that owns that check.
- Do not move code from `packages/genesis-verifier/` into an MIT file. That package is Apache-2.0. See `NOTICE.md`.
- Do not add a hosted service, an account, or a model call to the default path.
- Do not write a model answer into `packages/model-evidence-archive/records/public/` unless a collector captured those bytes and the hash still matches.
- Issues are the list of work. Small pull requests are the way in.

## Layout

| Path | What you edit it for |
|---|---|
| `tools/quote-receipt.mjs` | Turning a file and a sentence into a receipt |
| `packages/genesis-verifier/` | Recomputing a receipt against bytes |
| `packages/source-dependence/` | Shared origins, cycles, unknown lineage |
| `packages/model-evidence-archive/` | Storing a model answer that was actually collected |
| `playground/` | A file from whatever you are working on |
