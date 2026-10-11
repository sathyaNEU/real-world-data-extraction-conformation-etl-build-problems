---
name: build-pipeline
description: "The stage machine that takes a domain and an objective to a shipped task: draw, design (gated by precut.py), build (gated by the generator's checks, figures_check.py and the realism sweep), the leak check and the duplicate check in parallel, the solver round with its hardening loop and the ask gate, the determinism judge in the background, ship. Owns pipeline.json, the gate each stage has to pass, the worth-it gate, the returned-task fast path (a shipped task brought back with portal feedback is repaired design, build, commit, ship, with the free mechanical gates only), and re-rooting and retirement. Invoked by /build and whenever a session resumes a build in flight."
---

# Build pipeline

> Design, build, leak check and duplicate check together, solver round, determinism check, ship. The
> expensive stages (the leak reader, the clone pre-flight, the solver round, the judge) each run once per
> build on a pack that the free mechanical gates have already passed, because the record says what they
> find: in 79 in-house rounds the landed calls were readable rungs and default paths that a paper screen
> catches, the judge's findings were forks and typed figures that a closure table and `figures.json`
> catch, and the reader's realism tells were a sweep's business. The paper gate (`precut.py`) and the
> build gates are where a build now passes or fails; the threads confirm.

## The stages

| # | Stage | Skills invoked | Gate (the stage is not left until this holds) |
|---|---|---|---|
| 0 | intake | `fingerprint` (`recent`, `coverage`) | the `taskNN` handed out from the root `START_HERE.md` (its seed read from `taskNN/START_HERE.md`, its Status set to `in build` on `main`), the domain and the objective fixed, the build's branch cut from `main` under the author's prefix where `.claude/authors/` sets one, `pipeline.json` written |
| 1 | draw | `guide-to-prompt` (pairing, shape), `stumping` Part 1 and Part 6, `fingerprint` (`new`, `check`, `register`), exemplars | card registered at PASS or answered WARN, with `stump_strategy`, `decisive_rule_filed`, `official_decoy` and `validated_decoy` filled, the three rules answered (`stump_class` analytical, `analyst_test` and `domain_test`), the two layers named (`layer2_family`, `layer2_pattern` from `stumping/references/client/layer2-rigor-patterns.md` or `own:`, `layer1` from `dataset-generation/references/layer1-messiness.md`), the people drawn with `guard.py names`; **the default path written and ending on a wrong answer, the stump sentence naming it, the data-native sentence written** (`stumping` Part 1.5 to 1.7); the nearest exemplars read as idea seeds |
| 2 | design | `stumping` (the readability screen, the semantic fork table, the ladder of 3 to 5 rungs, the oracle list), `determinism-check` (the literal-reader line, the 22-axis closure table), `supplemental-stumping` (the ask sheet with the cracker sheet and the pair ceiling), `guide-to-prompt` (`prompt.txt`) | **`python3 .claude/skills/stumping/precut.py taskNN` exits 0**: every design-note section present, the default path not the golden, the decisive rung silent, every semantic fork ruled out, 22 axes closed, the pair ceiling at or under 40, every cracker-sheet row a miss, and `voice-check.py` passing on `prompt.txt`. On a hardening loop the brief from the last round is answered in the ladder, the default path is rewritten, and the gate re-runs |
| 3 | build | `dataset-generation` (the pack, the realism sweep), `determinism-check` (assertions, `figures_check.py`), `submission-writeup`, `golden-realism`, `reduce-house-fixes`, `fingerprint` (`surface`) | generator green with every semantic fork row asserted, verifier green, two builds byte-identical, input gates, `metadata.json` clean, **`figures_check.py` exit 0**, the realism sweep clean (no identical counts across periods, no round headline totals, no constant streams, no reused remarks, names drawn, containers scrubbed), goldens through `golden-realism`, the `reduce-house-fixes` register passed, `guard.py surface` clean |
| 4 | leak check | `leak-check` (`leak.py`, then one `/leak-check` reader pass on Sonnet at medium effort) | `leak.py` not LEAK with every REVIEW line answered in the design note; the reader quotes no sentence for question 1, names no file for questions 2 and 3, every filed sentence it quotes for question 5 executes literally to the golden, and any fork it sizes on the main call is closed. Those findings are fixed in the generator before the round. Its realism tells and forks on ask figures are written into the design note and deferred to 6b. The reader runs once per build, after the realism sweep, and again only when a fix changed a document under `target/` or the prompt; a data-only repair is checked by `leak.py` alone. **Runs in parallel with stage 5** |
| 5 | duplicate check | `fingerprint` (`heart`), `clone-check` (the `clone-auditor` agent, pre-flight mode) | `guard.py heart` not BLOCK, and the pre-flight returns no Exact, Same seed, Dataset or Template finding (`clone-check` Part 3); a Shape echo or Idiom finding is reported, not looped on; a reject-tier finding sends the build to stage 1 once with the colliding axis redrawn, or retires it. On a hardening loop the heart check re-runs and the pre-flight re-runs only when the driver changed. **Runs in parallel with stage 4**; the round waits for both |
| 6 | solver round | `solver-round` (`/solve taskNN`: one isolated solver in a sandbox holding `prompt.txt` and `target/`) | **the worth-it gate and the ask gate** (below): `grade.py` exit 0. Exit 2 (LANDED): the hardening loop, back to stage 2 with the round's brief. Exit 3 (ASKS LEAK): the ask layer is rebuilt (`supplemental-stumping` Part 4) in a fresh agent and a fresh round runs; the ladder is not touched |
| 6b | post-round repair | `dataset-generation`, `determinism-check`, `golden-realism`, `reduce-house-fixes` | after a passing round, one repair of the reader's deferred findings, each fork asserted closed; `leak.py` re-run; the reader re-runs only if a document under `target/` or the prompt changed; a fresh round only if the prompt, a rung or the decisive path changed. A data-only repair goes straight to stage 7 |
| 7 | determinism check | `determinism-check` (the `determinism-judge` agent, spawned from the thread that holds the `Agent` tool, in the background) | DETERMINISTIC with APPROVE: stage 8. FIX_NOW: fixed in the generator or the filed documents, rebuilt through the stage 3 gates, a fresh round only when the fix moved a graded figure, a rung or a document the solver read (a wording fix gets none), then one re-judge. SEND_BACK: re-root or retire |
| 8 | ship | `fingerprint` (card fields), `reduce-house-fixes` (H4, H7) | the client's pre-ship check answered in the design note, `target.zip` cut from the final rebuild, the card updated, `pipeline.json` delivered, Status `shipped` on main; the author has the bundle, the stump sentence, the leak line, the duplicate-check line, the solver line and the judge line |
| 9 | portal | the author | the result reported; only then the ledger row, lessons, memory. A task the author brings back takes the **returned-task path** below and never re-enters stages 4 to 7 |

