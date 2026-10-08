# OS38 — Backyard homes potential: early-adopter neighbourhoods are not the city

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Adoption sizing from early adopters (feature uptake in pilot markets, new product categories) where early uptake comes from the most receptive segments |
| Domain | Housing / construction |
| Task shape | 13 · Scenarios and the flip point (uptake rate × eligible-parcel definition → ADUs built over 5 years; the prefab ADU factory capacity committed and the uptake at which the plan breaks even) |
| Core method | Eligible parcels (single-family zoned, lot size ≥ memo threshold) from assessor data; historical ADU permits linked to parcels (one ADU per parcel; multiple permits for the same ADU deduplicated); uptake hazard by parcel segment (lot size band × assessed value band) estimated from permits since the law change; projection = Σ segments eligible parcels remaining × segment hazard; scenarios |
| Analytical stump | Applying the citywide permit rate from the first years to all eligible parcels, or worse, the rate in the hottest neighbourhoods, assumes everyone behaves like early adopters. Counting permits instead of distinct ADUs double counts revisions and phased permits. Segment hazards on the remaining risk set give a different 5-year total |
| Primary sources | City of Los Angeles building permits (LA open data); Los Angeles County Assessor parcel data (open data portal) |

## 1. The real-world situation

A prefab ADU manufacturer sizes a factory for Los Angeles. The deck took the number of ADU permits in the three busiest community plan areas
per eligible parcel and applied that rate to all eligible parcels, projecting 60,000 ADUs over five years. Investors asked for a segment-based
projection and the uptake level at which the factory breaks even.

## 2. The decision (one deterministic recommendation)

**The factory capacity committed (units per year, from 1,000 / 2,000 / 4,000) — the largest option whose utilisation is ≥ 70% in year 3 under
central uptake — and the uptake multiplier at which the next-larger option would qualify.**

Rules (investment memo):

* Parcels: LA County Assessor parcels in the City of Los Angeles with single-family use codes and lot size ≥ 5,000 sq ft.
* ADU permits: City of LA building permits with ADU work descriptions (memo's pattern list), 2017–2023; deduplicate to one ADU per parcel (the
  first issued permit).
* Segments: lot size band (3) × assessed value band (3).
* Hazard per segment-year = new ADUs ÷ parcels without an ADU at the start of the year; central hazard = average 2021–2023.
* Projection 2025–2029: risk set shrinks by ADUs built; market share for prefab = 15% (memo).
* Utilisation in year 3 = prefab ADUs in 2027 ÷ capacity; scenarios: uptake multiplier 0.5, 1.0, 1.5.
* Flip point: multiplier at which the next-larger option reaches 70%.

## 3. Why capable analysts get it wrong

* Early-adopter rates are visible and persuasive.
* Uptake differs strongly by lot size and owner wealth; segment mix matters.
* Permits are not units; duplicates inflate counts.
* Risk sets shrink as parcels adopt.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Building_and_Safety_Permit_Information.csv` | CSV | ~1.5M | City of Los Angeles Open Data | LA open data terms (public) | Permits with descriptions, APN |
| 2 | `Assessor_Parcels_Data_<year>.csv` | CSV | ~2.4M (county) | LA County Assessor open data | Public | Use codes, lot size, values |
| 3 | `adu_permit_patterns.json` | JSON | ~20 | Task author | — | ADU identification |
| 4 | `investment_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `deck_early_adopter_projection.xlsx` | XLSX | — | Task author | — | Naive projection |
| 6 | `segment_bands.json` | JSON | — | Task author | — | Bands |
| 7 | `state_adu_law_summary_citation.pdf` | PDF | — | California HCD (cite) | Public | Context |

## 5. Deterministic solution path

1. Identify eligible parcels; identify ADU permits; deduplicate per parcel.
2. Segment hazards 2017–2023; central hazards.
3. Project 2025–2029 by segment; prefab share; utilisation by option and scenario.
4. Choose capacity; flip point; contrast with the deck.

## 6. Wrong paths (method errors, not misreadings)

**A — hot-area rate applied citywide.** Overstated.

**B — permits as units.** Double counting.

**C — constant risk set.** Overstated over time.

**D — citywide average hazard without segments.** Mix effects lost.

## 7. Why the stump is analytical, not semantic

Identification, segments and projection are specified. The trap is extrapolating from early adopters and miscounting units.

## 8. Draft task prompt (prose)

> What factory capacity should we commit for LA backyard homes? Project ADU uptake by parcel segment as the investment memo specifies and test
> the uptake scenarios. Provide `adu_projection.csv` (segment × year: risk set, hazard, ADUs; option utilisation), `uptake_scenarios.png`, and a
> one-page `capacity_decision.pdf`.

## 9. Deliverables

* `adu_projection.csv`, `uptake_scenarios.png`, `capacity_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 9 segment hazards; 5 annual totals; 9 option × scenario utilisations; choice; flip point; deck contrast.

## 11. Golden-output checklist

* Parcel filters; permit patterns; dedupe; risk sets; projection; utilisation; flip point.

## 12. Build notes (scope tuning)

* Confirm the deck projects ≥ 2× the segment-based total.
