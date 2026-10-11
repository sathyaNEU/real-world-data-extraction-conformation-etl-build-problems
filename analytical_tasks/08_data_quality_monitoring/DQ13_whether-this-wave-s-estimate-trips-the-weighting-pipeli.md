# DQ13, Whether this wave's estimate trips the weighting-pipeline quality alert

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `survey-research-official-statistics` / `nonresponse-calibration-measurement-error-adjustment` |
| Layer 2 pattern | `survey-research-official-statistics/nonresponse-calibration-measurement-error-adjustment/1` |
| Layer 2 family | `field_method` |
| Committed call | Which published domains are flagged in this wave's quality report. |

## The pitfall

Nonresponse adjustment is computed within the named weighting cells on base weights. One overall unweighted factor leaves differential nonresponse in the estimate and moves it across the alert band.

## The tempting shortcut

Inflate every respondent weight by the inverse of the overall unweighted response rate.

## What pins the rigorous method

The weighting specification names the cells and the base-weighted adjustment; the alert band is filed.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
