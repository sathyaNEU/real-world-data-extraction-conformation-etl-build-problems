---
name: build-pipeline
description: "The stage machine that takes a domain and an objective to a shipped task: draw, design, build (the pack, the write-up and goldens, reduce-house-fixes, the leak check, the surface and heart checks), one solver, the determinism judge, ship. Owns pipeline.json (the one state file a task folder carries), the gate each stage has to pass, the hardening loop that feeds a landed solver's path back into the ladder, and retirement. Invoked by /build and whenever a session resumes a build in flight. Costs nothing itself; the stages that spend tokens (the solver and the judge) are the ones the pipeline exists to sequence."
---

# Build pipeline

> Design, build, solve, judge, ship. The solver is the filter: when it commits to any answer other
> than the golden one, the build is stumping and goes to the determinism judge; when it lands the
> golden answer, the build is hardened. Nothing waits on the author between the draw and the ship.

## The stages

| # | Stage | Skills invoked | Gate (the stage is not left until this holds) |
|---|---|---|---|
| 0 | intake | `fingerprint` (`recent`, `coverage`) | the next free `taskNN`, the domain and the objective fixed, `pipeline.json` written |
| 1 | draw | `guide-to-prompt` (pairing, shape), `stumping` Part 6.1, `fingerprint` (`new`, `check`, `register`), exemplars | card registered at PASS or answered WARN; **the stump sentence written**; the decisive rung named from `stumping/references/traps/_measured.md`; the two nearest exemplars read |
| 2 | design | `stumping` (the ladder, 5 to 6 rungs), `determinism-check` (the 22-axis closure table), `supplemental-stumping` (the ask sheet), `guide-to-prompt` (the prompt), `voice-check.py` | design note carries DRAW, Gate G line, stump sentence, ladder with gaps, closure table, ask sheet with pair arithmetic; prompt passes voice-check |
| 3 | build | `dataset-generation`, `determinism-check` (assertions), `submission-writeup`, `golden-realism`, `reduce-house-fixes`, `leak-check` (`leak.py`), `fingerprint` (`surface`, `heart`) | generator green, verifier green, two builds byte-identical, input gates, metadata clean, goldens through `golden-realism`, the `reduce-house-fixes` register passed, `leak.py` not LEAK with every REVIEW line answered, surface screen clean, heart not BLOCK |
| 4 | solve | `solver-round` (one plain solver) | the solver commits to any answer other than the golden one: go to stage 6, whatever its proxy score; it lands the golden answer: **harden** and return to 3; still landed after three loops: **retire** |
| 5 | second round | `solver-round` (plain and skeptic) | not part of the flow; run only when the author asks (`/solve taskNN 2`) |
| 6 | determinism judge | `determinism-check` (the `determinism-judge` agent) | DETERMINISTIC with APPROVE: go to stage 8; FIX_NOW: fix in the generator or the filed documents, rebuild with the stage 3 gates and re-run the judge; SEND_BACK: **retire** |
| 7 | leak reader | `/leak-check` reader pass | not part of the flow; the mechanical leak check runs in stage 3, and the reader pass runs only when the author asks |
| 8 | ship | `fingerprint` (card fields), `reduce-house-fixes` (H4, H7) | `target.zip` cut from the final rebuild, card updated, `pipeline.json` delivered; the author has the bundle, the stump sentence, the solver's result and the judge line |
| 9 | portal | the author | the result reported; only then the ledger row, lessons, memory |

**Invoking `/build` is the author's licence for stages 4 and 6.** The solver and the judge
rehearsal spend tokens in isolated threads, and each skill's own rule says the author asks for them
in their own words. A `/build` that names the task is that ask. Outside `/build`, each stays
author-triggered as its skill states.

## `pipeline.json`

The one state file a task folder carries, beside the design note. It records where the build is,
not why (the design note holds the why). Created at intake, read on every resume, written at every
stage boundary.

