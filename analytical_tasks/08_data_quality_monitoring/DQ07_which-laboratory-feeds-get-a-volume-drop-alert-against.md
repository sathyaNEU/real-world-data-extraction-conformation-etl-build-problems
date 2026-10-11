# DQ07, Which laboratory feeds get a volume-drop alert, against the seasonal baseline

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `epidemiology-public-health` / `disease-surveillance-outbreak-anomaly-detection` |
| Layer 2 pattern | `epidemiology-public-health/disease-surveillance-outbreak-anomaly-detection/1` |
| Layer 2 family | `forecast_uncertainty` |
| Committed call | Which feeds are escalated to the laboratory liaison this week. |

## The pitfall

Incoming report volume moves with the season. The expected count comes from the same weeks in prior seasons with trend, past anomalies downweighted; comparing with recent weeks flags a normal seasonal fall as a feed failure.

## The tempting shortcut

Compare this week's volume with the mean of the last four weeks.

## What pins the rigorous method

The feed-monitoring standard names the baseline method and the number of prior seasons, and the alert threshold.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
