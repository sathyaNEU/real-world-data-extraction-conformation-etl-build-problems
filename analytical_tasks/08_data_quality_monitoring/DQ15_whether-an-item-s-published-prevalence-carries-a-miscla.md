# DQ15, Whether an item's published prevalence carries a misclassification flag

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `survey-research-official-statistics` / `nonresponse-calibration-measurement-error-adjustment` |
| Layer 2 pattern | `survey-research-official-statistics/nonresponse-calibration-measurement-error-adjustment/3` |
| Layer 2 family | `estimation_fit` |
| Committed call | Which items are flagged in the next release. |

## The pitfall

With sensitivity and specificity from a record check, the corrected proportion is (p + Sp - 1) / (Se + Sp - 1). Ignoring false positives, or dividing by sensitivity alone, badly biases a rare trait.

## The tempting shortcut

Report the observed proportion, or divide it by sensitivity alone.

## What pins the rigorous method

The record-check study gives both error rates, and the quality standard sets the tolerance between published and corrected figures.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
