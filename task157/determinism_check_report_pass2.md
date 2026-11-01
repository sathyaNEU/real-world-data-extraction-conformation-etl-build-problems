# determinism-check report, task157, 2026-11-01 (pass 2, re-judge of the pass-1 FIX_NOW)

## Verdict
DETERMINISTIC. No SOLUTION_WRONG.
**Disposition:** APPROVE.
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call (routes 27, 41, 58) is forced by the AVL record, the traffic management plan's journey-time model (the Marsh Lane close-out shows plan and AVL within half a minute) and the duty schedule. The judge's own simulation puts 41, 27 and 58 at about 65, 72 and 72 per cent and every other route at or near its autumn level (lowest, route 19, 82.8). The 27/58 result rests on crew interworking at Merchant Row (3 and 4 minute joins), which the baseline AVL shows is real. Route 41 alone and 41 plus 33 are the easy routes the files rule out. The pass-1 lost-km gap is closed: all nine routes and the Lot 2 total reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Autumn punctuality (AVL, UTC to Europe/London, 1,189 re-sends dropped, ARR excluded, -60 s to +359 s) | 88.4, 87.7, 85.1, 82.8, 86.9, 84.0, 84.3, 84.6, 85.4 | identical, all nine | Yes |
| Lost km by route (6, 12, 14, 19, 22, 27, 33, 41, 58) | 598, 281, 279, 264, 364, 412, 269, 452, 255 | identical | Yes |
| Lost km Lot 2 | 3,174 | 3,174 | Yes |
| Reliability by route and Lot 2 (scheduled km 125,430 / 87,493 / 91,234 / 67,003 / 66,297 / 94,757 / 75,370 / 104,845 / 85,815) | 99.52, 99.68, 99.69, 99.61, 99.45, 99.57, 99.64, 99.57, 99.70; Lot 2 99.60 | identical | Yes (unchanged whether or not RW is excused) |
| Closure forecast | 27, 41, 58 below; others above | 27 72.9, 41 65.1, 58 72.0 below; 6 86.1, 12 85.2, 14 85.1, 19 82.8, 22 86.9, 33 84.3 above | Yes |
| Duty joins | 41 to 27 at 3 min, 41 to 58 at 4 min, 41 to 33 at 26 to 38 min | 85 of 85 joins resolved uniquely; same gaps | Yes |
| Boardings, all day | 488 | 488.5 | Yes |
| Towards city AM / other / PM | 77 / 217 / 39 | 76.6 / 215.8 / 39.4 | Yes (within 0.6 per cent of AVL-lost sales) |
| Towards Ravensholme AM / other / PM | 12 / 106 / 38 | 12.0 / 106.6 / 38.1 | Yes (same) |

Sensitivity on the call: minimum dwell 0 gives 27 at 75.4 and 58 at 75.1; crew minimum 0 or 2 gives 74.2 and 70.3; TMP delays scaled to 0.8 gives 76.0 and 76.9; no bus cascade gives 77.9 and 77.0. Only stacking no cascade, zero dwell and 0.8 scale lifts route 58 to 80.3, which the judge called implausible.

## Competing answers that survived
Main call: none. Route 41 alone (block-only propagation, 27 at 84.0 and 58 at 85.4) and 41 plus 33 (33 stays 84.3 on a 26 minute or longer stand) are refuted. Route 19 watch point: monthly AVL punctuality 84.0, 84.2, 81.0 and 78.5 (1 to 6 December); a solver forecasting from the last four weeks only lands near 80.1, on the line but not below it; the published monthly series holds 82.3 to 84.2 since January 2025. Margin 2.8 points, thin but clean.
Ask 4 fork (judge, supplementary only): band basis (sale time against the journey's scheduled start, 67 / 226 / 39 and 13 / 105 / 39 under the second) and direction (the ETM `journey_direction` field disagrees with AVL direction on about 13 per cent of sales; using it gives 65 / 209 / 39 and 20 / 116 / 40). No shipped text then said which governs.
Resolution (main thread): the prompt now files the WHAT in the asking sentence, "by the direction the bus was travelling and the traffic management plan's time band each boarding fell in". The golden is unchanged (it bands by the boarding's time and takes direction from the bus's AVL journey, which the judge's rebuild matched). This edit came after the pass-2 judge's single pass and was not re-judged; one pass only. It files population, unit and basis, not a method.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | Yes |
| Formats | 3 or more | csv, pdf, xlsx, xml | Yes |
| Large file | 25,000 rows or more | AVL 473,216 rows | Yes |
| Distractors in metadata.json | 2 or more, no file name labels one | ring_road_crossing_atc_counts_2026.csv, street_works_permits_2027q1.csv | Yes |
| Distractor relevance | unused by solution, weighable | judge lists Marsh Lane close-out, monthly file, ATC counts, permits, cause codes as usable decoys, all unused by the solution; none answers a graded quantity | Yes |
| Deliverables | 1 to 3, in golden | 2 (xlsx, svg) | Yes |
| Asks | multi-dimensional, unit and rounding stated | stated in prompt | Yes |
| Prompt | one paragraph, under 1,000 characters | 900 characters after the edit, one paragraph | Yes |
| 25 or more criteria; LLM tells; golden realism | as specified | not assessed in this thread | Not verified |

## Gate G reconciliation
Judge: forecasting / analytical_non_defect / no / no; passes Gate G. Matches the design note's Gate G (same four values) and the card's `stump_class: analytical`. The judge named no declared distractor as the surface read, and the Route 19 weak November and the Ring Road +2 minutes are described as decoys leaning the other way, not as carrying the task. Gate H: `domain: pass, layers: pass, decisive_step: analytical`; matches the card's analyst_test (route 41 alone) and domain_test. The judge's caveat, that once the crew link is found the simulation is mechanical, places the stump in finding that the link governs, which is the analysis and not a stated rule.

## Stump power (Gate F)
Moderate to good. The delay reaches routes 27 and 58 through the driver rota, not any shared bus or route, so block-level and route-level forecasts file 41 alone. The duty schedule must be joined to the timetable by board and time, so the risk of being too easy is low. For the main thread to weigh against the ladder: the judge reproduced the golden from the record without any filed method, and its forecast margins (27 and 58 at about 72, not near 80) are wide, so a solver who finds the link lands the call robustly.

## Findings, ranked
1. None blocking. Every graded figure reproduces.
2. Ask 4 band basis and direction fork, closed by the prompt edit above; not re-judged.
3. The unverified items in the spec table above.

## Next action for the author
Run `voice-check.py` on the edited prompt (900 characters, one paragraph), then proceed to ship with the leak reader's verdict.
