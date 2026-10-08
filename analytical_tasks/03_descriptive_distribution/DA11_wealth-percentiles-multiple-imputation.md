# DA11 — Wealth percentiles from a survey with five imputations: one implicate is not the data, five are not five times the sample

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Analytics on datasets with model-imputed fields (imputed income or demographics in ad platforms, imputed revenue in CRM enrichment) where uncertainty from imputation must be carried into reported figures |
| Domain | Household finance |
| Task shape | 14 · Cuts of a distribution (P25, P50, P75, P90 of net worth for 4 age groups with standard errors; the target segment for a retirement-product launch) |
| Core method | Survey of Consumer Finances multiple imputation: compute each statistic within each of the 5 implicates with the main weight; point estimate = average across implicates; variance = sampling variance from replicate weights (implicate 1, per SCF guidance) + (1 + 1/5) × between-implicate variance (Rubin's rules) |
| Analytical stump | Using only the first implicate understates uncertainty; stacking all five implicates as if they were 5× the respondents shrinks standard errors by about √5; ignoring the 999 replicate weights uses simple-random-sample variance on a complex list-plus-area design. The segment decision depends on whether two groups' medians are distinguishable |
| Primary sources | Federal Reserve Board Survey of Consumer Finances (SCF) public data — summary extract and full public data set with replicate weights |

## 1. The real-world situation

A retirement-products team will launch in the age group whose median net worth is closest to the product's $250,000 sweet spot, but only
if that median is statistically distinguishable from its neighbouring age groups' medians. The analyst used the SCF summary extract,
stacked all rows (five per family) as independent observations and found tight intervals.

## 2. The decision (one deterministic recommendation)

**The target age group, its median net worth with a correctly computed standard error, and whether it is distinguishable from adjacent
groups (|difference| > 1.96 × combined SE).**

Rules (research memo):

* Data: SCF 2022 summary extract (five implicates per family, variable `networth`, weight `wgt`), replicate weights file (999 replicates).
* Age groups of the reference person: < 35, 35–44, 45–54, 55–64 (65+ excluded for this product).
* Point estimate: weighted percentile (memo's definition) within each implicate; average across implicates.
* Sampling variance: from replicate weights, computed on implicate 1, per the SCF documentation's recommended approach (replicate variance
  formula in the memo, including the replicate multiplicity adjustment).
* Imputation variance: B = variance of the five implicate estimates; total variance = sampling variance + (6/5) × B.
* Differences between adjacent groups: compute the difference within each implicate and replicate, then apply the same rules.
* Target = group with median closest to $250,000; launch if its differences from both neighbours are significant.

## 3. Why capable analysts get it wrong

* Five rows per family look like data duplication and invite stacking or de-duplication.
* Imputation adds real uncertainty, especially at the top of the wealth distribution.
* Replicate weights are needed for the SCF's dual-frame design.
* Differences must be computed within implicates/replicates, not by combining separate SEs naïvely.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `rscfp2022.csv` (summary extract) | CSV | ~22.9k (5 × ~4.6k families) | Federal Reserve Board SCF | U.S. Gov public domain | Net worth, demographics, weights |
| 2 | `p22i6.csv` (full public data) | CSV | ~22.9k | Federal Reserve Board | Public domain | Full variables (context) |
| 3 | `p22_rw1.csv` (replicate weights) | CSV | ~4.6k × 999 | Federal Reserve Board | Public domain | Replicate weights |
| 4 | `scf2022_codebook.html` | HTML | — | Federal Reserve Board | Public domain | Variable definitions |
| 5 | `scf_variance_estimation_guide.pdf` | PDF | — | Federal Reserve Board | Public domain | Replicate and imputation variance |
| 6 | `research_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `analyst_stacked_results.xlsx` | XLSX | 4 | Task author | — | Naive results |
| 8 | `rubin_rules_citation.pdf` | PDF | — | Rubin (1987) (cite) | Cite | Combining rules |
| 9 | `weighted_percentile_definition.json` | JSON | — | Task author | — | Percentile definition |
| 10 | `bulletin_published_medians_2022.xlsx` | XLSX | ~20 | Federal Reserve Bulletin tables | Public domain | Validation of point estimates |

## 5. Deterministic solution path

1. Load extract; assign age groups; compute weighted percentiles per implicate.
2. Average across implicates; validate medians against the Bulletin.
3. Replicate variance on implicate 1; between-implicate variance; total SE.
4. Adjacent differences; target and launch decision.

## 6. Wrong paths (method errors, not misreadings)

**A — stacked implicates as independent rows.** SEs too small.

**B — implicate 1 only.** Imputation variance ignored.

**C — SRS formulas.** Design ignored.

**D — combining group SEs as if independent.** Wrong difference tests.

## 7. Why the stump is analytical, not semantic

The estimator, variance rules and decision are specified. The trap is carrying imputation and design uncertainty correctly.

## 8. Draft task prompt (prose)

> Which age group should the retirement product target, and is its median net worth clearly different from its neighbours'? Use the SCF
> 2022 data with the implicate and replicate-weight rules in the research memo. Provide `networth_percentiles.csv` (group: P25, P50, P75, P90,
> SEs, variance components), `median_intervals.png`, and a one-page `target_segment.pdf`.

## 9. Deliverables

* `networth_percentiles.csv`, `median_intervals.png`, `target_segment.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 groups × 4 percentiles = 16; 4 median SEs with components; 3 adjacent differences; target; launch call; validation.

## 11. Golden-output checklist

* Implicate averaging; replicate variance; Rubin combination; difference method; decision rule.

## 12. Build notes (scope tuning)

* Confirm the stacked analysis declares a significant difference that the correct analysis does not, for the chosen target's neighbour.
