---
description: Build one task end to end (draw, design gated by precut.py, build, leak and duplicate check together, determinism judge, ship) without stopping for the author, then start the next open task. Takes a task number from START_HERE.md, or a domain and an objective. Resumes a build from its pipeline.json, and takes a shipped task with portal feedback down the returned-task path.
argument-hint: taskNN | <domain> <objective> [taskNN] | resume taskNN | taskNN from <stage> | taskNN returned
---

# /build

Run the pipeline for `$ARGUMENTS`. Invoke the `build-pipeline` skill first: the stages, gates, models,
`pipeline.json`, returned tasks and retirement are its business and are not restated here.

**Arguments.**

- `taskNN`: the build handed out in the root `START_HERE.md`, from the seed in `taskNN/START_HERE.md`.
- `<domain> <objective>`: a new build. The domain is a client or house domain, the objective one of the
  eight; map plain words to the vocabulary keys. Use the number given, or add a row to the root
  `START_HERE.md` on main first.
- `resume taskNN`: continue from the stage in `<task>/pipeline.json`.
- `taskNN from <stage>`: re-enter at a named stage, for example after the author fixed something by hand.
- `taskNN returned`: the returned-task path. The portal result goes into the brief; a designer when the
  call or determinism failed, a builder otherwise; the free mechanical gates only; commit, re-cut, ship.
  No reader, clone check or judge.

**Run the stages in order**, invoking each stage's skills before its work and leaving a stage only when
its gate holds.

1. **Do not stop for the author.** When the draw is filed, show it in ten lines (pairing, niche, the
   default path's answer against the golden, the stump sentence, shape, deliverables, nearest exemplar,
   guard verdict) and carry on. A failed gate is fixed and re-run without asking.
2. **Stage 2 is left only on `precut.py` exit 0.** A default path that ends on the golden is redesigned,
   not argued; two failures on the default path re-root the draw before any data is cut.
3. **Stage 3 is left only when the free gates are green**: generator checks with every fork asserted,
   `verify`, two byte-identical builds, `figures_check.py`, the realism sweep, `leak.py`, `guard.py
   surface`.
4. **This invocation licenses every thread the pipeline sequences**: the leak reader (`/leak-check`'s
   one Sonnet agent, again only when a fix changed a document or the prompt), the clone pre-flight (the
   `clone-auditor` agent), and the determinism judge (the `determinism-judge` agent, one pass). Follow
   each one's own command or skill for how to spawn. Every agent runs on the model and effort
   `build-pipeline` sets for its role.
5. **Stage 4 spawns the reader and the pre-flight together.** Their findings are fixed in the generator
   by a fresh builder; a decisive-step sentence or a main-call fork goes back to a designer first.
6. **Stage 5, the judge, runs in the background** once stage 4 is clean, while the card and pre-ship
   check proceed. FIX_NOW is repaired by a fresh agent and re-judged once; SEND_BACK re-roots or retires.
7. **Every repair is a fresh agent** spawned from the main session with a short brief naming the
   committed inputs (`pipeline.json`, the report, the design note), never a finished agent resumed.

**Write `pipeline.json` at every stage boundary**, with `updated` as the ISO date.

**At ship**, report to the author in this order: the committed answer, the stump sentence and the default
path's answer, the three-rules line, the leak line (`leak.py` verdict and the reader's question 1), the
duplicate line (heart verdict, nearest build and similarity, pre-flight verdict), the judge's verdict and
Gate G line, the zip path. Then **start the next open task at once** (`build-pipeline`, Throughput). A
retired build is reported in one line with the reason.

**Do not** write the shipped ledger (it waits for the portal), or create any file in the task folder other
than the ones the skills name.
