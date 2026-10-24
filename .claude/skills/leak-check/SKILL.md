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
- **Returned tasks** (`/fix-determinism`, `/fix-rubric`): `leak.py` after every rebuild, and **the reader
  again whenever the repair added or reworded a sentence under `target/` or in the prompt**. A determinism
  repair closes a fork by filing something, and the sentence that fixes a basis can name the move:
  task196's repair added one line to an operations note to close a fork the records already closed by
  convergence, `leak.py` saw nothing, and the next reader quoted that line as what pointed it at the
  decisive step and landed the call exactly. A data-only repair is still `leak.py` alone.

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

`leak.py` **carries the reader's section across a rewrite**: anything from the `## Solver's-eye read`
heading onward in the existing report is preserved, because the sweeps are this script's output while the
read is evidence it did not produce. Before that, a repair pass that re-ran the sweeps silently destroyed
the read that had found its defect, and two passes in one sitting had to restore it from a transcript.

LEAK stops the ship and is fixed in the generator, never by hand. Each REVIEW line gets one line in the
design note saying why it is harmless, or a fix.

**What it cannot see:** a sentence naming the move in other words; a document teaching the method by
example; a file whose presence is the hint; an ordinary column whose values partition the candidates on
the decisive property; a filed sentence whose literal execution is the easy answer.

**The single-use test, run by the builder before the reader, because `leak.py` reads vocabulary and
figures and never purpose.** Of every file in the pack and every sentence a repair adds, ask what else
the organisation uses it for. A file with exactly one use, and that use being the decisive step,
announces it; so does a lone sentence whose only work is to make the solver notice a structure, and so
does a column of commentary that names what a source omits. What settles it is the deletion test from
`stumping` Part 4: take the file or the clause out and recompute, and if the answer stays forced it
handed over the insight and goes. Two stage-4 readers in one window landed the call and each named a
single-use artifact as what pointed it there: a close-out register whose only use was to show how
incomplete the recent counts were, and the repair-added line above, which the generator's own
measurement showed was unnecessary because the fork converged without it. The repair for an announcement
is to delete it, or to give the file the other uses its genre really has, never to redesign the decisive
step: `build-pipeline` classes a rung executed as a work order as announced, not as a design failure.

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
6. What decides the main answer: an analytical choice, reading one field, code, unit or definition
   correctly, following a stated rule or procedure, or catching something that looks planted? Quote the
   sentence or name the file that decides it. Anything but an analytical choice is a 10/10 rule 3 finding
   (`CLAUDE.md`, first section): the build goes back to stage 2.

Answers append to the report under `## Solver's-eye read`, with a verdict on each REVIEW line. The main
thread rules fix or harmless per line, harmless ones one line each in the design note.

**The stump-vocabulary sweep's lines never reach the reader.** Their parentheses list the stump
paragraph's own words, so handing them over tells the reader where the decisive step lives and turns its
call into an announced rung (`build-pipeline` Returned tasks), not a measurement. task305's third pair
both went first to the rating list's holiday parks at Wrentoft, the two words the sweep line named, and
both landed a call the four readers before them had missed. The main thread rules those lines itself;
question 1 asks the same thing cold.

**The reader also hands back every figure it committed to, as a JSON object keyed exactly as
`<task>/generator/figures.json` is keyed** (a nested value by a dotted key, `"a1_Norte.contacts": 1965`),
holding only the figures it actually answered. Score it before reading its verdict:

```
python3 .claude/skills/leak-check/score_reader.py taskNN <reader.json>   # 0 holds; 2 thin; 1 Gate F failed
```

A hit is an exact match at the golden's own precision. Exit 1 on a hit of the call, or on 35 per cent or
more of the ask figures: Gate F has failed, and **a reader hit means the device is absent from that
reader's path rather than weak**, so the repair re-sites the device and never re-words the ask
(`supplemental-stumping` 1.1c). Exit 2 between a fifth and 35 per cent names the ask that leaked. The
design note's cracker table is a model of the opponent written by the author; this is the measurement, and
it outranks the table. task190 architecture 6 shipped a cracker table claiming all three asks missed and a
`precut.py` pair ceiling of 28.5 through three stage 4 rounds; its round-3 reader reported 43 of 43.

**One reader is a sample, so the pack that ships is read twice.** Two isolated scored readers, each on its
own fresh copy, each scored with `score_reader.py`; the build ships when both miss the call and neither
exits 1. Readers on one pack differ by whole asks and by the call itself: three readers on task164's
frozen call split two landed and one missed, and on task162 and task165 one of two readers found an ask
device the other never saw. A call any reader lands is spent, whatever the other reader does.

## The scored read, and how its own harness leaks

A scored read hands the reader a list of figure names so its answers can be matched to the golden. **Those
names are part of the pack as the reader sees them, so a key that states the decisive quantity in words hands
over the step.** One audit handed a reader `sections_twice_failed_in_service` per candidate, and the reader's
own report then said nothing had told it to use a recurrent-failure model and that it inferred the repeat
pattern itself, which was false: the key names said it. Another was handed `rung0_count`, which is the
author's own ladder vocabulary.

So the handed list is built from the **Deliverable Answers the prompt actually asks for**, under the prompt's
own words, and the Critical Components keys are either relabelled neutrally (`cc1`, `cc2`) or withheld. Sweep
the list for the design's vocabulary exactly as sweep 2 sweeps the pack, since a key name is a shipped string
for the length of the read. Where a scored read has already run on a contaminated list, its Gate F evidence is
contaminated too: say so, and re-establish the verdict from the clean truth rather than from the read.

## Not a leak

- A figure the prompt states or `stated_inputs` lists.
- A governing clause that pins a convention once. The test: would the sentence exist without the trap?
- A real-world string in a real dataset.
- A noun of the fiction's own field that the author vocabulary also holds (a mosquito trap, a golden eagle), declared
  under `field_terms` in `metadata.json`: `leak.py` reports it REVIEW, answered in one design-note line. A file name
  avoids it where the field has another word.
- A confirming corpus the strategy needs (a sentence pointing at it would be).

## Checklist

- [ ] `leak.py --asof` CLEAN or REVIEW, sweep 11 clean; every REVIEW answered or fixed
- [ ] Reader run once after the realism sweep: nothing quoted for question 1, every question-5 sentence executes to the golden
- [ ] `score_reader.py` run on the reader's own figures before its verdict is read: exit 0, the call missed
- [ ] The pack that ships read by two scored readers: both miss the call, neither exits 1
- [ ] All reader findings fixed in the generator before the judge; `leak.py` re-run after every rebuild
