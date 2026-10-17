# determinism-check report, task241, 2026-10-17

## Verdict
DETERMINISTIC (no SOLUTION_WRONG on the decisions; one soft spot in the third decimal of two offsets)
**Disposition:** FIX_NOW (solution text only; no prompt or file change, no rerun)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The release thread files the estimand (float salinity less the true salinity of the water it sampled, flag 1 or 2, 1,400 to 1,900 dbar, mean over 2027 ascending profiles, tolerance 0.010). Executed on potential-temperature levels at each profile's position it gives six adjusted floats, and the other 18 sit at 0.004 or less in magnitude. Asks 2 and 3 reproduce exactly. The judge thread's sources are the scratch bundle only (/tmp/determinism-check-task241-1792272746/verdict.md).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Profiles / resent | 878 / 38 | 878 / 38 | yes |
| Good layer values | 8,791 | 8,791 | yes |
| Six adjusted offsets | -0.022, -0.021, -0.027, -0.030, +0.021, +0.020 | -0.02175, -0.02052, -0.02655, -0.02968, +0.02134, +0.01998 | yes to 3 dp (see soft spot) |
| Largest other | -0.003 (1990016) | -0.00317 | yes |
| Ask 2, casts to 2,000 dbar 2015 to 2025 | 23,18,21,23,21,12,23,21,18,22,16 | identical | yes |
| Ask 3, in-24h by month | 69,64,69,66,68,68,67,68,64,69,62,66 (800) | identical | yes |

## Competing answers that survived
None on the decisions. Variants tested (no interaction term, cubic, window, archive only, RHD only, year ranges, nearest 3/8/15 casts, flag handling, IPTS-68 off) all give the same six floats. Fixed-pressure gives 14 (healthy floats wrongly flagged), pooled theta gives 12, and a self-first-profiles read gives 4. The thread records no fork that closes on the filed text only by accident; the "water it sampled" wording rules out the fixed-pressure read.
Soft spot: 1990004 (-0.0205) and 1990005 (-0.0265) sit on a rounding boundary, so the three-decimal value moves by 0.001 under the no-interaction fit. Decisions are unaffected.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 (thread said 15; metadata and the zip list 16) | yes |
| Formats | 3+ | csv, md, pdf, eml, docx | yes |
| Large file | 25,000+ rows | ibfa_profile_levels_2027.csv 93,853 | yes |
| Distractors in metadata, none named in a file | 2+ | ibfa_recovered_sensor_checks.csv, ibfa_oxygen_2027.csv (file names do not label them) | yes |
| Distractor unused yet weighable | yes | lab errors of about -0.01 to -0.02 do not tie to the 2027 offsets; oxygen has no salinity; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 24 offsets, 11 years, 12 months; practical salinity to 3 dp stated, counts are integers | yes |
| Prompt shape, 25+ criteria | identifiable | shape 10 scorecard; 24 floats + 11 + 12 + decisions + chart exceed 25 by construction (not counted here) | yes |
| Not LLM generated, realistic goldens | yes | judge found no tell; I did not run golden-realism | yes (judge) |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note's stump sentence and the card (stump_class analytical, analyst_test, domain_test) agree: the decisive step is theta-level, position-mapped comparison against a fixed-pressure or pooled read. The declared distractors are not named by the thread as carrying the task. Card fields `mechanism` and `stumping_family` are None, so there is nothing to mismatch; the card should record them. Counts differ across texts: the design note and card say the fixed-pressure route files 15 (14 on clean truth) and pooled-theta 13; the submission says 14 to 17 and 13; the thread measured 14 and 12. These are prose discrepancies, not a decision change.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Delayed-mode float salinity calibration against CTD reference on theta levels with a basin gradient is the field's own estimation; the swap test fails to swap. Layer 1 is units, clocks, resent files and overlapping reference sources; Layer 2 is mapping the reference water to the sampled water. The easy route (fixed-pressure difference against the reference mean) gives 14 to 15 adjusted floats, about nine of them healthy. The design note's Three rules lines are present and agree.

## Stump power (Gate F)
Plausible. The main call can be cleared by a model that knows OWC-style practice, so most stump pressure comes from the asks (IPTS-68, depth to pressure, 116 duplicate RHD casts, repeat casts, truncated v1 files, K-float juld, Lisbon clock change). The files do not hint at either easy route.

## Findings, ranked
1. Medium (solution text): offsets to three decimals are method-dependent in the third decimal (1990004, 1990005). Fix: carry the stated plus or minus 0.003 acceptance into the grading note for the xlsx. No prompt change.
2. Low (solution text): the fixed-pressure and pooled-theta adjusted counts disagree across submission.md (14 to 17, 13), the design note and card (15, 13), and the thread (14, 12). Align the prose to a single recomputed pair in submission.md; keep the "at least eight healthy" claim only if it reproduces.
3. Low (optional): name the fit window as the reference casts' own theta range in step 5 so no solver extrapolates.
4. Low (bookkeeping): the thread counted 15 files; the true count is 16. The card lacks `mechanism` and `stumping_family`.
5. Info: no Gate G, Gate H or hygiene failure; no exclusion-level item.

## Next action for the author
Edit submission.md step and component text for findings 1 and 2 (state the plus or minus 0.003 acceptance and one recomputed set of counts), rebuild nothing, and re-judge only if the edit touches a graded figure.
