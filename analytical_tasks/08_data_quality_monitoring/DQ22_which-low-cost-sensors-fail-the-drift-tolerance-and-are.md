# DQ22, Which low-cost sensors fail the drift tolerance and are pulled for recalibration

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `sensor-calibration-measurement` |
| Layer 2 pattern | `own:calibration-direction` |
| Layer 2 family | `estimation_fit` |
| Committed call | The pull list for the next maintenance round. |

## The pitfall

A sensor is calibrated by regressing its reading on the co-located reference (the known value) and inverting; regressing the reference on the sensor gives a different correction and a different drift verdict.

## The tempting shortcut

Regress the reference on the sensor reading and apply that line as the correction.

## What pins the rigorous method

The calibration protocol names the reference as the known value and the drift tolerance on the corrected scale.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
