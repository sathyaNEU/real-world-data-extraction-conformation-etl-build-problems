# DQ18, Which monitoring sites' annual compliance statistic is reportable

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `environmental-monitoring-exceedance` |
| Layer 2 pattern | `own:data-capture-before-exceedance` |
| Layer 2 family | `field_method` |
| Committed call | Report, report with a data-capture flag, or withhold, for each site. |

## The pitfall

A daily or annual statistic is valid only when the data capture rule is met (a stated share of valid hours per day, of valid days per quarter). Counting exceedances over whatever readings arrived biases the compliance figure and hides gaps.

## The tempting shortcut

Count exceedances and compute annual means over the readings that exist.

## What pins the rigorous method

The network's QA standard states the capture thresholds and the averaging periods.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
