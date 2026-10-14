# Verdict: task134 architecture 3 (Ridgemont Line TOD target)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. Nothing needs repair, and no rerun is needed. The cross-batch fingerprint could not be run (no other task folder was readable). Optional notes are under Fix.

**Why:** Every committed figure reproduced from the shipped files with my own pipeline: the 3,701 lots, the 3.0 / 8.5 / 2.0 percent rates, 85,906 homes, 13,005.4 over five years, the yearly figures, and the completions and standing-homes tables. The method is not filed, but the data separate the candidates. Every one of the 2,715 counted new-construction permits in 2014 to 2026 falls on a lot-year that was economically feasible, and the rate per feasible lot-year is flat by year, area and margin. The golden's bucket (13,000) and each yearly bucket hold under every reasonable variant I ran. The one reasonable variant that leaves the bucket is skipping the "each lot once" depletion, and the shipped history rejects it.

## Evidence (recomputed; file and field in brackets)

| Item | Golden | Recomputed | Source |
|---|---|---|---|
| Lots on Schedule A carried to current folios | n/a | 14,851 lots become 14,939 current folios (two are retired folios with 37 and 53 children). 14,120 sit on the 2026 roll; 819 strata lots are not on it. | tod_order_schedule_a.xlsx, folio_history, roll_extract_2019-2026 |
| Standing houses, commercial sites and rental buildings with no counted new-construction permit | 3,701 | 3,701 (3,317 houses, 140 commercial, 244 rental). The 16 vacant lots all hold permits. | rolls, building_permits |
| Houses, feasible lot-years and rebuilds | 490 / 16,349 | 490 / 16,349 = 2.997% | both rolls, zoning, reference tables |
| Commercial | 2,016 / 23,723 | 2,016 / 23,723 = 8.498% | same |
| Rental | 209 / 10,487 | 209 / 10,487 = 1.993% | same |
| Best building at order FAR on all 3,701 lots (2026 values and costs) | wood frame at 3.0 FAR | Wood frame at 3.0 FAR on all 3,701. Concrete margin per gross sq ft is negative at every station: Ellery -9.2, Westerly -34.6, Haldane -62.5, Pell Road -85.4. Wood frame wins on all lots, and the best value is 1.34 to 3.61 times the assessed land plus improvements. | housing_reference_tables |
| Net new homes at 3.0 FAR less roll dwelling units | 85,906 | 85,906 (houses 75,275, commercial 5,187, rental 5,444). The minimum per lot is 10, so no lot nets negative. | rolls (acres converted) |
| Yearly homes 2027 to 2031 | 2,805.4 / 2,698.1 / 2,596.2 / 2,499.1 / 2,406.6; total 13,005.4 | 2,805.4 / 2,698.1 / 2,596.2 / 2,499.1 / 2,406.6; total 13,005.4 | rate times (1-rate)^t applied to each kind's homes |
| Completions 2022 to 2026 by station | 888 / 1,050 / 793 / 909 / 654 and the per-station table | Exact match when homes are the first-occupancy building's units from permit_buildings (interim or final, once per building) | occupancy_permits, permit_buildings, building_permits |
| Standing homes by station and band | 21,094 in total, with the 12 cells listed | Exact match (house and rental dwelling units, plus strata residences) | roll_extract_2019-2026 |

**Sensitivity of the main call.** All of these round to 13,000 and to the same yearly buckets unless noted:

- Rate window 2019 to 2026 gives 12,992; 2022 to 2026 gives 12,953; 2024 to 2026 gives 12,949.
- Lagging the sale and cost year by one gives identical rates, because every feasible lot clears its assessed value by more than 30 percent.
- Calling a lot feasible when it beats the land value alone gives identical rates.
- The first variant that leaves the bucket is feasibility defined as a positive margin only. It adds 25,200 RM1 house lot-years with zero rebuilds and cuts the house rate to 1.18 percent. The shipped history rejects it.
- Station-area-only history gives commercial 8.51 percent and rental 1.80 percent, a negligible change.
- Not depleting the lots gives 2,805 a year and 14,027 in total, so 14,000. This is the only reasonable fork that leaves the bucket. It is not licensed: the methodology counts a lot's net new homes once, the golden states "each lot once", and permits fall from 318 in 2014 to 131 in 2026 as the pool is used up.

**Competing answers from the easy routes** (all rejected by the data):

| Route | Result |
|---|---|
| Unconditional house rate (0.46%) | about 4,100 |
| One pooled rate on feasible lots (5.37%) | about 20,700 |
| Zoned capacity at 5.0 / 4.0 FAR | far above 85,906 |
| Household growth in the station areas (population_projections, a distractor) | about 7,000 |

**Literal-reader forks the text leaves open** (the data close each one):

