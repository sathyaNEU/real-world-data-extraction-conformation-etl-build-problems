# task203_ext

A **raw dataset drop**, not a task.

| field | value |
|---|---|
| domain | General Statistics & Data Science |
| task type | benchmarking-and-ablations |
| contents | `target/` only, 14 files, 6 formats |
| largest file | `runs_2026.jsonl`, 26,780 records |
| provenance | synthetic, written by `generator/make.py` at seed 20261019 |
| determinism | two consecutive builds are byte-identical, workbook container included |
| licence | internal; nothing here is derived from a third-party dataset |

## What it deliberately does not have

There is **no stump**. Nothing in this corpus was placed to be got wrong, and the pipeline
machinery that exists to enforce a stump does not apply:

- no `prompt.txt`, no question, no committed call
- no `submission.md`, no golden deliverable, no `figures.json`
- no design note, no default path, no ladder, no readability screen, no fork table
- no supplementary asks and no devices
- no planted defect, no decoy, no withheld rule, no distractors
- no fingerprint card registered, so `guard.py` holds no axis on this number and it bans nothing

The rough edges in the data are the ordinary unconformed state of a real export, not traps: layouts
that changed between exporters, two clocks, heterogeneous metric keys, three spellings of the same
host, inconsistent version strings, crashed runs with no metrics, a re-export that repeated part of
a quarter, and a hand-kept spreadsheet that is behind the system of record. All eleven are listed
in `target/MANIFEST.md` in the group's own words, so a reader can conform the corpus without
guessing, and anyone who later wants to build a task on top of this starts from scratch.

## Regenerating

    cd task203_ext && python3 -I generator/make.py

The generator reads no clock and takes one seed, so the rebuild is byte-identical. The workbook is
re-serialised after openpyxl writes it, which fixes the zip member dates and replaces the
library's own `dc:creator` stamp, since otherwise every rebuild would differ and the file would
carry a writing-library signature.
