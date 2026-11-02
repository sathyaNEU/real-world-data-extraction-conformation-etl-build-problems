# determinism-check report, task473, 2026-11-02 (pass 3)

## Verdict
NOT_DETERMINISTIC (court ask 2 only; the main call, rates and deaths are forced)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection (missing-data imputation of an arrest-biased test; etl_conformance in the court ask), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, `/tmp/determinism-check-task473-032828/verdict.md`, bundle md5 76759c758992d8cdccbc959b554a48f5. Governing label: underspecified_objective. Gates A and B pass; Gate C fails for ask 2 only.

## Why
The court file has no person column and no shipped file says how a re-opened case links to its predecessor. Guidelines 3.1 says only "one for each person charged and offense". The golden counts a case dismissed on the day the same court opened another for the same offense date and agency as one prosecution with that later case. The files equally support linking only when the lead charge is unchanged (all 14 counties move) and linking a dismissed case to any later same-key case filed after the dismissal (4 counties move).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Deaths, 14 counties (aoc/fcc crash+person, injury K, 30 days) | 32, 59, 60, 79, 90, 85, 78, 43, 51, 54, 102, 67, 57, 66 | 32.0, 58.8, 60.0, 79.0, 90.0, 84.8, 78.1, 43.1, 51.2, 54.1, 101.9, 66.7, 57.2, 65.8 | yes, all 14 |
| Rates (DVMT x 1000 x days, 366 in 2024) | Aldous 0.52 ... Corwin 0.71, Hatchell 0.68, Ossian 0.68, Tanager 0.66, Kittredge 0.57 | same at 2 dp, all 14 | yes |
| Certified list | Corwin, Hatchell, Ossian, Tanager | same; smallest margin 0.030 (Tanager) | yes |
| CC1 arrest rates at universal-test agencies | 28.6%, 88.9% | 20/70 and 72/81 (937 drivers tested) | yes |
| CC2 Tanager untested impaired | 21.0 | 8 x 2.5 + 8 x 0.125 = 21.0 | yes |
| Back-test RMS miss | 1.1 vs 3.4 | 1.16 vs 3.48 (3.92 pooled) | yes |
| 7.2% unarrested share | 7.2 | 59/820 | yes |
| Pooled catch 60.9% list | Brisbin, Corwin, Hatchell, Ossian | same | yes |
| Ask 2 offenses, 14 counties | 160, 335, 225, 354, 400, 340, 523, 192, 250, 211, 379, 370, 314, 415 | same under the same-day link | yes, under that link only |
| Ask 2 per cent convicted | 57.5, 63.3, 62.7, 62.4, 62.5, 60.0, 64.6, 58.3, 56.8, 60.2, 54.9, 62.4, 60.8, 62.2 | same under the same-day link | yes, under that link only |

## Competing answers that survived
Court file: 31,430 rows, key (court, case_number) unique, 4,762 DUI-lead cases with a 2025 offense date, 886 dismissed, 294 of those re-opened the same day.

| Reading (n / % convicted) | Counties changed |
|---|---|
| Golden: link a dismissal to the same-key case filed that day | none |
| (a) one per case number (Aldous 171 / 53.8, Tanager 437 / 59.0, Pruett 399 / 52.1) | all 14; contradicts guidelines 3.1 |
| (b) link only if lead charge also the same, 65 of 294 pairs change charge (Aldous 162 / 56.8, Brisbin 340 / 62.4, Corwin 231 / 61.0, Delmont 361 / 61.2, Tanager 418 / 61.7) | all 14 n, 13 of 14 per cents; cannot be dismissed, "offense" can mean the charged offense |
| (c) link a dismissal to any later same-key case filed on or after dismissal, 6 extra cases (Delmont 353 / 62.3, Fairlee 398 / 62.6, Keswick 521 / 64.7, Renwick 369 / 62.3) | 4 counties; defensible |
| (d) collapse every same-key case (Aldous 149 / 56.4, Keswick 420 / 66.9) | all 14; weakest |
| (e) weight by counts column (Aldous 269 / 55.8) | all 14; excluded by the text |

