# FC28 — Allocating driver incentives across neighbourhoods: area forecasts that add up, and add up correctly

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Ride-hailing and delivery marketplaces allocating supply incentives from hierarchical demand forecasts |
| Domain | Two-sided marketplaces / urban mobility operations |
| Task shape | 05 · Allocation to a fixed total (incentive budget across 77 community areas; solve the per-trip rate under a floor) |
| Core method | Hierarchical forecast reconciliation (bottom-up, top-down by historical proportions, top-down by forecast proportions, OLS projection) chosen by hold-out accuracy at the area level; floor-constrained allocation |
| Analytical stump | Top-down allocation with historical shares assumes the geographic mix is stable; after downtown demand recovered at a different pace from neighbourhoods, historical shares misallocate. Bottom-up sums of noisy area forecasts make the city total noisy. The reconciliation must be chosen by out-of-sample area-level error |
| Primary sources | City of Chicago Transportation Network Providers (TNP) trips |

## 1. The real-world situation

A ride-hailing operator allocates a fixed **$2,000,000 monthly driver-incentive budget** across Chicago's 77 community areas in
proportion to forecast trip demand, with a minimum of $8,000 per area. The city-level forecast is good, so the team splits it by
each area's share of trips over the past year. After downtown demand rebounded faster than other areas, drivers were paid
incentives where demand was weakening.

## 2. The decision (one deterministic recommendation)

**The per-forecast-trip incentive rate and each area's allocation for the target month.**

Rules (marketplace planning memo):

* Series: weekly trip counts by pickup community area (trips with a pickup area) and the city total of those trips, 2022-01 through
  the forecast origin.
* Base forecasts for every series: seasonal naive with drift on weekly data (value 52 weeks ago × ratio of last 13 weeks to the same
  13 weeks a year earlier).
* Reconciliation candidates: BU (sum of areas), TDH (city forecast × last-52-week area shares), TDF (city forecast × area base
  forecast shares), OLS (projection onto the coherent subspace).
* Select the method with the lowest mean absolute error across areas on the 13 weeks before the origin (rolling one-step-ahead,
  re-forecast weekly).
* Target month forecast = Σ of the selected method's weekly area forecasts for the 4 weeks of the month.
* Allocation_a = max($8,000, r × forecast_a), r solved so the total is exactly $2,000,000; largest-remainder rounding.

## 3. Why capable analysts get it wrong

* Splitting a good total by historical shares is simple and usually fine — until the mix shifts.
* Bottom-up looks "granular" but sums noisy forecasts.
* Choosing a reconciliation by city-level accuracy ignores the area-level decision.
* Floors make the rate a fixed-point problem.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–3 | `Transportation_Network_Providers_Trips_2022.csv`, `…_2023.csv`, `…_2024.csv` (area/time extracts) | CSV | 60–80M each (extract to needed columns) | City of Chicago Data Portal | City of Chicago data terms (free use) | Trips with pickup community area, timestamps |
| 4 | `tnp_weekly_area_counts.parquet` | Parquet | ~12k | Derived | Same | Weekly series |
| 5 | `community_areas.geojson` | GeoJSON | 77 | City of Chicago | Same | Boundaries |
| 6 | `tnp_dataset_description.pdf` | PDF | — | City of Chicago | Same | Fields, privacy rules |
| 7 | `hyndman_reconciliation_reference.pdf` (citation) | PDF | — | Cite | Cite | Reconciliation methods |
| 8 | `marketplace_planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `incentive_budget.json` | JSON | — | Task author | — | Budget, floor, target month |
| 10 | `last_month_allocation_tdh.xlsx` | XLSX | 77 | Task author | — | Historical-share allocation |

## 5. Deterministic solution path

1. Build weekly area and city series; compute base forecasts.
2. Reconcile with each method; rolling one-step hold-out over 13 weeks; area-level MAE; select.
3. Forecast the target month with the selected method; solve r with floors; allocate.
4. Contrast with TDH allocations.

## 6. Wrong paths (method errors, not misreadings)

**A — TDH by habit.** Misallocates when shares are trending.

**B — selection by city-level error.** Picks a method that is good for the total, not for areas.

**C — BU without evaluation.** Noisy totals.

**D — proportional then floor.** Total ≠ budget.

## 7. Why the stump is analytical, not semantic

Series, base forecasts, candidates, selection criterion and allocation are defined. The traps are about mix shift and evaluation
level — analytical choices in hierarchical forecasting.

## 8. Draft task prompt (prose)

> Allocate next month's $2 million incentive budget across Chicago's 77 community areas in proportion to forecast trips with an
> $8,000 floor, following the planning memo: test the four reconciliation methods on the last 13 weeks, use the best at the area
> level, and solve the rate. Provide `area_allocation.csv` (area, forecast trips, floor flag, allocation, last month's allocation),
> `reconciliation_errors.png` comparing area-level MAE of the four methods, and a one-page `allocation_memo.pdf` with the selected
> method, the rate, and the five areas whose allocation changes most versus last month's method.

## 9. Deliverables

* `area_allocation.csv`, `reconciliation_errors.png`, `allocation_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 methods' MAE; selected method; rate; allocations for 10 named areas; floor areas; top-5 changes; total check.

## 11. Golden-output checklist

* Correct base forecasts; reconciliation formulas; rolling hold-out; selection; floors; exact total.

## 12. Build notes (scope tuning)

* Pick an origin when area shares were shifting (e.g. 2023 downtown recovery); confirm TDH is not selected.
* Document the extraction (columns kept, trips without pickup area excluded).
