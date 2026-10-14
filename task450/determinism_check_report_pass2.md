# determinism-check report, task450, 2026-10-14 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Scope: stage 4 re-ship after the second analytical layer (the shared items screened before the link). One Sonnet/medium thread, fresh unzip at /tmp/determinism-check-task450-p2/target/, verdict at /tmp/determinism-check-task450-p2/verdict.md. Pass 1 report kept as determinism_check_report.md.

## Why
Every graded figure recomputed from the bundle. The decisive step is the link of the 2026 form to the 2025 scale. Items 3, 11 and 35 (TEKS 5.4F) moved +27.7, +29.3 and +30.0 points while the other 22 shared items moved +0.4 to +3.1. On the 22 stable anchors the passing raw score is 25 under chained equipercentile, Tucker and Levine, and it holds when one to four more anchors are dropped and under the uncorrected key. The filed rules, the key notice and the technical report fix population, rated set and the 15 designated campuses. No competing answer survived for the main call or asks 1 to 5.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2025 tests / mean | 6,554 / 24.97 | 6,554 / 24.97 | yes |
| 2026 tests / mean (M547961 keyed B) | 6,341 / 24.07 | 6,341 / 24.07 (24.20 uncorrected) | yes |
| Common-position items | 25 | 25 | yes |
| Items 3, 11, 35 percent correct 2025 to 2026 | 51.3/45.8/47.4 to 79.1/75.1/77.4 | 51.3/45.8/47.4 to 79.1/75.1/77.4 | yes |
| 22 stable anchors mean | 10.69 to 11.08 | 10.69 to 11.08 | yes |
| Passing raw score on 22 anchors | 25 | 25 (chained 24 to 298.1, 25 to 304.4; Tucker, Levine same) | yes (frequency estimation and Rasch not run by the judge) |
| 2025 conversion applied raw | cut 27, 32 campuses | cut 27, 32 | yes |
| Distribution-matching cut | 26, 23 campuses | 26, 23 | yes |
| FAY tested at 54 rated campuses | 5,727 | 5,727 (Vereda 8 unrated) | yes |
| Met standard / share | 2,745 / 47.9 | 2,745 / 47.9 | yes |
| 54 per-campus tested and met | listed | 0 differences | yes |
| Designated campuses | 15 | 15 (Vance 36.8 vs Chinaberry/Elmhurst 41.6) | yes |
| Tobar with Delgadillo | 61 of 176, 34.7 | 143+106 reading, 34.7 | yes |
| Ask 4 by community (2025) | N 1,431/56.8, C 1,408/41.2, E 1,184/38.2, S 1,172/36.2, W 1,359/49.3 | identical | yes |
| Ask 5 no-result counts | 18/25/18/19/18, district 98 | identical (148 without the merge) | yes |

## Competing answers that survived
None on the main call or asks 1 to 5.
- Minor, ask 4: SCHOOL_CODE in the 2025 file collides with 2026 campus numbers (code 111 is Agarita Bend in 2025, Pinto Mesa in the directory). The name is the only self-consistent key and the prompt does not say so. The judge rated it an optional wording note, not a fork. Optional: one clause in the technical report excerpt or data dictionary that 2025 codes are the old platform's.
- Alternate-route counts: the judge found the all-25 chained equipercentile link passes at raw 22 or 23 (design note: 23, 6 campuses) and ran no campus count for it. This is a wrong-route figure quoted in the submission ("6 or 13"), not a golden figure. See findings.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | grade5_math_responses_2026.csv, 317,050 rows | yes |
| Distractors named, none labelled in a file name | 2 or more | grade5_enrollment_projection_2026-27.csv and math_professional_learning_hours_2025-26.csv in metadata.json distractor_files; names do not say "distractor" | yes |
| Distractor unused yet weighable, none answers a graded quantity | yes | both unused by the solution (design note); neither reproduces a graded figure; judge saw no use | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 54-campus table, 5-community table, 6-row no-result table; percentages to one decimal and whole-number counts stated in the prompt | yes |
| Prompt shape and 25 or more criteria | yes | shape 14 (cuts of a distribution) in metadata; 15 + 54x3 + 15 + 6 graded cells far above 25 | yes |
| Not LLM-reading, goldens real work product | yes | judge saw no authoring leakage; golden realism was a stage-3 gate | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, analyst_test and domain_test present; the card's mechanism and decisive_step fields are None. Design note: Layer 2 is estimand_identification then estimation_fit, decisive step is screening the shared items and linking through the 22. These agree in kind (equating design and anchor selection). No mismatch.
- Declared distractors (enrollment projection, professional-learning log) were not named by the judge as a surface read carrying the task: not too load-bearing.
- No shipped artifact ranks the campuses wrongly; the 2025 conversion is the 2025 form's own and the technical report scopes it.
- Judge's borderline note: the three 5.4F items look planted. The design note answers that the rise is the 2026 cohort's real answers under a curriculum teaching the standard earlier, no record is defective, and the 22 others moved with the cohort (No decoy line). Left to the portal to confirm.

Gate H: domain pass, layers pass, decisive_step analytical. Matches the card and the note's Three rules.

## Stump power (Gate F)
Strong. An analyst who cleaned the data and read every rule would reach 32 (2025 conversion), 23 (distribution matching) or 6 to 13 (all 25 anchors), not 15. The drift is found only by anchor stability screening, which no file hints at.

## Findings, ranked
1. None blocking.
2. The submission's section 1 and the design note give the all-25 link as pass raw 23 or 24 by method and 6 or 13 campuses. The judge's chained equipercentile put the all-25 pass at 22 or 23 and ran no campus count. These are wrong-route statements, not graded figures, and the design note's own checks assert them; re-check that "23 or 24" holds in `checks.py` for chained equipercentile.
3. The judge did not run frequency estimation or Rasch true-score linking, so submission step 3's claim that they give 25 rests on the generator's own checks (SF2 asserted).
4. Optional ask 4 wording note above (SCHOOL_CODE versus name).
5. Live-test the screen as a method choice (judge's borderline note).

## Next action for the author
Proceed to ship: no FIX_NOW. Optionally confirm in `checks.py` that the all-25 chained equipercentile passing raw score matches the "23" quoted in section 1 (the judge saw 22 or 23), and add the one-clause 2025 SCHOOL_CODE note if cheap.
