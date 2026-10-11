# DQ25, Which low-level channels trip the drift alert when readings sit below the detection limit

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `physical-environmental-sciences` / `sensor-calibration-measurement` |
| Layer 2 pattern | `own:detection-limit-censoring` |
| Layer 2 family | `estimation_fit` |
| Committed call | The channels escalated to the laboratory this quarter. |

## The pitfall

Readings below the limit of detection are censored. Substituting half the limit biases the channel mean and its drift; a censored-data estimator gives the level the alert compares.

## The tempting shortcut

Substitute LOD/2 for censored readings and compute the mean.

## What pins the rigorous method

The laboratory flags censored readings and the alert standard defines the level on the censored-data estimator.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
