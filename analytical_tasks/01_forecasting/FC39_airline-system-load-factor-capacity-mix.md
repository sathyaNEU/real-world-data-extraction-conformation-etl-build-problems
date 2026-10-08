# FC39 — Next summer's load factor: forecast the parts under the new capacity plan, not the ratio's history

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Airline network planning and revenue-management targets (system load factor under a changing capacity mix) |
| Domain | Aviation / network planning |
| Task shape | 02 · Forecast across many periods (June–August monthly system load factors → one committed summer target) |
| Core method | Segment-group load factors forecast from same-month history, weighted by the planned seats in each group (ratio of sums), aggregated to the system |
| Analytical stump | A system load factor is a seat-weighted ratio; its history embeds last year's capacity mix. Trend-forecasting the ratio, or averaging segment load factors unweighted, ignores that the plan shifts seats toward groups with very different load factors |
| Primary sources | BTS T-100 Domestic Segment data (all carriers), BTS carrier and airport lookups |

## 1. The real-world situation

An airline sets a **summer system load factor target** that drives pricing and overbooking settings. The planner forecast June–August
load factor by extending the trend in the system ratio. The capacity plan for the coming summer, however, moves seats from short-haul
business markets (lower load factors) to long-haul leisure markets (higher), and adds regional flying in thin markets.

## 2. The decision (one deterministic recommendation)

**The committed summer target = the seat-weighted June–August system load factor under the capacity plan (one decimal).**

Rules (network planning memo):

* Data: T-100 Domestic Segment for the chosen carrier, 2018, 2019, 2022, 2023, 2024 (2020–2021 excluded).
* Segment groups: stage length (< 500, 500–1,499, ≥ 1,500 miles) × aircraft class (regional jet ≤ 76 seats, mainline) = 6 groups.
* Group load factor forecast for month m = Σ passengers ÷ Σ seats in month m over the last two eligible years (2023, 2024).
* Planned seats by group and month from `capacity_plan_summer_2025.csv`.
* Monthly system LF = Σ_g (forecast LF_g × planned seats_g) ÷ Σ_g planned seats_g. Summer target = Σ (LF × seats) over June–August ÷
  Σ seats.

## 3. Why capable analysts get it wrong

* Ratios are tracked as KPIs and forecast like any series; their history reflects past mix.
* Averaging group load factors without seat weights over-weights small groups.
* Using departures as weights ignores gauge differences.
* Pandemic years distort level and mix; the memo excludes them.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–5 | `T_T100D_SEGMENT_ALL_CARRIER_2018.csv`, `…2019`, `…2022`, `…2023`, `…2024` | CSV | 300k–450k each | BTS TranStats | U.S. Gov public domain | Segment seats/passengers |
| 6 | `L_AIRCRAFT_TYPE.csv` | CSV | ~600 | BTS | Public domain | Aircraft types |
| 7 | `aircraft_seat_classes.csv` | CSV | ~600 | Derived (typical seats by type) | Public domain | Regional vs mainline class |
| 8 | `L_UNIQUE_CARRIERS.csv` | CSV | ~1.7k | BTS | Public domain | Carrier codes |
| 9 | `t100_documentation.pdf` | PDF | — | BTS | Public domain | Field definitions |
| 10 | `capacity_plan_summer_2025.csv` | CSV | 18 | Task author (from published schedule changes) | — | Planned seats by group × month |
| 11 | `network_planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 12 | `planner_ratio_trend.xlsx` | XLSX | ~20 | Task author | — | Trend forecast |

## 5. Deterministic solution path

1. Filter the carrier; classify segments into groups; compute monthly group load factors for 2023–2024.
2. Combine with planned seats; monthly system LF; summer target.
3. Decompose the difference from last summer's actual into rate and mix contributions.
4. Contrast with the ratio trend and unweighted averages.

## 6. Wrong paths (method errors, not misreadings)

**A — trend on the system ratio.** Ignores mix shift; target off.

**B — unweighted group average.** Over-weights small groups.

**C — departure weights.** Gauge ignored.

**D — including 2020–2021.** Distorted bases.

## 7. Why the stump is analytical, not semantic

Load factor and the plan are defined; the trap is forecasting an aggregate ratio without accounting for its changing weights.

## 8. Draft task prompt (prose)

> Set next summer's system load factor target from the capacity plan, as the network planning memo describes: forecast load factor
> for each segment group and weight by planned seats. Provide `summer_lf_forecast.csv` (month × group: forecast LF, planned seats,
> contribution), `mix_vs_rate.png` decomposing the change from last summer, and a one-page `lf_target.pdf` with the target and how the
> trend method compares.

## 9. Deliverables

* `summer_lf_forecast.csv`, `mix_vs_rate.png`, `lf_target.pdf`.

## 10. Where 25+ rubric criteria come from

* 18 group-month LFs; 3 monthly system LFs; target; mix and rate contributions; trend contrast.

## 11. Golden-output checklist

* Correct grouping; ratio-of-sums; plan weights; exclusions; decomposition.

## 12. Build notes (scope tuning)

* Build the capacity plan from public schedule announcements so the mix shift is realistic; confirm ≥ 1.5-point difference from the
  trend method.
* Document the seat-class mapping for aircraft types.
