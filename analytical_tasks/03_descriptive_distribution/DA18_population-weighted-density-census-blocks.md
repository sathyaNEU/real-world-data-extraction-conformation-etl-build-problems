# DA18 — How dense is a metro for the people who live there? Area density averages in empty land

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Site-selection and network-planning teams (delivery, ride-hail, telecom) that need density *as experienced by customers*; capacity teams comparing request-weighted with time-averaged utilisation |
| Domain | Urban analytics / site selection |
| Task shape | 01 · Ranked list under a cap (the 5 metros chosen for a dense-urban delivery pilot) |
| Core method | Population-weighted density: Σ_i p_i × (p_i ÷ a_i) ÷ Σ p_i over census blocks (land area only), computed from blocks aggregated to tracts per the memo to limit differential-privacy noise; comparison with total population ÷ total area |
| Analytical stump | Metro density computed as population over area is dominated by empty land at the fringe; metros with large rural counties look sparse. The density a typical resident experiences is a population-weighted average. Using raw 2020 block counts amplifies disclosure-avoidance noise in tiny blocks; aggregation to a stable unit is required |
| Primary sources | 2020 Census Redistricting Data (P.L. 94-171) block-level population and land area; Census CBSA delineation files |

## 1. The real-world situation

A delivery company will pilot a dense-urban service in **5** metropolitan areas. The strategy deck ranked metros by population per square
mile of the CBSA. Operations noted that several metros at the top of the list had sprawling low-density footprints with dense cores, while
compact metros with large rural counties ranked low.

## 2. The decision (one deterministic recommendation)

**The 5 metros selected (highest population-weighted density at tract level), and the 6th.**

Rules (strategy memo):

* Metros: the 50 most populous CBSAs (2020).
* Units: 2020 census tracts (blocks summed to tracts to reduce disclosure-avoidance noise per the memo), land area only (ALAND).
* Population-weighted density PWD = Σ_t P_t × (P_t ÷ A_t) ÷ Σ_t P_t, A in square miles.
* Eligibility: metros where ≥ 30% of residents live in tracts with density ≥ 10,000 per square mile.
* Rank eligible metros by PWD; top 5; report #6.
* Report conventional density (Σ P ÷ Σ A) and block-level PWD for contrast.

## 3. Why capable analysts get it wrong

* Population over area is the standard published density.
* It describes land, not people; experienced density weights each person by their own neighbourhood's density.
* Block-level counts in 2020 include disclosure-avoidance noise that is large relative to tiny blocks.
* Water area must be excluded.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–51 | `<st>2020.pl.zip` (state P.L. 94-171 files, 50 states + DC) | Pipe-delimited text (geo header + segments) | ~8.1M blocks total | U.S. Census Bureau | U.S. Gov public domain | Block population, land area |
| 52 | `2020_PL94-171_technical_documentation.pdf` | PDF | — | Census Bureau | Public domain | File layout, disclosure avoidance |
| 53 | `list1_2023.xlsx` (CBSA delineation) | XLSX | ~1.9k | Census Bureau / OMB | Public domain | County → CBSA |
| 54 | `strategy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 55 | `strategy_deck_density.xlsx` | XLSX | 50 | Task author | — | Conventional ranking |
| 56 | `tract_pop_area.parquet` | Parquet | ~85k | Derived | Public domain | Tract aggregates |
| 57 | `das_noise_note.pdf` | PDF | — | Census Bureau (cite) | Public domain | Disclosure avoidance context |

## 5. Deterministic solution path

1. Parse geo headers; aggregate blocks to tracts (population, land area).
2. Assign tracts to CBSAs via county codes; top 50 CBSAs.
3. PWD, conventional density, eligibility share; rank; top 5 + #6.
4. Block-level PWD contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — conventional density.** Fringe land dominates.

**B — block-level PWD.** Noise in tiny blocks inflates extremes.

**C — total area including water.** Coastal metros distorted.

**D — mean of tract densities (unweighted).** Neither land nor people.

## 7. Why the stump is analytical, not semantic

Units, formulas and eligibility are specified. The trap is the weighting basis and noise at small geographies.

## 8. Draft task prompt (prose)

> Which five metros should host the dense-urban delivery pilot? Rank the top 50 metros by population-weighted density as the strategy memo
> defines it, with the eligibility test. Provide `metro_density.csv` (metro: population, conventional density, tract PWD, block PWD, share in
> dense tracts, rank), `density_comparison.png`, and a one-page `pilot_metros.pdf`.

## 9. Deliverables

* `metro_density.csv`, `density_comparison.png`, `pilot_metros.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 metros + #6; PWD for 10 metros; eligibility for 6; deck contrast; block-level contrast.

## 11. Golden-output checklist

* Land area; tract aggregation; CBSA mapping; PWD formula; eligibility; ranking.

## 12. Build notes (scope tuning)

* Confirm at least two of the deck's top five fail eligibility or drop out under PWD.
