# FC24 — Budgeting fleet fuel after a wholesale crash: pump prices fall like feathers

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Fleet and logistics operators budgeting fuel and setting surcharges (parcel carriers, ride-hailing driver economics) |
| Domain | Energy procurement / fleet operations |
| Task shape | 02 · Forecast across many periods (8 weekly retail-price forecasts → one committed fuel budget) |
| Core method | Engle–Granger error-correction model with asymmetric short-run pass-through (separate coefficients for wholesale increases and decreases), estimated on a pre-specified window and iterated forward |
| Analytical stump | Retail prices respond to wholesale rises quickly and to falls slowly. A levels regression implies instant pass-through; a symmetric ECM averages the two speeds; a differences-only model loses the long-run anchor. After a wholesale drop, all three under-forecast the next weeks' pump prices |
| Primary sources | EIA weekly retail gasoline prices, EIA spot prices (RBOB), EIA Petroleum Marketing documentation |

## 1. The real-world situation

A delivery fleet sets its fuel budget for the next eight weeks right after a sharp fall in wholesale gasoline. The analyst
regressed weekly retail prices on wholesale prices in levels and applied the new wholesale level, forecasting an immediate 40-cent
drop at the pump. Drivers saw prices fall a few cents a week; the budget was blown by week three.

## 2. The decision (one deterministic recommendation)

**The committed 8-week fuel budget (sum of forecast weekly retail price × planned gallons), from the forecast origin in the
folder.**

Rules (procurement memo):

* Retail: EIA weekly U.S. regular gasoline retail price (all formulations), $/gal; wholesale: weekly average of daily NY Harbor
  RBOB spot, $/gal (weeks ending Monday aligned to retail survey dates as in the memo).
* Estimation window: the 260 weeks before the origin.
* Step 1: long-run relation r = θ₀ + θ₁ w by OLS; residual u.
* Step 2: Δr_t = α + Σ_{i=0..2} (β⁺_i Δw⁺_{t−i} + β⁻_i Δw⁻_{t−i}) + γ u_{t−1} + ε, where Δw⁺ = max(Δw, 0), Δw⁻ = min(Δw, 0).
* Forecast: iterate weekly for 8 weeks using the wholesale futures-implied path in the folder (taken as given).
* Budget = Σ forecast price × planned gallons per week, rounded to the nearest $1,000.

## 3. Why capable analysts get it wrong

* Levels regressions of two trending price series fit extremely well (high R²) and imply that retail jumps to the new equilibrium
  at once.
* Symmetric models are the textbook default; asymmetry has to be allowed explicitly.
* Differencing removes the trend but also removes the error-correction pull back to equilibrium.
* Weekly alignment between survey dates and spot averages matters for lag structure.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `pet_pri_gnd_dcus_nus_w.xls` (weekly retail gasoline) | XLS | ~1.8k weeks | EIA | U.S. Gov public domain | Retail prices |
| 2 | `pet_pri_spt_s1_d.xls` (daily spot prices) | XLS | ~10k days × products | EIA | Public domain | RBOB spot |
| 3 | `eia_api_retail_regions_weekly.json` | JSON | ~15k | EIA Open Data API | Public domain | Regional retail (context) |
| 4 | `retail_spot_weekly_aligned.parquet` | Parquet | ~1.5k | Derived | Public domain | Aligned series |
| 5 | `eia_gasoline_price_survey_methodology.pdf` | PDF | — | EIA | Public domain | Survey timing |
| 6 | `borenstein_cameron_gilbert_1997_citation.pdf` | PDF | — | QJE 1997 (cite) | Cite | Asymmetry background |
| 7 | `futures_implied_wholesale_path.csv` | CSV | 8 | Task author (from public settlement prices on the origin date) | Public | Wholesale path |
| 8 | `planned_gallons.csv` | CSV | 8 | Task author | — | Fleet consumption plan |
| 9 | `procurement_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `analyst_levels_forecast.xlsx` | XLSX | ~10 | Task author | — | Levels-regression forecast |

## 5. Deterministic solution path

1. Align weekly retail and wholesale; restrict to the estimation window.
2. Estimate the long-run OLS; compute residuals; estimate the asymmetric ECM.
3. Iterate forecasts 8 weeks with the given wholesale path; compute the budget.
4. Contrast with levels and symmetric-ECM forecasts; report realized prices if the origin is historical (validation only).

## 6. Wrong paths (method errors, not misreadings)

**A — levels regression.** Immediate full pass-through; budget too low.

**B — symmetric ECM.** Average speed; budget too low after a drop.

**C — differences without error correction.** No convergence; drifts.

**D — misaligned weeks.** Lag coefficients shift.

## 7. Why the stump is analytical, not semantic

Series, window, alignment and model are specified. The trap is dynamic specification — asymmetric adjustment and cointegration —
not a reading error.

## 8. Draft task prompt (prose)

> Wholesale gasoline just dropped sharply and we need the next eight weeks' fuel budget. Following the procurement memo, estimate
> the retail–wholesale relationship on the last five years and forecast weekly pump prices along the given wholesale path. Provide
> `fuel_forecast.csv` (week: wholesale, forecast retail, gallons, cost), `pass_through_paths.png` comparing the asymmetric forecast with
> the levels and symmetric alternatives, and a one-page `fuel_budget.pdf` with the committed budget and the estimated up/down
> pass-through speeds.

## 9. Deliverables

* `fuel_forecast.csv`, `pass_through_paths.png`, `fuel_budget.pdf`.

## 10. Where 25+ rubric criteria come from

* θ₀, θ₁, γ, six β coefficients; 8 weekly forecasts; budget; levels/symmetric contrasts.

## 11. Golden-output checklist

* Alignment; two-step estimation; asymmetric terms; iteration; budget.

## 12. Build notes (scope tuning)

* Choose an origin right after a large wholesale decline (e.g. late 2022) so the asymmetric forecast differs by > 15 ¢/gal at week 4.
* Publish the reference coefficient estimates.
