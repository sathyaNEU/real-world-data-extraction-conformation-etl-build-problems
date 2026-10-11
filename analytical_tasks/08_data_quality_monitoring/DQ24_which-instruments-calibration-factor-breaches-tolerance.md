# DQ24, Which instruments' calibration factor breaches tolerance when both instruments are noisy

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `sensor-calibration-measurement` |
| Layer 2 pattern | `own:errors-in-both-instruments` |
| Layer 2 family | `estimation_fit` |
| Committed call | The instruments flagged for recalibration. |

## The pitfall

When the comparison instrument also has measurement error, the OLS slope between the two is attenuated. An errors-in-variables fit (Deming with the known error ratio) gives the calibration factor.

## The tempting shortcut

Use the OLS slope of one instrument on the other as the factor.

## What pins the rigorous method

Both instruments' precision is filed from repeatability tests, and the protocol calls for an errors-in-variables fit.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