```json
{"task": "task108", "domain": "supply-chain-logistics", "objective": "forecasting",
 "stage": 4, "stage_name": "solver round 1", "updated": "2026-10-06",
 "stump": "one sentence: the wrong committed answer and the step that lands a solver there",
 "harden_loops": 1,
 "solver_rounds": [{"label": "round 1, plain", "date": "2026-10-06", "score": 61.2, "landed": true, "cracked": 3, "items": 5}],
 "judge": {"verdict": "", "disposition": "", "report": ""},
 "approved": null, "delivered": null, "portal": null}
```

`grade.py` appends to `solver_rounds`; `/approve` sets `approved`; nothing else writes it but the
pipeline. It is not a design document and carries no reasoning, so it is outside the no-second-note
rule in `CLAUDE.md`; `solver_rounds/` and `leak_check_report.md` are reports, like the judge's.

## Resuming

A session that opens a task folder with a `pipeline.json` reads `stage`, reads the design note's
`## Tried and rejected`, and continues from that stage's gate: it re-checks the gate before doing
new work, because a stage left green can have been edited since. A folder with no `pipeline.json`
and a finished submission is at stage 3 complete; write the file and go to checkpoint B.

## The hardening loop (the solver lands the call)

The solver's report carries its path. The hardening brief is one sentence: *the solver reached the
call by doing X at step k*. The repair is a rung after which doing X still completes and still
returns the wrong answer, drawn from the measured catalogue first (`_measured.md`: the top four
traps decided 37 of 64 client tasks and share one architecture, a published control set, a
reproduction clause, a hidden unit, an obvious construction that matches most controls). Not a
louder pin, not a defect, not a second decoy. Write the attempt into `## Tried and rejected` with
the solver's own sentence, rebuild (stage 3 gates in full, because a new rung moves figures), and
re-run the round. Three loops on one architecture is the limit; a build whose solver still lands the
call after them is retired, its card kept so the architecture is not drawn again, and the next design
in the queue takes its slot.

## No author checkpoints in the flow

Every gate is a script's exit status or a thread's verdict. The draw is checked by the fingerprint
guard and filed with `guard.py register`; the heart check (`guard.py heart`, the mechanical half of
`/approve`) runs inside stage 3. The author is shown each draw in ten lines when it is filed, reads
the shipped bundle, and can stop or redraw a build at any point; `/approve` stays available when
they want to sign a build off by hand.

## Retirement

A build is retired, not re-rooted, when its solver still lands the golden answer after three
hardening loops, or when the judge returns SEND_BACK. Write a `## Retired` section in the design
note and one line in `## Tried and rejected`, set `pipeline.json` to stage `retired`, and keep the
card (its notes say retired and not submitted) so the architecture is never drawn again. The next
design in the queue takes the slot.

## Throughput

Each build runs as its own background run, so several tasks move at once at different stages. A
wave's draws are drafted in parallel and registered in task-number order, because the guard's bans
reach the last three builds and registration has to be serial; the next wave's draws can run while
the current wave builds. Nothing waits on the author, so the pace is set by the hardening loops: a
build whose first solver misses the golden answer ships in one pass.

## Standing rules the pipeline enforces

- The decisive rung is named from the measured catalogue, or the design note says in one line why
  it is not. A rung with no measured record is a bet; the ledger carries the cost of those bets.
- The asks are the outputs of the decisive construction by segment, each with its own silent
  device (`supplemental-stumping` Part 2), so a wrong basis fails every figure and a cracker still
  loses the device layer.
- Every stage's gate is a script's exit status or a thread's verdict, never a sentence in the chat.
- The design note is the only reasoning record; `pipeline.json` is the only state record; the
  reports (`solver_rounds/`, `leak_check_report.md`, `determinism_check_report*.md`) are evidence.
- Bookkeeping (ledger row, skill lessons, memory) happens after the portal result and never before
  delivery.
