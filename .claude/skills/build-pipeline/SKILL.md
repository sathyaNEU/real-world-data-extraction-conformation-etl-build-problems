---
name: build-pipeline
description: "The stage machine that takes a domain and an objective to a shipped task: draw, design, build (the pack, the write-up and goldens, reduce-house-fixes, the surface and heart checks), the leak check (leak.py and the solver's-eye reader), the duplicate check, the solver round with its hardening loop, the determinism check, ship. Owns pipeline.json (the one state file a task folder carries), the gate each stage has to pass, the worth-it gate the solver round sets, and re-rooting and retirement. Invoked by /build and whenever a session resumes a build in flight. Costs nothing itself; the stages that spend tokens (the leak reader, the adjudicated duplicate check, the solver round and the determinism judge) are the ones the pipeline exists to sequence."
---

# Build pipeline

> Design, build, leak check, duplicate check, solver round, determinism check, ship. The solver round
> is the in-house filter: one isolated solver who never sees the design works the task cold in a
> sandbox, and a build it cracks goes back to design and is hardened, rebuilt and solved again, until
> the solver misses the main call or the architecture is spent. The portal stays the only stump oracle; the loop
> exists so that what reaches it is worth the day it costs.

## The stages

| # | Stage | Skills invoked | Gate (the stage is not left until this holds) |
|---|---|---|---|
| 0 | intake | `fingerprint` (`recent`, `coverage`) | the `taskNN` handed out from the root `START_HERE.md` (its seed read from `taskNN/START_HERE.md`, its Status set to `in build` on `main`), the domain and the objective fixed, the build's branch cut from `main` under the author's prefix where `.claude/authors/` sets one, `pipeline.json` written |
| 1 | draw | `guide-to-prompt` (pairing, shape), `stumping` Part 6.1, `fingerprint` (`new`, `check`, `register`), exemplars | card registered at PASS or answered WARN, with `stump_strategy`, `decisive_rule_filed`, `official_decoy` and `validated_decoy` filled, the three rules answered (`stump_class` analytical, `analyst_test` and `domain_test` written, `stumping` Part 1), and the two layers named (`client_domain` where the domain is a house one, `layer2_family`, `layer2_pattern` from `stumping/references/client/layer2-rigor-patterns.md` or `own:`, `layer1` from `dataset-generation/references/layer1-messiness.md`); **the stump sentence and the data-native sentence written** (`stumping` Part 2); the two nearest exemplars read as idea seeds, never as architectures |
| 2 | design | `stumping` (the ladder, 5 to 6 rungs), `determinism-check` (the 22-axis closure table), `supplemental-stumping` (the ask sheet), `guide-to-prompt` (the prompt), `voice-check.py` | design note carries DRAW, Gate G line, stump sentence, ladder with gaps, closure table, ask sheet with pair arithmetic; prompt passes voice-check; on a hardening loop, the brief from the last solver round is answered in the ladder and the design note says how |
| 3 | build | `dataset-generation`, `determinism-check` (assertions), `submission-writeup`, `golden-realism`, `reduce-house-fixes`, `fingerprint` (`surface`) | generator green, verifier green, two builds byte-identical, input gates, metadata clean, goldens through `golden-realism`, the `reduce-house-fixes` register passed, surface screen clean |
| 4 | leak check | `leak-check` (`leak.py`, then one `/leak-check` reader pass on Sonnet) | `leak.py` not LEAK on the final cut with every REVIEW line answered in the design note; the reader quotes no sentence for its question 1 and names no file that ranks the candidates or states the asked figures (question 2) or exists only to help the analyst (question 3), and any fork it sizes on the main call is closed. Those findings are fixed in the generator before the solver round (stage 3 re-run). The reader's realism tells and the forks it sizes on ask figures are written into the design note and **deferred**: repaired once at stage 6b when the round passes, or folded into the hardening brief when the solver lands. `leak.py` runs after every rebuild; the reader runs again only when a fix changed a document under `target/` or the prompt, never after a data-only repair |
| 5 | duplicate check | `fingerprint` (`heart`), `clone-check` (the `clone-auditor` agent, pre-flight mode on this build) | `guard.py heart` not BLOCK, and the adjudicated pre-flight returns no Exact, Same seed, Dataset or Template finding (`clone-check` Part 3); a Shape echo or Idiom finding is reported to the author, not looped on; a reject-tier finding sends the build back to stage 1 once with the colliding axis redrawn, or retires it. On a hardening loop the heart check re-runs and the adjudicated pre-flight re-runs only when the driver changed |
| 6 | solver round | `solver-round` (`/solve taskNN`: one isolated solver in a sandbox) | **the worth-it gate** (below): the solver does not commit to the main call. Pass: stage 7. Landed: the hardening loop, back to stage 2 with the round's brief |
| 6b | post-round repair | `dataset-generation`, `determinism-check`, `golden-realism`, `reduce-house-fixes` | after a passing round, one repair of the reader's deferred findings (realism tells, forks on ask figures), each fork asserted closed in the checks; `leak.py` re-run; the reader re-runs only if the repair changed a document under `target/` or the prompt; a fresh round only if the repair changed the prompt, a rung or the decisive path. A data-only repair that keeps the method and the ladder goes straight to stage 7 |
| 7 | determinism check | `determinism-check` (the `determinism-judge` agent) | DETERMINISTIC with APPROVE: stage 8; FIX_NOW: fix in the generator or the filed documents, rebuild with the stage 3 and 4 gates, re-run stage 6 when the fix moved a graded figure, a rung or a document the solver read, then re-run the judge once; SEND_BACK: re-root or retire (below) |
| 8 | ship | `fingerprint` (card fields), `reduce-house-fixes` (H4, H7) | the client's pre-ship check (the three rules and the two layers) answered in the design note (`stumping/references/client/two-layer-task-design.md`), `target.zip` cut from the final rebuild, card updated, `pipeline.json` delivered, Status `shipped` in the root `START_HERE.md`; the author has the bundle, the stump sentence, the leak line, the duplicate-check line, the solver line and the judge line |
| 9 | portal | the author | the result reported; only then the ledger row, lessons, memory |

