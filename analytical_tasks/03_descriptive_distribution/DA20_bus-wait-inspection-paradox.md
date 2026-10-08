# DA20 — "A bus every 10 minutes": riders who arrive at random wait longer than half the headway

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Ride-hail and delivery ETA analytics (experienced wait versus average dispatch interval); queue-age metrics; any interval metric experienced by randomly arriving users |
| Domain | Public transit operations |
| Task shape | 01 · Ranked list under a cap (6 routes for a headway-management intervention) |
| Core method | Observed headways from departure times at timepoints; expected wait for randomly arriving passengers = E[H²] ÷ (2 E[H]) = (E[H] ÷ 2)(1 + CV²); excess wait = expected wait − scheduled headway ÷ 2; ranking by riders × excess wait |
| Analytical stump | Average headway halves to the wait only when buses are perfectly regular. Passengers are more likely to arrive during long gaps (length-biased sampling), so bunching raises experienced waits even when the average headway meets the schedule. Ranking routes by average headway or on-time percentage misses the bunched ones |
| Primary sources | MBTA (Massachusetts Bay Transportation Authority) bus arrival-departure times open data; MBTA ridership by route |

## 1. The real-world situation

A transit agency can deploy headway-management supervisors on **6** high-frequency bus routes. The service report ranked routes by the gap
between average observed headway and scheduled headway. Rider surveys described long waits on routes that looked fine on that measure, where
buses ran in pairs.

## 2. The decision (one deterministic recommendation)

**The 6 routes selected, ranked by weekday peak passenger-hours of excess wait, and the 7th.**

Rules (service memo):

* Data: MBTA bus arrival-departure records for the quarter in the memo; weekday peak periods (07:00–09:00, 16:00–18:30); high-frequency
  routes (scheduled headway ≤ 15 min in peaks).
* Headways: at each route-direction timepoint, consecutive actual departure times; drop headways > 3× scheduled (service gaps flagged
  separately per memo) — retained in a separate count.
* Expected wait per timepoint-period: E[H²] ÷ (2E[H]); scheduled wait = scheduled headway ÷ 2; excess = expected − scheduled.
* Route excess = boardings-weighted mean of timepoint excess (boardings per timepoint from the ridership file).
* Passenger-hours = route excess (hours) × peak weekday boardings × weekdays in quarter.
* Rank by passenger-hours; top 6; report #7.

## 3. Why capable analysts get it wrong

* Average headway is the operational headline.
* The waiting time of a random arrival depends on headway variance.
* Bunching leaves the mean unchanged while raising experienced waits.
* Ranking by minutes per rider ignores how many riders are affected.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–3 | `MBTA-Bus-Arrival-Departure-Times_<yyyy>-<mm>.csv` (3 months) | CSV | ~4–6M each | MBTA Open Data Portal | MBTA open data terms (public; verify) | Scheduled and actual times at timepoints |
| 4 | `MBTA_Bus_Ridership_by_Trip_Season_Route_Line_and_Stop.csv` | CSV | ~1M | MBTA Open Data Portal | Same | Boardings by stop/time period |
| 5 | `gtfs_<date>.zip` | GTFS (CSV) | ~20 files | MBTA | Same | Stops, timepoints, scheduled headways |
| 6 | `data_dictionary_arrival_departure.pdf` | PDF | — | MBTA | Same | Fields |
| 7 | `service_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `service_report_headway_ranking.xlsx` | XLSX | ~25 | Task author | — | Current ranking |
| 9 | `wait_time_formula_note.pdf` | PDF | — | Cite (Osuna & Newell; transit capacity manual) | Cite | Formula |
| 10 | `peak_headways.parquet` | Parquet | ~600k | Derived | Same | Convenience |

## 5. Deterministic solution path

1. Filter periods and routes; compute headways at timepoints; apply the gap rule.
2. Expected and scheduled waits; excess per timepoint-period.
3. Boardings-weighted route excess; passenger-hours; rank; top 6 + #7.
4. Contrast with the service report.

## 6. Wrong paths (method errors, not misreadings)

**A — average headway versus schedule.** Bunching invisible.

**B — wait = average headway ÷ 2.** Inspection paradox ignored.

**C — minutes per rider ranking.** Ignores volume.

**D — dropping long gaps silently.** Understates experienced waits; the memo counts them separately.

## 7. Why the stump is analytical, not semantic

The headway and wait formulas are specified. The trap is length-biased sampling of intervals by random arrivals.

## 8. Draft task prompt (prose)

> Which six routes need headway supervisors? Use actual departures and the experienced-wait formula in the service memo, weighted by riders.
> Provide `route_excess_wait.csv` (route: mean headway, CV, expected wait, scheduled wait, excess, passenger-hours, rank), `headway_cv_chart.png`,
> and a one-page `supervisor_deployment.pdf`.

## 9. Deliverables

* `route_excess_wait.csv`, `headway_cv_chart.png`, `supervisor_deployment.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 routes + #7; CV and excess for 8 routes; passenger-hours; gap counts; contrast.

## 11. Golden-output checklist

* Peak filter; timepoint headways; gap rule; E[H²]/(2E[H]); weighting; ranking.

## 12. Build notes (scope tuning)

* Confirm at least two routes with on-schedule mean headways but CV > 0.6 enter the top six.
