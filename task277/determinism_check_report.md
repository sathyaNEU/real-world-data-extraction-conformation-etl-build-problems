# determinism-check report, task277, 2026-11-02 (covers pass 1 and pass 2)

## Verdict
**Pass 2 (final cut, target.zip 2a534d35): DETERMINISTIC**, no SOLUTION_WRONG.
**Disposition:** APPROVE (pass 1 on the first cut: DETERMINISTIC, FIX_NOW; fixed in the generator in one pass and re-judged once).
**Stumping type:** mechanism: forecasting (standardisation by pick type under a changed case mix, plus etl_conformance for the claims ask), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Verdict files: /tmp/determinism-check-task277-20261102T022215/verdict.md (pass 1), /tmp/determinism-check-task277-20261102T025132/verdict.md (pass 2).

## Why
The 2026 record rebuilds from the two WMS exports (CSV local time, parquet UTC, Amsterdam pick date, zero-confirmed lines dropped, SHORT/OVER/WRONG_ITEM only) and matches the close-out month by month. Failure rate by the pick a line calls for reproduces. The PCN and item master put Daily on inners of four from February, so about two thirds of Daily retail lines become whole-inner-plus-loose picks. The plan gives 100 and 110 failing lines, 99.7 per cent in both months, against a break-even of about 63 and 70 lines. "Not held" holds under every reasonable variant.

Pass 1 findings, all fixed before pass 2: (1) close-out December note said 9 per cent, its own table gives 6.3 per cent; (2) rate pooling was not closed, so sub-pooled rates moved the second decimal and the nearest-5 count; the generator now makes the pooled, channel, range and inner-size rates converge and the graded forecast moved to the precision the data carry (nearest 10, one decimal); (3) two Daily new-pack item master rows had valid_to before valid_from, removed.

## Recomputation ledger (pass 2, final cut)
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2026 lines / failing lines | 414,766 / 526 | 414,766 / 526 (all exceptions matched) | yes |
| Whole-inner failure rate | 0.061 % (109/177,273) | 0.0615 % | yes |
| Loose below one inner | 0.111 % (245/221,100) | 0.1108 % | yes |
| Whole plus loose | 1.049 % (172/16,393) | 1.0492 % | yes |
| Feb 2027 planned / failing / accuracy | 31,460 / 100 / 99.7 | 31,460 / 100.0 / 99.68 | yes |
| Mar 2027 planned / failing / accuracy | 35,170 / 110 / 99.7 | 35,170 / 112.1 / 99.68 | yes (rounds to 110) |
| Ask 3, 16 customer-quarter cells (total 7,051) | as in submission | all 16 identical | yes |
| PNG series | 2026 months, 99.7 forecasts, 99.80 target | consistent | yes |

## Competing answers that survived
- None that moves the call or a graded figure. Robustness: class x channel, Feb/Mar-only, range x class, all-year mix and discontinued-SKU-dropped variants all give 100 / 110 and 99.7. Only H2-only class rates (102.6 / 115.0) touch a rounding edge, and that is not a reasonable reading of "the record".
- Wrong routes, correctly separated: range x channel cell rate gives about 38 / 44 lines, 99.88, "held"; overall rate 40 / 45; opened-inner rate on Daily also keeps the target.
- Advisory, ask 3 only (judge: data-semantics ask, allowed, not a determinism failure): the store order unit and the portal's pre-July quantity convention are in no shipped file but are unique from the data (EDI/portal pair ratios and gcd of retail ordered quantities agree; any break date in the empty 10 to 20 July portal window gives the same figures). 28 accepted Vlietmarkt `HV...` claims match no delivery and are excluded by "quarter of delivery" and "2026 retail deliveries" (including them would move Vlietmarkt by about 30 units).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 4 (csv, parquet, pdf, xlsx) | yes |
| Large file | 25,000 or more rows | 242,567-row parquet, 183k-row CSV | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | cycle_counts_2026.csv, bms_zone_temperatures_2026.csv named; file names carry no label; lms_shifts and wms_users are also unused | yes |
| Distractors unused yet weighable | yes | unused by the solution; nothing in them answers a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | forecast by month, claims by customer x quarter (16 cells); rounding sentence in the prompt | yes |
| Prompt shape and 25 or more criteria | shape identified, 25+ | shape 02 in metadata.json; rubric is generated and not shipped, graded cells (6 forecast figures, 16 claim cells, components, chart) exceed 25 by count, not verified by me | yes (by count) |
| Not LLM generated, goldens read as work products | yes | judge saw no authoring language; real-looking exports and Dutch labels | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (read after return): Layer 2 is estimation_fit, the error probability belongs to the pick a line calls for and the forward change moves Daily store lines into the pick that fails ten times as often. Match. The thread did not name the declared distractors as the surface read, and it named the same wrong routes the note and prompt anticipate. The close-out and 2026 accuracies are correct, so no shipped artifact ranks the candidates wrongly: Gate G pass.

Gate H line: `domain: pass`, `layers: pass`, `decisive_step: analytical`. The judge reached the golden by projecting a pick-type failure gradient through a mix shift that the data had to settle (which picks the Daily lines become), not by executing a stated method, so I do not read this as a landable textbook route.

## Stump power (Gate F)
Strong on paper. The record, close-out and Schedule 3 all show compliance, and the easy routes (cell rate, trailing rate, opened-inner rate) land on about 38 to 45 failing lines, 99.88, "held". Only carrying the Daily inner change through pick type reaches 100 / 110. The PCN and item master state the change but not its consequence. Main thread weighs it against the design note's ladder.

## Findings, ranked
1. None open on the main call.
2. Ask 3 watch item: store order unit and portal quantity convention are inferred, not filed (advisory, left as is by the author).
3. Closed in pass 1 to 2: close-out December percentage, pooling convergence and rounding precision, invalid item master rows.
4. Not checked by me: rubric criterion count (rubric is not shipped).

## Next action for the author
Proceed to SHIP with the pass-2 cut. Ask 3 is the only residual risk, and the author has chosen not to file the store order unit.
