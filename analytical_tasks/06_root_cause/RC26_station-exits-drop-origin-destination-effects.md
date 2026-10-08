# RC26 — Exits at a downtown station fell 15%: is something wrong at the station, or did its riders' home stations stop travelling?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Two-sided marketplace drops (a restaurant's orders fall because its delivery zone's demand fell vs because it lost share; a seller's sales fall because its buyers' regions shrank) |
| Domain | Public transport / urban mobility |
| Task shape | 12 · Drill-down to one leaf (station exits change → system-wide, origin-side and destination-specific effects from an origin–destination model → the origin corridor or the station itself) |
| Core method | Weighted two-way decomposition of origin–destination log changes: log(T_od,cur ÷ T_od,ref) = μ + a_o + b_d + e_od, weighted by reference trips; the destination effect b for the station measures its station-specific change relative to the network; the station's exit change is split into system (μ), origin mix (Σ weights × a_o), destination effect (b_d) and residual; drill into origin corridors via grouped residuals |
| Analytical stump | Comparing the station's exit change with the system's average blames the station when its riders come disproportionately from origins whose travel fell most (for example, suburban corridors where remote work persisted). The fair comparison holds origins fixed: did riders from each origin choose this station less than other destinations? Only the destination effect speaks to station-specific causes |
| Primary sources | BART (Bay Area Rapid Transit) hourly ridership by origin–destination pair, annual files |

## 1. The real-world situation

A downtown station's average weekday exits fell 15% between two autumn quarters while system exits fell 7%. Local business groups blamed station
conditions (escalator outages, cleanliness, safety perception) and asked for a station-improvement programme. Planners suspected that the station's
catchment — commuters from outer East Bay corridors — had cut office days more than other riders.

## 2. The decision (one deterministic recommendation)

**Whether to fund the station-improvement programme (fund only if the station's destination effect is ≤ −5% and its 95% interval excludes zero),
with the decomposition of the exit change and the origin corridor contributing most.**

Rules (planning memo):

* Data: BART hourly OD ridership files; weekdays (excluding federal holidays) in the memo's reference and current quarters; average weekday trips per
  OD pair.
* Pairs: origins ≠ destinations; pairs with < 20 average weekday trips in the reference quarter excluded from the model (kept in totals).
* Model: weighted least squares of y_od = log(T_cur ÷ T_ref) on origin and destination fixed effects with sum-to-zero constraints, weights =
  T_ref; μ = intercept.
* Station decomposition (station X as destination): Σ_o w_o y_oX with w_o = T_oX,ref ÷ Σ T_oX,ref, split into μ, Σ w_o a_o (origin mix), b_X
  (destination effect) and Σ w_o e_oX (residual). Convert log points to percentages for reporting.
* Interval for b_X: cluster-robust by origin.
* Drill-down: origin corridors (memo's grouping of stations); contribution = Σ over corridor origins of w_o (a_o + e_oX); name the corridor with the
  most negative contribution.

## 3. Why capable analysts get it wrong

* Station exits compared with the system average is the standard dashboard.
* Catchments differ: some stations draw from origins that changed much more.
* Station-specific causes should show up as riders from every origin choosing the station less.
* Small OD pairs produce noisy log changes.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `date-hour-soo-dest-<ref_year>.csv.gz` | CSV | ~10M | BART ridership reports (hourly OD) | BART open data terms (public; verify) | Reference trips |
| 2 | `date-hour-soo-dest-<cur_year>.csv.gz` | CSV | ~10M | Same | Same | Current trips |
| 3 | `station_info.csv` | CSV | ~50 | BART station list (GTFS stops) | BART GTFS licence (verify) | Station codes and lines |
| 4 | `federal_holidays.json` | JSON | ~20 | OPM federal holidays | Public domain | Weekday filter |
| 5 | `corridor_groups.csv` | CSV | ~50 | Task author | — | Station → corridor |
| 6 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2, station X, quarters |
| 7 | `business_group_letter.pdf` | PDF | — | Task author | — | The station-conditions claim |

## 5. Deterministic solution path

1. Filter weekdays and quarters; average weekday OD trips.
2. Exclude small pairs for the model; build y_od and weights.
3. Fit the weighted fixed-effects model; extract μ, a_o, b_d and residuals.
4. Decompose station X's change; interval for b_X; corridor contributions.
5. Decision; contrast with the business group's comparison.

## 6. Wrong paths (method errors, not misreadings)

**A — station vs system average.** The catchment effect is attributed to the station.

**B — unweighted model.** Small pairs dominate the fixed effects.

**C — destination totals only.** Without origins, the origin mix cannot be separated.

**D — weekends included.** Different travel purposes and catchments distort the comparison.

## 7. Why the stump is analytical, not semantic

Every quantity comes from OD counts with specified rules. The trap is a two-sided count analysed from one side.

## 8. Draft task prompt (prose)

> Business groups want money for the downtown station because its exits fell twice as much as the system. Use the planning memo's OD decomposition to
> tell me whether the station itself is the problem and, if not, where the decline came from. Provide `exit_decomposition.csv` (component: %),
> `od_effects_map.png`, and a one-page `station_programme_decision.pdf`.

## 9. Deliverables

* `exit_decomposition.csv` — system, origin mix, destination effect (with interval), residual; corridor contributions.
* `od_effects_map.png` — map of origin effects a_o with corridor contributions to station X.
* `station_programme_decision.pdf` — decision and why the station-vs-system comparison misleads.

## 10. Where 25+ rubric criteria come from

* Weekday filter and averaging (days counted per quarter): 2.
* Pairs modelled and excluded: 2.
* μ, b_X and its interval: 4.
* Decomposition components and closure: 5.
* Origin effects for the 8 largest origins of X: 8.
* Corridor contributions and the named corridor: 3.
* Decision and contrast: 3.

## 11. Golden-output checklist

* Holidays excluded; quarter windows exact.
* Weighted fixed effects with sum-to-zero constraints.
* Station decomposition with w_o weights; log-to-percent conversion.
* Cluster-robust interval; corridor grouping.

## 12. Build notes (scope tuning)

* Choose a station and quarters where the station's dominant corridors fell sharply; confirm that b_X is within ±5% or its interval includes zero
  while the raw station change is at least twice the system change.
