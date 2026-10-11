---
name: solver-round
description: "Stage 6 of the build pipeline, the in-house filter before the determinism judge and the portal. One isolated solver works a built task in a sandbox holding only prompt.txt and the bundle, and returns its committed call and every ask figure as structured output; grade.py turns that into a proxy score, a landed-or-missed flag on the main call, the ask share a missed-call response kept and a per-ask hit table, written to <task>/solver_rounds/ and pipeline.json. Two gates: the solver does not commit to the main call (exit 2 otherwise), and a response that missed the call keeps under 35 per cent of the ask weight and cracks no item (exit 3 otherwise). Run by /build at stage 6 and by /solve. A round is a filter, never an oracle."
---

# Solver round

> The portal is the oracle and it costs a day per answer. A solver round costs a quarter of an hour
> and answers the two questions the author most needs before spending that day: does a competent
> reader with no knowledge of the design land the call, and if it misses, do the asks still pay it?
> When either answer is yes, the build goes back, and the round has said so for the price of a coffee.

## What a round is

One isolated agent, handed a sandbox (a fresh copy of `prompt.txt` and `target/` in the scratch
directory and nothing else), asked to do the work the prompt asks for and to return, as structured
output: the committed main call in one sentence, every figure every deliverable owes in the prompt's
unit and rounding, the path it took in ordered steps, its confidence and any notes. No deliverable
files are produced; the figures are what the rubric grades and what `grade.py` compares.

**The solver is told nothing about the task's purpose.** Not that it is a benchmark, not that there is
a trap, not what the client's model tends to miss. The one thing it is told beyond the prompt is the
working rule a real analyst has: compute from the files, reconcile where the files let you, commit to
one answer per ask, and state units.

**The solver** is an `Explore` type agent (it carries no repository instructions), spawned with
`model: opus` and `effort: high` and the prompt in `/solve`. The model is passed explicitly, because an
`Explore` agent otherwise runs on its own default model. High effort, because the portal's strongest
model took a reading two in-house solvers at medium declined (task133 v1, scored 100 on the portal after
two passing rounds): the round is a filter in front of a stronger solver.

## The decision rule

`grade.py` exits 0, 2 or 3 and the exit is the decision.

**Exit 2, LANDED.** The solver committed to the main call. The build goes back to design with a brief
in one sentence: the path step that landed the call, with the next rung built so that exact step
completes and still returns the wrong answer. Read the path against the design note's `## Default
path` first: a landing in minutes along that path means the default construction was the golden
(task134 loop 0, four minutes), and the repair is the decisive step, not a rung above it. The attempt
goes into `## Tried and rejected` with the solver's own sentence. A hardening deepens the analysis and
never plants; three loops per architecture, then re-root; three architectures, then retire
(`build-pipeline`).

**Exit 3, ASKS LEAK.** The solver missed the call and still kept 35 per cent or more of the ask weight,
or cracked any ask item. The second slot of the top two is exactly this response, so its ask share enters
the average directly: task181 shipped after two rounds at 65.2 and 59.0 with the call missed and came
back from the portal at 52. The repair is the ask layer's (`supplemental-stumping` Part 4), in a fresh
agent, with a fresh round after; the ladder is not touched.

**Exit 0, pass.** The solver did not commit to the main call and the asks held. On to the judge. Whether
the missed call is a stump or a fork (a second defensible answer the pack does not rule out) is the
judge's question at stage 7.

**Rounds run on a finished build that has passed the free gates and the leak check**, after the
submission is written and the goldens recompute, because the grader reads blocks 1 and 4 of
`submission.md` and a solver reading a leak measures nothing.

## Grading

```
python3 .claude/skills/solver-round/grade.py task100 <solver_output.json> --label "round 1" [--landed yes|no]
```

