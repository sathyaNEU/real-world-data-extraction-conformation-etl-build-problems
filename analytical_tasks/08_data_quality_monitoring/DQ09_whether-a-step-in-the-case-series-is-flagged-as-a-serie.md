# DQ09, Whether a step in the case series is flagged as a series break caused by testing volume

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `epidemiology-public-health` / `disease-surveillance-outbreak-anomaly-detection` |
| Layer 2 pattern | `epidemiology-public-health/disease-surveillance-outbreak-anomaly-detection/3` |
| Layer 2 family | `estimand_identification` |
| Committed call | Which series carry a break flag in the next publication. |

## The pitfall

Counts rise when testing rises, for example when a new laboratory joins the network. A series break is diagnosed on tests performed and positivity, not on raw counts.

## The tempting shortcut

Treat the step in confirmed cases as real and publish it unflagged.

## What pins the rigorous method

The stream carries tests performed, and the publication standard defines a series break on testing effort.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
