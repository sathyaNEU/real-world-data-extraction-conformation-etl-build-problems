# FC30 — Platform crowding after hybrid work: the "average weekday" no longer exists

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Office-occupancy and transit demand planning after hybrid work (Tuesday–Thursday peaks at offices, campuses and transit hubs) |
| Domain | Urban transit operations / station staffing |
| Task shape | 10 · Scorecard against thresholds (station × day-type peak forecast vs crowding threshold → deploy / no) |
| Core method | Day-type-specific (Mon, Tue–Thu, Fri) peak-hour forecasts from recent same-day-type observations, recovery growth estimated on matching day types, threshold tests per station |
| Analytical stump | Pooling Monday–Friday into one weekday profile averages away the Tuesday–Thursday concentration of commuting; peak-day crowding is under-forecast exactly where it matters. Year-over-year growth measured on pooled weekdays also mixes changing day-of-week shares |
| Primary sources | MTA Subway Hourly Ridership (NY Open Data), MTA daily ridership |

## 1. The real-world situation

A transit agency deploys platform conductors at stations whose **morning peak hour** entries are forecast to exceed a crowding
threshold next spring. The planning analyst forecast each station's average weekday 8–9 a.m. entries and found few stations over
threshold. Station managers reported dangerous crowding on Tuesdays through Thursdays at several stations not on the list.

## 2. The decision (one deterministic recommendation)

**Which stations get conductors on which day types for March 2026?** (Station × day-type go/no-go; headline = number of stations
needing Tue–Thu deployment.)

Rules (operations planning memo):

* Data: hourly entries (ridership) by station complex, all fare classes, from February 2022 onward.
* Peak hour: 08:00–08:59 entries. Day types: Monday, Tue–Thu, Friday (holidays and the week between Christmas and New Year
  excluded).
* Base level for a station × day type = mean peak-hour entries over the last 8 eligible weeks before the forecast origin
  (Tue–Thu: mean over the 24 eligible days).
* Growth = (same day type, same 8 calendar weeks of the latest year) ÷ (same weeks one year earlier), computed per station × day
  type and capped to [0.95, 1.10].
* Forecast = base × growth. Deploy if forecast ≥ the station's threshold in `station_thresholds.csv`.

## 3. Why capable analysts get it wrong

* The pre-pandemic habit of a single weekday profile is embedded in planning tools.
* Mondays and Fridays are now much lighter; pooling them with Tue–Thu lowers the peak-day forecast by 10–20%.
* Growth rates computed on pooled weekdays move with changing day-of-week mix, not with demand.
* Monthly averages include holidays and dilute peaks.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `MTA_Subway_Hourly_Ridership_2024.csv` (peak-hour extract) | CSV | ~5–10M | NY Open Data (MTA) | NY Open Data terms (public) | Hourly entries |
| 2 | `MTA_Subway_Hourly_Ridership_2025.csv` (to origin) | CSV | ~5–10M | Same | Same | Recent weeks |
| 3 | `MTA_Daily_Ridership_Data.csv` | CSV | ~1.5k | NY Open Data | Same | System totals check |
| 4 | `station_complexes.csv` | CSV | ~430 | MTA | Same | Station names, boroughs |
| 5 | `station_thresholds.csv` | CSV | ~60 | Task author (from public platform-capacity studies) | — | Crowding thresholds |
| 6 | `nyc_public_holidays_2024_2026.json` | JSON | ~40 | Public | Public | Exclusions |
| 7 | `hourly_ridership_data_dictionary.pdf` | PDF | — | MTA / NY Open Data | Same | Field meanings |
| 8 | `operations_planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `analyst_weekday_forecast.xlsx` | XLSX | ~60 | Task author | — | Pooled-weekday forecast |
| 10 | `station_peak_hour_long.parquet` | Parquet | ~500k | Derived | Same | Station × day peak series |

## 5. Deterministic solution path

1. Extract 08:00 entries per station-day; tag day types; drop excluded dates.
2. Compute base levels and capped growth per station × day type; forecast.
3. Compare with thresholds; produce the deployment grid.
4. Contrast with pooled-weekday forecasts.

## 6. Wrong paths (method errors, not misreadings)

**A — pooled weekdays.** Under-forecasts Tue–Thu; misses deployments.

**B — growth on pooled days.** Mixes mix-change with demand change.

**C — monthly averages incl. holidays.** Dilutes peaks.

**D — all hours averaged.** Not the peak hour.

## 7. Why the stump is analytical, not semantic

Definitions are explicit. The trap is aggregating heterogeneous days into one profile — an aggregation-bias error in forecasting.

## 8. Draft task prompt (prose)

> Decide where we need platform conductors next March, by station and day type, using the operations memo: forecast each station's
> 8 a.m. peak hour separately for Mondays, Tuesday–Thursday and Fridays and compare with the crowding thresholds. Provide
> `deployment_grid.csv` (station × day type: base, growth, forecast, threshold, deploy), `peak_by_daytype.png` for the ten busiest
> stations, and a one-page `deployment_memo.pdf` with the stations added versus the pooled-weekday analysis.

## 9. Deliverables

* `deployment_grid.csv`, `peak_by_daytype.png`, `deployment_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* ~60 stations × 3 day types decisions (spot-check 30); count of Tue–Thu deployments; pooled-weekday contrast.

## 11. Golden-output checklist

* Correct day types and exclusions; base windows; capped growth; threshold tests.

## 12. Build notes (scope tuning)

* Select the ~60 candidate stations near thresholds; confirm ≥ 8 stations flip between pooled and day-type methods.
* Document the extraction query (08:00 hour only) to keep files manageable.
