# FC47 — Launching satellites into a stormy sky: solar-cycle phase and storm clustering decide the risk

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Satellite-constellation operators managing atmospheric-drag risk after launch (the 2022 loss of newly launched satellites to a geomagnetic storm) |
| Domain | Space operations / launch planning |
| Task shape | 13 · Scenarios and the flip point (month × storm-threshold grid; risk tolerance at which the plan flips) |
| Core method | Analog forecasting by solar-cycle phase: historical cycles aligned by months from sunspot maximum; empirical probability that a 7-day post-launch window contains a storm day, computed on windows (not on independent days) |
| Analytical stump | Climatological storm probabilities ignore the cycle phase (the declining phase brings recurrent storms). Treating storm days as independent misstates the chance a window contains at least one — storms cluster and recur every ~27 days. Monthly mean indices hide the daily extremes that matter |
| Primary sources | GFZ Potsdam Kp index (definitive, 1932–present), NOAA SWPC solar-cycle progression data |

## 1. The real-world situation

A small-satellite operator plans a **batch launch to a low insertion orbit** in 2026, where a strong geomagnetic storm in the first
week can raise drag enough to lose satellites before orbit raising. Policy: launch in a month only if the probability that the 7 days
after launch contain a day with Kp ≥ 6− is at most 5%. The analyst used the all-years share of storm days and the independence formula
1 − (1 − p)^7.

## 2. The decision (one deterministic recommendation)

**Which months of 2026 are launch-eligible, and the risk tolerance at which the first-ranked month flips?**

Rules (mission assurance memo):

* Storm day: any 3-hour Kp ≥ 6− (5.67) in the UT day (GFZ definitive Kp).
* Cycle phase: months since the smoothed sunspot maximum of each cycle (cycles 17–24 analogs; cycle 25 maximum date as published by
  NOAA SWPC/SILSO consensus in the folder). 2026 months map to phases +14 … +25 months.
* For each 2026 month, analog windows = every 7-day window starting on any day within ±1 month of the same phase in cycles 17–24;
  probability = share of analog windows containing ≥ 1 storm day.
* Eligible if probability ≤ 5%. Scenario grid: storm threshold {Kp ≥ 5−, 6−, 7−} × the 12 months; flip tolerance = the probability of
  the lowest-risk month (it becomes eligible at that tolerance).

## 3. Why capable analysts get it wrong

* Average storm frequencies over all years blend solar minimum and maximum phases.
* Storm days cluster (multi-day storms, 27-day recurrence), so window probabilities are lower per storm day than independence implies —
  and different by phase.
* Monthly averages of Kp smooth away the 3-hour peaks that define storm days.
* Aligning cycles by calendar year rather than by phase mixes different parts of the cycle.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Kp_ap_Ap_SN_F107_since_1932.txt` | Text | ~34k days (8 Kp values each) | GFZ Potsdam | CC BY 4.0 | Kp, ap, daily sunspot number, F10.7 |
| 2 | `Kp_definitive_since_1932.json` | JSON | ~270k 3-hour values | GFZ Kp web service | CC BY 4.0 | Same, 3-hourly |
| 3 | `observed-solar-cycle-indices.json` | JSON | ~3k months | NOAA SWPC | Public domain | Smoothed sunspot numbers |
| 4 | `predicted-solar-cycle.json` | JSON | ~100 | NOAA SWPC | Public domain | Cycle 25 maximum context |
| 5 | `solar_cycle_maxima_dates.csv` | CSV | ~10 | Derived from #3 (documented rule) | Public domain | Phase anchors |
| 6 | `gfz_kp_documentation.pdf` | PDF | — | GFZ | CC BY 4.0 | Index definitions |
| 7 | `starlink_feb2022_public_statement.pdf` (citation) | PDF | — | Public company statement (cite) | Cite | Context |
| 8 | `mission_assurance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `analyst_independence_calc.xlsx` | XLSX | ~12 | Task author | — | Climatology × independence |
| 10 | `launch_manifest_2026.json` | JSON | — | Task author | — | Candidate months |

## 5. Deterministic solution path

1. Build daily storm flags from 3-hour Kp; compute cycle phase for each day.
2. For each 2026 month and threshold, collect analog windows; compute window probabilities.
3. Eligibility at 5%; grid; flip tolerance.
4. Contrast with all-years climatology and independence.

## 6. Wrong paths (method errors, not misreadings)

**A — all-years climatology.** Phase ignored; months mis-ranked.

**B — independence formula.** Window risk misstated.

**C — monthly mean Kp.** Storm days invisible.

**D — calendar alignment.** Wrong analogs.

## 7. Why the stump is analytical, not semantic

The storm definition, phase alignment and window rule are explicit; the trap is conditioning and dependence in event probabilities.

## 8. Draft task prompt (prose)

> Which 2026 months can we launch in under the mission assurance memo's 5% storm-risk rule? Use the Kp history aligned by solar-cycle
> phase and compute, for each month, the chance a 7-day post-launch window contains a storm day. Provide `launch_risk_grid.csv` (month ×
> threshold: analog windows, probability, eligible), `storm_risk_by_phase.png`, and a one-page `launch_window_decision.pdf` with the
> eligible months and the flip tolerance.

## 9. Deliverables

* `launch_risk_grid.csv`, `storm_risk_by_phase.png`, `launch_window_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 months × 3 thresholds = 36 probabilities; eligible months; flip tolerance; independence contrast.

## 11. Golden-output checklist

* 3-hour threshold; phase anchors; analog window construction; window probabilities; eligibility.

## 12. Build notes (scope tuning)

* Document how cycle maxima are dated (smoothed sunspot number) and how incomplete cycles are excluded.
* If no month is eligible at 5%, the flip tolerance is still deterministic; consider stating 10% instead before freezing.
