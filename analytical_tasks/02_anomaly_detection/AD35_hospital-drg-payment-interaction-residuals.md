# AD35 — Payment outliers by hospital and DRG: a high-cost hospital is not an anomaly in every DRG

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Payer contract analytics and price-transparency vendors; cloud-cost anomaly detection across account × service where some accounts are uniformly expensive |
| Domain | Healthcare finance |
| Task shape | 01 · Ranked list under a cap (25 hospital–DRG cells for payment review) |
| Core method | Log-additive two-way model of average payments: log(pay) = hospital effect + DRG effect + residual, fitted by weighted least squares (weights = discharges); anomalies are standardized residuals (interaction), not within-DRG z-scores of raw payments |
| Analytical stump | Within-DRG z-scores flag hospitals that are expensive everywhere (teaching status, wage index, outlier payments) and DRGs with wide spreads. The review target is a hospital paid unusually *for one DRG relative to its own overall level* — a cell-specific deviation that only the interaction residual isolates |
| Primary sources | CMS "Medicare Inpatient Hospitals — by Provider and Service" public use file |

## 1. The real-world situation

A Medicare Administrative Contractor reviews **25** hospital–DRG combinations a year for payment anomalies (coding, outlier claims,
transfers). Its current list ranks combinations by how far the hospital's average Medicare payment sits above the DRG's national mean, in
standard deviations. Nearly every flagged cell belonged to six academic medical centres whose payments are high across the board.

## 2. The decision (one deterministic recommendation)

**The 25 hospital–DRG cells selected for review, ranked by standardized interaction residual, and the 26th.**

Rules (review memo):

* Data: the 2021 inpatient provider-and-service file; cells with ≥ 20 discharges; measure = `Avg_Mdcr_Pymt_Amt`.
* Scope: hospitals with ≥ 15 eligible DRGs; DRGs with ≥ 50 eligible hospitals.
* Model: log(payment) = α_h + β_d + ε, weighted by discharges; solve by alternating weighted means until the change in all effects < 1e-8.
* Residual variance: per DRG, the weighted variance of residuals; standardized residual r = ε ÷ √(var_d ÷ discharges × mean discharges of
  DRG) per the memo's formula.
* Rank positive r (overpayment direction); top 25; report #26.

## 3. Why capable analysts get it wrong

* Within-group z-scores are the standard outlier tool and ignore a unit's overall level.
* Payment levels differ by wage index, teaching and disproportionate-share adjustments — multiplicative effects across all DRGs.
* Multiplicative effects need logs; additive models on dollars misattribute variation to expensive DRGs.
* Small cells are noisy; weights and the standardization address it.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `MUP_INP_RY23_P03_V10_DY21_PrvSvc.csv` | CSV | ~150k | CMS data.cms.gov | U.S. Gov public domain | Hospital × DRG cells |
| 2 | `MUP_INP_RY23_P03_V10_DY21_Prv.csv` | CSV | ~3k | CMS | Public domain | Hospital summary |
| 3 | `inpatient_methodology.pdf` | PDF | — | CMS | Public domain | Definitions, suppression |
| 4 | `ipps_impact_file_fy2021.xlsx` | XLSX | ~3.2k | CMS IPPS final rule impact file | Public domain | Wage index, teaching status (context) |
| 5 | `review_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `current_z_score_list.xlsx` | XLSX | 25 | Task author | — | Current list |
| 7 | `msdrg_v38_definitions.csv` | CSV | ~770 | CMS | Public domain | DRG titles, weights |
| 8 | `model_reference_values.json` | JSON | ~10 | Task author | — | Check values for convergence |
| 9 | `hospital_ccn_crosswalk.csv` | CSV | ~3.2k | Derived | Public domain | Identifiers |
| 10 | `two_way_fit_citation.pdf` | PDF | — | Cite | Cite | Median polish / two-way fits |

## 5. Deterministic solution path

1. Filter cells; apply hospital and DRG scope rules iteratively until stable.
2. Fit the weighted two-way log model.
3. Residual variances by DRG; standardized residuals.
4. Rank; top 25 + #26; compare with the z-score list.

## 6. Wrong paths (method errors, not misreadings)

**A — within-DRG z-scores of raw payments.** Expensive hospitals dominate.

**B — additive model on dollars.** High-weight DRGs dominate.

**C — unweighted fit.** Small cells move effects.

**D — scope rules applied once.** Cells left without enough partners.

## 7. Why the stump is analytical, not semantic

The model, weights and ranking are specified. The trap is separating main effects from interactions.

## 8. Draft task prompt (prose)

> Give me the 25 hospital–DRG cells for payment review using the two-way residual method in the review memo. Provide `cell_residuals.csv`
> (hospital, DRG, discharges, payment, hospital effect, DRG effect, residual, r, rank), `effects_heatmap.png` (residuals for the top hospitals
> × DRGs), and a one-page `review_cells.pdf` comparing with the z-score list.

## 9. Deliverables

* `cell_residuals.csv`, `effects_heatmap.png`, `review_cells.pdf`.

## 10. Where 25+ rubric criteria come from

* 25 cells + #26; effects for 5 hospitals and 5 DRGs; convergence; overlap with the z-score list.

## 11. Golden-output checklist

* Iterative scoping; log scale; weights; convergence; standardization; ranking.

## 12. Build notes (scope tuning)

* Publish reference effects for a test subset.
* Confirm ≤ 5 of the z-score list's cells survive.
