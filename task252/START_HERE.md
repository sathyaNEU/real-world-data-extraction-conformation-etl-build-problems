# task252: start here

| | |
|---|---|
| Task | task252 |
| Objective (Axis 1) | Data Quality Monitoring & Alerting |
| Block | task228 to task252 |
| Lane owner | developer 3 (current owner and status: the root `START_HERE.md` on main) |
| Seed | DQ25, `analytical_tasks/08_data_quality_monitoring/DQ25_which-low-level-channels-trip-the-drift-alert-when-read.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task252`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task252-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** Which low-level channels trip the drift alert when readings sit below the detection limit
- **objective:** Data Quality Monitoring & Alerting
- **domain:** physical-environmental-sciences · sensor-calibration-measurement
- **committed_call:** The channels escalated to the laboratory this quarter.
- **driving_force:** Readings below the limit of detection are censored. Substituting half the limit biases the channel mean and its drift; a censored-data estimator gives the level the alert compares.
- **technique:** own:detection-limit-censoring

## Seed note

## DQ25, Which low-level channels trip the drift alert when readings sit below the detection limit

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `sensor-calibration-measurement` |
| Layer 2 pattern | `own:detection-limit-censoring` |
| Layer 2 family | `estimation_fit` |
| Committed call | The channels escalated to the laboratory this quarter. |

### The pitfall

Readings below the limit of detection are censored. Substituting half the limit biases the channel mean and its drift; a censored-data estimator gives the level the alert compares.

### The tempting shortcut

Substitute LOD/2 for censored readings and compute the mean.

### What pins the rigorous method

The laboratory flags censored readings and the alert standard defines the level on the censored-data estimator.

### Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

### Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
