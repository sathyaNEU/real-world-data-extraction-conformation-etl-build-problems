# determinism-check report, task478 (run r4c, re-judge after the ask-3 repair), 2026-10-22

## Verdict
NOT_DETERMINISTIC (supplementary ask 3 only). The main call, ask 1, ask 2 and the chart are DETERMINISTIC. No SOLUTION_WRONG.
**Disposition:** FIX_NOW (one filed sentence on how cold_mix_lb is entered; the analytic surface stays byte-identical)
**Stumping type:** mechanism: method_or_model_selection (sensor-latency calibration then spatial dedup), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread isolation: one cold thread, no earlier report given; derivation.md written before blocks.md was opened (order kept). Its first-pass dedup (about 1,292 potholes) was coarse and is superseded by replicating the golden method.

## Why
The shipped dictionary says only "One row per task line ... cold_mix_lb is the cold mix pounds as entered", so the literal execution sums every line, which differs from the golden in every section. The golden counts an order whose lines share one figure and one finished time once. The data favour that strongly (all 50 multi-line single-finish-time orders carry identical figures of 125 to 300 lb against 20 to 110 on single-line orders) but no shipped text says so. Gate C/E competing_defensible_answer on ask 3. The main call and the 14 rates are forced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Roadway lane-miles | 2,428.9 | 2,428.9 (turnback removes 12.374, all section 407) | yes |
| Unit latency range | 0.47 to 1.74 s | 0.473 to 1.743 s, 34 units | yes |
| Distinct potholes | 1,427 | 1,427 for any join gap 8 to 20 ft (1,432 at 5, 1,418 at 25) | yes |
| Rates per ten lane-miles | 8,7,8,4,4,7,9,3,8,4,5,3,8,2 | 8.14, 6.90, 8.00, 3.71, 4.06, 7.09, 9.13, 2.96, 8.15, 3.98, 4.95, 3.14, 7.93, 2.03 | yes |
| Designated | 401,402,403,406,407,409,413 | same seven (lowest margin 402 at 6.90, 411 at 4.95) | yes |
| Cold mix lb, all 14 | 1,705 / 1,255 / 4,135 / 625 / 1,155 / 1,485 / 4,445 / 615 / 2,150 / 395 / 3,335 / 1,115 / 1,420 / 690 | reproduces under reading B only | only under an unfiled convention |

## Competing answers that survived
Cold-mix entry (492 lines, 334 orders). Reading A, literal sum of every line: 2495, 1855, 10450, 935, 1405, 1615, 6070, 875, 2275, 520, 8150, 1255, 3140, 825 (sections 401 to 414). Reading B (golden): order's one entry counted once when all lines carry one figure and one finish time. They differ by 2x or more in 403, 411 and 413. Shipped rule meant to close it: none in a filed document.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, pdf, xlsx, json | yes |
| Large file | 25,000 rows | 103,162 and 62,800 | yes |
| Distractors | 2 or more, in metadata.json, not by file name | 3, not labelled by name; thread found winter operations, pavement condition, sessions present | yes |
| Deliverables | 1 to 3 | 2 | yes |
| Asks | multi-dimensional, unit and rounding | 3 asks x 14 plus chart, whole numbers | yes |
| Rubric 25+ | yes | about 45 items (my estimate) | yes |
| Reads real | yes | no authoring leakage found | yes |
| Ask 3 single reading | one | two | no |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no (r4b said yes; the thread notes no reported figure is wrong). Design note's stump: directional instrument latency (estimation_fit); easy route = cluster at one distance. Match: the thread's easy route gives about 1,267 potholes and drops Fenwick Gap and Kestrelton. The declared distractors are not the surface read. Gate G line: PASS.

## Stump power (Gate F)
High. Raw or direction-paired clustering gives 1,267 to 1,292 potholes and misses two of the seven; only the cover-calibrated correction is stable across gap sizes.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the design note.

## Findings, ranked
1. Cold-mix entry convention is inferred from a repeated-value pattern, not filed (ask 3).
2. Minor: sole_data_defect differs between r4b (yes) and r4c (no); no consequence.

## Next action for the author
File one sentence in tamsett_pilot_data_dictionary.pdf (or the program document) saying a work order closed together carries its one entry repeated on each line, so counted once; or restate ask 3's wording. Leave the call, rates and chart frozen. The coordinator reports r4d is the one re-judge after this FIX_NOW.
