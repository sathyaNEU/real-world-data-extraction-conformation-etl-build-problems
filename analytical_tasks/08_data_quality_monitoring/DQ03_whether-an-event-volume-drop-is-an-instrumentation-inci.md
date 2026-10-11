# DQ03, Whether an event-volume drop is an instrumentation incident or a mix shift toward a new client version

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `product-analytics` / `metric-definition-measurement-science` |
| Layer 2 pattern | `product-analytics/metric-definition-measurement-science/3` |
| Layer 2 family | `estimand_identification` |
| Committed call | Which of the monitored event streams get an instrumentation incident opened this week. |

## The pitfall

A topline events-per-user metric can fall while every client segment is flat, because the user mix moved toward a low-baseline client. Decompose into within-segment rate and composition before calling an instrumentation loss.

## The tempting shortcut

Read the topline drop as lost events and open the incident.

## What pins the rigorous method

Segment sizes and rates are filed for both periods, and the incident policy defines an instrumentation loss as a within-segment fall.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