## Models and effort

Each role runs on one model at one effort, passed as `model` and `effort` on every `Agent` call (or set
in the agent's definition). The thinking goes into the design; everything after it executes a design that
is already written.

| Role | Stages | Model | Effort |
|---|---|---|---|
| **Designer**: the draw, the default path, the stump sentence, the readability screen, the semantic fork table, the ladder, the closure table, the ask sheet, `prompt.txt`; the paper half of every hardening loop and re-root; the design half of a returned task whose call fell | 1, 2, the paper half of each loop | Opus | max |
| **Builder**: the generator, the pack, the goldens, the write-up, the verifiers, the house fixes, the free gates; the rebuild that executes a committed design; the 6b repair; a FIX_NOW that edits data or prose; the ask-layer rebuild after ASKS LEAK; the returned-task rebuild; ship | 3, the mechanical half of 4 and 5, 6b, the FIX_NOW of 7, 8, 9 | Opus | medium |
| **Leak reader** | 4 | Sonnet | medium |
| **Duplicate-check auditor** (`clone-auditor`) and its adjudicators | 5 | Opus | medium |
| **Solver** (`Explore`) | 6 | Opus | **high** |
| **Determinism judge** (`determinism-judge` and its one thread) | 7 | Sonnet | medium |

The solver runs at high effort because the in-house round at medium passed task133 v1 twice while the
portal's strongest model took the reading both in-house solvers declined and scored 100; the round is a
filter in front of a stronger solver, and a filter weaker than the thing it filters for lets the build
through. One solver per round stays: the second lens of the earlier two-solver rounds caught one landing in
nine that the first missed, which the paper gate now catches at stage 2.

The designer reads before it draws and never cuts data. The builder executes the committed design; a
builder that finds the design will not hold commits what it has and hands back the reason, and the next
paper pass goes to a designer.

## The worth-it gate, the ask gate and the hardening loop

One solver works the task cold in a sandbox (a fresh copy holding only `prompt.txt` and `target/`) and
commits to an answer; `grade.py` scores it at the rubric's weights and exits 0, 2 or 3.

**The round passes (exit 0) when the solver does not commit to the main call and the asks hold**: a
response that missed the call keeps under 35 per cent of the ask weight and cracks no ask item. Whether a
missed call is a stump or a fork is the judge's question at stage 7.

**LANDED (exit 2)** sends the build to stage 2 with a brief in one sentence: the path step that landed the
call, and the next rung built so that exact step completes and still returns the wrong answer. The default
path is rewritten first (`stumping` Part 1.5), because a landing in minutes with the default construction
means the default path was the golden. The brief carries the reader's deferred findings so the rebuild
repairs them in the same pass.

**ASKS LEAK (exit 3)** sends the build to the ask layer, not the ladder: the cracker sheet is rewritten
and the failing devices are moved off every filed sentence, marker and referee (`supplemental-stumping`
Part 4), then a fresh round. The proxy score is recorded and never gates on its own; task181 shipped at
65.2 and 59.0 with the call missed and came back from the portal at 52.

Each attempt goes into `## Tried and rejected` with the solver's own path sentence. A hardening deepens
Layer 2 or Layer 1 and never plants; if the only fix that stops the solver is a plant, the architecture is
spent. **Three hardening loops per architecture, then re-root; three architectures per number, then
retire** (Retirement below).

## Returned tasks

A shipped task the author brings back with portal feedback (the call landed, the asks scored, a
determinism finding) is repaired on a fast path: **design, build, commit, ship**. It runs no leak reader,
no solver round, no judge and no clone check, because each of those already ran on the architecture and
the portal result is a stronger measurement than any of them. It keeps every free mechanical gate: the
generator's checks with every semantic fork asserted, `verify`, two byte-identical rebuilds, `leak.py`,
`guard.py validate` and `heart`, `voice-check.py`, `figures_check.py` and `precut.py`.

- **The call held and the asks scored**: the builder's revision of the ask paths alone, the main call's
  inputs byte-identical (`supplemental-stumping` Part 6).
- **The call landed**: a designer rewrites the default path and the decisive step against the portal's
  reading and re-runs `precut.py`; a builder rebuilds from that commit. A reading the portal took that the
  design called unlikely is the semantic fork table's row, not a solver's eccentricity.
- **A determinism finding**: the fork is added to the closure or semantic fork table, closed by convergence
  first, asserted, rebuilt.

The repair runs in a fresh agent from a one-screen brief (the portal result verbatim, the design note, the
generator files on the paths that change), commits, re-cuts `target.zip`, records the return in
`pipeline.json` and sets Status `shipped` on main in its own commit. The author re-tests. A return counts
as a loop against the architecture's cap, so a third failed return on one architecture re-roots or
retires it. New builds keep the full workflow.

## Running the stages

**Not optional.** The leak reader, the solver round and the judge run on every new build, and a build
reaches stage 7 only through a passing round. The returned-task path is the one route that skips them.

**Free gates first, threads after.** Nothing with a token cost runs on a pack that `precut.py`, the
generator's checks, `figures_check.py`, the realism sweep, `leak.py` and `guard.py` have not passed.
Realism is checked by the sweep at stage 3, so the reader confirms rather than finds: task132 spent about
six hours on three realism rebuilds before its second round, and task180 and task132 together spent most
of a day on reader passes against a one-per-build rule.

**Stages 4 and 5 run together.** The reader and the clone pre-flight read the same finished pack and
neither changes it, so both are spawned at once and the round starts when both have returned. While they
run, the next build's draw is registered (Throughput).

**The judge runs in the background** after the round passes, spawned from whichever thread holds the
`Agent` tool (`determinism-check`, Running the judge rehearsal); the ship stage's non-figure work (the
card, the pre-ship check) proceeds meanwhile. A FIX_NOW that moves only words gets no fresh round; one
that moves a figure, a rung or a document the solver read gets one.

