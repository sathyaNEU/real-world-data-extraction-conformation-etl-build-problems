# FC02 — Firm capacity for a four-zone portfolio: the peak of the sum is not the sum of the peaks

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Domain | Electric utilities / capacity procurement / transmission planning |
| Task shape | 02 · Forecast across many periods (12 monthly P90 peaks → one committed level) |
| Core method | Weather-year replay of growth-normalized hourly zone loads, summed hour by hour before taking maxima; empirical quantiles of monthly maxima |
| Analytical stump | Maxima are not additive: zone peaks occur at different hours, so summing per-zone peak forecasts overstates the combined requirement; quantiles of maxima must be taken on the combined series |
| Primary sources | ERCOT hourly native load by weather zone (2015–2024), ERCOT load-zone documentation |

## 1. The real-world situation

A utility holding company serves load spread across four ERCOT weather zones and must contract a **firm capacity block
for 2025** sized to the 1-in-10 (P90) monthly peak of its combined load. The planning team forecast each zone's P90 peak
with its usual zone-level tool and added the four numbers. Finance noticed the contract cost had jumped and asked why the
combined requirement exceeded any hourly combined load the portfolio had ever drawn.

## 2. The decision (one deterministic recommendation)

**How many MW of firm capacity should be contracted for 2025, and which month sets it?**

Forecast rules (planning memo):

* Portfolio load in hour h = Σ of the four zones' hourly loads in hour h.
* Replay years 2015–2024. Before combining, scale each zone's hourly series in year y by (that zone's 2024 annual energy ÷
  its year-y annual energy), so every replay year is expressed at 2024 load levels.
* For each calendar month and each replay year, take the maximum hourly portfolio load in that month (calendar month
  boundaries in Central Prevailing Time; hour-ending convention as published).
* Monthly P90 = the 90th percentile of the ten replay-year maxima, using the inclusive linear-interpolation convention
  (position = 1 + 0.9 × (n − 1)).
* Committed block = the largest of the twelve monthly P90 values, rounded up to the next 10 MW.

## 3. Why capable analysts get it wrong

* Zone-level forecasting tools are standard; adding their outputs is the natural "bottom-up" step.
* Zones peak at different hours and on different days (coastal humidity vs. far-west industrial load); the combined peak is
  lower than the sum of zone peaks by a diversity factor that is easy to forget.
* Quantiles are not additive either: P90 of a sum ≠ sum of P90s.
* Fitting a normal distribution to ten maxima looks more "statistical" than an order statistic but changes the tail.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–10 | `Native_Load_2015.xlsx` … `Native_Load_2024.xlsx` | XLSX | ~8.8k hourly rows each × 9 columns | ERCOT hourly load data archives | ERCOT public data (terms of use; verify) | Hourly load by weather zone |
| 11 | `native_load_2015_2024_long.parquet` | Parquet | ~700k | Derived from 1–10 | Same | Tidy long format |
| 12 | `ercot_weather_zone_map.pdf` | PDF | — | ERCOT | Public | Zone definitions |
| 13 | `annual_zone_energy.csv` | CSV | ~80 | Derived (for checking) | Same | Growth factors |
| 14 | `portfolio_zones.json` | JSON | 4 | Task author | — | Zones in scope |
| 15 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 16 | `zone_forecasts_from_tool.xlsx` | XLSX | 48 | Task author (zone P90s as the team computed them) | — | The bottom-up figure to challenge |

## 5. Deterministic solution path

1. Load hourly zone loads; compute each zone's annual energy per year and scaling factors to 2024.
2. Scale each zone's hourly series; sum the four zones hour by hour.
3. For each month × replay year, take the maximum portfolio hour.
4. Monthly P90 across the ten years with the stated percentile convention; commit = max monthly P90 rounded up.
5. Report the diversity factor: Σ zone monthly P90s ÷ portfolio monthly P90.

## 6. Wrong paths (method errors, not misreadings)

**A — sum of zone P90 peaks.** Overstates the binding month by the diversity margin; the contract is oversized.

**B — scaling the combined series by combined growth.** Distorts the hour-by-hour coincidence when zones grew at very
different rates; binding-month value shifts.

**C — normal fit to maxima.** Mean + 1.2816 SD of ten maxima differs from the order statistic; can change the binding month.

**D — no growth normalization.** Older years understate demand; the P90 is too low.

## 7. Why the stump is analytical, not semantic

The memo defines portfolio load, scaling, the percentile convention and the committed block without ambiguity. The wrong
answers come from performing the operations in the wrong order (aggregate-then-maximize vs maximize-then-aggregate) — an
analytical property of maxima and quantiles, not a misunderstanding of any field.

## 8. Draft task prompt (prose)

> Size our 2025 firm-capacity block from the ERCOT zone loads in the folder, following the planning memo: replay ten
> years at 2024 load levels, find each month's 1-in-10 peak of our combined four-zone load, and commit to the largest. Give
> me `monthly_p90_forecast.csv` with, for every month, the ten replay-year combined maxima, the P90, the sum of the four
> zones' own P90s and the resulting diversity factor; `p90_by_month.png`, a chart of the twelve monthly P90s against the
> summed-zone figures with the committed block drawn; and a short `capacity_memo.pdf` stating the block, the binding
> month, and how many MW the bottom-up method would have over-contracted.

## 9. Deliverables

* `monthly_p90_forecast.csv`, `p90_by_month.png`, `capacity_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 monthly P90s; 12 summed-zone comparisons or diversity factors; committed block; binding month; over-contract figure.

## 11. Golden-output checklist

* Per-zone scaling then hourly summation; monthly maxima per year; inclusive P90; max over months; rounding up.

## 12. Build notes (scope tuning)

* Choose four zones with different peak timing (e.g. a coastal and a far-west zone) so the diversity factor exceeds 3%.
* Verify the hour-ending and DST handling in the ERCOT files you ship (the 25-hour day must not create a duplicate key).
