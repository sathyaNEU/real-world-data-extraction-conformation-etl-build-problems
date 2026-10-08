# ET19 — Plant emissions intensity across EPA and EIA: choosing a key for a many-to-many world

| Field | Value |
|---|---|
| Domain | ESG data products / climate disclosure / power-sector analytics |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 15 · Fields conformed to one schema (the adopted entity-matching rule is the answer) |
| Core technique | Graph connected components ("subplants") over a many-to-many unit↔generator crosswalk; per-field lineage and unit conversion; double-count tests on mass and energy |
| Trap family (honest data) | Row-level joins through a many-to-many crosswalk; multi-valued facility→plant codes; short vs metric tons; biogenic CO₂ |
| Primary sources | EPA Power Sector Data Crosswalk (CAMD–EIA), EPA CAMD/CAMPD emissions, EPA GHGRP (FLIGHT) data, EIA-923/860 |

## 1. The real-world project

An ESG data vendor publishes plant-level CO₂ intensity (t CO₂ per MWh) for every U.S. fossil plant, combining EPA's
measured stack emissions (CAMD, unit level), EPA greenhouse-gas program totals (GHGRP, facility level), and EIA
generation (generator/plant level). Customers reconcile state totals to EPA and EIA publications; a utility customer
found the vendor's state total CO₂ 18% above EPA's and its intensity for one combined-cycle plant 40% below physical
plausibility.

## 2. The business decision (one deterministic recommendation)

**Which entity-matching rule does the product adopt as its plant key, and what does it produce for the state's plants?**

Candidate rules (documented in the folder):

* **R1 – Facility ORIS join:** GHGRP facility ↔ EIA plant on the facility's reported ORIS code(s).
* **R2 – Crosswalk row join:** CAMD unit ↔ EIA generator via the Power Sector Data Crosswalk, summing across joined rows.
* **R3 – Crosswalk components:** build connected components of CAMD units and EIA generators linked by the crosswalk
  ("subplants"); sum each unit's emissions once and each generator's generation once per component; roll components up
  to the EIA plant.
* **R4 – Name/state match:** fuzzy plant-name match within state.

Acceptance tests (data-product standard): (T1) each CAMD unit's CO₂ is counted exactly once; (T2) each EIA generator's MWh
is counted exactly once; (T3) matched CAMD CO₂ ≥ 95% of the state's CAMD total; (T4) state CO₂ within ±2% of EPA's
published CAMD state total after unit conversion. Adopt the first rule (R1→R4 order) that passes all four.

Target schema fields (each with mandated source and transformation): plant_id (EIA), plant_name (EIA-860), operator
(EIA-860), camd_unit_ids (list), ghgrp_facility_ids (list), co2_tonnes (CAMD short tons × 0.90718474; fossil only),
ghgrp_co2_tonnes (GHGRP subpart D/C, non-biogenic, metric tons), net_generation_mwh (EIA-923), nameplate_mw (EIA-860
operable generators), co2_intensity_t_per_mwh, primary_fuel (EIA-923 plurality of fuel MMBtu), match_rule.

## 3. Why this gets overlooked in real projects

* Crosswalks look like lookup tables. Joining through them row by row repeats a unit's emissions once per linked
  generator and a generator's MWh once per linked unit.
* GHGRP facilities sometimes list multiple ORIS codes in one field; splitting them and joining multiplies facility totals
  across plants.
* CAMD reports CO₂ in short tons; GHGRP in metric tons; mixing them is a quiet 10% error.
* Biogenic CO₂ is reported separately in GHGRP; including it changes intensity for co-firing plants.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `epa_eia_crosswalk.csv` | CSV | ~6–7k | EPA Power Sector Data Crosswalk (github.com/USEPA/camd-eia-crosswalk) | U.S. Gov public domain | Unit↔generator links |
| 2 | `camd_annual_emissions_2022.csv` | CSV | ~4–5k units | EPA CAMPD | Public domain | Unit CO₂ (short tons), gross load |
| 3 | `camd_facility_attributes_2022.csv` | CSV | ~5k | EPA CAMPD | Public domain | Unit attributes |
| 4 | `ghgrp_2022_data_summary.xlsx` (Direct Emitters) | XLSX | ~7k facilities | EPA GHGRP / FLIGHT | Public domain | Facility CO₂, ORIS codes, biogenic |
| 5 | `ghgrp_subpart_d_2022.csv` | CSV | ~1.5k | EPA Envirofacts GHG tables | Public domain | Subpart D detail |
| 6 | `EIA923_2022_Page1_GenFuel.xlsx` | XLSX | ~15k | EIA-923 | Public domain | Net generation, fuel |
| 7 | `3_1_Generator_Y2022.xlsx` | XLSX | ~27k | EIA-860 | Public domain | Generators, nameplate |
| 8 | `2___Plant_Y2022.xlsx` | XLSX | ~12k | EIA-860 | Public domain | Plant names, operators |
| 9 | `crosswalk_readme.pdf` | PDF | — | EPA | Public domain | Match types, many-to-many explanation |
| 10 | `camd_state_totals_2022.json` | JSON | ~50 | EPA CAMPD API | Public domain | T4 reconciliation |
| 11 | `data_product_standard.pdf` | PDF | — | Task author | — | Rules, tests, schema |

## 5. Deterministic solution path

1. Implement each rule for the state; run T1–T4 on each.
2. R1 fails T1/T4 when multi-ORIS facilities exist; R2 fails T1/T2 on many-to-many links; R3 passes if implemented as
   components; R4 fails T3. (Confirm on data — the adopted rule is whatever the tests select.)
3. Populate the target schema under the adopted rule with each field's mandated source and conversion.
4. Report state totals, reconciliation, and plant intensities.

## 6. The traps

**Trap A — row-level crosswalk joins (R2 as "correct").** Double counts; intensities for multi-unit combined cycles
distort; T4 fails but the solver does not test it.

**Trap B — R1 multi-ORIS fan-out.** Facility totals copied to each listed plant.

**Trap C — unit mix.** Short tons treated as metric tons; T4 tolerance breached.

**Trap D — biogenic included.** Intensity of co-firing plants overstated.

## 7. Why the data is honest

All sources are official EPA and EIA publications; the crosswalk is EPA's own and explicitly documents many-to-many
relationships. The work is building a key that respects them.

## 8. Draft task prompt (prose)

> Our plant-intensity product needs one matching rule for the state in the folder, chosen by the acceptance tests in our
> data-product standard. Run the four candidate rules, tell me which one we adopt and why the others fail, and populate
> the target schema with it. Deliver `plant_intensity_2022.csv` in the exact target schema (one row per plant, every field
> from its mandated source and conversion) and `rule_test_matrix.png`, a grid of the four rules against the four tests
> with pass/fail and the measured value in each cell. Then write a one-page `matching_rule_memo.pdf` that states the
> adopted rule, the state CO₂ total versus EPA's published total, and the three plants whose intensity changes most
> between the adopted rule and the row-level crosswalk join.

## 9. Deliverables

* `plant_intensity_2022.csv`, `rule_test_matrix.png`, `matching_rule_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 16 rule × test cells; adopted rule; state total vs EPA; per-field source/transformation checks (12 fields); top-3 movers.

## 11. Golden-output checklist

* Components-based key; once-only counting; correct units; non-biogenic; tests reported; decision stated.

## 12. Build notes (scope tuning)

* Pick a state with several combined cycles and multi-ORIS GHGRP facilities so R1 and R2 fail visibly.
* Confirm the crosswalk version/year matches the emissions year; the crosswalk repository is versioned.
