# DQ04, Whether the network-total shortfall alert fires when the missing reads are multiply imputed

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `general-statistics-data-science` / `missing-data-censoring-measurement-error` |
| Layer 2 pattern | `general-statistics-data-science/missing-data-censoring-measurement-error/1` |
| Layer 2 family | `estimation_fit` |
| Committed call | Which reporting zones raise a shortfall alert for the closing period. |

## The pitfall

Multiply imputed totals are pooled with Rubin's rules, within and between imputation variance added. Averaging the imputations into one file and testing once understates the variance and fires the alert too often.

## The tempting shortcut

Average the imputed reads into one dataset and test the total against the tolerance once.

## What pins the rigorous method

The pipeline ships every imputation, and the alert standard defines the test on the pooled estimate and its variance.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
