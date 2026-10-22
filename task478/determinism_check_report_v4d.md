# determinism-check report, task478 (run r4d, re-judge with the yard stores file), 2026-10-22

## Verdict
NOT_DETERMINISTIC (supplementary ask 3). The thread could not reproduce ask 1 and the call from a literal reading and treats them as unverified, not passed. No SOLUTION_WRONG.
**Disposition:** SEND_BACK (the thread's wording: prior runs on ask 3 are void, a rerun is needed)
**Stumping type:** mechanism: method_or_model_selection (measurement-error calibration then dedup), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread isolation: one cold thread; derivation.md written before blocks.md was opened (order kept).

## Why
Ask 3 is not forced by the shipped text. The data notes define cold_mix_lb as "the cold mix pounds as entered" per task line, and no file says a multi-line order whose lines carry one figure and one finished time holds one entry for the order. The thread also read section_yard_stores_2027-03.csv as a competing record: the golden matches neither the line sum nor the yard net. Gate C fails on ask 3 (competing_defensible_answer, underspecified_objective on the pounds definition).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cold mix lb, golden | 401 1,705 ... 414 690 | reproduces only under "identical lines counted once" (149 lines in 50 orders collapsed) | only under an unfiled convention |
| Literal line sum | not claimed | 41,865 lb total (403 10,450; 411 8,150; 407 6,070; 413 3,140; 401 2,495) | n/a |
| Yard net_lb | not claimed | 28,500 lb (403 4,650; 411 3,650; 407 4,900; 413 1,750; 401 2,050) | n/a |
| Potholes 1,427; 7 of 14 designated | 1,427; seven | not reproduced from a literal reading: single-linkage on milepost at 0.01 to 0.05 mi gives 1,250 to 1,940 and moves 402, 404, 405, 406, 410 across 6.0; 401, 403, 407, 409, 413 always designated, 408, 412, 414 never | no (unverified) |
| Turnback | five SR 11 segments dropped | dropped; no cold patches fall on them | yes |

## Competing answers that survived
1. Cold mix: per-line sum, yard net, golden (three whole-number answers for 401, 403, 407, 411, 413). Shipped rule meant to close it: none filed.
2. Call: the thread found no filed dedup radius and did not itself apply the latency correction, so it could not confirm that the data force the golden's 10 ft join. It notes the data does carry that structure. Earlier cold threads (r4b, r4c) did reproduce 1,427 and the seven by calibrating latency on the covers; this thread's failure is a Gate A signal worth weighing, since the real reviewer may also fail to find the latency method from the text. The CLAUDE.md rule files the WHAT, not the HOW, so this is expected, but the main thread should weigh it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 plus manifest (17 in this bundle) | yes |
| Formats | 3 or more | csv, pdf, xlsx, json | yes |
| Large file | 25,000 rows | detections 103,162; traversals 62,800 | yes |
| Distractors | in metadata.json | declared earlier (3); not rechecked against the new bundle by the thread | not rechecked |
| License | recorded | export_manifest lacks a license column per the thread; metadata.json carries CC0 | check |
| Ask 3 single reading | one | three | no |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. It names latency calibration then dedup as the stump, as in the design note. The easy route (raw or fixed-radius clustering, or 69,367 raw detections) matches the declared easy path. Gate G line: PASS (no mismatch; distractors not the surface read).

## Stump power (Gate F)
Plausible genuine stump on ask 1. Ask 3 adds a hidden-convention trap that stumps for the wrong reason.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical.

## Findings, ranked
1. Cold-mix roll-up of multi-line orders unfiled; the yard stores file adds a third reading (net_lb) instead of closing the fork.
2. Call not reproduced by this thread without a filed latency step (unverified, not failed).
3. Minor: license field in export_manifest.

## Next action for the author
Remove or reconcile the yard stores record so it does not compete, and file one data-notes sentence on how a multi-line order's mix is counted; the coordinator has rebuilt without the yard file for r4e.
