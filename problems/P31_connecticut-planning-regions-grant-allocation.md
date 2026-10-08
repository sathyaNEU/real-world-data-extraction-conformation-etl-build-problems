# P31 — Allocating a fixed grant across Connecticut's new county-equivalents: rebuilding history from towns

| Field | Value |
|---|---|
| Domain | State & local government finance / formula grants / geographic data conformance |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 05 · Allocation to a fixed total (solve the per-person rate under a floor) |
| Core technique | Geographic re-tabulation across a boundary-system change by aggregating a stable lower geography (towns/county subdivisions) to the new units; floor-constrained rate solving; largest-remainder rounding |
| Trap family (honest data) | Legacy-county data apportioned to planning regions by area or a single dominant mapping; mixing vintages on different geographies |
| Primary sources | Census ACS 5-year (county subdivision level), Census geography change notes and relationship files for Connecticut planning regions |

## 1. The real-world project

Beginning with 2022 data products, the Census Bureau replaced Connecticut's eight legacy counties with **nine planning
regions** as county-equivalents (FIPS 09110–09190). A state agency allocates a fixed **$12,000,000** anti-poverty
program across the nine regions using a five-vintage average of the population below poverty. Older vintages are
published for the legacy counties. The analyst "converted" them with a county-to-region area crosswalk; regional
councils with dense cities in large rural legacy counties lost money.

## 2. The business decision (one deterministic recommendation)

**What per-person rate r (dollars per person below poverty) exhausts the $12,000,000 exactly under the floor rule, and
what does each region receive?**

Rules (allocation statute summary in the folder):

* Need measure for each region = mean over ACS 5-year vintages 2015–2019, 2016–2020, 2017–2021, 2018–2022 and 2019–2023 of
  the population below poverty (table B17001, total below poverty), built by **summing towns (county subdivisions)** into
  planning regions using the official town→planning-region assignment. (Towns nest in both systems; legacy counties do not
  nest in regions.)
* Allocation_i = max($400,000, r × need_i), with r chosen so Σ allocation_i = $12,000,000.
* Round to whole dollars by largest remainder so the total is exact.

## 3. Why this gets overlooked in real projects

* County is the default geography for most pipelines; the 2022 change breaks every county-keyed time series in the state.
* An area-weighted or "majority overlap" county-to-region crosswalk is quick and looks reasonable on a map — but poverty is
  concentrated in cities whose legacy county spans several regions.
* Town (county subdivision) data exist for all vintages and nest exactly in both systems, but are a less familiar summary
  level (060).
* Floor rules make the rate a fixed-point problem; proportional shares followed by adding floors overshoots the total.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–5 | `acs5_2019_B17001_ct_cousub.csv` … `acs5_2023_B17001_ct_cousub.csv` | CSV | ~170 towns × many columns | Census ACS API / data.census.gov | U.S. Gov public domain | Town-level poverty by vintage |
| 6 | `acs5_2021_B17001_ct_county.csv` | CSV | 8 | Census | Public domain | Legacy-county figures (tempting shortcut) |
| 7 | `acs5_2023_B17001_ct_county.csv` | CSV | 9 | Census | Public domain | Planning-region figures (check target) |
| 8 | `ct_town_to_planning_region.xlsx` | XLSX | ~170 | Census geography change notes / CT OPM | Public | Assignment |
| 9 | `ct_2020_tract_to_2022_tract_relationship.txt` | Pipe-delimited | ~900 | Census relationship files | Public domain | Shows recoding (context) |
| 10 | `BlockAssign_ST09_CT_MCD.txt` | Pipe-delimited | ~50k blocks | Census 2020 Block Assignment Files (county subdivision) | Public domain | Nesting check: every 2020 block's town lies in exactly one planning region |
| 11 | `ct_legacy_county_to_region_area_overlap.csv` | CSV | ~20 | Task author from TIGER/Line polygons | Public domain inputs | The tempting crosswalk |
| 12 | `tl_2023_09_cousub.zip` | Shapefile | ~170 | Census TIGER/Line | Public domain | Optional map |
| 13 | `geography_change_notes_ct_2022.pdf` | PDF | — | Census Bureau | Public domain | Documentation |
| 14 | `allocation_statute_summary.pdf` | PDF | — | Task author | — | Rules in §2 |

## 5. Deterministic solution path

1. Load each vintage's town table; keep total-below-poverty estimates; map towns to regions; sum.
2. Verify the 2019–2023 region sums equal Census's published planning-region figures, and confirm with the block assignment file that
   every town nests in one planning region.
3. Average across five vintages per region.
4. Solve r: sort regions by need; iterate floors (regions where r × need < floor get the floor); solve r on the rest;
   repeat until stable.
5. Round by largest remainder; report allocations and r.
6. Contrast: area-crosswalk method allocations.

## 6. The traps

**Trap A — area crosswalk.** Shifts need from urban to rural regions; several allocations move by > 10%.

**Trap B — latest vintage only on regions + older on counties.** Mixes geographies; averages inconsistent units.

**Trap C — proportional then floor.** Total exceeds $12m; scaling afterwards breaks the floor.

**Trap D — margins as estimates / wrong table line.** Using the poverty-universe total instead of below-poverty count.

## 7. Why the data is honest

All estimates are official ACS products on documented geographies; the boundary change is a real, documented
administrative decision. Town data make an exact re-tabulation possible.

## 8. Draft task prompt (prose)

> The $12 million program must be split across Connecticut's nine planning regions by the statute summary in the folder:
> a per-person rate on the five-vintage average poverty count, with a $400,000 floor, adding up exactly to the total.
> Using the ACS town files and the town-to-region assignment, compute each region's need, solve the rate and give me the
> allocations. Provide `ct_allocation.xlsx` with towns-to-regions detail, each region's five vintage values and average,
> floor status and final allocation, plus `ct_allocation_chart.png` comparing each region's allocation under our method
> and under the county-area crosswalk. On the first sheet, state the rate, the regions on the floor, and the region that
> gains the most relative to the crosswalk method.

## 9. Deliverables

* `ct_allocation.xlsx`, `ct_allocation_chart.png`.

## 10. Where 25+ rubric criteria come from

* 9 regions × (average need, allocation) = 18; rate r; floor regions; 5 vintage sums for 2 regions; crosswalk comparison;
  largest gainer.

## 11. Golden-output checklist

* Town aggregation for all vintages; check against published 2023 region figures; floor-solved rate; exact total.

## 12. Build notes (scope tuning)

* Tune the floor so 1–3 regions bind; confirm Trap A moves at least one region by > $250k.
* Verify the town→region list against the Census geography change documentation (towns nest exactly).
