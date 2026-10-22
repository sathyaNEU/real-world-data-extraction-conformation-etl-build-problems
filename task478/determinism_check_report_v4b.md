# determinism-check report, task478 (run r4b, re-judge after the r4a repair), 2026-10-22

## Verdict
NOT_DETERMINISTIC (supplementary ask 3, cold mix, only). The main call, ask 1 (rates), ask 2 (crew) and the chart are DETERMINISTIC. No SOLUTION_WRONG.
**Disposition:** SEND_BACK (ask 3 changes what solvers see; the main call, rates and chart stay frozen)
**Stumping type:** mechanism: other (entity resolution of repeated detections after calibrating a directional sensor latency), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: yes (thread flags the clean-data test as borderline)

Thread isolation: one sonnet/medium thread; derivation.md was written before blocks.md was opened (order kept, reported by the thread). Disclosure: its pre-blocks derivation used a coarse gap rule (1,292 potholes, five sections); after reading the blocks it replicated the latency method and found it fits far better (position error to the work-order milepost 1.8 ft against 65 ft uncorrected), superseding its earlier count.

## Why
The r4a fork (WO-27004908's repeated 60 lb) is closed, but the same convention fork survives in a wider form. The golden pounds hold only under a rule no shipped file states: a multi-line order repeating one figure on every line is counted once if the figure exceeds what single-line orders used for lines of those severities, and summed otherwise. SOLUTION_STEPS step 6 also leans on "the mobile app's order total", which is in no shipped file. The data dictionary says only "cold_mix_lb is the cold mix pounds as entered" per task line. Two literal readings give different pounds for all 14 sections. Gate C (competing_defensible_answer, semantic root) fails on ask 3 only.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Program roadway (lane-miles) | 2,428.9 | 2,428.938 (road_inventory_2026.csv less five SR 11 segments in the turnback notice) | yes |
| Unit latency range (s) | 0.47 to 1.74 | 0.47 to 1.74 over 34 units (utility_cover detections vs utility_cover_inventory_2026.csv, within 0.05 mi) | yes |
| Distinct potholes on roadway | 1,427 | 1,427 (1,441 before turnback; flat for any join gap of 8 to 20 ft) | yes |
| Rates per ten lane-miles | 8,7,8,4,4,7,9,3,8,4,5,3,8,2 | 8.14, 6.90, 8.00, 3.71, 4.06, 7.09, 9.13, 2.96, 8.15, 3.98, 4.95, 3.14, 7.93, 2.03 | yes |
| Designated sections | 401,402,403,406,407,409,413 | same seven | yes |
| Cold mix lb (ask 3), all 14 | 1,620 / 1,220 / 3,925 / 625 / 1,115 / 1,485 / 4,360 / 635 / 2,135 / 395 / 3,200 / 1,055 / 1,345 / 690 | reproduces only under the inferred severity-range rule | only under an unfiled convention |

## Competing answers that survived
1. Multi-line order convention (governing). 110 orders have more than one line; 91 repeat one figure on every line. The golden counts 73 as totals and sums 18 (all two-line) by fitting severity-by-pounds ranges on 223 single-line orders (sev 1: 20 to 40, sev 2: 30 to 65, sev 3: 60 to 110), a model no shipped text states. Golden / literal sum of every line / identical figure counts once always: 401 1,620 / 2,630 / 1,595; 402 1,220 / 1,890 / 1,200; 403 3,925 / 10,440 / 3,895; 407 4,360 / 6,215 / 4,255; 411 3,200 / 8,465 / 3,180; 414 690 / 825 / 640. All 14 sections differ under both alternatives. The 60 lb case is edge-sitting: WO-27004552 (two sev-3 lines, 60 each) is summed to 120, yet 60 is the smallest figure any single-line sev-3 order shows; WO-27004247 and WO-27005174 (60 on two sev-1 lines) count as 60. Shipped rule meant to close it: none.
2. Re-patched potholes (note). 58 lines repeat an ext_ref already patched in another order. The golden counts both patches; "first patch only" gives 401 2,350, 403 9,995, 407 5,720. "Its March cold patches used" favours counting both, so a note, not governing.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, pdf, xlsx, json (4) | yes |
| Large file | 25,000 rows or more | 103,162 and 62,800 rows | yes |
| Distractors | 2 or more in metadata.json, none named by a file | 3 (pavement_condition_2026.csv, winter_operations_2027-03.csv, kerbline_unit_sessions_2027-03.json), file names do not label them | yes |
| Distractor weight | unused by solution, weighs, ruled out by a shipped fact | each has a stated reason; none answers a graded quantity (thread: usable) | yes |
| Deliverables | 1 to 3, all in golden | 2 (csv, pdf), no format family required | yes |
| Asks | multi-dimensional, unit and rounding stated | 3 asks x 14 sections plus chart, whole numbers stated | yes |
| Rubric | 25 or more criteria | roughly 45 gradable items (call, 14 x 3 asks, chart, components) | yes |
| Real work product / not LLM-looking | yes | thread found no authoring language; golden realism not re-read here | yes |
| Cold-mix determinism | one reading | three readings survive | no (Gate C) |

## Gate G reconciliation
Thread: mechanism other (entity resolution after latency calibration), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect yes. Design note and card: estimation_fit, directional instrument latency, easy path = link at one distance (five sections, or a seven with Grisholt and Oxbrae). These match: the thread reached the same easy-route failures (raw detections designate 14, uncorrected clusters 11, direction-merged five) and the same correct seven. No shipped artifact ranks the candidates wrongly; the declared distractors are not the surface read carrying the task (surface_read_dependency no). The one soft spot is the thread's note that the clean-data test is borderline (with exact positions naive clustering stumps little); the latency is the difficulty by design, so consistent with the note.
Gate G line: PASS (no mismatch with the declared stump; distractors not load-bearing).

## Stump power (Gate F)
Strong. Easy routes give 14, 11 or 5 designated sections against the correct seven; only the per-unit latency model fitted on covers collapses the scatter into the 8 to 20 ft plateau. The method is a recognised estimation step, not a filed procedure; the data separate the candidates. Ask 3 adds failures that are not valid stumps (unfiled order-total convention).

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the design note's Three rules (estimation_fit, directional instrument latency; analyst test lands on five or a different seven). Swap test fails for other fields' nouns in the cleaning, holds as general statistics' own method.

## Findings, ranked
1. Cold-mix entry convention is unfiled and the golden rests on an inferred severity-range model (Gate B/C, ask 3). Fix in the generator and the data notes.
2. Step 6 cites "the mobile app's order total", present in no file.
3. Re-patched ext_refs (58 lines) unaddressed by the notes.
4. Minor: 620 pothole detections fall outside every session (no effect on any figure).

## Next action for the author
In the generator, make the cold-mix convention a filed uniform fact: either regenerate the 18 per-line look-alike orders so no multi-line order repeats one figure unless it is the order total (and add a data-notes line saying how a multi-line order carries its mix), or give every line its own figure with no repeats; state whether a twice-patched pothole counts twice; drop "the mobile app's order total" from step 6. Rebuild, recompute ask 3, and leave the call, rates and chart frozen.
