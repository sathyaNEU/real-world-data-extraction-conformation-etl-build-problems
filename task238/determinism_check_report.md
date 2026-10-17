# determinism-check report, task238, 2026-10-17 (pass r2)

History: r1 was DETERMINISTIC with FIX_NOW on asks 2 and 3; fixed by filing in plan section 5 that a return or interview counts only from the person the letters ask for (age 18 or over). This report replaces the r1 text at the main session's direction and judges the rebuilt bundle (r2 thread unzip), plus two later changes that touch no graded figure: the published series' Q2 2027 now matches the letter B completes it was released from, and DATA_DICTIONARY.md now says END_TIME is when the interviewer coded the result.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_selection, stumping_family: analytical_method (causal identification by random allocation), surface_read_dependency: no, sole_data_defect: no

## Why
The band is forced by MS-14 section 5 (widest whole-point band keeping every index within Table 2) and the mode effects are identified by the random letter allocation (plan sections 2 and 5). With the plan's counting rules heavy drinking's effect is 6.63 points, 0.30/6.63 = 4.53, so the band is 4. Every filed convention tested leaves it at 4, and every golden figure reproduced. No Gate A to E failure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Completes | 40,821 | 40,821 (web returns, CATI interviews) | yes |
| BD mode effect | >6 and <=7.5 | 6.63 pp, band 4.53 | yes |
| VL band | 6 to <7 | 6.83 | yes |
| Other indexes | 8 or more | 9.11 to 37.58 | yes |
| Band | 4 | 4 | yes |
| Response rates Q2 A / Q2 B / Q3 A / Q3 B | 57.3 / 56.4 / 56.3 / 56.8 | 57.33 / 56.43 / 56.33 / 56.81 | yes |
| Valid answers, 12 indexes online / telephone | LS 21,463/19,144 ... FS 20,753/18,830 | all 24 pairs exact | yes |

## Competing answers that survived
None on the main call. Web vs telephone difference gives band 2 and the covariate-adjusted version band 3; both are ruled out by MS-14 section 3 (counterfactual mode effect) and visible selection into mode (telephone BD mean 13.4 under A vs 18.3 under B). Cleaning forks (fixed +12 close for Q3, no close, staff returns online, CATI START vs END, age filter order) all give band 4; they move only ask 2/3 counts, and the plan section 5 age rule and the dictionary END_TIME line now close them.
Residuals, none moves a committed answer: (1) ask 4 does not say whether non-binding bars are floored whole points or one decimal (LS, WW, HY sit near whole numbers); (2) the response-rate eligibility of 144 addresses coded 4.1/4.2 holding a counted complete rests on the plan's highest-result sentence (strict reading gives 57.2, 56.3, 56.2, 56.7); (3) docx internal timestamps and a large styles part could be scrubbed.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 (the thread's "11" is a miscount; target.zip lists 12) | yes |
| Formats | 3 or more | 5 (csv, pdf, docx, xlsx, md) | yes |
| Large file | 25,000 rows or database | cati_call_records 204,006 rows; addresses 76,000 | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | call records and published indexes; names neutral | yes |
| Distractor relevance | unused by solution, weighs, shipped fact rules out | published series (telephone-first design, Q2 matches letter B completes) and call records (contact attempts, not answers) are not used by any figure | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | band (whole points), 4 rates (one decimal), 24 counts, chart; chart bar rounding unstated (residual 1) | yes, minor |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 04 identified; 29 gradable figures plus call components exceed 25; the generated rubric is not in the folder, so the count is not verified here | yes (unverified count) |
| Not LLM-generated, goldens real | | no authoring language seen; README and dictionary read slightly tidy | yes |

## Gate G reconciliation
Thread: mechanism method_selection, stumping_family analytical_method, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; default path (covariate-adjusted web vs telephone) files 3 with safe after dark binding, golden 4 from the letters' random allocation. The thread found the same trap (adjusted gives 3, naive 2; it records BD, not SF, as the binding index on those routes' arithmetic, which does not change the band answers). Gate G passes: no shipped artifact ranks the bands; the declared distractors are not named as carrying the task. Match, no finding.
Gate H: domain pass, layers pass, decisive_step analytical. Matches the card's analyst_test and domain_test and the note's Three rules (no decoy, not semantics because the default path reads every field right and files 3, not rule application because MS-14 files the quantity but not the identification step).

## Stump power (Gate F)
Good. A strong model that cleans the data correctly still fails at the estimand by comparing web with telephone (band 2 or 3). Moderate too-easy risk because the plan states the random allocation, but turning the definition into an identification step is required.

## Findings, ranked
1. Optional: state in ask 4 whether non-binding bars are floored whole points (MS-14 "whole-point" supports floors) or one decimal.
2. Optional: scrub docx metadata.
3. Optional: note the 144-address eligibility reading in the workbook notes; plan text supports the golden.

## Next action for the author
Ship; optionally add the rounding phrase to ask 4 only if a rebuild is already planned (it touches no graded figure).
