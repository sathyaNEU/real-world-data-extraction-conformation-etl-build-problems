# OS08 — Replacement market from an installed base: base ÷ mean life ignores the age profile

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Sizing replacement and refresh demand (device upgrades, battery swaps, tyre or part replacement) from an installed base that grew quickly and is still young |
| Domain | Automotive aftermarket |
| Task shape | 02 · Forecast across many periods (annual out-of-warranty battery replacement demand 2025–2030; the year a refurbishment plant reaches its 5,000-unit break-even) |
| Core method | Installed base by first-registration year (vintages) from vehicle registry snapshots, net of scrappage/export; age-specific replacement hazard h(a) from the memo's Weibull parameters; annual demand = Σ_vintage survivors × h(age); comparison with base ÷ mean life |
| Analytical stump | A young, fast-growing EV fleet has few vehicles at the ages where replacements happen; dividing the installed base by mean battery life spreads replacements evenly and grossly overstates near-term demand. Demand arrives in waves that follow the sales curve with a lag |
| Primary sources | RDW (Netherlands vehicle authority) open data — registered vehicles with fuel type, first admission date and status |

## 1. The real-world situation

A battery-refurbishment start-up plans a plant that breaks even at 5,000 out-of-warranty battery replacements per year in the Netherlands.
The pitch deck divided the current battery-electric car fleet by an average 12-year battery life and showed break-even in 2025. An investor
asked for a vintage-based projection.

## 2. The decision (one deterministic recommendation)

**The first year (2025–2030) in which projected out-of-warranty replacements reach 5,000, with annual projections.**

Rules (investment memo):

* Fleet: RDW registered passenger cars with fuel type electricity (battery-electric), by first admission year (world or NL per memo), status
  active as of the snapshot; exported/scrapped vehicles excluded.
* Survival to future years: annual scrappage rate by age from `scrappage_by_age.csv` (memo, from RDW historical status changes).
* Replacement hazard: Weibull with shape k = 3.5 and scale λ = 14 years for battery replacement need; out-of-warranty = age > 8 years (warranty
  replacements excluded).
* New sales 2025–2030 from `sales_projection.csv` (they cannot reach age 8 within the window, kept for completeness).
* Annual demand in year Y = Σ_vintages survivors(Y) × [F(age) − F(age − 1)] ÷ [1 − F(age − 1)] for ages > 8.
* Break-even year = first Y with demand ≥ 5,000; "not reached" if none.

## 3. Why capable analysts get it wrong

* Base ÷ life is the textbook steady-state flow.
* Steady state requires a stable age distribution; growth markets are far from it.
* Warranty coverage removes early replacements from the addressable market.
* Scrappage before replacement age must be netted out.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Open_Data_RDW_Gekentekende_voertuigen.csv` (extract) | CSV | ~16M vehicles (passenger extract ~9M) | RDW Open Data | CC0 | Vehicles, first admission, status |
| 2 | `Open_Data_RDW_Gekentekende_voertuigen_brandstof.csv` | CSV | ~16M | RDW Open Data | CC0 | Fuel type |
| 3 | `rdw_data_dictionary.pdf` | PDF | — | RDW | CC0 | Fields |
| 4 | `scrappage_by_age.csv` | CSV | ~25 | Task author (derived from RDW status changes) | CC0-derived | Survival |
| 5 | `sales_projection.csv` | CSV | 6 | Task author | — | Future sales |
| 6 | `battery_hazard_parameters.json` | JSON | — | Task author (from published battery-durability studies; cite) | — | Weibull |
| 7 | `investment_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `pitch_deck_sizing.xlsx` | XLSX | 6 | Task author | — | Naive sizing |
| 9 | `bev_vintages.parquet` | Parquet | ~15 | Derived | CC0 | Fleet by vintage |

## 5. Deterministic solution path

1. Join vehicles and fuel; filter BEV passenger cars active; count by vintage.
2. Project survivors by vintage to 2025–2030.
3. Conditional replacement hazards for out-of-warranty ages; annual demand.
4. Break-even year; contrast with base ÷ life.

## 6. Wrong paths (method errors, not misreadings)

**A — base ÷ mean life.** Overstated near-term demand.

**B — unconditional Weibull density instead of conditional hazard on survivors.** Misstated.

**C — including warranty-age replacements.** Not addressable.

**D — no scrappage.** Overstated survivors.

## 7. Why the stump is analytical, not semantic

The registry, survival and hazard rules are specified. The trap is stock-to-flow conversion in a non-steady-state population.

## 8. Draft task prompt (prose)

> When does Dutch out-of-warranty battery replacement demand reach our 5,000-unit break-even? Project it by vintage from RDW registrations as
> the investment memo specifies. Provide `replacement_projection.csv` (year: survivors by age band, demand), `demand_vs_deck.png`, and a one-page
> `break_even_year.pdf`.

## 9. Deliverables

* `replacement_projection.csv`, `demand_vs_deck.png`, `break_even_year.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 annual demands; vintage counts (10); hazards at 6 ages; break-even year; deck contrast.

## 11. Golden-output checklist

* Fleet filter; vintage counts; survival; conditional hazard; warranty cut; break-even.

## 12. Build notes (scope tuning)

* Record the RDW snapshot date; confirm the deck's method reaches break-even ≥ 3 years earlier.
