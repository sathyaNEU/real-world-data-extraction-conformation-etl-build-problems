---
description: Build one task end to end from a domain and an objective, through the pipeline's stages (draw, design, build, duplicate check, determinism check, ship) without stopping for the author. No solver round and no re-iteration loop. Resumes a build in flight from its pipeline.json.
argument-hint: <domain> <objective> [taskNN] | resume taskNN | taskNN from <stage>
---

# /build

Run the build pipeline for the task described by `$ARGUMENTS`. Invoke the `build-pipeline` skill
first; the stage table, the gates, `pipeline.json` and retirement are its business and are not
restated here.

**Resolve the arguments.**

- `<domain> <objective>` starts a new build. Both must be one of the nine domains and one of the
  eight objectives in `guide-to-prompt`; map plain words to the vocabulary keys (`supply chain`
  to `supply-chain-logistics`, `forecasting` to `forecasting`). The task number is the next free
  `taskNN` under the repo root unless one is given.
- `resume taskNN` continues from the stage in `<task>/pipeline.json`.
- `taskNN from <stage>` re-enters at a named stage (a number or a name from the stage table), for
  example after the author has fixed something by hand.

**Then run the stages in order**, invoking each stage's skills before doing its work, and leaving a
stage only when its gate holds. Two rules about how:

1. **The command does not stop for the author.** When the draw is filed, show it in ten lines
   (pairing, niche, stump sentence, shape, deliverables, nearest exemplar and its measured mean,
   guard verdict) and carry on; the author can interrupt or redraw. Every gate is a script or a
   thread, and a failed gate is fixed and re-run without asking.
2. **This invocation is the author's licence for the two token-spending stages**: the adjudicated
   duplicate check (stage 4, the `clone-auditor` agent in pre-flight mode on this build, spawned
   once) and the determinism judge (stage 5, the `determinism-judge` agent, spawned once per pass).
   Follow each one's own command or skill text for how to spawn.

**There is no solver round.** Do not run `/solve` or the `solver-round` skill, and do not rebuild a
design because an in-house solve reached the golden answer. Difficulty is argued on paper in the
design note (the stump sentence, the ladder, the closure table) and checked by the determinism
judge. The only loop is the judge's FIX_NOW, which is a repair of a determinism or spec defect and
is re-judged once.

**Write `pipeline.json` at every stage boundary**, and `updated` with the ISO date.

**At ship**, report to the author in this order: the committed answer, the stump sentence, the
duplicate-check line (heart verdict, nearest build and its similarity, the pre-flight verdict), the
judge's verdict and Gate G line, the leak verdict, the zip path. Then stop. The ledger row, the
skill lessons and memory wait for the portal result. A build retired under `build-pipeline`'s
retirement rule is reported in one line with the reason.

**Do not** write the shipped ledger, run the `/leak-check` reader pass (the author's; the mechanical
`leak.py` sweep runs in stage 3), or create any file in the task folder other than the ones the
skills name.
