# DQ01, Which guardrail metric the experiment platform's automated alert watches

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `product-analytics` / `metric-definition-measurement-science` |
| Layer 2 pattern | `product-analytics/metric-definition-measurement-science/1` |
| Layer 2 family | `estimation_fit` |
| Committed call | The metric the platform's auto-alert is wired to for next quarter, with its threshold. |

## The pitfall

A candidate alert metric is scored on past launches with known outcomes: how often it detects a real regression and agrees in direction, against its own variance. The metric that moved most is usually the noisiest.

## The tempting shortcut

Pick the candidate with the largest percent movement across past launches.

## What pins the rigorous method

A labelled set of past launches with known regressions, and the alert standard naming sensitivity at a stated false-alert rate as the criterion.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
