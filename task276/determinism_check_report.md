# determinism-check report, task276, 2026-11-03

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Run r5: one isolated Sonnet thread on the scratch bundle /tmp/determinism-check-task276-r5/ (fresh unzip, prompt.txt, blocks.md). Its verdict is /tmp/determinism-check-task276-r5/verdict.md. The thread derived every figure literally before opening blocks.md.

## Why
The cab fit standard defines a failure as a driver who cannot be seated in the posture the Ellisand model predicts for them in that cab, with the eye point inside the vision zone. Executed literally on the 2,658 rostered drivers, with the posture placed against the bulkhead trim face, this gives Pennick FD35 166 fails (160 women) and Ostrel FD35 319, a gap of 153. Every fleet figure (jobs, miles, rates, off-road days, vehicle-years) reproduces once the three Layer 1 joins are done: reused fleet numbers, 22 carried-over jobs counted once, and units that keep recording after removal. No printed value sits at a rounding edge. The order of the cabs changes only if the backrest is not tested against the bulkhead at all.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pennick FD35 fails / women | 166 / 160 | 166 / 160 | yes |
| Ostrel FD35 | 319 / 305 | 319 / 305 | yes |
| Pennick RD43 | 399 / 359 | 399 / 359 | yes |
| Wrenfold RD43 | 435 / 121 | 435 / 121 | yes (geometry-dependent, see findings) |
| Wrenfold FD35 | 450 / 109 | 450 / 109 | yes (same) |
| Runner-up gap | 153 | 153 | yes |
| Pennick jobs Q1-Q4 | 76/74/85/81 | same | yes |
| Ostrel jobs Q1-Q4 | 40/38/30/50 | same | yes |
| Miles Pennick / Ostrel | 2,231,700 / 1,280,400 | 2,231,720.7 / 1,280,381.4 | yes (20.7 and 31.4 miles inside the edge) |
| Jobs per 100,000 miles | 14.16 / 12.34 | 14.159 / 12.340 | yes |
| FD35 off-road days Q1-Q4 | 901/875/933/906 | same | yes |
| RD43 off-road days Q1-Q4 | 422/457/524/523 | same | yes |
| Vehicle-years FD35 / RD43 | 109.9 / 52.6 | 109.926 / 52.614 | yes |
| Days per vehicle-year | 32.9 / 36.6 | 32.886 / 36.606 | yes |

## Competing answers that survived
- Hip point in stated travel only (with or without vision): Wrenfold FD35 wins at 107 to 109. This is the easy route. The literal text allows it only if "posture" is read as hip point plus eye point. The thread rules it the wrong estimand, not a defensible rival, but notes a literal basis exists because the standard does not itemise the backrest test.
- Backrest tested on the torso line only (rear-face offset dropped): Wrenfold FD35 118, so Wrenfold wins. This is the same fork as above, one step later.
- Backrest geometry variants that keep the test: Wrenfold 440/421 or 445/425 against the golden 450/435. The call holds; only the two Wrenfold cells move.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 20 (metadata and tree; the thread said 21, a miscount) | yes |
| Formats | 3 or more | 4 (csv, docx, pdf, xlsx) | yes |
| Large file | 25,000 or more rows | telematics_daily_odometer_2025_26.csv, 58,851 rows | yes |
| Distractors | 2 or more named, none labelled by file name | tender_prices_2027_shortlist.xlsx and adult_body_dimensions_reference_tables.pdf in metadata.json; file names do not label them | yes |
| Distractor role | unused by solution, weighs, no graded quantity | prices rank on price (cheapest Ostrel FD35); reference tables are population tables; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | cab, quarter, converter and chassis cuts; each states whole numbers, nearest hundred, two or one decimals | yes |
| Prompt shape and 25 criteria | identifiable, 25 or more | shape 01 declared in metadata; the rubric is generated downstream and is not in the folder, so the count is not verifiable here | not verifiable |
| Reads as real work product | yes | no LLM tells reported by the thread; golden realism is not re-judged here | yes (thread) |

## Gate G reconciliation
Thread: no shipped artifact ranks the cabs, converters or chassis on the decision question; the surface read (stated travel, hip point only) is something the solver builds, and it is not carried by any file. Prices were not named as the surface read.
Design note and card: `stump_class: analytical`; the declared distractor is the tender prices (cheapest Ostrel FD35, not the call); no file ranks the cabs on drivers fitted. This matches. The distractor is not too load-bearing, since neither the thread nor I find it carrying the call.

Gate H. Thread: domain Human Factors (anthropometric design fit); Layer 1 is the forms in imperial units, Vennerley numbers, SgRP-axis packages and the fleet-system joins; Layer 2 is the whole predicted posture against the package; decisive step ruled (a) analytical. Design note and card: same domain; same Layer 1 and Layer 2; same decisive step (the backrest placed at the predicted torso angle against the bulkhead line); `analyst_test` names Wrenfold FD35 at 109 as the strong analyst's answer. This matches. The thread and the note differ in one word. The note calls the backrest test "silent"; the thread calls it "allowed and implied by posture, not stated". Both agree the standard does not itemise it.

## Stump power (Gate F)
Real on paper. The easy route of hip point against stated travel plus vision gives Wrenfold FD35 at 109 and the wrong cab. The route that places the whole posture against the bulkhead gives Pennick FD35 at 166. The thread did not class the decisive step analytical merely because the golden is a standard method: the golden needs the seat sheet, the package data, the model's torso angle and a geometry the solver builds, with no filed procedure. A strong solver who thinks about the backrest against the structure lands it. This is a physical-fit check that a human-factors expert makes routinely, so the main thread should weigh it against the ladder as a landable call (`stumping` 1.3). The asks carry separate difficulty (carried-over jobs, reused numbers, unit overlap, union of spells).

## Findings, ranked
1. Wrenfold counts (450 and 435) depend on reading Brevin S4 as length along the torso line and S5 as the offset behind it. 21 Wrenfold FD35 drivers sit within 3 mm of the bulkhead line, and other plausible geometries give 421 to 445. The recommendation, the runner-up gap and the Pennick and Ostrel figures do not move. These two cells (xlsx ask 1 and critical component 3) are the only reproducibility exposure. Closing it means filing the HOW of the geometry, which would make the decisive step rule application, so leave it.
2. The backrest-to-bulkhead test is implied, not stated. A solver who reads "posture" as hip point plus eye point has a literal basis for Wrenfold FD35. The thread judged this acceptable because the geometry itself rules the easy route out and the wording stays on the WHAT. This is the intended stump and the main residual reading risk.
3. Miles assume the entered-at-fitting odometer is the unit's opening value. A first-reading baseline gives 2,230,300 and 1,279,200 (rates 14.17 and 12.35). The order does not change. This is a Layer 1 convention rather than a stated rule, so confirm the shipped telematics notes close it.
4. Hygiene: the thread's file count of 21 is off by one against 20 in metadata and the tree. This does not affect any gate.

## Next action for the author
No determinism repair is needed. Proceed to ship with the other stage 4 gates. If you want to reduce finding 3's exposure, confirm that a shipped sentence in the telematics unit changes file or the reporting standard names the opening odometer value, and assert that in `checks.py`.
