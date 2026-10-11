# task238: start here

| | |
|---|---|
| Task | task238 |
| Objective (Axis 1) | Data Quality Monitoring & Alerting |
| Block | task228 to task252 |
| Lane owner | developer 3 (current owner and status: the root `START_HERE.md` on main) |
| Seed | DQ11, `analytical_tasks/08_data_quality_monitoring/DQ11_whether-a-new-survey-mode-s-data-can-be-pooled-into-the.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task238`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task238-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** Whether a new survey mode's data can be pooled into the tracker
- **objective:** Data Quality Monitoring & Alerting
- **domain:** psychology-behavioral-science · psychometric-measurement-scale-validation
- **committed_call:** Pool, pool with a mode adjustment flag, or keep the mode separate, for each tracked index.
- **driving_force:** Five-point items are ordinal. Invariance across modes is tested with polychoric correlations and a categorical estimator; Pearson-based ML fit attenuates loadings and misjudges invariance.
- **technique:** psychology-behavioral-science/psychometric-measurement-scale-validation/2

## Seed note

## DQ11, Whether a new survey mode's data can be pooled into the tracker

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `psychology-behavioral-science` / `psychometric-measurement-scale-validation` |
| Layer 2 pattern | `psychology-behavioral-science/psychometric-measurement-scale-validation/2` |
| Layer 2 family | `field_method` |
| Committed call | Pool, pool with a mode adjustment flag, or keep the mode separate, for each tracked index. |

### The pitfall

Five-point items are ordinal. Invariance across modes is tested with polychoric correlations and a categorical estimator; Pearson-based ML fit attenuates loadings and misjudges invariance.

### The tempting shortcut

Run ML CFA on Pearson correlations of the items and compare fit by mode.

### What pins the rigorous method

Items are filed as ordinal, and the tracker's quality standard names the categorical estimator and the invariance criterion.

### Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

### Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
