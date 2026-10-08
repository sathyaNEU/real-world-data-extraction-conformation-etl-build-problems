# FC40 — How many summer days will the bridge path overflow? Count probabilities, not point forecasts above a line

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Capacity-exceedance planning from probabilistic forecasts (event crowd control, server burst budgets, warehouse surge days) |
| Domain | Urban mobility / traffic management |
| Task shape | 02 · Forecast across many periods (92 daily exceedance probabilities → one committed number of crew-days) |
| Core method | Log-scale regression of daily counts on calendar effects and trend with residual variance estimated by season; exceedance probability per day from the predictive distribution; expected exceedance days = Σ probabilities |
| Analytical stump | Comparing point forecasts with the threshold counts zero days when every forecast sits just below it, even though many days have a substantial chance to exceed. Constant-variance (levels) intervals under-state summer spread; the expected count of exceedances is a sum of probabilities |
| Primary sources | Seattle Fremont Bridge bicycle counter (hourly), NOAA daily weather |

## 1. The real-world situation

A city deploys **traffic-control crews** on days when bicycle volume on a bridge path is expected to exceed 7,000 riders, and
budgets crew-days for the summer in advance. The analyst forecast each summer day's count and counted the days whose forecast
exceeded 7,000: two. The previous summer there had been fourteen such days.

## 2. The decision (one deterministic recommendation)

**Committed crew-days for June–August next year = expected number of days with count > 7,000, rounded up.**

Rules (traffic operations memo):

* Data: hourly counts summed to daily totals (both directions), 2014 – last complete year; days with any missing hour excluded.
* Model: ln(daily count) = day-of-week effects + month effects + federal-holiday indicator + linear trend, OLS on 2014 onward
  excluding March 2020 – December 2021.
* Residual standard deviation estimated separately for each month (pooled across years) from OLS residuals.
* For each day of next June–August: mean μ_d from the model; P(count > 7,000) = 1 − Φ((ln 7,000 − μ_d) ÷ σ_month).
* Crew-days = ceil(Σ_d P_d).

## 3. Why capable analysts get it wrong

* Threshold planning is usually done by comparing forecasts to the threshold — a deterministic view of a random quantity.
* Weather (rain) creates large day-to-day swings; the forecast mean is the typical day, not the upper tail.
* Levels models with constant variance put the same absolute spread on summer and winter days.
* The expected number of exceedance days is E[Σ 1{X_d > T}] = Σ P(X_d > T) — linearity of expectation.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Fremont_Bridge_Bicycle_Counter.csv` | CSV | ~100k hourly | Seattle Open Data | City of Seattle open data terms (public) | Hourly counts by direction |
| 2 | `fremont_daily_totals.parquet` | Parquet | ~4k | Derived | Same | Daily series |
| 3 | `ghcnd_USW00024233_daily.csv` (Seattle–Tacoma airport) | CSV | ~4k | NOAA NCEI | Public domain | Rain and temperature (context) |
| 4 | `us_federal_holidays_2014_2026.json` | JSON | ~140 | OPM | Public domain | Holiday indicator |
| 5 | `seattle_bike_counters_metadata.pdf` | PDF | — | Seattle DOT | Public | Counter description |
| 6 | `other_counters_daily.csv` (Burke-Gilman, Spokane St.) | CSV | ~30k | Seattle Open Data | Same | Context |
| 7 | `traffic_operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `analyst_point_forecast.xlsx` | XLSX | 92 | Task author | — | Point-forecast count |
| 9 | `threshold_rationale.pdf` | PDF | — | Task author | — | 7,000/day path capacity |
| 10 | `calendar_next_summer.csv` | CSV | 92 | Derived | — | Day attributes |

## 5. Deterministic solution path

1. Build daily totals; drop incomplete days and the excluded period.
2. Fit the log model; compute monthly residual SDs.
3. For each summer day compute μ_d and P_d; sum; ceiling.
4. Validate on the last observed summer: expected vs realized exceedances for both methods.

## 6. Wrong paths (method errors, not misreadings)

**A — point forecasts vs threshold.** Near-zero crew-days.

**B — constant variance in levels.** Summer tail under-stated.

**C — one pooled SD.** Seasonal heteroscedasticity ignored.

**D — counting days with P > 0.5.** Still a deterministic rule; biased low.

## 7. Why the stump is analytical, not semantic

Counts, threshold and model are specified. The trap is the difference between the forecast of a quantity and the forecast of an
event defined on it — a probabilistic reasoning error.

## 8. Draft task prompt (prose)

> Budget next summer's crew-days for bridge traffic control: the expected number of days with more than 7,000 riders, computed as
> the traffic operations memo describes. Provide `summer_exceedance.csv` (date: forecast mean, σ, exceedance probability),
> `exceedance_calendar.png` (a calendar heat map of probabilities) and a one-page `crew_budget.pdf` with the committed crew-days and
> the back-test against last summer.

## 9. Deliverables

* `summer_exceedance.csv`, `exceedance_calendar.png`, `crew_budget.pdf`.

## 10. Where 25+ rubric criteria come from

* Model coefficients (DOW, months, holiday, trend); monthly σ (3); 92 probabilities (spot-check 15); committed crew-days; back-test.

## 11. Golden-output checklist

* Daily totals; exclusions; log model; monthly σ; Σ probabilities; ceiling.

## 12. Build notes (scope tuning)

* Choose the threshold near the upper tail of recent summer days so the point-forecast method yields ≤ 3 days and the probabilistic
  method ≥ 10.
* Note counter replacement dates (if any) in the memo.
