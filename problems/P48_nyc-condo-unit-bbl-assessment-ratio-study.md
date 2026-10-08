# P48 — Condo assessment uniformity in New York City: unit lots vs billing lots and the package sale repeated on every unit

| Field | Value |
|---|---|
| Domain | Property tax administration / real-estate valuation / municipal data |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (five neighborhoods re-reviewed) |
| Core technique | Hierarchical parcel-key conformance (condo unit BBL ↔ billing BBL); multi-parcel ("package") sale reconstruction; arm's-length screening; IAAO ratio-study statistics with trimming |
| Trap family (honest data) | Unit-lot sales joined to billing-lot (whole-building) values; package price counted on each unit; nominal/$0 transfers kept; COD computed without trimming or on means |
| Primary sources | NYC Department of Finance rolling/annualized sales, DOF property assessment roll, Digital Tax Map condominium tables, PLUTO; IAAO Standard on Ratio Studies |

## 1. The real-world project

NYC's assessor's quality team runs a **ratio study** on residential condominium sales: for each neighborhood, compare
each unit's assessed market value with its sale price and measure uniformity with the coefficient of dispersion (COD).
The team can re-review **five neighborhoods** per cycle — the five with the worst COD. An analyst joined sales to PLUTO by
BBL. Most condo sales failed to join (unit lots are not in PLUTO); the ones that did — via a billing-lot workaround — had
ratios above 100.

## 2. The business decision (one deterministic recommendation)

**Which five neighborhoods are re-reviewed (highest COD among neighborhoods with ≥ 30 qualifying sales), and which is
sixth?**

Rules (ratio-study procedure, following the IAAO Standard on Ratio Studies):

* Sales: DOF annualized sales for the study year, building class categories for condominium residential units (codes listed),
  sale price > $10,000 (nominal and $0 transfers excluded).
* Parcel key: sale `BLOCK`/`LOT` → unit BBL. Assessed market value comes from the assessment roll **for the same unit BBL**
  (condo units have their own lots, typically 1001+; the billing lot, typically 7501+, represents the whole condominium).
  Unit lots are mapped to their condominium via the Digital Tax Map condo table only for building attributes, never for value.
* Package sales: rows with the same sale date, same price and the same condominium (billing BBL) with more than one unit lot
  are **one sale**: ratio = Σ unit market values ÷ the single price.
* Ratio = assessed market value ÷ sale price. Per neighborhood, trim ratios outside Q1 − 1.5·IQR … Q3 + 1.5·IQR, then COD =
  100 × mean(|ratio − median|) ÷ median.
* Rank by COD descending among neighborhoods with ≥ 30 sales after trimming.

## 3. Why this gets overlooked in real projects

* BBL is "the" NYC property key, but condominiums have two kinds: one billing lot per condo and one lot per unit. PLUTO and
  many tools are lot-level for billing lots only.
* Sales files repeat the total price of a multi-unit deed on each unit row; each looks like an independent sale.
* $0 and $10 transfers (family transfers, LLC restructurings) are common.
* COD is sensitive to outliers; the standard specifies trimming, which casual analyses skip.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–5 | `2023_manhattan.xlsx`, `2023_brooklyn.xlsx`, `2023_queens.xlsx`, `2023_bronx.xlsx`, `2023_statenisland.xlsx` | XLSX | 5k–25k each | NYC DOF Annualized Sales | NYC open data terms | Sales |
| 6 | `property_valuation_assessment_fy2024.csv` (assessment roll incl. condo unit lots) | CSV | ~1.1M+ | NYC DOF via NYC Open Data | NYC open data terms | Market values by BBL |
| 7 | `dtm_condominium_units.csv` | CSV | ~200k+ | NYC DOF Digital Tax Map (NYC Open Data) | NYC open data terms | Unit BBL → condo/billing BBL |
| 8 | `pluto_24v1.csv` | CSV | ~860k | NYC DCP PLUTO | NYC open data terms | Billing-lot attributes (tempting join) |
| 9 | `rolling_sales_glossary.pdf` | PDF | — | NYC DOF | Public | Field definitions, $0 sales note |
| 10 | `iaao_standard_on_ratio_studies.pdf` (excerpt/citation) | PDF | — | IAAO (copyright; cite, quote sparingly) | Cite | COD, trimming |
| 11 | `building_class_codes.csv` | CSV | ~200 | NYC DOF | Public | Condo class codes |
| 12 | `ratio_study_procedure.pdf` | PDF | — | Task author | — | Rules in §2 |

## 5. Deterministic solution path

1. Load sales; filter condo residential classes and price > $10,000; build unit BBLs.
2. Map unit BBL → condo billing BBL via the DTM table; detect package sales; collapse packages.
3. Join unit BBLs to the assessment roll; sum for packages; compute ratios.
4. Trim per neighborhood; compute medians and COD; apply the 30-sale floor; rank; five + sixth.
5. Contrast: PLUTO/billing-lot join; packages as separate sales; untrimmed COD.

## 6. The traps

**Trap A — billing-lot values.** Ratios in the hundreds; COD meaningless; wrong neighborhoods.

**Trap B — packages per unit.** Each unit's value over the whole package price → ratios far too low; COD inflated in new-
development neighborhoods.

**Trap C — nominal transfers kept.** Extreme ratios.

**Trap D — no trimming / mean-based COD.** Rankings driven by a handful of outliers.

## 7. Why the data is honest

DOF's sales and assessment records are official; the condominium lot structure and package-deed listing are documented
features of NYC's tax map. The procedure defines how to handle them.

## 8. Draft task prompt (prose)

> We can re-review five neighborhoods this cycle: the five with the worst condominium assessment uniformity (COD) in
> 2023 sales, following the ratio-study procedure in the folder. Using the DOF sales, assessment roll and tax-map files,
> compute every qualifying neighborhood's median ratio and COD and tell me the five and the sixth. Deliver
> `condo_ratio_study.xlsx` (sale-level ratios with package flags and trim flags; neighborhood summary with sales count,
> median ratio, COD, rank) and `condo_cod_chart.png`, ranked bars of COD with the top five highlighted and the IAAO
> reference level drawn. On the first sheet, give the five, the COD gap between fifth and sixth, and how many sales were
> collapsed as packages.

## 9. Deliverables

* `condo_ratio_study.xlsx`, `condo_cod_chart.png`.

## 10. Where 25+ rubric criteria come from

* 5 neighborhoods + 6th + gap; COD and median ratio for ~12 neighborhoods; package count; trimmed counts; join coverage.

## 11. Golden-output checklist

* Unit-BBL values; packages collapsed; nominal sales excluded; IQR trimming; COD per standard; decision stated.

## 12. Build notes (scope tuning)

* Verify that the assessment dataset contains condo unit lots with market values for the roll year; if not, use DOF's
  condo-unit valuation dataset and adjust the procedure.
* Choose a year with significant new-development package deeds so Trap B changes the five.
