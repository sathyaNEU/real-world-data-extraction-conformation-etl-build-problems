# OS24 — Flexible EV charging: energy delivered is not flexibility at the peak

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Demand-response and flexible-compute sizing (deferrable batch jobs, shiftable deliveries), where only load that is present at the peak and has slack can move |
| Domain | Electricity networks / EV charging |
| Task shape | 07 · Grid of cells (charging site groups × weekday/weekend → average shiftable kW during the 16:00–19:00 network peak; the flexibility volume bid into the network operator's tender) |
| Core method | Per session: plugged-in interval, energy delivered, maximum charger power; minimum charging time = energy ÷ power; slack = dwell − minimum charging time; shiftable power during the peak window = charging power drawn in the window by sessions whose slack allows deferral to after 19:00 within their dwell; average over days |
| Analytical stump | Sizing flexibility as total energy delivered ÷ hours (or as all sessions overlapping the peak) ignores whether a session is actually charging during the peak and whether it has time to finish later. Many peak-overlapping sessions are short top-ups with no slack; long workplace sessions are mostly finished before 16:00 |
| Primary sources | Dundee City Council EV charging session data (public charge points) |

## 1. The real-world situation

A charge-point operator plans to bid flexibility into a distribution network operator's peak-reduction tender (MW available 16:00–19:00 on
weekdays). The commercial team sized the bid as the average power of all sessions overlapping the peak window. Engineers pointed out that
many of those sessions must charge immediately.

## 2. The decision (one deterministic recommendation)

**The flexibility volume bid (kW, rounded down to 10 kW) = average weekday shiftable power during 16:00–19:00 across the network, with the
site-group × day-type grid.**

Rules (commercial memo):

* Data: Dundee charging sessions for the year in the memo (start, end, energy kWh, charger ID and type).
* Charger power: from `charger_power.csv` (7 kW AC, 22 kW AC, 50 kW DC).
* Session power profile: constant at charger power from plug-in until energy is delivered (memo's "charge-first" assumption), then idle until
  unplug.
* Shiftable in a 30-minute peak slot: charging power of sessions whose dwell after 19:00 is ≥ the energy they would still need if deferred from
  that slot (memo formula); DC sessions excluded (not deferrable).
* Average shiftable kW = mean over weekdays of the mean over the six peak slots.
* Bid = floor to 10 kW.
* Report the "all overlapping sessions" estimate for contrast.

## 3. Why capable analysts get it wrong

* Overlap with the peak window seems like flexibility.
* Charging typically occurs at the start of a session; by 16:00 many long sessions are idle.
* Without dwell after the peak, deferral is impossible.
* Rapid chargers serve drivers who will not wait.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `dundee_ev_charging_sessions_<year>.csv` | CSV | ~60–90k sessions | Dundee City Council open data | Open Government Licence v3 | Sessions |
| 2 | `charger_locations.csv` | CSV | ~100 | Dundee City Council | OGL | Charger IDs, site types |
| 3 | `charger_power.csv` | CSV | ~100 | Task author (from charger type field) | — | Power ratings |
| 4 | `site_groups.json` | JSON | ~4 | Task author | — | Groups (car parks, residential, workplace, rapid hubs) |
| 5 | `commercial_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `commercial_team_bid.xlsx` | XLSX | — | Task author | — | Naive bid |
| 7 | `dno_flexibility_tender_citation.pdf` | PDF | — | DNO tender documents (cite) | Public | Product definition |
| 8 | `session_profiles.parquet` | Parquet | ~5M slots | Derived | OGL | Half-hourly profiles |

## 5. Deterministic solution path

1. Clean sessions; assign power; build half-hourly charging profiles.
2. For each weekday peak slot, compute shiftable power per memo.
3. Averages by site group and day type; bid.
4. Contrast with the overlap estimate.

## 6. Wrong paths (method errors, not misreadings)

**A — all overlapping sessions' average power.** Overstated.

**B — energy ÷ hours.** Ignores timing.

**C — including DC sessions.** Non-deferrable.

**D — ignoring dwell after 19:00.** Infeasible deferrals counted.

## 7. Why the stump is analytical, not semantic

The profile assumption and slack rule are specified. The trap is confusing presence with flexibility.

## 8. Draft task prompt (prose)

> How much peak flexibility can we bid into the network tender? Compute shiftable charging power in the 16:00–19:00 window from Dundee sessions
> as the commercial memo specifies. Provide `flexibility_grid.csv` (site group × day type: overlap kW, shiftable kW), `peak_profile.png`, and a
> one-page `tender_bid.pdf`.

## 9. Deliverables

* `flexibility_grid.csv`, `peak_profile.png`, `tender_bid.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 groups × 2 day types × 2 measures = 16; slot values for 6 slots; bid; contrast.

## 11. Golden-output checklist

* Power assignment; charge-first profile; slack rule; DC exclusion; averaging; rounding.

## 12. Build notes (scope tuning)

* Confirm the overlap estimate is ≥ 3× the shiftable estimate.
