# task486: start here

| | |
|---|---|
| Task | task486 |
| Objective (Axis 1) | Data Extraction & Conformation (ETL) |
| Block | task445 to task493 |
| Lane owner | unassigned (current owner and status: the root `START_HERE.md` on main) |
| Seed | ET43, `analytical_tasks/07_data_extraction_conformation/ET43_trade-mirror-statistics-asymmetry-bridge.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task486`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task486-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** Mirror trade statistics: why U.S. pharma exports to Germany don't equal Germany's pharma imports from the U.S.
- **objective:** Data Extraction & Conformation (ETL / Pipeline Build)
- **domain:** Market sizing / trade analytics / official statistics reconciliation
- **decision_shape:** 03 · Bridge between two totals (exporter-reported → importer-reported)
- **committed_call:** Which figure does the model adopt, the importer-reported value, or the mirror-adjusted average, and what is it?
- **technique:** Bilateral asymmetry reconciliation: valuation basis (FOB vs CIF), currency conversion at matching frequency, re-export removal, partner-attribution concepts (destination vs origin; national vs community concept), confidential trade; residual-driven source adoption
- **trap:** Annual-average FX; CIF/FOB ignored; total exports including re-exports; mixing national-concept and community-concept importer data
- **sources:** U.S. Census Bureau international trade (API / USA Trade Online), Eurostat Comext, Destatis GENESIS foreign trade tables, OECD ITIC (CIF/FOB margins), ECB exchange rates

## Seed note

## ET43, Mirror trade statistics: why U.S. pharma exports to Germany don't equal Germany's pharma imports from the U.S.

| Field | Value |
|---|---|
| Domain | Market sizing / trade analytics / official statistics reconciliation |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 03 · Bridge between two totals (exporter-reported → importer-reported) |
| Core technique | Bilateral asymmetry reconciliation: valuation basis (FOB vs CIF), currency conversion at matching frequency, re-export removal, partner-attribution concepts (destination vs origin; national vs community concept), confidential trade; residual-driven source adoption |
| Trap family (honest data) | Annual-average FX; CIF/FOB ignored; total exports including re-exports; mixing national-concept and community-concept importer data |
| Primary sources | U.S. Census Bureau international trade (API / USA Trade Online), Eurostat Comext, Destatis GENESIS foreign trade tables, OECD ITIC (CIF/FOB margins), ECB exchange rates |

### 1. The real-world project

A pharmaceutical market-sizing team needs **2023 U.S.-origin pharmaceutical (HS 30) imports into Germany** for a revenue
model. The U.S. figure (exports to Germany) and the German/EU figure (imports from the U.S.) differ by billions. The analyst
averaged the two. Finance asked which number is right and why.

### 2. The business decision (one deterministic recommendation)

**Which figure does the model adopt, the importer-reported value, or the mirror-adjusted average, and what is it?**

Rules (market-sizing data standard):

* Importer figure: Eurostat Comext, reporter DE, partner US, product HS 30 (CN chapter 30), flow import, 2023, **community
  concept**, statistical value in EUR.
* Exporter figure: U.S. Census exports to Germany, HS 30, 2023, **domestic exports only** for the bridge (total exports =
  domestic + foreign/re-exports), USD FAS value.
* Bridge (in EUR): U.S. total exports (converted **month by month** at ECB monthly average USD/EUR) → − re-exports →
  + freight & insurance (CIF/FOB margin for US→DE HS 30 from OECD ITIC for the latest available year) → ± quasi-transit
  (difference between Destatis national-concept and Eurostat community-concept imports from the U.S., HS 30) → ± confidential
  trade adjustments where published → residual → importer figure.
* Adopt the importer figure if |residual| ≤ 10% of it; otherwise adopt the mean of the importer figure and the fully adjusted
  exporter figure and flag the residual.

### 3. Why this gets overlooked in real projects

* "Exports from A to B should equal imports of B from A" is intuitive; the conventions that make them differ (valuation,
  origin vs consignment, customs clearance location) are buried in methodology notes.
* Annual average FX applied to annual totals misweights months with very different volumes.
* U.S. exports include re-exports of foreign-origin goods, which the importer attributes to the original country.
* Goods arriving via Rotterdam/Antwerp may be cleared there; EU "community concept" and German "national concept" figures
  differ, and mixing them double counts or drops quasi-transit.

