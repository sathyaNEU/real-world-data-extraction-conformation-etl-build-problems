# determinism-check report, task269, 2026-10-19 (pass 2)

## Verdict
NOT_DETERMINISTIC (confined to ask 4 of osce2027_station_plan.xlsx; main call and asks 1 to 3 and the chart reproduce). Governing label: underspecified_objective.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The "December allocation" has no filed day. Policy 5.2 uses "the three years before the allocation"; the delivery plan only says the allocation is in December. The training file holds a 24-row refresher session on 19 Dec 2023. An allocation on 1 to 19 December 2026 keeps those attendees; 20 to 31 December drops them. Ask 4 then moves from CSC 28,28,29,30 / SS 33,33,34,34 / CSU 22,24,21,19 to CSC 27,27,28,29 / SS 31,32,32,32 / CSU 21,22,21,18. The golden's 7 December 2023 window start appears in no shipped file. Minor second reading: the register's training columns disagree with the attendance file for about 35 people; policy 5.2 says "completed", so the attendance file governs, but no file says so.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Variance components (cand, cand x domain, domain, station in domain, cand x station, examiner in station, residual) | 0.92, 0.76, 0.22, 0.49, 1.36, 1.06, 1.08 | 0.925, 0.757, 0.221, 0.492, 1.355, 1.059, 1.076 | yes (marks export, station sheet, allocation, minutes item 2) |
| Reliability 12 to 18 | 0.79, 0.81, 0.82, 0.83, 0.84, 0.84, 0.85 | 0.793, 0.806, 0.818, 0.828, 0.836, 0.845, 0.852 | yes |
| Ask 1 stations | 13 | 13 | yes |
| Ask 3 cases / SP | HIS 26/26, EXM 22/15, COM 15/15, PRO 17/5 | same (20 re-created CV records each match one predecessor) | yes |
| Ask 4 sessions | 28,28,29,30 / 33,33,34,34 / 22,24,21,19 | same only for allocation 1 to 19 Dec 2026 | yes under an unfiled date; fork |

## Competing answers that survived
- Ask 4, allocation date: 1 to 19 Dec 2026 gives the golden; 20 to 31 Dec gives CSC 27,27,28,29 / SS 31,32,32,32 / CSU 21,22,21,18. Shipped rule meant to close it: none. This is the fork.
- Ask 4, register versus attendance file: attendance file with outcome Attended taken as governing; unstated, minor.
- Main call, tested and closed: domains fixed (policy 4.2/4.3) gives 13; domains random gives no number within 18 (0.795 at 18); examiner error ignored gives 12. Item 14 kept gives 0.794/0.807 and N/A as 0 gives 0.792/0.805; the call is still 13. Margin at 13 is thin (0.806).

## Spec gates (checked by me against the unzipped bundle and metadata.json)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | pdf, xlsx, csv, docx, txt | yes |
| Large file | 25,000 rows or more | osce2026_marks_export.csv, 35,040 rows | yes |
| Distractors | 2 or more, in metadata, not in file names | 3 (sp_agency_invoices, candidate_feedback_summary, global_grades), listed in metadata.json; names do not label them | yes |
| Distractor behaviour | unused, relevant, ruled out by a shipped fact | judge found them unused; global grades ruled out by policy 3.2 | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 4 asks plus chart; the prompt gives two-decimal reliabilities; the counts are plain integers | yes |
| Rubric 25 or more criteria | 25 | not checked here (no rubric file in scope); the 7 + 8 + 12 + chart figures make it likely | not verified |
| Reads as LLM generated / golden realism | none | judge found no authoring language, hidden sheets or PDF metadata issues | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g method_or_model_selection, stump_class analytical, with analyst_test and domain_test present. These agree. The declared distractors (invoices, feedback, global grades) are not the surface read carrying the task. One finding on the stump description: the design note and card put the analyst's easy route at 16 stations (pooled bank decision study). The judge's own easy routes were 12 (examiner error ignored, about 0.85 at 12) and "none within 18" (domains random, 0.795 at 18). The judge did not reproduce 16. The author should confirm which wrong answer the pooled study actually files and correct the note and the golden's first-paragraph wording ("Not 16 stations") if 16 is not what that method yields. The stump is still analytical, but the golden's rebuttal of 16 is a stated figure that the judge could not recompute.
Gate H: domain pass, layers pass (Layer 1 mess: day-coding changes, bank migration, badge versus staff numbers; Layer 2: fixed-facet G/D-study), decisive_step analytical.

## Stump power (Gate F)
Good. Candidate-by-station reliability or alpha gives 12; domain-random gives no feasible number; only the fixed-domain, single-examiner D-study gives 13.

## Findings, ranked
1. Ask 4: the December allocation date is unpinned, so 12 figures fork on the 19 Dec 2023 session (FIX_NOW).
2. The golden's "Not 16 stations" claim, and the design note's 16 default path, are not reproduced by the judge's pooled-bank variants. Verify and correct.
3. The register-versus-attendance precedence is unstated (minor).
4. The margin at 13 stations is thin (0.806). Every tested variant stays at 13.

## Next action for the author
Pin the allocation date (any day 1 to 19 December 2026, for example 7 December) in final_osce_2027_delivery_plan.docx or in the prompt, add the matching fork-table row and checks.py assertion, rebuild twice, then re-judge once. In the same pass, check the 16-station claim for the pooled study and fix the wording in the submission and design note if it does not reproduce.
