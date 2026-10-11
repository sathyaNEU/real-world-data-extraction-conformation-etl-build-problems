# DQ10, Whether a translated questionnaire passes the release gate on reliability

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `psychology-behavioral-science` / `psychometric-measurement-scale-validation` |
| Layer 2 pattern | `psychology-behavioral-science/psychometric-measurement-scale-validation/1` |
| Layer 2 family | `field_method` |
| Committed call | Release, hold or rework each language version in the wave. |

## The pitfall

Alpha assumes equal loadings and says nothing about dimensionality. The gate is model-based reliability, omega from the fitted congeneric structure.

## The tempting shortcut

Report alpha above the cutoff and pass the version.

## What pins the rigorous method

The release standard names omega under a congeneric model as the gate, with its threshold.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
