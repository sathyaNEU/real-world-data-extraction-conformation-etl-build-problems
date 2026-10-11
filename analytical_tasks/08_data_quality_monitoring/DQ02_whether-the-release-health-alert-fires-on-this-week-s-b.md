# DQ02, Whether the release-health alert fires on this week's build, when the metric is the average user's rate

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `product-analytics` / `metric-definition-measurement-science` |
| Layer 2 pattern | `product-analytics/metric-definition-measurement-science/2` |
| Layer 2 family | `estimation_fit` |
| Committed call | Fire or hold the release-health alert for each build in the current train. |

## The pitfall

A per-user rate and a pooled ratio answer different questions, and a pooled ratio is carried by heavy users. The alert metric follows the stated unit of analysis, and its control limits follow from that choice.

## The tempting shortcut

Divide total crashes by total sessions for the build and compare with the pooled limit.

## What pins the rigorous method

The release-health standard defines the metric on the average user, with its limit method.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
