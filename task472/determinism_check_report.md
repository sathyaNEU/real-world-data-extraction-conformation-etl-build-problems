# determinism-check report, task472, 2026-10-20

Judged pack: the fresh unzip of target.zip at /tmp/determinism-check-task472-1792496898/target/ (the thread's view). The main session rebuilt task472/target afterwards; this report does not cover that rebuild.

## Verdict
DETERMINISTIC (main call and every golden figure reproduce); asks 5 and 6 carry two unpinned conventions.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: binding_constraint (with etl_conformance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Rules 3.5 and 3.6, the Harbor Master's Directions (3.4, 8.1, 9.2, 9.3), the tide file and the pilot record pin one counterfactual sailing process. All 784 actual sailings equal the first permitted time an hour or more after notice, so the data fixes the regime. The 331-hour lead (37 percent of the winner) survives DST handling, per-call rounding, either overlap source and boundary inclusion. Two ask conventions are stated nowhere in the shipped files (see forks).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Large FY2026 calls | 784 | 784 | yes |
| Millrace / Halyard / Pine Neck / Ore Dock / Gannet Point / Saltworks | 887 / 556 / 449 / 423 / 395 / 257 | 886.76 / 555.70 / 448.76 / 422.76 / 395.28 / 257.19 | yes |
| Lead | 331 | 331 | yes |
| Ask 5 breakdown hours (ORD, PNC, GNP, HLY, SLT, MRW) | 1,271 / 968 / 499 / 1,118 / 701 / 1,715 | 1270.67 / 968.23 / 499.32 / 1117.82 / 700.85 / 1714.78 | yes |
| Ask 6 labor hours (same order) | 2,759 / 3,097 / 1,661 / 2,935 / 2,169 / 3,554 | 2758.75 / 3097.25 / 1660.75 / 2934.75 / 2168.75 / 3553.75 | yes |

## Competing answers that survived
1. Ask 5, DMG orders: 13 DMG orders carry downtime code BRKDWN. Counting them gives ORD 1278, PNC 985, GNP 508, HLY 1132, SLT 706, MRW 1727. The dictionary defines BD and DMG as distinct and says type at the pull is what the extract shows, which supports the golden. The prompt never says "work order type". Margin: low, shifts exceed rounding.
2. Ask 6, timesheet dedup key: 12 in-year timesheet days share an order and day with a ledger CONTRACT row but not its hours. The golden adds them. Matching on "order and day" would move every graded figure (ORD 39, PNC 17.75, GNP 15, HLY 11, MRW 6.25, SLT 6 hours). No shipped file states the key; it appears only in the solution step. Open fork, underspecified_objective, unless pinned.
3. Main call, shifting the actual sailing back by 0.2 x cargo work and snapping gives Halyard (465). Not licensed (3.4 sets the sailing from the notice, and the record confirms it). Rule 8.2 (two 1,250 ft vessels) cannot be executed and is not operative in the record. Residual risk: low.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / big file | 10+ / 3+ / 25,000 rows | 19 / 5 (csv, xlsx, json, pdf, txt) / 80,059 rows (tos_crane_activity) | yes |
| Distractors | 2+ in metadata.json, none named by file name | 3 named (ais_berth_segments, cmms_yard_equipment_work_orders, berth_windows_fy2027); file names do not label them | yes |
| Distractors relevant but unused, ruled out by a shipped fact | yes | thread found them usable and unused; each has a stated reason in metadata.json | yes |
| Deliverables | 1 to 3, all in golden | 2, both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | six-terminal figures; "two decimals" and "whole hours" in the prompt | yes |
| Prompt shape, 25+ criteria | 25+ | other, 28 per the design note (not independently counted) | yes (note) |
| Not LLM-looking / goldens realistic | yes | thread found clean provenance and real operational mess; golden realism not checked by me | yes (thread) |

## Gate G reconciliation
Thread: mechanism binding_constraint, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: strategy binding_constraint, Layer 2 family allocation_constraints, no planted defect. Match. The declared distractors (AIS, yard equipment, 2027 berth windows) are not named as the surface read carrying the task. Gate G line: binding_constraint / analytical_non_defect / surface_read no / sole_data_defect no, matches the design.

Gate H: thread says domain pass, layers pass, decisive_step analytical. Design note: domain_test pass, Layer 1 and Layer 2 declared, decisive step analytical (counterfactual replay of each sailing from earlier readiness). Match. Gate H line: domain pass, layers pass, decisive_step analytical.

## Stump power (Gate F)
Plausible wrong answers: 0.2 x cargo work gives Saltworks (991); one gate only gives Saltworks (1243) or Pine Neck (922 over Millrace 887); no gates gives Saltworks. The thread records a borderline: once the gating is recognised, executing it is rule application, so the stump rests on recognising that the allocated sailing binds the stay. Note for the main thread: the rules file the WHAT and directions 3.4 and the record show the sailing is the first permitted time after notice, so a strong solver who builds the notice-to-sailing replay lands the call. Weigh this with the scored readers' result. The asks add independent traps (relocated cranes, February double count, timesheet dedup).

## Findings, ranked
1. Ask 6 timesheet dedup key is unstated in the files; dropping on order-and-day moves every graded figure. Pin it.
2. Ask 5 "breakdown" is not tied to work order type BD at the pull in the prompt or dictionary; DMG orders with BRKDWN code shift every figure. Pin it.
3. Stump rests on recognising the replay (borderline analytical, see Stump power).
4. This verdict covers the pre-rebuild pack; the rebuilt pack is unjudged.

## Next action for the author
Add two pins to data_dictionary.txt (or the prompt): a breakdown is a work order whose WORKTYPE at the pull is BD, and a maker timesheet day is already keyed only where the ledger holds a CONTRACT row on the same order, day and hours. File the WHAT only; the main call, ladder and golden figures stay frozen.
