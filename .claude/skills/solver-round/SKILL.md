---
name: solver-round
description: "Stage 6 of the build pipeline, the in-house filter before the determinism judge and the portal. One isolated solver works a built task in a sandbox holding only the prompt and the bundle, and returns its committed call and every ask figure as structured output; grade.py turns that into a proxy score, a landed-or-missed flag on the main call and a per-ask hit table, written to <task>/solver_rounds/ and pipeline.json. The worth-it gate is one fact: the solver does not commit to the main call. A pass sends the build on to the determinism judge; a landed call sends it back to design with a hardening brief, three loops per architecture. Run by /build at stage 6 and by /solve. A round is a filter, never an oracle: a build the solver cracks does not go to the portal, and a build it does not crack still has to."
---

# Solver round

> The portal is the oracle and it costs a day per answer. A solver round costs a quarter of an hour
> and answers the one question the author most needs before spending that day: does a competent
> reader with no knowledge of the design land the call? When the answer is yes, the build goes back to
> design and the round has said so for the price of a coffee. When the answer is no, the build moves
> on toward shipping, and the portal still has the last word.

## What a round is

One isolated agent, handed a sandbox (a fresh copy of `prompt.md` and `target/` in the scratch
directory and nothing else), asked to do the work the prompt asks for and to return, as structured
output: the committed main call in one sentence, every figure every deliverable owes in the prompt's
unit and rounding, the path it took in ordered steps, its confidence and any notes. No deliverable
files are produced; the figures are what the rubric grades and the figures are what `grade.py`
compares.

**The solver is told nothing about the task's purpose.** Not that it is a benchmark, not that there
is a trap, not what the client's model tends to miss. A solver that hunts for a trap is not the
portal's model. The one thing it is told beyond the prompt is the working rule a real analyst has:
compute from the files, reconcile where the files let you, commit to one answer per ask, and state
units.

**The solver** is an `Explore` type agent (it carries no repository instructions), spawned with
`model: opus` and `effort: medium` and the prompt in `/solve`. The model is passed
explicitly, because an `Explore` agent otherwise runs on its own default model. It reads as the
portal's model.

## The decision rule

**The worth-it gate** (`build-pipeline`, stage 6). **A round passes when the solver does not commit
to the main call**: its committed answer is anything other than the golden one. A pass sends the
build on to stage 7. The proxy score is recorded and does not gate.

Whether a missed call is a stump or a fork (a second defensible answer the pack does not rule out) is
the determinism judge's question at stage 7, which reviews the bundle for exactly that. A fork the
judge finds comes back as FIX_NOW and is closed with a pin.

**A landed call is hardened, not sent on.** The brief is one sentence: the path step that landed the
main call, with the next rung built so that exact step completes and still returns the wrong answer.
The attempt goes into the design note's `## Tried and rejected` with the solver's own sentence, and
the build loops through design, build, leak check and duplicate check to a fresh round in a fresh
sandbox.

**A hardening deepens the analysis, never plants.** It works in Layer 2 (the analytical pitfall) or
Layer 1 (honest mess), within the client's two-layer standard. A rung whose only purpose is to trip
this solver's particular sentence is tuning to the solver, and a fix that needs a decoy, a doctored
figure or a withheld rule means the architecture is spent.

**Three hardening loops per architecture, then re-root; three architectures per task number, then
retire** (`build-pipeline`, Retirement). A ladder patched three times against the same solver is
being tuned to it, and the portal is a different solver.

**Rounds are run on a finished build that has passed the leak check**, after the submission is
written and the goldens recompute, because the grader reads block 1 and block 4 of `submission.md`
and a solver reading a leak measures nothing.

## Grading

```
python3 .claude/skills/solver-round/grade.py task100 <solver_output.json> --label "round 1" [--landed yes|no]
```

