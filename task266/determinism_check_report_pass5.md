# determinism-check report, task266, 2026-11-01 (pass 5)

## Verdict
NOT_DETERMINISTIC (ask 2 only; main call, ask 1 and ask 3 reproduce)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
Bundle: target.zip md5 79d75971c082b313965780bdc952cbc5 (reship after the leak-gate repair; extract notes and manifest no longer shipped). The judge thread ran from /tmp/determinism-check-task266-162553/ (verdict.md there). Legacy prompt.md not in use.

## Why
Policy 4.1 says only "the credit hours registered at the census". fall2026_census_registrations.csv carries its own course_credit_hours column and fall2026_section_schedule.xlsx a different Cr Hrs column; no shipped file names a tie-breaker now that the registrar's notes are gone. The registration column repeats course credits on lab/clinical/shop rows (BIO 101 LAB 4 vs 0 in the schedule; NUR 201 CLN 7 vs 0) and carries 4 for ENG 101 and MAT 110 where the schedule has 3. Read literally on the registration column: GS 1,320.9 / BIOL 473.3 / BUSA 570.2 / PSYC 429.5 / MEDA 498.3 / ECED 361.5 / CRJU 422.5 / HVAC 396.5 / NURS 847.7, against the golden 1,148.8 / 352.5 / 525.2 / 399.4 / 381.5 / 341.0 / 391.2 / 272.3 / 533.1. Taxonomy: competing_defensible_answer. Ask 3 reproduces but its merge convention now rests on inference only (see forks).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 3-yr completion, 9 programs (Aalen-Johansen, TO/WD competing, open censored) | 20.9 24.9 22.2 25.9 26.2 19.5 32.5 44.4 36.7 | 20.92 24.88 22.23 25.87 26.23 19.47 32.52 44.43 36.72 | yes (ir_fall_entering_students, sis_admissions_exits, conversion map, register, term calendar) |
| Programs below 30, count | 6 | 6 | yes |
| Entrants | 5,292 (5 DC removed) | 1,691+1,752+1,849 | yes |
| FTE, 9 programs (schedule Cr Hrs, program of record, RE/RW <= 8 Sep 2026 plus WC, /15) | 1,148.8 ... 533.1 | identical under the golden choices | yes, only under the schedule-Cr-Hrs choice |
| FTE, registration course_credit_hours | n/a | 1,320.9 ... 847.7 | alternative survives |
| Classes under ten, 9 programs | 2 15 7 7 10 5 8 21 79 | 2 15 7 7 10 5 8 21 79 | yes (with merge of overlapping-week same instructor/days/time pairs) |

## Competing answers that survived
1. Ask 2 credit-hour source: schedule Cr Hrs (golden) vs registration course_credit_hours (every program moves, e.g. NURS 533.1 vs 847.7). Policy 4.1 and the shipped files do not close it. Fix needed.
2. Ask 2 variants the files do close: registration program_code (949 rows differ) closed by "program of record at the census" plus the history file; dropping WC closed by 4.3; registration column on LEC rows only (GS 1,204.9, NURS 546.7) is a further unstated variant of fork 1.
3. Ask 3 merge convention: no merging gives 4 16 10 8 11 7 9 22 80, against golden 2 15 7 7 10 5 8 21 79. Policy 4.2 closes it only through "meet together"; the sole evidence the HOL/TRV pairs meet together is same instructor, days, time and a V room suffix. Weakened by the dropped notes; the thread judged the golden reading the forced one but live. Merging disjoint-week pairs is excluded by the policy wording; schedule Enrl in place of census counts is closed by 4.3.
Main call: closed. Alternatives (KM with leavers censored: one program, ECED; fall 2023 class alone: seven; degrees to date: eight) are each closed by policy 3.2 and 3.3. CRJU is nearest the floor (31.5 to 32.5 across estimator variants), call stable.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | >= 10 | 12 | yes |
| Formats | >= 3 | 4 (xlsx 5, csv 5, txt, pdf) | yes |
| Large file | >= 25,000 rows | fall2026_census_registrations.csv 28,117 | yes |
| Distractors | >= 2 named in metadata.json, none labelled by file name | course_success_rates, service_area_occupational_outlook named; conferrals file is a further live decoy for readmit degrees (unnamed, an extra) | yes |
| Distractors unused yet weighable, ruled out by a shipped fact | yes | none answers a graded quantity as shipped; conferrals counts readmit degrees, ruled out by policy 3.2 | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | 3 asks, 9 rows each, prompt states one decimal | yes |
| Prompt shape; rubric >= 25 criteria | identifiable, 25+ | shape 10 scorecard; rubric is generated, not checkable here (9 shares, 9 FTE, 9 counts, call, set gives well over 25) | yes (by construction) |
| Reads as real, not LLM generated | yes | document properties are registrar/IR/academic-affairs; no tool banners, hidden sheets or comments | yes |
Hygiene: PASS. Cross-batch clone check not run by the thread.

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (round 2 and 3 judges, Gate G line): statistical_rigor and analytical_non_defect. Match. No declared distractor carries the call; the two named distractors are not the surface read. Gate H: thread domain pass, layers pass, decisive_step analytical (cumulative incidence with TO/WD competing against 1 minus Kaplan-Meier with leavers censored); note and card (`stump_class: analytical`, analyst_test, domain_test) agree: Layer 1 is conversion IDs, codes, readmits, program changes; Layer 2 the competing-risk estimand. Mismatch: none. The thread's stump power read is moderate to high; the decisive step is a method choice the data separate (one program vs six), not a landable textbook route reached without judgment. The asks' devices currently add chance forks rather than difficulty.

## Stump power (Gate F)
Moderate to high on the main call: a strong analyst who cleans correctly and files standard KM answers one program, the to-date count eight, the 2023 class alone seven. Asks 2 and 3 carry independent hazards (credit source, census status, merge) that, until pinned, are forks rather than analysis.

## Findings, ranked
1. Ask 2 credit-hour source is open (NOT_DETERMINISTIC). The leak repair removed the only text that stated which credit column is summed; policy 4.1 does not. Pin by a WHAT sentence in policy 4.1 (credit hours are the section's hours in the term schedule; lab, shop and clinical sections carry none) or restore a one-line definition of the registration column. File the unit, not a method for the call; the main call is untouched.
2. Ask 3 merge convention rests on inference (same instructor, days, time, V room); the no-merge reading gives different counts in all nine programs. Pin in the schedule or policy 4.2 that sections with the same instructor, days and start time and overlapping dates meet together and count as one class. Do so without naming the leak-gate-banned notes file: put it in the policy text or a schedule column, not a how-to-read sheet.
3. Re-grade asks 2 and 3 after the pin; main call and ask 1 stay byte-identical, no rerun for them. The leak check should re-run on the pin text since the repair came from a leak gate.
4. Advisory: undefined codes (history change_reason ADM/CHG/SEC/RDM, schedule Link) are not needed for any graded figure; no action.

## Next action for the author
Add one sentence to policy 4.1 stating that the credit hours summed are the section's Cr Hrs in the term schedule (laboratory, shop and clinical sections carry none), add the meeting-together convention to 4.2, rebuild twice byte-identical, assert ask 2 and 3 figures in checks.py, and re-judge once.
