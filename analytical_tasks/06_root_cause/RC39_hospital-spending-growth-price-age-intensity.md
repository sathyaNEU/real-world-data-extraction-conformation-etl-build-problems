# RC39 — Hospital spending grew 45% in a decade: more people, older people, higher prices, or more care per person?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Cost-growth decompositions for planning (cloud spend = customers × usage mix × unit price × intensity; claims cost = members × age mix × price × utilisation) |
| Domain | Healthcare economics / health-system strategy |
| Task shape | 03 · Bridge between two totals (national hospital care spending, year A → year B, bridged by population, age–sex mix, economy-wide inflation, excess medical price inflation and residual intensity) |
| Core method | Multiplicative factor decomposition as in the national health accounts: growth = population × age–sex mix index × economy-wide price × relative medical price × residual (use and intensity per age-adjusted person); age–sex mix index from per-capita spending by age–sex group at base-year relative weights; log decomposition so factors add exactly; compare with additive shortcuts |
| Analytical stump | Strategy decks deflate with consumer medical-care CPI (which tracks out-of-pocket prices) or treat ageing as the population aged 65+ share. The right deflator is the hospital services price index used by the national accounts, and the ageing effect must weight each age–sex group by its relative per-capita spending. Mixing additive percentage points with multiplicative factors leaves a residual that is then called "intensity" |
| Primary sources | CMS National Health Expenditure Accounts (historical tables by type of service; health spending by age and sex); U.S. Census Bureau population estimates by single year of age and sex; BEA personal consumption expenditure price indexes |

## 1. The real-world situation

A hospital system's strategy team presented the board with a decade of national hospital spending growth and argued that rising use per person (an
"intensity boom") justified major capacity expansion. The CFO asked for a decomposition separating population, ageing, prices and genuine intensity,
because capacity should follow use, not prices.

## 2. The decision (one deterministic recommendation)

**Whether the expansion case is supported (supported if residual intensity contributes ≥ 35% of the log growth in hospital spending), with the
five-factor decomposition.**

Rules (strategy memo):

* Spending: NHE hospital care expenditures (nominal $), years A and B.
* Population: Census resident population, July estimates, years A and B.
* Age–sex mix index: groups per the CMS age and sex tables (memo's 7 age groups × 2 sexes); relative per-capita hospital spending weights from the
  CMS age–sex table for the year closest to A; index = Σ population share_g × relative weight_g, for A and B.
* Economy-wide price: GDP implicit price deflator (BEA), A and B.
* Relative medical price: BEA PCE price index for hospital services ÷ GDP deflator.
* Residual intensity = spending growth ÷ (population × mix × GDP price × relative medical price growth).
* Contributions as shares of ln(spending_B ÷ spending_A); report each factor's average annual growth.
* Supported if intensity share ≥ 35%.

## 3. Why capable analysts get it wrong

* "Use per person" is often estimated as spending per capita adjusted by CPI medical care.
* Ageing is often measured by the 65+ share without spending weights.
* Additive decompositions of multiplicative growth leave residuals.
* Different price indexes give very different "real" growth.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `nhe_historical_tables.xlsx` | XLSX | ~3k | CMS National Health Expenditure Accounts | U.S. Government work (public domain) | Hospital care spending |
| 2 | `nhe_age_gender_tables.xlsx` | XLSX | ~500 | CMS NHE by age and sex | Public domain | Per-capita spending by group |
| 3 | `census_pop_single_year_age_sex_<years>.csv` | CSV | ~25k | Census Bureau population estimates | Public domain | Population by age and sex |
| 4 | `bea_nipa_table_2_4_4.csv` | CSV | ~4k | BEA (PCE price indexes by type of product) | Public domain | Hospital services price index |
| 5 | `bea_gdp_deflator.csv` | CSV | ~300 | BEA | Public domain | Economy-wide price |
| 6 | `strategy_memo.pdf` | PDF | — | Task author | — | Rules in §2, years, age groups |
| 7 | `board_intensity_deck.xlsx` | XLSX | — | Task author | — | CPI-deflated per-capita analysis |

## 5. Deterministic solution path

1. Extract hospital spending, population by group, price indexes for A and B.
2. Age–sex mix index with base weights.
3. Factor growths; residual intensity; log shares.
4. Decision; contrast with the CPI-deflated per-capita deck.

## 6. Wrong paths (method errors, not misreadings)

**A — CPI medical care deflator.** Measures consumer out-of-pocket prices, not hospital service prices.

**B — 65+ share as ageing.** Ignores spending differences among groups and sexes.

**C — additive percentage points.** Leaves a residual that is misread as intensity.

**D — nominal per-capita growth as intensity.** Folds prices into use.

## 7. Why the stump is analytical, not semantic

The indexes, groups and formulas are specified. The trap is the choice of deflator and the construction of the ageing index.

## 8. Draft task prompt (prose)

> Our strategy deck says an intensity boom justifies expansion. Decompose national hospital spending growth with the strategy memo's factor method
> and tell me whether the case holds. Provide `spending_factors.csv` (factor: annual growth, share of log growth), `spending_factor_bridge.png`, and a
> one-page `expansion_case_note.pdf`.

## 9. Deliverables

* `spending_factors.csv` — five factors with growth rates and shares.
* `spending_factor_bridge.png` — stacked log-growth bar by factor.
* `expansion_case_note.pdf` — decision and why the deck's per-capita analysis overstates intensity.

## 10. Where 25+ rubric criteria come from

* Inputs (spending, population, two price indexes) for A and B: 8.
* Mix index construction (group shares, weights, index values): 4.
* Factor growths and log shares (5): 10.
* Decision: 1.
* Contrasts (CPI deflator, 65+ share): 3+.

## 11. Golden-output checklist

* Hospital care line; July population estimates.
* Base-year relative weights; 14 groups.
* Hospital services PCE price relative to GDP deflator; log shares.

## 12. Build notes (scope tuning)

* Choose A and B a decade apart within the available tables; confirm the intensity share falls below 35% with the memo's deflator while the deck's
  method shows it above.
