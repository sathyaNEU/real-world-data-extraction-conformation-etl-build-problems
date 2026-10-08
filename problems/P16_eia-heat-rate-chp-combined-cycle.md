# P16 — Most-efficient gas plants from EIA-923: combined cycles split in two and CHP fuel that never made electricity

| Field | Value |
|---|---|
| Domain | Power generation / utility resource planning / energy data engineering |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (must-run efficiency list of N plants) |
| Core technique | Grain alignment across survey schedules (plant–prime mover–fuel vs generator vs boiler); combining combined-cycle components; electric-only fuel for CHP; handling negative net generation |
| Trap family (honest data) | Heat rate by prime mover (CA vs CT); total fuel instead of electric fuel for CHP; fan-out joins to EIA-860 generators |
| Primary sources | EIA-923 (Generation and Fuel, Generator, Boiler Fuel pages), EIA-860 (plants, generators, boiler–generator associations) |

## 1. The real-world project

A balancing-authority planning team builds a **must-run efficiency list**: the eight most efficient natural-gas plants
in its footprint by annual net heat rate (Btu per net kWh). The data engineer joined EIA-923 "Page 1 Generation and Fuel"
to EIA-860 generators and computed heat rate per generator, then rolled up. Steam turbines of combined-cycle plants
appeared at 0 Btu/kWh; several industrial CHP plants appeared worse than peakers; one plant appeared with a heat rate
of 6,000 Btu/kWh.

## 2. The business decision (one deterministic recommendation)

**Which eight natural-gas plants make the 2023 must-run efficiency list, and which plant is ninth?**

Rules (planning methodology):

* Data year 2023, EIA-923 final release; plants in the balancing authority; primary fuel natural gas (NG ≥ 90% of
  electric fuel MMBtu); nameplate ≥ 100 MW.
* Plant-level heat rate = Σ **electric** fuel consumption (`ELEC_FUEL_CONSUMPTION_MMBTU`) across all prime movers and
  fuels ÷ Σ net generation (`NET_GENERATION_MWH`) × 1,000. Combined-cycle components (`CA`, `CT`, `CS`, `CC`) are
  combined at plant level by construction; never compute per prime mover.
* CHP plants (`COMBINED_HEAT_AND_POWER_PLANT = Y`) are included; total fuel (`TOTAL_FUEL_CONSUMPTION_MMBTU`) is not used.
* Plants with non-positive annual net generation are excluded.
* No joins to generator-level tables for the numerator or denominator (EIA-860 is used only for BA, nameplate, and CHP
  confirmation, aggregated to plant first).
* Rank ascending; ties by larger net generation.

## 3. Why this gets overlooked in real projects

* EIA-923 Page 1 is at plant–prime mover–fuel grain; EIA-860 is at generator grain; boiler fuel is at boiler grain. A
  plant with 6 generators joined to Page 1 rows multiplies fuel and generation — sometimes not equally.
* Combined cycles report fuel against the combustion turbines (`CT`) and generation from both `CT` and the steam part
  (`CA`). Per-prime-mover heat rates are meaningless but look like a "finer" analysis.
* CHP plants burn fuel for useful thermal output; EIA estimates electric fuel separately. Total fuel ÷ generation
  penalizes efficient cogeneration.
* Station-service-heavy or mostly-idle plants have negative net generation, producing negative heat rates that sort first.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `EIA923_Schedules_2_3_4_5_M_12_2023_Final.xlsx` (Page 1 Generation and Fuel; Page 3 Boiler Fuel; Page 4 Generator) | XLSX | Page 1 ≈ 15–20k | EIA-923 | U.S. Gov public domain | Fuel and generation |
| 2 | `EIA923_Schedule_8_Annual_Environmental_Information_2023.xlsx` | XLSX | ~10k | EIA-923 | Public domain | Context (not needed for answer) |
| 3 | `2___Plant_Y2023.xlsx` | XLSX | ~12k | EIA-860 | Public domain | BA code, plant attributes |
| 4 | `3_1_Generator_Y2023.xlsx` | XLSX | ~27k | EIA-860 | Public domain | Nameplate, prime mover, status |
| 5 | `6_1_EnviroAssoc_Y2023.xlsx` (boiler–generator associations) | XLSX | ~10k | EIA-860 | Public domain | Shows the many-to-many trap |
| 6 | `EIA923_File_Layout_2023.xlsx` | XLSX | — | EIA | Public domain | Column definitions |
| 7 | `eia923_instructions.pdf` | PDF | — | EIA | Public domain | Electric vs total fuel, CHP allocation |
| 8 | `eia860_instructions.pdf` | PDF | — | EIA | Public domain | Prime mover codes |
| 9 | `ba_footprint.json` | JSON | ~1 | Task author | — | BA code(s) in scope |
| 10 | `planning_methodology.pdf` | PDF | — | Task author | — | Rules in §2 |
| 11 | `eia_api_plant_generation_2023.json` | JSON | ~5k | EIA Open Data API (electricity/facility-fuel) | Public domain | Reconciliation cross-check |

## 5. Deterministic solution path

1. Load Page 1; filter year and BA plants (BA from EIA-860 plant file).
2. Aggregate to plant: Σ electric fuel MMBtu, Σ net generation MWh, fuel shares.
3. Apply NG ≥ 90% electric-fuel share, nameplate ≥ 100 MW (sum of operable generators from 3_1, aggregated first), net
   generation > 0.
4. Compute heat rate; rank; top eight + ninth.
5. Show contrast: per-prime-mover rates for one combined cycle; total-fuel rates for CHP plants; generator-join totals.

## 6. The traps

**Trap A — per prime mover.** CA rows show near-zero heat rate and enter the list as "plants" or pull the plant average
down if averaged.

**Trap B — total fuel for CHP.** Efficient cogeneration plants drop out of the top eight.

**Trap C — fan-out join.** Joining Page 1 to generators before aggregating multiplies rows; ratios distort when the
multiplication differs between fuel rows and generation rows.

**Trap D — negative generation.** Negative heat rates sort first.

**Trap E — mean of monthly heat rates.** Annual ratio ≠ mean of monthly ratios; low-output months dominate.

## 7. Why the data is honest

EIA-923 and EIA-860 are official survey data with documented grains and fuel-allocation methods. Every quirk is a
feature of how plants physically operate and how EIA collects data.

## 8. Draft task prompt (prose)

> We need the eight most efficient gas plants in our balancing authority for the 2023 must-run list, ranked by annual net
> heat rate under the planning methodology in the folder. Using the EIA-923 and EIA-860 workbooks, give me the eight and
> the plant that just missed. Provide `must_run_list.csv` with every eligible plant's electric fuel, net generation, heat
> rate, CHP flag, nameplate and rank, and `heat_rate_ranking.png`, a ranked bar chart of all eligible plants with the
> top eight highlighted and CHP plants marked. In a short `must_run_note.pdf`, state the list, the gap between eighth and
> ninth, and which plants would have been on the list if total fuel had been used for CHP plants.

## 9. Deliverables

* `must_run_list.csv`, `heat_rate_ranking.png`, `must_run_note.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 plants + 9th + gap; heat rates for ~12 named plants; CHP total-fuel variant list; eligibility exclusions; chart
  markers.

## 11. Golden-output checklist

* Plant-level aggregation; electric fuel; CC combined; negatives excluded; no fan-out; decision stated.

## 12. Build notes (scope tuning)

* Choose a BA with several industrial CHP gas plants and multiple combined cycles (e.g. Gulf Coast BAs); verify Trap B
  changes the list.
* Copy column names exactly from the 2023 layout file; EIA renames columns between years.
