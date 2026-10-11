---
description: Build one task end to end through the pipeline's stages (draw, design, build, leak check, duplicate check, solver round with its hardening loop, determinism check, ship) without stopping for the author, looping design and build until the solver round's worth-it gate passes. Takes a task number handed out in START_HERE.md, or a domain and an objective. Resumes a build in flight from its pipeline.json.
argument-hint: taskNN | <domain> <objective> [taskNN] | resume taskNN | taskNN from <stage>
---

# /build

Run the build pipeline for the task described by `$ARGUMENTS`. Invoke the `build-pipeline` skill
first; the stage table, the gates, `pipeline.json` and retirement are its business and are not
restated here.

**Resolve the arguments.**

- `taskNN` starts the build handed out in the root `START_HERE.md`, from the seed and the objective
  in `taskNN/START_HERE.md`.
- `<domain> <objective>` starts a new build. The domain must be a client domain or a house domain and
  the objective one of the eight in `guide-to-prompt`; map plain words to the vocabulary keys
  (`supply chain` to `supply-chain-logistics`, `forecasting` to `forecasting`). The task number is
  the one given, or a new row added to the root `START_HERE.md` on `main` first.
- `resume taskNN` continues from the stage in `<task>/pipeline.json`.
- `taskNN from <stage>` re-enters at a named stage (a number or a name from the stage table), for
  example after the author has fixed something by hand.

**Then run the stages in order**, invoking each stage's skills before doing its work, and leaving a
stage only when its gate holds. Two rules about how:

1. **The command does not stop for the author.** When the draw is filed, show it in ten lines
   (pairing, niche, stump sentence, shape, deliverables, nearest exemplar and its measured mean,
   guard verdict) and carry on; the author can interrupt or redraw. Every gate is a script or a
   thread, and a failed gate is fixed and re-run without asking.
2. **This invocation is the author's licence for every token-spending stage**: the leak reader
   (stage 4, `/leak-check`'s one isolated agent, on every loop where a document changed), the
   adjudicated duplicate check (stage 5, the `clone-auditor` agent in pre-flight mode on this build),
   every solver round the loop needs (stage 6, `/solve taskNN`: one isolated `Agent` in a sandbox)
   and the determinism judge (stage 7, the
   `determinism-judge` agent, spawned once per pass). Follow each one's own command or skill text
   for how to spawn.

**The solver round drives the loop.** After the leak check and the duplicate check, run the round
(`solver-round`); when the solver does not commit to the main call, go to the judge; when it lands
the call, take the round's brief back to stage 2,
harden, rebuild, leak-check and solve again, three loops per architecture, then re-root at stage 1
in the same objective and number, three architectures, then retire (`build-pipeline`, the worth-it
gate and Retirement). Difficulty is still argued on paper first (the stump sentence, the ladder, the
closure table); the round tests it. The judge's FIX_NOW repairs a determinism or spec defect and is
re-judged once, with a fresh round first when the fix moved a graded figure, a rung or a document.

**Write `pipeline.json` at every stage boundary**, and `updated` with the ISO date.

**At ship**, report to the author in this order: the committed answer, the stump sentence, the
three-rules line (the swap test, both layers, the decisive step's class and the analyst test), the leak line (`leak.py` verdict and the reader's question-1 answer), the duplicate-check line (heart
verdict, nearest build and its similarity, the pre-flight verdict), the solver line (rounds run,
architectures used, the passing round's proxy, the answer the solver committed to and where it left
the ladder), the judge's verdict and Gate G line, the zip path. Then stop. The ledger row, the
skill lessons and memory wait for the portal result. A build retired under `build-pipeline`'s
retirement rule is reported in one line with the reason.

**Do not** write the shipped ledger, or create any file in the task folder other than the ones the
skills name (`solver_rounds/` included).
