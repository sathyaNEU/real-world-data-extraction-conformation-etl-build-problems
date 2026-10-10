# ET12 — A public-health "win" that is a coding seam: mortality trends across the ICD-9 → ICD-10 break

| Field | Value |
|---|---|
| Domain | Public health surveillance / program evaluation |
| Objective family | Experiment & Causal Analysis (with code-set conformance) |
| Task shape | 17 · Periods around a change point |
| Core technique | Harmonizing cause-of-death definitions across classification revisions with published comparability ratios; consistent age adjustment to one standard population; baseline projection and run-length test |
| Trap family (honest data) | Real classification change coinciding with the evaluation window; mixed age-adjustment standards |
| Primary sources | CDC WONDER (Compressed Mortality 1979–1998, Underlying Cause of Death 1999+), NCHS comparability-ratio report, NCHS 2000 standard population |

## 1. The real-world project

A state health department's performance office must certify whether a program launched in 1998 "bent the curve" on
a cause of death. Certification unlocks a multi-year performance appropriation. An analyst pulled age-adjusted death
rates for 1990–2005 from CDC WONDER and saw a sharp level shift in 1999.

1999 is the year U.S. death certificates moved from ICD-9 to ICD-10 coding — and the year NCHS moved age adjustment from
the 1940 to the 2000 U.S. standard population. NCHS published **comparability ratios** (ICD-10 count ÷ ICD-9 count on
a dual-coded sample) precisely so trends could be bridged; e.g. influenza & pneumonia ≈ 0.70, Alzheimer's disease ≈ 1.55,
septicemia ≈ 1.19 (preliminary estimates, NVSR 49(2)).

## 2. The business decision (one deterministic recommendation)

**Certify or do not certify: does the program's target cause show a sustained departure from its pre-program trend
after 1998, and if certified, what appropriation does the run length unlock?**

Rules (performance-certification protocol):

* Cause definition: NCHS "113 selected causes" code ranges for ICD-9 (1990–1998) and ICD-10 (1999–2005).
* Comparability: multiply ICD-9-era death **counts** by the NCHS preliminary comparability ratio for the cause (from the
  report in the folder) before computing rates. National ratios are applied to state data.
* Age adjustment: direct method, 11 NCHS age groups, **2000 U.S. standard population**, for every year (recompute from
  counts and populations; do not use published age-adjusted rates from pre-1999 reports).
* Baseline: ordinary least-squares line through 1990–1998 adjusted rates, projected to 1999–2005.
* A post year departs if its rate is below the projection by more than 5% (target cause is expected to *fall*).
* Certify if the longest run of consecutive departing years is ≥ 4; appropriation = $2.5m × run length (from protocol).

## 3. Why this gets overlooked in real projects

* WONDER serves ICD-9 and ICD-10 years from different databases; analysts stitch exports and plot them without opening
  the documentation.
* The break and the program start coincide, so the step change has a ready-made explanation.
* Age-adjusted rates appear in many historical reports; mixing 1940-standard and 2000-standard rates creates a second
  step in the same year.
* Comparability ratios are applied to counts, not to rates; applying them in the wrong direction (dividing) doubles the
  distortion.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `cmf_1979_1998_state_age_icd9.txt` | TSV (WONDER export) | ~50k–200k | CDC WONDER Compressed Mortality | Public domain; WONDER data-use restrictions (no re-identification, suppression <10) | ICD-9 era counts & populations |
| 2 | `ucd_1999_2005_state_age_icd10.txt` | TSV | ~50k–200k | CDC WONDER Underlying Cause of Death | Same | ICD-10 era counts & populations |
| 3 | `ucd_1999_2005_state_age_113causes.txt` | TSV | ~100k+ | CDC WONDER (113 cause list grouping) | Same | Cross-check |
| 4 | `nvsr49_02_comparability.pdf` | PDF | — | NCHS National Vital Statistics Reports 49(2), 2001 | Public domain | Comparability ratios |
| 5 | `nchs_113_causes_icd9_icd10_codes.xlsx` | XLSX | 113 | NCHS (instruction manual tables) | Public domain | Code ranges per era |
| 6 | `us_standard_population_2000.csv` | CSV | 11–19 | NCHS / SEER | Public domain | Weights |
| 7 | `nvsr47_03_age_adjustment.pdf` | PDF | — | NCHS (age-adjustment standard change) | Public domain | Standard change documentation |
| 8 | `state_published_rates_1996_1998.pdf` | PDF | — | State vital statistics annual report (public) | Public | Example of 1940-standard rates |
| 9 | `program_timeline.json` | JSON | ~5 | Task author | — | Program start, target cause |
| 10 | `certification_protocol.pdf` | PDF | — | Task author | — | Rules in §2 |

## 5. Deterministic solution path

1. Extract counts and populations by state, year, age group for the cause in each era with the correct code ranges.
2. Multiply 1990–1998 counts by the cause's comparability ratio.
3. Compute age-specific rates and 2000-standard age-adjusted rates for every year.
4. Fit the 1990–1998 OLS line; project; compare 1999–2005; find the longest departing run; certify or not; compute amount.
5. Show unadjusted and mixed-standard series for contrast.

## 6. The traps

**Trap A — no comparability adjustment.** For a cause with ratio ≈ 0.70, the 1999 level drops ~30% "because of the
program"; every post year departs → certify with full appropriation.

**Trap B — dividing by the ratio / applying to post years.** Reverses or doubles the seam.

**Trap C — published pre-1999 age-adjusted rates.** 1940-standard rates are much lower for causes concentrated in the
elderly; a spurious jump or drop appears in 1999.

**Trap D — wrong code ranges.** Using ICD-10 J09–J18 vs J10–J18 or including unrelated ICD-9 codes changes counts by a
few percent — enough to move a 4-year run.

## 7. Why the data is honest

All counts are official NCHS tabulations; the coding revision and standard-population change are real and documented,
with published bridging ratios. The analysis must use them.

## 8. Draft task prompt (prose)

> The legislature will release the performance appropriation only if the target cause in the program file shows a
> sustained break below its pre-program trend, as defined in our certification protocol. Using the WONDER extracts and
> NCHS documents in the folder, build the comparable series for 1990–2005, test each year from 1999 on against the
> committed 1990–1998 trend, and tell me whether to certify and what the run length unlocks. Provide
> `trend_break.png`, the annual adjusted rates with the projected baseline, the 5% band, departing years highlighted
> and the 1999 coding change marked, and `certification_memo.pdf` leading with the decision and amount, then a table of
> all sixteen years (deaths, comparability-adjusted deaths, age-adjusted rate, projection, departure flag) and a
> paragraph on what an unadjusted analysis would have concluded.

## 9. Deliverables

* `trend_break.png`, `certification_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 16 annual adjusted rates; 7 post-year projections/flags; slope/intercept; run length; decision; amount; unadjusted
  contrast.

## 11. Golden-output checklist

* Comparability ratio on ICD-9 counts; 2000 standard throughout; correct code ranges; decision follows protocol.

## 12. Build notes (scope tuning)

* Choose a state and cause where the unadjusted series certifies and the adjusted series does not (influenza &
  pneumonia or Alzheimer's/septicemia in the opposite direction). Small states hit WONDER suppression; prefer large
  states.
* Quote the exact ratio (with its confidence interval) from the NVSR table you include; final vs preliminary ratios
  differ slightly — the protocol must name which one.
