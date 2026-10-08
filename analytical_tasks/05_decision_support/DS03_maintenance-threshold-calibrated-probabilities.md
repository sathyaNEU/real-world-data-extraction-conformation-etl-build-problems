# DS03 — Truck air-system maintenance: the cost-optimal threshold only works on calibrated probabilities

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Predictive-maintenance and risk teams turning model scores into actions with asymmetric costs (fleet operators, manufacturers, insurers) |
| Domain | Fleet maintenance / heavy vehicles |
| Task shape | 04 · Setting one dial (the score threshold for sending a truck to workshop inspection, and the expected cost per 1,000 trucks) |
| Core method | Train a classifier on the provided training set; calibrate probabilities (isotonic or Platt per memo) on a held-out calibration split; apply the Bayes-optimal threshold p* = C_FP ÷ (C_FP + C_FN) = 10 ÷ 510 on calibrated probabilities; total cost on the provided test set; compare with thresholds chosen on uncalibrated scores |
| Analytical stump | Class-weighted or resampled training distorts predicted probabilities; applying the theoretical threshold to uncalibrated scores (or using 0.5) gives the wrong operating point and much higher cost. The cost-optimal decision requires calibrated probabilities that reflect the true base rate |
| Primary sources | UCI "APS Failure at Scania Trucks" dataset (IDA 2016 challenge) |

## 1. The real-world situation

A truck manufacturer's service organisation flags trucks for inspection of the air pressure system (APS). A missed APS failure costs 500 units; an
unnecessary inspection costs 10. The data-science team trained a balanced classifier and flagged trucks with score > 0.5; another analyst
applied the theoretical threshold 10/510 to the same scores and flagged half the fleet.

## 2. The decision (one deterministic recommendation)

**The inspection threshold on calibrated probability (and the corresponding score cut), the expected cost per 1,000 trucks on the test set, and
whether it beats the current rule (inspect all trucks with ≥ 2 APS warnings — modelled per memo).**

Rules (service memo):

* Data: APS training set (60,000) and test set (16,000) as provided; missing values imputed by training medians; features as provided.
* Model: gradient-boosted trees with class weights per memo (fixed hyperparameters and seed).
* Calibration: hold out 20% of training (stratified, seed 7) for isotonic calibration.
* Decision: inspect if calibrated p ≥ 10 ÷ 510.
* Cost on test = 10 × FP + 500 × FN (the dataset's official cost metric); reported per 1,000 trucks.
* Report costs for: threshold 0.5 on raw scores; p* on raw scores; p* on calibrated probabilities; current rule.

## 3. Why capable analysts get it wrong

* 0.5 is the default threshold.
* Class weighting shifts scores upward for the minority class; raw scores are not probabilities.
* The Bayes threshold assumes calibrated probabilities at the deployment base rate.
* Calibration needs data not used for training.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `aps_failure_training_set.csv` | CSV | 60,000 | UCI ML Repository (id 421) | CC BY 4.0 | Training data |
| 2 | `aps_failure_test_set.csv` | CSV | 16,000 | UCI | CC BY 4.0 | Test data |
| 3 | `aps_failure_description.txt` | Text | — | UCI | CC BY 4.0 | Cost metric and description |
| 4 | `service_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `model_spec.json` | JSON | — | Task author | — | Hyperparameters, seeds |
| 6 | `current_rule_definition.json` | JSON | — | Task author | — | Current rule proxy |
| 7 | `team_threshold_results.xlsx` | XLSX | 2 | Task author | — | Earlier choices |
| 8 | `calibration_reference.pdf` | PDF | — | Cite (Niculescu-Mizil & Caruana 2005) | Cite | Calibration |

## 5. Deterministic solution path

1. Impute; split training into fit and calibration parts; train the model.
2. Calibrate; compute test probabilities.
3. Apply thresholds; costs per 1,000 trucks; reliability diagram.
4. Decision versus the current rule.

## 6. Wrong paths (method errors, not misreadings)

**A — threshold 0.5.** Too few inspections; many missed failures.

**B — p* on uncalibrated scores.** Too many inspections.

**C — calibrating on the test set.** Leakage.

**D — optimising threshold on the test set.** Optimistic cost.

## 7. Why the stump is analytical, not semantic

Costs, splits and model are specified. The trap is applying decision theory to scores that are not probabilities.

## 8. Draft task prompt (prose)

> What inspection threshold should our APS model use, and what will it cost? Calibrate the model and apply the cost-optimal rule as the service
> memo specifies, comparing with the alternatives. Provide `threshold_costs.csv` (rule: threshold, FP, FN, cost per 1,000), `reliability_diagram.png`,
> and a one-page `inspection_policy.pdf`.

## 9. Deliverables

* `threshold_costs.csv`, `reliability_diagram.png`, `inspection_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 rules × (threshold, FP, FN, cost) = 16; calibration metrics; decision; reliability bins (10).

## 11. Golden-output checklist

* Imputation from training; splits; calibration; threshold; cost convention; decision.

## 12. Build notes (scope tuning)

* Confirm the calibrated rule has the lowest cost and that raw-score rules differ by ≥ 20%.
