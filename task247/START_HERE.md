# task247: start here

| | |
|---|---|
| Task | task247 |
| Objective (Axis 1) | Data Quality Monitoring & Alerting |
| Block | task228 to task252 |
| Lane owner | developer 3 (current owner and status: the root `START_HERE.md` on main) |
| Seed | DQ20, `analytical_tasks/08_data_quality_monitoring/DQ20_whether-the-provisional-data-alert-rule-is-kept-retuned.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task247`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task247-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** Whether the provisional-data alert rule is kept, retuned or retired
- **objective:** Data Quality Monitoring & Alerting
- **domain:** physical-environmental-sciences · environmental-monitoring-exceedance
- **committed_call:** Keep, retune (with the new threshold) or retire the rule for next season.
- **driving_force:** Alerts run on provisional data, and ratification later applies calibration corrections. An alert rule's hit and false-alarm rates are scored against ratified concentrations, aligned on the episode the alert claimed.
- **technique:** own:alert-scored-on-ratified-data

## Seed note

## DQ20, Whether the provisional-data alert rule is kept, retuned or retired

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `environmental-monitoring-exceedance` |
| Layer 2 pattern | `own:alert-scored-on-ratified-data` |
| Layer 2 family | `forecast_uncertainty` |
| Committed call | Keep, retune (with the new threshold) or retire the rule for next season. |

### The pitfall

Alerts run on provisional data, and ratification later applies calibration corrections. An alert rule's hit and false-alarm rates are scored against ratified concentrations, aligned on the episode the alert claimed.

### The tempting shortcut

Score the rule against the provisional stream it ran on.

### What pins the rigorous method

Ratified datasets are published with their ratification dates, and the alert policy states the target hit and false-alarm rates.

### Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

### Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
