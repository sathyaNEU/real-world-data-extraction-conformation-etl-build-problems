# determinism-check report, task445 (architecture 3), 2026-11-01

target.zip sha256 51f94b0ef73a713b64044e63a6be16bc3d91cf91657b79448210234cf1e4261c. One judge thread (sonnet, medium), scratch /tmp/determinism-check-task445-r1/, verdict at /tmp/determinism-check-task445-r1/verdict.md. Prompt is prompt.txt (not legacy .md).

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (thread's words: no repair needed; optional hardening of the filed wording is a lever, not a defect)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed answer reproduced from the shipped files. Code of practice 4.2/4.3 files the estimand (the marks the paper's candidates would have earned on a question against the others taken together; scaled at 1.5 or more; nearest whole mark) and the awarding minute files the boundaries. Only the 1,422 candidates who wrote all three essays have actual marks on all three questions; there Q6 is +2.09 (SE about 0.12), so +2. Chooser means give about 0.5, the easy route, which files no scaling.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Candidates who sat | 30,697 | 30,697 (every Section A scan, none of 730 ABSENT rows) | yes |
| Moved candidates | booklet keeps earlier number | 160 moved, 333 essay rows remapped, region from later-entry centre, WITHDRAWN dropped | yes |
| Final marks | senior re-mark stands | 62,426 after SENIOR supersedes FIRST | yes |
| Triple-essay candidates | 1,422 | 1,422 | yes |
| Demand Q4 / Q5 / Q6 | below 0 / below 0 / over 1.5, Q6 +2 | -0.69 / -1.40 / +2.09 | yes |
| Grades after +2 (cap 25, best two, Section A, boundaries 66/57/48/39/30) | A 5,732, B 5,934, C 7,337, D 5,945, E 3,561, U 2,188 | identical | yes |
| Grades changed | 1,854 | 1,854 | yes |
| Region sat; Q4, Q5, Q6 | six regions per submission | all six match; Q6 regional sum 10,640 | yes |

## Competing answers that survived
1. Estimator fork (the intended stump, per the thread). Chooser question means: Q6 13.14 against others pooled 13.68, gap 0.53, no scaling. Section A adjusted regression 0.51, no scaling. Within-candidate triple-writer comparison 2.09, scale by 2. The code says "would have earned", and only triple writers have marks on all three questions; chooser and Section A routes inherit topic-knowledge selection. No shipped sentence files the population (candidates observed on all three) and no rule says whose marks measure demand. The thread rates this a mild reading risk, a method choice on honest data rather than a semantic fork. Closure is by the data separating the candidates, not by a filed sentence.
2. Triple writers' Section A mean is lower (22.0 against 24.1). The within-candidate difference removes level, and the 95 per cent band of about 1.85 to 2.33 sits wholly inside the 1.5 to 2.5 rounding cell, so every triple-writer form lands on +2.
3. "Taken together" read as a sum would be unscaled and incoherent; the mean of the other two is the only sensible reading.
4. The raise applies before the best two are credited; Q4 and Q5 are not lowered (4.3).
5. Nearest whole mark and cap 25. The 2025 statistics agree in direction (Q6 lowest facility) but are a named distractor.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 11 files; csv, pdf, xlsx, eml (4) | yes |
| Large file | 25,000+ rows | essay marks CSV 65,941 rows; entries xlsx 31,587 | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | 3 named: teacher_predicted_grades_2026.csv, p2_question_statistics_2025.xlsx, post_results_reviews_2025.csv; none labelled in a file name | yes |
| Distractor behaviour | unused by solution, relevant enough to weigh, ruled out by a shipped fact | 2025 stats point the same direction but are last year's paper, with a reason recorded in metadata; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 3 (docx with chart, csv 30,697 rows, xlsx), all present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | by region x question counts; per-candidate mark and grade; prompt states whole marks and whole counts | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | single-paragraph prompt (558 characters) with the call, three deliverables and many cells; the rubric is generated downstream and I did not count it, so the 25-criteria gate is unverified here | unverified |
| Reads as real, not LLM | none | the thread found the code, minute and email read as real artifacts; no authoring leakage | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical; analyst_test names chooser means, Section A adjustment and each candidate's own pair as the easy route and the all-three writers as the way out. Design note (Three rules, Not rule application) names the same family: 0.53, 0.51, 0.50, 0.52 against 2.09 (forms 1.85 to 2.33). Match. The declared distractors (2025 statistics, 2025 reviews, teacher predictions) were not named by the thread as the surface read carrying the task, so the distractors are not too load-bearing. No Gate G finding.

## Gate H line (thread)
domain: pass, layers: pass, decisive_step: analytical. Layer 1: re-marks, moved candidates, merged-centre codes, absent scripts. Layer 2: selection-corrected estimate of demand. Design note and card agree (domain_test is the examinee-choice problem of test equating; decisive step is recognising that choosers knew the topic and reading demand from the all-three writers). No mismatch.

## Stump power (Gate F)
Adequate. The surface read (chooser means or the 2025 per-question statistics) says about half a mark and files no scaling, which gets the call and every grade count wrong. The ETL layer adds ask-level difficulty without deciding the call. The thread did not class the decisive step analytical because the field's standard method is the golden; it reached +2 only after separating the candidates by selection, so no landable-call caveat applies. A strong solver who tests for selection will still find the triple-writer route, which is the main-thread weighing for the ladder.

## Findings, ranked
1. Low: the population (candidates observed on all three questions) is not filed, and no rule says whose marks measure demand. This is CLAUDE.md's "population filed, method open only where the data separate the candidates" tension. The thread accepts it as a method choice. Filing the population in the code's 4.2 wording, without the method, would remove the residual fork. Optional.
2. Info: the rubric criteria count was not checked here.
3. Info: all graded figures reproduced; no hygiene finding.

## Next action for the author
No repair required. If you want the literal reading tightened, add the population (candidates observed on all three questions) to the code's 4.2 wording without naming the method, then rebuild twice and re-run the gates.
