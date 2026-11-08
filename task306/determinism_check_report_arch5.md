# Determinism verdict, task306 (architecture 5, pass 1)

Judged cut: target.zip sha256 0bacf975417942bda8ded8b87d3c590433362b13976eb95853d4c95eb95b59f9, 2026-11-08. One isolated judge thread (Sonnet, medium effort) reading only the unzipped bundle and the graded blocks. The fix that followed is in DESIGN_NOTE.md, section Stage 4; the re-judge is determinism_check_report_arch5_pass2.md.

- **Verdict:** DETERMINISTIC, SOLUTION_WRONG (SOLUTION_STEPS step 6 wording only; every golden figure reproduces).
- **Disposition:** FIX_NOW. Reword step 6 so the GP Connect match reads "patient and sender, document date on or after the letter date and within 15 days (the GP Connect document date is the day of receipt)". Optionally also state the Marches re-send rule and the bank-holiday rule in the solution blocks. No bundle change, no model rerun.
- **Why:** The main call is forced by the shipped files. Review B (12.0 harms) beats C (8.1) and A (6.2) once the pilot off-rate is split by who started the medicine, a split the specialist-started patients make decisive. A is 86% specialist-started in scope and 15% in the pilot, and specialist-started patients come off at about 4% in all three reviews. Pooled pilot rates give A 24.1, B 11.8, C 10.8, so the easy route recommends A. Every number reproduced.

## Evidence (recomputed from target/)
| Item | Result | Reproduced |
|---|---|---|
| Scope on 31 Dec 2026 (outside Clun, registered at date, protocols A/B/C incl. exclusions, ages from birth_month) | A 612, B 1,239, C 1,636 | yes. Unchanged under issue-window variants (1 Jul or 2 Jul start), repeat-only against all issues |
| Specialist-started share (letter naming the class, letter_date 0 to 60 days before the earliest course's first_issue_date; Marches dd/mm/yyyy, lookup resolves 9,514 pseudonym-less lines, 0 unresolved) | A 85.8%, B 6.1%, C 43.9% | yes. Identical under letter_date or encounter_date, Start-only or any recommendation, windows 30 to 365 days (letter lags are 5 to 26 days, nothing in 30 to 365) |
| Pilot six-month rows split the same way | A 63/136 and 1/24; B 68/276 and 1/24; C 65/192 and 2/48 | yes |
| Patients off | A 62.2, B 289.7, C 340.7 | yes (60, 290, 340) |
| Harms a year (table 1 rate at age 31 Dec 2026) | A 6.15, B 11.99, C 8.10 | yes (6, 12, 8). Gap 3.9, shown as 4 either way |
| Ask 7 letters, H1 | 46.0 / 43.5 / 45.7 / 42.3 / 43.0 | yes |
| Ask 7 letters, H2 | 43.3 / 40.4 / 40.6 / 37.4 / 41.7 | yes, but only with the corrected GP Connect match (below). Literal "patient, sender and document date equal to the letter date" matches 757 of about 3,960 Oct to Dec letters and gives 28.8 / 26.5 / 27.1 / 25.3 / 28.3 |
| Ask 1 consultations (attended hub 1-to-1 in UK time, clinical-system rows less hub duplicates, attended group patients; network on the day; list at quarter start) | all 20 cells match golden | yes, with "next working day" skipping bank holidays. Weekend-only skipping moves one cell: Wrekinside North Q2 11.7 against 11.6 |

Robustness checks:
- The off-rate column in the pilot log matches the issue record exactly. For C, "off" means no gabapentinoid issued; opioids stay issued in all 240 cases. The gabapentinoid class is therefore grounded. An opioid-inclusive class would give C 398 patients, 9.4 harms and a gap of 3, but the data rule it out.
- The pilot is homogeneous by practice, pharmacist, month, plan and course duration. The starter split is the only effect modifier.
- Deaths: a reviewed denominator instead of a checked denominator gives 60.7 / 286.6 / 337.5 patients and 6.0 / 11.9 / 8.0 harms. The rounded answers are unchanged.

## Competing answers and forks
- **A by pooled pilot rates (40.0%, 23.0%, 27.9% in the close-out):** this is the easy route, not a defensible alternative. The pilot patients' mix of starters is 15% specialist against 86% in scope for A, and the pilot rate by starter is not transportable otherwise.
- **Uncertainty on 1/24 specialist-started cells:** A would only overtake B if its specialist rate exceeded about 14% (the point estimate is 4.2%). The same ~4% shows in all three reviews (4/96 pooled), so a reasonable estimator does not reach it. The margin is thin on A's side only in a confidence-interval sense.
- **Ask 7, H1 cells (residual risk, not decisive):** the Marches re-send rule is unfiled. 152 Marches letters were re-issued on 7 April 2026 under new MMH-EPR references with identical patient, service, encounter date and lines, and the practice received both copies. Without the rule H1 reads 46.8 / 44.1 / 46.5 / 43.0 / 43.6. An expert counts them once, but no shipped sentence says so. A convention this open should be closed in the design note's fork table.
- **Ask 1 bank holidays:** "next working day" is not defined in the package. The data show it: the lag histogram is 0, 1, 3, plus 4 for Fridays before a Monday bank holiday, and there is no clinic activity on bank holidays. One cell differs under a weekend-only reading.

## Files / Hygiene: PASS
18 files in csv, parquet, pdf and xlsx, with four formats. The feed is 176,956 rows, the workflow 43,805 rows and the registrations 317,930 rows. Distractors present: falls admissions, ePACT2 summary, close-out report. Mixed date formats (Marches dd/mm/yyyy against ISO), reference-format change to GUIDs on 1 Oct, EPR migration and merged practices read as authentic system mess. No authoring language and no temporal contradiction (close-out 5 Jan 2027, extract 6 Jan 2027, board in January 2027). No exclusion-level finding.

## Stump power (Gate F)
Strong. The close-out report states homogeneity by practice, age and sex (true), so a solver who stops there pools the pilot and files A at about 24 harms against a golden 6, flipping the call. The stump needs the effect modifier found through the large letter feed, the lookup and the course start dates. The data separate the candidates cleanly, with no near-tie on the B-over-C call (3.9 harms).

## Stumping type (Gate G)
`mechanism: decomposition_attribution` (standardising honest pilot rates to the target population's case mix), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported pooled rates are correct for the pilot and the difficulty sits in transporting them, and the task still stumps on perfectly clean data.

## Three rules (Gate H)
`domain: pass`, `layers: pass` (Layer 1: layout and reference-format changes, hash-less feeds joined through a lookup, merged practices, UTC to UK time, re-sent letters; Layer 2: pilot-to-programme transportability by treatment initiator), `decisive_step: analytical`.
Medicines optimisation estimates harm avoided from uptake rates and baseline risk. The easy route, a strong analyst applying the pooled pilot off-rate to scope, recommends A (about 24 harms) against the golden B (12).
The swap test fails if the nouns change, since uptake and attributable harm by age band are the field's own work, so the domain is not a backdrop.

## Fix
solution: reword step 6's GP Connect match (above). Optionally state the Marches re-send and bank-holiday conventions in the design note's fork table so ask 7 and ask 1 each have a closed row.
