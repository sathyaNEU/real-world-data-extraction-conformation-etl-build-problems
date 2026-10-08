# P21 — Building-emissions penalties under NYC Local Law 97: statutory coefficients, mixed uses and campus rows

| Field | Value |
|---|---|
| Domain | Real estate / building decarbonization / municipal climate policy |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (25 outreach slots) |
| Core technique | Recomputing a regulated metric from raw energy with statutory coefficients (not the vendor's pre-computed column); area-weighted limits for mixed occupancies via a published type mapping; parent/child de-duplication; unit discipline (kWh vs kBtu) |
| Trap family (honest data) | Using Portfolio Manager's "Total GHG Emissions"; single-use limit for mixed-use buildings; parent + child rows both counted; kWh coefficient on kBtu |
| Primary sources | NYC LL84 benchmarking disclosure (NYC Open Data), LL97 Covered Buildings List, NYC Admin Code §28-320 and 1 RCNY §103-14 |

## 1. The real-world project

A city-funded building-decarbonization accelerator has advisors for **25 buildings** per cycle in a target community
district; it wants the covered buildings with the largest estimated first-period (2024–2029) LL97 penalty. The analyst
took the LL84 file's "Total GHG Emissions (Metric Tons CO2e)", divided by floor area, compared it to the limit for the
building's largest use type, and multiplied the excess by $268. Several buildings on the list had no exposure under the
DOB's own calculator; several large mixed-use buildings were missing.

## 2. The business decision (one deterministic recommendation)

**Which 25 covered buildings in the district receive advisors, and which building is 26th?**

Rules (accelerator estimation method):

* Scope: buildings on the LL97 Covered Buildings List in the district; energy from the LL84 submission for calendar year
  2023 (as the proxy for 2024 compliance).
* Emissions = Σ energy by fuel × LL97 2024–2029 coefficients (from the Admin Code): grid electricity
  0.000288962 tCO₂e/kWh; natural gas 0.00005311 tCO₂e/kBtu; #2 oil 0.00007421; #4 oil 0.00007529; district steam
  0.00004493 tCO₂e/kBtu. (Verify every coefficient against the code text in the folder.) Electricity in **kWh**.
* Limit = Σ over property uses (gross floor area of each use × the 2024–2029 limit of the LL97 occupancy group mapped
  from that Portfolio Manager property type via the 1 RCNY §103-14 mapping table).
* Campuses: use the **parent** property row when a parent exists and its children are listed; never sum parent and
  children. Standalone properties use their own row.
* Penalty = max(0, emissions − limit) × $268.
* Rank by penalty; ties by higher excess emissions.

## 3. Why this gets overlooked in real projects

* The LL84 file already has a GHG column. It is computed by ENERGY STAR Portfolio Manager using EPA factors that differ
  from LL97's statutory coefficients, especially for electricity and steam.
* "Largest property use type" is the convenient one-column summary; LL97 limits are area-weighted across uses, and
  residential (R-2) vs office (B) limits differ greatly.
* Campus reporting creates parent and child rows; naive filters keep both.
* The file carries electricity in both kWh and kBtu columns; applying the per-kWh coefficient to kBtu inflates emissions
  ~3.4×.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `ll84_disclosure_2022_present.csv` | CSV | ~60–90k | NYC Open Data (LL84 benchmarking) | NYC Open Data terms (free use) | Energy by fuel, use areas, parent/child |
| 2 | `ll97_covered_buildings_list_2024.xlsx` | XLSX | ~50k | NYC DOB | NYC public data | Scope |
| 3 | `admin_code_28-320_excerpt.pdf` | PDF | — | NYC Administrative Code | Public law | Coefficients, limits, penalty |
| 4 | `1rcny_103-14_property_type_mapping.pdf` | PDF | — | NYC Rules (DOB) | Public | ESPM type → occupancy group |
| 5 | `pluto_24v1.csv` (district extract) | CSV | ~40k | NYC DCP PLUTO | NYC open data terms | BBL → community district |
| 6 | `ll84_data_dictionary.xlsx` | XLSX | — | NYC Mayor's Office of Climate & Environmental Justice | NYC public | Column meanings/units |
| 7 | `espm_technical_reference_ghg.pdf` | PDF | — | ENERGY STAR (EPA) | Public domain | Why PM GHG differs |
| 8 | `accelerator_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `dob_ll97_calculator_examples.json` | JSON | ~5 | Task author from DOB public calculator | — | Spot-check expectations |
| 10 | `community_district.json` | JSON | 1 | Task author | — | District in scope |

## 5. Deterministic solution path

1. Filter CBL to the district (via BBL → PLUTO); join LL84 2023 rows by BBL/BIN; resolve parent/child.
2. Compute emissions per building with statutory coefficients in correct units.
3. Map each use's property type to an occupancy group; compute area-weighted limit.
4. Penalty; rank; top 25 + 26th.
5. Show differences vs PM-GHG/largest-use method.

## 6. The traps

**Trap A — PM GHG column.** Emissions differ by 10–30% for electricity- or steam-heavy buildings; the list changes.

**Trap B — largest use only.** Mixed residential/office buildings mis-limited; big penalties appear or vanish.

**Trap C — parent + children.** Campus emissions doubled.

**Trap D — kWh vs kBtu.** Electricity emissions ×3.412.

**Trap E — total GFA vs use-level GFA.** Using self-reported total GFA with use-level limits double counts area.

## 7. Why the data is honest

LL84 data are owners' benchmarking submissions as published by the City; the law's coefficients and mapping are public.
Portfolio Manager's GHG is correct for its own purpose — just not the LL97 metric.

## 8. Draft task prompt (prose)

> Our advisors can take twenty-five buildings this cycle in the district in the folder: the covered buildings with the
> largest estimated 2024–2029 LL97 penalty under our estimation method, using 2023 benchmarking data. Tell me which
> twenty-five and who is twenty-sixth. Produce `ll97_outreach_list.xlsx` with every covered building in the district:
> BBL, property name, energy by fuel, LL97 emissions, area-weighted limit, excess and penalty, rank; and
> `penalty_ranking.png`, ranked bars for the top forty with the cut after twenty-five and mixed-use buildings marked.
> On the first sheet, give the list, the penalty gap between 25th and 26th, and how many of the twenty-five would differ
> if Portfolio Manager's GHG figure and the largest use type had been used.

## 9. Deliverables

* `ll97_outreach_list.xlsx`, `penalty_ranking.png`.

## 10. Where 25+ rubric criteria come from

* 25 buildings + 26th + gap; penalties for ~8 named buildings (mixed-use, steam-heavy, campus); naive-method difference
  count; chart cut and markers.

## 11. Golden-output checklist

* Statutory coefficients with correct units; area-weighted limits; parent/child resolved; decision stated.

## 12. Build notes (scope tuning)

* Pick a district with many mixed-use buildings and some district-steam users (e.g. Manhattan districts) and confirm
  Traps A and B each change ≥ 3 of the 25.
* Quote limits/coefficients only from the code text you include; check for any amendments in force for 2024–2029.
