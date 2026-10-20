# determinism-check report, task472 (pass 2), 2026-10-20

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (Ask B only; the main call and Ask A are forced)
**Stumping type:** mechanism: other (counterfactual replay of the realised sailing, validated against actual sailings), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Scope: this judges what the thread saw (the rebuilt target.zip and submission.md). The main session has since applied fixes in the generator; those are not judged here.

## Why
The 784 large FY2026 calls were rebuilt from the bundle. Every pilot sailing equals the first time at least 1 h after the notice that Harbor Master 8.1 (1,250 ft or more, 0600 to 2000 ET) and 9.2/9.3 (draft 41 ft or more, Salt Point tide window shifted by passage time) permit (784 of 784 to the minute). Replaying each call from a notice moved forward by a fifth of its cargo work gives Millrace 886.76, Halyard 555.70, Pine Neck 448.76, Ore Dock 422.76, Gannet Point 395.28, Saltworks 256.99. The lead is 331.06 h and matches the golden (887 / 556 / 449 / 423 / 395 / 257; 331). Ask A reproduces. Ask B has three unpinned readings that move figures by tens of hours (below).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Large FY2026 calls | 784 | 784 (PNC 176, SLT 156, ORD 141, HLY 117, MRW 103, GNP 91) | yes |
| Berth hours saved MRW/HLY/PNC/ORD/GNP/SLT | 887/556/449/423/395/257 | 886.76/555.70/448.76/422.76/395.28/256.99 | yes |
| Lead over runner-up | 331 | 331.06 | yes |
| Ask A ORD/PNC/GNP/HLY/SLT/MRW | 1,273/972/501/1,121/704/1,715 | 1,272.7/971.7/501.2/1,120.8/703.8/1,715.3 (all at least 0.2 from a .5 edge) | yes |
| Ask B ORD/PNC/GNP/HLY/SLT/MRW | 2,963/3,042/1,711/2,931/2,278/3,571 | 2,963.0/3,042.25/1,711.25/2,931.25/2,278.25/3,570.75 | yes, under the golden's readings only |

## Competing answers that survived
All in Ask B; the main call is unaffected.
1. Doubled labor rows. The dictionary says "one row per person, work order and work day", but 214 person/WO/day keys carry two rows (44 repeated keys in FY crane orders). Golden adds both. Keeping one row per key lowers ORD 113, PNC 59, HLY 41, MRW 27, SLT 24, GNP 11. Closure needed: a person can have more than one row for a work order and day; add them.
2. Makers' hours inside SRT LABOUR_HRS. For 5 SRT jobs (J25-04407, J25-04704, J25-04896, J25-05014, J25-04723) LABOUR_HRS exceeds the visit total, so the visit could be inside it. Golden adds all 20 visits; not adding those 5 drops SLT 79 and MRW 7.75. Closure needed: LABOUR_HRS is SRT's own staff only.
3. Damage orders (DMG). Golden counts their labor (25.8 to 38.8 h per terminal). The dictionary sets damage apart "from the cranes' breakdowns" only. Closure needed: all crane work orders count for labor.
Main-call forks: none. The naive 0.2 x cargo work reading (Saltworks 991) is a different estimand from Rule 3.6 ("all fast to let go"), not a competing answer. Millrace wins every variant that keeps the filed rules.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 19 | yes |
| Formats | 3 or more | csv, xlsx, pdf, json, txt | yes |
| Large file | 25,000 rows or more | tos_crane_activity 80,059; srt_tos_export 38,781 | yes |
| Distractors in metadata.json, none labelled by file name | 2 or more | 3 (ais_berth_segments, cmms_yard_equipment_work_orders, berth_windows_fy2027); names do not label them | yes |
| Distractors unused yet weighable | yes | AIS measures time alongside, yard orders share the ledger, 2027 windows; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2, both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | six-terminal cuts across systems; prompt states "two decimals" for per-call hours and whole hours otherwise | yes |
| Prompt shape and rubric of 25 or more | yes | per-call table plus six terminals by three measures; rubric not generated in the folder, not checked | not verified |
| Reads as real, no LLM tell | yes | thread found none; DST, name changes, mis-keyed call signs, SRT/CMMS overlap | yes |
Hygiene note: the shipped cmms_labor_transactions_fy2026.csv has 9,654 data rows against 9,681 in metadata.json rows. Refresh the count in metadata.json (not checked beyond line count).

## Gate G reconciliation
Thread: mechanism other (counterfactual replay), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card/design note: stump class analytical, allocation_constraints, decisive step the replay of each gated call from the earlier readiness, Layer 2 binding constraint inside a counterfactual. Match. The thread did not name a declared distractor (AIS, yard orders, 2027 windows) as the surface read; the easy route it names is the 0.2 x cargo work reading (Saltworks 991), the same as the note's R0.

Gate G line: analytical_non_defect, surface_read_dependency no, sole_data_defect no, no mismatch with the design note.

## Stump power (Gate F)
Strong. A strong analyst who cleans and reads every rule files saving = 0.2 x cargo work (Saltworks 991 against Millrace 531). The truth needs a sailing model validated on 784 actual sailings and a counterfactual replay, which shrinks Saltworks to 257 and favours Millrace's small ships (856 of 887 h). The thread flags a borderline: a reviewer could class the window quantisation as rule application. The directions fix when ships may sail but no filed text says how the saving follows, and the design note argues this. The main thread should weigh it with the scored readers' result. Rule 3.6 deliberately files the estimand and not the method.

Gate H line: domain pass, layers pass, decisive_step analytical. Matches the design note's `## Three rules` (domain test, Layer 1, Layer 2 and decisive step agree). The swap test fails by design (tide windows do not move to a school).

## Findings, ranked
1. FIX_NOW, Ask B: three data-dictionary pins (doubled rows add; LABOUR_HRS is own staff only; DMG labor counts). No data value, rung or main-call figure changes and no model rerun is needed. Do not file the notice-follows-last-move convention, since that would file HOW.
2. Rubric of 25 or more criteria not verified here.
3. Row-count mismatch in metadata.json for the labor file.
4. Borderline stump-class note above.

## Next action for the author
Add the three dictionary lines (doubled labor rows add; LABOUR_HRS excludes makers' hours; damage-order labor counts toward crane maintenance labor, breakdown downtime unchanged) and refresh the labor row count in metadata.json. Rebuild twice, confirm the data is byte-identical, then proceed to ship.
