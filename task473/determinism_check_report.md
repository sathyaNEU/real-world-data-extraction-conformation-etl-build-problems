# Determinism check, task473, pass 1 (judge thread on target.zip sha256 2c016b81fa5ecb4a)

# Verdict (task473, run r1)

- **Verdict:** NOT_DETERMINISTIC (with the golden blocks otherwise reproducing exactly; no SOLUTION_WRONG on figures).
- **Disposition:** SEND_BACK. The estimator for "the number expected from the records" (guidelines 2.2) has to be closed in the filed text (the WHAT: which records the unknown-BAC chance is drawn from and what it is conditioned on), the unstated local time zone pinned, and the baseline denominators/injury scope made literal; the main list changes with the estimator, so a model rerun is required.
- **Why:** Guidelines 2.2 says only that an unknown-BAC driver's crash "counts its deaths times the chance that at least one of its drivers was at .08 or more", and no shipped file says how that chance is formed. My own derivation from the files (before opening the blocks) used the most direct conditional imputation: untested surviving drivers are exactly the non-arrested drivers at the agencies that do not draw blood routinely (manual 4.2), and the surviving non-arrested drivers tested under the State Patrol/Corwin/Ossian procedure are at .08 or more 7.5% of the time (46 of 612; flat across hour, collision type, vehicle count). That gives high-range = Corwin 0.75, Ossian 0.70, Hatchell 0.66, **Pruett 0.64** (Tanager 0.51), not the golden's Corwin, Hatchell, Ossian, **Tanager**. The golden itself names this route as the wrong one ("Not Corwin, Hatchell, Ossian and Pruett, which one share of unarrested drivers ... (7.5 per cent) gives"). Gate C fails on the main call and supplementary answer 1 (deaths and rates; Pruett 119 vs 102, Tanager 51 vs 67); taxonomy label **competing_defensible_answer** (underspecified method on the decisive quantity). The data lean toward the golden's band-specific catch-rate estimator but do not force it: arrest rates by band are 28.6% vs 88.9% (reproduced), but the county heterogeneity that separates the estimators is weak (chi-square on the .08-.149 share of non-arrested impaired drivers by county 21.0 on 13 df, about p 0.07), and a county-level back-test on the State Patrol drivers' own hidden counts favours the pooled share (corr 0.84, RMSE 1.4) over band-IPW (corr 0.27, RMSE 3.2).

## Evidence (recomputed from the bundle)

| Item | Golden | Mine | Source |
|---|---|---|---|
| Catch rate .08-.149 / .15+ at SP, Corwin SO, Ossian SO survivors | 28.6% / 88.9% | 16/56 and 48/54 (SP only 14/49, 40/45: same ratios) | fcc_2023_person, fcc_2024_2025_person, fcc_agency_directory |
| Tanager arrests 9 / 5, untested impaired 23.1 | 23.1 | 23.12 (96 untested survivors, county agencies incl. UP02701) | person files |
| Deaths (golden band-IPW, uniform within county) | 31,59,63,79,90,84,78,43,52,55,102,66,58,67 | reproduced exactly (31.25, 58.77, 63.14, 78.98, 89.93, 83.99, 78.07, 42.92, 51.76, 55.00, 102.09, 66.00, 57.84, 66.84) | person/crash files, dot_county_dvmt (DVMT x 1000 x 365/366/365) |
| Rates | 0.52 0.56 0.74 0.51 0.45 0.67 0.34 0.57 0.54 0.69 0.55 0.38 0.41 0.67 | reproduced to 2 dp | same |
| Baseline (a) arrests and per cent | 168/41.7 ... 454/32.4 | all 14 reproduce under the literal pipeline | stl_specimen_extract, fcc_agency_directory (post from SPHQ000 case-number prefix) |
| Baseline (b) crashes | 26,80,55,78,79,80,121,26,32,47,122,90,66,104 | all 14 reproduce (latest accepted version, public road, A/B/C, deduped SP/SO twin reports, census-linked crashes and their twins removed, MOTOR VEHICLE driver HAD BEEN DRINKING) | crs_reports_2025, crs_units_2025, fcc_2024_2025_crash |

