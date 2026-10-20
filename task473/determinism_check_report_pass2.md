# determinism-check report, task473, 2026-10-20 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Gate G and Gate H reconciliation
The thread's mechanism and family match the card (stump_class analytical). Gate H: domain pass, layers pass, decisive_step analytical. It reached the golden by the band catch rate only after its own leave-one-agency-out check rejected the pooled share, one catch rate and the covariate models, so the method is forced by the data rather than filed.

## After the pass
Ask B's primary was re-sited after this pass (stage 4 readers took it through a coordinate link to the census); the call, the estimand and every main-call figure are unchanged, and the new device is asserted fair in checks.py (each K report outside the census a supplement submitted more than 30 days after its crash).

## Thread verdict (verbatim)



**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair is needed and no model rerun is required. One optional hardening note is under Why.

**Why:** I rebuilt every committed answer from the shipped files and they all reproduce exactly. The main call is Corwin 0.71, Hatchell 0.68, Ossian 0.68 and Tanager 0.66, with Kittredge 0.57 the nearest below the line. The decisive inputs are all in the package:
- Guidelines 2.2 to 2.4 give the estimand: expected deaths per crash, with 366 days in 2024.
- Manual 4.2 says the State Patrol and the Corwin and Ossian sheriffs draw blood from every surviving driver.
- The 144 arrested drivers at the other agencies are the only ones tested there.
- The universal-test agencies give the arrest rates by BAC band (see Evidence).

The method for untested drivers is not filed in the prompt. The shipped data separates the candidates, which makes the decisive step a validated method choice rather than a hidden rule, so Gates A to E pass.
- The wrong-method routes each give a different list. A single unarrested share gives Corwin, Hatchell, Ossian and Pruett. A single catch rate gives Brisbin, Corwin, Hatchell and Ossian. A covariate model gives Pruett in and Tanager out (residual form) or Tanager and Pruett both in (direct form).
- A leave-one-agency-out check at the 16 universal-test agencies prefers the band catch rate. Its RMSE is 1.4 drivers, against 3.2 to 3.6 for the single-rate and share routes and 3.5 to 5.6 for the covariate routes.

**Evidence:**

| Item | Result |
|---|---|
| Surviving-driver arrest rates at universal-test agencies | 20 of 70 at .08 to .149 (28.6%); 72 of 81 at .15 or more (88.9%). Reproduced. |
| Tanager excess impaired, untested | 21.0 of 87 untested. Reproduced. |
| Deaths and rates, 14 counties | All deaths match to the whole number and all rates to two decimals. Tanager is 65.8 deaths on 9.9913 billion miles, 0.659. Hatchell is 0.679 and Ossian 0.680. |
| STL arrests and per cent at .15 or more, 2025 | All 14 counties match. |
| CRS injury-crash counts | All 14 counties match (total 1,001). |

How the STL and CRS counts were reproduced:
- **STL arrests.** Central-time date of the first kit, tube 1, amended result over superseded, serum divided by 1.16. The 210 PD+SO same-jail same-minute pairs are collapsed, and State Patrol headquarters submissions go to the post named in the case number.
- **CRS counts.** Latest accepted version, public road, severity A, B or C, a motor-vehicle driver HAD BEEN DRINKING. The 46 SP+SO duplicate pairs (same date and road, up to 12 minutes apart, matching drivers) are collapsed. The census exclusion is by report number, then by date, road and time within 10 minutes (or blank census time with the same agency or county).

Competing readings for the main call, by name and the answer each gives:

| Reading | List it gives |
|---|---|
| Single unarrested share (7.2%) | Corwin, Hatchell, Ossian, Pruett |
| Single catch rate (60.9%) | Brisbin, Corwin, Hatchell, Ossian |
| Covariate (night, single-vehicle, age, road) logistic, direct | Corwin, Hatchell, Ossian, Pruett, Tanager |
| Covariate logistic, residual | Corwin, Hatchell, Ossian, Pruett |
| Smooth log-BAC logistic for catch | Adds Kittredge (0.63) |
| Linear-BAC logistic catch | Same four; Kittredge 0.594 |
| Re-banding the catch rate: any cut sets between .10 and .15, plus a five-band split | Same four |
| Per-agency allocation | Same four |
| 2025 untested drivers imputed from the officer's observed condition in the CRS | Same four; Tanager 0.674, Kittredge 0.572 |

