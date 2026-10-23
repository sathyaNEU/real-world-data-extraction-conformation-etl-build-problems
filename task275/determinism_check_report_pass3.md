# determinism-check report (pass 3), task275, 2026-10-23

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Bundle judged: target.zip md5 04c5972e1d920462c1150dd5d92fdcbb, fresh unzip at /tmp/determinism-check-task275-r3/target/. One thread; verdict at /tmp/determinism-check-task275-r3/verdict.md. Passes 1 and 2 are kept as history. This pass covers the dateless equipment record (vms_transponders.csv) and the regenerated steps 6 to 8.

## Why
The terms file the estimand (every trip begun in 2025, landed plus returned, live weight, register segment). Unobserved discards are not recorded, so the shares are reachable only by raising the observer sample ground by ground, which the data force: marketable kg an hour match between observed and unobserved trips per segment and ground, unobserved trips declare 5 to 20 times less BMS an hour, and observed BT trips fished 39 per cent of hours on WC14/15 against 69 per cent unobserved. Shares: TR1 12.8, TR2 12.0, NEP 14.2, BT 11.8, SN 7.7, GN 7.1, LL 4.8, POT 6.3, giving 13/12/14/12/8/7/5/6. Bootstrap bands sit wholly above 10 for the four (BT 11.4 to 12.4) and below for the rest.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Trips / observed | 12,000 / 856 | 12,000; 856 matched one-to-one (nearest trip within 2.3 h, next at least 45 h) | yes |
| Observed BMS kg/h TR1, TR2, NEP, BT, SN | 25.28, 9.97, 1.44, 4.66, 6.81 | same | yes |
| BT WC14/15 hours share | 39 vs 69 per cent | confirmed in the judge's evidence on ground imbalance | yes |
| Shares, whole per cent | 13, 12, 14, 12, 8, 7, 5, 6 | 12.8, 12.0, 14.2, 11.8, 7.7, 7.1, 4.8, 6.3 | yes |
| Ask 2 kStg | 12,012.6 / 7,159.1 / 8,031.6 / 9,687.6 / 3,561.4 / 1,725.9 / 694.5 / 2,338.2 | identical; 715 lines dropped, match ratio gap clean (at most 3 per cent vs at least 28 per cent) | yes |
| Ask 3 days | 2,236 / 3,032 / 3,517 / 2,128 / 1,737 / 2,419 / 1,362 / 2,593 | identical with the 14 shared terminals split by previous/current chains (no report between windows) | yes |

## Competing answers that survived
- Ask 2, grade term of the lot key: step 7's text names vessel, landing date, species and grade, so grade is shipped in the solution wording; the judge saw it as absent from any shipped data text. Without grade, 6 more lines drop (11 pairs differ in grade) and SN 3,561.2, TR1 12,011.6, TR2 7,159.0 move at 1 dp. Low risk; a different grade is a different lot.
- Main call forks (pooled raising BT 8.5; DIS only NEP 12.0; not subtracting BMS pushes GN to 10.4) are analytical wrong routes the files refute.
- Ask 3 by UTC dates or terminal labels as given (BT 2,152 / 1,932) is closed by the terms and the equipment record.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 17 / csv x12, pdf x3, xlsx, txt | yes |
| Large file | 25,000 rows | vms 197,077; sales 99,002 | yes |
| Distractors | 2+ in metadata.json, none named by file | quota_uptake_2025.xlsx, gear_specifications_2025.csv; unused | yes |
| Deliverables | 1 to 3, all in golden | 2, in golden/ | yes |
| Asks | unit and rounding stated | stated | yes |
| 25+ criteria | yes | by count yes; generated rubric not seen | yes (by count) |
| Not LLM-flavoured | yes | judge: PO extracts with real mess; README an in-fiction index | yes |

## Gate G reconciliation
Judge: method_or_model_selection / analytical_non_defect / surface_read no / sole_data_defect no. Matches the design note and passes 1 and 2 (pass 2 used the label statistical_rigor for the same mechanism). Declared distractors do not carry the task. Passes.

## Gate H reconciliation
Judge: domain pass, layers pass, decisive_step analytical. Matches the card and the note's Three rules. No mismatch.

## Stump power (Gate F)
Judge: good. The unrepresentative observer sample is what stumps, and no shipped file documents the path. Same standing caveat as before: stratified raising is field-standard, so weigh with the scored readers (both missed the call in round 2).

## Findings, ranked
1. None blocking.
2. Optional, closed by the coordinator after the verdict: the grade term of ask 2's key. The coordinator reports a generator change (private quay sales kept more than 5 per cent off every market lot, so the key finds the same lines with or without grade, asserted) and a change to lawful discards varying by ground and season with segment year totals unchanged. Those generator changes post-date this judgment and were not judged by this pass; the md5 above is the bundle judged. At the time of writing target.zip still has that md5.

## Next action for the author
Ship per the pipeline; record in the build record that the post-verdict generator fixes were not re-judged, and confirm the final target.zip rebuild reproduces every graded figure.