**Every repair starts in a fresh agent, from what is committed.** A hardening rebuild, an ask-layer
rebuild, the 6b repair, a FIX_NOW and a returned-task repair are never handed back to the agent that built
the pack, and a finished agent is never resumed, because a resumed agent reloads its whole transcript. The
main session spawns a new agent with a short brief in the scratchpad naming the committed inputs: the
round's log in `solver_rounds/`, the round's row and brief in `pipeline.json`, the leak report's deferred
findings, the design note (`## Tried and rejected` first), or for a returned task the portal result. A
hardening loop and a re-root are two fresh agents in turn (a designer on paper, then a builder from its
commit); a 6b repair, a FIX_NOW that edits data or prose, an ask-layer rebuild and a held-call return need
only the builder. No stage ends with work left only in an agent's context.

**Invoking `/build` is the author's licence for every token-spending stage it sequences**: the reader,
the clone pre-flight, every solver round the loop needs and the judge. Outside `/build` each stays
author-triggered as its own skill states.

## `pipeline.json`

The one state file a task folder carries, beside the design note. It records where the build is, not why.

```json
{"task": "task108", "domain": "supply-chain-logistics", "objective": "forecasting",
 "stage": 6, "stage_name": "solver round", "updated": "2026-10-11",
 "stump": "one sentence: the wrong committed answer the default path files and the step that lands it there",
 "architecture": 1, "loops": 0,
 "precut": {"exit": 0, "date": "2026-10-11"},
 "leak": {"leak_py": "", "reader": ""},
 "duplicate_check": {"heart": "", "nearest": "", "clone_check": ""},
 "solver_rounds": [{"round": 1, "architecture": 1, "solver": {"landed": null, "proxy": null, "ask_share": null, "gate": ""},
                    "decision": "pass | harden | asks | reroot", "brief": ""}],
 "judge": {"verdict": "", "disposition": "", "report": ""},
 "returned": [{"date": "", "portal": "", "repair": "asks | design | fork", "commit": ""}],
 "approved": null, "delivered": null, "portal": null}
```

