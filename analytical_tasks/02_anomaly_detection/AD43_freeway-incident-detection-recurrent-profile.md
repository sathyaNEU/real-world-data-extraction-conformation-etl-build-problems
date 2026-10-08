# AD43 — Freeway incident alerts: rush hour is slow every day

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Incident detection in navigation apps and traffic-management centres (crowd-sourced and loop-detector speed feeds) |
| Domain | Transportation operations |
| Task shape | 08 · Rule replayed on history (the profile-based incident rule replayed over a year of detector data; confirmed incidents caught, false alerts per day, and operator hours freed) |
| Core method | Time-of-week speed profiles per detector station (median over prior 8 same weekdays, 5-minute bins); deviation ratio; spatial confirmation (station and the next downstream station both deviate) and persistence (3 consecutive bins); exclusion of samples with low observed percentage (imputed) |
| Analytical stump | Fixed speed thresholds (e.g., < 35 mph) fire every weekday at recurrent bottlenecks and stay silent for incidents on routes that are normally congested anyway. PeMS also imputes missing loop data; imputed samples smooth over incidents or create artefacts. Non-recurrent congestion is a deviation from that location's own time-of-week pattern, confirmed in space |
| Primary sources | Caltrans Performance Measurement System (PeMS) station 5-minute data and station metadata; PeMS incident (CHP) feed |

## 1. The real-world situation

A traffic-management centre pages operators when speeds drop below 35 mph at any station on a corridor. Operators acknowledge 40–60 pages a
day, almost all at the same bottlenecks during peaks, and two serious incidents last year were noticed only from phone calls. The centre is
evaluating a profile-based rule before rostering fewer operators on alert duty.

## 2. The decision (one deterministic recommendation)

**The number of operator alert-shift hours per week that the profile-based rule frees up next year, given that it catches at least 85% of
CHP incidents with lane closures over the replay year.**

Rules (operations memo):

* Data: PeMS 5-minute station data for one corridor (mainline stations listed in the memo), one calendar year; drop samples with
  `% Observed` < 50.
* Profile: for each station, weekday and 5-minute bin, the median speed over the prior 8 same weekdays, skipping holidays (a skipped day
  is replaced by the next earlier same weekday).
* Deviation: speed ÷ profile < 0.6 at the station **and** at the next downstream station, for 3 consecutive bins → alert; alerts within 30
  minutes on adjacent stations merge.
* Ground truth: CHP incidents on the corridor with lane closures; caught if an alert starts within 15 minutes after the incident time and
  within 1 mile.
* Freed hours: legacy alerts require 1 operator-hour per 4 alerts; profile rule likewise; freed = (legacy − profile) ÷ 4 ÷ 52 per week.
* If recall < 85%, freed hours = 0 (rule not adopted).

## 3. Why capable analysts get it wrong

* Absolute thresholds are simple and match how drivers describe congestion.
* Recurrent congestion is predictable and not an incident.
* Imputed samples are not measurements; including them blurs detection.
* Single-station dips are often detector noise; spatial confirmation distinguishes shockwaves.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `d<dist>_text_station_5min_<yyyy_mm>.txt.gz` (12 months) | CSV-like text | ~15–20M each (district) | Caltrans PeMS Clearinghouse | Caltrans PeMS public data (account required; verify terms) | Speeds, flows, % observed |
| 13 | `d<dist>_text_meta_<date>.txt` | TSV | ~5k | PeMS | Same | Station metadata (route, direction, postmile) |
| 14 | `all_text_chp_incidents_<year>.txt.gz` | CSV-like text | ~500k | PeMS CHP incident feed | Same | Incidents |
| 15 | `corridor_stations.json` | JSON | ~60 | Task author | — | Mainline stations in order |
| 16 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 17 | `legacy_threshold_alerts.csv` | CSV | ~18k | Task author (replayed legacy rule) | — | Legacy alerts |
| 18 | `holiday_calendar.json` | JSON | ~11 | Task author | — | Holidays |
| 19 | `pems_data_quality_doc_citation.pdf` | PDF | — | PeMS documentation (cite) | Cite | Imputation and % observed |

## 5. Deterministic solution path

1. Filter corridor stations; drop low-observed samples.
2. Build rolling profiles; deviations; spatial and persistence rules; merge alerts.
3. Match alerts to lane-closure incidents; recall; alert counts.
4. Compare with legacy alerts; freed hours.

## 6. Wrong paths (method errors, not misreadings)

**A — absolute speed threshold.** Recurrent bottlenecks dominate.

**B — including imputed samples.** Detection artefacts.

**C — no spatial confirmation.** Single-detector noise.

**D — profile from the whole year (including future days).** Look-ahead in the replay.

## 7. Why the stump is analytical, not semantic

Data filters, profile and matching are specified. The trap is separating recurrent from non-recurrent congestion and respecting data quality.

## 8. Draft task prompt (prose)

> Replay the profile-based incident rule in the operations memo over last year on our corridor and tell me how many alert-shift hours per week
> it frees, provided it catches enough lane-closure incidents. Provide `replay_by_month.csv` (month: alerts, incidents, caught, legacy alerts),
> `speed_profile_example.png` (one station's day with profile, speeds and alerts), and a one-page `alert_rule_decision.pdf`.

## 9. Deliverables

* `replay_by_month.csv`, `speed_profile_example.png`, `alert_rule_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 months × (alerts, caught) = 24; recall; freed hours; legacy totals; dropped-sample share.

## 11. Golden-output checklist

* % observed filter; rolling profile; deviation and confirmation; merging; matching; freed-hours formula.

## 12. Build notes (scope tuning)

* Choose a corridor with recurrent bottlenecks and ≥ 40 lane-closure incidents in the year.
* Confirm the legacy rule produces ≥ 10,000 alerts.
