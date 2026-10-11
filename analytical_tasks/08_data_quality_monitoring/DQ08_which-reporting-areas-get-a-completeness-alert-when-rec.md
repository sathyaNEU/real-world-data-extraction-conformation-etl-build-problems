# DQ08, Which reporting areas get a completeness alert, when recent weeks are still filling in

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `epidemiology-public-health` / `disease-surveillance-outbreak-anomaly-detection` |
| Layer 2 pattern | `epidemiology-public-health/disease-surveillance-outbreak-anomaly-detection/2` |
| Layer 2 family | `forecast_uncertainty` |
| Committed call | Which areas receive a completeness alert in this week's run. |

## The pitfall

Notifications arrive with delay, so the latest weeks are undercounted in every area. Completeness is judged against what the empirical delay distribution says should have arrived by now, not against final counts.

## The tempting shortcut

Flag every area whose latest weeks sit below the area's usual weekly count.

## What pins the rigorous method

Report dates are in the extract so the delay distribution is estimable, and the completeness standard defines the expected share received by each lag.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
