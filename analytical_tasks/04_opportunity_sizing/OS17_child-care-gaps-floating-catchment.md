# OS17 — Child-care supply gaps: tract-by-tract shortfalls ignore that families cross tract lines

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Two-sided marketplace supply–demand gap analysis (delivery couriers per zone, rideshare drivers by area, clinic capacity) where users travel across zone boundaries |
| Domain | Early childhood services / social infrastructure |
| Task shape | 01 · Ranked list under a cap (10 census tracts for new-centre start-up grants) |
| Core method | Two-step floating catchment area (2SFCA): supply-to-demand ratio for each provider over its catchment (children within 10 miles), then accessibility for each tract = Σ ratios of reachable providers; gap = children × (target ratio − accessibility); rank by gap |
| Analytical stump | Within-tract comparisons of licensed slots versus children label tracts with no centres as deserts even when large centres sit across the boundary, and miss tracts whose nearby centres are oversubscribed by neighbours. Accessibility must account for competition for the same supply |
| Primary sources | Texas Health and Human Services child-care licensing data (Texas Open Data Portal); Census ACS children under 5 by tract |

## 1. The real-world situation

A state agency awards start-up grants to new child-care centres in **10** census tracts with the largest shortfall of licensed capacity. The
first list compared each tract's licensed slots with its children under 5. Several "desert" tracts sat next to large centres with spare
capacity, while some suburban tracts with centres were in fact underserved because the centres drew from many neighbouring tracts.

## 2. The decision (one deterministic recommendation)

**The 10 tracts receiving grants ranked by 2SFCA gap (children lacking a slot at the 0.33 slots-per-child target), and the 11th.**

Rules (agency memo):

* Supply: licensed centres and licensed homes with capacity, active status, in the metro area plus a 10-mile buffer; capacity for ages 0–5 per
  memo.
* Demand: children under 5 by tract (ACS 5-year), located at population-weighted tract centroids.
* Step 1: for each provider j, R_j = capacity_j ÷ Σ children in tracts within 10 miles (great-circle).
* Step 2: accessibility A_i = Σ R_j over providers within 10 miles of tract i.
* Gap_i = max(0, children_i × (0.33 − A_i)).
* Rank by gap; top 10; report #11; within-tract ratio ranking for contrast.

## 3. Why capable analysts get it wrong

* Within-zone supply/demand ratios are simple and map well.
* Families travel; supply is shared across zones.
* Large providers serve many tracts; their capacity must be divided by all demand in reach.
* Buffers beyond the study area matter at the edges.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `HHSC_CCL_Daycare_and_Residential_Operations_Data.csv` | CSV | ~25k operations | Texas Open Data Portal (HHSC) | Texas open data terms (public) | Providers, type, capacity, status, location |
| 2 | `acs5_b09001_tract.csv` | CSV | ~6.9k tracts | Census ACS 5-year | Public domain | Children by age |
| 3 | `tract_pop_weighted_centroids.csv` | CSV | ~6.9k | Census | Public domain | Centroids |
| 4 | `metro_tracts.json` | JSON | ~1.1k | Task author | — | Study area |
| 5 | `agency_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `within_tract_ranking.xlsx` | XLSX | ~1.1k | Task author | — | Naive ranking |
| 7 | `luo_wang_2sfca_citation.pdf` | PDF | — | Luo & Wang 2003 (cite) | Cite | Method |
| 8 | `provider_geocodes.parquet` | Parquet | ~25k | Derived | Public | Coordinates |

## 5. Deterministic solution path

1. Filter active providers with capacity; buffer area; geocodes.
2. Step 1 ratios; step 2 accessibility.
3. Gaps; rank; top 10 + #11; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — within-tract ratio.** Boundary artefacts.

**B — sum of capacity within 10 miles ÷ tract children.** Ignores competing demand.

**C — no buffer at study edges.** Edge tracts misstated.

**D — ranking by accessibility instead of gap.** Small tracts dominate.

## 7. Why the stump is analytical, not semantic

The method and parameters are specified. The trap is spatial supply–demand matching with shared supply.

## 8. Draft task prompt (prose)

> Which ten tracts should get child-care start-up grants? Measure gaps with the floating catchment method in the agency memo. Provide
> `tract_gaps.csv` (tract: children, accessibility, gap, rank), `accessibility_map.png`, and a one-page `grant_tracts.pdf` comparing with the
> within-tract list.

## 9. Deliverables

* `tract_gaps.csv`, `accessibility_map.png`, `grant_tracts.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 tracts + #11; accessibility and gaps for 12 tracts; R_j for 5 providers; contrast.

## 11. Golden-output checklist

* Provider filters; buffer; two steps; gap; ranking.

## 12. Build notes (scope tuning)

* Confirm at least four within-tract "deserts" fall out of the top 10.
