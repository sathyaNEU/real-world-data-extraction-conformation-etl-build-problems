---
description: Build one task end to end through the pipeline's stages (draw, design gated by precut.py, build, leak check and duplicate check together, solver round with its hardening loop and ask gate, determinism check in the background, ship) without stopping for the author. Takes a task number handed out in START_HERE.md, or a domain and an objective. Resumes a build in flight from its pipeline.json, and takes a shipped task brought back with portal feedback down the returned-task path.
argument-hint: taskNN | <domain> <objective> [taskNN] | resume taskNN | taskNN from <stage> | taskNN returned
---

# /build

Run the build pipeline for the task described by `$ARGUMENTS`. Invoke the `build-pipeline` skill
first; the stage table, the gates, `pipeline.json`, the returned-task path and retirement are its
business and are not restated here.

**Resolve the arguments.**

- `taskNN` starts the build handed out in the root `START_HERE.md`, from the seed and the objective
  in `taskNN/START_HERE.md`.
- `<domain> <objective>` starts a new build. The domain must be a client domain or a house domain and
  the objective one of the eight in `guide-to-prompt`; map plain words to the vocabulary keys. The task
  number is the one given, or a new row added to the root `START_HERE.md` on `main` first.
- `resume taskNN` continues from the stage in `<task>/pipeline.json`.
- `taskNN from <stage>` re-enters at a named stage, for example after the author fixed something by hand.
- `taskNN returned` takes a shipped task the author has brought back with portal feedback down the
  returned-task path (`build-pipeline`, Returned tasks): the portal result pasted into the brief, a
  designer when the call landed, a builder when it held, the free mechanical gates only, commit, re-cut,
  ship. No reader, round, judge or clone check runs for it.

**Then run the stages in order**, invoking each stage's skills before doing its work, and leaving a
stage only when its gate holds. Rules about how:

1. **The command does not stop for the author.** When the draw is filed, show it in ten lines (pairing,
   niche, the default path's answer against the golden, the stump sentence, shape, deliverables, nearest
   exemplar and its measured mean, guard verdict) and carry on; the author can interrupt or redraw. Every
   gate is a script or a thread, and a failed gate is fixed and re-run without asking.
2. **Stage 2 is left only on `precut.py` exit 0** (`stumping` Part 5). A default path that ends on the
   golden is redesigned, not argued; a note that fails twice on the default path is re-rooted before any
   data is cut.
3. **Stage 3 is left only when the free gates are green**: the generator's checks with every semantic
   fork asserted, the verifier, two byte-identical builds, `figures_check.py`, the realism sweep,
   `leak.py`, `guard.py surface`.
4. **This invocation is the author's licence for every token-spending stage**: the leak reader (stage 4,
   `/leak-check`'s one isolated Sonnet agent, once per build and again only when a fix changed a document
   or the prompt), the adjudicated duplicate check (stage 5, the `clone-auditor` agent in pre-flight
   mode), every solver round the loop needs (stage 6, `/solve taskNN`: one isolated `Agent` in a
   sandbox) and the determinism judge (stage 7, the `determinism-judge` agent, one pass). Follow each one's
   own command or skill text for how to spawn. Every agent runs on the model and effort `build-pipeline`
   (Models and effort) sets for its role: the designer on Opus at max, the solver on Opus at high, the
   rest at medium.
5. **Stages 4 and 5 are spawned together** and the round waits for both. While they run, register the
   next number's draw if a slot is free.

**The solver round drives the loop** (`solver-round`). `grade.py` exit 0 passes: repair the reader's
deferred findings once (stage 6b) and spawn the judge in the background while the ship stage's
non-figure work proceeds. Exit 2 (LANDED): take the round's brief, with the deferred findings folded in,
back to stage 2; the designer rewrites the default path and the decisive step, `precut.py` re-runs, a
builder rebuilds, the leak check, the heart check and a fresh round follow; three loops per architecture,
then re-root at stage 1 in the same objective and number, three architectures, then retire. Exit 3 (ASKS
LEAK): a builder rebuilds the ask layer against a rewritten cracker sheet (`supplemental-stumping` Part 4)
and a fresh round runs; the ladder is not touched. Each repair is a fresh agent spawned from the main
session with a short brief pointing at the committed round log, `pipeline.json` and the design note,
never the agent that built the pack resumed. The judge's FIX_NOW is repaired and re-judged once, with a
fresh round first only when the fix moved a graded figure, a rung or a document the solver read.

**Write `pipeline.json` at every stage boundary**, with `updated` as the ISO date.

**At ship**, report to the author in this order: the committed answer, the stump sentence and the
default path's answer, the three-rules line, the leak line (`leak.py` verdict and the reader's
question-1 answer), the duplicate-check line (heart verdict, nearest build and its similarity, the
pre-flight verdict), the solver line (rounds run, architectures used, the passing round's proxy and ask
share, the answer the solver committed to and where it left the ladder), the judge's verdict and Gate G
line, the zip path. Then stop. The ledger row, the skill lessons and memory wait for the portal result. A
build retired under the retirement rule is reported in one line with the reason.

**Do not** write the shipped ledger, or create any file in the task folder other than the ones the
skills name (`solver_rounds/` included).
