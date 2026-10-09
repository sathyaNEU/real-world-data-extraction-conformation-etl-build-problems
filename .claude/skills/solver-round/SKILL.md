---
name: solver-round
description: "Run an independent solve of a built task in-house, before the portal, and grade it against submission.md with the rubric's weights. One plain solver first; two solvers (plain and skeptic) only when the first was stumped. The solver sees the prompt and the bundle and nothing else, returns its committed call and every ask figure as structured output, and grade.py turns that into a proxy score, a landed-or-missed flag on the main call and a per-ask hit table, written to <task>/solver_rounds/ and pipeline.json. Invoked by /solve and by the /build pipeline's stages 4 and 5; the result goes back to the builder as the hardening brief. A round is a filter, never an oracle: a build a solver cracks does not go to the portal, and a build no solver cracks still has to."
---

# Solver round

> The portal is the oracle and it costs a day per answer. A solver round costs a quarter of an hour
> and answers the one question the author most needs before spending that day: does a competent
> reader with no knowledge of the design land the call? When the answer is yes, the build is dead
> and the round has said so for the price of a coffee. When the answer is no, the round has said
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

**Round 1: one plain solver.** Pass when the main call is missed **and** the proxy score is under
40. Otherwise the build is hardened, not sent on. The round's report says which step of the path
landed the solver on the call, and that step is the hardening brief: the next rung is built so that
exact step completes and still returns the wrong answer, and the attempt is written into the
design note's `## Tried and rejected` with the solver's own sentence.

**Round 2: two solvers, plain and skeptic, run together.** Only after round 1 passes. Pass when the
two proxy scores average under 40 and at least one is under 25. Both solvers landing the call is a
re-root, not a hardening: the mechanism is readable. **The author's standing waiver:** when the
three hardening loops are spent, both solvers of the last round 2 missed the main call and the pair
averages under 40, the build goes on to the judge rehearsal without the one-under-25 condition. That
condition is the one most often missed for a reason the proxy cannot see (a block 4 with few items,
where one kept ask outweighs the whole device layer), and a pair that held the call twice over sits
well inside the portal bar of 50. Record the waiver in `pipeline.json` and the design note.

**Three hardening loops per architecture, then re-root.** A ladder that has been patched three times
against the same solver is being tuned to that solver, and the portal is a different one.

**Rounds are run on a finished build**, after the submission is written and the goldens recompute,
because the grader reads block 1 and block 4 of `submission.md`. A round on an unfinished build
grades against nothing.

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

- [ ] The build is finished: submission written, goldens recompute, `leak.py` not LEAK
- [ ] Round 1 run with one plain solver on a fresh scratch copy, path read against the ladder
- [ ] Main call read by the main thread, `--landed` passed where the token match misjudged
- [ ] Round 1 passed (missed, under 40) before round 2 was run
- [ ] Round 2 run with plain and skeptic together; average under 40, one under 25
- [ ] Every hardening written to `## Tried and rejected` with the solver's own path sentence
- [ ] No more than three hardening loops on one architecture
