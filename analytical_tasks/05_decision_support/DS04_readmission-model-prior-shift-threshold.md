# DS04 — Deploying a readmission model to a new hospital system: the base rate moved, so the threshold must move

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Launching a trained model in a new market, region or customer segment whose outcome prevalence differs (fraud rates, churn, conversion) |
| Domain | Healthcare analytics |
| Task shape | 04 · Setting one dial (the risk threshold for enrolling patients in a transitional-care programme at the new system, given its capacity) |
| Core method | Train on source hospitals; estimate the target system's prevalence without labels using EM prior-shift adjustment (Saerens et al.) on target predictions; adjust posterior probabilities by the prior ratio; set the threshold that fills capacity on adjusted probabilities and compute expected readmissions captured; validate with the target's later labels |
| Analytical stump | Reusing the source threshold (or source-calibrated probabilities) in a population with a different readmission rate misstates risk and fills capacity with the wrong patients or leaves it unused. Label shift must be estimated and corrected before choosing the threshold |
| Primary sources | UCI "Diabetes 130-US hospitals for years 1999–2008" dataset |

## 1. The real-world situation

A health-analytics vendor's readmission model was built on a group of hospitals. A new client system wants to enrol the top-risk diabetic
patients into transitional care, with capacity for 15% of discharges. The vendor proposes reusing the source threshold. The client's readmission
rate is known to differ.

## 2. The decision (one deterministic recommendation)

**The threshold on prior-adjusted probabilities that enrols 15% of the target system's discharges, and the expected number of 30-day
readmissions captured per 1,000 discharges (validated against target labels).**

Rules (analytics memo):

* Source/target split: encounters grouped by `admission_source_id` × payer per memo to emulate two systems (source and target sets in
  `system_split.json`), first encounter per patient only.
* Outcome: readmitted < 30 days.
* Model: logistic regression with the memo's features, trained and Platt-calibrated on source.
* Prior shift: EM algorithm on target predictions (no labels) to estimate target prevalence π_t; adjusted p' = (π_t/π_s · p) ÷ (π_t/π_s · p + (1−π_t)/(1−π_s) · (1 − p)).
* Threshold: 85th percentile of adjusted p' on target (enrol top 15%).
* Captured readmissions = target positives among enrolled (labels used only for validation).
* Contrast: source threshold (85th percentile of source probabilities) applied to target.

## 3. Why capable analysts get it wrong

* Thresholds are often treated as model properties.
* Prevalence differences change posteriors even if the class-conditional feature distributions are similar.
* Unlabelled target data can estimate the new prior.
* Capacity-based thresholds depend on the target's own score distribution.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `diabetic_data.csv` | CSV | 101,766 encounters | UCI ML Repository (id 296) | CC BY 4.0 | Encounters, features, readmission |
| 2 | `IDs_mapping.csv` | CSV | ~70 | UCI | CC BY 4.0 | Admission source/type codes |
| 3 | `strack_2014_citation.pdf` | PDF | — | Strack et al., BioMed Res Int 2014 (cite) | Cite | Dataset description |
| 4 | `system_split.json` | JSON | — | Task author | — | Source/target definition |
| 5 | `feature_spec.json` | JSON | — | Task author | — | Features |
| 6 | `analytics_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `vendor_threshold_proposal.xlsx` | XLSX | — | Task author | — | Source threshold |
| 8 | `saerens_2002_citation.pdf` | PDF | — | Cite | Cite | EM prior adjustment |

## 5. Deterministic solution path

1. Split systems; first encounters; train and calibrate on source.
2. Predict on target; EM estimate of π_t; adjust probabilities.
3. Threshold for 15%; captured readmissions; validation.
4. Contrast with the source-threshold approach.

## 6. Wrong paths (method errors, not misreadings)

**A — source threshold reused.** Wrong enrolment volume and mix.

**B — no prior adjustment but recalibrating on target labels.** Not available at launch (memo).

**C — multiple encounters per patient.** Leakage across splits.

**D — prevalence estimated as mean predicted probability.** Biased under shift.

## 7. Why the stump is analytical, not semantic

The split, model and adjustment are specified. The trap is label shift in deployment decisions.

## 8. Draft task prompt (prose)

> What threshold should the readmission programme use at the new client? Adjust the model for the client's base rate as the analytics memo specifies
> and set the threshold for 15% capacity. Provide `threshold_analysis.csv` (approach: threshold, enrolled share, captured per 1,000), `prior_shift.png`,
> and a one-page `deployment_threshold.pdf`.

## 9. Deliverables

* `threshold_analysis.csv`, `prior_shift.png`, `deployment_threshold.pdf`.

## 10. Where 25+ rubric criteria come from

* π_s, π_t (EM and true); thresholds; enrolled shares; captured counts; calibration bins; contrast.

## 11. Golden-output checklist

* First-encounter filter; split; calibration; EM; adjustment; capacity threshold; validation.

## 12. Build notes (scope tuning)

* Choose the split so target prevalence differs by ≥ 30% relative; confirm the source threshold enrols < 10% or > 20% of target discharges.
