# determinism-check report (pass 3, /build stage 4 re-judge, run r3), task268, 2026-10-19

## Verdict
NOT_DETERMINISTIC (SOLUTION_WRONG does not apply; ask 2 is not forced by the shipped text)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor (informative censoring, IPCW), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread kept the order (derivation.md written before graded_blocks.md opened in full).

## Why
Ask 2 (NT-proBNP tests and counts at or above 400) holds only under an unfiled rule. ntprobnp_results_2025.csv has 206 pairs with the same mrn, lab and collection time, a different accession, a different result and a later release. Both rows are status F, with no correction flag and no lab note, and no shipped document mentions re-release. Read literally ("tests its laboratory reported"), both rows are tests: Fennick 10,461 / 6,860 against the golden 10,421 / 6,832 (keep latest). Keep-first gives 10,421 / 6,834, and 61 of the 206 pairs cross 400, so the counts depend on an undeclared supersession rule. Label: underspecified_objective on supplementary ask 2. The main call, the survival figures and asks 1 and 3 reproduce under the golden method. The survival estimator is data-forced, not text-forced: the filed estimand is defined (charter 3.1/3.2, patients no longer followed included), the rest is residual risk.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cohort 2022-23 | 9,339 | 9,339 (patients.csv) | yes |
| Gullhaven patients / moved beyond linkage | 2,996 / 612 | 2,996 / 612 | yes |
| Gullhaven NYHA III/IV at move visit | 581 | not separately reproduced | no (unchecked) |
| Wrenhaven left at re-consent | 347 | 356 censored before 2y, all exit types | partly (prose, immaterial to figures) |
| Two-year survival GUL/FEN/WRE/BRE/LIN | 58/61/64/66/70 | 57.96/60.96/64.00/65.98/69.63 (hospital-specific cumulative IPCW) | yes |
| Gap | 3 | 3 | yes |
| Kaplan-Meier FEN/GUL | 61/62 | 61.1/62.3 | yes |
| Ask 2 tests / >=400 (FEN) | 10,421; 6,832 | 10,461; 6,860 literal, 10,421; 6,832 keep-latest | only under an unfiled rule |
| Ask 3 (FEN, GUL) | 832/483; 1,555/897 | same after the two forced inferences (re-registrations, enrolment date) | yes |

## Competing answers that survived
1. Ask 2: every released row is a test (10,461 / 6,860 for Fennick, all five hospitals differ) against a re-released specimen counted once at its last result (golden). Closing rule needed: one sentence in the prompt or a lab note.
2. Survival estimator: naive (host Fennick, gap 5), KM (Fennick, gap 1), pooled exit rates (Fennick, gap 2), last-class-only weights (Gullhaven 60.45 against Fennick 61.05, gap 1) against the golden hospital-specific cumulative IPCW (Gullhaven, gap 3). The judge treats the others as not equally licensed by the data (shown heterogeneity, invalid IPCW), so this is residual risk, not a failure.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, txt) | yes |
| Large file | 25,000 rows or more | visits 104,323; labs 49,162 | yes |
| Distractors | 2 or more in metadata.json, no file name labels one | echo_lab_activity_2025.xlsx, hf_clinic_sessions_2026.csv; names are neutral | yes |
| Distractor behaviour | unused, weighs, ruled out by a shipped fact | neither is used by the solution; judge found them relevant and unused; neither ranks survival | yes |
| Deliverables | 1 to 3, each in golden | 2 (xlsx, pptx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | per-hospital multi-figure asks; rounding stated for survival and gap; counts are integers | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | five hospitals by several figures plus call; rubric count not verifiable here | not verified |
| Realism | no LLM tells, goldens read as work products | judge hygiene: nothing exclusion-level; golden realism not re-read | yes (hygiene) |

## Gate G reconciliation
Gate G: PASS. No shipped artifact ranks the hospitals on survival and gets it wrong. The distractors (echo workbook, 2026 clinic timetable) rank nothing on survival. The judge named no distractor as the surface read carrying the task. The judge's mechanism (informative censoring, IPCW), family (analytical_non_defect) and surface_read_dependency (no) match the design note (Kaplan-Meier on Fennick is the easy route; the exits follow NYHA class IV) and the card's stump_class analytical. sole_data_defect: no. No mismatch.

## Stump power (Gate F)
Strong. Naive, KM and complete case each file the wrong host or the wrong gap. A strong model running standard KM with moves as ordinary censoring lands on Fennick with Gullhaven at 62%. Only the severity-linked exit pattern (class IV visits end in a move at about 16% per visit at Gullhaven, under 0.8% elsewhere) overturns it. Not too easy.

## Gate H
Gate H: domain pass, layers pass (Layer 1: crosswalk, BRE/BRN split, NYHA and setting format changes, duplicate lab releases, date slips, extract overrun; Layer 2: informative loss to follow-up), decisive_step analytical. Matches the card's analyst_test and domain_test and the note's Three rules (No decoy, Not semantics, Not rule application).

## Findings, ranked
1. Ask 2 re-released specimens are an unfiled rule (FIX_NOW). The design note's device D2 (a correction reported under a new accession) is intended, but the shipped text never says a re-release supersedes.
2. Golden prose inconsistency: "347 patients who left at the 2025 re-consent" against the judge's 356 censored before 2y at Wrenhaven; 581 (NYHA III/IV) not reproduced. Check both counts in the generator and reconcile or reword. No graded figure moves.
3. Survival estimator forks (pooled, last-class-only) are residual. If a pin is wanted, file the WHAT (the cohort's survival as if every patient had stayed in reach), never the weighting method.

## Next action for the author
Add one sentence to the prompt (or a lab data note in the pack) that a specimen re-released under a new accession counts once, at its last released result. Reconcile the 347 and 581 prose figures in submission.md against the generator. Leave the survival figures, the stump and the other asks byte-identical. This is the round-3 re-judge, so no further judge thread runs under this stage. Rebuild and re-check by script (figures_check.py).
