# task246: start here

| | |
|---|---|
| Task | task246 |
| Objective (Axis 1) | Data Quality Monitoring & Alerting |
| Block | task228 to task252 |
| Lane owner | developer 3 (current owner and status: the root `START_HERE.md` on main) |
| Seed | DQ19, `analytical_tasks/08_data_quality_monitoring/DQ19_how-many-public-alerts-the-network-should-have-issued-a.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task246`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task246-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** How many public alerts the network should have issued, and the alert configuration that follows
- **objective:** Data Quality Monitoring & Alerting
- **domain:** physical-environmental-sciences · environmental-monitoring-exceedance
- **committed_call:** The corrected alert configuration and next season's expected alert count per site.
- **driving_force:** An exceedance is assessed on the standard's averaging period and rounding rule (a rolling 8-hour mean, a 24-hour mean), not on hourly values. Alerts configured on hourly readings over-fire.
- **technique:** own:standard-averaging-period-alerts

## Seed note

## DQ19, How many public alerts the network should have issued, and the alert configuration that follows

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `environmental-monitoring-exceedance` |
| Layer 2 pattern | `own:standard-averaging-period-alerts` |
| Layer 2 family | `field_method` |
| Committed call | The corrected alert configuration and next season's expected alert count per site. |

### The pitfall

An exceedance is assessed on the standard's averaging period and rounding rule (a rolling 8-hour mean, a 24-hour mean), not on hourly values. Alerts configured on hourly readings over-fire.

### The tempting shortcut

Count hours above the limit value as exceedances.

### What pins the rigorous method

The standard names the averaging period, the data rule for a valid average and the reporting rounding.

### Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

### Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
