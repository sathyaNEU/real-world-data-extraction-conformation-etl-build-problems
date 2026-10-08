# OS13 — New fast-charging sites: count the people newly covered, not everyone within reach

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Network-coverage expansion (cell sites, delivery zones, store and locker networks) where catchments overlap with existing coverage |
| Domain | EV infrastructure |
| Task shape | 01 · Ranked list under a cap (4 sites funded from 15 candidates by incremental population covered, chosen greedily) |
| Core method | Coverage as the union of catchments (population of census blocks whose centroid lies within 10 road-proxy miles of any DC fast charger); incremental coverage of a candidate = population covered after adding it − before; greedy sequential selection (submodular coverage) |
| Analytical stump | Summing each candidate's catchment population double counts people already within reach of existing chargers and people covered by two candidates. Choosing the top four by standalone population picks clustered sites near cities; greedy incremental coverage picks gap-filling sites |
| Primary sources | U.S. DOE Alternative Fuels Data Center (AFDC) station locations; Census 2020 block populations |

## 1. The real-world situation

A state energy office funds **4** DC fast-charging sites from 15 candidate locations to maximise the number of residents newly within 10 miles
of a fast charger. The draft scored each candidate by population within 10 miles and funded the top four — three of them near the same metro
area that already has many chargers.

## 2. The decision (one deterministic recommendation)

**The 4 funded sites (greedy incremental coverage), the population newly covered by each in selection order, and the 5th site.**

Rules (energy office memo):

* Existing coverage: AFDC public DC fast stations (EV network, DC fast count ≥ 1, status available) in the state and within 10 miles of the
  border, as of the snapshot date.
* Population: 2020 census block populations (P.L. 94-171) with block internal points.
* Distance: great-circle × 1.25 (road proxy per memo) ≤ 10 miles.
* Incremental coverage of a candidate given current set = Σ population of blocks within 10 miles of it and not within 10 miles of any station
  in the set.
* Greedy: pick the max incremental; update; repeat 4 times; report the 5th pick.
* Report standalone catchment populations for contrast.

## 3. Why capable analysts get it wrong

* Catchment population is easy and intuitive.
* Overlaps with existing and other new sites make populations non-additive.
* Coverage is a set function; sequential selection matters.
* Border stations in neighbouring states also cover residents.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `alt_fuel_stations (<date>).csv` | CSV | ~80k | DOE AFDC station locator | U.S. Gov public domain | Station locations, types |
| 2 | `<st>2020.pl.zip` (state P.L. 94-171) | Pipe-delimited | ~200k blocks | Census Bureau | Public domain | Block populations |
| 3 | `block_internal_points.parquet` | Parquet | ~200k | Census TIGER | Public domain | Coordinates |
| 4 | `candidate_sites.csv` | CSV | 15 | Task author | — | Candidates |
| 5 | `energy_office_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `draft_catchment_ranking.xlsx` | XLSX | 15 | Task author | — | Draft scores |
| 7 | `afdc_field_definitions.pdf` | PDF | — | DOE | Public domain | Fields |
| 8 | `max_coverage_reference.pdf` | PDF | — | Church & ReVelle (cite) | Cite | Maximal covering |

## 5. Deterministic solution path

1. Filter existing DC fast stations; compute currently covered blocks.
2. For each candidate, incremental coverage; greedy picks with updates.
3. Report picks, increments, 5th site; contrast with standalone ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — standalone catchment ranking.** Double counts.

**B — ignoring existing coverage.** Picks already-served areas.

**C — no update after each pick.** Two adjacent candidates both chosen.

**D — excluding out-of-state stations.** Overstates gaps near borders.

## 7. Why the stump is analytical, not semantic

Coverage, distance and selection are specified. The trap is non-additivity of overlapping coverage.

## 8. Draft task prompt (prose)

> Which four candidate sites should we fund to bring the most new residents within 10 miles of a fast charger? Use incremental coverage with
> greedy selection as the energy office memo specifies. Provide `site_selection.csv` (site: standalone population, incremental at each round,
> pick order), `coverage_map.png`, and a one-page `funding_awards.pdf`.

## 9. Deliverables

* `site_selection.csv`, `coverage_map.png`, `funding_awards.pdf`.

## 10. Where 25+ rubric criteria come from

* 15 candidates' round-1 increments; increments in rounds 2–4 for remaining candidates (sampled); picks; 5th; totals; contrast.

## 11. Golden-output checklist

* Station filter; border stations; distance proxy; incremental logic; greedy updates.

## 12. Build notes (scope tuning)

* Include clustered metro candidates and rural gap candidates; confirm the draft funds at least two different sites.
