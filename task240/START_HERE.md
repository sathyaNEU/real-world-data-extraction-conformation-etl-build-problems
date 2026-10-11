# task240: start here

| | |
|---|---|
| Task | task240 |
| Objective (Axis 1) | Data Quality Monitoring & Alerting |
| Block | task228 to task252 |
| Lane owner | developer 3 (current owner and status: the root `START_HERE.md` on main) |
| Seed | DQ13, `analytical_tasks/08_data_quality_monitoring/DQ13_whether-this-wave-s-estimate-trips-the-weighting-pipeli.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task240`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task240-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** Whether this wave's estimate trips the weighting-pipeline quality alert
- **objective:** Data Quality Monitoring & Alerting
- **domain:** survey-research-official-statistics · nonresponse-calibration-measurement-error-adjustment
- **committed_call:** Which published domains are flagged in this wave's quality report.
- **driving_force:** Nonresponse adjustment is computed within the named weighting cells on base weights. One overall unweighted factor leaves differential nonresponse in the estimate and moves it across the alert band.
- **technique:** survey-research-official-statistics/nonresponse-calibration-measurement-error-adjustment/1

## Seed note

## DQ13, Whether this wave's estimate trips the weighting-pipeline quality alert

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `survey-research-official-statistics` / `nonresponse-calibration-measurement-error-adjustment` |
| Layer 2 pattern | `survey-research-official-statistics/nonresponse-calibration-measurement-error-adjustment/1` |
| Layer 2 family | `field_method` |
| Committed call | Which published domains are flagged in this wave's quality report. |

### The pitfall

Nonresponse adjustment is computed within the named weighting cells on base weights. One overall unweighted factor leaves differential nonresponse in the estimate and moves it across the alert band.

### The tempting shortcut

Inflate every respondent weight by the inverse of the overall unweighted response rate.

### What pins the rigorous method

The weighting specification names the cells and the base-weighted adjustment; the alert band is filed.

### Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

### Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
