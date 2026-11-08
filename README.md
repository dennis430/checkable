# checkable

Open source. [MIT License](LICENSE), except [`packages/genesis-verifier`](packages/genesis-verifier/LICENSE), which is Apache-2.0. No contributor agreement.

Side project. Check a claim against the bytes it cites, and notice when two reports are the same source.

Any subject. A contract, a paper, a log, a note, a spreadsheet export. There is no server and no account. Node 20 or newer, and Python 3.10 or newer for the dependence and archive packages.

This repository is where those three packages are worked on together:

| Package | License | What it does |
|---|---|---|
| `packages/genesis-verifier` | Apache-2.0 | Recompute a receipt against a file. |
| `packages/source-dependence` | MIT | Tell a repeated report from a second origin. |
| `packages/model-evidence-archive` | MIT | Keep a model answer only if it was actually collected. |

The older repositories stay up as package history. New work goes here.

## Use it on a file you already have

```bash
git clone https://github.com/dennis430/checkable.git
cd checkable
pip install pytest pydantic networkx click cryptography
./checkable quote path/to/file.txt "the exact sentence"
./checkable genesis path/to/file.txt receipt.json
```

`quote` writes a receipt only when that exact text occurs once. Two matches is a refusal, not a guess. `genesis` then re-reads the file. Exit 0 means the span and the hash reproduced. It does not mean the file is genuine, the sentence is true, or anybody should act on it.

If you have two reports and you already know one copies the other:

```bash
./checkable analyze playground/dependence/shared-origin.json
```

`observations_counted` is 2. `distinct_documented_origin_group_count` is 1. The origin group is whatever you wrote down. The tool does not discover it for you.

```bash
./checkable demo
./checkable test
```

`demo` uses a field note in `playground/`, not an invoice. `test` runs the quote tool, all three packages, and that field note.

## What a pass is not

A reproduced quotation is not authenticity. A shared origin is not a finding that the claim is false. A bundle hash is not a signature. An empty archive is not a sample of model behavior. Those limits are the point of the code. They stay in force no matter what file you point it at.

## Work on it

`CONTRIBUTING.md` is the short version. Open an issue for the next hour of work. A new domain does not need a new architecture. It needs a file, a receipt, and a test that fails when the check is weakened.