- Occupancy `dwelling_units` against `permit_buildings`. On 334 of 2,424 occupancy rows the occupancy figure is the whole permit's total, entered against each of 2 or 3 buildings. It equals dwelling_units_created in all 334 rows, and the building-level figure is lower. Using it gives 1,056 / 1,241 / 917 / 1,018 / 792 instead of 888 / 1,050 / 793 / 909 / 654. An expert cross-checking building rows against the permit total lands on the golden. The extract note says only "as entered", so this is the weakest point of supplementary item 3, but the files resolve it.
- Strata parking in the current layout is labelled "Strata residential" and has no code of its own.
  - Treating missing floor area as parking gives 19,381.
  - Counting every strata lot gives 23,505.
  - The golden gives 21,094.
  - The data split cleanly. Parking lots have assessed totals under about 65,000 and residences over about 400,000, with nothing in between, and 521 old-layout 052 codes confirm the parking group. Missing floor area alone is therefore not a reliable parking flag (1,713 residences lack it). This is a semantics step on supplementary item 4, which is free of the main-call rule.
- Strata lots and the 16 vacant lots are left out of the forecast. No rebuild in 2014 to 2026 started from a strata lot, and all 16 vacant lots already hold permits.

## Files/Hygiene

**PASS.**

- 15 files in 4 formats: 9 CSV, 3 XLSX, 2 PDF, 2 TXT.
- The largest are the two roll extracts, 67,251 and 155,399 rows.
- Layer-1 mess is authentic and unplanted:
  - the layout changed in 2019
  - zone codes were renamed in 2020
  - permit areas switched from square feet to square metres in 2020
  - some lots are in acres
  - strata plans retire and create folios
  - revision permits supersede earlier ones
  - occupancy permits double up as interim and final
- Distractors: population_projections, rental_market_survey, and the cost and sale series for the other areas.
- No synthetic, benchmark or authoring language in any file. Dates are coherent: the order took effect on 1 January 2027, the permit pull was 11 January 2027 and ran to 31 December 2026, and the reference tables date to 20 November 2026.
- The licence statements are in-fiction (the open-licence line in folder_index, a fictional ministry). I did not treat this as exclusion-level.
- The data are fictional, so there is no public-answer contamination.
- No hidden sheets or comments in the workbooks.

## Stump power

Strong. A capable analyst has several plausible easy routes, and each lands far from 13,000:

- zoned capacity times the corridors' take-up;
- an unconditional rebuild rate, which gives about 4,100;
- one rate for every feasible lot, which gives about 20,700;
- a positive-margin feasibility test;
- no depletion, which gives 14,000.

Getting the call right requires the economics of redevelopment (the feasibility test against what stands, and the finding that concrete is infeasible at the order's 5.0 and 4.0 bands) plus a hazard estimated only on feasible lot-years by kind. Neither is in a document. The data separate them.

## Stumping type

`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`

The past is read correctly, and the forward figure depends on a conditional redevelopment rate and an economic feasibility test the trailing counts do not give. On perfectly clean data this would still stump. There is no banned scaffold.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`

- Swap test: replacing "homes", "lots" and "permits" with another field's nouns breaks the task, because the deciding quantity is a residual-land-value feasibility test and a feasibility-conditioned redevelopment rate, which is how a land-economics housing forecast is built.
- Layer 1: the changing roll layout, zone renames, mixed area units, folio retirement and strata subdivision, superseded revisions, and interim and final occupancy.
- Layer 2: feasibility-conditioned, kind-specific rebuild rates with depletion, and finding concrete infeasible at the order's densities.
- Easy route: apply the order's FAR to the 3,701 lots at some take-up. Or use an unconditional or pooled historical rate, giving about 4,100 or 20,700 against 13,005. A strong analyst who cleaned everything correctly can still take this route, so the step is analytical, not semantics or rule application.

## Fix

None required (location: none). Optional wording notes, none of which change the analytic surface:

- The extract note could say whether `dwelling_units` on an occupancy permit is per building or per permit, but this would remove a Layer-1 step.
- Whether the missing floor-area field marks a parking lot is left to inference from value.

## Disposition

APPROVE, shipped as architecture 3 on 2026-10-14. No document under `target/`, no graded figure and no part of the main call moved (`freeze.py check task134 --mode determinism` PASS; target.zip byte-identical, sha256 cffb3ab8).

- **Soft spot 1 (occupancy units against `permit_buildings`).** This is the designed device of Ask A. It is recorded as fork row SF22 and asserted in `checks.py`. On all 334 rows where the two figures differ, the occupancy figure is the permit's total on a permit of two or more buildings, and each permit's building units sum to that total.
- **Soft spot 2 (strata parking separated only by assessed value).** This is the designed device of Ask B. It is recorded as SF23 and asserted: a value cut anywhere between $95,000 and $310,000 marks exactly the strata lots that have neither a unit number nor a floor area.
- **The no-depletion variant (14,000).** It is ruled out by methodology 2.2 and the falling permit record, as the verdict states, and is already ladder row L1.
- **Optional wording notes.** Both are declined. Each would change a document under `target/` and would remove a designed ask device.
- **The stage 4 reader's three readings.** They are recorded as SF19 to SF21 and asserted. The five-year total rounded directly from 13,005.4 and the rounded years summed both give 13,000. Every Schedule A folio missing from the 2026 roll was created after its 31 October 2025 condition date. No strata plan summary record sits on the order's lots.
