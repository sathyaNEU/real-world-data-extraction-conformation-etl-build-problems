# RC50 — Bus journeys down 9% since the new rail line opened: cannibalisation, or a market that is still smaller than before?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Product decline attribution after a sister product launches (Instagram Stories vs feed time, a new subscription tier vs the old one, a new store vs nearby stores): category shrinkage vs secular share drift vs cannibalisation |
| Domain | Public transport / network planning |
| Task shape | 03 · Bridge between two totals (bus journeys, the year before the new line opened → the latest year, bridged by category change, secular share drift and corridor cannibalisation) |
| Core method | Bus journeys = total public-transport journeys × bus share; category effect at the reference share; secular share drift measured on bus routes that do not parallel the new line; cannibalisation = the extra share change on parallel routes beyond the non-parallel routes' change; closure check against the observed bus change |
| Analytical stump | Comparing bus journeys before and after the opening blames the new line for the whole decline, but the total travel market was still smaller than before the pandemic and bus share had been drifting down for years. Without a comparison group of non-parallel routes, secular drift is misread as cannibalisation; without the category term, a smaller market is misread as lost share |
| Primary sources | Transport for London — public transport journeys by type of transport (London Datastore); TfL bus route-level journeys by period; Elizabeth line station locations and opening dates |

## 1. The real-world situation

A transport authority's bus journeys were 9% lower in the year after a new cross-city rail line opened than in the year before. A budget review
proposed cutting frequencies on bus routes that parallel the new line, on the premise that the line had taken their riders. Planners argued that
remote working had shrunk the whole market and that bus share had been eroding for a decade. Frequency cuts on the wrong routes would cost
ridership elsewhere.

## 2. The decision (one deterministic recommendation)

**Whether to cut frequencies on parallel routes (cut if cannibalisation accounts for ≥ 30% of the bus decline), with the three-component bridge.**

Rules (planning memo):

* Data: TfL journeys by type of transport (4-weekly periods), 13 periods before the opening and the latest 13 periods; route-level bus journeys
  for the same periods.
* Parallel routes: routes with ≥ 40% of their stops within 500 m of a new-line station and running between two such stations (memo's route list
  derived from TfL stop locations and station coordinates; the list is provided).
* Totals: T = journeys over all modes; B = bus journeys; share s = B ÷ T; s_P and s_N = shares for parallel and non-parallel routes (route journeys ÷
  T).
* Category effect = (T_cur − T_ref) × s_ref.
* Secular drift = T_cur × (s_N,cur − s_N,ref) × (s_ref ÷ s_N,ref), i.e. non-parallel routes' proportional share change applied to all bus journeys.
* Cannibalisation = T_cur × [(s_P,cur − s_P,ref) − s_P,ref × (s_N,cur − s_N,ref) ÷ s_N,ref].
* Residual = ΔB − sum of the three (reported; zero up to rounding when route totals sum to B).
* Cut if cannibalisation ÷ |ΔB| ≥ 30%.

## 3. Why capable analysts get it wrong

* Before/after comparisons around an opening attribute everything to the opening.
* The post-pandemic market was still recovering, so category size changed.
* Bus share had a long-run downward drift independent of the new line.
* Parallel and non-parallel routes need a comparison to isolate cannibalisation.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `tfl-journeys-type.xlsx` | XLSX | ~200 periods × 8 modes | London Datastore (TfL public transport journeys by type of transport) | Open Government Licence v2.0 (London Datastore; verify) | Journeys by mode |
| 2 | `bus_route_journeys_<periods>.csv` | CSV | ~35k (route × period) | TfL open data (bus route-level usage; verify availability) | TfL open data terms (attribution) | Route journeys |
| 3 | `bus_stops.csv` | CSV | ~19k | TfL open data (bus stop locations) | TfL open data terms | Stop coordinates |
| 4 | `elizabeth_line_stations.geojson` | GeoJSON | ~41 | TfL open data | TfL open data terms | Station locations |
| 5 | `parallel_routes.csv` | CSV | ~60 | Task author (derived from files 3–4 with the memo rule) | — | Route classification |
| 6 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `budget_review_proposal.xlsx` | XLSX | — | Task author | — | Before/after comparison |

## 5. Deterministic solution path

1. Assemble period totals by mode; route journeys; validate that route totals sum to published bus journeys (report the gap).
2. Classify routes (or verify the provided list against the rule).
3. Compute shares; the three components; residual.
4. Decision; contrast with the budget review's before/after comparison.

## 6. Wrong paths (method errors, not misreadings)

**A — before/after bus journeys.** The whole decline attributed to the new line.

**B — share change without a comparison group.** Secular drift counted as cannibalisation.

**C — journeys without the category term.** A smaller market read as lost share.

**D — pre-pandemic baseline.** Compares with 2019 and attributes the pandemic loss to the new line.

## 7. Why the stump is analytical, not semantic

Route classification is geometric with a provided list; the formulas are fixed. The trap is separating category, drift and cannibalisation.

## 8. Draft task prompt (prose)

> The budget review wants to cut buses that parallel the new line because bus journeys fell 9%. Bridge the decline with the planning memo's method and
> tell me whether the cuts are justified. Provide `bus_decline_bridge.csv` (component: journeys, share), `bus_decline_waterfall.png`, and a one-page
> `frequency_decision.pdf`.

## 9. Deliverables

* `bus_decline_bridge.csv` — category, secular drift, cannibalisation, residual; shares by route group.
* `bus_decline_waterfall.png` — waterfall from reference to current bus journeys.
* `frequency_decision.pdf` — decision and why the before/after comparison misleads.

## 10. Where 25+ rubric criteria come from

* Period totals by mode (T and B, both windows): 4.
* Route-total reconciliation: 2.
* Route classification check: 2.
* Shares s, s_P, s_N in both windows: 6.
* Three components and residual: 5.
* Decision: 1.
* Contrasts (before/after, pre-pandemic baseline): 4.
* Chart elements: 2+.

## 11. Golden-output checklist

* 13-period windows; route classification rule.
* Shares relative to total journeys T.
* Component formulas and closure.

## 12. Build notes (scope tuning)

* If route-level journeys are not published for the needed periods, use the route-level boarding data TfL releases under its open data or FOI
  disclosure log and record the source; confirm cannibalisation is below 30% of the decline.
