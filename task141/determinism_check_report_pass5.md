# determinism-check report, task141, 2026-10-27 (pass 5, run r5)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one caution on Ask 3, no fix required)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Target.zip sha256 2cea32997e4cbfa8. The judge thread was spawned by the main session from my brief; the verdict is /tmp/determinism-check-task141-r5/verdict.md.

## Why
The shipped files force 7 pods. Instructions 4.1 requires the projection to follow the law in force and the courts' behaviour as the records show. Terms at their class maximum in the last 120 days drew a petition about 38 per cent of the time, in every felony class including DF4, against 6 per cent for terms with room. Section 5 of the Act leaves no capped term any room, so the at-maximum rate applies to the 3,114 terms ending 31 March 2027 and to terms reaching 24 months. The pooled rate (911, 5 pods) and the trailing year (827, 4 pods) are the easy routes and file the wrong count. The prompt now asks no admissions figure, which removes the nearest-100 fragility that failed pass 4. The 1,260 to 1,470 band is a filed pod-cover boundary, and the writeup states the projection as the band.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Open felony terms | 7,841 | 7,841 (cms2) | yes |
| Terms ending 31 Mar 2027 | 3,114 | 3,114 | yes |
| Trailing-year admissions | 827 | 827 | yes |
| At-maximum petition share | about 2 in 5 | 38.3% (3,782/9,881); every class 35.8 to 40.6% | yes |
| With-room petition share | 6% | 6.3% (1,265/20,149) | yes |
| Ask 4, 16 cells | listed | all 16 exact | yes |
| Ask 3 felony bed-days | 24,603 / 25,141 / 23,135 / 23,897 | 24,565 / 25,125 / 23,184 / 23,897 (best variant) | Q3 only |
| Ask 3 misdemeanor bed-days | 2,272 / 2,228 / 2,043 / 2,475 | 2,167 / 2,190 / 2,008 / 2,383 | no |
| 2027 projection | 1,424 (1,414 to 1,443) | rough build about 1,300 to 1,450 | band only; 1,424 not pinned |
| Pod count | 7 | consistent with every recompute | yes |

## Competing answers that survived
- Ask 3 (not the call): the thread tried the chain gap, order look-back, day cap and FIFO budget conventions and moved figures by 0.5 to 4 per cent in either direction, so it could not identify the rule that gives the golden digits. The author's evidence closes this:
  - verify.py, a separate pandas implementation reading only shipped files, reproduces all eight figures exactly.
  - Pass 3's isolated thread reproduced all eight exactly on the previous pack under the same 5.2 and 5.3.
  - Only 2 of 8,311 commitments run past their days ordered plus one, and both fall before the Ask A window.
  - The in-window stays holding a second order are felony commitments with a shorter misdemeanor commitment inside, so they are felony every night under 5.3.
  - The thread's misdemeanor shortfall in every quarter matches leaving out weekend-sentence stays, which 5.2 counts at each midnight.
  - Step 6 of the writeup now says so in words.
  I weigh this as a caution and not a fork. The thread's omission of weekend-sentence stays is a reading the filed 5.2 text excludes, and two independent reproductions exist. A reader who misses the weekend stays still lands the call.
- Ask 4 "supervising office" could be read as intake_office (differs for 1,655 terms). Closed by instructions 6.1 ("office supervising them at the extract") and by the renamed column, so intake_office reads as intake.
- No fork survives on the main call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 3 (CSV, PDF, XLSX) | yes |
| Large file | 25,000 or more rows | bookings 46,347; cms1 30,568 | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | apd_annual_report_2025.pdf, detention_daily_headcount_2025_2026.csv; names are neutral | yes |
| Distractors unused, relevant | weighable, ruled out by a shipped fact | the annual report counts fiscal 2025 only; the headcount is a 06:00 count against the midnight rule of 5.2 | yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, docx, png), all present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 24 figures; "whole days" in the prompt | yes |
| Prompt shape and rubric | 25 or more | design note counts 32; not independently regenerated | yes, per note |
| Reads as real, not LLM | no tool banners; goldens real | thread found none in PDF/XLSX metadata or CSVs; I did not re-audit goldens | yes |

The distractor list in metadata.json names two files. The thread named the crosswalk and the PV-OOS and PROB-COND bookings as additional distractors, which is a harmless superset.

## Gate G reconciliation
The thread's mechanism (forecasting under a regime change), family (analytical_non_defect), surface_read_dependency no and sole_data_defect no match the design note's Layer 2: family estimand_identification, with the comparison group for the capped terms' end-of-term petitions as the decisive choice. The thread's wording differs from the note's, but the content is the same. The thread did not name the declared distractors (annual report, headcount) as the surface read carrying the task, so they are not too load-bearing. The note's at-max share is 38.7 per cent against the thread's 38.3 per cent, and the note's 36 to 42 per cent class range matches the thread's 35.8 to 40.6; the difference is a definitional nuance and does not matter.

Gate H: the thread gave domain pass, layers pass, decisive_step analytical, matching the note's `## Three rules` (No decoy, Not semantics, Not rule application). Its easy route (911, 5 pods) is the same as the analyst test. The thread reached the golden call by applying the at-maximum comparison itself, with the data separating the analog (DF4 and the other at-max windows), so the analytical class is not just the standard method.

## Stump power (Gate F)
Strong per the thread: 827 gives 4 pods, the pooled 911 gives 5, and a capable analyst who cleans and reads the Act correctly still files 4 to 6 pods unless they split windows by class maximum. The split is one comparison, available in the data via the DF4 24-month class, and a strong solver can reach it. The note's own pair ceiling is 30.8. The main thread should weigh landability by the portal alone, since no solver result is available. Not a method textbook route; no discount applies beyond that.

## Findings, ranked
1. Caution (Ask 3, supplementary): the thread's bed-day rebuild missed the golden by 0.2 per cent for felony and 3 to 4 per cent for misdemeanor. Resolved by the author's verifier and pass 3 evidence plus the clarified step 6. No fix.
2. Caution (margin): the upper band edge 1,470 is 27 above the highest listed variant (1,443) and the golden sits 46 below it. The lower edge is 164 below the golden. Thin but clean; all variants share one method and none crosses an edge. The extreme-combination range 1,413 to 1,463 in the design note stays inside the band.
3. The thread did not rebuild 1,424 exactly (rough 1,300 to 1,450), so the projection's exact value is supported by the author's verifier and not by the judge; the pod count is supported by every recompute.
4. Ask 4 office reading is closed by 6.1; it remains the most likely place for a reader to diverge, but it is a graded ask and not the call.

## Next action for the author
Ship. Optionally re-run only the free gates once if the step 6 wording edit touches submission.md (figures unchanged); no regenerate of the bundle or prompt is needed.
