# DA21 — Who accounts for the spending? Concentration curves must include the people who spend nothing

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Revenue-concentration analysis in games and apps ("whales"), customer-value tiering at retailers, and cost-concentration programmes at health insurers |
| Domain | Health economics / payer analytics |
| Task shape | 14 · Cuts of a distribution (the spending thresholds and population shares for the top 1%, 5%, 10% and 50% across 3 insurance types; the care-management eligibility threshold) |
| Core method | Person-level weighted concentration: sort persons by annual expenditure, cumulative weighted population share versus cumulative weighted spending share; thresholds at weighted percentiles including zero spenders; spending share of top groups |
| Analytical stump | Computing concentration among spenders only (dropping zeros) understates concentration; unweighted person counts misrepresent the population; using household instead of person records double counts. The top-5% threshold that drives eligibility moves a lot depending on these choices |
| Primary sources | AHRQ Medical Expenditure Panel Survey (MEPS) Household Component full-year consolidated file |

## 1. The real-world situation

A health plan enrols members in care management when predicted annual spending exceeds the top-5% threshold of the population. A first
analysis used MEPS but computed thresholds among people with any spending, unweighted, and reported the top 5% accounting for 35% of
spending, contradicting the widely cited figure of roughly half.

## 2. The decision (one deterministic recommendation)

**The care-management eligibility threshold (USD, rounded to the nearest $1,000) = the weighted 95th percentile of total annual
expenditure for the plan's insurance type, and the spending shares of the top 1/5/10/50% for all three types.**

Rules (analytics memo):

* Data: MEPS HC full-year consolidated file for the year in the memo; persons with positive person weight (`PERWTyyF`).
* Expenditure: `TOTEXPyy` (total health care expenditures, all sources).
* Insurance type: any private, public only, uninsured all year (from the file's insurance coverage indicator per memo).
* Concentration: within each insurance type, weighted percentiles (memo's definition) including zeros; top-x% share = Σ w·exp over persons
  above the (100 − x) percentile ÷ Σ w·exp.
* Threshold for the plan (private): weighted P95, rounded.

## 3. Why capable analysts get it wrong

* Zero spenders seem irrelevant to "who spends", yet they are part of the population that thresholds are defined over.
* Survey weights correct for oversampling of certain groups.
* Household-level files and person-level files differ; the person is the unit.
* Shares at the top are sensitive to weighting and the percentile definition.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `h<nnn>.csv` (full-year consolidated) | CSV | ~22–28k persons, 1,400+ columns | AHRQ MEPS | U.S. Gov public domain | Expenditures, weights, insurance |
| 2 | `h<nnn>doc.pdf` | PDF | — | AHRQ | Public domain | Variable documentation |
| 3 | `h<nnn>cb.pdf` | PDF | — | AHRQ | Public domain | Codebook |
| 4 | `meps_concentration_statistical_brief.pdf` | PDF | — | AHRQ Statistical Brief (cite) | Public domain | Published concentration figures |
| 5 | `analytics_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `first_analysis_spenders_only.xlsx` | XLSX | ~12 | Task author | — | Earlier figures |
| 7 | `insurance_type_rule.json` | JSON | — | Task author | — | Classification |
| 8 | `weighted_percentile_definition.json` | JSON | — | Task author | — | Definition |
| 9 | `meps_persons_tidy.parquet` | Parquet | ~25k | Derived | Public domain | Convenience |
| 10 | `meps_variance_note.pdf` | PDF | — | AHRQ | Public domain | Design (context) |

## 5. Deterministic solution path

1. Load persons with positive weights; classify insurance type.
2. Weighted percentiles including zeros; thresholds.
3. Top-group spending shares per type; validate the all-person figures against the AHRQ brief.
4. Threshold for the plan; contrast with the first analysis.

## 6. Wrong paths (method errors, not misreadings)

**A — spenders only.** Concentration understated; threshold inflated.

**B — unweighted.** Misrepresents population.

**C — household-level aggregation.** Wrong unit.

**D — mean-based tiers (e.g., 3× mean).** Not the memo's percentile rule.

## 7. Why the stump is analytical, not semantic

The population, weights and percentile rule are specified. The trap is conditioning on positive values and ignoring weights.

## 8. Draft task prompt (prose)

> Set our care-management eligibility threshold and show how concentrated spending is by insurance type, following the analytics memo on
> MEPS. Provide `concentration_cuts.csv` (type: P50, P90, P95, P99 thresholds; top 1/5/10/50% shares), `concentration_curves.png`, and a
> one-page `eligibility_threshold.pdf`.

## 9. Deliverables

* `concentration_cuts.csv`, `concentration_curves.png`, `eligibility_threshold.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 types × (4 thresholds + 4 shares) = 24; plan threshold; validation; contrast.

## 11. Golden-output checklist

* Weight filter; insurance classification; zeros included; percentile definition; shares; rounding.

## 12. Build notes (scope tuning)

* Confirm the spenders-only P95 differs from the full-population P95 by ≥ 15%.
