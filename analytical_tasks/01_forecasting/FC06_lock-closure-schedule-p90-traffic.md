# FC06 — Scheduling river lock closures: plan against the bad weeks, not the average week

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Scheduling maintenance windows against tail demand (network and data-centre maintenance windows, warehouse system cutovers, release freezes) |
| Domain | Inland waterways / freight logistics / infrastructure maintenance |
| Task shape | 06 · Sequenced schedule under capacity (four closures, crew limit, blackout, one dependency) |
| Core method | Weekly traffic quantile forecasts from multi-year history (week-of-year P90 of tonnage), constraint-feasible sequencing that minimizes exposed traffic, quantiles of window sums computed on the sums |
| Analytical stump | Closures must avoid weeks whose *high-percentile* traffic is large, and a 2-week closure's exposure is the P90 of the 2-week sum — not the sum of two weekly P90s, and not mean traffic. Harvest-season volatility moves the optimal windows |
| Primary sources | USACE Lock Performance Monitoring System (LPMS) / Corps Locks public data, USACE Waterborne Commerce statistics |

## 1. The real-world situation

A Corps of Engineers district must schedule **four two-week maintenance closures** at four locks on one river segment
next year. When a lock is closed, tows queue or divert; the district's rule is to schedule closures where the traffic at
risk is lowest in a bad year, because shippers' contracts are written for bad years. Planners averaged weekly tonnage over
ten years and picked the quietest average weeks — two of which sit at the start of harvest season, when tonnage swings
wildly from year to year.

## 2. The decision (one deterministic recommendation)

**The closure schedule: the start week of each of the four closures.**

Rules (district maintenance memo):

* Traffic exposure of a closure at lock k starting in ISO week w = the 90th percentile, across 2014–2023, of that lock's
  total tonnage in weeks w and w+1 (sum first, then the percentile; inclusive linear-interpolation convention).
* Constraints: one dive/maintenance crew → closures cannot overlap and need ≥ 1 week between them; blackout weeks 36–47
  (harvest) and weeks 1–8 (ice) are not allowed; lock B's closure must finish before lock C's starts (shared equipment
  barge moves downstream).
* Objective: minimize the sum of the four closures' exposures. Ties: earlier start weeks first.
* Weeks with zero recorded traffic because the lock was already closed are excluded from that lock's history for that
  week-pair (reported as missing, not zero).

## 3. Why capable analysts get it wrong

* Average weekly tonnage is the standard planning view; it hides that some quiet-on-average weeks are occasionally
  enormous (early harvest, low-water rushes).
* Percentiles are not additive: summing two weekly P90s overstates the two-week P90, and picks different windows than the
  P90 of the two-week sum.
* Historical closure weeks recorded as zero traffic look like the quietest weeks of all.
* With a dependency and a single crew, greedy "best window per lock" choices can be infeasible or suboptimal.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `lpms_lockages_2014_2023.csv` (four locks) | CSV | ~150k lockage records | USACE Navigation Data / LPMS (Corps Locks website) | U.S. Gov public domain | Lockages with tonnage and timestamps |
| 2 | `lpms_monthly_summary_2014_2023.xlsx` | XLSX | ~500 | USACE | Public domain | Reconciliation |
| 3 | `lock_closure_history.csv` | CSV | ~200 | USACE Corps Locks notices (historical stoppages) | Public domain | Weeks to exclude |
| 4 | `waterborne_commerce_segment_tonnage.pdf` | PDF | — | USACE Waterborne Commerce Statistics Center | Public domain | Context |
| 5 | `lock_attributes.json` | JSON | 4 | USACE | Public domain | Lock IDs, river miles |
| 6 | `iso_weeks_2014_2024.csv` | CSV | ~550 | Derived | — | Week calendar |
| 7 | `usda_grain_transportation_report_extract.pdf` | PDF | — | USDA AMS Grain Transportation Report | Public domain | Harvest-season context |
| 8 | `maintenance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `planner_draft_schedule.xlsx` | XLSX | 4 | Task author | — | Average-based draft |
| 10 | `river_stage_2014_2023.csv` | CSV | ~3.6k daily | USGS/USACE gauge | Public domain | Low-water context |

## 5. Deterministic solution path

1. Aggregate lockage tonnage to lock × ISO week × year; mark closure-affected weeks missing.
2. For every lock and admissible start week, compute the 2-week sums per year and their P90.
3. Enumerate feasible schedules (four locks, non-overlap with gaps, blackouts, B before C) and minimize total exposure
   (small enough for exhaustive search); apply tie-breaks.
4. Report each closure's exposure, the total, and the planner draft's exposure under the same metric.

## 6. Wrong paths (method errors, not misreadings)

**A — mean tonnage.** Picks volatile weeks; total P90 exposure higher.

**B — sum of weekly P90s.** Different (and overstated) window ranking.

**C — closure weeks counted as zero.** Historical closure windows look ideal and get re-selected.

**D — lock-by-lock greedy.** Violates the dependency or misses the joint optimum.

## 7. Why the stump is analytical, not semantic

Exposure, constraints and conventions are fully defined. The errors are statistical (quantile additivity, missing-vs-zero
in a history) and combinatorial (joint feasibility), not interpretive.

## 8. Draft task prompt (prose)

> We have to fit four two-week lock closures into next year with one crew, no closures during harvest or ice season, and
> lock B finishing before lock C starts. Using the LPMS history and the maintenance memo in the folder, find the schedule
> that minimizes the bad-year traffic exposed to closures. Give me `closure_schedule.csv` (lock, start week, end week,
> exposure in tons, rank of that window among the lock's feasible windows) and `exposure_heatmap.png`, a lock × start-week
> heatmap of exposure with blackouts greyed and the chosen windows outlined. Add a one-page `schedule_memo.pdf` comparing
> total exposure for our schedule and the planner's average-based draft.

## 9. Deliverables

* `closure_schedule.csv`, `exposure_heatmap.png`, `schedule_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 start weeks, 4 exposures, total; feasibility checks (gap, blackout, dependency); exposures of runner-up windows;
  draft comparison; heatmap marks.

## 11. Golden-output checklist

* P90 of 2-week sums; closure weeks missing; all constraints; exhaustive optimum with tie-break.

## 12. Build notes (scope tuning)

* Choose locks where harvest-adjacent weeks are low on average but high at P90; confirm Traps A and B change ≥ 2 windows.
* Verify the LPMS export fields (tonnage per lockage, timestamps) and document how lockages map to ISO weeks.
