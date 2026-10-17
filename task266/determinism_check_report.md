# determinism-check report, task266, 2026-10-17

## Verdict
NOT_DETERMINISTIC (on the main call: one open fork, SF5, the treatment of the fall 2024 and 2025 classes whose nine terms are not over). The thread rated it DETERMINISTIC and APPROVE; I do not accept that rating, because the contract treats a golden that holds only under an unstated method as an open fork, and the thread's own literal reading licenses three answers.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor (competing-risks cumulative incidence with censoring), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Policy 3.3 says the share covers "those still enrolled included, from the student record as it stands at the end of the spring 2027 term". Policy 3.1 says "within three years ... by the end of the ninth term". Fall 2024 is observed to 8 terms and fall 2025 to 5. No shipped text says how a student whose nine terms have not elapsed enters the share. Literal readings:
- Degrees to date over all entrants (the policy's words read literally): 8 programs (CRJ 26.7 and NUR 27.6 join).
- Dropping unfinished students: 5 programs (MED 31.3 leaves).
- The golden's competing-risks cumulative incidence: 6 programs.
The golden holds only under the third, which no filed sentence selects. The leak reader (Q5 and Q6) independently found the same fork, and the design note's own fork table leaves SF5 as "R0'" without a closing sentence, so `precut.py` should refuse it. Everything else in the main call and all three asks reproduce. The repair is to file the WHAT in the policy (the share by the ninth term for the students still inside their window, the share who would hold the degree by then), never the HOW (do not name Aalen-Johansen or cumulative incidence), per CLAUDE.md "a determinism repair that files the method".

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Entrants (ir_fall_entering_students xlsx, 3 sheets) | 5,292 | 1,691+1,752+1,849 = 5,292, 0 unmapped | yes |
| Exits after 5 DC removed (sis_admissions_exits) | not stated | GR 1,169, TO 843, WD 1,378, open 1,897 | n/a |
| Completion share GEN, BIO, BUS, PSY, MED, ECE | 20.9, 24.9, 22.2, 25.9, 26.2, 19.5 | same | yes |
| Completion share CRJ, HVA, NUR | 32.5, 44.4, 36.7 | same | yes |
| Rejected wrong answers (KM: ECE only; 2023 class only: CRJ 26.8; degrees to date: NUR 27.6, eight programs) | as in the recommendation text | match | yes |
| FTE (census registrations, section schedule Cr Hrs, program_of_record_history, /15) | GEN 1,164.1, BIO 358.0, BUS 531.7, PSY 404.0, MED 386.6, ECE 343.6, CRJ 397.1, HVA 274.5, NUR 538.3 | same, all nine | yes |
| Classes under ten | GEN 1, BIO 14, BUS 5, PSY 5, MED 9, ECE 3, CRJ 3, HVA 13, NUR 78 | same, all nine | yes |

## Competing answers that survived
1. SF5 (main call, blocking): degrees to date over all entrants gives eight programs; dropping unfinished students gives five; the golden gives six. Shipped rule meant to close it: policy 3.3 "those still enrolled included", which on its own text supports the eight-program reading. Open.
2. Credit hours (ask 2): registration credit_hours repeats lab, shop and clinical hours (HVA 388.3, NUR 842.3 if summed). Closed by the schedule's Cr Hrs (0 for LAB, SHP, CLN) and the registrar notes, but the notes' sentence is thin (the pipeline already schedules a clearer sentence).
3. Program of record (ask 2): the registration file's program_code is as of extraction (GEN 1,185.1, PSY 435.0 if used). Policy 4.1 closes it; the notes should say the vintage.
4. Classes meeting together (ask 3): policy 4.2 says "scheduled to meet together" without defining it; the V-room inference is clean (same instructor, days, start). Without merging GEN 3, BUS 8, PSY 6, MED 10.
5. Empty active BIO lab CRN 10417 (ask 3): BIO 14, or 13 if it did not run. Marginal.
Forks 2 to 5 sit on asks only (asks are free of Rule 3) but each moves a graded figure, so each wants a filed sentence.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, pipe-delimited txt) | yes |
| Large file | 25,000 rows or more | registrations 28,135 rows (history 17,857) | yes |
| Distractors in metadata.json | 2 or more, none named in a file name | course_success_rates_fa2021-sp2026.xlsx and service_area_occupational_outlook_2024-2034.csv; the file names do not label them | yes |
| Distractors unused yet weighty | unused by the solution, ruled out by a shipped fact | thread: relevant but unused; neither answers a graded quantity (not independently re-derived by me) | yes (thread-attested) |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx and pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | three asks over nine programs; percentages and FTE to one decimal, counts of classes | yes |
| Prompt shape and 25 or more criteria | identifiable shape | review-list-with-profile shape; criteria count not checkable from the bundle (figures_check 54 of 54 per the build) | yes (build-attested) |
| Reads as real, not LLM generated | clean | registrar and IR exports, fictional college; the leak reader flagged small realism items already in the pipeline's fix list (reason_changed_on, conversion dates, manifest dates and grammar, "1 pages") | pass after that fix list |

## Gate G reconciliation
The thread's line: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The card has stump_class analytical and the stump sentence (Kaplan-Meier censoring the competing exits gives ECE alone; competing-risks incidence gives six). The card's `mechanism` field is empty, so there is nothing to mismatch. The design note's Layer 2 is estimand_identification (competing risks), the same thing under a different label. Matches. The declared distractors (course success rates, occupational outlook) were not named by the thread as the surface read carrying the task, so they are not too load-bearing. No shipped artifact ranks the programs wrongly. Gate G: pass.
Note the mismatch that does exist is not in Gate G but in the note's Not rule application line, which says "no filed rule says how to estimate the share for admissions whose nine terms are not over". That line concedes the fork is open; the stump is the estimator, but the note cannot leave the population or window of the share unfiled.

## Stump power (Gate F)
Good, and analytical. Easy routes each end on a wrong list: degrees to date gives eight programs, Kaplan-Meier with exits censored gives one (ECE), the 2023 class alone gives seven. Nothing shipped ranks candidates. One decisive step carries the main call, so the asks must hold the ladder.

## Findings, ranked
1. NOT_DETERMINISTIC, main call: SF5 unclosed. Literal policy 3.3 gives eight programs. File in the policy the quantity for classes still inside their window (the share who hold the degree by their ninth term), as a WHAT, not the estimator, then assert it in `checks.py` and fill the SF5 row with a closing sentence.
2. Ask 3: a filed definition that sections meeting together means in-person sections with the same instructor, days and start time (policy 4.2), and a sentence on a zero-registration active section.
3. Ask 2: registrar notes should state that Cr Hrs in the schedule governs credit (0 for LAB, SHP, CLN) and that the registration program_code is as of extraction.
4. Policy 3.2: a readmission after withdrawal is not a degree under the entering admission (21 WD admissions later earn a degree; the set is unchanged, but the sentence should say so).
5. Realism: reason_changed_on, one conversion date on every map row, manifest dates and grammar, "1 pages".
Items 2 to 5 match the fix list already recorded in `pipeline.json`.

## Next action for the author
Run `/fix-determinism task266` with the SF5 finding: add to policy 3.3 a filed estimand sentence for the classes whose nine terms are not over (the share who hold the degree by the end of their ninth term, not the share holding it so far), fix findings 2 to 5 in the generator in the same pass, rebuild, and re-judge once.
