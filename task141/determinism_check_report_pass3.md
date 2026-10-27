# determinism-check report, task141, 2026-10-27 (pass 3, run r3)

Judged zip: target.zip sha256 2b59136607bde453. The coordinator reports the FIX_NOW below is already applied on a rebuilt zip (9d45538d7ae0b10a); that zip gets its own re-judge and is not covered here.

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG (Ask 3 of the xlsx listed the five parts of the projection with no admissions, so it had no committed values to grade).
**Disposition:** FIX_NOW (solution block only; bundle and prompt unchanged, no rerun).
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call is forced by the shipped files. Sections 4 and 5 of SB 26-118 leave the 3,003 terms no room to extend. The record shows terms at their class maximum drawing a petition in their last 120 days about 2 in 5 times, against 6 per cent for terms with room. That at-maximum rate holds in every class, including DF4, whose 24-month maximum matches the Act's cap. Instructions 4.1 make the courts' and officers' recorded behaviour the basis of the projection. The judge's own rebuild gives 1,357 to 1,395 against the golden's 1,383, which is 7 pods in every build it ran. The pooled-rate route (886, 5 pods) and the trailing year (833, 4 pods) are the wrong easy routes.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Open felony terms at 30 Sep 2026 | 7,598 | 7,598 (cms2, FELONY and OPEN; cms1 all closed) | Yes |
| Terms ending 31 Mar 2027 | 3,003 | 3,003 (also 3,003 using the PROB-COND release date) | Yes |
| End-of-term petition share, at class maximum | about 2 in 5 | 38.5% (3,629 of 9,424); 37.96% to 38.98% for 90 to 150 day windows | Yes |
| End-of-term petition share, with room | 6 per cent | 6.19% (1,255 of 20,286); 5.1% to 7.1% across window lengths | Yes |
| Room windows ending in an extension | more than half | 56.0% | Yes |
| Trailing-year admissions | 833 | 833 | Yes |
| Projection | 1,383 (1,370 to 1,402) | 1,357 to 1,395 from an independent hazard rebuild | Not exactly (method is open); brackets it and rounds to 1,400 |
| Pooled-rate route | 886 | about 0.8 to 0.9 thousand | Consistent |
| Pods | 6 pods cover 1,260; 7 pods cover 1,261 to 1,470 | same (instructions Annex, 64 beds, 210 per pod) | Yes |
| Bed-days, four quarters, felony and misdemeanor | 24,970 / 2,219; 24,266 / 2,281; 23,100 / 2,062; 24,762 / 2,475 | all eight exact | Yes |
| Office-by-tenure cells | 16 cells, Central 982/915/640/735 and so on | all 16 exact (officer's office in effect on 30 Sep 2026) | Yes |
| Hazard back-test | not claimed | 1,010 predicted without attrition (957 with) against 996 actual petitions, Jan to Sep 2026 | The no-attrition build is the better calibrated |

## Competing answers that survived
No fork survives that changes the pod count, but four are recorded.
1. **Attrition-adjusted build.** A 13 to 15 per cent annual exit hazard gives 1,281 to 1,318, so 1,300 to the nearest 100, still 7 pods but only about 21 above the 1,260 line at the low end. The back-test favours the shipped no-attrition build, and the standing-variants list does not name attrition. This is the thinnest part of the task. 7 pods holds in every build; the nearest-100 figure of 1,400 does not hold under attrition.
2. **Section 4 proviso read literally.** The 552 terms whose scheduled expiration falls between 1 Jan and 30 Mar 2027 could be moved to 31 Mar. The effect is at most about 60 admissions (1,443 at most). The pod count and 1,400 are unchanged. The coordinator says the rebuilt zip restates section 4 of the Act, which should close this.
3. **Lost-extension split (1,108, 6 pods) and every would-be extension a petition (1,728).** Neither is defensible against the direct at-maximum rate the record gives (39.1% for DF4, 36.6% to 41.9% for F2 to F6).
4. **Office of a probationer (Ask 5).** The cms2 intake `office` column gives a different table (Central 829/913/707/818, Eastfield 426/121/0/0), and 1,621 of 7,598 cases disagree. No shipped file defines that column. The officer's assignment office is the better-supported reading. It is a data-semantics step on one supplementary ask only, low to moderate risk.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | Yes |
| Formats | 3 or more | csv (10 including the codes lists), pdf (3), xlsx (1) | Yes |
| Large file | 25,000 rows or more | bookings 45,550; crosswalk 50,323; cms1 30,028 | Yes |
| Distractors | 2 or more in `metadata.json`, none labelled in a file name | `apd_annual_report_2025.pdf` and `detention_daily_headcount_2025_2026.csv`; neither name labels a distractor | Yes |
| Distractors relevant but unused | weigh, but do not answer a graded quantity | The report is fiscal-2025 only and the headcount is a 06:00 occupancy, so neither reproduces an admission count and the instructions' definitions rule both out | Yes |
| Deliverables | 1 to 3, all in the golden | 3 (xlsx, docx, png), all present in `golden/` | Yes |
| Asks | multi-dimensional, unit and rounding stated | Prompt fixes nearest 100 and whole days. Bed-days (8 cells) and office by tenure (16 cells) are multi-dimensional. Ask 3 had no committed values (FIX_NOW). | Yes after the Ask 3 fix |
| Prompt shape and rubric | identifiable, 25 or more criteria | Design note records 33 criteria | Yes |
| Not LLM-generated, goldens real | no tells | The judge found no provenance leakage in the PDFs or file names and the layouts carry realistic mess. I did not render the golden documents for a realism read. | Yes (golden realism not independently checked) |

## Gate G reconciliation
The judge's mechanism (forecasting), stumping family (analytical_non_defect), surface_read_dependency (no) and sole_data_defect (no) agree with the design note: the stump is the comparison group for the capped terms' end-of-term petitions, the at-maximum rate against the pooled rate. The judge's easy route (pooled rate, 886, 5 pods) is the note's analyst test word for word. No declared distractor carries the task, and the two named distractors are not named by the judge as a surface read. The judge's own measured rates (38.5 and 6.19 per cent) sit close to the note's 38.8 and 6.0. No mismatch.

## Gate H line
`domain: pass`, `layers: pass`, `decisive_step: analytical`. The judge and the design note's Three rules agree: Layer 1 is the two case systems, local against UTC jail clocks, merged person keys and reassigned officers. Layer 2 is a competing-risks style projection of end-of-term petitions. The easy route (886) is filed after cleaning and reading every rule correctly.

## Stump power (Gate F)
Strong on paper. The pooled rate (886, 5 pods), the trailing year (833, 4 pods) and the lost-extension split (1,108, 6 pods) are each reachable by a capable analyst who cleaned the data and read the Act correctly. Only conditioning the end-of-term petition rate on room, then removing the room under the Act, gives 7 pods. The judge reached the at-maximum comparison by its own exploration of the data, so the call was not a textbook method applied without a judgment the data had to settle. The bed-day and office tables are long multi-step reproductions, so partial credit on the asks will be hard to earn. No scored reader ran, per the project rules; the portal measures stump power.

## Findings, ranked
1. **Ask 3 has no committed values (SOLUTION_WRONG).** It lists five parts with no admissions. Already applied on the rebuilt zip 9d45538d7ae0b10a, with the five parts adding to 1,383; the re-judge verifies it.
2. **The nearest-100 figure is not robust to attrition.** An attrition-adjusted build gives about 1,300. 7 pods survives it but only narrowly (about 21 above 1,260). The back-test favours the shipped build. Optionally add the attrition variant to the standing-variants note so the 1,400 claim states its real lower edge.
3. **Section 4 proviso ambiguity** (552 terms, at most about 60 admissions). The coordinator says the rebuilt zip restates the section.
4. **Office reading for Ask 5 is unstated.** Optional: state in the solution that the office is the officer's on 30 September 2026.
5. **"Two more than in 2026" rested only on the unit name `V PODS 1-5` in the headcount file.** Dropped from the final recommendation on the rebuilt zip.

## Next action for the author
Re-judge the rebuilt zip (9d45538d7ae0b10a) once to confirm the Ask 3 parts and the restated section 4. At the same time, decide whether to state the attrition lower edge in the standing-variants note.
