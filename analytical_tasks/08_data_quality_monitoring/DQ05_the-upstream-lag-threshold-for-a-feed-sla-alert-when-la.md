# DQ05, The upstream-lag threshold for a feed SLA alert, when lag is itself measured with error

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `general-statistics-data-science` / `missing-data-censoring-measurement-error` |
| Layer 2 pattern | `general-statistics-data-science/missing-data-censoring-measurement-error/2` |
| Layer 2 family | `estimation_fit` |
| Committed call | The lag threshold at which the feed SLA alert pages, per feed. |

## The pitfall

Random error in a covariate attenuates its slope toward zero. Setting an alert on upstream lag from a naive regression of downstream error on measured lag understates how much lag matters and puts the threshold too high.

## The tempting shortcut

Treat the logged lag as exact and read the threshold off the naive fit.

## What pins the rigorous method

Replicate lag measurements give the error variance, and the SLA standard sets the threshold at a stated downstream error rate.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
