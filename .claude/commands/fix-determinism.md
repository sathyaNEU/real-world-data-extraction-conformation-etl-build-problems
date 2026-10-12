---
description: Repair a build whose portal determinism block failed while its rubric score and stump were fine. Closes the judges' fork in the record so the literal reading is the golden, without moving the main call, the stump, the ladder or any graded figure, proves the scope with freeze.py, re-judges once, and re-ships.
argument-hint: taskNN <the portal's determinism finding, pasted or summarised>
effort: max
---

# /fix-determinism

The build named in `$ARGUMENTS` passed on difficulty and failed the portal's determinism block. The job is
to make the shipped text, read literally, land on the golden it already has. The stump and the rubric are
what passed; they are not touched.

Invoke `determinism-check` and `build-pipeline` first. If the finding is not in `$ARGUMENTS`, read it from
`pipeline.json` (`portal`, `returned`) or ask once and stop.

**1. Freeze before any edit.**
`python3 .claude/skills/build-pipeline/freeze.py snapshot taskNN`. Read the design note's `## Semantic fork
table`, `## Closure table`, `## Literal reader` and `## Tried and rejected`.

**2. Classify the finding** against the gates (`determinism-check` §6) and write it as a new fork-table row
(`SFn`): the term or convention, the golden reading, each reading the judges took, and the call or figure
under each.

- `semantic_fork`, `underspecified_objective`, `competing_defensible_answer`: a reading the record leaves open.
- `prompt_ambiguity`: an ask or the decision worded two ways.
- `solution_incorrect`, `missing_input_data`, `answer_contradicts_files`: a figure that does not recompute
  from the shipped files, or a fact the golden uses that no file carries.

**3. The stump test, before choosing a move.** Ask whether the fork *is* the stump: does the golden's lead
over the easy answer come from the reading rather than from the analysis? If closing the fork in either
direction makes the default path land on the golden, the stump lived in the fork (eight builds died this
way). **Stop**: write the line in `## Tried and rejected`, set `pipeline.json` `status` `design`, and report
that this is a redesign (`/build taskNN from 2`), not a determinism fix. Never keep a fork open to keep a stump.

**4. Close it with the strongest move that holds** (`determinism-check` §3):
- **C1 converge:** align the records so every reading selects the same rows and the same figure; asserted on
  the figure and the counts. Preferred, because it adds no sentence.
- **C2 confirm / C3 corridor / C4 separate**, in that order, as the closure table defines them.
- **A pin at authority, once:** one filed sentence in the governing document (never the prompt, which
  carries the question and no convention) that fixes the WHAT (population, window, unit, inclusion,
  rounding), never the HOW. Run the readability screen (`stumping` 2.1, test 1) on the exact wording: a pin
  that names the decisive quantity, or only makes the solver ask the question, spends the stump; reword it
  or use C1.
- A figure that does not recompute is fixed in the generator so `figures.json`, the golden and the write-up
  agree; the write-up is redrafted from `figures.json` (`submission-writeup`).
- `prompt_ambiguity` on an ask: tighten that ask's wording only, unit and rounding kept, `voice-check.py`
  green. The prompt's call sentence is frozen.

**5. Assert, rebuild, prove the scope.** Add the `SFn` row to `checks.py` and `verify.py`, rebuild twice
(byte-identical), then the free gates: generator checks, `verify`, `figures_check.py`, `precut.py`,
`leak.py`, `voice-check.py`, `guard.py validate` and `heart`. Then:

```
python3 .claude/skills/build-pipeline/freeze.py check taskNN --mode determinism
```

Exit 1 means a frozen item moved: undo that change and find a closure that does not move it. Only when the
golden itself was the non-literal figure (a `solution_incorrect` the author accepts) is a move allowed, with
`--allow <figures.json key>` and the reason in the fork-table row.

**6. Re-judge once.** Spawn the `determinism-judge` agent (medium effort in its definition) on the rebuilt
bundle; this command licenses that one pass. APPROVE: go on. FIX_NOW: repair in this thread, rerun step 5,
and ship without a third judge only if the finding is the same fork closed further. SEND_BACK: stop and
report; it is a redesign.

**7. Re-ship.** Re-cut `target.zip`, append to `pipeline.json` `returned` (`repair: "determinism"`), set
`status` `shipped`, one `## Tried and rejected` line naming the fork and the move, rewrite the ledger row's
status, and commit `RESHIPPED (taskNN): determinism, <the fork closed>` with the zip and `golden/` force-added
(`CLAUDE.md`, Git).

**Report:** the fork in one line, the move used, the `freeze.py` verdict, the judge's verdict, the zip path.
No clone check, no leak reader (unless a document's wording changed near the decisive step), no solver.
