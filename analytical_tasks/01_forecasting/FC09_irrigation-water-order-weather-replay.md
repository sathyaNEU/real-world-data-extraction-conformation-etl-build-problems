# FC09 — Ordering irrigation water for next season: replay the weather, then take the percentile

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Path-dependent simulation of resource needs (inventory with carry-over, battery state of charge, cloud budget burn), where percentiles require replaying whole scenarios |
| Domain | Agricultural water management / irrigation districts |
| Task shape | 08 · Rule replayed on history (30 weather seasons through a daily soil-water balance → P80 order) |
| Core method | Daily root-zone water balance with crop coefficients, replayed over historical weather years; empirical percentile of seasonal totals |
| Analytical stump | Irrigation need is a nonlinear, path-dependent function of daily weather (bucket fills and spills, deficits accumulate). Running the model on an "average year", or adding monthly percentiles, gives a different — wrong — P80 than replaying each year and taking the percentile of seasonal totals |
| Primary sources | CIMIS daily station data, FAO-56 crop coefficients, county crop acreage (USDA NASS / county crop report) |

## 1. The real-world situation

An irrigation district must place its **2026 surface-water order** before the season, sized so that in 4 out of 5 years
growers' irrigation needs are covered (P80). The district engineer computed crop water demand from long-term average daily
ETo and average rainfall, then added a 15% margin. In the last dry spring, the order ran out in July.

## 2. The decision (one deterministic recommendation)

**The 2026 water order in acre-feet (P80 of seasonal net irrigation requirement over the district's crop mix).**

Rules (district operations memo):

* Weather: daily reference ET (ETo) and precipitation at the district's CIMIS station for seasons 1994–2023 (each season
  1 March – 31 October). Missing or QC-flagged days are filled from the backup station on the same date.
* Crops and acreage: the four crops and irrigated acres in the folder; FAO-56 single crop coefficients with the stage
  lengths and Kc values given in the memo (linear interpolation in development and late stages).
* Daily soil-water balance per crop: root-zone available water 75 mm (bucket starts full on 1 March); rain adds to storage
  up to capacity (excess lost); crop ET = Kc × ETo removes storage; whenever depletion would exceed 50% of capacity,
  irrigate exactly enough to refill to capacity; irrigation efficiency 80% (delivered = applied ÷ 0.8).
* Seasonal requirement for a year = Σ crops (delivered depth × acres), converted to acre-feet.
* Order = P80 across the 30 seasonal requirements (inclusive linear-interpolation convention), rounded up to 100 AF.

## 3. Why capable analysts get it wrong

* "Average year" engineering is a long tradition; it treats the outcome as a function of average inputs, but bucket overflow
  and refill thresholds make the outcome nonlinear in daily weather.
* Monthly balances smear storms across days, overstating effective rain in wet months.
* Percentiles of monthly totals cannot be added to get a seasonal percentile.
* A flat margin on the mean is not a percentile.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `cimis_station_primary_daily_1994_2023.csv` | CSV | ~11k | California Irrigation Management Information System (CIMIS) | State of California public data (verify) | ETo, precipitation, QC flags |
| 2 | `cimis_station_backup_daily_1994_2023.csv` | CSV | ~11k | CIMIS | Same | Gap filling |
| 3 | `cimis_station_metadata.json` | JSON | 2 | CIMIS | Same | Station info |
| 4 | `cimis_qc_flags.pdf` | PDF | — | CIMIS | Same | Flag meanings |
| 5 | `fao56_crop_coefficients_extract.pdf` | PDF | — | FAO Irrigation and Drainage Paper 56 (cite) | FAO copyright (cite; quote tables used) | Kc and stage lengths |
| 6 | `crop_acreage_district.xlsx` | XLSX | ~4 crops | County crop report / USDA NASS Cropland Data Layer summary | Public | Acres by crop |
| 7 | `cropland_data_layer_district_counts.csv` | CSV | ~100 | USDA NASS CDL | Public domain | Acreage cross-check |
| 8 | `district_operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `engineer_average_year_calc.xlsx` | XLSX | ~250 | Task author | — | Average-year approach |
| 10 | `historical_deliveries_2014_2023.csv` | CSV | ~10 | District annual report (public) | Public | Sanity check |

## 5. Deterministic solution path

1. Assemble daily weather 1994–2023 with gap filling; build Kc(day) per crop.
2. For each season and crop, run the daily bucket model; record delivered depth.
3. Convert to acre-feet with acreage; sum crops per season (30 values).
4. P80 with the stated convention; round up.
5. Contrast: average-year run; monthly-step run; sum of monthly P80s; mean × 1.15.

## 6. Wrong paths (method errors, not misreadings)

**A — average-year model run.** Underestimates the P80 (and the mean) because storage dynamics are nonlinear.

**B — sum of monthly P80s.** Overstates; dry months rarely coincide every year.

**C — monthly time step.** Mis-states effective rain and refill timing.

**D — mean plus margin.** Not a percentile; may over- or under-shoot.

## 7. Why the stump is analytical, not semantic

The bucket model, coefficients, efficiency and percentile convention are fully specified. The error is summarizing
inputs before running a nonlinear model, or aggregating quantiles — analytical mistakes.

## 8. Draft task prompt (prose)

> Size our 2026 water order so it covers growers' needs in four years out of five, following the operations memo. Replay
> every season from 1994 to 2023 through the daily soil-water model for our crop mix using the CIMIS weather in the folder,
> and give me the order. Provide `season_replay.csv` (one row per season: rain, ETo, delivered acre-feet by crop and total),
> `requirement_distribution.png` showing the thirty seasonal totals as a sorted bar chart with the P80 and the engineer's
> average-year figure marked, and a one-page `water_order_memo.pdf` with the order, the median season, and the shortfall the
> average-year method would have left in the 80th-percentile season.

## 9. Deliverables

* `season_replay.csv` (30 rows), `requirement_distribution.png`, `water_order_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 30 seasonal totals (spot-check ~15), P80, order, median, average-year comparison, crop-level splits for 2–3 seasons.

## 11. Golden-output checklist

* Daily model per season; gap filling; Kc interpolation; efficiency; percentile of totals; rounding.

## 12. Build notes (scope tuning)

* Choose a station with both very dry and wet springs so the average-year approach differs from the P80 by > 10%.
* Publish a reference implementation output for one season to calibrate graders.
