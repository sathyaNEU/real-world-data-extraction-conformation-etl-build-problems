# DQ12, Which items leave a dashboard index after the structure check

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `psychology-behavioral-science` / `psychometric-measurement-scale-validation` |
| Layer 2 pattern | `psychology-behavioral-science/psychometric-measurement-scale-validation/3` |
| Layer 2 family | `field_method` |
| Committed call | The list of items that stay in the index for the next cycle. |

## The pitfall

The eigenvalue-over-one rule keeps too many factors, which changes which items cross-load and which get dropped. Parallel analysis sets the factor count before any item decision.

## The tempting shortcut

Keep every factor with an eigenvalue above one and drop cross-loaders from that solution.

## What pins the rigorous method

The production QA standard names parallel analysis and the item-retention rule.

## Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

## Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
