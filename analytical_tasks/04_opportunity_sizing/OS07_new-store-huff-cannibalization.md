# OS07 — Sizing a new grocery store: the radius counts people your other stores already serve

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Retail and restaurant site selection at chains (incremental sales net of cannibalisation), dark-store and locker network expansion |
| Domain | Retail / food access |
| Task shape | 01 · Ranked list under a cap (2 sites chosen from 8 candidates by incremental chain sales) |
| Core method | Huff gravity model: probability that residents of block group i shop at store j ∝ size_j^α ÷ distance_ij^β, normalised across all stores (competitors and own); new-site sales = Σ_i demand_i × P_ij; incremental chain sales = new-site sales − own-store sales lost (recomputed probabilities) |
| Analytical stump | Counting the population within a radius of a candidate site (and multiplying by spend per head) ignores competitors and the chain's own nearby stores. A site next to an existing store "wins" on radius demand but mostly takes sales from itself; incremental sales rank sites differently |
| Primary sources | USDA FNS SNAP-authorised retailer data (historical store locations and types); Census block group population and income |

## 1. The real-world situation

A regional grocery chain will open **2** stores among 8 candidate sites. The real-estate team ranked sites by grocery spend within a 3-mile
radius. Two top sites are within 4 miles of existing chain stores. Finance asked for incremental chain sales.

## 2. The decision (one deterministic recommendation)

**The 2 sites opened (highest incremental chain sales; the second chosen given the first is open), and the 3rd-best site.**

Rules (real-estate memo):

* Stores: SNAP-authorised supermarkets and super stores active on the reference date in the study area (store type codes in memo); the chain's
  stores identified in `chain_stores.csv`; store size proxy by type (memo table).
* Demand: block group grocery spend = population × per-capita grocery spend by income band (memo table).
* Huff: P_ij = (S_j / d_ij^β) ÷ Σ_k (S_k / d_ik^β), α = 1, β = 2, distances in road-network miles approximated by great-circle × 1.2 (memo);
  stores beyond 15 miles ignored.
* Incremental chain sales for site s = Σ_i demand_i × [Σ_{own incl. s} P_ij(with s) − Σ_{own} P_ij(without s)].
* Choose the best site; then recompute with it open to choose the second; report the third.
* Report radius-based ranking for contrast.

## 3. Why capable analysts get it wrong

* Radius demand is simple and visual.
* Shoppers choose among all nearby stores; competition reduces capture.
* Own-store cannibalisation is invisible unless own stores are in the model.
* Sequential choice matters: two adjacent candidates cannibalise each other.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `historical_snap_retailer_data.csv` | CSV | ~650k | USDA FNS SNAP retailer data | U.S. Gov public domain | Store locations, types, authorisation dates |
| 2 | `cbg_population_income.csv` | CSV | ~8k (study area) | Census ACS 5-year (block group) | Public domain | Demand inputs |
| 3 | `cbg_centroids.csv` | CSV | ~8k | Census TIGER | Public domain | Locations |
| 4 | `chain_stores.csv` | CSV | ~25 | Task author | — | Own stores |
| 5 | `candidate_sites.csv` | CSV | 8 | Task author | — | Candidates |
| 6 | `store_size_proxy.json` | JSON | ~6 | Task author | — | Size by store type |
| 7 | `grocery_spend_by_income.json` | JSON | ~8 | Task author (from BLS CE published tables) | Public | Spend per head |
| 8 | `real_estate_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `radius_ranking.xlsx` | XLSX | 8 | Task author | — | Naive ranking |
| 10 | `huff_1964_citation.pdf` | PDF | — | Cite | Cite | Model |

## 5. Deterministic solution path

1. Select active supermarkets on the reference date; assign sizes; build demand.
2. Compute baseline Huff probabilities and own-store sales.
3. For each candidate, add the site, recompute probabilities, incremental sales; pick best; repeat for second.
4. Contrast with the radius ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — radius demand.** Ignores competition and cannibalisation.

**B — new-site sales instead of incremental chain sales.** Counts cannibalised sales as gains.

**C — picking the top two independently.** Ignores mutual cannibalisation.

**D — including stores no longer authorised on the reference date.** Stale competition set.

## 7. Why the stump is analytical, not semantic

Model and parameters are specified. The trap is gross versus incremental sizing in competitive spatial demand.

## 8. Draft task prompt (prose)

> Which two candidate sites should we open? Size each by incremental chain sales with the Huff model in the real-estate memo, choosing
> sequentially. Provide `site_incrementality.csv` (site: radius demand, new-site sales, cannibalised, incremental, rank), `cannibalisation_map.png`,
> and a one-page `site_selection.pdf`.

## 9. Deliverables

* `site_incrementality.csv`, `cannibalisation_map.png`, `site_selection.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 sites × (new-site sales, cannibalised, incremental) = 24; second-round values; choices; contrast.

## 11. Golden-output checklist

* Store filter; demand; Huff normalisation; cannibalisation; sequential choice.

## 12. Build notes (scope tuning)

* Confirm at least one radius top-2 site is not chosen.
