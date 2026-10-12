---
name: leak-check
description: "Check a built bundle for anything that hands the solver the answer or the author's intent: golden figures in a memo, the stump's vocabulary in a filed document, a sentence that announces the decisive step, a file name that names the trap, hidden sheets or tracked changes, toolchain signatures, a shipped artifact that ranks the candidates, dates after the setting, a prompt that fails the prompt gate. leak.py runs eleven mechanical sweeps and writes leak_check_report.md; the /leak-check command adds one solver's-eye read by one isolated agent. Stage 4 of the build pipeline, together with the duplicate check and before the determinism judge; leak.py again after any rebuild, the reader again only when a document or the prompt changed."
---

# Leak check

A leak is the author's text (the submission's answers, the design note's stump sentence, the generator's
library names) turning up in `prompt.txt` or under `target/`. `leak.py` looks for it mechanically; one
reader then reads the pack as a solver would.

## When

- **Stage 4 of `/build`**, after the build stage's free gates (generator checks, `figures_check.py`, the
  realism sweep, `guard.py heart`), spawned beside the determinism judge in the background. Every finding (a LEAK, a quoted question-1 sentence, a question-2 or question-3
  file, a question-5 sentence that does not execute to the golden, a main-call fork, a realism tell, an
  ask-figure fork) is fixed in the generator in the same pass as the judge's findings.
- **`leak.py` after every rebuild** and after any edit to a document under `target/`.
- **The reader once per build**, at medium effort, after the realism sweep (so it confirms realism
  rather than finds it; repeated passes cost task132 and task180 most of a day), and again only when a fix
  changed a document or the prompt. A data-only repair is checked by `leak.py` alone.
- Before `/approve`, which refuses a build whose last report is LEAK.
- **Returned tasks** (`/fix-determinism`, `/fix-rubric`): `leak.py` only, no reader.

## The mechanical half: `leak.py`

```
python3 .claude/skills/leak-check/leak.py task100 --asof 2027-05-14
```

`--asof` is the fiction's as-of date from the design note's `## Draw`; without it sweep 9 is skipped. Exit
2 LEAK, 1 REVIEW, 0 CLEAN; the report overwrites `<task>/leak_check_report.md`. The prompt is
`prompt.txt` (a legacy `prompt.md` is named as such). Figures the prompt states, or listed under
`stated_inputs` in `metadata.json`, are not leaks.

| Sweep | Hunts |
|---|---|
| 1 file names | author nouns (`trap`, `golden`, `clean_`, `_v2`, `answer`), dot and system files, code in the pack |
| 2 author vocabulary | `rung`, `decoy`, `the solver`, `rubric`, `placeholder`, library names, home paths, `claude`, em dashes (data files: toolchain terms only); a sentence saying the pack was built (`constructed for this exercise`, `are invented`, `are fictional`) is LEAK in any file, the bare words `fictional`, `fictitious`, `this exercise` REVIEW in documents (`reduce-house-fixes` H24) |
| 3 answer figures | a golden figure (4+ digits) from blocks 1 and 4 in a document is LEAK; a candidate beside decision vocabulary, or a long figure in data, is REVIEW |
| 4 design-note vocabulary | a document with 3+ of the stump paragraph's distinctive terms, a prompt sentence with 2 |
| 5 announcements | `make sure`, `note that`, `must ... exclude`, `the correct basis`: the sentence naming the decisive step |
| 6 ranking artifacts | a file naming most candidates beside numbers (Gate G); a declared wrong-basis distractor is the one exception |
| 7 hidden content | hidden sheets, rows, columns, defined names, comments, tracked changes, hidden text, annotations, embedded files, nested zips |
| 8 column names | `_true`, `is_`, `flag`, `seed`, `planted`, `debug`; Python nulls and booleans |
| 9 dates | ISO dates after `--asof` that the prompt does not carry |
| 10 container | writer signature or out-of-band timestamp (`reduce-house-fixes` H1 script) |
| 11 prompt gate | `voice-check.py` on `prompt.txt`: a markdown character or line break is LEAK, any other failing rule REVIEW (all REVIEW on legacy `prompt.md`) |

LEAK stops the ship and is fixed in the generator, never by hand. Each REVIEW line gets one line in the
design note saying why it is harmless, or a fix.

**What it cannot see:** a sentence naming the move in other words; a document teaching the method by
example; a file whose presence is the hint; an ordinary column whose values partition the candidates on
the decisive property; a filed sentence whose literal execution is the easy answer.

## The reader: `/leak-check`

`/leak-check taskNN` runs `leak.py`, then one isolated Sonnet agent at medium that sees only fresh copies of
`prompt.txt` and `target/`, never the design note, generator, submission or report. It answers as a solver:

1. Which sentence or file tells you the decisive step? Quote it.
2. Which file already ranks or scores the candidates on the prompt's question?
3. Which file exists only to help the analyst?
4. Which figure or name reads as the answer rather than context?
5. Which filed sentence, read literally, fixes how the main figure is computed or over which population?
   Quote it and give its literal result. The main thread checks it is the golden; if it is the easy
   answer it is a main-call fork (`determinism-check` §1).

Answers append to the report under `## Solver's-eye read`, with a verdict on each REVIEW line. The main
thread rules fix or harmless per line, harmless ones one line each in the design note.

## Not a leak

- A figure the prompt states or `stated_inputs` lists.
- A governing clause that pins a convention once. The test: would the sentence exist without the trap?
- A real-world string in a real dataset.
- A confirming corpus the strategy needs (a sentence pointing at it would be).

## Checklist

- [ ] `leak.py --asof` CLEAN or REVIEW, sweep 11 clean; every REVIEW answered or fixed
- [ ] Reader run once after the realism sweep: nothing quoted for question 1, every question-5 sentence executes to the golden
- [ ] All reader findings fixed in the generator before the judge; `leak.py` re-run after every rebuild
