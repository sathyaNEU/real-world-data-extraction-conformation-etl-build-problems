# determinism-check report, task243, 2026-10-18

## Verdict
DETERMINISTIC, with SOLUTION_WRONG (minor: step 5 and some stated whole-per-cent figures do not recompute exactly; the call and all 12 in/out decisions do).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call is forced by the shipped files. The ToR defines D1 as the registered share of residents' deaths at 15+ in 1 Aug 2015 to 30 Apr 2020. The estimate of "all deaths" comes from the censuses, the registered deaths and the 2020 residence-five-years-ago tabulation, whose ELSEWHERE IN THE PHILIPPINES rows the cover note describes. With net movement in the balance, Santa Cruz, San Isidro, Libertad, San Luis and Del Carmen fall below 80 and the other seven sit in the high 80s. Without it Esperanza, Magsaysay and Mabini fall to 71-74 and eight offices go in. The set of five is identical under every variant the judge tried (arithmetic or geometric person-years, orthogonal or OLS, shift or no shift, spread or not, duplicate conventions, window end, fit ranges starting at 10+ or 15+, and 55+ to 75+). B1 reproduces exactly. C1 reproduces exactly only when blank-birth-date pairs are matched as duplicates.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| D1 five flagged offices (SC, SI, Lib, SL, DC) | 63, 63, 56, 64, 52 | 62, 62, 54, 62, 51 (no shift: 63, 62, 55, 64, 52) | Set yes; whole-per-cent values 1 to 2 below, inside the filed ranges |
| D1 Esperanza, Magsaysay, Mabini | 89 each | 87 each (no shift about 89) | Decision yes; value within range |
| D1 Kalinawan City, Quezon, Rizal, San Miguel | 89, 90, 89, 90 | 88, 88, 87, 88 | Decision yes; value within range |
| D1 without movement (easy route) | 8 offices | Esp 71-72, Mag 74-75, Mab 73-74; 8 in | Yes |
| Step 5 "no reading crosses 80" | claimed | A 5+ to 30+ fit puts all 12 below 80 (cause: fall in the 0-4 group) | NO |
| B1, all 12 | 88.0 ... 83.3 | identical for all 12 | Yes |
| C1, all 12 | 77.2 ... 75.9 | identical only if blank-birth-date pairs are matched; otherwise up to +0.4 (77.3, 84.8, ...) | Yes, conditional |
| FHSIS ratios | n/a | 0.78 to 1.55, not interpretable as completeness | n/a |

## Competing answers that survived
- Closed balance (eight offices): not a fork on the files. The shipped tabulation and cover note rule it out, and the judge counts it as the decisive step.
- C1 duplicate convention (blank birth date matched vs not): moves ask 3 by up to 0.4 point, which is outside one-decimal grading. This is the one surviving fork. The golden's reading is the better one, but the filed step 1 does not say it.
- Lower-range fit at 5+ to 30+ flips all 12 below 80. This is not a fork for the call, because the ToR's D1 is at 15+ and no competent reading starts at 5, but it falsifies the step 5 sentence.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, eml, md) | yes |
| Large file | 25,000 rows or more | death extract 56,866 rows; birth extract 49,950 | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | fhsis_m2_mortality_reports_2015_2022.csv, lcro_capacity_survey_jul2023.xlsx; names unlabelled | yes |
| Distractor weighs but is unused, and is ruled out | yes | FHSIS counts reported deaths (a different incomplete count) and flags offices other than the golden's; no file presents it as completeness | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 12-row grids; whole per cent and one decimal stated in the prompt | yes |
| Prompt shape and 25 or more criteria | identifiable | shape 07 grid; design note counts 12 + 12 + 24 + set + chart parts, well over 25 | yes (by design note, not independently generated) |
| Not LLM-reading, goldens realistic | yes | judge saw nothing exclusion-level; golden realism not re-judged here | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: strategy decomposition_attribution, layer 2 field_method, pattern "migration-term-in-the-growth-balance", easy route the closed balance giving eight. The substance matches (open-population estimator against the closed balance; eight against five; Esperanza, Magsaysay and Mabini are the swing offices). Only the taxonomy label differs and the judge's name for it is more generic. The declared distractors (FHSIS, capacity survey) are not named by the judge as carrying the task, so they are not too load-bearing. The judge found no shipped artifact ranking the offices on completeness. Gate G: PASS. Gate H: domain pass, layers pass, decisive_step analytical; this agrees with the card and the design note's `## Three rules`. Mild caution: the judge notes a model that knows Hill and Queiroz's migration adjustment, or that cross-checks against the special tab, will get the call.

## Stump power (Gate F)
Moderate to good. The closed balance is the textbook route and gives eight. The solver must see that older residents leave, and must use the ELSEWHERE rows to net them out. The asks (decimals of B1 and C1, roster join) add real difficulty. The design note's own pair ceiling is 36.

## Findings, ranked
1. Step 5 in submission.md asserts "no reading crosses 80 per cent", and the judge shows that false for a 5+ to 30+ fit. Restate it or limit the lower fits to start at 10+ or 15+, then recheck the quoted accepted ranges. Note the design note's 312-reading margin table also needs checking against this.
2. Stated whole-per-cent completeness (63, 63, 56, 64, 52; 89 x3; 89, 90, 89, 90) is 1 to 2 points above the judge's half-group-shifted rebuild and matches its unshifted rebuild better. Reconcile with a stated shift convention, or keep grading inside the accepted ranges, which contain every judge value.
3. C1 (ask 3) depends on matching blank birth dates in second-office duplicate pairs; one-decimal figures move up to 0.4 otherwise. Say so in step 1 and give ask 3 a tolerance of at least 0.5, or state the convention in the files.
4. Step 3's movement handling (carried half a group younger, scaled to the interval) files HOW rather than WHAT. The design note says the decisive step is the movement itself and the shift is a detail. This is acceptable only because the prompt and ToR do not file the method, and submission.md is not shown to the reviewer in that form. Confirm that nothing shipped names the migration term.

## Next action for the author
Edit step 5 and the accepted ranges in submission.md, and the matching design-note margin lines, to what recomputes (fits starting at 10+ or 15+), and add the blank-birth-date matching convention to step 1. Do not change prompt.txt or the target files. Then re-judge once if the coordinator licenses it.
