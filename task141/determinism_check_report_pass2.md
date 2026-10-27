# determinism-check report, task141, 2026-10-27 (pass 2, architecture 4, target.zip sha256 4066ee80afa5fdfa)

## Verdict
DETERMINISTIC (no SOLUTION_WRONG on the load-bearing blocks; the projection figure and three ask groups were not reproduced to the figure, see ledger)
**Disposition:** APPROVE (thread's disposition; this report adds a pre-ship hygiene list, and a re-judge is already planned on the hardened rebuild)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The Act (sections 4 and 5) removes all extension room from the 3,003 terms ending on 31 March 2027 and from every term reaching 24 months. The record's terms at their class maximum petition at about 39 per cent in the last 120 days, against about 6 per cent for terms with room. The at-max share is 37 to 42 per cent in every class and 39 per cent with or without a prior extension, so the comparison group is forced by the data. Instructions 4.1 ("acting as the county's records show them acting") licenses applying that rate. Pooled rate gives 886 (5 pods), trailing year 833 (4 pods). The pod standard (one pod per 220 admissions or part of 220) is stated in the annex; 1,383 and 1,400 both give 7 pods.
One pass, one thread, one verdict. Isolated thread at /tmp/determinism-check-task141-r1/ (verdict.md there).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Open felony terms at extract | 7,598 | 7,598 | yes (cms2 OPEN, FELONY) |
| Terms ending 31 Mar 2027 | 3,003 | 3,003 | yes |
| Terms reaching 24 months | 2,465 | 2,457 | within 8 (end-date convention) |
| Trailing-year revoked felony petitions | 833 | 833 | yes |
| Ask 5, 16 cells (officer's office on 30 Sep 2026, completed years) | as filed | identical | yes, exact |
| At-max window share | 3,669 of 9,467 (38.8%) | about 3,700 of 9,700 (38%; 36 to 39% across eligibility variants) | within about 3 points |
| With-room window share | 1,131 of 18,781 (6.0%) | about 1,240 of 19,600 (6.3%) | within about 3 points |
| Ask 4 felony bed-days by quarter | 24,970 / 24,266 / 23,100 / 24,762 | 25,004 / 24,290 / 23,125 / 24,844 | no, within 0.3% |
| Ask 4 misdemeanor bed-days | 2,219 / 2,281 / 2,062 / 2,475 | 2,168 / 2,234 / 2,050 / 2,464 | no, within 2.3% |
| Projection | 1,383 | crude build: 573 to 588 (3,003 terms) plus 216 (other capped); no-room component 790 to 804 against golden 863 | not reproduced to the figure |
| Ask 3 components (34 / 206 / 968 (863) / 175) | as filed | not rebuilt | no |

## Competing answers that survived
None on the call. 886 (5), 1,108 (6), 1,728 (8) and 833 (4) are each ruled out by the record's observed at-max rate. Residual points, both being hardened by the author before the re-judge: (1) the Act's "24 months" read as calendar months (the 2,465 vs 2,457 gap sits here); (2) the county's pod standard wording. Neither moves the pod count in the thread's reading.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 3 (10 CSV, 3 PDF, 1 XLSX) | yes |
| Large file | 25,000 or more rows | crosswalk 50,323; bookings 45,550; cms1 30,028 | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | apd_annual_report_2025.pdf, detention_daily_headcount_2025_2026.csv; neither name labels one | yes |
| Distractor quality | unused by solution, weighs, ruled out by a shipped fact | annual report counts fiscal 2025 on another basis, headcount counts at 06:00; instructions define admission; thread did not use either as the surface read | yes |
| Deliverables | 1 to 3, all in golden, no format family | 3 (xlsx, docx, png), all present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 24 graded ask figures plus the build components; prompt states nearest 100 and whole days; counts are integers | yes |
| Shape and rubric | shape identifiable, 25 or more criteria | shape 02 (forecast across periods); design note counts 33 | yes (author's count, not regenerated) |
| Reads as real | no LLM tells, goldens real | thread found no authoring or benchmark language; realism of goldens not re-read here (golden-realism owns it) | yes, with that limit |

## Gate G reconciliation
Thread: forecasting, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: `estimand_identification`, stump_class analytical, decoy none. Match. The thread did not name the declared distractors (annual report, headcount) as the surface read, so they are not too load-bearing. No banned_stumping_type.
Gate H: thread domain pass, layers pass, decisive_step analytical. Note's `## Three rules` says domain pass (revocation forecast from hazards and end-of-term behaviour), Layer 2 comparison group for capped terms, analytical via the 886 vs 1,383 analyst test. Match; no mismatch finding.

## Stump power (Gate F)
Thread: the pooled end-of-term rate (886, 5 pods) and the trailing year (833, 4 pods) are the natural easy routes; the split of at-max against with-room is not announced and the projection is long, so failure is moderate to good. Not a case of a standard method reached with no judgment: the thread found the split only after testing candidate groups against the record. Main thread should weigh the portal measure; the margin is the soft point (below).

## Findings, ranked
1. Margin: 1,383 is 63 admissions (4.8%) above the 1,320 line. The thread's cruder build omitted the "second end at the cap" terms and landed well under the golden, near 1,300 to 1,340 at the 6-pod line. Judged a modelling omission, not a second valid estimate, but a solver who lands there files 6 pods with the correct comparison group. Residual determinism and stump-power risk on the call.
2. The projection (1,383), ask 3 components and ask 4 bed-days were not reproduced exactly by the thread (bed-days within 0.3% felony, 2.3% misdemeanor; weekend-commitment bounding and booking chaining are likely sources). Asks 3 and 4 are exact-figure grades, so the instructions must close those conventions; verify in the rebuild that they do.
3. Window counts and the 2,465 depend on window-eligibility and end-date conventions. Optional: state them in the write-up so a close recomputation is not read as a miss.
4. Hardening in progress on calendar-month reading of 24 months and the pod standard; re-judge follows on the rebuilt zip.
5. Narrative "two more than in 2026" rests on 5 violator pods in the headcount file; not graded.

## Next action for the author
Finish the two hardenings, then add to the instructions (or the generator's closure table) the weekend-commitment and booking-chaining conventions behind ask 4 and the window-eligibility convention behind the 2,465, rebuild, and have the re-judge confirm the 6-pod line is not reached by a plausible solver variant that keeps the at-max split.
