# OS06 — Retrofit packages: insulation and a heat pump do not save the sum of their separate savings

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Sizing bundles of improvements whose effects interact (multiple product features each measured alone, layered cost-reduction initiatives, combined performance optimisations) |
| Domain | Building energy / utility programmes |
| Task shape | 03 · Bridge between two totals (sum of single-measure savings → package savings from sequential simulation; the package offered in the utility programme) |
| Core method | Use building-energy model outputs for the baseline, each measure alone, and the full package; sequential (multiplicative) combination — savings of later measures apply to the reduced load left by earlier ones; interaction term = sum of singles − package |
| Analytical stump | Envelope upgrades reduce the heating load that a heat pump would have served more efficiently; a heat pump reduces the energy value of insulation. Adding single-measure savings double counts. Package savings must come from simulating the package or applying measures sequentially |
| Primary sources | NREL ResStock end-use load profiles and measure packages (public datasets on the Open Energy Data Initiative) |

## 1. The real-world situation

A utility designs a whole-home retrofit offer for single-family homes in one climate zone. The programme plan added the average savings of
attic insulation, air sealing, duct sealing and a heat pump — each simulated alone — and promised customers 70% savings. Engineers warned
that the measures overlap.

## 2. The decision (one deterministic recommendation)

**The package offered: the measure combination (from the memo's three candidate packages) with the highest package savings per dollar,
using ResStock package results; and the bridge from summed single-measure savings to package savings.**

Rules (programme memo):

* Data: ResStock (release in memo) annual results for the climate zone's single-family detached sample: baseline, single-measure upgrades
  (attic insulation, air sealing, duct sealing, heat pump) and packages P1 (envelope only), P2 (heat pump only), P3 (envelope + heat pump).
* Weights: each sample building's weight (dwellings represented).
* Savings: site energy (kWh-equivalent) baseline − upgrade, weighted mean per dwelling.
* Package savings: from package upgrade results (not summed).
* Costs: `measure_costs.csv` (per dwelling, by measure; package cost = sum).
* Choose the package with highest savings ÷ cost.
* Bridge for P3: Σ singles → interaction (envelope–heat pump) → P3.

## 3. Why capable analysts get it wrong

* Single-measure results are widely published; adding them is natural.
* Savings are fractions of a load that the other measures change.
* Packages must be simulated or combined multiplicatively.
* Weighting by dwellings represented matters for the zone average.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `baseline_metadata_and_annual_results.parquet` | Parquet | ~550k buildings (national) | NREL ResStock (OEDI) | CC BY 4.0 | Baseline results |
| 2–8 | `upgrade<NN>_metadata_and_annual_results.parquet` (singles and packages) | Parquet | ~550k each | NREL ResStock | CC BY 4.0 | Upgrade results |
| 9 | `resstock_upgrade_definitions.pdf` | PDF | — | NREL | CC BY 4.0 | Measure definitions |
| 10 | `resstock_data_dictionary.tsv` | TSV | ~1k | NREL | CC BY 4.0 | Columns |
| 11 | `measure_costs.csv` | CSV | 7 | Task author (from public cost references) | — | Costs |
| 12 | `programme_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 13 | `programme_plan_summed.xlsx` | XLSX | 4 | Task author | — | Naive sizing |
| 14 | `climate_zone_filter.json` | JSON | — | Task author | — | Sample filter |

## 5. Deterministic solution path

1. Filter climate zone and building type; join baseline and upgrades by building ID.
2. Weighted savings per measure and package; costs.
3. Savings per dollar; choose package; bridge for P3.
4. Contrast with summed singles.

## 6. Wrong paths (method errors, not misreadings)

**A — summed single savings.** Double counting.

**B — unweighted means.** Sample, not stock.

**C — package savings computed as 1 − Π(1 − s_i) of average fractions.** Better, but not package simulation; differs for heterogeneous homes.

**D — comparing savings without costs.** Ignores the rule.

## 7. Why the stump is analytical, not semantic

Data, weights and rule are specified. The trap is additivity of overlapping effects.

## 8. Draft task prompt (prose)

> Which retrofit package should the programme offer, and how much will it really save? Use ResStock package results as the programme memo specifies.
> Provide `package_savings.csv` (measure/package: savings, cost, savings per $), `interaction_bridge.png`, and a one-page `package_offer.pdf`.

## 9. Deliverables

* `package_savings.csv`, `interaction_bridge.png`, `package_offer.pdf`.

## 10. Where 25+ rubric criteria come from

* 7 upgrades × (savings, cost, ratio) = 21; bridge items; choice; contrast; weights.

## 11. Golden-output checklist

* Filters; join; weights; package results; cost; ratio; bridge.

## 12. Build notes (scope tuning)

* Confirm summed singles exceed P3 savings by ≥ 25%.
