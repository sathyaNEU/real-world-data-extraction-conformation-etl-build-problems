# DS09 — Delivery promise windows: plan on the 95th-percentile trip, not the average trip

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Promise-time and ETA setting at delivery, logistics and ride-hail companies, where reliability targets require tail travel times |
| Domain | Freight / regional logistics |
| Task shape | 04 · Setting one dial (the dispatch departure time for each of 4 corridor × time-of-day combinations so that 95% of trips arrive before the delivery window opens) |
| Core method | Travel-time distributions by corridor, weekday and departure time from loop/probe data; planning time = 95th percentile travel time; departure time = window start − planning time; comparison with mean-based and "mean + 10 minutes" rules; on-time rate replay over the evaluation quarter |
| Analytical stump | Average travel time plus a fixed buffer under-protects peak periods (heavy right tails) and over-protects off-peak. Reliability promises map to percentiles of the travel-time distribution specific to the corridor and departure time, and percentiles must be computed from trip-level distributions, not averaged across days |
| Primary sources | Washington State DOT travel times (corridor travel time data feeds/archives) |

## 1. The real-world situation

A regional distributor promises customers deliveries within 07:30–08:00 windows across four Seattle-area corridors. Dispatch currently leaves at
window start minus average travel time plus 10 minutes. Late arrivals cluster on two corridors in winter and on Mondays.

## 2. The decision (one deterministic recommendation)

**The dispatch time for each corridor and departure bucket (to the nearest 5 minutes) that achieves ≥ 95% on-time arrival in the evaluation
quarter, and the on-time rates of the current rule.**

Rules (dispatch memo):

* Data: WSDOT corridor travel times (2-minute or 5-minute updates) for the 4 corridors in memo; calibration: previous 12 months; evaluation: the
  next quarter.
* Trip travel time for a departure at time d: the travel time reported for the corridor at d (memo convention for corridor-level data).
* Planning time per corridor × weekday group (Mon, Tue–Thu, Fri) × winter/non-winter: 95th percentile of calibration-period travel times for
  departures between 06:30 and 07:30.
* Dispatch time = 07:30 − planning time, rounded down to 5 minutes.
* Evaluation: on-time if arrival ≤ 07:30 for each evaluation day; report on-time rates per corridor for new and current rules.

## 3. Why capable analysts get it wrong

* Averages are stable and easy to communicate.
* Travel-time distributions are skewed; incidents and weather create long tails.
* Weekday and season effects shift the tail more than the mean.
* Percentiles of daily averages differ from percentiles of trips.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `wsdot_travel_times_<year>.csv` | CSV | ~3–5M records | WSDOT Traveler Information (travel time API/archive) | WSDOT public data (verify terms) | Corridor travel times |
| 2 | `wsdot_travel_time_routes.json` | JSON | ~100 routes | WSDOT | Public | Route definitions |
| 3 | `corridors_in_scope.json` | JSON | 4 | Task author | — | Corridors |
| 4 | `dispatch_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `current_rule.json` | JSON | — | Task author | — | Mean + 10 min |
| 6 | `fhwa_reliability_measures_citation.pdf` | PDF | — | FHWA travel time reliability guide (cite) | Public domain | Planning time index |
| 7 | `holiday_calendar.json` | JSON | — | Task author | — | Exclusions |

## 5. Deterministic solution path

1. Filter corridors and departure windows; tag weekday groups and seasons.
2. Compute 95th percentiles per cell; dispatch times.
3. Replay evaluation quarter for new and current rules; on-time rates.
4. Recommendation.

## 6. Wrong paths (method errors, not misreadings)

**A — mean + fixed buffer.** Unequal reliability.

**B — percentile of daily mean travel times.** Understates tails.

**C — pooling weekdays and seasons.** Misplaces buffers.

**D — evaluating on the calibration year.** Optimistic.

## 7. Why the stump is analytical, not semantic

The cells, percentile and replay are specified. The trap is planning on means under skewed travel times.

## 8. Draft task prompt (prose)

> What dispatch times give us 95% on-time deliveries on each corridor? Use planning-time percentiles as the dispatch memo specifies and replay next
> quarter against the current rule. Provide `dispatch_times.csv` (corridor × weekday group × season: planning time, dispatch time, on-time new and
> current), `travel_time_distributions.png`, and a one-page `dispatch_policy.pdf`.

## 9. Deliverables

* `dispatch_times.csv`, `travel_time_distributions.png`, `dispatch_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 corridors × 3 weekday groups × 2 seasons = 24 dispatch times; on-time rates; current-rule contrast.

## 11. Golden-output checklist

* Filters; cell definitions; percentiles; rounding; replay.

## 12. Build notes (scope tuning)

* Confirm the current rule achieves < 90% on-time on at least two corridors in the evaluation quarter.
