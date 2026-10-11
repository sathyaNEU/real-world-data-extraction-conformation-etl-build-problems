# DQ11, Whether a new survey mode's data can be pooled into the tracker

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `psychology-behavioral-science` / `psychometric-measurement-scale-validation` |
| Layer 2 pattern | `psychology-behavioral-science/psychometric-measurement-scale-validation/2` |
| Layer 2 family | `field_method` |
| Committed call | Pool, pool with a mode adjustment flag, or keep the mode separate, for each tracked index. |

## The pitfall

Five-point items are ordinal. Invariance across modes is tested with polychoric correlations and a categorical estimator; Pearson-based ML fit attenuates loadings and misjudges invariance.

## The tempting shortcut

Run ML CFA on Pearson correlations of the items and compare fit by mode.

## What pins the rigorous method

Items are filed as ordinal, and the tracker's quality standard names the categorical estimator and the invariance criterion.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
