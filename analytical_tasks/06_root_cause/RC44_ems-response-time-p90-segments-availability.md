# RC44 — Ninetieth-percentile medical response time up 90 seconds: traffic, slow dispatch, slow turnout, or units arriving from farther away?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Latency breakdowns of a request path (queueing, processing, network) where a tail percentile moved and percentiles of the parts do not add up; capacity spillover (requests served by a farther region when the nearest is busy) |
| Domain | Fire and emergency medical services |
| Task shape | 12 · Drill-down to one leaf (P90 response time change → call processing, turnout, travel → within travel, first-due vs out-of-area units → battalion → the leaf) |
| Core method | Per incident: processing (received → dispatched), turnout (dispatched → en route), travel (en route → on scene) for the first-arriving unit; P90 counterfactuals swapping one segment's current-period values for reference-period values by quantile mapping within station area; Shapley over the three segments for the P90 change; within travel, share of first-arriving units from outside the station area and their travel penalty |
| Analytical stump | Percentiles are not additive, so comparing each segment's P90 does not explain the total P90. Travel time rose, so the city blamed traffic; but travel time also rises when the first-due unit is busy and a unit from another station area responds. Separating out-of-area responses (an availability problem) from same-area travel (a traffic problem) points to a staffing or deployment fix rather than traffic engineering |
| Primary sources | San Francisco Fire Department Calls for Service (DataSF) — incident and unit timestamps, station areas, battalions, unit IDs |

## 1. The real-world situation

A city's 90th-percentile response time for life-threatening medical calls rose by about 90 seconds year over year. The mayor's office attributed
the rise to traffic congestion and proposed signal-priority investments. The fire department believed that rising call volume left first-due units
busy, so more calls were answered by units from farther stations.

## 2. The decision (one deterministic recommendation)

**The investment the city makes — traffic signal priority (if same-area travel is the largest contributor) or additional unit-hours in the leaf
battalion (if out-of-area travel or turnout is) — with the Shapley P90 decomposition and the travel split.**

Rules (city memo):

* Data: DataSF Fire Department Calls for Service, medical incidents with the memo's priority codes (life-threatening), reference and current
  calendar years.
* First-arriving unit per incident: the unit with the earliest on-scene time; exclude incidents with any missing or non-monotonic timestamp.
* Segments: processing = dispatch − received; turnout = response (en route) − dispatch; travel = on scene − response.
* Unit home station: parsed from the unit ID per the memo's mapping; out-of-area if the home station ≠ the incident's station area.
* Counterfactual for segment k: replace each current incident's k value with the reference-period value at the same within-station-area percentile
  rank (quantile mapping); compute the P90 of total response time.
* Shapley over 3 segments for ΔP90 (8 combinations).
* Travel split: out-of-area share and mean travel penalty (out-of-area minus same-area mean travel) in each year; contribution of the change in
  out-of-area share × reference penalty, reported in seconds of mean travel.
* Drill to the battalion with the largest increase in out-of-area share.
* Signal priority if same-area travel change (mean seconds) exceeds the out-of-area contribution; otherwise unit-hours in the leaf battalion.

## 3. Why capable analysts get it wrong

* Segment percentiles are compared as if additive.
* Travel time is equated with traffic.
* Unit availability is not visible in incident-level response times without unit home stations.
* Data quality issues (missing and out-of-order timestamps) are common.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Fire_Department_Calls_for_Service.csv` (2 years) | CSV | ~650k unit-responses | DataSF | ODC PDDL (DataSF open data) | Incidents and unit timestamps |
| 2 | `fire_station_areas.geojson` | GeoJSON | ~50 | DataSF | ODC PDDL | Station areas |
| 3 | `unit_home_station_mapping.csv` | CSV | ~300 | Task author (from unit ID conventions; cite SFFD) | Cite | Unit → station |
| 4 | `call_type_priority_codes.csv` | CSV | ~40 | Task author (from the dataset's documentation) | — | Life-threatening medical filter |
| 5 | `city_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `mayor_traffic_brief.xlsx` | XLSX | — | Task author | — | Traffic explanation |

## 5. Deterministic solution path

1. Filter incidents; choose first-arriving units; validate timestamps.
2. Compute segments; map unit home stations; flag out-of-area responses.
3. Quantile-mapped counterfactuals; Shapley for ΔP90.
4. Travel split; battalion drill-down; decision.

## 6. Wrong paths (method errors, not misreadings)

**A — segment P90s compared.** Non-additive; the sum does not match the total.

**B — travel time as traffic.** Availability spillover attributed to congestion.

**C — all responding units instead of first-arriving.** Later units' times dilute the analysis.

**D — no timestamp validation.** Negative or missing segments distort percentiles.

## 7. Why the stump is analytical, not semantic

All fields are timestamps and IDs with explicit rules. The trap is non-additive percentiles and a confounded segment.

## 8. Draft task prompt (prose)

> The mayor's office says traffic is behind our slower medical response times and wants signal priority. Decompose the P90 change with the city memo's
> method and tell me what drove it and where to invest. Provide `response_time_decomposition.csv` (segment: Shapley seconds; travel split; battalion
> detail), `response_segments.png`, and a one-page `response_time_investment.pdf`.

## 9. Deliverables

* `response_time_decomposition.csv` — Shapley contributions, travel split and battalion drill-down.
* `response_segments.png` — segment distributions by year and the P90 waterfall.
* `response_time_investment.pdf` — decision and why the traffic explanation is incomplete.

## 10. Where 25+ rubric criteria come from

* Filtering and validation counts: 4.
* P90 totals and segment medians by year: 8.
* Shapley contributions (3) and closure: 4.
* Out-of-area shares, penalties and contribution: 5.
* Battalion leaf: 2.
* Decision and contrast: 3.

## 11. Golden-output checklist

* First-arriving unit; timestamp monotonicity.
* Quantile mapping within station area; 8-combination Shapley.
* Out-of-area definition from unit home station.

## 12. Build notes (scope tuning)

* Choose years with rising medical call volume; confirm the out-of-area contribution exceeds same-area travel change.
