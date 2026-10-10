# ET33 — Did poverty really rise in these tracts? Non-overlapping ACS periods, margins of error and moved tract lines

| Field | Value |
|---|---|
| Domain | Community development / municipal grants / survey statistics |
| Objective family | Descriptive & Distribution Analysis (statistical scorecard) |
| Task shape | 10 · Scorecard against thresholds (tract × test) |
| Core technique | Survey-estimate comparison with documented MOE propagation and significance testing; re-apportioning older estimates to current tract geography via a weighted crosswalk; correct universe for rates |
| Trap family (honest data) | Overlapping 5-year periods compared; tract GEOIDs matched across the 2010/2020 boundary change; MOEs ignored or mis-scaled; total population as denominator |
| Primary sources | Census ACS 5-year detailed tables (B17001), Census guidance on comparing ACS data, 2010↔2020 tract relationship/crosswalk files |

## 1. The real-world project

A city's neighborhood-stabilization fund designates a neighborhood when **at least 3 of its 8 census tracts** show a
statistically significant increase in poverty rate *and* a current poverty rate of at least 20%. The analyst compared
ACS 2018–2022 with 2019–2023, matched tracts by GEOID, and compared point estimates. Six tracts "rose"; the fund's
statistician refused to sign.

## 2. The business decision (one deterministic recommendation)

**Go / no-go: does the applicant neighborhood qualify?**

Rules (fund's statistical standard):

* Periods: ACS 5-year **2014–2018** vs **2019–2023** (non-overlapping, per Census guidance).
* Geography: 2020 tracts. Re-apportion 2014–2018 (2010-tract) counts to 2020 tracts with the crosswalk in the folder
  (2010→2020 tract weights based on block-level population); MOE of a re-apportioned count = √Σ (w × MOE)².
* Rate = below poverty ÷ population for whom poverty status is determined (B17001 total).
* MOE of a proportion: (1/Y)·√(MOE_X² − p²·MOE_Y²); if the radicand is negative use + (Census formula).
* SE = MOE ÷ 1.645; Z = (p₂ − p₁) ÷ √(SE₁² + SE₂²); significant increase if Z > 1.645.
* Tract passes if significant increase **and** p₂ ≥ 20%. Neighborhood qualifies if ≥ 3 of its 8 (2020) tracts pass.

## 3. Why this gets overlooked in real projects

* Consecutive 5-year releases are the most natural comparison and Census tables make them easy to download; they share
  four of five years of sample, so differences are mostly noise.
* Many tract GEOIDs survived the 2020 redraw with changed boundaries; others split (new suffixes) or merged. GEOID joins
  "work" and are wrong.
* Point-estimate comparisons look decisive in a table; tract-level MOEs are large.
* B17001's universe excludes people in institutions, college dorms and some others — total population is the wrong
  denominator.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `acs5_2018_B17001_tracts_state.csv` | CSV | ~1.5–8k tracts × ~60 columns | Census ACS API | U.S. Gov public domain | 2014–2018 estimates + MOEs (2010 tracts) |
| 2 | `acs5_2023_B17001_tracts_state.csv` | CSV | ~1.5–8k × ~60 | Census | Public domain | 2019–2023 estimates + MOEs (2020 tracts) |
| 3 | `acs5_2022_B17001_tracts_state.csv` | CSV | same | Census | Public domain | Overlapping-period decoy |
| 4 | `tab20_tract20_tract10_natl.txt` | Pipe-delimited | ~200k | Census 2020 relationship files | Public domain | Area-based relationships |
| 5 | `nhgis_tr2010_tr2020_crosswalk_state.csv` | CSV | ~10–50k | IPUMS NHGIS geographic crosswalks | IPUMS NHGIS terms (free; citation required) | Population weights |
| 6 | `acs_general_handbook_ch7_ch8.pdf` | PDF | — | Census "Understanding and Using ACS Data" | Public domain | MOE formulas, overlapping-period warning |
| 7 | `tl_2023_xx_tract.zip` | Shapefile | ~tracts | Census TIGER/Line | Public domain | Map |
| 8 | `neighborhood_tracts.json` | JSON | 8 | Task author | — | Applicant tracts |
| 9 | `fund_statistical_standard.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `acs_table_shell_B17001.xlsx` | XLSX | — | Census | Public domain | Line meanings |

## 5. Deterministic solution path

1. Extract below-poverty and universe estimates/MOEs for both periods.
2. Re-apportion 2014–2018 counts to 2020 tracts with crosswalk weights; propagate MOEs.
3. Compute rates and proportion MOEs; Z-scores; tests; pass flags; count passing tracts.
4. Decide; show the overlapping-period and GEOID-match variants.

## 6. The traps

**Trap A — overlapping periods.** Different, unstable answer; the standard forbids it.

**Trap B — GEOID matching across 2010/2020.** Split tracts compare unlike areas; one or two tracts flip.

**Trap C — no MOEs.** Every point increase counts; neighborhood qualifies falsely.

**Trap D — 1.96 / wrong proportion formula.** Borderline tracts flip.

**Trap E — total population denominator.** Rates shift in tracts with dorms or institutions.

## 7. Why the data is honest

ACS estimates and MOEs are official; the comparison rules and formulas are Census-published. Tract redraws are real
decennial changes.

## 8. Draft task prompt (prose)

> The applicant neighborhood qualifies for the stabilization fund only if at least three of its eight tracts show a
> statistically significant rise in poverty rate and a current rate of at least 20%, under our statistical standard.
> Using the ACS files and crosswalks in the folder, test each tract and give me the decision. Deliver
> `tract_tests.xlsx` with one row per 2020 tract showing both periods' counts, universes, rates and MOEs, the Z-score and
> both test results; and `tract_change_chart.png`, a dot-and-interval chart of each tract's two rates with 90% intervals
> and passing tracts highlighted. On the first sheet, state the decision, the number of passing tracts, and the tract
> closest to flipping.

## 9. Deliverables

* `tract_tests.xlsx`, `tract_change_chart.png`.

## 10. Where 25+ rubric criteria come from

* 8 tracts × (rates both periods, Z, test results) ≈ 32 checks; decision; closest-to-flip tract.

## 11. Golden-output checklist

* Non-overlapping periods; re-apportioned to 2020 tracts; Census MOE formulas; correct universe; decision stated.

## 12. Build notes (scope tuning)

* Choose a neighborhood with at least one 2010 tract split in 2020 and 2–4 tracts near the significance boundary;
  confirm Trap C or Trap A flips the decision.
* Record the NHGIS crosswalk version and cite IPUMS NHGIS as its terms require.
