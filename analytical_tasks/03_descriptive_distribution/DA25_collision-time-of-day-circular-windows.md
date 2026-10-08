# DA25 — The worst three hours: when the window crosses midnight, the arithmetic mean of clock time lies

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Choosing deploy or maintenance windows (lowest-traffic hours) and staffing peaks on 24-hour cycles; any time-of-day or day-of-year summary |
| Domain | Road safety / enforcement operations |
| Task shape | 01 · Ranked list under a cap (the 3-hour enforcement window for each of 8 police force areas, ranked by share of serious and fatal collisions covered; the 3 forces receiving extra night patrols) |
| Core method | Circular statistics on time of day: circular mean and resultant length; maximum-coverage 3-hour window found by a wrap-around sliding window over 1,440 minutes; comparisons with linear mean and linear windows that cannot cross midnight |
| Analytical stump | Averaging clock times linearly puts the "average" of 23:00 and 01:00 at noon; windows restricted to 00:00–24:00 cannot cover 22:30–01:30. Night-time collision peaks are split across midnight, so linear methods undercount their concentration and misplace the window |
| Primary sources | UK Department for Transport STATS19 road safety data (collisions) |

## 1. The real-world situation

A roads-policing unit assigns a 3-hour targeted patrol window in each force area, and extra night patrols to the three areas where the best
window covers the largest share of serious and fatal collisions. The analyst reported the "average collision time" per area and chose
windows centred on it, which placed several windows mid-afternoon in areas known for late-night crashes.

## 2. The decision (one deterministic recommendation)

**For each of 8 force areas, the 3-hour window (start time to the minute) maximising coverage of serious and fatal collisions; and the 3 areas
with the highest coverage share whose window includes any time between 22:00 and 04:00.**

Rules (operations memo):

* Data: STATS19 collisions for the 5 years in the memo; severity serious or fatal (adjusted severity where provided per memo); police force
  codes for the 8 areas.
* Time: collision time (HH:MM) to minutes after midnight.
* Coverage window: for each start minute s (0–1439), count collisions with time in [s, s + 180) modulo 1440; choose the s with maximum count
  (ties → earliest s).
* Coverage share = count ÷ total collisions in the area.
* Circular mean time and resultant length R̄ reported per area (angles θ = 2π × minute ÷ 1440).
* Night-patrol areas: among areas whose window intersects 22:00–04:00, the 3 with the highest coverage share.

## 3. Why capable analysts get it wrong

* Linear means and histograms with a midnight edge are the default.
* Peaks spanning midnight are split across the ends of a linear axis.
* Window searches must wrap around.
* Severity adjustments changed over time; the memo specifies which field to use.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `dft-road-casualty-statistics-collision-<years>.csv` | CSV | ~500k (5 years) | DfT STATS19 | Open Government Licence v3 | Collisions with time, severity, police force |
| 2 | `dft-road-casualty-statistics-vehicle-<years>.csv` | CSV | ~900k | DfT | OGL | Context |
| 3 | `dft-road-casualty-statistics-casualty-<years>.csv` | CSV | ~650k | DfT | OGL | Context |
| 4 | `stats19_guidance_and_variable_lookup.xlsx` | XLSX | — | DfT | OGL | Codes, adjusted severity |
| 5 | `force_areas_in_scope.json` | JSON | 8 | Task author | — | Areas |
| 6 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `analyst_average_time_windows.xlsx` | XLSX | 8 | Task author | — | Naive windows |
| 8 | `circular_statistics_reference.pdf` | PDF | — | Fisher, Statistical Analysis of Circular Data (cite) | Cite | Method |
| 9 | `collisions_minutes.parquet` | Parquet | ~60k | Derived | OGL | Convenience |

## 5. Deterministic solution path

1. Filter years, severity and areas; convert times.
2. Wrap-around window search per area; coverage shares.
3. Circular means and R̄.
4. Night-patrol selection; contrast with average-time windows.

## 6. Wrong paths (method errors, not misreadings)

**A — window centred on the linear mean.** Misplaced windows.

**B — linear windows only.** Midnight-spanning peaks missed.

**C — hourly bins.** Window start limited to the hour; coverage lower.

**D — unadjusted severity when the memo specifies adjusted.** Different collision set.

## 7. Why the stump is analytical, not semantic

Time conversion and the search rule are specified. The trap is treating a circular variable as linear.

## 8. Draft task prompt (prose)

> Set each force area's 3-hour targeted patrol window and pick the three areas for extra night patrols, following the operations memo. Provide
> `patrol_windows.csv` (area: window start/end, coverage, share, circular mean, R̄, naive window and its coverage), `clock_rose.png` (rose plots
> per area with windows), and a one-page `patrol_plan.pdf`.

## 9. Deliverables

* `patrol_windows.csv`, `clock_rose.png`, `patrol_plan.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 areas × (window start, share, circular mean) = 24; night selection; naive contrasts.

## 11. Golden-output checklist

* Severity field; minute conversion; wrap-around search; tie rule; circular stats; selection.

## 12. Build notes (scope tuning)

* Choose areas including at least three with night peaks spanning midnight.
