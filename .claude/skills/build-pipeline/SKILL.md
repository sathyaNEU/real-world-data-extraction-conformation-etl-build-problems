---
name: build-pipeline
description: "The stage machine from a task number to a shipped task: draw, design (precut.py), build, leak and duplicate check together, determinism judge, ship, then the next task at once. Owns pipeline.json, the stage gates, models and effort per role, returned tasks, re-rooting and retirement. Invoked by /build and when resuming a build in flight."
---

# Build pipeline

Every gate is a script's exit status or a thread's verdict; no thread runs before the free gates pass.
There is no solver round: stump power is argued on paper (`precut.py`), checked by the leak reader and
the judge's Gate F, measured by the portal.

## The stages

| # | Stage | Skills | Gate to leave the stage |
|---|---|---|---|
| 0 | intake | `fingerprint` (`recent`, `coverage`) | `taskNN` from root `START_HERE.md`, Status `in build` on main; branch from main under the author's prefix; `pipeline.json` |
| 1 | draw | `guide-to-prompt`, `stumping`, `fingerprint` (`check`, `register`, `names`) | card at PASS or answered WARN, three rules answered, both layers named, people drawn, the stump unique; **default path ending on a wrong answer, stump sentence, data-native sentence** |
| 2 | design | `stumping` (screen, fork table, 3 to 5 rungs), `determinism-check` (closure), `supplemental-stumping`, `guide-to-prompt` | **`precut.py taskNN` exit 0** (runs `voice-check.py`) |
| 3 | build | `dataset-generation`, `determinism-check`, `submission-writeup`, `golden-realism`, `reduce-house-fixes`, `fingerprint` | generator green, every fork asserted; `verify`; two byte-identical builds; input gates; `metadata.json`; `figures_check.py` exit 0; realism sweep; house-fix register; `guard.py surface` |
| 4 | leak + duplicate, together | `leak-check`, `fingerprint` (`heart`), `clone-check` (pre-flight) | `leak.py` not LEAK, REVIEW answered; reader: no decisive-step sentence, no helping file, quoted sentences execute to the golden, no main-call fork; `heart` not BLOCK; no Exact, Same seed, Dataset or Template finding. Fixes in the generator; reader re-runs only if a document or the prompt changed |
| 5 | judge | `determinism-check` | APPROVE ships. FIX_NOW: fixed, stage 3 gates and `leak.py`, re-judged once. SEND_BACK: re-root or retire |
| 6 | ship | `fingerprint`, `reduce-house-fixes` | pre-ship check in the design note; `target.zip` from the final rebuild; card updated; commit `SHIPPED (taskNN): <the call>`; Status `shipped` on main; author handed the bundle and the stump, leak, duplicate and judge lines. **Then the next task** |
| 7 | portal | the author | the result; then ledger row, lessons, memory |

Back to design: a reader finding a decisive-step sentence or a main-call fork; a FIX_NOW that moves the
decisive path; a reject-tier clone finding (redraw the axis once, or retire); a portal return.

## Models and effort

Passed as `model` and `effort` on every `Agent` call, or set in the agent definition.

| Role | Stages | Model | Effort |
|---|---|---|---|
| Designer (also the paper half of a re-root or return) | 1, 2 | Opus | max |
| Builder (also every repair of a committed design) | 3, 4 fixes, FIX_NOW, 6 | Opus | medium |
| Leak reader | 4 | Sonnet | medium |
| `clone-auditor` and its adjudicators | 4 | Opus | medium |
| `determinism-judge` and its thread | 5 | Sonnet | medium |

The designer never cuts data. A builder that finds the design will not hold commits and hands back the
reason to a designer.

## Running the stages

- **Not optional.** Reader, pre-flight and judge run on every new build; only a return skips them.
- **Stage 4 spawns both threads at once** (same pack, neither changes it); the judge waits for both and
  runs in the background while the card and pre-ship check proceed. Register the next draw meanwhile.
