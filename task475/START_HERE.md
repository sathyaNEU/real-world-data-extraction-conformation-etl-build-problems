# task475: start here

| | |
|---|---|
| Task | task475 |
| Objective (Axis 1) | Data Extraction & Conformation (ETL) |
| Block | task445 to task493 |
| Lane owner | unassigned (current owner and status: the root `START_HERE.md` on main) |
| Seed | ET32, `analytical_tasks/07_data_extraction_conformation/ET32_hud-zip-county-crosswalk-capped-allocation.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task475`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task475-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** ZIP-level tax data to county allocations: the crosswalk direction, the ratio type and the "other ZIPs" row
- **objective:** Descriptive & Distribution Analysis (allocation)
- **domain:** State program administration / formula allocation / geographic conformance
- **decision_shape:** 05 · Allocation to a fixed total (capped per-return rate)
- **committed_call:** What per-return rate exhausts the $20,000,000 under the 12% cap, and what does each county receive?
- **technique:** Many-to-many ZIP→county apportionment with the correct ratio file and ratio type; vintage alignment; treatment of suppressed/combined ZIP rows; cap-and-redistribute solving
- **trap:** COUNTY_ZIP ratios used to allocate ZIP data; total instead of residential ratio; dominant-county assignment; state-total and 99999 rows double counted
- **sources:** IRS SOI Individual Income Tax ZIP Code Data; HUD-USPS ZIP Code Crosswalk Files

## Seed note

## ET32, ZIP-level tax data to county allocations: the crosswalk direction, the ratio type and the "other ZIPs" row

| Field | Value |
|---|---|
| Domain | State program administration / formula allocation / geographic conformance |
| Objective family | Descriptive & Distribution Analysis (allocation) |
| Task shape | 05 · Allocation to a fixed total (capped per-return rate) |
| Core technique | Many-to-many ZIP→county apportionment with the correct ratio file and ratio type; vintage alignment; treatment of suppressed/combined ZIP rows; cap-and-redistribute solving |
| Trap family (honest data) | COUNTY_ZIP ratios used to allocate ZIP data; total instead of residential ratio; dominant-county assignment; state-total and 99999 rows double counted |
| Primary sources | IRS SOI Individual Income Tax ZIP Code Data; HUD-USPS ZIP Code Crosswalk Files |

### 1. The real-world project

A state energy office splits a fixed **$20,000,000** weatherization fund across counties in proportion to the number of
tax returns claiming the Earned Income Tax Credit (a proxy for low-income working households), with no county receiving
more than 12% of the fund. EITC counts come from IRS ZIP-code tables; the program needs counties. The analyst used the
HUD crosswalk, the file named COUNTY_ZIP, and the TOT_RATIO column. The capital county's share jumped.

### 2. The business decision (one deterministic recommendation)

**What per-return rate exhausts the $20,000,000 under the 12% cap, and what does each county receive?**

Rules (allocation method):

* Source: IRS SOI ZIP data for tax year 2021, the state's rows; EITC return count field (`N59660`, verify in the SOI
  documentation for the year); exclude the state-total row (`zipcode` 00000).
