# DQ14, Which domain estimates fail the calibration margin check and are reissued

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `survey-research-official-statistics` / `nonresponse-calibration-measurement-error-adjustment` |
| Layer 2 pattern | `survey-research-official-statistics/nonresponse-calibration-measurement-error-adjustment/2` |
| Layer 2 family | `field_method` |
| Committed call | The reissue list for the release. |

## The pitfall

Raking cycles through every margin until all match within tolerance. One pass matches only the last margin, so earlier margins and the domain estimates built on them drift.

## The tempting shortcut

Treat one ratio pass per margin as calibrated.

## What pins the rigorous method

Marginal control totals for several variables and a stated convergence tolerance are filed.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
