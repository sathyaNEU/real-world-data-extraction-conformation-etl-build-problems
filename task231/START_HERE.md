# task231: start here

| | |
|---|---|
| Task | task231 |
| Objective (Axis 1) | Data Quality Monitoring & Alerting |
| Block | task228 to task252 |
| Lane owner | developer 3 (current owner and status: the root `START_HERE.md` on main) |
| Seed | DQ04, `analytical_tasks/08_data_quality_monitoring/DQ04_whether-the-network-total-shortfall-alert-fires-when-th.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task231`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task231-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** Whether the network-total shortfall alert fires when the missing reads are multiply imputed
- **objective:** Data Quality Monitoring & Alerting
- **domain:** general-statistics-data-science · missing-data-censoring-measurement-error
- **committed_call:** Which reporting zones raise a shortfall alert for the closing period.
- **driving_force:** Multiply imputed totals are pooled with Rubin's rules, within and between imputation variance added. Averaging the imputations into one file and testing once understates the variance and fires the alert too often.
- **technique:** general-statistics-data-science/missing-data-censoring-measurement-error/1

## Seed note

## DQ04, Whether the network-total shortfall alert fires when the missing reads are multiply imputed

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `general-statistics-data-science` / `missing-data-censoring-measurement-error` |
| Layer 2 pattern | `general-statistics-data-science/missing-data-censoring-measurement-error/1` |
| Layer 2 family | `estimation_fit` |
| Committed call | Which reporting zones raise a shortfall alert for the closing period. |

### The pitfall

Multiply imputed totals are pooled with Rubin's rules, within and between imputation variance added. Averaging the imputations into one file and testing once understates the variance and fires the alert too often.

### The tempting shortcut

Average the imputed reads into one dataset and test the total against the tolerance once.

### What pins the rigorous method

The pipeline ships every imputation, and the alert standard defines the test on the pooled estimate and its variance.

### Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

### Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
