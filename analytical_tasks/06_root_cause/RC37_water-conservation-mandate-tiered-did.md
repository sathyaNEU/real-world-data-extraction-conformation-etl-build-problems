# RC37 — Did the tiered conservation mandate cause the extra water savings, or were high users already cutting back?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Tiered targets assigned by past performance (sales quotas by prior-year volume, energy-reduction targets by baseline usage, cost-cut targets by prior spend), where the assignment rule creates regression to the mean and different trends |
| Domain | Water utilities / public policy |
| Task shape | 11 · Before and after with a control (suppliers with different assigned conservation standards, before and after the mandate; intensity difference-in-differences with pre-trend checks) |
| Core method | Monthly residential gallons per capita per day (R-GPCD) by supplier; outcome = log R-GPCD relative to the same month of the 2013 baseline; intensity DiD: outcome on standard × post with supplier fixed effects and hydrologic-region × month fixed effects (absorbing weather); event-study by quarter to check pre-trends; marginal effect = percentage-point savings per percentage point of assigned standard |
| Analytical stump | Standards were assigned by 2013 per-capita use, so high users got high targets. A cross-sectional regression of savings on the standard credits the mandate with savings that high users would have made anyway (they have more discretionary outdoor use to cut, and some were already cutting in the voluntary period). Within-supplier change against a pre-period, with region-by-month effects for weather, is required |
| Primary sources | California State Water Resources Control Board — Urban Water Supplier Conservation Reports (monthly production, R-GPCD, population, assigned conservation standards) |

## 1. The real-world situation

After a drought, a state water board reviewed its tiered conservation mandate, which had assigned suppliers reduction standards from 4% to 36%
based on their 2013 per-capita use. The board's evaluation showed a steep relationship between assigned standards and achieved savings and
recommended tiered standards for the next drought. An economist argued that the high-standard suppliers were already reducing faster before the
mandate. The board must decide whether to reuse tiers.

## 2. The decision (one deterministic recommendation)

**Whether tiered standards are reused (reused if the DiD marginal effect is ≥ 0.5 points of savings per point of standard and the pre-trend test
passes), with the estimated marginal effect.**

Rules (board memo):

* Data: supplier monthly reports, June 2014 – February 2016; outcome y = log(R-GPCD) − log(R-GPCD in the same month of 2013).
* Suppliers: those with an assigned standard and complete data for ≥ 18 of the 21 months; R-GPCD values outside 20–600 set to missing.
* Pre period: June 2014 – May 2015 (voluntary call); post period: June 2015 – February 2016 (mandate).
* Model: y = β × standard × post + supplier FE + hydrologic region × month FE; standard in percentage points; cluster SEs by supplier.
* Marginal effect = −β × 100 (points of savings per point of standard; positive means more savings).
* Event study: standard × quarter interactions (reference: March–May 2015); pre-trend test passes if the joint test of pre-period interactions has
  p ≥ 0.10.
* Comparison: the board's cross-sectional slope (post-period mean savings vs standard, OLS).

## 3. Why capable analysts get it wrong

* The cross-sectional dose–response looks like a clean experiment.
* Assignment by baseline use builds in regression to the mean and different trends.
* Weather differs by region and month; region × month effects are needed.
* Reported R-GPCD has outliers and reporting gaps.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `uw_supplier_data_<date>.csv` | CSV | ~45k (supplier × month, 2014–2023) | California SWRCB Urban Water Supplier conservation reports (data.ca.gov) | California open data (verify terms) | Production, R-GPCD, standards |
| 2 | `supplier_hydrologic_regions.csv` | CSV | ~410 | SWRCB | Same | Region mapping |
| 3 | `emergency_regulation_fact_sheet.pdf` | PDF | — | SWRCB | Public | Tier rules |
| 4 | `board_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `board_evaluation_slope.xlsx` | XLSX | — | Task author (cross-sectional regression) | — | The board's evidence |
| 6 | `did_intensity_reference.pdf` | PDF | — | Cite (intensity DiD references) | Cite | Method |

## 5. Deterministic solution path

1. Filter suppliers and months; clean outliers; construct y.
2. Fit the intensity DiD; marginal effect with clustered SE.
3. Event study and pre-trend test.
4. Cross-sectional slope for comparison; decision.

## 6. Wrong paths (method errors, not misreadings)

**A — cross-sectional slope.** Credits the mandate with pre-existing differences in savings trajectories.

**B — no pre-period.** Cannot detect differential trends.

**C — no region × month effects.** Weather differences confound savings.

**D — levels instead of logs relative to 2013.** High-use suppliers dominate the estimate mechanically.

## 7. Why the stump is analytical, not semantic

The panel, outcome and model are specified. The trap is treatment assigned on baseline outcomes.

## 8. Draft task prompt (prose)

> Our evaluation says tiered standards drove savings and recommends them again. Re-estimate the mandate's effect with the board memo's intensity DiD
> and pre-trend check and tell me whether tiers should be reused. Provide `mandate_effect.csv` (estimate, SE, event-study coefficients),
> `event_study.png`, and a one-page `tier_reuse_decision.pdf`.

## 9. Deliverables

* `mandate_effect.csv` — marginal effect, SE, event-study coefficients and the cross-sectional slope.
* `event_study.png` — coefficients by quarter with the mandate start marked.
* `tier_reuse_decision.pdf` — decision, estimates and why the cross-sectional slope misleads.

## 10. Where 25+ rubric criteria come from

* Panel construction (suppliers kept, outliers, months): 4.
* DiD estimate, SE, marginal effect: 4.
* Event-study coefficients (7 quarters) and the pre-trend test: 9.
* Cross-sectional slope: 2.
* Decision: 1.
* Contrast and interpretation: 3+.

## 11. Golden-output checklist

* Outcome relative to the same month of 2013.
* Supplier and region × month fixed effects; clustered SEs.
* Reference quarter for the event study; joint pre-trend test.

## 12. Build notes (scope tuning)

* Confirm on the data that the cross-sectional slope is well above 0.5 and that the DiD estimate is lower; set the reuse threshold so the decision
  differs between the two methods.
