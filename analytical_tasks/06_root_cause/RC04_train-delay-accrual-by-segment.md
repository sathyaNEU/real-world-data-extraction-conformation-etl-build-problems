# RC04 — Where do trains lose time? Not where the delay is observed, but where it is gained

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Latency attribution along multi-hop paths (request traces, delivery legs, manufacturing routing) where the end-to-end delay accumulates upstream |
| Domain | Rail operations |
| Task shape | 12 · Drill-down to one leaf (line → direction → time band → the station-to-station segment or station dwell where the most delay is gained) |
| Core method | From actual and scheduled times at every timetable point, compute delay at each point; delay gained on a running segment = delay at arrival(next) − delay at departure(previous); delay gained at a station = departure delay − arrival delay; aggregate positive and net gains by segment; drill down from the line's arrival-delay increase |
| Analytical stump | Final-destination arrival delay (or arrival delay at the busiest station) shows where delay is noticed, not where it arises. Delay also recovers on padded segments. Attribution needs differences of delay along the path, separating dwell from running time |
| Primary sources | Digitraffic (Fintraffic) railway open data — train timetables and actual times at each station (historical trains) |

## 1. The real-world situation

A regional commuter line's on-time performance at Helsinki deteriorated over the autumn timetable. Operations blamed congestion at the main
terminal approach. An analyst suspected long dwell times at an intermediate interchange added after a timetable change.

## 2. The decision (one deterministic recommendation)

**The segment or station (leaf) that contributes the most net delay gained in the morning peak inbound direction this autumn compared with last
autumn, and its contribution in minutes per train.**

Rules (operations memo):

* Data: Digitraffic historical train data for the line's commuter trains (train numbers in memo), Sept–Nov this year and last year; time table rows
  with scheduled and actual times (arrival/departure) per station.
* Delay at a point = actual − scheduled (seconds); cancelled stops excluded.
* Running gain for segment s→s+1 = arrival delay at s+1 − departure delay at s; dwell gain at s = departure delay − arrival delay.
* Morning peak inbound: departures from origin 06:30–09:00.
* Mean gain per train per segment/station; change versus last year.
* Leaf = largest positive change in mean gain; report top 5 contributors and the recovery segments.

## 3. Why capable analysts get it wrong

* Arrival punctuality at the terminal is the headline KPI.
* Delays propagate and are partly recovered; where they appear differs from where they arise.
* Dwell and running time require separate measures.
* Timetable changes alter schedules; gains must be relative to schedule.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `trains_<date>.json` (daily dumps, 2 × 3 months) | JSON | ~2,000 trains/day × ~20 stops | Digitraffic rata.digitraffic.fi | CC BY 4.0 | Time table rows with actual times |
| 2 | `stations.json` | JSON | ~600 | Digitraffic | CC BY 4.0 | Station codes |
| 3 | `cause_codes.json` | JSON | ~200 | Digitraffic | CC BY 4.0 | Delay cause categories (context) |
| 4 | `line_trains.json` | JSON | ~100 train numbers | Task author | — | Scope |
| 5 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `terminal_otp_report.xlsx` | XLSX | — | Task author | — | Original claim |
| 7 | `timetable_change_notes.json` | JSON | — | Task author (from published timetable notices) | — | Context |

## 5. Deterministic solution path

1. Extract time table rows for scope trains; compute point delays.
2. Running and dwell gains per segment/station; filter peak inbound.
3. Means by period; changes; leaf; top contributors.

## 6. Wrong paths (method errors, not misreadings)

**A — terminal arrival delay.** Wrong location.

**B — delay level at each station instead of gains.** Accumulation confused with cause.

**C — ignoring recovery (negative gains).** Overstates some segments.

**D — mixing directions.** Different paths.

## 7. Why the stump is analytical, not semantic

Delay definitions and aggregation are specified. The trap is attributing cumulative quantities to the point of observation.

## 8. Draft task prompt (prose)

> Where is the commuter line losing time this autumn? Compute delay gained by segment and dwell as the operations memo specifies and drill down to the
> biggest contributor. Provide `delay_gain_by_segment.csv` (segment/station: mean gain this year, last year, change), `delay_profile.png`, and a one-page
> `line_delay_rca.pdf`.

## 9. Deliverables

* `delay_gain_by_segment.csv`, `delay_profile.png`, `line_delay_rca.pdf`.

## 10. Where 25+ rubric criteria come from

* Gains for ~20 segments/stations × change; leaf; top 5; recovery segments; terminal OTP change.

## 11. Golden-output checklist

* Train scope; delay computation; gains; peak filter; changes; leaf.

## 12. Build notes (scope tuning)

* Confirm the leaf is an intermediate dwell or segment, not the terminal approach.
