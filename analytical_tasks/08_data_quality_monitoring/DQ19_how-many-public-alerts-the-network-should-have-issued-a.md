# DQ19, How many public alerts the network should have issued, and the alert configuration that follows

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `environmental-monitoring-exceedance` |
| Layer 2 pattern | `own:standard-averaging-period-alerts` |
| Layer 2 family | `field_method` |
| Committed call | The corrected alert configuration and next season's expected alert count per site. |

## The pitfall

An exceedance is assessed on the standard's averaging period and rounding rule (a rolling 8-hour mean, a 24-hour mean), not on hourly values. Alerts configured on hourly readings over-fire.

## The tempting shortcut

Count hours above the limit value as exceedances.

## What pins the rigorous method

The standard names the averaging period, the data rule for a valid average and the reporting rounding.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