* ZIP→county: HUD **ZIP_COUNTY** file for Q4 2021 (each ZIP's ratios sum to 1 across counties); use **RES_RATIO**.
* County count = Σ over ZIPs (EITC returns × RES_RATIO). The SOI "other ZIP codes" row (99999) and SOI ZIPs absent from
  the crosswalk are distributed to counties in proportion to the county totals from matched ZIPs.
* Allocation_c = min(12% × $20m, r × count_c); r solved so the sum is exactly $20m (iterate: cap binding counties at 12%,
  re-solve r for the rest).
* Largest-remainder rounding to whole dollars.

### 3. Why this gets overlooked in real projects

* HUD publishes both ZIP_COUNTY and COUNTY_ZIP; their names differ by word order only, and the wrong one still produces
  plausible numbers.
* RES_RATIO, BUS_RATIO, OTH_RATIO and TOT_RATIO sit side by side; TOT is the "obvious" one, but business addresses
  concentrate in downtown ZIPs.
* "Assign each ZIP to its main county" is a common simplification that over-allocates to the county holding most of a
  split ZIP.
* SOI files contain a state-total row and an aggregated "other" row that look like ordinary ZIPs.

### 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `21zpallagi.csv` | CSV | ~160k (national, by AGI class) | IRS SOI ZIP Code Data | U.S. Gov public domain | EITC returns by ZIP/AGI class |
| 2 | `21zpallnoagi.csv` | CSV | ~28k | IRS SOI | Public domain | ZIP totals across AGI classes |
| 3 | `21zpdoc.docx` | DOCX |, | IRS SOI | Public domain | Field definitions, 99999 rule |
| 4 | `ZIP_COUNTY_122021.xlsx` | XLSX | ~54k | HUD USPS Crosswalk | Public domain (HUD; registration) | Correct direction |
| 5 | `COUNTY_ZIP_122021.xlsx` | XLSX | ~54k | HUD | Public domain | Wrong-direction file |
| 6 | `ZIP_COUNTY_062024.xlsx` | XLSX | ~54k | HUD | Public domain | Wrong vintage |
| 7 | `hud_crosswalk_documentation.pdf` | PDF |, | HUD PD&R | Public domain | Ratio definitions |
| 8 | `county_fips_state.csv` | CSV | ~100 | Census | Public domain | County names |
| 9 | `allocation_method.pdf` | PDF |, | Task author |, | Rules in §2 |
| 10 | `soi_state_totals_2021.xlsx` | XLSX | ~55 | IRS SOI Historic Table 2 | Public domain | Control total check |

### 5. Deterministic solution path

1. Filter SOI to the state; sum EITC returns over AGI classes per ZIP (or use the no-AGI file); drop 00000; hold 99999.
2. Join ZIP_COUNTY Q4 2021 on ZIP; multiply by RES_RATIO; sum by county; distribute 99999 and unmatched proportionally.
3. Check the state total against SOI state totals.
4. Solve r with the cap; round; report.
5. Contrast: COUNTY_ZIP, TOT_RATIO, dominant county, 2024 vintage.

### 6. The traps

**Trap A, COUNTY_ZIP.** Ratios are county shares; allocation no longer conserves ZIP totals; big counties swell.

**Trap B, TOT_RATIO.** Downtown-heavy county gains, possibly hitting the cap.

**Trap C, dominant county.** Rural counties sharing ZIPs lose.

**Trap D, 00000/99999 rows.** State total double counted; "other" left unallocated.

**Trap E, proportional then cap without re-solve.** Total ≠ $20m.

### 7. Why the data is honest

Both IRS SOI and HUD files are official, documented releases; ZIPs are not areal units and the crosswalk is HUD's documented
solution. Nothing is planted.

### 8. Draft task prompt (prose)

> Split the $20 million weatherization fund across the state's counties in proportion to EITC returns, capped at 12% per
> county, exactly as our allocation method says. Using the IRS ZIP files and HUD crosswalks in the folder, convert the ZIP
> counts to counties, solve the rate and give me every county's award. Produce `county_awards.csv` (county, EITC returns
> allocated, cap flag, award) and `county_awards_chart.png`, a ranked bar chart of awards with capped counties marked and
> a second panel showing how each county's EITC count would change under the COUNTY_ZIP file and under TOT_RATIO. Add a
> one-page `award_memo.pdf` with the rate, the counties at the cap, and the county most affected by the crosswalk choice.

### 9. Deliverables

* `county_awards.csv`, `county_awards_chart.png`, `award_memo.pdf`.

### 10. Where 25+ rubric criteria come from

* County awards and allocated counts (choose a state with 15–30 counties); rate; capped counties; state total check;
  variant deltas.

### 11. Golden-output checklist

* ZIP_COUNTY + RES_RATIO + Q4 2021; special rows handled; cap-and-resolve; exact total; decision stated.

### 12. Build notes (scope tuning)

* Choose a state with many split ZIPs and one dominant urban county near the 12% cap; confirm Traps A/B flip the cap
  status.
* Confirm the EITC field code for tax year 2021 in the SOI documentation.
