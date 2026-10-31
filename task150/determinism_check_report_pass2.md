# determinism-check report, task150 (pass 2), 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: method_model_selection, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet medium thread over a fresh unzip of target.zip (13 files) and the five blocks only; verdict at /tmp/determinism-check-task150-pass2/verdict.md. Earlier reports were not given to it.

## Why
Every graded figure reproduced from the shipped files. Policy FEA-R2 2(e) and 3 pin the need rule (excess over 24, rounded up) and the descending-excess placement. Definitions 2(f) (homeroom section counted once per school, room and session) and 2(g) (preschool by classroom location) close the forks that the removed notes used to cover; the thread confirmed the facts now live in the exports' own columns and in the policy. The projection method is the one open choice and the data separate the candidates: the pupil-level transition model fitted to 2019 misses each 2026 school count by 5.0 per cent or less, while grade-progression ratios (1, 2, 3, 5 or 13 years) miss by up to 12 per cent at Fifth Street and 8 to 10 per cent at Prairie Rose. Residual risk, not a fail: the prompt and policy never say to validate, so a solver stopping at progression ratios has a literal-text defence. The judge's optional lever (file the WHAT, e.g. a projection that reproduces each school's 2026 count from the 2019 count) would move no figure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| October 2026 K-5 counts (membership vs meal_eligibility) | 778, 804, 733, 845, 949, 726, 566 | same | yes |
| Pupil rows, 14 count days | 76,597 | 76,597, no duplicate pupil per day, 50 rows without SASID or crosswalk match | yes |
| Excess over rated capacity, PR / Lincoln / 5th St / Bluestem / Kessler / N Fork / Ortega | 152, 131, 109, 89, 60, 10, -92 | 152, 131, 109, 88 to 89, 60, 10, -92 | yes (Bluestem 88 to 89 rounds to the same need of 4) |
| Need | 7, 6, 5, 4, 3, 1, 0 (26) | same | yes |
| Placement | 7, 6, 5, 4, 2, 0, 0 | same | yes |
| Homeroom classes K-2 | 17, 19, 19, 15, 21, 15, 13 | same | yes |
| Homeroom classes 3-5 | 17, 15, 13, 20, 20, 17, 13 | same | yes |
| Preschool children (5th St, Ortega, Kessler, N Fork) | 88, 94, 51, 35 | same | yes |
| Preschool classrooms | 4, 4, 3, 3 | same | yes |
| Back-test, flow model | within 5.0 per cent | -0.6, -0.6, +5.0, +2.2, -1.0, +1.4, +0.3 | yes |
| Back-test, five-year ratios | -8.2 at Fifth Street, +8.3 at Prairie Rose | -8.0 and +8.3 | no, minor: Fifth Street reproduces at -8.0, the submission states -8.2 (SOLUTION_WRONG wording only, no figure graded moves) |

## Competing answers that survived
None on the main call under the literal text. Method alternatives are closed by data, not by a filed rule:
| Method | Prairie Rose | Fifth Street | Lincoln | Bluestem | Kessler |
|---|---|---|---|---|---|
| 5-year progression ratios | 8 | 3 | 6 | 7 | 0 |
| 3-year ratios | 8 | 4 | 6 | 6 | 0 |
| 1-year ratios | 7 | 0 to 1 | 5 to 6 | 6 | 5 to 6 |
| Golden (flow model) | 7 | 5 | 6 | 4 | 2 |
Placement held across fitting windows (2013, 2016, 2019, 2021) and future-birth assumptions (last, 3-, 5-, 10-year mean). The one exception is births held at the single 2024 value (Bluestem 5, Kessler 1 in two of four windows), an arbitrary non-expected choice with 2025 births on file as provisional. Two literal-text notes: counting sections instead of rooms and sessions, or preschool by case school, would change figures, and 2(f) and 2(g) close both.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 13 files; csv, txt, xlsx, pdf; october_membership_2019-2026.csv 44,314 rows | yes |
| Distractors | 2+ named in metadata.json, none labelled in a file name | facility_condition_assessment_2025.xlsx, meal_eligibility_2026-10.csv; names carry no label | yes |
| Distractors unused yet weighable, not answering a graded quantity | | both rank nothing on enrollment (design note); meal counts match the 2026 K-5 counts but project nothing | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, svg), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | | tables over seven schools and four sites; whole numbers stated once for every figure | yes |
| Prompt shape, 25+ criteria | | placement schedule plus two October 1 tables plus chart; roughly 14 + 14 + 8 + 7 graded cells before the call | yes (rubric is generated, not counted here) |
| No describing file ships | | no notes, manifest or readme in target.zip (grep count 0) | yes |
| Reads as real work product / not LLM generated | | schedule and SVG; not judged beyond the thread's hygiene read | yes, by the thread's read |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family method_model_selection, surface_read_dependency no, sole_data_defect no. Design note and card: mechanism gap time with population (G6, G16, G13), strategy population_selection, Gate G `forecasting`, declared wrong route progression ratios. Consistent: the family reads as forecasting in both. The thread names neither declared distractor as the surface read, so the distractors are not too load-bearing. The thread's competing answers (8/3/6/7/0 for five-year ratios) match the card's analyst_test schedule exactly.

## Gate H line
domain: pass; layers: pass; decisive_step: analytical. Card: stump_class analytical, analyst_test and domain_test present; the thread's wrong route (five-year ratios giving Prairie Rose 8, Fifth Street 3, Bluestem 7, Kessler 0) is the card's. The decisive step is out-of-sample validation of the projection, not a field reading or a rule execution, and the thread did not class it analytical merely because the method is the field standard: it reached the golden only through the back-test.

## Stump power (Gate F)
Strong by the thread's read: the pupil-level linking needed to see arrivals and transfers is demanding, and the easy ratio route lands a different, wrong schedule. Weigh against the design note's ladder: the cohort-component model is a textbook demographic route a strong solver can take (stumping 1.3), and the filed text never asks for validation, so a solver who tests ratios against the 2019 back-test lands the call.

## Findings, ranked
1. Low: the submission's Step 4 and Final Recommendation give the five-year-ratio miss at Fifth Street as 8.2 per cent low; recomputed value is 8.0. The text of the submission needs the 8.0 figure or the stated basis. This is outside the graded blocks' load-bearing figures.
2. Low, optional: the prompt could file the WHAT (a projection that reproduces each school's 2026 count from the 2019 count). It would not move any figure and is not required for DETERMINISTIC.
3. Note: Bluestem excess reproduces as 88 to 89 across runs; the need of 4 is unchanged.

## Next action for the author
No repair required. Optionally correct the Fifth Street ratio miss from 8.2 to 8.0 per cent in submission.md steps 1 and 4 if the generator's figures.json also gives 8.0, then proceed to ship checks.
