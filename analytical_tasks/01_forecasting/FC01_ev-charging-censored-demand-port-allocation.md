# FC01 — Where do 24 new charging ports go? Forecasting the drivers you never saw

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Capacity-censored demand at any constrained service (rejected GPU or quota requests, sold-out inventory, data-centre power slots), where recorded usage understates the busiest sites |
| Domain | Municipal EV infrastructure / transport electrification |
| Task shape | 05 · Allocation to a fixed total (24 ports across 8 sites) |
| Core method | Loss-system (M/G/c/c) demand recovery: invert observed (carried) load to offered load; grow it; allocate ports by greedy marginal reduction in lost arrivals |
| Analytical stump | Recorded sessions are censored by capacity — turned-away drivers leave no record. Treating recorded sessions or utilization as demand understates exactly the busiest sites; blocking is nonlinear in ports, so proportional allocation is wrong |
| Primary sources | City of Palo Alto EV charging station usage (2011–2020), California Energy Commission light-duty vehicle population |

## 1. The real-world situation

A city has budget for **24 additional charging ports** across its 8 public garages next year. The sustainability team
ranked garages by sessions per port and by utilization (occupied hours ÷ available hours) and proposed adding ports
roughly in proportion to sessions. The garages that are full every weekday at lunchtime looked only "moderately busy"
in the data — because drivers who find every port occupied simply drive on, and no session is ever recorded.

## 2. The decision (one deterministic recommendation)

**How many of the 24 ports does each garage receive?**

Planning rules (folder memo):

* Design window: weekdays (non-holiday) 08:00–18:00 in 2019. A port is occupied from plug-in to unplug (the session's
  total duration), not only while charging.
* Drivers arrive at each garage as a Poisson process. A driver who finds every port occupied leaves; no record is created.
  Plan for the drivers who **want** to charge, not only those who were recorded.
* Each garage behaves as a loss system with c ports and occupancy times drawn from that garage's 2019 design-window
  sessions; only the mean occupancy time enters the blocking formula.
* Next-year demand = 2019 demand at each garage × the county's ZEV-population growth factor (2020 ÷ 2019, CEC file).
* Allocate ports one at a time to the garage with the largest reduction in expected turned-away drivers per design hour;
  ties go to the garage with the higher current blocking probability.

## 3. Why capable analysts get it wrong

* Session logs feel like demand data. At a full garage the log records only the drivers who got a port, so the busier the
  site, the more the log understates demand.
* Utilization saturates near 100% and cannot distinguish "just full" from "turning away half its drivers".
* Blocking probability falls steeply and non-linearly with each added port; spreading ports proportionally to sessions
  wastes ports where blocking is already near zero.
* Using 24-hour averages hides the weekday midday peak where blocking happens.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `EVChargingStationUsage.csv` | CSV | ~260k sessions | City of Palo Alto Open Data | City open-data terms (verify; widely republished) | Sessions with start, end, total duration, station, port |
| 2 | `palo_alto_ev_sessions_2019.parquet` | Parquet | ~60–70k | Derived extract of #1 | Same | 2019 working slice |
| 3 | `station_inventory_2019.json` | JSON | ~40 ports | Derived from #1 (distinct station/port IDs active in 2019) | Same | Ports per garage |
| 4 | `cec_light_duty_vehicle_population_2019.xlsx`, `…_2020.xlsx` | XLSX | ~50k each | California Energy Commission | Public (State of California) | ZEV counts by county |
| 5 | `us_federal_holidays_2019.csv` | CSV | ~11 | OPM | Public domain | Design-window filter |
| 6 | `erlang_loss_reference.pdf` | PDF | — | Public teaching reference on loss systems (cite) | Cite | Formula and insensitivity property |
| 7 | `garage_locations.geojson` | GeoJSON | 8 | City GIS / OpenStreetMap | ODbL if OSM | Map |
| 8 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `council_proposal_proportional.xlsx` | XLSX | 8 | Task author (the proportional proposal) | — | Baseline to beat |
| 10 | `data_dictionary.pdf` | PDF | — | City of Palo Alto | Same | Field meanings |

## 5. Deterministic solution path

1. Filter 2019 design-window sessions by start time; assign sessions to garages; count ports per garage.
2. Per garage: λ_obs = sessions ÷ design hours; E[S] = mean total duration (hours); carried load a_c = λ_obs × E[S].
3. Solve offered load a from a × (1 − B(c, a)) = a_c (Erlang B), giving λ_offered = a ÷ E[S].
4. Grow: a′ = g × a with g from the CEC county ZEV counts.
5. Greedy allocation of 24 ports by marginal reduction in λ′ × B(c, a′); report final allocation, blocking before/after,
   turned-away drivers per design hour before/after.

## 6. Wrong paths (method errors, not misreadings)

**A — recorded sessions as demand.** Using a_c instead of a understates offered load most at saturated garages; they
receive too few ports.

**B — utilization ranking / proportional split.** Ignores the convexity of blocking; ports pile into large but
uncongested garages.

**C — 24-hour or all-days rates.** Dilutes the peak; every garage looks fine; allocation flattens.

**D — charging time as occupancy.** Understates service time (idle plugged-in time occupies the port).

## 7. Why the stump is analytical, not semantic

Every term is defined in the memo: what occupies a port, what happens to blocked drivers, the design window, the growth
factor. A solver who reads all of it correctly still has to recognize that the recorded arrivals are the *carried* stream
and invert the loss formula. Skipping that inversion — not misreading a field — is what produces the wrong allocation.

## 8. Draft task prompt (prose)

> We can add twenty-four ports across our eight garages before next year. Using the 2019 charging sessions and the
> planning memo in the folder, work out how much demand each garage really has in the weekday design window — including
> drivers who were turned away because every port was busy — grow it for next year, and allocate the ports one at a time
> where each one prevents the most turned-away drivers. Give me `port_allocation.csv` with one row per garage (ports
> today, recorded arrivals per hour, mean occupancy, recorded and true offered load, blocking now and after, ports added),
> `blocking_curves.png` showing each garage's blocking probability against number of ports with today's and the new
> port count marked, and a one-page `allocation_memo.pdf` comparing our allocation with the proportional proposal and
> stating how many turned-away drivers per design hour each plan leaves.

## 9. Deliverables

* `port_allocation.csv`, `blocking_curves.png`, `allocation_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 garages × (offered load, current blocking, ports added) = 24; total turned-away drivers before/after; proportional
  plan comparison; growth factor.

## 11. Golden-output checklist

* Design-window filter; total duration as occupancy; Erlang-B inversion; growth; greedy marginal allocation; totals sum
  to 24.

## 12. Build notes (scope tuning)

* Confirm 2–3 garages had carried load close to capacity in 2019 (blocking > 20% after inversion) so Trap A moves ≥ 4
  ports.
* Freeze the garage-to-station mapping and port counts in `station_inventory_2019.json`.
