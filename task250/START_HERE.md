# task250: start here

| | |
|---|---|
| Task | task250 |
| Objective (Axis 1) | Data Quality Monitoring & Alerting |
| Block | task228 to task252 |
| Lane owner | developer 3 (current owner and status: the root `START_HERE.md` on main) |
| Seed | DQ23, `analytical_tasks/08_data_quality_monitoring/DQ23_the-per-station-drift-alert-threshold-that-meets-the-ne.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task250`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task250-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** The per-station drift-alert threshold that meets the network's false-alert budget
- **objective:** Data Quality Monitoring & Alerting
- **domain:** physical-environmental-sciences · sensor-calibration-measurement
- **committed_call:** The threshold, and the expected alerts per month it produces.
- **driving_force:** A two-sigma rule at every one of many stations fires several false alerts a week. The threshold is set for the network: a stated false-alert budget per month across all stations, from the stations' in-control behaviour.
- **technique:** own:network-false-alarm-budget

## Seed note

## DQ23, The per-station drift-alert threshold that meets the network's false-alert budget

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `sensor-calibration-measurement` |
| Layer 2 pattern | `own:network-false-alarm-budget` |
| Layer 2 family | `forecast_uncertainty` |
| Committed call | The threshold, and the expected alerts per month it produces. |

### The pitfall

A two-sigma rule at every one of many stations fires several false alerts a week. The threshold is set for the network: a stated false-alert budget per month across all stations, from the stations' in-control behaviour.

### The tempting shortcut

Apply a per-station two-sigma rule.

### What pins the rigorous method

The operations standard states the acceptable false alerts per month across the network.

### Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

### Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
