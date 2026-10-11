# task232: start here

| | |
|---|---|
| Task | task232 |
| Objective (Axis 1) | Data Quality Monitoring & Alerting |
| Block | task228 to task252 |
| Lane owner | developer 3 (current owner and status: the root `START_HERE.md` on main) |
| Seed | DQ05, `analytical_tasks/08_data_quality_monitoring/DQ05_the-upstream-lag-threshold-for-a-feed-sla-alert-when-la.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task232`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task232-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** The upstream-lag threshold for a feed SLA alert, when lag is itself measured with error
- **objective:** Data Quality Monitoring & Alerting
- **domain:** general-statistics-data-science · missing-data-censoring-measurement-error
- **committed_call:** The lag threshold at which the feed SLA alert pages, per feed.
- **driving_force:** Random error in a covariate attenuates its slope toward zero. Setting an alert on upstream lag from a naive regression of downstream error on measured lag understates how much lag matters and puts the threshold too high.
- **technique:** general-statistics-data-science/missing-data-censoring-measurement-error/2

## Seed note

## DQ05, The upstream-lag threshold for a feed SLA alert, when lag is itself measured with error

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `general-statistics-data-science` / `missing-data-censoring-measurement-error` |
| Layer 2 pattern | `general-statistics-data-science/missing-data-censoring-measurement-error/2` |
| Layer 2 family | `estimation_fit` |
| Committed call | The lag threshold at which the feed SLA alert pages, per feed. |

### The pitfall

Random error in a covariate attenuates its slope toward zero. Setting an alert on upstream lag from a naive regression of downstream error on measured lag understates how much lag matters and puts the threshold too high.

### The tempting shortcut

Treat the logged lag as exact and read the threshold off the naive fit.

### What pins the rigorous method

Replicate lag measurements give the error variance, and the SLA standard sets the threshold at a stated downstream error rate.

### Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

### Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