Weights 35 / 7 / 58, the planning weights. The main call is matched on its tokens (the names and figures
in block 1's bold sentence, 80 per cent present in the solver's sentence); a wrong set can share most of
the right names, so **the main thread reads both sentences and passes `--landed`** when the token match
is wrong. Each block 4 item is one ask; its tokens are its numbers and capitalised names, and a number
hits only within half a unit of the golden's own rounding (a 0.5 per cent relative band hid task229's
leak; it survives only for figures of six or more significant digits). An item is cracked at 80 per cent
of its tokens. Instruction-following is paid for answering every deliverable. A missed main call keeps 5
of 35, the rubric's surviving components.

The report (`solver_rounds/<label>.md` and the `pipeline.json` row) carries the proxy, landed or
missed, the ask share kept, the items cracked and the gate: LANDED, ASKS LEAK or PASS.

## Isolation, which is the whole value

- The sandbox is fresh for every round (`<scratchpad>/solve-<task>-<k>/`), unzipped from `target.zip`
  where it exists so the solver sees the shipped bytes. Nothing else sits under the scratchpad while the
  solver runs.
- The spawn prompt names the sandbox as the only readable location and forbids everything else on the
  machine. It forbids `Agent`, `WebSearch`, `WebFetch` and every server-side tool, and it says the files
  are the universe: a fact absent from the folder does not exist.
- The solver gets `Bash`, because the work is pandas work and a solver that cannot compute is grading the
  prompt's readability.
- The solver's output is written by the main thread to a results folder outside the scratchpad and graded
  from there. The task folder receives only `solver_rounds/<label>.md` and the row in `pipeline.json`.

## Reading a path

The solver's `path` is the trace the portal never gives you. Read it against the design note's default
path and the ladder's rungs: the last rung whose step appears in the path is the depth it reached, and
the step after that is where it left the ladder. Four shapes recur:

- **It walked the default path to the golden.** The default construction was the answer (`stumping`
  Part 1.5). The decisive step is redesigned, never a rung added above.
- **It stopped at a rung it never saw.** The rung is silent, which is what was wanted; if the solver
  still landed the call, discriminator dominance failed and the fix is in the magnitudes.
- **It saw the rung and declined it.** The path names the quantity and argues it away ("no basis in the
  folder to exclude these"). The selection criterion is not filed (`determinism-check` §1): file the
  criterion, never the method. And note that a stronger solver may take what this one declined (task133
  v1), so a declined reading is a semantic fork table row, not a hold.
- **It executed the rung as a work order.** The rung was announced somewhere; `leak-check` sweeps 4 and 5
  find where, and the readability screen (`stumping` Part 2.1) should have.

**Then classify where the miss happened, against the three rules** (`stumping` Part 1). A miss counts only
when the solver left the ladder at the decisive analytical step; a solver that missed because it misread
a field, code or unit, or misapplied a stated rule, missed on a lower rung that says nothing about the
stump. Record it as such, and if it is the only way the round was missed, the build goes back to design.

**Read the asks too.** Diff the solver's figures against block 4 item by item; a chart's order and title
count as items. An item the solver got while missing the call names the device that is readable.

## What this is not

- Not the portal. The ledger row waits for the portal result.
- Not a judge. Whether a different answer is a stump or a defensible second reading is decided at stage 7.
- Not a second opinion on the design. The solver never sees the design note.

## Checklist

- [ ] The build is finished and through the free gates and the leak check: `precut.py`, the generator's checks, `figures_check.py`, `leak.py` not LEAK, the reader quoted nothing for question 1
- [ ] One `Explore` solver (`model: opus`, `effort: high`) run in a fresh sandbox holding `prompt.txt` and `target/`, its path read against the default path and the ladder
- [ ] Main call read by the main thread, `--landed` passed where the token match misjudged
- [ ] The exit read as the decision: 0 pass, 2 harden (the default path rewritten first), 3 the ask layer rebuilt
- [ ] A landed round's brief written, and the attempt in `## Tried and rejected` with the solver's own path sentence
- [ ] Round, proxy, ask share, gate and decision recorded in `pipeline.json` `solver_rounds`
- [ ] No more than three hardening loops on one architecture, then re-root; three architectures, then retire
