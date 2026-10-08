# FC50 — Planning for the busy shift: emergency call counts vary more than Poisson says

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Percentile-based staffing from count forecasts (contact centres, trust & safety queues, field service) where demand is over-dispersed |
| Domain | Fire & emergency medical services planning |
| Task shape | 07 · Grid of cells (area × 4-hour block → P90 call count and units required) |
| Core method | Count forecasts with negative-binomial predictive distributions (dispersion estimated by method of moments per cell), P90 of counts, conversion to units via service time |
| Analytical stump | Treating counts as Poisson fixes the variance equal to the mean; real call counts vary with weather, events and heat, so P90 under Poisson is too low — the busiest shifts are under-staffed. Normal approximations on small counts add further error |
| Primary sources | Seattle Real Time Fire 911 Calls (Seattle Open Data), Seattle Fire Department station areas (GIS) |

## 1. The real-world situation

A fire department staffs medic units by area and 4-hour block so that 9 shifts out of 10 have enough units. The analyst forecast mean
calls per cell and used Poisson 90th percentiles; on hot weekends and event nights units ran out repeatedly.

## 2. The decision (one deterministic recommendation)

**Units required for each area × 4-hour block next summer (and the total unit-blocks per week).**

Rules (planning memo):

* Calls: medical response types listed in the memo, June–August of the last three years; assigned to 5 planning areas by point-in-
  polygon on station areas; blocks 00–04, 04–08, …, 20–24 local time; weekdays and weekends separate (so 5 × 6 × 2 = 60 cells).
* For each cell, daily counts over the 3 summers give mean μ and variance v; dispersion k = μ² ÷ (v − μ) if v > μ, else Poisson.
* P90 = 90th percentile of the negative binomial with mean μ and dispersion k (or Poisson) — smallest count with CDF ≥ 0.9.
* Units = ceil(P90 × 1.2 hours mean unit time per call ÷ 4 hours).
* Weekly unit-blocks = Σ over cells (units × number of such blocks per week).

## 3. Why capable analysts get it wrong

* Poisson is the default model for counts; its variance is often far smaller than observed.
* Mixing weekdays and weekends inflates variance in a way that looks like overdispersion but is structure — the memo separates them.
* Normal approximations at small means misplace percentiles.
* Planning to the mean leaves half the shifts short.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Seattle_Real_Time_Fire_911_Calls.csv` | CSV | ~2M | Seattle Open Data | City of Seattle open data terms (public) | Calls with type, time, location |
| 2 | `fire_station_areas.geojson` | GeoJSON | ~35 | Seattle GIS open data | Same | Station areas |
| 3 | `planning_area_mapping.csv` | CSV | ~35 | Task author | — | Station area → planning area |
| 4 | `call_type_list.json` | JSON | ~40 | Task author | — | Medical response types |
| 5 | `daily_cell_counts.parquet` | Parquet | ~55k | Derived | Same | Daily counts per cell |
| 6 | `noaa_seattle_daily_tmax.csv` | CSV | ~1k | NOAA NCEI | Public domain | Heat context |
| 7 | `seattle_fire_annual_report_extract.pdf` | PDF | — | Seattle Fire Department | Public | Unit time context |
| 8 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `analyst_poisson_staffing.xlsx` | XLSX | 60 | Task author | — | Poisson P90 staffing |
| 10 | `negative_binomial_reference.pdf` (citation) | PDF | — | Cite | Cite | Distribution |

## 5. Deterministic solution path

1. Filter call types and summers; geocode to areas; build daily counts per cell.
2. μ, v, k per cell; NB or Poisson P90; units; weekly unit-blocks.
3. Contrast with Poisson staffing; show shortfall frequency in back-test.

## 6. Wrong paths (method errors, not misreadings)

**A — Poisson P90.** Under-staffs high-variance cells.

**B — weekdays and weekends pooled.** Wrong dispersion and means.

**C — normal approximation.** Wrong percentiles at small means.

**D — staffing at the mean.** Shortfalls half the time.

## 7. Why the stump is analytical, not semantic

Cells, filters and the conversion are defined. The trap is the variance assumption of the count model.

## 8. Draft task prompt (prose)

> Set next summer's medic staffing by area and 4-hour block so nine shifts in ten are covered, following the planning memo. Provide
> `staffing_grid.csv` (cell: μ, variance, dispersion, P90, units; Poisson P90 and units for comparison), `variance_vs_mean.png` (cells'
> variance against mean with the Poisson line), and a one-page `staffing_memo.pdf` with the weekly unit-blocks and the cells the Poisson
> plan under-staffs.

## 9. Deliverables

* `staffing_grid.csv`, `variance_vs_mean.png`, `staffing_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 60 cells (spot-check 25 for P90/units); weekly unit-blocks; under-staffed cells under Poisson.

## 11. Golden-output checklist

* Filters; geocoding; separate day types; moment dispersion; NB percentile; ceiling; totals.

## 12. Build notes (scope tuning)

* Confirm a majority of cells show v > μ; choose planning areas so cells have mean ≥ 2 calls per block.
* Document the geocoding of calls without coordinates.