Competing main-call answers from the same files (high-range lists):
- Golden band-IPW by county: Corwin, Hatchell, Ossian, Tanager.
- Pooled share of non-arrested tested survivors (7.5%, or SP-only 7.1%, Pruett 0.635 to 0.640): Corwin, Hatchell, Ossian, Pruett. Survives as defensible; this is the fork.
- Known-only (no imputation): Corwin, Hatchell, Ossian (Pruett 0.53). Naive and not defensible given 4.2.
- Single catch rate 58.2%: Brisbin, Corwin, Hatchell, Ossian. Ruled out by the 28.6 vs 88.9 band rates.
- Rate of all tested drivers (25-30%): eight or more counties incl. Pruett 0.98. Ruled out (testing is selected).
- Kittredge (0.568, 2 and 2 arrests behind a 0.328 per-driver share) sits 5% below the line on a thin base; Tanager (0.669) and Pruett (0.550) clear by margins that are not noise within the golden method.

Lesser forks on the deliverable asks (each moves graded figures, none changes the list):
1. Local time zone for "arrests made in 2025" is never stated (collected_utc is UTC). It is recoverable only by matching FATAL CRASH specimens to census crash times (about UTC-6 in winter); reading UTC instead changes arrests in 8 counties (e.g. Corwin 251 vs 252, Stroud 342 vs 339, Pruett 417 vs 416) and several per cents at one decimal. Gate B/C minor.
2. Denominator of the per cent: "those arrests" read literally includes drug-only and cancelled kits (golden). Restricting to arrests with an ethanol result lifts every county 2 to 5 points (Brisbin 70.0, Tanager 34.7). The STL annual report's own table uses ethanol-result kits as its base, which makes the other reading natural.
3. "Injury crashes": C (possible injury) counted (golden, 1,006 in total) vs A and B only (542); any-unit drinking (1,160) is excluded by the guidelines' driver definition; the CRS notes define the extract as killed or injured, which supports the golden.
4. Estimator details inside the golden method (pooled vs SP-only catch rates are identical; allocation of the county excess uniformly over untested drivers; county vs agency pooling) are unpinned but did not move the list in my checks.

## Files/Hygiene
PASS. 18 files; formats csv, xlsx, pdf, txt; two files over 25,000 rows (crs_units_2025 45,503, stl_specimen_extract 31,082). Distractors present and unused (fcc_2026_preliminary_crash.csv, dmv_licensed_drivers_by_county_2025.xlsx, stl_annual_report_2025_tables.pdf, whose kit-date basis and unconverted serum differ from the guidelines). Layout change 2011 to 2024 form and agency renumbering, versioned CRS reports with rejected supplements, SP/sheriff twin reports of the same crash, UTC collection times are realistic Layer 1 mess. Dates are coherent with the 1 May 2027 certification (extracts March 2027). cts_fy2028_package_index.csv is a transmittal list, not authoring leakage. No public-data contamination or benchmark disclosure found; fictional state and agencies, with a plausible but synthetic feel. No exclusion-level finding.

## Stump power
High in the intended direction: known-only counting, imputing the tested rate, one catch rate for all BAC, and a pooled non-arrested share each file a different list, so a strong model plausibly fails. But the failure that would be measured is partly a choice between two defensible estimators (pooled share vs band-specific inverse catch rate), which is Gate C territory and cannot be credited as a clean stump until the estimator is closed.

## Stumping type
`mechanism: statistical_rigor` (missing-not-at-random BAC imputation with arrest-dependent testing, a method/model selection), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported figure or stakeholder conclusion is overturned; on clean data the arrest-selection-aware imputation would still separate the answers. Gate G passes.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: estimating alcohol-involved fatalities when BAC is unknown (a FARS-style imputation) with a rate on state vehicle miles is what the field estimates; the swap test fails to read the same. Layer 1: two crash-form layouts and agency renumbering, versioned CRS reports with duplicate agency twins, UTC specimen times, serum versus whole blood. Layer 2: recognising that testing and arrest depend on BAC band, so the unknown-BAC chance must be built from the arrested drivers' band mix rather than the tested rate. Easy route: impute the tested-driver rate (Pruett 0.98 and eight counties in) or the non-arrested share (Pruett 0.64 in, Tanager out). Passes only if the fork is closed.

## Fix
prompt/input_files (guideline 2.2 text): file the estimand for the unknown-BAC chance so its literal execution is the golden (for instance that an unknown driver's chance is derived from how the State Patrol and the Corwin and Ossian sheriffs, who test every surviving driver, arrest drivers by BAC band and from the county's own arrested drivers), state the local zone for collected_utc, and say whether the per cent is of all arrests with a blood specimen or of those with an ethanol result and whether possible-injury (C) crashes count. Keep the data unchanged.
