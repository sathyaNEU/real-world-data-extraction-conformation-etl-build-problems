# DQ16, Which local areas' register counts breach the undercoverage alert

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `survey-research-official-statistics` / `census-register-administrative-data-quality` |
| Layer 2 pattern | `survey-research-official-statistics/census-register-administrative-data-quality/1` |
| Layer 2 family | `field_method` |
| Committed call | The areas flagged for the register-improvement programme. |

## The pitfall

Dual-system estimates are computed within post-strata where capture is homogeneous, after removing erroneous enumerations. A pooled Lincoln-Petersen estimate carries correlation bias and counts duplicates.

## The tempting shortcut

One pooled estimate from raw register and survey counts.

## What pins the rigorous method

Matched counts and erroneous enumeration rates by post-stratum are filed, and the alert defines net undercoverage.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
