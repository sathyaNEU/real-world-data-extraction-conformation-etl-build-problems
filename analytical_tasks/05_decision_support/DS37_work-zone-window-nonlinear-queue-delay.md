# DS37 — When to close a lane for roadworks: delay explodes above capacity, so the average hour misleads

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Scheduling maintenance windows that reduce capacity (database maintenance, deploys with fewer replicas, warehouse line stoppages) where delay is nonlinear in load |
| Domain | Highway operations |
| Task shape | 07 · Grid of cells (weekday × start hour → expected vehicle-hours of delay for a 6-hour lane closure; the window adopted for the 8-week works) |
| Core method | Deterministic queueing (cumulative arrivals versus reduced capacity) on hourly volumes by weekday and hour from the counter's history; expected delay over the distribution of historical days (not the average day); constraints on allowed windows; choose the window minimising expected delay |
| Analytical stump | Choosing the window with the lowest average traffic volume (or evaluating queue delay on the average day) ignores that delay is zero below capacity and grows quadratically above it; days with demand slightly above capacity dominate. Expected delay over the distribution of days ranks windows differently |
| Primary sources | UCI "Metro Interstate Traffic Volume" dataset (I-94 westbound, Minnesota DOT ATR station, hourly volumes 2012–2018) |

## 1. The real-world situation

A DOT schedules an 8-week resurfacing that requires closing one of three lanes for 6 hours per night or day. Work-zone capacity drops to 1,500
vehicles/hour (memo). The planner picked the 6-hour window with the lowest average hourly volume. Night windows near weekends occasionally see
event traffic that exceeds the reduced capacity.

## 2. The decision (one deterministic recommendation)

**The weekday-specific 6-hour closure window (start hour) minimising expected vehicle-hours of delay, and the expected delay of the planner's window.**

Rules (operations memo):

* Data: I-94 hourly traffic volume 2016–2018 (to avoid earlier data gaps per memo); remove duplicate timestamps (keep first) and hours flagged by the
  memo's gap rule.
* Days: grouped by weekday; holidays excluded.
* Capacity during closure: 1,500 veh/h; queue starts at window start and clears after the window ends at full capacity 4,500 veh/h (memo).
* Delay for a given day and window: area between cumulative arrivals and cumulative departures (deterministic queue), in vehicle-hours.
* Expected delay for weekday × start hour = mean over that weekday's historical days.
* Allowed starts (`allowed_windows.json`): 19:00, 20:00, 21:00, 22:00 and 23:00 on Sunday–Thursday nights, and 09:00 and 10:00 on Monday–Friday;
  choose the weekday × start with the minimum expected delay.
* Contrast: lowest mean volume window.

## 3. Why capable analysts get it wrong

* Average volume is the obvious proxy for disruption.
* Queue delay is a nonlinear function of excess demand; averages hide the days that matter.
* Queues persist beyond the window until cleared.
* Data cleaning (duplicates, gaps) affects volumes.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Metro_Interstate_Traffic_Volume.csv` | CSV | 48,204 | UCI ML Repository (id 492) | CC BY 4.0 | Hourly volume, weather, holiday |
| 2 | `metro_interstate_description.html` | HTML | — | UCI | CC BY 4.0 | Variables |
| 3 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 4 | `planner_average_window.xlsx` | XLSX | — | Task author | — | Naive choice |
| 5 | `queue_model_reference.pdf` | PDF | — | Cite (HCM work zone chapter; queueing diagrams) | Cite | Method |
| 6 | `allowed_windows.json` | JSON | — | Task author | — | Constraints |
| 7 | `mndot_atr_station_note.pdf` | PDF | — | MnDOT (cite) | Public | Station context |

## 5. Deterministic solution path

1. Clean data; select years; group by weekday and hour.
2. For each allowed window and each historical day, compute queue delay.
3. Expected delay per window; choose; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — lowest average volume.** Ignores tail days.

**B — delay on the average day.** Underestimates expected delay.

**C — ignoring queue clearance after the window.** Undercounts.

**D — keeping duplicate timestamps.** Inflated volumes.

## 7. Why the stump is analytical, not semantic

The queue model and constraints are specified. The trap is averaging inputs to a nonlinear function.

## 8. Draft task prompt (prose)

> When should the lane closures run? Compute expected queue delay over historical days for each allowed window as the operations memo specifies and
> compare with the lowest-volume window. Provide `window_delay_grid.csv` (weekday × start hour: expected delay), `delay_distribution.png`, and a
> one-page `closure_schedule.pdf`.

## 9. Deliverables

* `window_delay_grid.csv`, `delay_distribution.png`, `closure_schedule.pdf`.

## 10. Where 25+ rubric criteria come from

* Expected delay for 30+ allowed windows (sampled); chosen window; planner contrast; cleaning counts.

## 11. Golden-output checklist

* Cleaning; holiday exclusion; queue computation; clearance; expectation; choice.

## 12. Build notes (scope tuning)

* Confirm the lowest-average-volume window is not the minimum expected-delay window.
