# DQ17, Which coding categories trip the reinterview quality alert

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `survey-research-official-statistics` / `census-register-administrative-data-quality` |
| Layer 2 pattern | `survey-research-official-statistics/census-register-administrative-data-quality/2` |
| Layer 2 family | `estimand_identification` |
| Committed call | The categories sent back to coding review. |

## The pitfall

Net difference rate measures bias in a category's total; gross difference rate measures how many units are misclassified. Offsetting errors make net small while gross is large.

## The tempting shortcut

Report the net change in category totals as the misclassification rate.

## What pins the rigorous method

The quality standard defines the alert on the gross rate, or on the net rate, and says which.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