## The worth-it gate and the hardening loop

The client's bar is the top two responses averaging under 50 with at least one genuinely stumped. The
in-house round checks the fact that decides it: whether a competent reader with no knowledge of the
design lands the main call. One solver works the task cold in a sandbox (a fresh scratch copy holding
only `prompt.md` and `target/`) and commits to an answer; `grade.py` scores it at the rubric's weights.

**A round passes when the solver does not commit to the main call** (its committed answer is anything
other than the golden one). The build goes straight on to stage 7. The proxy score is recorded in
`pipeline.json` and does not gate. Whether the solver's different answer is a stump or a fork (a second
defensible answer the pack does not rule out) is the determinism judge's question at stage 7; a fork the
judge finds comes back as FIX_NOW and is closed with a pin.

**A round where the solver lands the main call sends the build back to stage 2 with a brief** in one
sentence: the path step that landed it, and the next rung built so that exact step completes and still
returns the wrong answer. The brief also carries the leak reader's deferred findings (stage 4), so the
hardening rebuild repairs them in the same pass and no repair is spent on a pack that is about to be cut
again.

Each attempt goes into the design note's `## Tried and rejected` with the solver's own path sentence,
then the build runs stages 2, 3, 4 and 5 again and a fresh round (`k + 1`) in a fresh sandbox.

**Hardening stays inside the client's standard.** A hardening deepens the analytical pitfall (Layer 2)
or the honest mess (Layer 1); it never plants a decoy, a doctored figure or a rule withheld to be
recovered, and never builds a rung whose only purpose is to trip this solver's particular sentence.
If the only fix that would stop the solver is a plant, the architecture is spent.

**Caps.** Three hardening loops per architecture. A build that still fails after its third loop is
**re-rooted**: a new draw at stage 1 in the same objective and the same task number, a new Layer 2
pitfall and a new card, the dead architecture written into `## Tried and rejected` and noted on the
old card. A task number gets three architectures; when the third is spent the number is retired.

## Running the stages

**Not optional.** The leak reader (stage 4), the solver round (stage 6) and the judge (stage 7) run
on every build, and a build reaches stage 7 only through a passing round.

**Solver first, polish after.** The round runs as soon as the pack is free of leaks: the reader's
question 1 to 3 findings and any fork on the main call are fixed before the solver sees the pack, and
everything else the reader raises (realism tells, forks on ask figures) waits for a round the solver
misses (stage 6b). A build the solver cracks is rebuilt by the hardening loop anyway, so repairing it
first spends a repair and a second read on a pack that is about to change. The leak reader runs on
Sonnet (`model: sonnet` on its `Agent` call): it reads the pack and answers four questions, it does not
solve, so it needs no stronger model. One read per build, and a second only when a fix changed a
document under `target/` or the prompt. The solver and the leak
reader are always isolated threads on fresh scratch copies; no solve or read happens in the main
thread, which has seen the design.