The six (c) cases: Delmont CT-25-00530 / 00680, Fairlee CT-25-00314 / 00695 and CT-25-00643 / 00771, Keswick CT-25-00824 / 01350 and CT-25-01370 / CT-26-00211, Renwick CT-25-00374 / 00828 (gaps 1 to 83 days).

Closed readings: window boundaries have one reading (offense in calendar 2025 by offense_date; latest filing 2026-06-05, latest disposition 2027-02-28, so the cutoff binds nothing). Conviction is closed (guilty plea or verdict with a DUI convicted_charge; amended charge, deferral, dismissal, acquittal, blank are not; disposition and convicted_charge agree on every row). County comes from the court (0 mismatches). Minor fork: if DUI-drugs (1201(3)) were excluded, all 14 counties change (Aldous 154 / 57.8, Tanager 391 / 61.9); inclusion is the natural reading of "impaired-driving".

Rate-side sensitivities are stable (allocation by county, agency or county-year; 365-day DVMT; State Patrol only or sheriffs only calibration). Only a 2023-only calibration moves four values, not a reasonable reading. The estimator is not literally filed ("the number expected from the records", guidelines 2.2) but is forced by the data, manual 4.2 and the back-test.

## Spec gates
Checked by me against the unzipped bundle and metadata.json.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | CSV, XLSX, PDF | yes |
| Large file | 25,000 rows or more | aoc file 31,430 rows | yes |
| Distractors | 2 or more, named in metadata, none labelled in a file name | dmv_licensed_drivers_by_county_2025.xlsx, fcc_2026_preliminary_crash.csv (names carry no label) | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | judge: neither enters the solution | yes |
| Deliverables | 1 to 3, all in golden | 2, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | stated in the prompt; ask 2 is not determinate (above) | no, ask 2 |
| Prompt shape and 25 criteria | identifiable, 25 or more | not assessed by the judge thread; not re-verified here | open |
| Reads as real work | no LLM tells | judge: only a mild tell (identical catch rates 28.6 / 88.9 at the State Patrol and the two sheriffs) | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H line: domain pass, layers pass, decisive_step analytical (field's own BAC imputation then rate per VMT; Layer 1 is the 2024 form change, former agency codes, thousandths, DVMT in thousands, re-opened court cases; Layer 2 is the arrest-selection correction). The design note (`DESIGN_NOTE.md` ## Three rules, decisive step "G") names the same decisive move, band-specific catch rates measured at the universal-test agencies; its declared distractors (licensed-driver counts, the 2026 preliminary crash file) match metadata.json and the thread did not name either as the surface read. No mismatch found. The note says nothing arbitrates the court ask's link device, which is the finding.

## Stump power (Gate F)
Moderate to good. A strong model that reads manual 4.2 and guidelines 2.2 will impute but may pool one catch rate (Brisbin in, Tanager out) or use one unarrested share (Pruett in, Tanager out). The decisive step is the field's standard imputation reached with a back-test the data settle, so a strong solver can land it; the main thread weighs this against the ladder. Ask 2's refiling reconstruction stumps on its own but not validly until pinned.

## Findings, ranked
1. Ask 2 (county_impaired_driving_rates_2023_2025.csv, offenses and per cent convicted): the definition of one prosecution is open; readings (b) and (c) are both defensible and move 14 and 4 counties.
2. Six same-key cases filed after dismissal on a later day create reading (c).
3. Minor: DUI-drugs inclusion is natural but unstated.
4. Estimator not literally filed; accepted as forced by data and back-test.

## Next action for the author
Fix in the prompt or guidelines section 3.1 (WHAT, not HOW): state that a case dismissed and re-opened the same day against the same offense date and agency is one prosecution with the re-opened case, and whether a changed charge subsection counts; optionally remove or separate the six later-day same-key cases. Rebuild, reproduce the ask-2 regrade, leave the main call, rates and deaths byte-identical, re-judge once.
