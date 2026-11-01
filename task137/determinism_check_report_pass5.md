# determinism-check report, task137 (pass 5), 2026-11-01

## Verdict
DETERMINISTIC (minor SOLUTION_WRONG on one wording claim in critical component 3)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Reship after the leak-gate repair; target.zip md5 8f5c6aa228c4385bd09c5d4fdf29e2c8, 12 files, no data_dictionary.csv. One thread, one pass, judge output at /tmp/determinism-check-task137-pass5/verdict.md.

## Why
Read literally, the plan is 2025-26 GP-form arrivals with the run-out suppression taken out, grown by 1.035 squared. It lands in the 45,000 bucket (43,750 to 46,250) under every well-fitting specification the judge tried (44,600 to 45,100). The reachable wrong answers are 40,000 (seen only) and 42,500 (seen plus turned away). The main call is forced. The only defect on the graded blocks is the AIC gap claim. Two soft forks sit on asks 2 and 3.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| GP seen 2025-26 | 37,853 | 37,853 | yes |
| GP turned away | 1,365 on 56 of 253 days | 1,365 on 56 of 253 | yes |
| Window by AIC | 8 weeks | 8 (9 weeks 3.7 worse) | yes |
| Lag coefficient | about -0.37, SE 0.026 | -0.372, SE 0.026 | yes |
| Gap, windows of 5 weeks or fewer | at least 67 worse | L=5 is 65.3 worse (62.6 on a common sample); L=1 to 4 more than 90 worse | NO |
| Underlying 2025-26 | about 41,800 to 42,000 | 41,784 (L=8), 41,983 (L=9) | yes |
| Plan | 44,800 to 45,000, so 45,000 | 44,760 and 44,973, so 45,000 | yes |
| Ask 2, 7 specialties by quarter (17,222 total) | as submission | cell by cell match under the golden code mapping | yes |
| Ask 3 days lost | 29, 23, 39, 23 | 29, 23, 39, 23 | yes |
| Ask 3 rate | 6.8, 5.6, 8.7, 5.2 | 6.79, 5.60, 8.71, 5.22 | yes |

## Competing answers that survived
- **Ask 2, old clinic-code mapping (soft fork A).** The register's clinic_days match each old code's whole-history weekdays one for one. That gives a second mapping: C01 to Rheumatology, C02 to Haematology, C03 to Renal, C04 to Cardiology, C05 to Diabetes, C06 to Gastroenterology, C07 to General medicine. It moves the spikes into other specialties. Two shipped facts rule it out: late-March 2026 forms fall on the old codes' weekdays only under the golden mapping, and weekly volume is continuous across the switch only under the golden mapping. No shipped sentence states either fact, so the data separate the readings but the text does not.
- **Ask 3, "Vacant line = Y" (soft fork B).** Read literally, the flag means vacancy. That gives 11, 10, 13 and 9 days (rates 2.6, 2.4, 2.9, 2.0). The annual report names one vacancy only, but the roster flags four other stretches. Each is a named holder's own line, entered right after five Sickness days and returned to the same holder. The export convention is filed nowhere.
- **Main call:** no surviving fork. The competing answers 40,000 and 42,500 are analytical errors, not reading differences.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, json) | yes |
| Large file | 25,000 rows or more | 306,115 rows (queue events); legacy 85,649 | yes |
| Distractors | 2 or more, named in metadata.json, none labelled in a file name | phlebotomy_patient_survey_2025.csv, community_hub_session_plan_2027.xlsx; the judge found them plausible | yes |
| Deliverables | 1 to 3, all in the golden | 2 (hub_plan_2027-28.xlsx, gp_demand_2025-26.png); both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | yes (quarter x specialty; days whole, rates one decimal) | yes |
| Prompt shape and rubric of 25 or more criteria | identifiable, 25 or more | shape "other" in metadata; the 25-criterion count is not checked here (rubric is generated) | not verified |
| Realism | no LLM-generated read | judge found no generation language; mixed formats and messiness present | yes |

Minor hygiene, not decisional: the annual report gives 41 per cent waiting over 45 minutes and 78 per cent rating good, against 40.3 and 76.7 per cent in the survey file.

## Gate G reconciliation
The judge's line is mechanism statistical_rigor, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. This matches the design note's `## Three rules` and the card's analytical class. The declared distractors (survey, session plan) are not the surface read; the judge named seen plus turned away as the easy route, and the note names the same route. No mismatch. The judge's remark that the prompt word "underlying" leans toward the answer is recorded and not counted as a leak.

Gate H line: domain pass, layers pass, decisive_step analytical. This matches the note's domain test (unconstrained demand with deterrence undone by a fit-selected window).

## Stump power (Gate F)
Good. Seen plus turned away files 42,500, seen alone files 40,000, and only a lagged-displacement model with the fit-chosen window reaches 45,000. The judge classed the step analytical on a method it had to estimate and select by fit, not a textbook route. The bucket is robust, so a strong solver who fits windows lands the call. No contrasting model runs were supplied. The main thread weighs this against the note's ladder.

## Findings, ranked
1. **The AIC gap statement does not reproduce.** "Every window of five weeks or fewer at least 67 worse" appears in critical component 3 / step 3 of submission.md and in the design note's `## Three rules` (Not rule application and Analyst test lines). The judge measures L=5 at 65.3 worse (62.6 on a common sample). It is immaterial to the call. Reword to what reproduces ("at least 60 worse"), and update the design note and checks.py if they assert 67.
2. **Soft fork A (ask 2).** The rule that closes the old-code mapping (late-March weekday match plus volume continuity) is filed nowhere. Record it in the solution steps. The stronger repair is a prompt or register sentence, which would change what solvers see.
3. **Soft fork B (ask 3).** The rule that closes the roster convention (five-day-then-unassigned pattern plus the report's single named vacancy) is filed nowhere. Same treatment as fork A.
4. **Chart ask.** The kept-in-house band depends on the window (8 against 9 weeks moves the year total by about 200 visits), and the weeks that straddle the fiscal year ends are partial. This is loosely gradable only, not a determinism defect.

## Next action for the author
Correct the AIC gap figure from 67 to a value that reproduces (60) in `submission.md`, the design note and any `checks.py` assertion, and add the two closing facts for the code mapping and the roster rule to the solution steps. No input file, prompt or model rerun is needed. Then re-judge once, per the FIX_NOW rule. Rewording only: the optional pin on forks A and B in the prompt or register is a larger change and needs a rerun.