Weights 35 / 7 / 58, the planning weights. The main call is matched on its tokens (the names and
figures in block 1's bold sentence, 80 per cent present in the solver's sentence); a wrong set can
share most of the right names, so **the main thread reads both sentences and passes `--landed`
when the token match is wrong**. Each block 4 item is one ask; its tokens are the numbers (to the
golden's own rounding, or 0.5 per cent) and the capitalised names in it; an item is cracked at 80
per cent. Instruction-following is paid for answering every deliverable. A missed main call keeps
5 of 35, the rubric's surviving components.

The score is a proxy and is recorded for the record, not for the gate. The decision reads one fact
from it: landed or missed.

## Isolation, which is the whole value

- The sandbox is fresh for every round (`<scratchpad>/solve-<task>-<k>/`), unzipped from
  `target.zip` where it exists so the solver sees the shipped bytes. Nothing else sits under the
  scratchpad while the solver runs: no earlier round's copy, no results, no notes.
- The spawn prompt names the sandbox as the only readable location and forbids everything else on
  the machine. It forbids `Agent`, `WebSearch`, `WebFetch` and every server-side tool, and it says
  the files are the universe: a fact absent from the folder does not exist.
- The solver gets `Bash`, because the work is pandas work and a solver that cannot compute is
  grading the prompt's readability.
- The solver's output is written by the main thread to a results folder outside the scratchpad and
  graded from there. The task folder receives only `solver_rounds/<label>.md` and the row in
  `pipeline.json`.

## Reading a path

The solver's `path` is the trace the portal never gives you. Read it against the ladder's rungs:
the last rung whose step appears in the path is the depth it reached, and the step after that is
where it left the ladder. Three shapes recur:

- **It stopped at a rung it never saw.** The path goes from rung k straight to the answer with no
  sentence about rung k+1's quantity. The rung is silent, which is what was wanted; if the solver
  still landed the call, discriminator dominance failed (the rung cannot move the answer) and the
  fix is in the magnitudes, not the silence.
- **It saw the rung and declined it.** The path names the quantity and argues it away ("no basis in
  the folder to exclude these"). The pin is too weak or the control that would have settled it is
  not tied to the method. Tie it (a clause that makes reproduction the gate) rather than louder.
- **It executed the rung as a work order.** The path performs the step with no apparent effort. The
  rung was announced somewhere; `leak-check` sweep 4 and 5 find where.

**Then classify where the miss happened, against the three rules** (`../stumping/SKILL.md` Part 1). A
miss counts only when the solver left the ladder at the decisive analytical step: its path read the
fields and applied the stated rules correctly and still took the easy analytical route the card's
`analyst_test` names. A solver that missed because it misread a field, code or unit, or misapplied a
stated rule, is a miss on a lower rung that tells you nothing about the stump; record it as such in the
round's file, and if it is the only way the round was missed, the round says nothing about the decisive
step and the build goes back to design to make the analytical step decisive.

## What this is not

- Not the portal. The ledger row waits for the portal result, and nothing a solver round says is
  written there.
- Not a judge. Determinism is the `determinism-check` skill's business and the rehearsal is its
  agent; whether a different answer is a stump or a defensible second reading is decided there, at
  stage 7.
- Not a second opinion on the design. The solver never sees the design note, so it cannot comment
  on it.

## Checklist

- [ ] The build is finished and through the leak check: submission written, goldens recompute, `leak.py` not LEAK, the reader quoted nothing for question 1
- [ ] One `Explore` solver (`model: opus`, `effort: medium`) run in a fresh sandbox, its path read against the ladder
- [ ] Main call read by the main thread, `--landed` passed where the token match misjudged
- [ ] Worth-it gate applied: pass when the solver did not commit to the main call
- [ ] A landed round's brief written, and the attempt in `## Tried and rejected` with the solver's own path sentence
- [ ] Round, score and decision recorded in `pipeline.json` `solver_rounds`
- [ ] No more than three hardening loops on one architecture, then re-root; three architectures, then retire
