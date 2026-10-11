---
name: solver-round
description: "Stage 6 of the build pipeline, the in-house filter before the determinism judge and the portal. Run an independent solve of a built task in-house, before the portal, and grade it against submission.md with the rubric's weights. Each solver sees the prompt and the bundle and nothing else and returns its committed call and every ask figure as structured output; grade.py turns that into a proxy score, a landed-or-missed flag on the main call and a per-ask hit table, written to <task>/solver_rounds/ and pipeline.json. Plain and skeptic run together; the worth-it gate (one solver off the main call, the pair's mean proxy at 40 or less, no fork) sends the build on to the judge, and a failed round sends it back to design with a hardening brief, three loops per architecture. Run by /build at stage 6 and by /solve. A round is a filter, never an oracle: a build the solvers crack does not go to the portal, and a build they do not crack still has to."
---

# Solver round

> The portal is the oracle and it costs a day per answer. A solver round costs a quarter of an hour
> and answers the one question the author most needs before spending that day: does a competent
> reader with no knowledge of the design land the call? When the answer is yes, the build goes back to
> design and the round has said so for the price of a coffee. When the answer is no, the round has said
> nothing certain, and the build goes to the portal with one fewer way to fail.

## What a round is

One or two isolated agents, each handed a fresh copy of `prompt.md` and `target/` in the scratch
directory and nothing else, each asked to do the work the prompt asks for and to return, as
structured output: the committed main call in one sentence, every figure every deliverable owes in
the prompt's unit and rounding, the path it took in ordered steps, its confidence and any notes.
No deliverable files are produced; the figures are what the rubric grades and the figures are what
`grade.py` compares.

**The solver is told nothing about the task's purpose.** Not that it is a benchmark, not that there
is a trap, not what the client's model tends to miss. A solver that hunts for a trap is not the
portal's model. The one thing it is told beyond the prompt is the working rule a real analyst has:
compute from the files, reconcile where the files let you, commit to one answer per ask, and state
units.

**Two lenses, used in order.**

| Lens | Agent | Told | Reads as |
|---|---|---|---|
| plain | `Explore` type (carries no repo instructions) | the prompt, the folder, the working rule | the portal's model |
| skeptic | `general-purpose` type | the same, plus: "the published figures in the folder are a test of your method; a method that does not reproduce every one of them is not admissible" | the strongest response in the field |

The skeptic is an upper bound. A build the skeptic cracks may still stump the portal; a build the
plain solver cracks will not.

## The rounds, and the decision rule

**Every round runs both lenses together** (`/solve taskNN 2`), because the bar averages the top two
responses: the plain solver stands for the field and the skeptic for its strongest response.

**The worth-it gate** (`build-pipeline`, stage 6). A round passes when at least one solver misses the
main call, the two proxy scores average 40 or less, and every miss is a stump rather than a fork. The
main thread reads each path to decide the last: a different answer reached for a reason the pack does
not rule out is a determinism finding, closed with a pin at stage 2 or 3, and never counted as a pass.

**A failed round is hardened, not sent on.** The report names, for each failure, the brief the next
design answers: the path step that landed the main call (the next rung is built so that exact step
completes and still returns the wrong answer), the asks that leaked score (hardened in the ask layer
against the pair ceiling), or the pin a fork needs. Each attempt goes into the design note's
`## Tried and rejected` with the solver's own sentence, and the build loops through design, build,
leak check and duplicate check to a fresh round on fresh scratch copies.

**A hardening deepens the analysis, never plants.** It works in Layer 2 (the analytical pitfall) or
Layer 1 (honest mess), within the client's two-layer standard. A rung whose only purpose is to trip
this solver's particular sentence is tuning to the solver, and a fix that needs a decoy, a doctored
figure or a withheld rule means the architecture is spent.

**Three hardening loops per architecture, then re-root; three architectures per task number, then
retire** (`build-pipeline`, Retirement). A ladder patched three times against the same solvers is
being tuned to them, and the portal is a different solver.

**Rounds are run on a finished build that has passed the leak check**, after the submission is
written and the goldens recompute, because the grader reads block 1 and block 4 of `submission.md`
and a solver reading a leak measures nothing.

## Grading

```
python3 .claude/skills/solver-round/grade.py task100 <solver_output.json> --label "round 1, plain" [--landed yes|no]
```

Weights 35 / 7 / 58, the planning weights. The main call is matched on its tokens (the names and
figures in block 1's bold sentence, 80 per cent present in the solver's sentence); a wrong set can
share most of the right names, so **the main thread reads both sentences and passes `--landed`
when the token match is wrong**. Each block 4 item is one ask; its tokens are the numbers (to the
golden's own rounding, or 0.5 per cent) and the capitalised names in it; an item is cracked at 80
per cent. Instruction-following is paid for answering every deliverable. A missed main call keeps
5 of 35, the rubric's surviving components.

The score is a proxy. It is read for two facts, landed or missed and which asks held, and the
pair arithmetic in `supplemental-stumping` Part 0 is applied to those facts rather than to the
decimal.

## Isolation, which is the whole value

- The scratch copy is fresh for every round (`<scratchpad>/solve-<task>-<k>/`), unzipped from
  `target.zip` where it exists so the solver sees the shipped bytes.
- The spawn prompt names the scratch path as the only readable location and names the task folder,
  `DESIGN_NOTE.md`, `generator/`, `submission.md`, `solver_rounds/`, `leak_check_report.md` and every
  other task folder as forbidden. It forbids `Agent`, `WebSearch`, `WebFetch` and every server-side
  tool, and it says the files are the universe: a fact absent from the folder does not exist.
- The solver gets `Bash`, because the work is pandas work and a solver that cannot compute is
  grading the prompt's readability.
- The solver's output is written by the main thread to `<scratchpad>/solve-<task>-<k>/<lens>.json`
  and graded from there. The task folder receives only `solver_rounds/<label>.md` and the row in
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

## What this is not

- Not the portal. The ledger row waits for the portal result, and nothing a solver round says is
  written there.
- Not a judge. Determinism is the `determinism-check` skill's business and the rehearsal is its
  agent; a solver that lands a different answer for a defensible reason is a determinism finding,
  not a stump, and the round's report says which.
- Not a second opinion on the design. The solver never sees the design note, so it cannot comment
  on it.

## Checklist

- [ ] The build is finished and through the leak check: submission written, goldens recompute, `leak.py` not LEAK, the reader quoted nothing for question 1
- [ ] Plain and skeptic run together on fresh scratch copies, each path read against the ladder
- [ ] Main calls read by the main thread, `--landed` passed where the token match misjudged
- [ ] Worth-it gate applied: one solver off the call, mean proxy at 40 or less, every miss a stump and not a fork
- [ ] A failed round's brief written, and the attempt in `## Tried and rejected` with the solver's own path sentence
- [ ] Round, scores and decision recorded in `pipeline.json` `solver_rounds`
- [ ] No more than three hardening loops on one architecture, then re-root; three architectures, then retire