### 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `census_exports_hs6_by_country_2023_monthly.csv` | CSV | 0.5–1M | U.S. Census International Trade API (HS exports) | U.S. Gov public domain | Domestic/foreign exports by month |
| 2 | `census_exports_hs30_germany_2023.json` | JSON | ~300 | Census API | Public domain | Focused pull |
| 3 | `comext_DS-045409_2023_DE_US.tsv` (or current Comext dataset) | TSV | ~0.2M (DE all partners, CN8) | Eurostat Comext | Eurostat free re-use with attribution | Importer data (community concept) |
| 4 | `destatis_51000-0006_2023_US_HS30.csv` | CSV | ~1k | Destatis GENESIS-Online | Data licence Germany – attribution 2.0 | National concept |
| 5 | `oecd_itic_cif_fob_margins.csv` | CSV | ~50k | OECD ITIC database | OECD terms (free with attribution) | CIF/FOB margin |
| 6 | `ecb_usd_eur_monthly.csv` | CSV | ~300 | ECB SDW | ECB re-use with attribution | Monthly FX |
| 7 | `eurostat_comext_user_guide.pdf` | PDF |, | Eurostat | Re-use permitted | Partner concepts, valuation |
| 8 | `census_trade_definitions.pdf` | PDF |, | U.S. Census FT-900 notes | Public domain | FAS, domestic vs foreign exports |
| 9 | `us_eu_trade_asymmetry_reconciliation.pdf` (published reconciliation study, if available) | PDF |, | Statistical agencies (public) | Public | Method reference |
| 10 | `market_sizing_standard.pdf` | PDF |, | Task author |, | Rules in §2 |
| 11 | `hs_cn_chapter30_concordance.xlsx` | XLSX | ~200 | Eurostat CN / Census Schedule B | Public | Product scope |

### 5. Deterministic solution path

1. Pull U.S. exports to Germany HS 30 by month, split domestic vs foreign; convert monthly to EUR.
2. Pull Eurostat community-concept imports (DE from US, CN 30) and Destatis national-concept equivalent.
3. Apply bridge items in order; compute residual; apply the adoption rule.
4. Report each bar's magnitude and the adopted figure.

### 6. The traps

**Trap A, annual FX.** Mis-sizes the conversion bar; residual shifts across the 10% line.

**Trap B, CIF/FOB omitted.** Residual inflated by the freight margin.

**Trap C, re-exports kept.** Exporter side overstated.

**Trap D, concept mixing.** Using Destatis national figures as "the importer figure" while also adding a quasi-transit bar
double counts.

### 7. Why the data is honest

Each agency's figure is correct under its documented conventions; asymmetries are a well-studied, real phenomenon. The
bridge applies those conventions explicitly.

### 8. Draft task prompt (prose)

> Our pharma model needs one 2023 figure for U.S.-origin pharmaceutical imports into Germany, chosen the way the
> market-sizing standard in the folder prescribes. Walk from the U.S.-reported exports to the German/EU-reported imports one
> reconciling item at a time, and tell me which figure we adopt and its value. Deliver `mirror_bridge.png`, a waterfall in
> euros from U.S. exports to the importer figure (conversion, re-exports, CIF/FOB, quasi-transit, confidential trade,
> residual) with the ±10% band marked, and `mirror_memo.docx`, one page stating the adopted figure, the residual as a share
> of the importer figure, and the item that moves the total most.

### 9. Deliverables

* `mirror_bridge.png`, `mirror_memo.docx`.

### 10. Where 25+ rubric criteria come from

* 12 monthly conversions (or monthly EUR values), each bridge bar, residual, adoption decision, adopted value, largest item;
  domestic vs foreign split; concept choice.

### 11. Golden-output checklist

* Monthly FX; domestic exports; CIF margin; community concept as importer figure; quasi-transit as a separate bar; rule applied.

### 12. Build notes (scope tuning)

* Pharmaceuticals between the U.S. and Germany/Netherlands/Belgium typically show large asymmetries; confirm that at least one
  trap moves the residual across the 10% line.
* Record the exact Comext dataset code and extraction date (Eurostat restructured Comext datasets over time).
