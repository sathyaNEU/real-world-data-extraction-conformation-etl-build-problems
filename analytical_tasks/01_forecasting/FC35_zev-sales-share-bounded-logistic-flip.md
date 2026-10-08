# FC35 — Planning for electric-vehicle load: a sales share cannot exceed 100%, and a fleet share is not a sales share

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Automakers' compliance planning and utilities' EV-load planning under zero-emission-vehicle mandates |
| Domain | Automotive / utility planning |
| Task shape | 13 · Scenarios and the flip point (fit window × ceiling grid; flip ceiling for the plan decision) |
| Core method | Flow measure (new-vehicle sales share by model year) derived from registration snapshots; logistic model fitted by OLS on the logit of share ÷ ceiling; scenario grid and flip-point search |
| Analytical stump | Linear or exponential extrapolation of a share is unbounded; fleet (stock) shares lag sales (flow) shares by years and understate adoption; fitting on raw shares instead of logits misstates the curve's bend |
| Primary sources | California DMV vehicle fuel type counts by ZIP code (annual snapshots), California Energy Commission ZEV sales data |

## 1. The real-world situation

A California utility must choose between **Plan A** (accelerated residential transformer replacement assuming ZEVs exceed 65% of
new light-duty sales in model year 2030) and **Plan B** (targeted upgrades). The planner extrapolated the linear trend in the share of
registered vehicles that are electric — the fleet share — and found 2030 far below 65%. A second analyst extrapolated recent sales
growth exponentially and found over 100%.

## 2. The decision (one deterministic recommendation)

**Plan A or B, the base-case 2030 sales share, and the ceiling at which the base decision flips.**

Rules (planning memo):

* Sales share for model year Y = vehicles of model year Y with fuel in {Battery Electric, Plug-in Hybrid, Hydrogen Fuel Cell}
  ÷ all light-duty vehicles of model year Y, counted in the DMV snapshot taken in January of Y + 1 (first registration year).
* Model: ln[s_Y ÷ (C − s_Y)] = α + β·Y, OLS, ceiling C.
* Scenario grid: fit window {MY2016–2024, MY2019–2024} × ceiling C ∈ {1.00, 0.90, 0.80}.
* Base case: window 2016–2024, C = 1.00. Plan A if base 2030 share ≥ 65%.
* Flip point: the ceiling C (two decimals, with base window) at which the 2030 share equals 65%.

## 3. Why capable analysts get it wrong

* Fleet shares are easy to compute from registration counts and move slowly because the stock turns over over 15+ years.
* Shares are bounded; linear and exponential trends are not.
* The logistic's linearization requires the logit transform with the ceiling; fitting a straight line to raw shares or to log
  shares gives different curves.
* Model-year counts need the snapshot taken soon after the model year to approximate sales.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–9 | `vehicle_fuel_type_count_by_zip_2017.csv` … `2025.csv` (January snapshots) | CSV | 1–2M rows each | California Open Data (DMV) | CA open data terms (public) | Counts by ZIP, model year, fuel, make, duty |
| 10 | `cec_zev_sales_by_quarter.xlsx` | XLSX | ~5k | California Energy Commission | Public (State of California) | Cross-check of ZEV sales |
| 11 | `dmv_fuel_type_data_dictionary.pdf` | PDF | — | CA DMV / Open Data | Same | Fuel categories, duty |
| 12 | `carb_acc_ii_requirements_extract.pdf` | PDF | — | California Air Resources Board | Public | Context (mandate path) |
| 13 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 14 | `planner_fleet_share_trend.xlsx` | XLSX | ~15 | Task author | — | Fleet-share extrapolation |
| 15 | `analyst_exponential_sales.xlsx` | XLSX | ~15 | Task author | — | Exponential extrapolation |

## 5. Deterministic solution path

1. For each model year 2016–2024, compute the sales share from the following January snapshot (light-duty only).
2. Fit the logistic in each scenario cell; forecast 2030; decide on the base cell.
3. Solve for the flip ceiling; report the grid.
4. Contrast fleet-share and exponential projections.

## 6. Wrong paths (method errors, not misreadings)

**A — fleet share trend.** Plan B by a wide margin.

**B — exponential sales growth.** > 100% shares; Plan A for the wrong reason.

**C — linear share trend.** Unbounded; mis-timed.

**D — log of share instead of logit.** Different curvature.

## 7. Why the stump is analytical, not semantic

The share definition and model are explicit. The traps are stock–flow confusion and unbounded models for bounded quantities —
analytical modelling errors.

## 8. Draft task prompt (prose)

> Pick Plan A or Plan B for transformer replacement based on the 2030 ZEV share of new sales, computed and projected as the
> planning memo describes from the DMV registration snapshots. Provide `zev_share_scenarios.csv` (model-year shares; fitted α, β per
> cell; 2030 share per cell), `share_projection.png` showing observed shares, the six logistic paths, and the two analysts'
> extrapolations against the 65% line, and a one-page `plan_decision.pdf` with the decision and the flip ceiling.

## 9. Deliverables

* `zev_share_scenarios.csv`, `share_projection.png`, `plan_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 9 model-year shares; 6 cells × (α, β, 2030 share); decision; flip ceiling; two contrasts.

## 11. Golden-output checklist

* Flow share from first-registration snapshots; logit transform with ceiling; grid; flip solve.

## 12. Build notes (scope tuning)

* Verify snapshot timing and the light-duty filter in each annual file; confirm the base decision differs from the fleet-share
  method.
* If the base case is far from 65%, adjust the plan threshold before freezing (document it) so the flip point is informative.
