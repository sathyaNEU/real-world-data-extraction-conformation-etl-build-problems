# DA22 — How different are hospitals really? Observed spread includes sampling noise

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Rating-distribution analysis on marketplaces (seller, driver or host ratings from varying numbers of reviews) and survey-based KPI comparisons across stores or agents |
| Domain | Healthcare quality / patient experience |
| Task shape | 14 · Cuts of a distribution (true between-hospital SD and the 10th/90th percentiles of true "top-box" rates for 4 measures; the measure chosen for a performance-tier programme) |
| Core method | Method-of-moments deconvolution: observed variance of hospital rates minus the average binomial sampling variance (p(1−p)/n with survey completes as n, design-adjusted per memo) gives between-hospital variance; percentiles of the true-rate distribution under a normal approximation on the logit scale (memo); signal-to-noise per measure |
| Analytical stump | The spread of observed percentages across hospitals mixes true differences with sampling noise, which is large for hospitals with few completed surveys. Tiering on raw spread exaggerates differences; some measures with wide observed spread have little true variation |
| Primary sources | CMS Care Compare — HCAHPS hospital-level survey results |

## 1. The real-world situation

A health system wants to create performance tiers on one patient-experience measure. It chose the measure with the widest observed spread
of top-box percentages across hospitals, reasoning that it discriminates best. A statistician noted that several measures have low
response counts at small hospitals, inflating their apparent spread.

## 2. The decision (one deterministic recommendation)

**The measure used for tiering: the one with the highest reliability (true variance ÷ (true + average noise variance)), and its true
10th–90th percentile range of top-box rates.**

Rules (quality memo):

* Data: HCAHPS hospital file for the reporting period in the memo; four measures (nurse communication, doctor communication, quietness,
  recommend hospital) with top-box percentages and number of completed surveys.
* Hospitals: ≥ 100 completed surveys and no footnotes suppressing the measure.
* Logit transform: y = logit(p) with the memo's continuity adjustment; sampling variance v = 1 ÷ (n_eff p (1 − p)), n_eff = completes ÷ design
  effect 1.3 (memo).
* Between-hospital variance τ² = max(0, var(y) − mean(v)).
* Reliability = τ² ÷ (τ² + mean(v)).
* True P10/P90 on the logit scale: mean(y) ± 1.2816 τ; back-transform.
* Choose the measure with the highest reliability; report observed and true ranges for all four.

## 3. Why capable analysts get it wrong

* Observed spread is the obvious discrimination measure.
* Noise variance depends on sample size and proportion; small hospitals add spread.
* On the percentage scale, variance depends on the mean; the logit stabilises it (memo).
* Reliability, not spread, determines whether tiers reflect real differences.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `HCAHPS-Hospital.csv` | CSV | ~350k (hospital × question rows) | CMS Provider Data Catalog | U.S. Gov public domain | Hospital results |
| 2 | `HCAHPS-State.csv`, `HCAHPS-National.csv` | CSV | ~3k | CMS | Public domain | Benchmarks |
| 3 | `Hospital_General_Information.csv` | CSV | ~5.4k | CMS | Public domain | Hospital attributes |
| 4 | `hcahps_footnotes.csv` | CSV | ~30 | CMS | Public domain | Footnote meanings |
| 5 | `hcahps_technical_notes.pdf` | PDF | — | CMS HCAHPS | Public domain | Measures, completes |
| 6 | `quality_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `observed_spread_analysis.xlsx` | XLSX | 4 | Task author | — | Earlier choice |
| 8 | `measure_question_ids.json` | JSON | 4 | Task author | — | Measure → question IDs |
| 9 | `deconvolution_check.json` | JSON | — | Task author | — | Toy example |
| 10 | `hospital_measure_long.parquet` | Parquet | ~16k | Derived | Public domain | Tidy data |

## 5. Deterministic solution path

1. Extract top-box percentages and completes for the four measures; filters.
2. Logit transform; sampling variances.
3. τ², reliability, true percentiles per measure.
4. Choose; contrast with observed spread ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — observed spread.** Noise-inflated measure chosen.

**B — ignoring design effect.** Noise understated.

**C — variance on percentage scale with a single p.** Mis-specified noise.

**D — including tiny hospitals.** Noise dominates.

## 7. Why the stump is analytical, not semantic

The measures, transforms and formulas are specified. The trap is confusing observed dispersion with true heterogeneity.

## 8. Draft task prompt (prose)

> Which patient-experience measure should we use for tiering? Separate true hospital differences from sampling noise as the quality memo
> describes. Provide `measure_reliability.csv` (measure: hospitals, observed SD, noise variance, τ, reliability, observed and true P10/P90),
> `observed_vs_true.png`, and a one-page `tiering_measure.pdf`.

## 9. Deliverables

* `measure_reliability.csv`, `observed_vs_true.png`, `tiering_measure.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 measures × (τ², reliability, true P10, true P90, observed P10, observed P90) = 24; choice; contrast; toy check.

## 11. Golden-output checklist

* Filters; logit; n_eff; τ²; reliability; back-transform; choice.

## 12. Build notes (scope tuning)

* Confirm the widest-observed-spread measure is not the most reliable.
