# checkable

Open source. [MIT License](LICENSE), except [`packages/genesis-verifier`](packages/genesis-verifier/LICENSE), which is Apache-2.0. No contributor agreement.

Side project. Check a claim against the bytes it cites, and notice when two reports are the same source.

Any subject, as plain text. A note, a log, a markdown file, or source code. There is no server and no account. Node 20 or newer, and Python 3.10 or newer for the dependence and archive packages.

This repository is where those three packages are worked on together:

| Package | License | What it does |
|---|---|---|
| `packages/genesis-verifier` | Apache-2.0 | Recompute a receipt against a file. |
| `packages/source-dependence` | MIT | Tell a repeated report from a second origin. |
| `packages/model-evidence-archive` | MIT | Keep a model answer only if it was actually collected. |

The older repositories stay up as package history. New work goes here.

## Files that work

There is no upload site. The command reads a file on disk.

`./checkable quote` finds an exact sentence only when those characters are stored in a row in the file. It does not open Word, Excel, or a photo.

| File | `quote` | Notes |
|---|---|---|
| `.txt`, `.md`, `.log`, source code | Yes | The sentence must occur once unless you explicitly select an occurrence with `--nth`. A second copy is otherwise a refusal, not a guess. |
| `.csv` saved as plain text | Yes, for a sentence. Sums of dollar amounts need a receipt, not `quote`. | LF or CRLF both work for a quotation. The CSV profiles are stricter and are for cell checks. |
| `.html` | Only if the sentence is not split by tags | `<b>closed</b>` is not the word `closed`. |
| PDF with real text | No | A scan, a photo, an encrypted PDF, or a custom font is unverifiable. A simple text PDF can be checked by the PDF profile, not by `quote`. |
| `.docx`, `.xlsx`, `.png`, `.jpg` | No | Export `.txt` or a plain `.csv` first. |

Send a `.txt` or `.md` file and the exact sentence copied from it. That is enough to run.

```bash
git clone https://github.com/dennis430/checkable.git
cd checkable
pip install pytest pydantic networkx click cryptography
./checkable quote path/to/file.txt "the exact sentence"
./checkable genesis path/to/file.txt receipt.json
```

`quote` writes a receipt only when that exact text occurs once, or when you explicitly select a match with a positive, one-based index: `./checkable quote path/to/file.txt "the exact sentence" --nth 2`. Without `--nth`, two matches is a refusal, not a guess. An out-of-range index also fails without writing a receipt. `genesis` then re-reads the file. Exit 0 means the span and the hash reproduced. It does not mean the file is genuine, the sentence is true, or anybody should act on it.

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
