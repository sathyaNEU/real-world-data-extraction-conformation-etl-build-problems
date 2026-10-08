# AD11 — BGP hijack paging: most new origins are legitimate, and the pager must know it

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Network-monitoring and CDN providers detecting route hijacks and leaks (large public incidents in 2018 and 2020 diverted traffic of major cloud and DNS providers) |
| Domain | Internet routing / network security operations |
| Task shape | 10 · Scorecard against thresholds (origin-change event × test → page / suppress; go/no-go on the policy) |
| Core method | Event construction from BGP update streams (prefix, new origin AS, first seen, duration, peer visibility), RPKI route-origin validation against the ROA set valid at event time, 30-day origin history, persistence and visibility filters |
| Analytical stump | Multi-origin announcements (anycast, CDNs, customer–provider changes) are routine, so "new origin = hijack" pages thousands of times a day. RPKI state must be evaluated with the ROAs in force at the event time, and short-lived, low-visibility announcements behave differently from real hijacks |
| Primary sources | RIPE NCC RIS raw BGP updates (MRT), RouteViews archives, RPKI validated ROA archives |

## 1. The real-world situation

A network operator's NOC adopted a simple hijack alert: page when any of its monitored prefixes — or any prefix of its top
customers — is announced by an origin AS not seen in the previous minute. On the day of a large route leak the pager went off
thousands of times; on ordinary days it still fired hundreds of times, mostly for CDN and anycast networks. The SRE lead wants a policy
that would have paged for the leak and stayed quiet otherwise.

## 2. The decision (one deterministic recommendation)

**Adopt or reject the proposed paging policy, given (a) whether it pages on the incident day for the monitored prefixes and (b) its
page count on a normal control week.**

Rules (NOC memo):

* Monitored set: prefixes in `monitored_prefixes.csv` (operator + customers).
* Events: from RIS collectors rrc00, rrc01, rrc03, rrc12 update files, a (prefix, origin AS) pair is a new-origin event if that
  origin was not announcing that prefix (or a covering prefix) in the previous 30 days of RIB dumps.
* Tests per event: T1 RPKI status of (prefix, origin) using the validated ROA snapshot closest before the event (invalid / valid /
  not-found); T2 maximum visibility = share of full-feed RIS peers that carried the route; T3 duration ≥ 5 minutes.
* Policy P: page if T1 = invalid and T2 ≥ 5%; or T1 = not-found, T2 ≥ 10% and T3 holds. Never page for T1 = valid.
* Adopt P if it pages at least once for the incident window in the folder and produces ≤ 10 pages in the control week.

## 3. Why capable analysts get it wrong

* Origin changes are frequent and mostly benign; base rates make naive detectors useless.
* RPKI coverage and ROAs change daily; validating with today's ROAs mis-classifies historical events.
* Visibility matters: an announcement seen by one peer for seconds is not a hijack of global traffic.
* Covering-prefix history (a /24 more-specific of an announced /16) must be considered to avoid flagging normal de-aggregation.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–4 | `rrc00/updates.YYYYMMDD.HHMM.gz` (incident day + control week, 4 collectors) | MRT (binary) | millions of updates | RIPE NCC RIS | RIPE NCC data terms (free use with attribution) | BGP updates |
| 5–6 | `bview.YYYYMMDD.0000.gz` (30 days of daily RIB dumps, 4 collectors) | MRT | ~1M routes per dump | RIPE NCC RIS | Same | Origin history |
| 7 | `routeviews_updates_sample/` | MRT | ~1M | University of Oregon RouteViews | Public | Cross-check |
| 8 | `rpki_vrps_YYYYMMDD.csv` (daily validated ROA payloads) | CSV | ~500k each | RPKI archive (e.g. RIPE NCC / rpkiviews) | Open data (verify) | ROAs over time |
| 9 | `parsed_events_incident_and_control.parquet` | Parquet | ~200k events | Derived | Same | Candidate events |
| 10 | `monitored_prefixes.csv` | CSV | ~400 | Task author (public prefixes of the affected networks) | — | Scope |
| 11 | `incident_window.json` | JSON | — | Task author (from public incident reports) | — | Incident timing |
| 12 | `noc_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 13 | `rfc6811_rov.pdf` | PDF | — | IETF RFC 6811 | IETF Trust (permissive) | Origin validation algorithm |

## 5. Deterministic solution path

1. Parse updates and RIBs; build 30-day origin histories per prefix (with covering prefixes).
2. Derive new-origin events for monitored prefixes; compute T1 (time-correct ROAs), T2, T3.
3. Apply P; count pages in the incident window and the control week; decide.
4. Contrast with the naive "any new origin" detector and with ROV using current ROAs.

## 6. Wrong paths (method errors, not misreadings)

**A — any new origin.** Thousands of pages; policy appears "sensitive".

**B — current ROAs for historical events.** Mis-classified validity.

**C — no covering-prefix history.** De-aggregation flagged.

**D — ignoring visibility/duration.** Pages on transient single-peer artefacts.

## 7. Why the stump is analytical, not semantic

Every test is defined (RFC 6811 for validation). The traps are base rates, time alignment of reference data and event construction —
analytical design choices.

## 8. Draft task prompt (prose)

> Would the proposed hijack-paging policy in the NOC memo have caught the incident in the folder without drowning us in pages on a normal
> week? Build the origin-change events from the RIS data, validate them with the ROAs in force at the time, apply the tests and give me
> adopt or reject. Provide `event_scorecard.csv` (event: prefix, new origin, RPKI state, visibility, duration, page flag),
> `pages_timeline.png` (pages per hour, incident vs control), and a one-page `paging_policy_decision.pdf`.

## 9. Deliverables

* `event_scorecard.csv`, `pages_timeline.png`, `paging_policy_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* Event tests for ~20 spot-check events; pages in incident window; pages in control week; decision; naive-detector counts.

## 11. Golden-output checklist

* 30-day histories incl. covering prefixes; time-correct ROV; visibility over full-feed peers; duration; policy logic.

## 12. Build notes (scope tuning)

* Choose a well-documented public incident (date/time windows from operator post-mortems) and a quiet control week.
* Freeze the ROA snapshots used; publish the parser and peer list.
