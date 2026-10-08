# OS37 — Who can use a transit-pass benefit? Both ends of the commute must be near transit

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Two-sided eligibility in matching markets (both rider and destination in service area, both buyer and seller in supported regions, both endpoints on a supported network) |
| Domain | Employee benefits / urban transport |
| Task shape | 01 · Ranked list under a cap (3 employment centres where an employer coalition pilots a transit-pass programme, by eligible commuters) |
| Core method | Origin–destination commuter flows at census-block level; eligibility requires the home block and the work block each within 0.5 miles of a frequent transit stop; count eligible commuters per employment centre (sum over OD pairs whose work block lies in the centre) |
| Analytical stump | Counting workers who *live* near transit (or employees at workplaces near transit) treats one-sided access as eligibility; many such commutes have no usable transit at the other end. The product of residential and workplace coverage shares assumes independence. Pair-level OD data give the joint condition directly |
| Primary sources | U.S. Census LEHD Origin–Destination Employment Statistics (LODES) OD files; GTFS feeds for frequent-network stops |

## 1. The real-world situation

An employer coalition will pilot a subsidised transit pass in **3** employment centres. The programme team ranked centres by the number of jobs
within half a mile of frequent transit. Planners noted that many of those workers live far from transit.

## 2. The decision (one deterministic recommendation)

**The 3 centres piloting the programme, ranked by commuters whose home and work blocks are both within 0.5 miles of a frequent stop, and the
4th.**

Rules (programme memo):

* Data: LODES8 OD main and aux files for the state(s) in memo, latest year; all jobs (JT00) with S000 counts.
* Frequent stops: stops served at ≤ 15-minute headways in the weekday 07:00–09:00 peak, computed from the regional GTFS feeds (memo's
  algorithm); block internal points within 0.5 miles (great-circle) are "near".
* Employment centres: polygons in `employment_centres.geojson` (8 candidates).
* Eligible commuters per centre = Σ S000 over OD pairs with work block in the centre, both blocks near.
* Rank; top 3; report #4; report one-sided counts for contrast.

## 3. Why capable analysts get it wrong

* Workplace-side coverage is easy to compute and looks like the employer's lever.
* Commute use requires transit at the home end too.
* Coverage at the two ends is correlated (urban cores), so multiplying shares is wrong.
* Frequent-network definition matters; any stop is not useful.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `<st>_od_main_JT00_<year>.csv.gz` | CSV | ~5–10M OD pairs | Census LEHD LODES8 | U.S. Gov public domain | In-state OD flows |
| 2 | `<st>_od_aux_JT00_<year>.csv.gz` | CSV | ~1M | Census LEHD | Public domain | Out-of-state residents |
| 3 | `<st>_xwalk.csv.gz` | CSV | ~200k | Census LEHD | Public domain | Block geography |
| 4 | `gtfs_<agency>.zip` (regional agencies) | GTFS (CSV) | ~10–20 files each | Agencies' public GTFS feeds | Agency licences (open; verify) | Stops and schedules |
| 5 | `employment_centres.geojson` | GeoJSON | 8 | Task author | — | Candidate centres |
| 6 | `programme_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `workplace_coverage_ranking.xlsx` | XLSX | 8 | Task author | — | Naive ranking |
| 8 | `frequent_stops.csv` | CSV | ~3k | Derived | Open | Frequent stops |
| 9 | `lodes_technical_document.pdf` | PDF | — | Census LEHD | Public domain | Definitions |

## 5. Deterministic solution path

1. Compute frequent stops from GTFS; near-flags for blocks.
2. Filter OD pairs to work blocks in each centre; apply both-ends flags; sum.
3. Rank; top 3 + #4; one-sided contrasts.

## 6. Wrong paths (method errors, not misreadings)

**A — workplace-side coverage only.** Overstated.

**B — product of shares.** Independence assumed.

**C — any stop instead of frequent stops.** Overstated.

**D — ignoring aux file.** Cross-state commuters missed.

## 7. Why the stump is analytical, not semantic

Data and rules are specified. The trap is one-sided eligibility in a two-sided match.

## 8. Draft task prompt (prose)

> Which three employment centres should pilot the transit-pass benefit? Count commuters with frequent transit at both ends from LODES, as the
> programme memo specifies. Provide `centre_eligibility.csv` (centre: jobs, workplace-near, both-ends eligible, rank), `od_eligibility_map.png`, and
> a one-page `pilot_centres.pdf`.

## 9. Deliverables

* `centre_eligibility.csv`, `od_eligibility_map.png`, `pilot_centres.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 centres × 3 counts = 24; ranking; #4; frequent-stop count; contrast.

## 11. Golden-output checklist

* Frequent-stop algorithm; near flags; OD filtering; both-ends rule; ranking.

## 12. Build notes (scope tuning)

* Confirm the workplace-coverage leader is not first on both-ends eligibility.
