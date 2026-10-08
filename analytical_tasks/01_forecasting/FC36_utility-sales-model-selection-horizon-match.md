# FC36 — Choosing a budget forecasting model: the winner one month ahead loses twelve months ahead

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Corporate FP&A model selection where tools report short-horizon accuracy but budgets need annual totals |
| Domain | Electric utility finance / revenue budgeting |
| Task shape | 07 · Grid of cells (candidate model × evaluation horizon → error; adopt the model best at the decision horizon) |
| Core method | Rolling-origin evaluation at the horizon and aggregation the decision uses (12-month-ahead fiscal-year total), compared with one-step monthly accuracy |
| Analytical stump | One-step-ahead monthly MAPE rewards models that track the latest level (persistence-like) and penalizes structural models; the budget needs an accurate 12-month cumulative total, where errors compound or cancel differently. Selecting on the wrong horizon picks the wrong model |
| Primary sources | EIA-861M monthly retail electricity sales by state and sector, NOAA degree-day data |

## 1. The real-world situation

A utility's budgeting team chooses one of four models to forecast next fiscal year's total retail sales (which drives the revenue
budget). Their forecasting tool ranks models by one-month-ahead MAPE, and a drift-based seasonal model won. Its annual budgets
were off by 3–5% two years running, while a weather-and-trend model that "lost" the bake-off would have been within 1%.

## 2. The decision (one deterministic recommendation)

**Which model forecasts next fiscal year's total sales, and what is the forecast?**

Rules (budgeting memo):

* Series: monthly retail sales (MWh), all sectors, for the state in the folder, from EIA-861M, January 2005 onward.
* Candidates: M1 seasonal naive; M2 seasonal naive × trailing-12-month growth; M3 OLS on month effects + linear trend + monthly
  HDD + CDD (state population-weighted, NOAA), forecast with 15-year normal degree days; M4 three-year average monthly profile ×
  trailing-12-month total.
* Evaluation origins: every October from 2012 to 2023 (fiscal year Oct–Sep). For each origin, (a) one-step monthly APE averaged over
  the 12 months of the fiscal year using rolling one-month origins; (b) absolute percentage error of the 12-month total forecast
  made at the October origin.
* Adopt the model with the lowest mean of (b). Forecast fiscal year Oct 2025 – Sep 2026 with it.

## 3. Why capable analysts get it wrong

* Short-horizon accuracy is what most tools report by default.
* Persistence-type models are hard to beat one step ahead and drift at longer horizons.
* Weather-normalized models look worse month to month (they don't chase weather noise) but forecast normal-weather annual totals well.
* Errors in monthly forecasts are correlated; summing them does not behave like independent errors.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `sales_ult_cust_monthly_2005_2025.xlsx` (EIA-861M) | XLSX | ~60k (utility × state × month) | EIA | U.S. Gov public domain | Monthly sales |
| 2 | `eia_api_retail_sales_state_monthly.json` | JSON | ~15k | EIA Open Data API | Public domain | State totals cross-check |
| 3 | `climdiv-hddcst-v1.0.0.txt`, `climdiv-cddcst-v1.0.0.txt` | Fixed-width | ~10k each | NOAA NCEI climate divisional data | Public domain | State degree days |
| 4 | `population_weights_state.csv` | CSV | ~50 | Census | Public domain | Weighting reference |
| 5 | `eia861m_documentation.pdf` | PDF | — | EIA | Public domain | Definitions |
| 6 | `budgeting_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `tool_bakeoff_report.xlsx` | XLSX | ~10 | Task author | — | One-step ranking |
| 8 | `state_scope.json` | JSON | 1 | Task author | — | State |
| 9 | `monthly_state_series.parquet` | Parquet | ~250 | Derived | Public domain | Working series |
| 10 | `normal_degree_days_15yr.csv` | CSV | 12 | Derived | Public domain | Normals |

## 5. Deterministic solution path

1. Build the state monthly series and degree days.
2. For each origin and model, compute (a) and (b); average across origins.
3. Adopt the model with the lowest (b); produce the FY2026 forecast.
4. Show where (a) and (b) rankings disagree.

## 6. Wrong paths (method errors, not misreadings)

**A — select by one-step MAPE.** Adopts M2; biased annual totals.

**B — evaluate monthly forecasts but sum MAPEs.** Not the budget error.

**C — M3 with actual degree days in forecasts.** Look-ahead in evaluation.

**D — single origin.** Noisy selection.

## 7. Why the stump is analytical, not semantic

The quantity budgeted and the evaluation rule are explicit. The trap is horizon/aggregation mismatch in model selection.

## 8. Draft task prompt (prose)

> Pick the model for next fiscal year's sales budget the way the budgeting memo specifies — by how well each candidate has forecast
> the fiscal-year total from October — and give me the FY2026 forecast. Provide `model_grid.csv` (model × criterion: one-step MAPE,
> annual-total APE, ranks) and `horizon_errors.png` comparing both error measures per model across origins. Add a one-page
> `budget_model_memo.pdf` with the adopted model, its forecast and why the tool's ranking misled.

## 9. Deliverables

* `model_grid.csv`, `horizon_errors.png`, `budget_model_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 models × 2 criteria = 8 means; 12 origins × annual APE for the adopted model; adopted model; FY2026 forecast; tool contrast.

## 11. Golden-output checklist

* Correct origins; normal-weather forecasts for M3; criterion (b); forecast.

## 12. Build notes (scope tuning)

* Choose a state where one-step and annual rankings disagree; confirm before freezing.
* State the population-weighting method for degree days precisely.
