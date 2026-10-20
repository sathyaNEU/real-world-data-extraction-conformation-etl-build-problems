# determinism-check report, task471, 2026-10-20 (run v3r1, architecture 3, first judge pass)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread (sonnet, medium, scratch path only) reproduced the six qualifying counties from the shipped files. The call holds under every valid dual-frame estimator it ran: inclusion-probability weights, Hartley at theta 0 to 1, and post-stratified by list membership. Lowest qualifier is Brannock (304; range 293 to 308). Highest non-qualifier is Ivyridge (199; Dunmere 223 under Hartley theta 0). All 16 per-county rows of ask 2 and the chart in ask 3 reproduce. The retest date basis is closed by WWA-2027-01 4.2 and the design report. Border-ZIP attribution is closed by "its wells the survey first tested".

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Permit list | 32,933 | 32,933, all 16 counties match Table 2 | yes |
| Parcel list | 35,440 | 35,440, all 16 match | yes |
| Rates | 8.3% (2,740), 4.0% (1,407) | same | yes |
| Tested / on both lists | 3,996 / 3,002 | same | yes |
| Survey population | 42,598 | 42,598, 16 county counts identical | yes |
| Tested wells above 10 mg/L | 313 | 313 | yes |
| Counties at or above 250 | 6 | 6 (Brannock 304 lowest, Ivyridge 199 highest below) | yes |
| Retests | 232 retested, 195 still above | same, 16 rows match | yes |

## Competing answers that survived
None. Closed forks: retest date basis (4.2), county attribution of border-ZIP requests, superseded lab results, duplicate permit numbers across counties. Residual risk is only a solver who ignores 4.2.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 12 files; csv, pdf, xlsx; permits csv 41,116 rows, assessor xlsx 74,518 rows | yes |
| Distractors in metadata.json, none labelled by file name | 2+ | fact sheet pdf and certified labs csv named in metadata.json (a "distractor" is not in either file name). | yes |
| Distractors unused, relevant, one that answers a graded quantity ruled out by a shipped fact | | Neither answers a graded quantity. The fact sheet's 4.4 factor does not change the classification (no Kinsale value between 44.0 and 44.27). The labs roster is the weaker one: weighable but thin. | yes (weak, non-blocking) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | | 16-row table of 4 figures each, whole numbers stated | yes |
| Prompt shape and rubric | shape identified, 25+ criteria | shape 10 scorecard; design note lists the call and count, 16 verdicts, 16 counts, 32 retest figures, so over 25 | yes |
| Reads as real, no LLM tell | | the judge saw no authoring leakage or benchmark language; no em dashes found in prompt.txt or submission.md | yes |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: Gate G method_or_model_selection, `stump_class: analytical`. They match. The declared distractors are not the surface read carrying the task. The card has no separate stumping_family, surface or defect fields to compare (all None), so the match rests on the design note's text.

Gate H: domain pass, layers pass, decisive_step analytical. This matches the card's `analyst_test` and `domain_test` and the note's `## Three rules`.

One count differs. The judge's rate-of-drawing-list route gave 11 or 12 counties, while the note and submission say ten. The route is under-specified across variants; the pooled route (three) and the wrong direction match. This does not affect the verdict, but the 10 in submission.md and the card is one variant of several.

## Stump power (Gate F)
The decisive step is choosing the dual-frame estimator, with the filed estimand but no filed method. The easy routes file 3 (pooled share) or 10 to 12 (drawing-list rate). Hartley and inclusion-probability are the field's textbook methods, so a strong solver who knows survey design lands the call. The design note and the judge both say partial failure on the asks is likely from the linkage and retest matching. The main thread should weigh this with the scored readers' result.

## Findings, ranked
1. Non-blocking: the "ten" wrong answer is one of several variants (the judge got 11 or 12). Consider wording that does not depend on the exact count.
2. Non-blocking: the certified labs roster is a thin distractor.
3. Optional: the date basis for "retested by June 30" rests on WWA-2027-01 4.2 alone.

## Next action for the author
Proceed to ship stage 5; no generator change is required. Optionally reword the "ten" count in submission.md to "about ten" or match it to the judge's variant.
