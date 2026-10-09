---
description: Build one task end to end from a domain and an objective, through the pipeline's stages (draw, design, build, /approve, two solver rounds, judge rehearsal, leak read, deliver), stopping only at the two author checkpoints. Resumes a build in flight from its pipeline.json.
argument-hint: <domain> <objective> [taskNN] | resume taskNN | taskNN from <stage>
---

# /build

Run the build pipeline for the task described by `$ARGUMENTS`. Invoke the `build-pipeline` skill
first; the stage table, the gates, `pipeline.json` and the hardening loop are its business and are
not restated here.

**Resolve the arguments.**

- `<domain> <objective>` starts a new build. Both must be one of the nine domains and one of the
  eight objectives in `guide-to-prompt`; map plain words to the vocabulary keys (`supply chain`
  to `supply-chain-logistics`, `forecasting` to `forecasting`). The task number is the next free
  `taskNN` under the repo root unless one is given.
- `resume taskNN` continues from the stage in `<task>/pipeline.json`.
- `taskNN from <stage>` re-enters at a named stage (a number or a name from the stage table), for
  example after the author has hardened by hand.

**Then run the stages in order**, invoking each stage's skills before doing its work, and leaving a
stage only when its gate holds. Two rules about how:

1. **Checkpoint A and checkpoint B are the only places this command stops for the author.** At A,
   present the draw in ten lines (pairing, niche, stump sentence, shape, deliverables, nearest
   exemplar and its measured mean, guard verdict) and ask go or redraw with `AskUserQuestion`. At
   B, tell the author the build is cut and ask them to run `/approve taskNN` after reading the
   stump sentence against the pack; stop there, because `/approve` is theirs. Every other gate is
   a script or a thread, and a failed gate is fixed and re-run without asking.
2. **This invocation is the author's licence for the token-spending stages** (solver rounds via the
   `/solve` procedure, the judge rehearsal via `determinism-check`, the leak reader via
   `/leak-check`). Follow each one's own command or skill text for how to spawn, and spawn each
   exactly as many times as the stage says.

**Write `pipeline.json` at every stage boundary**, and `updated` with the ISO date. On a hardening
loop, increment `harden_loops` and write the solver's path sentence to the design note's
`## Tried and rejected` before touching the generator.

**At delivery**, report to the author in this order: the committed answer, the stump sentence, the
two rounds' proxy scores (landed or missed, asks cracked), the judge's verdict and Gate G line, the
leak read's four answers, the heart verdict and nearest build, the zip paths. Then stop. The ledger
row, the skill lessons and memory wait for the portal result.

**Do not** run `/clone-check` from here (it is the author's), do not write the shipped ledger, and
do not create any file in the task folder other than the ones the skills name.
