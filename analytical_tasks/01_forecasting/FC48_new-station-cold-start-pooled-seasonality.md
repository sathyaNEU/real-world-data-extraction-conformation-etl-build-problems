# FC48 — Forecasting summer demand at stations that opened in winter: borrow the seasonality you haven't seen

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Cold-start forecasting for new stores, lockers, chargers or micro-fulfilment sites with only weeks of history |
| Domain | Micromobility / network expansion operations |
| Task shape | 10 · Scorecard against thresholds (new station × summer peak forecast vs dock capacity → expand / no) |
| Core method | Pooled (global) seasonal index from mature stations of the same type, applied to each new station's level estimated in its first weeks (deseasonalized), with partial pooling of the level toward its neighbourhood mean |
| Analytical stump | A station opened in December has only seen winter. Its own trend (or its winter average) says nothing about July; scaling its few weeks by nothing — or extrapolating a short upward trend caused by the season turning — mis-forecasts. Seasonality must come from mature peers, and the level must be deseasonalized before projection |
| Primary sources | Lyft Bay Wheels trip data, Bay Wheels station information (GBFS) |

## 1. The real-world situation

A bike-share operator opened a batch of new stations in winter. Before summer it must decide which need extra docks: a station whose
forecast July average weekday peak-hour departures exceed 80% of its dock count gets an expansion. The analyst forecast each new
station from its own first eight weeks (all in winter) with a linear trend; some showed explosive growth (spring was arriving), others
almost none.

## 2. The decision (one deterministic recommendation)

**Which new stations get dock expansions for July (station-level go/no-go) and how many?**

Rules (expansion memo):

* New stations: first trip between 1 December and 31 January of the chosen winter; history = their first 8 complete weeks.
* Mature peers: stations open ≥ 24 months before the new stations' opening, same zone group (in the memo).
* Seasonal index s(w) per ISO week = mature peers' weekday peak-hour (08:00–08:59) departures in week w ÷ their annual weekly mean,
  averaged over the two prior years.
* New station level L = mean over its 8 weeks of (weekday peak-hour departures ÷ s(w)); partial pooling: L* = (n·L + 4·Z) ÷ (n + 4),
  n = 8, Z = mean L of new stations in the same zone group.
* July forecast = L* × mean s(w) over July weeks. Expand if forecast > 0.8 × docks (from station information).

## 3. Why capable analysts get it wrong

* Station-level models are fit on each station's own history by default.
* Short winter histories contain a seasonal upswing that looks like a growth trend.
* Raw winter levels must be deseasonalized before projecting to summer.
* Without pooling, a few unusual weeks set the level for a station with tiny counts.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–24 | `YYYYMM-baywheels-tripdata.csv` (24 months) | CSV | 100k–250k each | Lyft Bay Wheels system data | Bay Wheels data license agreement (permissive; verify) | Trips with station IDs, start times |
| 25 | `station_information.json` (GBFS snapshot) | JSON | ~600 | Bay Wheels GBFS | Same | Capacity (docks), coordinates |
| 26 | `station_first_trip_dates.csv` | CSV | ~600 | Derived | Same | Opening dates |
| 27 | `zone_groups.geojson` | GeoJSON | ~10 | Task author | — | Peer groups |
| 28 | `us_federal_holidays.json` | JSON | ~30 | OPM | Public domain | Weekday filter |
| 29 | `expansion_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 30 | `analyst_trend_forecasts.xlsx` | XLSX | ~30 | Task author | — | Own-history trends |

## 5. Deterministic solution path

1. Identify new and mature stations; compute weekday peak-hour departures by station-week.
2. Build the peer seasonal index; deseasonalize new stations' weeks; pooled levels.
3. July forecasts; compare with 0.8 × docks; decisions.
4. Contrast with own-trend forecasts; validate against actual July if available.

## 6. Wrong paths (method errors, not misreadings)

**A — own linear trend.** Spring upswing extrapolated; over-expansion.

**B — winter level as July forecast.** Under-expansion.

**C — no pooling.** Noise-driven decisions.

**D — all-hours average.** Not the peak hour.

## 7. Why the stump is analytical, not semantic

All definitions are explicit. The trap is cold-start modelling — what information a short history can and cannot carry.

## 8. Draft task prompt (prose)

> Decide which of the winter-opened stations need extra docks for July, following the expansion memo: build a seasonal index from mature
> stations, deseasonalize each new station's first weeks, pool toward its zone, and compare the July peak forecast with 80% of docks.
> Provide `new_station_scorecard.csv` (station: weeks of history, raw and pooled level, July forecast, docks, decision),
> `seasonal_index.png`, and a one-page `expansion_decision.pdf` with the count and the stations that differ from the trend method.

## 9. Deliverables

* `new_station_scorecard.csv`, `seasonal_index.png`, `expansion_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* Decisions for ~30 new stations; seasonal index for July weeks; pooled levels for 6 spot-check stations; count; trend contrast.

## 11. Golden-output checklist

* Correct new/mature sets; peer index; deseasonalization; pooling formula; threshold.

## 12. Build notes (scope tuning)

* Choose a winter with ≥ 25 new stations; confirm trend and pooled methods disagree on ≥ 6 stations.
* Archive the GBFS snapshot used for capacities.
