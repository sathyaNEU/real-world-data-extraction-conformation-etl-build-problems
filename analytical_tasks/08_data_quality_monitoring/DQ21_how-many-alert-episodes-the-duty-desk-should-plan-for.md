# DQ21, How many alert episodes the duty desk should plan for

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `environmental-monitoring-exceedance` |
| Layer 2 pattern | `own:episodes-not-hours` |
| Layer 2 family | `estimation_fit` |
| Committed call | The desk rota for next season, sized on episodes. |

## The pitfall

Consecutive exceedance hours are one episode under the alert policy's gap rule. Treating hours as independent events inflates alert volume and the desk's staffing need.

## The tempting shortcut

Count exceedance hours, or per-hour alerts, as events.

## What pins the rigorous method

The alert policy defines an episode and the question asks episodes per site per season.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
