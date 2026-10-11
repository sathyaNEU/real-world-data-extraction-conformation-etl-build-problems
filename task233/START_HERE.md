# task233: start here

| | |
|---|---|
| Task | task233 |
| Objective (Axis 1) | Data Quality Monitoring & Alerting |
| Block | task228 to task252 |
| Lane owner | developer 3 (current owner and status: the root `START_HERE.md` on main) |
| Seed | DQ06, `analytical_tasks/08_data_quality_monitoring/DQ06_whether-a-register-statistic-keeps-its-quality-flag-whe.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task233`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task233-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** Whether a register statistic keeps its quality flag when the missing field may not be missing at random
- **objective:** Data Quality Monitoring & Alerting
- **domain:** general-statistics-data-science · missing-data-censoring-measurement-error
- **committed_call:** Publish with the standard flag, publish with a caution flag, or suppress, for each statistic in the release.
- **driving_force:** Imputation assumes missing at random. A tipping-point analysis shifts imputed values by stated offsets and finds the shift that breaks the quality tolerance; agreement between complete-case and imputed results is not robustness.
- **technique:** general-statistics-data-science/missing-data-censoring-measurement-error/3

## Seed note

## DQ06, Whether a register statistic keeps its quality flag when the missing field may not be missing at random

| Field | Value |
|---|---|
| Objective | Data Quality Monitoring & Alerting |
| Client domain / task type | `general-statistics-data-science` / `missing-data-censoring-measurement-error` |
| Layer 2 pattern | `general-statistics-data-science/missing-data-censoring-measurement-error/3` |
| Layer 2 family | `estimation_fit` |
| Committed call | Publish with the standard flag, publish with a caution flag, or suppress, for each statistic in the release. |

### The pitfall

Imputation assumes missing at random. A tipping-point analysis shifts imputed values by stated offsets and finds the shift that breaks the quality tolerance; agreement between complete-case and imputed results is not robustness.

### The tempting shortcut

Compare complete-case and imputed figures and call the statistic robust when they agree.

### What pins the rigorous method

The quality framework names the delta grid and the tolerance the published statistic must hold.

### Making it a monitoring task

The object under analysis is the health of the data or of the pipeline that delivers it, and the committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive or Forecasting without changing a word, the tag fails.

### Layer 1

Draw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` (the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register and alert routing beside what was published, every piece of mess something the real system would produce.
