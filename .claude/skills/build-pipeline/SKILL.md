---
name: build-pipeline
description: "The stage machine that takes a domain and an objective to a delivered task: draw, design, build, solver round 1, solver round 2, judge rehearsal, leak and heart checks, deliver. Owns pipeline.json (the one state file a task folder carries), the gate each stage has to pass, the two author checkpoints, the hardening loop that feeds a solver's path back into the ladder, and the day shape that gets four tasks through. Invoked by /build and whenever a session resumes a build in flight. Costs nothing itself; the stages that spend tokens (solvers, the judge, the leak reader) are the ones the pipeline exists to sequence."
---

# Build pipeline

> One task a day was the cost of two things: every stage waiting on the author, and the portal
> being the first solver to touch the build. The pipeline removes the waiting (the author decides
> twice, at the draw and at delivery) and puts two solvers in front of the portal. The build itself
> is the same skills in the same order; what changes is that nothing idles between them.

## The stages

| # | Stage | Skills invoked | Gate (the stage is not left until this holds) |
|---|---|---|---|
| 0 | intake | `fingerprint` (`recent`, `coverage`) | the next free `taskNN`, the domain and the objective fixed, `pipeline.json` written |
| 1 | draw | `guide-to-prompt` (pairing, shape), `stumping` Part 6.1, `fingerprint` (`new`, `check`, `register`), exemplars | card registered at PASS or answered WARN; **the stump sentence written**; the decisive rung named from `stumping/references/traps/_measured.md`; the two nearest exemplars read |
| A | **checkpoint: the author reads the draw** | | the author says go, or redraws an axis |
| 2 | design | `stumping` (the ladder, 5 to 6 rungs), `determinism-check` (the 22-axis closure table), `supplemental-stumping` (the ask sheet), `guide-to-prompt` (the prompt), `voice-check.py` | design note carries DRAW, Gate G line, stump sentence, ladder with gaps, closure table, ask sheet with pair arithmetic; prompt passes voice-check |
| 3 | build | `dataset-generation`, `determinism-check` (assertions), `submission-writeup`, `golden-realism`, `reduce-house-fixes`, `leak-check` (`leak.py`), `fingerprint` (`surface`) | generator green, verifier green, two builds byte-identical, input gates, metadata clean, `leak.py` not LEAK, surface screen clean |
| B | **checkpoint: `/approve`** | `fingerprint` (`heart`) | heart verdict not BLOCK; the author has read the stump sentence against the pack |
| 4 | solver round 1 | `solver-round` (one plain solver) | main call missed and proxy under 40; else **harden** (max three loops) and return to 3 |
| 5 | solver round 2 | `solver-round` (plain and skeptic) | average under 40, one under 25; both landing is a re-root to stage 1; with the three loops spent, both missing the call and the pair under 40 passes on the author's standing waiver (`solver-round`) |
| 6 | judge rehearsal | `determinism-check` (the `determinism-judge` agent) | DETERMINISTIC; FIX_NOW findings fixed in the generator and the stage re-run |
| 7 | leak read and heart | `/leak-check` reader pass, `guard.py heart` | no sentence quoted for question 1; heart not BLOCK |
| 8 | deliver | card fields updated, zips cut, summary | the author has the bundle, the stump sentence, both rounds' scores and the judge line |
| 9 | portal | the author | the result reported; only then the ledger row, lessons, memory |

**Invoking `/build` is the author's licence for stages 4 to 7.** The solver rounds, the judge
rehearsal and the leak reader all spend tokens in isolated threads, and each skill's own rule says
the author asks for them in their own words. A `/build` that names the task and the stage is that
ask. Outside `/build`, each stays author-triggered as its skill states.

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

## The hardening loop (stage 4 or 5 fails)

The solver's report carries its path. The hardening brief is one sentence: *the solver reached the
call by doing X at step k*. The repair is a rung after which doing X still completes and still
returns the wrong answer, drawn from the measured catalogue first (`_measured.md`: the top four
traps decided 37 of 64 client tasks and share one architecture, a published control set, a
reproduction clause, a hidden unit, an obvious construction that matches most controls). Not a
louder pin, not a defect, not a second decoy. Write the attempt into `## Tried and rejected` with
the solver's own sentence, rebuild (stage 3 gates in full, because a new rung moves figures), and
re-run the round that failed. Three loops on one architecture is the limit; the fourth is a re-root
at stage 1 with the old architecture moved into the card's `lineage`.

## The two checkpoints, and why only two

The draw is the cheapest thing in the build to change and the only thing the author's taste decides,
so it is shown before anything is built: the pairing, the niche, the stump sentence, the shape, the
deliverables, the nearest exemplar, the guard verdict, in ten lines. The author answers in one word
or redraws one axis. `/approve` is the second: the build exists, the heart check has run, and the
author reads the stump sentence against the pack before tokens are spent on solvers. Everything
else is gated by a script or a thread, and a human gate between scripted stages is where a day
goes.

## The day shape for four tasks

Stages 4 to 7 run in the background (Workflow and Agent runs return when they finish), so one
session carries two tasks at different stages, and the author's attention is needed only at the two
checkpoints.

```
morning     T1 draw -> checkpoint A -> T1 design and build       (author: 10 min at A)
            T2 draw -> checkpoint A                               (author: 10 min at A)
midday      T1 /approve -> rounds 1 and 2 in the background       (author: 15 min reading T1's pack)
            T2 design and build
afternoon   T1 judge, leak read, deliver -> portal                 (author: submits T1)
            T2 /approve -> rounds in the background; T3 draw -> checkpoint A
evening     T2 judge, leak read, deliver -> portal; T3 build; T4 draw
```

What makes the shape hold is that no stage waits on the author except A and B, and that a round
that fails costs a rebuild rather than a day. What breaks it is a re-root, which is why the draw
stage reads the measured catalogue and the exemplars first: a decisive rung from the top of that
list has a measured record of stumping, and a draw with a record is a draw that survives rounds.

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
