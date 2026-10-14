# determinism-check report, task127, 2026-10-14

## Verdict
NOT_DETERMINISTIC (main recommendation; the three deliverables' asks reproduce)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection (settlement-rate restatement of paid development), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Neither the prompt nor the reserving basis files a method. Basis 2.3 leaves "the selection of methods and assumptions" to the actuary, and 3.6 says only that the estimate "rests on paid loss and claimant feature counts". Several count-using or paid methods are defensible on the shipped data and land in different $25M buckets. No filed selection criterion and no shipped back-test separates them. The judge's own one-year-ahead emergence back-test did not favour the restated chain ladder. Gates C and E fail on the main call. Governing label: competing_defensible_answer (underspecified_objective runner-up). The asks (ledger tie-out, claim counts, chart) reproduce exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Paid to date, 40 accident quarters | $845.4M | $845,397,745.26 (legacy and platform payments) | yes |
| Booked BI loss | $344.6M | $344,600K (year_end_2026_preliminary_reserves.xlsx) | yes |
| Closed share, age 8, 2025Q1 / age 12, 2024Q1 | 71.9% / 80.6% | 0.719 / 0.806 | yes |
| Plain paid chain ladder | $316.8M | $316.84M | yes |
| Latest-diagonal factors | $283.6M to $314.1M | same | yes |
| Closure-restated chain ladder | $399.8M | $399.9M (interpolation detail, same bucket, over $12M from the edges) | yes (bucket) |
| Severity trended 2017 to 2019 | $356.5M | not attempted | n/a |
| Frequency x severity on paid per closed feature | not in golden | $343.8M, carry 350 | competing answer |
| Claim counts csv, 20 cells | as filed | all exact | yes |
| Ledger ask 2, quarterly issued earlier and not claims payments | as filed | to the cent, all 8 cells | yes |

## Competing answers that survived
1. Main call method: 316.8 / 343.8 / 356.5 / 399.9 give carried 325 / 350 / 350 / 400 and gaps to booked of a $19.6M release, +5.4, +5.4, +55.4. Nothing shipped says which adjustment governs. Closing rule: none filed.
2. Legacy features reopened once: the archive keeps only the last closing, so earlier states are unrecoverable. The golden treats such a feature as open until its last closing. Does not move the bucket.
3. Ask 2 Q4: relies on the Treasury convention (releases after 15:00 take the next business day's value date, a month's journal carries that month's value dates), found in no shipped document. Recoverable by reconciliation, a weak finding for the ask.
4. Batch CFB0031890 is a late post (carries 19 May checks); no ask figure moves.

## Spec gates (checked by me on the unzipped bundle)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 5 (csv, md, txt, xlsx, pdf) | yes |
| Large file | 25,000 or more rows | legacy archive 47,670; platform features 25,571; legacy payments 38,260 | yes |
| Distractors | 2 or more named, none labelled in a file name | metadata.json names earned_car_years_2017-2026.csv and motor_pd_paid_by_accident_quarter.csv; neither name labels a distractor | yes |
| Distractors unused yet weighable, none answers a graded quantity | | the judge found both unused; neither reproduces a graded figure | yes |
| Deliverables | 1 to 3, all in the golden | 3 (md, csv, png), all in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | | four quarters, ten accident years, a bar chart; cents and $25M stated | yes |
| Prompt shape and 25 or more rubric criteria | | prompt shape identifiable; rubric not part of the bundle, not verified here | not verified |
| Reads as real, not LLM generated | | the judge found no authoring or generator language | yes |

## Gate G reconciliation
Card: stump_class analytical; the design note's stump sentence and ladder name the plain chain ladder ($316.8M, carry 325) as the default path. The judge's mechanism is method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. These are consistent with the card on what the stump is, and the declared distractors (PD triangle, car years) carry nothing. The mismatch is on determinism: the design note says "the method stays open" (basis 2.3) and relies on the data to separate methods, but the card and note cite no filed selection criterion or shipped back-test, so frequency x severity ($343.8M, carry 350) and the trended severity ($356.5M, carry 350) survive as defensible answers. The note's ladder lists the trended severity as a dead rung, but the judge's back-test does not favour the golden's method. The pipeline's own CLAUDE.md rule says the method may stay open only where the design, a standard's general method or a filed selection criterion forces it; none does here.

Gate H line (judge): domain pass, layers pass, decisive_step analytical. The card's analyst_test and domain_test match the judge's read.

## Stump power (Gate F)
If the call were forced, the closure-share change would stump: the plain chain ladder lands on the wrong side of booked (a release). Not credited as valid until the method is forced, because a run filing 350 would be diverging on a defensible method choice.

## Findings, ranked
1. Main call is open between restated chain ladder (400) and frequency x severity or trended severity (350); no filed criterion or shipped back-test decides (Gates C and E).
2. The judge's own emergence back-test does not favour the golden method; any filed back-test must be run and shown to favour it, or the golden is the wrong one.
3. Ask 2 Q4 depends on an unfiled Treasury value-date convention (weak).
4. Rubric depth not verified here.

## Next action for the author
Re-root the determinism closure: file the estimand or a governing standard in the reserving basis (WHAT, not HOW) so the closure-restated development is the one general method, or file a selection criterion the shipped data decides (a back-test whose shipped result favours the golden), then confirm frequency x severity and trended severity land in the same $25M bucket. Optionally file the Treasury value-date convention in ledger_extract_notes_2026.md. Asks 1 and 3 need no change. Run /fix-determinism only if the main call, stump and figures can stay frozen; the judge's back-test result suggests the golden itself may need re-checking.
