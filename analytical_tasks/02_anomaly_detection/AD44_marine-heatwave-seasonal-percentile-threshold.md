# AD44 — Marine heatwave alerts for fish farms: "hot for August" is not "hot for the year"

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Aquaculture and fisheries operators' environmental alerting; any alert whose threshold must move with the season (latency by time of day, demand by month) |
| Domain | Ocean climate / aquaculture operations |
| Task shape | 17 · Periods around a change point (days of the 2022 season checked against a day-of-year climatological threshold; longest event; go/no-go on the emergency harvest plan and the biomass it brings forward) |
| Core method | Hobday et al. (2016) marine heatwave definition: day-of-year 90th percentile from a 30-year baseline with an 11-day window and 31-day smoothing; events = ≥ 5 consecutive days above threshold, gaps ≤ 2 days joined; intensity and duration metrics |
| Analytical stump | A single annual percentile (or a fixed temperature) flags every summer and never flags a winter heatwave, which is when stocking density and disease risk differ. Seasonal-percentile thresholds and duration/gap rules define the event; daily exceedances are not events |
| Primary sources | NOAA Optimum Interpolation Sea Surface Temperature v2.1 (OISST, daily 0.25°) |

## 1. The real-world situation

A salmon producer triggers an emergency harvest plan for a farm region when a marine heatwave of category II or worse lasts ≥ 15 days. Its
analyst flagged days when sea-surface temperature exceeded the 90th percentile of all daily values since 1982; every summer was a
"heatwave", and a long, intense spring event went unnoticed because spring temperatures never reach summer levels.

## 2. The decision (one deterministic recommendation)

**Whether the 2022 season at the farm-region grid cells triggers the emergency harvest plan, the event's start date and duration, and the
biomass (tonnes) brought forward under the plan's harvest schedule.**

Rules (environmental memo):

* Data: OISST daily SST for the 9 grid cells listed in the memo; region series = mean over cells.
* Baseline 1991–2020: for each day-of-year, climatological mean and 90th percentile pooled over an 11-day window centred on that day, then
  smoothed with a 31-day moving average (leap days handled per Hobday).
* Event: ≥ 5 consecutive days with SST > threshold; events separated by ≤ 2 days below threshold are joined.
* Category per day: (SST − climatology mean) ÷ (threshold − climatology mean): I < 2, II 2–3, III 3–4, IV ≥ 4 (memo convention: category of
  the event = maximum daily category).
* Trigger: an event in 2022 with category ≥ II and duration ≥ 15 days.
* Biomass brought forward: per `harvest_schedule.xlsx`, harvest of pens scheduled within 60 days after the trigger date is moved forward.

## 3. Why capable analysts get it wrong

* Annual percentiles are the simplest threshold and ignore the seasonal cycle.
* Duration and gap rules turn daily exceedances into events; without them, counts and durations are wrong.
* Category definitions are relative to the local seasonal spread, not absolute degrees.
* Baseline choice (30 years, window, smoothing) must follow the definition to be comparable.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `oisst_v2.1_farm_cells_1982_2022.nc` | NetCDF | ~15k days × 9 cells | NOAA NCEI OISST v2.1 | U.S. Gov public domain | Daily SST |
| 2 | `oisst_farm_cells_long.csv` | CSV | ~135k | Derived | Public domain | Tidy series |
| 3 | `farm_cells.json` | JSON | 9 | Task author | — | Grid cells |
| 4 | `hobday_2016_citation.pdf` | PDF | — | Hobday et al., Prog. Oceanogr. 2016 (cite) | Cite | Definition |
| 5 | `hobday_2018_categories_citation.pdf` | PDF | — | Hobday et al., Oceanography 2018 (cite) | Cite | Categories |
| 6 | `environmental_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `harvest_schedule.xlsx` | XLSX | ~40 pens | Task author | — | Biomass schedule |
| 8 | `analyst_annual_percentile_flags.csv` | CSV | ~1.5k | Task author | — | Naive flags |
| 9 | `climatology_check_values.json` | JSON | ~12 | Task author | — | Threshold check values for 12 days |
| 10 | `oisst_v2.1_readme.txt` | Text | — | NOAA | Public domain | Product notes |

## 5. Deterministic solution path

1. Build the region series; compute the day-of-year climatology and threshold per the definition.
2. Detect 2022 exceedances; form events with duration and gap rules; categories.
3. Apply the trigger; compute brought-forward biomass.
4. Contrast with annual-percentile flags.

## 6. Wrong paths (method errors, not misreadings)

**A — annual percentile threshold.** Summers flagged; spring event missed.

**B — no gap joining.** One event split into short pieces that fail duration.

**C — absolute degree categories.** Wrong severity.

**D — unsmoothed percentile.** Noisy threshold changes the start date.

## 7. Why the stump is analytical, not semantic

The definition is fully specified. The trap is using a non-seasonal threshold and treating daily exceedances as events.

## 8. Draft task prompt (prose)

> Did 2022 trigger our emergency harvest plan? Apply the marine heatwave definition in the environmental memo to the farm region's OISST series
> and tell me the event, its category and duration, and the biomass we would bring forward. Provide `events_2022.csv` (event: start, end,
> duration, max category, peak anomaly), `sst_vs_threshold.png` (2022 SST with climatology and threshold, events shaded), and a one-page
> `harvest_trigger.pdf`.

## 9. Deliverables

* `events_2022.csv`, `sst_vs_threshold.png`, `harvest_trigger.pdf`.

## 10. Where 25+ rubric criteria come from

* Threshold values for 12 check days; each 2022 event's start, end, duration and category; trigger; biomass; naive contrast.

## 11. Golden-output checklist

* Baseline period; window; smoothing; leap-day handling; event rules; categories; biomass.

## 12. Build notes (scope tuning)

* Choose a region with a documented 2022 off-season heatwave.
* Confirm the annual percentile method flags ≥ 60 summer days and misses the triggering event.
