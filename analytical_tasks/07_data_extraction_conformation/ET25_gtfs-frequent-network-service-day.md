# ET25 — Frequent-network eligibility from GTFS: service days, 25:10:00 departures and frequency-based trips

| Field | Value |
|---|---|
| Domain | Public transit planning / service standards / grant eligibility |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 10 · Scorecard against thresholds (route × direction × metric) |
| Core technique | GTFS service-calendar resolution (calendar + calendar_dates exceptions); service-day time arithmetic beyond 24:00; expansion of frequencies.txt; timepoint-based headway measurement |
| Trap family (honest data) | Times parsed modulo 24; exceptions ignored; frequency trips not expanded; both directions pooled; first-stop headways |
| Primary sources | An agency's static GTFS feed (archived version), GTFS reference, agency service standards |

## 1. The real-world project

A transit agency brands routes as **Frequent Network** (and becomes eligible for a state capital grant) when they meet
a service standard on a representative weekday. Planning built a GTFS-based checker; it certified a route that runs
every 30 minutes at midday, and rejected one with a 10-minute frequency-based schedule.

## 2. The business decision (one deterministic recommendation)

**Go / no-go: does the candidate route meet the Frequent Network standard on the representative weekday in the feed?**

Rules (service standard):

* Representative day: the date in the folder (a Wednesday). Active service IDs = those in `calendar.txt` whose weekday
  flag is 1 and whose date range contains the date, **plus** `calendar_dates.txt` exception_type 1 for the date, **minus**
  exception_type 2 for the date.
* Trips belong to the service day of their `service_id`; times ≥ 24:00:00 are on the same service day (e.g. 25:10:00 =
  01:10 next calendar morning) and never wrap to the start of the day.
* Frequency-based trips (`frequencies.txt`) are expanded into individual departures from `start_time` to `end_time` by
  `headway_secs`.
* Headways are measured at the route's designated timepoint stop (in the folder), per `direction_id`, using departures of
  trips that serve that stop.
* Metrics per direction: M1 max headway within 07:00–19:00 (including the gap from 07:00 to the first departure and from
  the last departure to 19:00) ≤ 15 min; M2 first departure ≤ 06:00; M3 last departure ≥ 24:00 service-day time
  (midnight); M4 ≥ 48 departures between 07:00 and 19:00.
* Go if all four metrics pass in **both** directions.

## 3. Why this gets overlooked in real projects

* `HH:MM:SS` strings beyond 24 hours break datetime parsers; wrapping modulo 24 moves late trips to early morning and
  makes the span look complete.
* Exceptions in `calendar_dates.txt` (holidays, special events, service changes) are easy to skip because `calendar.txt`
  "already has weekdays".
* Some agencies schedule frequent corridors only through `frequencies.txt`; each template trip appears once in
  `stop_times.txt`.
* Pooling both directions halves headways; first-stop headways count short-turn trips that never reach the timepoint.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `stop_times.txt` | CSV | 1–5M | Agency GTFS (archived feed version) | Agency open-data licence (choose a feed with an explicit open licence, e.g. CC BY 4.0) | Departures |
| 2 | `trips.txt` | CSV | 20k–100k | Same | Same | Trip → route, service, direction |
| 3 | `routes.txt` | CSV | ~100–300 | Same | Same | Route IDs |
| 4 | `stops.txt` | CSV | 5k–15k | Same | Same | Stops |
| 5 | `calendar.txt` | CSV | ~10–100 | Same | Same | Weekly patterns |
| 6 | `calendar_dates.txt` | CSV | ~100–5k | Same | Same | Exceptions |
| 7 | `frequencies.txt` | CSV | ~10–1k | Same | Same | Frequency-based service |
| 8 | `feed_info.txt`, `agency.txt` | CSV | small | Same | Same | Feed validity, timezone |
| 9 | `gtfs_reference_excerpt.pdf` | PDF | — | gtfs.org | CC BY 3.0/Apache (spec; verify) | Time semantics |
| 10 | `service_standard.pdf` | PDF | — | Task author (modelled on agency service standards) | — | Rules in §2 |
| 11 | `route_timepoints.json` | JSON | ~10 | Task author | — | Candidate route + timepoints |
| 12 | `feed_version.json` | JSON | 1 | Mobility Database / Transitland archive metadata | Open | Feed hash, download date |

## 5. Deterministic solution path

1. Resolve active service IDs for the date.
2. Select candidate-route trips with active service; expand frequency trips.
3. Extract departures at the timepoint per direction; convert to seconds since service-day midnight (no wrapping).
4. Compute M1–M4 per direction; decide.
5. Also run the scorecard for 5–8 other routes as context; show how each trap changes the candidate's result.

## 6. The traps

**Trap A — modulo-24 times.** Late trips appear before 06:00; M2/M3 pass falsely or headways near 07:00 shrink.

**Trap B — no exceptions.** Includes removed service (or misses added service) on the date; M1/M4 change.

**Trap C — frequencies ignored.** Frequency-based route fails M4 and M1.

**Trap D — pooled directions / first-stop headways.** M1 passes for a route that fails in one direction at the timepoint.

## 7. Why the data is honest

GTFS is the agency's published schedule; >24:00 times, exceptions and frequency templates are explicit features of the
specification. Nothing is planted.

## 8. Draft task prompt (prose)

> The candidate route in the folder becomes Frequent Network — and grant-eligible — only if it meets all four tests in our
> service standard in both directions on the representative weekday. Using the GTFS feed, tell me whether it qualifies.
> Produce `frequent_network_scorecard.csv` with one row per route-direction for the candidate and the comparison routes,
> each metric's value and pass/fail; and `headway_timeline.png`, the candidate route's departures at its timepoint across
> the service day for both directions, with the 07:00–19:00 window shaded and any headway over 15 minutes highlighted.
> Add a one-page `eligibility_memo.pdf` with the decision, the binding metric and direction, and its margin.

## 9. Deliverables

* `frequent_network_scorecard.csv`, `headway_timeline.png`, `eligibility_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* Candidate: 2 directions × 4 metrics (values + pass/fail); comparison routes' metrics; decision; binding metric and margin;
  chart elements.

## 11. Golden-output checklist

* Service resolution with exceptions; no time wrapping; frequency expansion; per-direction timepoint headways; decision.

## 12. Build notes (scope tuning)

* Choose a feed and date where the candidate route has after-midnight trips, a calendar_dates exception on the date for
  some service IDs, and frequency-based trips — and confirm at least two traps flip the decision.
* Archive the exact feed version; agencies replace feeds frequently.