**Invoking `/build` is the author's licence for every token-spending stage it sequences**: the leak
reader (stage 4), the adjudicated duplicate check (stage 5), every solver round the loop needs
(stage 6, one isolated `Agent` spawn as `/solve` sets out) and the judge (stage 7). Outside `/build`, each stays author-triggered
as its own skill states.

**The judge runs after the round passes**, because judging a build the next round may harden is
waste. It runs in the background while the ship stage's non-figure work (the card, the pre-ship
check, the realism pass on anything that did not move) proceeds.

## `pipeline.json`

The one state file a task folder carries, beside the design note. It records where the build is,
not why (the design note holds the why). Created at intake, read on every resume, written at every
stage boundary.

```json
{"task": "task108", "domain": "supply-chain-logistics", "objective": "forecasting",
 "stage": 6, "stage_name": "solver round", "updated": "2026-10-10",
 "stump": "one sentence: the wrong committed answer and the step that lands a solver there",
 "architecture": 1, "loops": 0,
 "leak": {"leak_py": "", "reader": ""},
 "duplicate_check": {"heart": "", "nearest": "", "clone_check": ""},
 "solver_rounds": [{"round": 1, "architecture": 1, "solver": {"landed": null, "proxy": null},
                    "decision": "pass | harden | reroot", "brief": ""}],
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
and a finished submission is at stage 3 complete; write the file and go to stage 4. A build resumed
mid-loop reads `architecture`, `loops` and the last round's `brief` before anything else.

## No author checkpoints in the flow

Every gate is a script's exit status or a thread's verdict. The draw is checked by the fingerprint
guard and filed with `guard.py register`. The author is shown each draw in ten lines when it is
filed, reads the shipped bundle, and can stop or redraw a build at any point; `/approve` stays
available when they want to sign a build off by hand.

## Retirement

An architecture is spent when its third hardening loop still fails the worth-it gate, when the judge
returns SEND_BACK, when the duplicate check finds a clone that one redraw did not clear, or when a
FIX_NOW repair fails its second judge pass. A spent architecture is **re-rooted**: a new draw at
stage 1 in the same objective and task number, `architecture` incremented and `loops` reset, the old
card's notes saying spent and why, and one line in `## Tried and rejected`. The number is **retired**
when its third architecture is spent: write a `## Retired` section in the design note, set
`pipeline.json` to stage `retired` and Status `retired` in the root `START_HERE.md`, and keep every
card so no spent architecture is drawn again.

## Throughput

**Two builds in flight per author.** An author's builds between intake and ship number at most two at
a time, and an architecture re-rooted after a portal result counts as one of the two; the next number
is drawn when one ships or retires. Each of the two runs as its own background run at its own stage.
Draws are registered in task-number order, because the guard's bans reach the last three builds and
registration has to be serial. Nothing waits on the author, so the pace is set by the build itself.

## Standing rules the pipeline enforces

- Every build is bespoke. The stump is chosen from the dataset's own analytic structure and the
  design note says so in the data-native sentence; the measured catalogue says which habits fail and
  never which architecture to copy. The guard's strategy bans and its decoy bans (an official decoy, the
  withheld rule with an official decoy, and the certified record that blesses the wrong method, each
  blocked on a new draw) are gates, not advice. Every build names its two layers in the design note:
  Layer 1, the realistic mess and the system that produces it; Layer 2, the analytical shortcut the
  stump rests on.
- The stump is argued on paper first: the design note names the wrong committed answer a competent
  solver files and the step that lands them there before the pack is cut. The solver round then
  tests that sentence, and the judge recomputes the golden. Neither replaces the other, and neither
  replaces the portal.
- The asks are the outputs of the decisive construction by segment, each with its own silent
  device (`supplemental-stumping` Part 2), so a wrong basis fails every figure and a cracker still
  loses the device layer.
- Every stage's gate is a script's exit status or a thread's verdict, never a sentence in the chat.
- The design note is the only reasoning record; `pipeline.json` is the only state record; the
  reports (`leak_check_report.md`, `clone_check_report.md`, `solver_rounds/`,
  `determinism_check_report*.md`) are evidence.
- Bookkeeping (ledger row, skill lessons, memory) happens after the portal result and never before
  delivery.
