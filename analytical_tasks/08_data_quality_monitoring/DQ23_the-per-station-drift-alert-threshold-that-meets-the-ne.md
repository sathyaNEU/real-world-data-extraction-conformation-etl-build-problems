# DQ23, The per-station drift-alert threshold that meets the network's false-alert budget

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `sensor-calibration-measurement` |
| Layer 2 pattern | `own:network-false-alarm-budget` |
| Layer 2 family | `forecast_uncertainty` |
| Committed call | The threshold, and the expected alerts per month it produces. |

## The pitfall

A two-sigma rule at every one of many stations fires several false alerts a week. The threshold is set for the network: a stated false-alert budget per month across all stations, from the stations' in-control behaviour.

## The tempting shortcut

Apply a per-station two-sigma rule.

## What pins the rigorous method

The operations standard states the acceptable false alerts per month across the network.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