`/approve` sets `approved`; nothing else writes it but the pipeline. It carries no reasoning, so it is
outside the no-second-note rule; `leak_check_report.md`, `clone_check_report.md`, `solver_rounds/` and
`determinism_check_report*.md` are evidence.

## Resuming

A session that opens a task folder with a `pipeline.json` reads `stage`, reads `## Tried and rejected`,
and re-checks that stage's gate before new work, because a stage left green can have been edited since.
A folder with no `pipeline.json` and a finished submission is at stage 3 complete. A build resumed
mid-loop reads `architecture`, `loops` and the last round's `brief` first. A shipped task opened with a
portal result takes the returned-task path.

## No author checkpoints in the flow

Every gate is a script's exit status or a thread's verdict. The author is shown each draw in ten lines
when it is filed, reads the shipped bundle, and can stop or redraw a build at any point; `/approve`
stays available when they want to sign a build off by hand.

## Retirement

An architecture is spent when its third hardening loop still lands, when the judge returns SEND_BACK,
when the duplicate check finds a clone one redraw did not clear, when a FIX_NOW fails its second judge
pass, or when its third return from the portal fails. A spent architecture is **re-rooted**: a new draw at
stage 1 in the same objective and number, `architecture` incremented and `loops` reset, the old card's
notes saying spent and why, one line in `## Tried and rejected`. The number is **retired** when its third
architecture is spent: a `## Retired` section in the design note, `pipeline.json` at stage `retired`,
Status `retired` on main, and every card kept so no spent architecture is drawn again. A draw that fails
`precut.py` twice on the default path (the default construction keeps landing on the golden) is re-rooted
before any data is cut, which is the cheapest retirement there is.

## Throughput

**Two builds in flight per author**, a re-rooted architecture counted as one of the two. While one build
waits on a reader, a pre-flight, a round, a judge or the portal, the other proceeds, and the next number's
draw is registered and its paper work done the moment a slot frees. Draws are registered in task-number
order because the guard's bans reach the last three builds. Nothing waits on the author.

## Standing rules the pipeline enforces

- Every build is bespoke: the stump comes from the dataset's own analytic structure, the design note says
  so in the data-native sentence, and the guard's bans are gates, not advice. Both layers are named.
- The stump is argued on paper first and `precut.py` is the proof: the default path ends on a wrong
  answer, the decisive rung is silent, no semantic fork is open. The round tests the sentence; the judge
  recomputes the golden; the portal decides.
- The asks are designed against the careful solver's path, decoupled from the call, each with its own
  silent device, and `grade.py`'s ask gate holds the round to it.
- Every stage's gate is a script's exit status or a thread's verdict, never a sentence in the chat.
- A build is set to `shipped` on main the moment its bundle is handed to the author, at stage 8 and after
  every returned-task repair, in a commit of its own (`Status: taskNN shipped (<owner>)`).
- The design note is the only reasoning record; `pipeline.json` is the only state record; the reports
  are evidence. Bookkeeping (ledger row, skill lessons, memory) happens after the portal result.
