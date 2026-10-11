# DQ06, Whether a register statistic keeps its quality flag when the missing field may not be missing at random

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `general-statistics-data-science` / `missing-data-censoring-measurement-error` |
| Layer 2 pattern | `general-statistics-data-science/missing-data-censoring-measurement-error/3` |
| Layer 2 family | `estimation_fit` |
| Committed call | Publish with the standard flag, publish with a caution flag, or suppress, for each statistic in the release. |

## The pitfall

Imputation assumes missing at random. A tipping-point analysis shifts imputed values by stated offsets and finds the shift that breaks the quality tolerance; agreement between complete-case and imputed results is not robustness.

## The tempting shortcut

Compare complete-case and imputed figures and call the statistic robust when they agree.

## What pins the rigorous method

The quality framework names the delta grid and the tolerance the published statistic must hold.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
