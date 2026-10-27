# determinism-check report, task309, 2026-10-27

## Verdict
DETERMINISTIC, SOLUTION_WRONG (minor: SOLUTION_STEPS step 7 wording, ask 7 only)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call is forced by the filed standard. MG-04 section 3 is a pass/fail reproduction test and the data separates the candidates. One pooled cut (0.106) fails Kendra, Marisol and Odile and files Marlin Shoals (1.07 removed against Cypress Ridge 0.46). The cut by 10 mph gust class passes all 5 storms and files Cypress Ridge 2.80 against Marlin Shoals 2.06. Cypress Ridge is first and Marlin Shoals second in every passing form tried. The one live defect is that step 7 of SOLUTION_STEPS, read literally (match permits by ZIP and house number), gives Heron Bay 380 homes and 137,213 for ask 7 against the golden's 382 and 137,967. The other three counties are unchanged.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Qualifying storms (FORTIFIED paid of USD 10M or more since 2012) | Ines, Kendra, Marisol, Odile, Quenby | same five (46.4, 16.6, 63.7, 21.5, 271.6 USD M) | yes |
| Class cuts vs paid, 5 storms | pass within 10% | +1.7, -0.0, -0.6, -3.8, +0.3 percent | yes |
| Pooled cut | fails Kendra, Marisol, Odile | 0.106; +3.2, +72, +46, +136, +3.7 percent | yes |
| 2027 annual EL (USD M) MRS/HRB/CLF/CYR | 10.12/5.65/0.51/4.38 | 10.118/5.650/0.513/4.379 | yes |
| Loss removed (USD M) | CYR 2.8, runner-up MRS | CYR 2.800, MRS 2.063, HRB 1.642, CLF 0.326 | yes |
| Ask 5 certificate counts and Coverage A | 1,711/681,915; 1,665/605,650; 1,420/504,862; 1,813/823,282 | identical | yes |
| Ask 6 legacy storms | 47,101/902; 10,486/265; 19,875/9,273 | identical | yes |
| Ask 7 roof age (with old-to-new street pairing inferred) | 77/30,285; 382/137,967; 520/185,473; 610/283,409 | identical | yes |
| Ask 7 as step 7 reads (ZIP and house number only) | same | HRB 380/137,213, others same | NO (wording fork) |

## Competing answers that survived
1. Ask 7, Heron Bay: ZIP and house number only gives 380 / 137,213; the golden's 382 / 137,967 needs the renamed street paired to its old name (Boggy Creek=Marsh Hen, Tram=Gulf Breeze, Sawmill=Laurel Hill, Pinebarren=Fort Dale). No shipped file gives the pairing, so a solver infers it from ZIP and house-number matches. With it inferred the answer is unique. The step wording is the defect.
2. Ask 2 grain: the figure is not unique across every form that passes MG-04. 10 mph classes give 2.80, classes derived from the 5 test storms only give 2.85 (still 2.8), bins at 100 and 130 mph give 2.77 (2.8), bins at 110 and 130 mph give 2.60. The 10 mph classes are the vendor hazard summary's own grain, so the judge rates this low risk. The call is unaffected.
3. Main call: Marlin Shoals wins only under the pooled cut, which MG-04 rejects. No surviving alternative.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 4 (csv, parquet, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | claims_payment_lines 111,707 rows | yes |
| Distractors in metadata.json | 2 or more, no file name labels one | reinsurance program PDF, contractor quotes xlsx; neither named as a distractor in a file name | yes |
| Distractors unused and weighable | each unused, weighable, ruled out by a shipped fact | judge found both unused; neither answers a graded quantity. Whether each reproduces a plausible wrong ranking was not checked. | yes, with that caveat |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, png, docx), all present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | asks 4 to 7 span counties or storms, and the prompt gives unit and rounding for each | yes |
| Prompt shape and rubric of 25 or more criteria | identifiable shape; 25 or more | shape 01 in metadata; the asks give about 40 gradable cells (4 + 4x2 + 3x2 + 4x2 + call, runner-up, county). The rubric itself is not generated yet. | yes (by count) |
| Reads as real, not LLM generated | yes | the judge found no authoring language. The prompt is one plain paragraph under 1,000 characters (950). I did not read the golden docx for realism. | provisional |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note declares estimation_fit with the decisive step "conditioning the cut on each event's peak-gust class". The card has stump_class analytical. These agree on the stump: the pooled-cut easy route lands on Marlin Shoals, and the gust-class cut lands on Cypress Ridge. The card carries no mechanism or family field to compare against. The thread named no distractor as the surface read carrying the task. The contractor-quotes and reinsurance distractors play no part in the easy route. The easy route's wrong answer (Marlin Shoals) comes from the unadjusted largest-EL ranking and the pooled cut, not from a shipped ranking. No Gate G finding.

Gate H line: domain pass, layers pass, decisive_step analytical. This matches the note's Three rules (domain test, Layer 1 mess that does not decide the call, Layer 2 estimation_fit) and the card's analyst_test and domain_test. No mismatch.

## Stump power (Gate F)
Good. The easy route is one pooled cut or the vendor's unadjusted ranking, and both name Marlin Shoals. MG-04's executable test rejects the pooled cut in 3 of 5 storms. The solver must then find the gust dependence to reach Cypress Ridge. Caution for the main thread: the thread labels executing MG-04 rule application and the choice of a passing form analysis. A strong solver who runs the filed test will probably reach classes, and the design's own ladder shows 20 mph classes fail while 100/130 and 110/130 bins pass in the judge's recompute. The note says two classes at 130 mph fail (Odile 13.0 percent). The judge's bins at 100/130 and 110/130 are different splits, so the claims do not conflict. But they widen the set of passing forms, and the printed figure varies (2.6 to 2.8). The main thread should weigh how likely a strong solver is to try the test at all, and whether the ladder's "R3 fails" claim holds against these alternative splits.

## Findings, ranked
1. FIX_NOW: SOLUTION_STEPS step 7 states the permit match as ZIP and house number to the new street name. Literal reading gives Heron Bay 380 / 137,213. Reword as: renamed street paired to its old name, then ZIP, house number and building. This is a submission.md change only, with no input or model change.
2. The old-to-new street pairing is in no shipped file. It is recoverable by inference, and the golden holds, but the main thread should confirm a mapping file or a stated rule is not needed for a literal reader. A data-semantics ask, which is free of rule 3.
3. Ask 2 grain: optionally state in the prompt that the cut is taken by the vendor's gust class, filing the WHAT and not the HOW. The 110/130 bins print 2.6 and so conflict with 2.8. This also bears on the stump: filing the class grain makes the decisive step easier, so weigh it carefully.
4. The design note's R3 claim (two classes at 130 mph fail) should be checked against the judge's passing 100/130 and 110/130 splits and the ladder text amended if it overstates.
5. Cross-batch fingerprinting was not possible in isolation. Left to guard.py.

## Next action for the author
Reword step 7 in submission.md (finding 1), rerun checks.py, then request the single permitted re-judge.
