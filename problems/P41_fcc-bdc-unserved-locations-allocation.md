# P41 — Broadband grant allocation from the FCC map: what counts as "served", and where are the locations nobody claims?

| Field | Value |
|---|---|
| Domain | Telecommunications policy / broadband infrastructure grants (BEAD-style) |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 05 · Allocation to a fixed total (rate per unserved-equivalent location, with a floor) |
| Core technique | Location-level de-duplication across provider × technology rows; policy-defined technology/latency/speed eligibility; reconstructing zero-provider locations from area totals; floor-constrained allocation |
| Trap family (honest data) | Satellite or unlicensed fixed wireless treated as reliable service; latency flag ignored; locations counted per availability row; locations with no provider missing from availability files |
| Primary sources | FCC Broadband Data Collection public availability files (by state/technology), FCC BDC summary-by-geography files, NTIA BEAD program definitions |

## 1. The real-world project

A state broadband office pre-allocates **$60,000,000** of a state infrastructure fund to counties in proportion to
unserved and underserved broadband-serviceable locations, before the competitive subgrant round. The analyst read the
provider availability files, flagged a location "served" when any row showed ≥ 25/3 Mbps, and counted rows. Rural counties
with heavy satellite and unlicensed wireless coverage appeared almost fully served; the office's map team disagreed.

## 2. The business decision (one deterministic recommendation)

**What rate per unserved-equivalent location exhausts the $60m with a $500,000 county floor, and what does each county
receive?**

Rules (allocation policy, aligned with NTIA BEAD definitions):

* Reliable service: technologies copper (10), cable (40), fiber (50), licensed fixed wireless (71) and licensed-by-rule fixed
  wireless (72) **with `low_latency = 1`**; satellite (60, 61) and unlicensed fixed wireless (70) do not count. Offerings must be
  residential or residential+business (`business_residential_code` R or X).
* A location is **served** if any reliable offering ≥ 100/20 Mbps; **underserved** if its best reliable offering is ≥ 25/3 but
  < 100/20; **unserved** otherwise (including locations with no claimed service at all).
* Total broadband-serviceable locations per county from the FCC summary-by-geography file of the same BDC release; unserved
  = total − served − underserved (this captures zero-provider locations absent from availability files).
* Unserved-equivalents = unserved + 0.5 × underserved.
* Allocation_c = max($500,000, r × UE_c), r solved so the sum is exactly $60m; largest-remainder rounding.
* BDC release: the as-of date and version in the folder (no mixing releases).

## 3. Why this gets overlooked in real projects

* Availability files have one row per location × provider × technology; counting rows inflates everything.
* "≥ 25/3 anywhere" is the intuitive served test; program rules exclude whole technologies and require low latency.
* A location no provider claims never appears in any availability file. Building totals bottom-up from availability rows
  loses exactly the unserved locations the program is meant to find.
* BDC data are re-released frequently with challenge outcomes; mixing files from different releases misaligns counts.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–6 | `bdc_<state>_<tech>_fixed_broadband_<asof>.csv` (copper, cable, fiber, LFW, LBR, unlicensed FW) | CSV | 0.1–3M each | FCC National Broadband Map data downloads | FCC public data (verify terms) | Location-level availability |
| 7 | `bdc_<state>_satellite_<asof>.csv` (GSO/NGSO) | CSV | 1–5M | FCC | Same | Excluded tech (present) |
| 8 | `bdc_us_fixed_broadband_summary_by_geography_<asof>.csv` | CSV | ~100k+ | FCC | Same | Total BSLs by county, tier summaries |
| 9 | `bdc_data_spec_public_availability.pdf` | PDF | — | FCC | Public | Field and code definitions |
| 10 | `ntia_bead_nofo_definitions_excerpt.pdf` | PDF | — | NTIA | Public domain | Reliable service, unserved/underserved |
| 11 | `county_fips_<state>.csv` | CSV | ~50–250 | Census | Public domain | Counties |
| 12 | `allocation_policy.pdf` | PDF | — | Task author | — | Rules in §2 |
| 13 | `bdc_release_metadata.json` | JSON | 1 | FCC release info | Public | As-of date and version |

## 5. Deterministic solution path

1. Load availability files for the release; keep R/X offerings; tag reliable offerings (tech + latency).
2. Collapse to one row per location: best reliable download/upload; classify served/underserved.
3. Count served and underserved locations by county (location → block GEOID → county).
4. Take total BSLs by county from the summary file; derive unserved; compute UE.
5. Solve r with the floor; round; report.
6. Contrast: any-tech served test; row counts; bottom-up totals.

## 6. The traps

**Trap A — satellite/unlicensed counted.** Unserved counts collapse in rural counties; money shifts to metro counties.

**Trap B — latency ignored.** Some high-latency offerings counted.

**Trap C — row counts.** Served counts inflated; unserved may go negative when subtracted from totals.

**Trap D — bottom-up totals.** Zero-provider locations vanish; unserved undercounted.

**Trap E — mixed releases.** Totals and availability from different as-of dates.

## 7. Why the data is honest

FCC publishes providers' filings and the location totals; NTIA publishes the program definitions. Each file is correct for
its release; the logic determines the counts.

## 8. Draft task prompt (prose)

> We're pre-allocating $60 million across counties in proportion to unserved-equivalent broadband locations, with a
> $500,000 floor, following the allocation policy in the folder and using only the FCC release it names. Classify every
> location, derive county counts and solve the rate. Deliver `county_bsl_allocation.xlsx` with each county's total
> locations, served, underserved, unserved, unserved-equivalents, floor flag and award, plus `county_allocation_map.png`
> (or a ranked bar chart if you prefer) showing awards with floor counties marked. On the first sheet, give the rate, the
> statewide unserved and underserved totals, and the county whose award changes most if satellite and unlicensed wireless
> were counted as reliable.

## 9. Deliverables

* `county_bsl_allocation.xlsx`, `county_allocation_map.png`.

## 10. Where 25+ rubric criteria come from

* County counts and awards (choose a state with 15–40 counties); rate; statewide totals; floor counties; trap-variant delta.

## 11. Golden-output checklist

* Reliable-tech + latency + R/X; location-level collapse; totals from summary file; single release; floor-solved rate.

## 12. Build notes (scope tuning)

* Choose a mostly rural state with significant unlicensed fixed wireless and satellite claims; confirm Traps A and D move
  several counties by > 10%.
* Record the exact BDC as-of date and release version; the FCC updates data frequently.
