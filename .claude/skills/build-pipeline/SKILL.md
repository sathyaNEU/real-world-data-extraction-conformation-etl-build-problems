---
name: build-pipeline
description: "The stage machine that takes a domain and an objective to a shipped task: draw, design, build (the pack, the write-up and goldens, reduce-house-fixes, the leak check, the surface and heart checks), the duplicate check, the determinism check, ship. Owns pipeline.json (the one state file a task folder carries), the gate each stage has to pass, and retirement. There is no solver round and no hardening loop in the flow. Invoked by /build and whenever a session resumes a build in flight. Costs nothing itself; the stages that spend tokens (the adjudicated duplicate check and the determinism judge) are the ones the pipeline exists to sequence."
---

# Build pipeline

> Design, build, duplicate check, determinism check, ship. One pass, no solver round and no
> re-iteration loop: a build is designed against the ladder on paper, built, checked for duplicates
> and for determinism, and handed to the author. The portal is the only stump oracle.

## The stages

| # | Stage | Skills invoked | Gate (the stage is not left until this holds) |
|---|---|---|---|
| 0 | intake | `fingerprint` (`recent`, `coverage`) | the next free `taskNN`, the domain and the objective fixed, `pipeline.json` written |
| 1 | draw | `guide-to-prompt` (pairing, shape), `stumping` Part 6.1, `fingerprint` (`new`, `check`, `register`), exemplars | card registered at PASS or answered WARN; **the stump sentence written**; the decisive rung named from `stumping/references/traps/_measured.md`; the two nearest exemplars read |
| 2 | design | `stumping` (the ladder, 5 to 6 rungs), `determinism-check` (the 22-axis closure table), `supplemental-stumping` (the ask sheet), `guide-to-prompt` (the prompt), `voice-check.py` | design note carries DRAW, Gate G line, stump sentence, ladder with gaps, closure table, ask sheet with pair arithmetic; prompt passes voice-check |
| 3 | build | `dataset-generation`, `determinism-check` (assertions), `submission-writeup`, `golden-realism`, `reduce-house-fixes`, `leak-check` (`leak.py`, mechanical, free), `fingerprint` (`surface`) | generator green, verifier green, two builds byte-identical, input gates, metadata clean, goldens through `golden-realism`, the `reduce-house-fixes` register passed, `leak.py` not LEAK with every REVIEW line answered, surface screen clean |
| 4 | duplicate check | `fingerprint` (`heart`), `clone-check` (the `clone-auditor` agent, pre-flight mode on this build) | `guard.py heart` not BLOCK, and the adjudicated pre-flight returns no Exact, Same seed, Dataset or Template finding (`clone-check` Part 3); a Shape echo or Idiom finding is reported to the author, not looped on; a reject-tier finding sends the build back to stage 1 once with the colliding axis redrawn, or retires it |
| 5 | determinism check | `determinism-check` (the `determinism-judge` agent) | DETERMINISTIC with APPROVE: go to stage 6; FIX_NOW: fix in the generator or the filed documents, rebuild with the stage 3 gates and re-run the judge once; SEND_BACK: **retire** |
| 6 | ship | `fingerprint` (card fields), `reduce-house-fixes` (H4, H7) | `target.zip` cut from the final rebuild, card updated, `pipeline.json` delivered; the author has the bundle, the stump sentence, the duplicate-check line and the judge line |
| 7 | portal | the author | the result reported; only then the ledger row, lessons, memory |

**Not in the flow.** The solver round (`solver-round`, `/solve`) and the hardening loop that fed a
landed solver's path back into the ladder are paused. Nothing in `/build` runs them, and a build is
never rebuilt because an in-house solver reached the golden answer. The skill and the command stay
in the repo and run only if the author lifts the pause in their own words. The optional reader pass
of `/leak-check` is likewise run only when the author asks.

**Invoking `/build` is the author's licence for stages 4 and 5.** The adjudicated duplicate check and
the judge rehearsal spend tokens in isolated threads, and each skill's own rule says the author asks
for them. A `/build` that names the task is that ask, once per stage. Outside `/build`, each stays
author-triggered as its skill states.

## `pipeline.json`

The one state file a task folder carries, beside the design note. It records where the build is,
not why (the design note holds the why). Created at intake, read on every resume, written at every
stage boundary.

```json
{"task": "task108", "domain": "supply-chain-logistics", "objective": "forecasting",
 "stage": 5, "stage_name": "determinism check", "updated": "2026-10-10",
 "stump": "one sentence: the wrong committed answer and the step that lands a solver there",
 "duplicate_check": {"heart": "", "nearest": "", "clone_check": ""},
 "judge": {"verdict": "", "disposition": "", "report": ""},
 "approved": null, "delivered": null, "portal": null}
```

`/approve` sets `approved`; nothing else writes it but the pipeline. It is not a design document and
carries no reasoning, so it is outside the no-second-note rule in `CLAUDE.md`; `leak_check_report.md`
and `determinism_check_report*.md` are reports, like the clone check's.

## Resuming

A session that opens a task folder with a `pipeline.json` reads `stage`, reads the design note's
`## Tried and rejected`, and continues from that stage's gate: it re-checks the gate before doing
new work, because a stage left green can have been edited since. A folder with no `pipeline.json`
and a finished submission is at stage 3 complete; write the file and go to stage 4.

## No author checkpoints in the flow

Every gate is a script's exit status or a thread's verdict. The draw is checked by the fingerprint
guard and filed with `guard.py register`. The author is shown each draw in ten lines when it is
filed, reads the shipped bundle, and can stop or redraw a build at any point; `/approve` stays
available when they want to sign a build off by hand.

## Retirement

A build is retired, not re-rooted, when the judge returns SEND_BACK, when the duplicate check finds
a clone that one redraw did not clear, or when a FIX_NOW repair fails its second judge pass. Write a
`## Retired` section in the design note and one line in `## Tried and rejected`, set `pipeline.json`
to stage `retired`, and keep the card (its notes say retired and not submitted) so the architecture
is never drawn again. The next design in the queue takes the slot.

## Throughput

Each build runs as its own background run, so several tasks move at once at different stages. A
wave's draws are drafted in parallel and registered in task-number order, because the guard's bans
reach the last three builds and registration has to be serial; the next wave's draws can run while
the current wave builds. Nothing waits on the author, so the pace is set by the build itself.

## Standing rules the pipeline enforces

- The decisive rung is named from the measured catalogue, or the design note says in one line why
  it is not. A rung with no measured record is a bet; the ledger carries the cost of those bets.
- The stump is argued on paper: the design note names the wrong committed answer a competent solver
  files and the step that lands them there, and the determinism check recomputes the golden. No
  in-house solve stands in for either.
- The asks are the outputs of the decisive construction by segment, each with its own silent
  device (`supplemental-stumping` Part 2), so a wrong basis fails every figure and a cracker still
  loses the device layer.
- Every stage's gate is a script's exit status or a thread's verdict, never a sentence in the chat.
- The design note is the only reasoning record; `pipeline.json` is the only state record; the
  reports (`leak_check_report.md`, `clone_check_report.md`, `determinism_check_report*.md`) are
  evidence.
- Bookkeeping (ledger row, skill lessons, memory) happens after the portal result and never before
  delivery.
