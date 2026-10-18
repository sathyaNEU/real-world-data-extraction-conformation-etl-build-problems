# determinism-check report, task244, 2026-10-18

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: etl_conformance (closer to statistical_rigor), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Pass history (this file is the one report for the build; pass 3 is the final pass on the shipped design):
- Pass 1, /tmp/determinism-check-task244-r1/verdict.md: DETERMINISTIC, APPROVE.
- Pass 2, /tmp/determinism-check-task244-r2/verdict.md: NOT_DETERMINISTIC, FIX_NOW on ask 2 (the match rate's linking of split households was unfiled). Closed by filing the link in methodology note section 8.2 with a new silent primary.
- Pass 3, /tmp/determinism-check-task244-r3/verdict.md (this report): DETERMINISTIC, APPROVE, fix none.
- After pass 3 the bundle was rebuilt once more for log-only realism (each supervisor's tablet takes the app update at its own Friday sync between 18 June and 9 July 2027; visit clock times smoothed). The author reports no graded figure moved, the generator's 186 checks and the verifier's 258 pass, and the advisory is now in solution step 2. The judge did not see this rebuild; that is the author's statement, not something this pass re-ran.

## Why
The call (No, 13 of 24 rates carry the warning) follows from methodology note 8.1 (joint true holding in both quarters, one-third line), protocol sections 4 and 7 (reconciled status, state-wide, unweighted, each person once) and note section 3 (a different interviewer each visit, so the two quarters' errors are independent). Inverting the state-wide misclassification matrix out of Table F1 reproduces all 24 shares and the 13 warned rates. The nearest rates to the line are 23.2 and 45.1 against 33.3, and every rate keeps its side in 500 bootstrap resamples of the reinterview. Asks 2 and 3 also reproduce from the bundle.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Persons reinterviewed in window | 15,221 | 15,221, unique, inside 14 days by visit_start | yes |
| Correct-record rates E/U/O | 98.82 / 83.96 / 97.73 | same | yes |
| U recorded E / O; E recorded U; O recorded U | 5.87 / 10.17; 0.44; 1.40 | same | yes |
| F1 on post-1-April districts | D04 EAs 3,7,9,12,14,15 in D02 | row totals match | yes |
| 24 shares, 11.9 to 69.0 (e.g. Lagoon Coast loss 45.1, Cocoa Belt East loss 69.0, Creeks loss 23.2, Fringe finding 11.9) | per golden | 45.07, 68.98, 23.20, 11.87 | yes |
| 13 warned rates (share of 1/3 or more) | named set | same 13 | yes |
| Match rate and persons, 12 districts | e.g. Core 92.0 / 11,266 | 10,364 of 11,266 = 92.0; University Towns 9,816 of 10,777 = 91.1 | yes, exact |
| Mean days to reinterview, 12 districts | 7.3 ... 6.1 | 7.26, 6.32, 6.92, 6.59, 7.13, 6.88, 6.77, 6.72, 6.60, 6.07, 6.69, 6.09 | yes |

## Competing answers that survived
None that change the call or a graded figure.
- PPV product or per-status discordance: 0 of 24 warned (wrong easy route; note 8.1 files the joint pair, so inversion is the literal reading).
- reint_status in place of reconciled: 14 warned; closed by protocol section 4 and note 8.1.
- Dropping 2026Q4 reinterviews, or error in one quarter only: still 13.
- Rounding matrix cells to 2 to 3 decimals: decisions hold, but Lagoon Coast job-loss moves 45.1 to 44.9 or 42.6. Advisory only; the author reports "carried unrounded" now in step 2.
- attempt_date in place of visit_start for ask 3: about 9.3 days for Metropolitan Core instead of 7.3. Closed by note 8.3 (visit date) and the data dictionary; Layer 1 on ask 3 only. Note that the post-judge rebuild changed the Friday-sync dates in the log, so this reading was not re-run on the final log.
- Fractional days instead of calendar dates: closed by "date" in note 8.3.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, eml, md) | yes |
| Large file | 25,000 rows or more | 45,409 rows (2027Q2 persons; five quarterly files near 44,000) | yes |
| Distractors | 2 or more, named in metadata.json, none labelled by file name | 3 (projections csv, job centre registers xlsx, Q3 bulletin pdf); file names do not label them | yes |
| Distractors unused yet weighty, none answers a graded quantity | required | rank nothing on classification error per judge and design note | yes |
| Deliverables | 1 to 3, all in golden, no format family | 2 (xlsx, docx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 24-row share table, 12-district match rate and persons, 12-district days; prompt states per cent to one decimal, whole persons, days to one decimal | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 07 (grid of cells); design note estimates well over 25; prompt.txt 736 characters, one paragraph | yes (rubric count taken from the design note, not generated here) |
| Reads as real | no LLM feel, goldens realistic | judge found no authoring leakage; goldens not separately judged | yes |

## Gate G reconciliation
Judge: mechanism etl_conformance, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical; analyst_test is the PPV product (18.1 per cent) or one less the correct-reading product (17.0), warning no rate; the judge's easy route is the same and it reproduced 0 of 24 warned. The design note's declared easy path matches. Gate G: no shipped artifact ranks the candidates wrongly; Table F1 and F2 are correct as tabulated. The declared distractors were not named by the judge as the surface read carrying the task. Match. One tension to note: the design note says no filed rule says how to estimate the share, while the judge calls inversion the literal reading of the joint pair in 8.1. Both end on 13 warned and the PPV route is not a literal reading of 8.1, so this is not a fork.

Gate H: judge `domain: pass`, `layers: pass`, `decisive_step: analytical`. Design note and card: domain test (gross-flows adjustment by inverting the reconciled misclassification matrix at both ends), Layer 1 (EA renumbering, duplicate batches, household renumbering, tablet sync dates) and Layer 2 (estimand identification) agree. No mismatch.

## Stump power (Gate F)
Good per the judge. The surface route files "release without warning" at 18.1 per cent for every rate; a solver who cleans everything and applies the filed rules still reaches the wrong call unless the classification error is taken out of the flows at both quarters. Layer 1 mess costs only asks 2 and 3. Measured stump power is the portal's to give.

## Findings, ranked
1. Advisory: the one-decimal shares need the reinterview matrix carried unrounded (Lagoon Coast job-loss moves to 44.9 or 42.6 at coarse rounding). Reported as now in solution step 2.
2. Process: the log-only realism rebuild after the judge ran was not re-judged. The author reports no graded figure moved and all checks pass; ask 3 depends on the log's visit_start and call dates, so a reader who wants certainty can re-run that one ask against the final target.zip.
3. No send-back-level finding.

## Next action for the author
Ship task244 as built (APPROVE); no second judge thread is licensed.