Only the first four and the log-logistic differ from the golden. Each is rejected by the leave-one-agency-out check, and the arrest rates show a step at .15, not a smooth curve.

Margin notes:
- Tanager's lead rests on the 20 of 70 mid-band catch rate. It drops below 0.60 only if that rate exceeds about 0.36 (sampling interval 0.19 to 0.40).
- Kittredge enters only if the rate is about 0.19 or lower.
- The estimand is the point estimate "expected from the records", and every defensible estimator of that point lands on the same list. This is thin but clean, not contested.
- Optional hardening is none.

Supplementary answers, each checked for a fork:
- **Arrests.** The sheriff and police same-jail same-minute duplicates are inferred from the data. All 210 pairs are PD+SO at a jail and none is PD+PD, so the inference is forced. Not collapsing them overstates each county by 2 to 10.
- **Injury crashes.** The duplicate and census matching is fuzzy (up to 12 minutes) but separates cleanly. Real duplicates have identical driver signatures and gaps of 12 minutes or less, and every non-duplicate has a gap of 63 minutes or more or a different county. Stroud's 14:23 sheriff report against the 11:51 census crash (152 minutes) must stay counted, and does in the golden. Counts are exact-graded, so a solver who uses only exact time or number matching misses by 1 to 6 per county. That is a difficulty source, not an ambiguity.
- **Placement of State Patrol headquarters submissions.** The post comes from the case-number prefix (P03 is post 3). No document states this. The CRS and census State Patrol report numbers use the same prefix pattern with the post agency IDs, so it is inferable. Assigning them to the headquarters county (Keswick) would shift roughly 1,470 arrests.

**Files/Hygiene:** PASS.
- 18 files in four formats: csv (9), xlsx (3), pdf (4), txt (1). The largest is stl_specimen_extract_2023_2025.csv with 31,781 rows.
- Distractors: fcc_2026_preliminary_crash.csv (outside the window), dmv_licensed_drivers_by_county_2025.xlsx, stl_annual_report_2025_tables.pdf (counts kits by received date, not arrests).
- Timeline coherent: certification due 1 May 2027, extracts dated February and March 2027.
- Minor: cts_fy2028_package_index.csv is a transmittal manifest listing every shipped file. It is in-fiction and not exclusion-level.
- Synthetic fictional state and counties, no authoring disclosure, nothing exclusion-level.

**Stump power:** Good. The trap is picking how to impute untested impaired drivers. The easy routes are a pooled catch rate, a pooled unarrested share, or covariate prevalence. They produce Brisbin or Pruett lists and drop Tanager, and a strong model could plausibly take one. The asks are heavy and exact-graded (CRS fuzzy dedupe and census matching, STL dedupe, State Patrol headquarters placement), which should hold the ask score down.

**Stumping type:** `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported number is wrong. The difficulty is a missing-data and selection problem (arrest depends on the BAC band), worked as an inverse-catch-rate imputation and validated out of sample.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1 is the 2011 and 2024 form layouts, agency recodes, serum and whole-blood results, amended against superseded reports, duplicate kits, UTC dates and cross-system crash duplicates. Layer 2 is a missing-BAC imputation for the impaired-driving fatality rate (the missing-alcohol-result problem traffic safety works on). A strong analyst who read every rule correctly could still use one pooled share, one catch rate or a covariate model, and file Pruett or Brisbin instead of Tanager. The swap test fails if "visits" or "megawatt-hours" are put in, because the rate depends on BAC, arrest selection and vehicle miles.

**Fix:** none.
