# determinism-check report, task464, 2026-10-28 (pass 8)

Thread judged target.zip md5 491993a850683ec6a7096285dc1d16a9 with the repaired prompt and submission blocks (placement, runner-up, populations, R1, R2). Raw verdict: /tmp/determinism-check-task464-1793183931/verdict.md.
After the thread returned, the main session applied its two optional pins: the board brief now ranks the practices on figures before rounding, and the specification's R2 numerator says "at any practice". Both close a reading toward the golden and move no graded figure. The pack was rebuilt (target.zip md5 b4b0fc88223e45b9a5097174052794cd); only the two PDFs' wording differs from the judged bundle. No new thread was run, so the final PDFs were not read by a judge.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The brief fixes the population and window; the data supply the 12% non-re-authorisation, a stop hazard near 0.7% per 28 days, about 2.1% a year deregistration and each patient's repeat structure. Marrick House leads every variant (stop hazard 0 to 1%, failure 10 to 14%, interval by record or supply) because 1,232 of its 1,648 patients sit on six-issue 56-day repeats authorised Feb/Mar 2026. All 28 supplementary figures reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Population by practice | 1017/829/877/1961/1648/1192/1124 (8,648) | same, both systems via cvd_product_lookup, register, issues | yes |
| Marrick on 6-issue 56-day repeat | 1,232 of 1,648 | 1,232 (authorisations A/B); no other practice has such a block (Wyndhollow 195, Cobbet 1,173 six-issue 28-day spread, Fennbridge 13-issue) | yes |
| CC1 lapse | 12% | 87.99% re-authorised of 13,590 | yes |
| R1 | 81.0, 80.3, 81.9, 77.8, 79.9, 75.8, 92.9 | same (694/523/587/1432/1123/669/750) | yes, all 7 |
| R2 | 82, 83, 83, 71, 84, 58, 55 | same (11/6/12/28/19/12/11) | yes, all 7 |
| Top two | Marrick, Cobbet | Marrick about 171; Cobbet 113 to 118; Fennbridge 102 to 110 | yes |

## Competing answers that survived
- Runner-up: Cobbet over Fennbridge holds in every variant by 6 to 18 units; with practice-specific hazards about 113 vs 107, both rounding to 110. The judge flagged it as thin but clean and holding on the unrounded figure; the unrounded-figure pin was applied after the judge returned and closes it.
- R2 attribution: "any practice" is the literal reading; start-practice-only would move Larkspur to 75 and Fennbridge to 68. The pin "at any practice" now closes it.
- Acute-only patients (100; 22 Marrick) are unspecified but move under 3 units, no order change.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 14 / csv, jsonl, xlsx, pdf | yes |
| Large file | 25,000 rows | 300k rows (A), 300k lines (B) | yes |
| Distractors | 2+ in metadata, unlabelled in names | qof_cvd_achievement and dispensed_items_cvd named; pcn profiles xlsx also unused; none carries the call | yes |
| Deliverables | 1 to 3, all in golden | 2 | yes |
| Asks | multi-dimensional, unit and rounding | 7 populations, placement, runner-up, 14 return percentages with decimals stated | yes |
| Prompt shape / 25 criteria | identifiable, 25+ | shape 01; rubric not checkable here | not verified |
| Realism | no LLM tells | judge: none, no temporal leak | yes |

## Gate G reconciliation
Judge: forecasting / analytical_non_defect / no / no. Card and design note: method_or_model_selection, stump_class analytical, strategy time_semantics, decisive step the clock a forward estimate runs on. Same mechanism, no mismatch. Judge's easy routes (largest list, point-in-time count of statin patients) are not the declared distractors (QOF, dispensed items); no distractor carries the task. Gate G: PASS.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the design note's Three rules. R1/R2 are rule application but are asks, free of rule 3.

## Stump power (Gate F)
Moderate per the judge. A naive count of repeats ending before March also reaches Marrick (1,295 / 838 / 522 / 509), and the Wyndhollow six-issue block (195) is a partial distractor. Since the prompt no longer asks for the figure, the call is landable by a rough pipeline count (stumping 1.3); the runner-up and the R1/R2 reconstructions carry the difficulty. Main thread to weigh against the design note's ladder.

## Findings, ranked
1. Judged bundle differs from the final zip in the two PDFs' wording (pins applied after the verdict); not re-read by a judge.
2. Runner-up margin thin on rounded figures (closed by the unrounded pin).
3. Naive run-out count lands the call (stump power).

## Next action for the author
Proceed to stage 5 with target.zip b4b0fc88223e45b9a5097174052794cd; no re-judge needed unless the PDF edits are doubted.
