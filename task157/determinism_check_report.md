# determinism-check report, task157, 2026-11-01 (pass 1)

## Verdict
DETERMINISTIC, with SOLUTION_WRONG flagged on one block (supplementary 3, lost kilometres, routes 6, 27, 41 and the Lot 2 total) pending the author's check. The flag is resolved by the main-thread finding below.
**Disposition:** FIX_NOW (a pin in the submission text; no figure, prompt or pack file moves). Re-judge once (pass 2 brief: /tmp/determinism-check-task157-r2/judge_brief.md).
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call (routes 27, 41, 58) is forced by the shipped record. Driver relief links at Merchant Row Interchange (3 and 4 minute gaps from a route 41 arrival to route 27 and route 58 departures) carry the 13 and 10 minute diversion delay; AVL lateness correlation across the join is 0.82 (route 27) and 0.88 (route 58), about 0.1 for route 33 (gaps of 26 minutes or more, which absorb the delay). Without the driver link only route 41 falls below 80, which is the easy wrong route-level answer. The punctuality asks reproduce all nine routes. Lost km did not reproduce on three routes in the judge's single pass (see ledger).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Autumn punctuality, nine routes (avl_timing_point_events.csv, UTC to Europe/London, re-sends dropped, clause 7.2 window) | 88.4, 87.7, 85.1, 82.8, 86.9, 84.0, 84.3, 84.6, 85.4 | same, all nine | Yes |
| Closure forecast: 41, 27, 58 below 80; 33 stays above | 27, 41, 58 | 41 about 46, 27 about 56, 58 about 56, 33 83.1, 22 86.8, others unchanged | Yes |
| Without driver link | n/a | only 41 below 80 | Confirms the fork is the driver link |
| Lost km routes 12, 14, 19, 22, 33, 58 | 281, 279, 264, 364, 269, 255 | identical | Yes |
| Lost km route 6 | 598 | 528 | No at pass 1 (see resolution) |
| Lost km route 27 | 412 | 391 | No at pass 1 |
| Lost km route 41 | 452 | 444 | No at pass 1 |
| Lost km Lot 2 | 3,174 (reliability 99.60) | 3,075 | No at pass 1; reliability consistent with 798,243 scheduled km |
| Boardings, all day stages 3 and 4 | 488 | 21,005 / 43 = 488.5 | Yes (total only) |
| Boardings direction and band split | 77/39/217 and 12/38/106 | not rebuilt (judge's crude split 313/176 against 333/156, sales not placed on AVL journeys) | Not independently reproduced |

## Competing answers that survived
None on the main call. Tested and rejected: route 41 only (record shows the driver link); 27, 41, 58 plus 33 (gap exceeds the delay, correlation about 0.1); route 19 falling on a seasonal fade (monthly file shows none).
Open at pass 1, closed by the finding below: the lost-km gap of 99 km. The judge's likely cause guess (police/emergency part losses) was wrong; the true cause is the midnight-spanning duty pieces.
Residual, not flipping the call: the knock-on rule is not stated in the prompt (it is found from the duty schedule and the record); the 30 minute join threshold in the solution text is not needed (26 or more already absorbs 13).

## Resolution of the FIX_NOW (main-thread finding, supplied by the coordinator; not re-derived by me)
The 99 km gap (route 6 598 vs 528, route 27 412 vs 391, route 41 452 vs 444) is reproduced exactly by four duty pieces relieved after midnight: route 6 duty 312 piece 1 (20:00 to 00:07, 30 Sep and 2 Dec, 9 journeys), route 27 duty 318 piece 2 (22:15 to 00:10, 3 Sep, 3 journeys), route 41 duty 584 piece 3 (21:28 to 00:02, 21 Nov, 1 journey). A reader taking the relief time on the booking day gets an empty piece. The golden is unchanged; step 5 of submission.md now names the handling ("a piece relieved after midnight running to that time the next morning"). Pass 2 re-judges the current pack (figure-neutral realism edits since the pass-1 brief; figures.json byte-identical). Whether the pack alone forces this reading is exactly what pass 2 must test.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | Yes |
| Formats | 3 or more | csv, pdf, xml, xlsx (4) | Yes |
| Large file | 25,000 rows or more | AVL 473,216 rows; ETM 95,234 | Yes |
| Distractors in metadata.json | 2 or more, no file name labels one | ring_road_crossing_atc_counts_2026.csv, street_works_permits_2027q1.csv; names neutral | Yes |
| Distractor relevance | unused by solution, weighable, ruled out by a shipped fact | judge confirms unused; the monthly series and Marsh Lane note are stated inputs, not distractors | Yes (not tested that a distractor answers a graded quantity) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both present in golden/ | Yes |
| Asks | multi-dimensional, unit and rounding stated | prompt states one decimal, whole km and boardings, two decimals reliability | Yes |
| Prompt shape and 25 or more criteria | identifiable, 25+ | not generated at this stage; shape is route-by-route grid (9 routes x 3 blocks plus direction x band) which supports 25+ | Not verified |
| No LLM tell, goldens real | read as real | not assessed here (leak and realism gates cover) | Not verified |
| Prompt length | under 1,000 characters, one paragraph | 855 characters | Yes |

## Gate G reconciliation
Judge: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note Gate G: identical on all four. The judge named no declared distractor as the surface read, and found no artifact that ranks or forecasts wrongly. Match. Gate H: judge `domain: pass, layers: pass, decisive_step: analytical` (unit of analysis: the route is the wrong unit for a delay people carry between routes), against the card's `stump_class: analytical`, with the analyst_test (route 41 alone) and domain_test. Match. The judge did not class the step analytical on the grounds of a textbook method; it reached the golden by modelling the data's crew structure.

## Stump power (Gate F)
The judge rates it good: the prompt never mentions drivers, a route-level or block-level forecast files 41 alone, and the discriminating evidence (relief gaps and cross-join lateness correlation) sits in the data. Risk the judge noted: the duty schedule is named in contract clause 7.8, so a thorough solver can find it; the heavy asks (UTC and re-sends, lost-km expansion through duty and timetable, ETM clock and midnight repairs) pull the top responses down. For the main thread to weigh against the design note's ladder: the judge reproduced the driver-link answer from the record in one pass.

## Findings, ranked
1. Lost-km block (routes 6, 27, 41, Lot 2) not reproduced at pass 1; closed in the submission by the midnight-piece pin. Needs pass 2 to confirm it is now forced by shipped text and files.
2. Boardings direction and band split not independently rebuilt by the judge (total reproduced). Pass 2 should attempt it, placing sales on AVL journeys.
3. Spec gates for 25+ criteria and golden realism not verified here.
4. The solution text's 30 minute join threshold is stricter than needed; harmless.

## Next action for the author
Spawn the pass-2 judge from /tmp/determinism-check-task157-r2/judge_brief.md (fresh unzip in the same folder), then re-invoke determinism-judge with its verdict.md; no second FIX_NOW re-judge is available after that.
