---
description: Build one task end to end (draw, design gated by precut.py, build, leak reader and determinism judge together, ship) in this session's main thread, then start the next open task. Takes a task number, or a domain and an objective. Resumes a build from its pipeline.json.
argument-hint: taskNN | next | <domain> <objective> [taskNN] | resume taskNN | taskNN from <stage>
effort: max
---

# /build

Run the pipeline for `$ARGUMENTS`. Invoke the `build-pipeline` skill first: the stages, gates, effort,
commits, `pipeline.json` and retirement are its business and are not restated here.

**Arguments.**

- `taskNN`: the number handed out; `status.py taskNN` prints its seed (header and Situation only).
- `next`: `python3 .claude/skills/build-pipeline/status.py next <handle>` names the next task in the backlog
  wave of the author file matching the session user. A `FAILED_TO_STUMP` rework resumes from its own
  `pipeline.json` at the stage its wave note gives (resume N, redesign at 2, re-root at 1).
- `<domain> <objective>`: a build outside the seeds. The domain is a client domain, the objective one of the
  eight; map plain words to the vocabulary keys. Use the number given, or the next open one in the lane.
- `resume taskNN`, `taskNN from <stage>`: continue from `pipeline.json`, re-checking that stage's gate first.

A returned task is not a `/build`: a determinism finding is `/fix-determinism`, a rubric over 50 with the call
held is `/fix-rubric`, a landed call is `/build taskNN from 2` with the portal result in the design note.

**Run the stages in order** in this thread, invoking each stage's skills before its work and leaving a stage
only when its gate holds.

1. **Do not stop for the author.** When the draw is filed, show it in ten lines (pairing, niche, the default
   path's answer against the golden, the stump sentence, shape, deliverables, nearest driver from `guard.py
   mechanisms`, guard verdict), commit `DRAWN (taskNN)`, and carry on. A failed gate is fixed and re-run
   without asking.
2. **Stage 2 is left only on `precut.py` exit 0.** A default path that ends on the golden is redesigned, not
   argued; two failures on the default path re-root the draw before any data is cut.
3. **Stage 3 is left only when the free gates are green**: generator checks with every fork asserted,
   `verify`, two byte-identical builds, `figures_check.py`, the realism sweep, `leak.py`, `guard.py surface`
   and `heart`.
4. **Stage 4 spawns two agents in one message, in the background:** the leak reader (as `/leak-check` step 4
   describes, `model: sonnet`, `effort: medium`) and the `determinism-judge` agent (medium in its
   definition). This invocation licenses both. While they run, bring the card current and write the
   pre-ship check. Fix every finding from both in one generator pass; re-judge once on FIX_NOW; re-read only
   if a document or the prompt changed. No clone pre-flight runs here; `/clone-check` is the author's call.
5. **Repairs run in this thread.** Spawn a fresh agent only near the context limit, briefed with
   `pipeline.json`, the design note and the findings.

**Write `pipeline.json` at every stage boundary** (with `status` and `updated`), and **commit only at the
status changes** `build-pipeline` names: `DRAWN`, `SHIPPED`, `PAUSED`, `RETIRED`.

**At ship**, report in this order: the committed answer, the stump sentence and the default path's answer,
the three-rules line, the leak line (`leak.py` verdict and the reader's question 1), the duplicate line (heart
verdict, nearest build), the judge's verdict and Gate G line, the zip path. Then **start the next open task
at once**. A retired build is reported in one line with the reason.

Create no file in the task folder other than the ones the skills name.
