# DS34 — Removing bus stops: count the riders who save time, not the stops with few boardings

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Removing low-usage features or locations (retiring app features, closing branches, pruning SKUs) where the benefit accrues to many other users and the cost falls on a few |
| Domain | Public transit operations |
| Task shape | 01 · Ranked list under a cap (stops removed on one route, up to 12, by net rider-minutes saved) |
| Core method | For each candidate stop: riders on board passing the stop × time saved per avoided stop (dwell + acceleration/deceleration, memo values, × probability the bus would have stopped) minus boarding/alighting riders at the stop × added walking time to the nearest remaining stop (walk distance difference ÷ walk speed); select greedily by net benefit, re-evaluating neighbours after each removal; spacing and accessibility constraints |
| Analytical stump | Removing stops with the fewest boardings ignores that stops on busy segments delay many through-riders, while a low-boarding stop at the end of a line saves little. Net rider-minutes depend on through-load, stop probability and walking penalties; removals interact (neighbouring stops) |
| Primary sources | Chicago Transit Authority (CTA) bus stop boardings (average weekday boardings and alightings by stop; Chicago Data Portal); CTA GTFS |

## 1. The real-world situation

A transit agency plans to consolidate stops on a busy bus route to speed up service. The draft list removed the 12 stops with the lowest daily
boardings. Riders' groups objected that some removed stops served older riders, and planners noted that several busy segments with closely spaced
stops were untouched.

## 2. The decision (one deterministic recommendation)

**The stops removed (up to 12) maximising net rider-minutes saved per weekday under the spacing and accessibility constraints, and the stops on the
draft list that are not removed.**

Rules (service memo):

* Data: CTA average weekday boardings and alightings by stop for the route (both directions) from the stop-level ridership file; stop sequence and
  coordinates from GTFS.
* Through-load at a stop = cumulative boardings − alightings upstream (direction-specific).
* Time saved per avoided stop = 25 seconds × P(stop requested) where P = 1 − exp(−(boardings + alightings) ÷ trips per day) (memo's Poisson
  approximation).
* Walking penalty: added distance to the nearest remaining stop (along the street, approximated by great-circle × 1.2) ÷ 1.2 m/s for that stop's
  boarding + alighting riders.
* Net benefit = through riders × time saved − walking penalty; constraints: spacing after removal ≤ 400 m; stops adjacent to hospitals/senior
  centres (memo list) cannot be removed.
* Greedy: remove the highest positive net benefit; recompute neighbours; repeat up to 12.

## 3. Why capable analysts get it wrong

* Low boardings is an intuitive signal of a "useless" stop.
* Benefits accrue to through-riders; costs to users of the stop.
* Probability that a bus actually stops matters.
* Removals change neighbours' walking penalties and spacing.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `CTA_-_Ridership_-_Avg._Weekday_Bus_Stop_Boardings.csv` | CSV | ~11k stops | Chicago Data Portal (CTA) | City of Chicago data terms (open) | Boardings and alightings by stop |
| 2 | `cta_gtfs.zip` | GTFS (CSV) | ~10 files | CTA developer GTFS | CTA terms (open; verify) | Stop sequence, coordinates, trips |
| 3 | `protected_stops.json` | JSON | ~10 | Task author (facility proximity) | — | Constraints |
| 4 | `service_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `draft_low_boardings_list.xlsx` | XLSX | 12 | Task author | — | Draft list |
| 6 | `stop_spacing_reference.pdf` | PDF | — | TCRP Report 19 (cite) | Public | Stop spacing guidance |

## 5. Deterministic solution path

1. Extract route stops by direction and sequence; boardings/alightings; through-loads.
2. Net benefit per stop; constraints; greedy removal with updates.
3. Final list; contrast with the draft.

## 6. Wrong paths (method errors, not misreadings)

**A — lowest boardings first.** Small benefits, wrong stops.

**B — ignoring stop probability.** Overstates savings at quiet stops.

**C — no re-evaluation after removal.** Adjacent removals violate spacing or double count.

**D — ignoring direction.** Through-loads wrong.

## 7. Why the stump is analytical, not semantic

The formulas and constraints are specified. The trap is judging removals by local usage rather than system-wide rider impact.

## 8. Draft task prompt (prose)

> Which stops should we consolidate on the route? Use the net rider-minutes method with constraints in the service memo and compare with the draft list.
> Provide `stop_consolidation.csv` (stop: boardings, through-load, net benefit, removed), `route_profile.png`, and a one-page `stop_changes.pdf`.

## 9. Deliverables

* `stop_consolidation.csv`, `route_profile.png`, `stop_changes.pdf`.

## 10. Where 25+ rubric criteria come from

* Removed stops (each); net benefits for 10 stops; total minutes saved; draft contrast; constraint checks.

## 11. Golden-output checklist

* Direction handling; through-load; stop probability; walking penalty; greedy updates; constraints.

## 12. Build notes (scope tuning)

* Choose a route with dense stop spacing on its busiest segment; confirm at least half the draft list is not removed.
