---
name: leak-check
description: "Check a built bundle for anything that hands the solver the answer or the author's intent: golden figures in a memo, the stump's vocabulary in a filed document, a sentence that announces the decisive step, a file name that names the trap, hidden sheets or tracked changes, toolchain signatures, a shipped artifact that ranks the candidates, dates after the setting. leak.py runs eleven mechanical sweeps and writes leak_check_report.md; the /leak-check command adds a solver's-eye read by one isolated agent. Run after the pack is cut and again after any edit to a document in target/. Costs nothing unless the command's agent pass is asked for."
---

# Leak check

> Everything the author knows and the solver must not be told is written down somewhere in the
> task folder: the submission's answers, the design note's stump sentence, the generator's library
> names. A leak is any of that text turning up in `prompt.md` or under `target/`. So the check takes
> the author's text and looks for it in the solver's text, which is mechanical, and then reads the
> pack once as a solver would, which is not.

## When to run it

- After the pack is cut and the submission is written, before `golden-realism` (so a figure a
  realism edit copies into a memo is caught on the second run too).
- After **any** edit to a document under `target/`, because documents are where leaks live: a
  memo written to add texture is the usual carrier.
- Before `/approve`, which refuses a build whose last report is LEAK.

## The mechanical half: `leak.py`

```
python3 .claude/skills/leak-check/leak.py task100 --asof 2027-05-14
```

`--asof` is the fiction's as-of date, read from the design note's DRAW block; without it the date
sweep is skipped and says so. Exit status: 2 LEAK, 1 REVIEW, 0 CLEAN. The report goes to
`<task>/leak_check_report.md` and is overwritten on every run, because it is a mechanical screen
and the current one is the only one that matters.

| Sweep | What it reads | What it hunts |
|---|---|---|
| 1 file names | every path under `target/` | the author's nouns (`trap`, `golden`, `clean_`, `_v2`, `answer`), stray dot and system files, code shipped in the pack |
| 2 author vocabulary | documents (and data for toolchain terms only) | `rung`, `decoy`, `the solver`, `rubric`, `placeholder`, library names, home paths, `claude`, em dashes |
| 3 answer figures | every file, against block 1 and block 4 of `submission.md` | a golden figure (four or more digits) in a document is LEAK; a candidate name beside decision vocabulary in a document is REVIEW; a long figure in a data file is REVIEW |
| 4 design-note vocabulary | documents and the prompt, against the stump and driver paragraphs of `DESIGN_NOTE.md` | a document carrying three or more of the stump's distinctive terms; a prompt sentence carrying two |
| 5 announcements | prompt and documents | `make sure`, `note that`, `must ... exclude`, `the correct basis`, `instead of ... counting rows`: the sentence that announces the decisive step |
| 6 ranking artifacts | every file | a file naming most of the answer-set candidates beside numbers, which the reader checks against Gate G's loud-artifact ban; the distractor declared in `metadata.json` is the one licensed exception |
| 7 hidden content | xlsx, docx, pdf containers | hidden sheets, rows and columns, defined names, comments, tracked changes, hidden text, annotations, embedded files, nested zips |
| 8 column names | delimited and workbook headers | `_true`, `is_`, `flag`, `seed`, `planted`, `debug`; Python nulls and booleans in the first rows |
| 9 dates after the setting | every file, with `--asof` | ISO dates later than the as-of date that the prompt does not itself carry |
| 10 container metadata | the bundle, via `reduce-house-fixes` H1's audit script | a writer signature or an out-of-band timestamp |
| 11 prompt form | `prompt.md` | bracketed blocks, `file.ext (Family)` headers, bulleted asks, a method enumerated in the prompt |

**Reading the report.** LEAK is ship-stopping and is fixed in the generator, never by hand in the
file (the next rebuild would reintroduce it). REVIEW is a reader's call: most REVIEW lines on a
sound build are the pack's own vocabulary overlapping the stump's (a circular that says `census`
is not a leak), and the reader's job is to say in one line why each one is harmless or to fix it.
The solver's-eye pass below reads every REVIEW line.

**What the mechanical half cannot see**, and why the second half exists: a sentence that names
the move without using the design note's words; a document that teaches the method by example; a
file whose mere presence is the hint (a prior-period snapshot shipped with no in-fiction reason to
exist); a column whose name is an ordinary word but whose values partition the candidates on the
decisive property.

## The reader's half: the `/leak-check` command

`/leak-check taskNN` runs `leak.py` and then spawns **one** isolated agent that sees only a fresh
copy of `prompt.md` and `target/` in the scratch directory, never the design note, the generator,
the submission or the report. It is asked four questions as a solver, not as a reviewer:

1. Which sentence or file, if any, tells you what the decisive step of this analysis is? Quote it.
2. Which file, if any, already ranks or scores the candidates on the question the prompt asks?
3. Which file has no reason to exist in this organisation's folder except to help the analyst?
4. Which figure or name in the documents reads as the answer rather than as context?

Its answers are appended to `leak_check_report.md` under `## Solver's-eye read`, with the reader's
verdict on each REVIEW line of the mechanical half. The main thread then decides, line by line,
fix or harmless, and writes the harmless ones into the design note in one line each.

## What is not a leak

- A figure the prompt itself states (a budget, a cap, a date). The sweep excludes these.
- A governing clause that pins a convention. Pinning is required by `determinism-check`; a pin is a
  rule stated once in a filed document, and a leak is the pack telling the solver *which* rule
  matters here. The test is whether the sentence would exist if the trap did not.
- A real-world string in a real dataset (an electoral division called GOLDEN). Data files are swept
  for toolchain terms only.
- The calibration corpus. It is supposed to be there and it is supposed to be used; the leak would
  be a sentence pointing at it.

## Checklist

- [ ] `leak.py` run with `--asof`, verdict CLEAN or REVIEW, never LEAK
- [ ] Every REVIEW line answered in one line in the design note, or fixed in the generator
- [ ] The solver's-eye read run once after the final cut, with no sentence quoted for question 1
- [ ] Re-run after every document edit under `target/`
