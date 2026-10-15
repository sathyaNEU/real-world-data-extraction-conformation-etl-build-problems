# determinism-check report, task457, 2026-10-14

## Verdict
DETERMINISTIC, SOLUTION_WRONG on one claim (step 3 says the n/(n+2) weighting "comes closest"; the golden's own configuration is not the closest in the natural family).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection (with etl_conformance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, sonnet, medium, scratch /tmp/determinism-check-task457-20261014T231654/ (verdict.md there). First pass (before the stage-4 re-centre): DETERMINISTIC, FIX_NOW on ask wording; this is the one re-judge.

## Why
The fifteen-member docket reproduces from the shipped files and is identical under every to-the-day, shrunk estimator tried (ratio of sums or mean of ratios, k = 1 to 4). It flips five members only under the two easy routes: reading each disclosure as covering its whole year, and an unweighted personal ratio. Asks 3, 4, 5 and the CSV row count reproduce. The weak point is the sixteenth member (Gentry 51,112, Singleton 50,859, Mahoney 50,329) and the chart's exact dollar values, which move up to about 5% with a convention the text does not file (ratio of sums vs mean of manufacturer-year ratios).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Owed 2026 (31 Dec primary, one per NPI) | 1,695 | 1,695 (appointments, department_codes) | yes |
| Not submitted by 11:59 p.m. ET 15 Jan 2027 | 91, 16 departments | 91 (32 never, 59 late), all 16 rows | yes |
| 2025 remuneration by nature | 4,531 / 1,387 / 768 / 254 / 190 / 7,131 ($000) | 4,531,292 / 1,387,184 / 768,158 / 254,183 / 190,105 = 7,130,921 | yes |
| 2026 non-reporting company items | 57 / 11 / 126 / 3 / 197 ($000) | 56,900 / 11,200 / 126,000 / 2,600 = 196,700 | yes |
| Conformed CSV rows | 9,987 | 9,987 | yes |
| Estimated faculty (CC1) | 278 | 278 | yes |
| December-2026 submitters in the fifteen (CC2) | 5 | 5 (Black, Hampton, Leach, Luna, Valenzuela) | yes |
| Back-test population (CC3) | 308 | 308; closeness to-the-day 537,889 vs whole-year 713,789 vs unweighted 1,028,262 | yes |
| Docket names and manufacturers | 15 | 15 reproduced; 15th Baldwin 72,267, 16th 51,112 | yes |
| Step 3 "n/(n+2) comes closest" | closest | not the minimiser: sum/mean variant 524,894 beats golden 537,889 | no |
| Sixteenth member (ask 2) | Gentry | Gentry or Singleton by convention | convention-dependent |

## Competing answers that survived
Fork: is a faculty member's ratio, and the faculty-wide ratio, a ratio of sums or a mean of manufacturer-year ratios (k = 2)?
| Personal | Faculty-wide | 2025 closeness | Sixteenth |
|---|---|---|---|
| sum | sum (golden) | 537,889 | Gentry |
| sum | mean | 524,894 (closest) | Gentry |
| mean | sum | 542,027 | Singleton |
| mean | mean | 532,124 | Singleton |
The fifteen are unaffected in all variants. The sixteenth and chart values (up to about 5%, e.g. Drake 120,180 vs 114,044) are not closed by any shipped rule; policy 5.4 leaves the candidate family open. Other forks checked and closed by files: non-reporting company by register not entity_type (entity_type would give 391,500; field definitions flag the list as dated); 2 disputed records (2,405) kept as published; blank record NPIs require the profile join.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | csv, xlsx, pdf | yes |
| Large file | 25,000+ rows | 90,088 rows (general jan2027 extract; 90,089 lines with header) | yes |
| Distractors | 2+ named in metadata.json, none in a file name | 3 named (research payments, NIH awards, June 2026 PY2025 extract); file names do not label them | yes |
| Distractor relevance | unused by solution, relevant enough to weigh, ruled out by a shipped fact | judge found them present and unused; June 2026 extract is a prior vintage of 2025 | yes (judge-reported) |
| Deliverables | 1 to 3, all in golden | 2 (docx, csv) | yes |
| Asks | multi-dimensional, unit and rounding stated | three tables plus chart plus CSV; dollars to nearest thousand stated in prompt; tables' units inside asks | yes |
| Prompt shape and 25 criteria | identifiable, 25+ | shape 01 ranked list under a cap; design note estimates about 38 criteria before asks | yes (design estimate, not generated rubric) |
| Reads as real, not LLM generated | | judge found system-export mess; no authoring disclosures; leak report REVIEW without LEAK | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump class analytical, strategy forecast_method_backtest (G16, method selection) with the whole-year docket as the easy route; the card's analyst_test names the same five swapped members (Blackwell, Gentry, Harper, Mahoney, Singleton for Black, Hampton, Leach, Luna, Valenzuela) that the judge found under the whole-year reading. Match. Declared distractors (research payments, NIH awards, June 2026 extract) were not named as carrying the task. Gate G: PASS, no shipped artifact ranks candidates on the decision question wrongly; difficulty survives deleting wrong numbers. Only discrepancy: the note's claim that n/(n+2) "comes closest" is true only against the note's own enumerated family (the judge's wider family has a closer variant), and the sixteenth is convention-dependent.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Layer 1 is mixed formats, UTC vs Eastern, divisional recoding, renamed manufacturers, typed company names. Layer 2 is estimating unobserved remuneration (reporter error on aligned reference windows, validated out of sample). Decisive step is comparing each disclosure with payments made by its submission day and grossing up December 2026 filers. Matches the card's domain_test and `## Three rules`.

## Stump power (Gate F)
Strong. Whole-year reading and unweighted personal ratio each put a wrong five on the docket; only the back-test against the latest publication, as policy 5.4 requires, separates them. Expect strong models to fail on the December-submission share and the shrinkage. No ban triggered.

## Findings, ranked
1. (FIX_NOW) Step 3 claims the n/(n+2) weighting "comes closest" under policy 5.4; a ratio-of-sums personal ratio with a mean-of-ratios faculty-wide ratio is closer (524,894 vs 537,889). Restate step 3 to the convention actually used (ratio of sums for both) and drop or correct "comes closest", or move the golden to the closest variant.
2. (FIX_NOW) The sixteenth member (Gentry vs Singleton) and the chart's dollar values (up to about 5%) depend on the unfiled ratio convention. File the population/ratio form in the prompt (the WHAT, never the method), or make ask 2's sixteenth and chart values tolerance-based. Filing the ratio form in the prompt is the larger change; if taken it risks turning the decisive step toward rule application, so prefer wording the golden and rubric to a convention and tolerance.
3. (note) The fifteen, tables and CSV need no change and no rebuild; first-pass ask-wording finding is not repeated by this thread.

## Next action for the author
Run /fix-determinism task457 on findings 1 and 2: state the golden's ratio-of-sums convention in step 3 and the chart/sixteenth answer (or give the chart a tolerance), leaving the main call, the stump and every graded figure of the docket, tables and CSV frozen.
