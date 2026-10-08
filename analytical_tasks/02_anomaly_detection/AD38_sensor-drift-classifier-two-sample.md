# AD38 — Sensor drift in a deployed classifier: 128 feature tests or one question?

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | ML-model monitoring for inline sensors (electronic noses, gas leak detection, quality inspection) at manufacturers; feature-drift dashboards in ML platforms |
| Domain | Industrial sensing / MLOps |
| Task shape | 17 · Periods around a change point (batches after deployment checked against the training batch; first batch where recalibration is required; go/no-go on the recalibration campaign) |
| Core method | Classifier two-sample test (domain classifier AUC with a permutation-calibrated threshold) between reference and each later batch, compared with 128 per-feature Kolmogorov–Smirnov tests with and without Bonferroni; link drift to accuracy drop of the frozen model |
| Analytical stump | Per-feature tests at 5% flag something in every batch (128 tests), and with Bonferroni they miss coordinated small shifts across many sensors. The question "has the joint distribution moved?" is answered by one multivariate test; the business question "does it hurt accuracy?" needs the frozen model's performance on labelled checks |
| Primary sources | UCI "Gas Sensor Array Drift Dataset" (Vergara et al., 2012; 36 months, 10 batches, 16 sensors × 8 features) |

## 1. The real-world situation

A gas-detection product classifies six gases from an array of 16 metal-oxide sensors. The model was trained on batch 1. Field
recalibration is expensive, so the product team wants to trigger it only when the sensors have drifted enough to hurt classification.
The monitoring dashboard runs per-feature KS tests and has shown red cells since the second batch.

## 2. The decision (one deterministic recommendation)

**The first batch at which recalibration is required, and whether to launch the recalibration campaign now (at batch 10) for the installed
base.**

Rules (monitoring memo):

* Reference: batch 1 (random 70% for training a frozen model; 30% held out as reference sample).
* Frozen model: standardised features (fit on training part), multinomial logistic regression with the memo's regularisation; accuracy on
  each later batch.
* Domain-classifier test per batch b: label reference = 0, batch b = 1; 5-fold cross-validated AUC of a logistic regression; significance by
  200 label permutations with seed 7 (permutation p < 0.01).
* Per-feature KS: 128 tests per batch at α = 0.05 (unadjusted) and α = 0.05/128 (Bonferroni).
* Recalibration required at batch b if the domain test is significant **and** frozen-model accuracy on batch b is ≥ 10 percentage points
  below its held-out accuracy on batch 1.
* Campaign now if recalibration is required at batch 10.

## 3. Why capable analysts get it wrong

* Feature dashboards are the default monitoring view; many tests guarantee red cells.
* Correction for multiplicity makes univariate tests insensitive to broad small shifts.
* Drift is not harm; some drift leaves the decision boundary unaffected.
* Using labelled batches to measure accuracy requires the frozen model, not one retrained per batch.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–10 | `batch1.dat` … `batch10.dat` | LibSVM text | 445–3,600 each (13,910 total) | UCI ML Repository (id 224) | CC BY 4.0 | Measurements and labels |
| 11 | `batch_months.json` | JSON | 10 | From dataset description | CC BY 4.0 | Batch time spans |
| 12 | `gas_sensor_drift_description.html` | HTML | — | UCI | CC BY 4.0 | Feature definitions |
| 13 | `monitoring_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 14 | `dashboard_ks_snapshot.xlsx` | XLSX | 128 × 9 | Task author | — | Current dashboard |
| 15 | `lopez_paz_oquab_c2st_citation.pdf` | PDF | — | Cite | Cite | Classifier two-sample tests |
| 16 | `features_long.parquet` | Parquet | ~1.8M | Derived | CC BY 4.0 | Tidy features |

## 5. Deterministic solution path

1. Parse LibSVM files; split batch 1 per seed in the memo.
2. Train the frozen model; accuracy by batch.
3. Domain-classifier AUC and permutation p per batch; KS counts with and without correction.
4. Apply the rule; first required batch; campaign decision.

## 6. Wrong paths (method errors, not misreadings)

**A — unadjusted KS dashboard.** Recalibrate immediately.

**B — Bonferroni KS only.** Misses coordinated drift.

**C — drift without accuracy check.** Recalibrates when not needed.

**D — retraining per batch to measure accuracy.** Hides the frozen model's degradation.

## 7. Why the stump is analytical, not semantic

Splits, tests and rule are specified. The traps are multiple testing, univariate versus joint drift, and drift versus harm.

## 8. Draft task prompt (prose)

> When did our gas classifier first need recalibration, and should we run the campaign now? Follow the monitoring memo on the ten drift
> batches. Provide `batch_monitoring.csv` (batch: AUC, permutation p, KS rejections raw/Bonferroni, frozen accuracy, rule), `drift_vs_accuracy.png`,
> and a one-page `recalibration_decision.pdf`.

## 9. Deliverables

* `batch_monitoring.csv`, `drift_vs_accuracy.png`, `recalibration_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 9 later batches × (AUC, accuracy, rule) = 27; KS counts; first required batch; campaign call.

## 11. Golden-output checklist

* Split and seed; frozen model; permutation test; KS counts; rule application.

## 12. Build notes (scope tuning)

* Publish the seed and regularisation; confirm at least one batch with significant drift but small accuracy loss.
