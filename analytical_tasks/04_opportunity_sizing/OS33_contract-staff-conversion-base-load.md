# OS33 — Converting agency nurses to staff: commit to the base, not the average

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Commitment sizing (reserved cloud instances versus on-demand, converting contractors to full-time employees, long-term carrier contracts) where committed capacity is paid whether used or not |
| Domain | Long-term care / workforce |
| Task shape | 04 · Setting one dial (the number of contract hours per week converted to employed staff positions at each facility, and the annual savings) |
| Core method | Weekly contract hours per facility from daily staffing records; convert the critical-fractile level of weekly need (newsvendor: P(need ≤ Q) = savings per used hour ÷ (savings per used hour + idle cost per hour) = 33 ÷ 95 ≈ 0.347); net savings = used converted hours × (agency − employed rate) − idle converted hours × employed rate |
| Analytical stump | Converting the average weekly contract hours creates positions that sit idle in low-need weeks (or must be used inefficiently), because contract hours swing with census and vacancies. The savings-maximising commitment is a quantile of the need distribution set by the cost ratio (newsvendor logic), not the mean |
| Primary sources | CMS Payroll-Based Journal (PBJ) Daily Nurse Staffing (employee and contract hours by facility and day) |

## 1. The real-world situation

A nursing-home chain spends heavily on agency nurses. The finance team proposed converting each facility's average weekly contract RN hours
into employed positions and sized savings as average hours × (agency rate − staff rate). Operations warned that contract hours vary a lot from
week to week.

## 2. The decision (one deterministic recommendation)

**The converted weekly RN hours per facility (the critical-fractile quantile of weekly contract hours) and the chain's annual net savings.**

Rules (finance memo):

* Data: PBJ daily nurse staffing for the chain's facilities (CCNs in memo), four quarters; contract RN hours = `Hrs_RN_ctr` (plus admin and DON
  contract hours per memo).
* Weekly contract hours = sum over Monday–Sunday.
* Costs: agency rate $95/h; employed loaded rate $62/h; converted hours are paid every week (idle if not needed).
* Critical fractile: convert level Q where P(weekly need ≥ Q) = (cost of idle) ÷ (cost of idle + savings per used hour) per memo → Q = the
  empirical quantile at 1 − 62 ÷ 95 = 0.347 of weekly contract hours.
* Net savings = Σ_weeks [min(need, Q) × (95 − 62) − max(0, Q − need) × 62] annualised.
* Report the mean-based conversion and its net savings for contrast.

## 3. Why capable analysts get it wrong

* Average hours look like the natural target.
* Committed hours cost money in weeks they are not needed.
* The optimal commitment depends on the ratio of savings to idle cost and on the distribution.
* Weekly aggregation from daily data must align weeks consistently.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–4 | `PBJ_Daily_Nurse_Staffing_<yyyy>_Q<q>.csv` | CSV | ~1.3M each | CMS Provider Data Catalog | U.S. Gov public domain | Daily hours by facility |
| 5 | `pbj_data_dictionary.pdf` | PDF | — | CMS | Public domain | Field definitions |
| 6 | `chain_facilities.json` | JSON | ~30 | Task author | — | Facilities in scope |
| 7 | `cost_assumptions.json` | JSON | — | Task author | — | Rates |
| 8 | `finance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `finance_mean_conversion.xlsx` | XLSX | ~30 | Task author | — | Naive sizing |
| 10 | `newsvendor_reference.pdf` | PDF | — | Cite | Cite | Critical fractile |

## 5. Deterministic solution path

1. Filter facilities; daily contract RN hours; weekly sums.
2. Critical-fractile quantile per facility; net savings by week; annualise.
3. Mean-based contrast; chain totals.

## 6. Wrong paths (method errors, not misreadings)

**A — convert the mean.** Idle costs ignored.

**B — convert the minimum.** Leaves savings on the table.

**C — gross savings without idle cost.** Overstated.

**D — daily instead of weekly quantiles.** Wrong planning unit.

## 7. Why the stump is analytical, not semantic

The cost structure and quantile rule are specified. The trap is committing to an average under variable demand.

## 8. Draft task prompt (prose)

> How many agency RN hours should each facility convert to employed staff, and what will the chain save? Use weekly PBJ contract hours and the
> critical-fractile rule in the finance memo. Provide `conversion_plan.csv` (facility: mean, quantile, converted hours, net savings), `weekly_need_example.png`,
> and a one-page `conversion_case.pdf`.

## 9. Deliverables

* `conversion_plan.csv`, `weekly_need_example.png`, `conversion_case.pdf`.

## 10. Where 25+ rubric criteria come from

* Converted hours and savings for 10 facilities; chain totals; mean-based contrast.

## 11. Golden-output checklist

* Hour fields; weekly alignment; quantile; savings formula; annualisation.

## 12. Build notes (scope tuning)

* Confirm mean-based conversion yields lower net savings than the quantile rule at most facilities.
