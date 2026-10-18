# determinism-check report, task266, 2026-10-18 (pass 4, stage 4 of the reship, run p4)

## Verdict
NOT_DETERMINISTIC (thread's words: the main call, six programs into review, is robust; the failure is on the graded supplementary figures, asks 1 and 2)
**Disposition:** SEND_BACK. The thread: pin the estimator convention and the credit-hour source in the prompt or the files (changes what solvers see), so a rerun is required.
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The set of programs below 30 per cent is the same under every licensed cumulative-incidence convention the thread tried (GS, Bio, Bus, Psy, MA, ECE in; CJ, HVAC, Nursing out). The thread found the committed one-decimal figures not uniquely forced: (1) the completion shares depend on an unpinned risk-set convention for leavers; (2) the FTE column depends on which of two disagreeing shipped credit-hour fields is "credit hours registered". Gates C/E fail on supplementary asks 1 and 2; taxonomy label underspecified_objective.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cohort 1,691 + 1,752 + 1,849 = 5,292; 5 DC removed | as filed | same | yes |
| Completion share GS / Bio / Bus / Psy / MA / ECE / CJ / HVAC / Nurs | 20.9 / 24.9 / 22.2 / 25.9 / 26.2 / 19.5 / 32.5 / 44.4 / 36.7 | 20.92 / 24.88 / 22.23 / 25.87 / 26.23 / 19.47 / 32.52 / 44.43 / 36.72 (ties all at risk in the exit term) | yes (per-class variant gives the same) |
| FTE, same order | 1,148.8 / 352.5 / 525.2 / 399.4 / 381.5 / 341.0 / 391.2 / 272.3 / 533.1 | 1148.8 / 352.5 / 525.2 / 399.4 / 381.5 / 341.0 / 391.2 / 272.3 / 533.1 (schedule Cr Hrs) | yes |
| Classes under ten, same order | 2 / 15 / 7 / 7 / 10 / 5 / 8 / 21 / 79 | 2 / 15 / 7 / 7 / 10 / 5 / 8 / 21 / 79 | yes (online TBA merging changes nothing; no rows on the census date) |
| GR exits with a conferral in the exit term | 1,169 | 1,169 of 1,169 | yes |

## Competing answers that survived
The thread's table:
| Fork | Answers | Thread's rating |
|---|---|---|
| 1. Leavers (TO/WD) in the risk set of their exit term (golden) vs not at risk in the exit term | Golden 20.9 / 24.9 / 22.2 / 25.9 / 26.2 / 19.5 / 32.5 / 44.4 / 36.7. Alternative 24.3 / 29.0 / 25.4 / 29.1 / 28.9 / 19.9 / 35.2 / 46.9 / 39.1. Same six in review; Bio and Psy sit 0.9 and 1.0 under the line | open (see adjudication, which finds it does not reproduce) |
| 2. Credit hours: registration credit_hours (course's) vs schedule Cr Hrs (section's) | Schedule (golden) GS 1148.8, Nurs 533.1, HVAC 272.3. Registration as filed 1320.9, 847.7, 396.5. Registration lecture rows only 1204.9, 546.7, 283.1. 6,690 of 26,085 in-place rows disagree | open |
| 3. Program of record at census: history file (golden) vs registration program_code (887 of 26,085 rows differ) | history favoured by "at the census" and effective/end terms | adequately closed |

Estimand forks closed by policy 3.1 to 3.3: Kaplan-Meier with leavers censored (only ECE in review); naive observed share (7 programs, CJ 27.9). Margins: CJ 2.5 over the line, Bio and Psy 4 to 5 under it.

## Main thread's adjudication (after the verdict, verdict unchanged)
1. Fork 1 (leavers in the risk set of their exit term) does not reproduce. With every transfer out and withdrawal taken out of the risk set before its exit term's awards, or dated one term earlier, the discrete Aalen-Johansen estimate equals the golden share to the last digit for all nine programs. checks.py now asserts this (R2/SF7, nine assertions). The thread's alternative figures (GS 24.3, Bio 29.0) come from no estimator that keeps the leavers as a competing ending, so the one-decimal shares are not open on this point.
2. Fork 2 (Ask A's credit-hour source) is the ask's built device. Pass 3 ruled it closed by the registrar's definitions: credit_hours is the course's credit hours, Cr Hrs is the section's, and policy 4.1 counts credit hours registered. The device stays as built. That pass 4 disagrees is reported to the author as an open risk on Ask A, with filing the source as the option, at the cost of Ask A's device.
3. Fork 3 is closed, as the thread itself rated it.
4. Ask B, the only ask the change since pass 3 touched, reproduced at 2, 15, 7, 7, 10, 5, 8, 21 and 79 under the overlapping-weeks merge.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 14 files; PDF, XLSX, CSV, TXT; registrations csv 28,117 rows | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | course_success_rates and service_area_occupational_outlook, named in metadata.json; thread found them unused; file names do not label them (I did not re-test that they reproduce a graded quantity) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf) | yes |
| Asks | multi-dimensional, unit and rounding stated | 3 asks x 9 programs, one decimal for percentages and FTE, counts whole | yes |
| Prompt shape, rubric 25+ | identifiable, 25+ criteria | per-program grid, 27 gradable figures plus call and chart; rubric not generated by me | yes (basis: figure count) |
| Reads as real, not LLM generated | | thread found no authoring language in PDFs or manifest; goldens not readable by the thread, so chart and workbook layout unchecked by it | yes, with that caveat |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note files strategy key `decomposition_attribution` (decisive generator G17, the event-history estimator); the same stump under the design's label. The thread did not name either declared distractor as carrying the task. Easy routes match the design's anticipated wrong answers (naive 7, KM 1). No mismatch.
Gate G: PASS.
Gate H: domain pass, layers pass, decisive_step analytical (cumulative incidence with TO/WD competing, open admissions censored); matches the card and the note's `## Three rules`.

## Stump power (Gate F)
Good, per the thread. Naive observed share gives 7 programs, Kaplan-Meier with leavers censored gives 1, only the competing-risk censoring-aware estimate gives 6. No hardening needed.

## Findings, ranked
1. Thread finding, fork 2 (Ask A credit-hour source): open under the thread, and the main thread keeps the device as built; this is an open risk for the author to decide on (file the source, losing Ask A's device).
2. Thread finding, fork 1 (leaver risk-set convention): the main thread's adjudication finds it does not reproduce under any estimator that keeps leavers as a competing ending; verdict as given stays NOT_DETERMINISTIC.
3. Margins: CJ 2.5 over the floor; call robust.
4. Change since pass 3 (section schedule dates, step 7 wording): Ask B reproduced.

## Next action for the author
Decide on fork 2: either accept the open risk on Ask A and ship as built, or file the credit-hour source (section Cr Hrs from the schedule) in the prompt or files and rebuild, then re-run the check. Fork 1 needs no change (checks.py R2/SF7 asserts it).
