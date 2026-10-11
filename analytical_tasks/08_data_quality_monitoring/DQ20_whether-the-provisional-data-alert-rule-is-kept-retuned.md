# DQ20, Whether the provisional-data alert rule is kept, retuned or retired

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `environmental-monitoring-exceedance` |
| Layer 2 pattern | `own:alert-scored-on-ratified-data` |
| Layer 2 family | `forecast_uncertainty` |
| Committed call | Keep, retune (with the new threshold) or retire the rule for next season. |

## The pitfall

Alerts run on provisional data, and ratification later applies calibration corrections. An alert rule's hit and false-alarm rates are scored against ratified concentrations, aligned on the episode the alert claimed.

## The tempting shortcut

Score the rule against the provisional stream it ran on.

## What pins the rigorous method

Ratified datasets are published with their ratification dates, and the alert policy states the target hit and false-alarm rates.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
