# FC42 — Ambulances needed by hour: busy units peak hours after calls peak

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Time-varying capacity planning where work outlasts arrivals (support queues, warehouse pick waves, compute jobs, field service) |
| Domain | Emergency medical services / public safety operations |
| Task shape | 06 · Sequenced schedule under capacity (8-hour tour start pattern covering the hour-of-week requirement, limited start slots) |
| Core method | Infinite-server offered load: units in service at each minute reconstructed from assignment-to-close intervals; hour-of-week P90 of busy units; tour-start scheduling to cover requirements |
| Analytical stump | Staffing proportional to call arrivals per hour assumes calls finish within the hour. With 60–90-minute job durations (hospital turnaround), occupancy peaks later and stays high into the evening; arrival-based staffing is short at the true peak and idle in the morning |
| Primary sources | NYC EMS Incident Dispatch Data (NYC Open Data) |

## 1. The real-world situation

An EMS agency in one borough sets ambulance **tour starts** (8-hour shifts) for next quarter. The planner forecast calls per hour of
the week and staffed units in proportion, peaking around noon. Field supervisors reported that the real crunch — units all busy,
calls holding — came in the late afternoon and evening.

## 2. The decision (one deterministic recommendation)

**The weekly tour-start schedule (number of tours starting at each allowed start hour) that covers the hour-of-week requirement with
the fewest tours.**

Rules (operations memo):

* Incidents in the borough from the last 52 weeks before the origin with a valid first-assignment time and a close time; busy
  interval = first assignment → incident close (capped at 6 hours).
* Busy units at each minute = number of open intervals; for each hour of the week take the maximum minute value in that hour on each
  of the 52 weeks; requirement R(h) = P90 across weeks (inclusive interpolation), rounded up.
* Tours are 8 hours; allowed start hours: 00, 04, 07, 10, 12, 15, 18, 20 (every day). Choose non-negative integer starts per day and
  start hour to cover R(h) for all 168 hours with the minimum total tours (integer program; ties → fewer late-night starts, then
  earlier starts).

## 3. Why capable analysts get it wrong

* Calls per hour are the familiar forecast; occupancy (work in progress) is what consumes units.
* Occupancy is a convolution of arrivals with service durations; its peak lags the arrival peak by about one mean duration.
* Average busy units understate the hourly peak minute; requirements need a within-hour maximum and a weekly percentile.
* Covering hourly requirements with fixed-length tours is a set-covering problem, not a proportional split.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `EMS_Incident_Dispatch_Data.csv` (borough, last 2 years) | CSV | 1–1.5M | NYC Open Data (FDNY EMS) | NYC open data terms | Incident timestamps |
| 2 | `EMS_Incident_Dispatch_Data_dictionary.xlsx` | XLSX | — | NYC Open Data | Same | Field definitions |
| 3 | `busy_units_by_minute.parquet` | Parquet | ~525k minutes | Derived | Same | Occupancy series |
| 4 | `hour_of_week_requirements.csv` | CSV | 168 | Derived | — | Requirement profile |
| 5 | `fdny_ems_response_time_reports.pdf` | PDF | — | FDNY public reports | Public | Context |
| 6 | `nyc_holidays.json` | JSON | ~20 | Public | Public | Context |
| 7 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `planner_arrival_based_tours.xlsx` | XLSX | ~56 | Task author | — | Arrival-proportional schedule |
| 9 | `tour_rules.json` | JSON | — | Task author | — | Allowed starts, tour length |
| 10 | `ilp_reference_solution_format.csv` | CSV | — | Task author | — | Output layout |

## 5. Deterministic solution path

1. Build busy intervals; count open intervals per minute; hourly maxima per week; P90 by hour of week.
2. Formulate and solve the covering integer program; apply tie-breaks.
3. Compare coverage of the arrival-based schedule against R(h).

## 6. Wrong paths (method errors, not misreadings)

**A — arrivals-proportional staffing.** Under-covers late afternoon/evening.

**B — mean busy units.** Under-covers peaks.

**C — proportional tour allocation.** Infeasible or wasteful coverage.

**D — no cap on long intervals.** A few stuck incidents inflate occupancy.

## 7. Why the stump is analytical, not semantic

Intervals, percentile and scheduling rules are defined. The trap is modelling capacity on arrivals rather than on work in progress —
a queueing insight.

## 8. Draft task prompt (prose)

> Build next quarter's ambulance tour-start schedule for the borough the way the operations memo describes: measure how many units
> are actually busy minute by minute, set each hour's requirement at the 90th-percentile week, and cover it with the fewest 8-hour
> tours. Provide `tour_schedule.csv` (day × start hour: tours), `occupancy_vs_arrivals.png` (hour-of-week profiles of calls and busy
> units with the requirement line), and a one-page `tour_memo.pdf` with the total tours and the hours the planner's schedule leaves
> uncovered.

## 9. Deliverables

* `tour_schedule.csv`, `occupancy_vs_arrivals.png`, `tour_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* Requirements for 168 hours (spot-check 20); tours per start slot (56); total tours; uncovered hours of the planner's schedule.

## 11. Golden-output checklist

* Correct intervals and cap; within-hour max; P90; ILP optimum with tie-breaks.

## 12. Build notes (scope tuning)

* Publish the reference ILP solution and solver settings; confirm the arrival-based schedule leaves ≥ 15 hours uncovered.
* Document how incidents without close times are handled.