- **Every repair is a fresh agent from what is committed** (a leak fix, a FIX_NOW, a re-root, a return),
  briefed in the scratchpad: `pipeline.json`, the report's findings, the design note (`## Tried and
  rejected` first) or the portal result. A finished agent is never resumed (it reloads its transcript).
  A re-root is a designer on paper, then a builder from its commit. No work is left only in a context.
- **`/build` licenses** the reader, the pre-flight and the judge; outside it each is author-triggered.
- **No author checkpoints.** The draw is shown in ten lines and the build carries on; the author can stop
  or redraw at any point, and `/approve` remains for a manual sign-off.

## Returned tasks

Repaired **design, build, commit, ship** with no reader, clone check or judge (each already ran; the
portal measures better), keeping every free gate: generator checks, `verify`, byte-identical rebuilds,
`leak.py`, `guard.py validate` and `heart`, `voice-check.py`, `figures_check.py`, `precut.py`.

- **Call landed:** a designer rewrites the default path and decisive step against the portal's reading,
  `precut.py` re-run; a builder rebuilds from that commit.
- **Determinism finding:** a designer adds the fork to the closure or fork table (convergence first); a
  builder asserts and rebuilds.
- **Call held, asks scored:** a builder revises the ask paths alone, the call's inputs byte-identical.

Read the portal's response against the default path and rungs; it left the ladder after the last rung
it shows:

- **Walked the default path to the golden:** redesign the decisive step, never add a rung above it.
- **Never saw the rung, yet landed:** discriminator dominance failed; fix the magnitudes.
- **Saw the rung and declined it:** file the selection criterion, never the method; a reading one model
  declines another takes, so it is a fork-table row, not a hold.
- **Executed the rung as a work order:** it was announced; the leak sweeps and readability screen find where.
- **Missed only on a misread field or misapplied rule:** a lower rung, not the stump; redesign.

Each attempt gets a `## Tried and rejected` line. The repair re-cuts `target.zip`, appends to
`returned`, sets Status `shipped` on main, and counts as a loop against the architecture.

## `pipeline.json`

The one state file in a task folder: where the build is, never why.

```json
{"task": "task108", "domain": "...", "objective": "forecasting",
 "stage": 4, "stage_name": "leak and duplicate check", "updated": "2026-10-11",
 "stump": "the stump sentence",
 "architecture": 1, "loops": 0,
 "precut": {"exit": 0, "date": ""},
 "leak": {"leak_py": "", "reader": ""},
 "duplicate_check": {"heart": "", "nearest": "", "clone_check": ""},
 "judge": {"verdict": "", "disposition": "", "report": ""},
 "returned": [{"date": "", "portal": "", "repair": "asks | design | fork", "commit": ""}],
 "approved": null, "delivered": null, "portal": null}
```

Older files may carry `solver_rounds` and old stage numbers: history; trust `stage_name`. `/approve`
sets `approved`. The leak, clone and determinism reports are evidence.

## Resuming

Read `stage` and `## Tried and rejected`, then re-check that stage's gate before new work. No
`pipeline.json` with a finished submission is stage 3 complete. A portal result means Returned tasks.

## Re-root and retirement

An architecture is **spent** when the judge returns SEND_BACK, a FIX_NOW fails its second pass, a clone
finding survives one redraw, its third portal return fails, or `precut.py` fails twice on the default path
(re-root before any data is cut). A hardening deepens Layer 2 or Layer 1 and never plants; if only a
plant would hold, the architecture is spent.

**Re-root:** a new draw at stage 1 in the same objective and number, `architecture` incremented, `loops`
reset, the old card's notes saying spent and why, one line in `## Tried and rejected`. **Retire** the
number when its third architecture is spent: a `## Retired` section in the design note, `stage`
`retired`, Status `retired` on main, every card kept. `.claude/authors/` files may set other caps.

## Throughput

Two builds in flight per author, a re-root counted as one; while one waits, the other proceeds. **The
moment a build ships or retires, start the next open number**: Status, branch, `/build`. Draws register
in task-number order, since the guard's bans reach the last three builds.
