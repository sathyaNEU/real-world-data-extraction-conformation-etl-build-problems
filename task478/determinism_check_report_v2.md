# determinism-check report, task478 (architecture 2), 2026-10-21

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (condition: target.zip is stale and must be rebuilt from target/ at ship, see Findings 1)
**Stumping type:** mechanism: method_or_model_selection (with etl_conformance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One sonnet thread (medium) judged a fresh unzip of target.zip plus the blocks as they stood then; its verdict is /tmp/determinism-check-task478-v2/verdict.md. The estimand is filed physically (program 2.2: every pothole once however many times or units recorded it; 2.4 roadway as at 31 March, lane-miles = length x through lanes; 2.1 the 6.0 line). Under it the seven designated sections and all 14 whole-number rates reproduce, and are unchanged for k = 2 to 5 times the RSS, per-unit or fixed sigma, median/mean/min cluster position, and an anchor-on-good-units method. Every single-distance join gives a different set (8 sections at 3 to 25 ft, 5 at 53 ft and up). Unit error is measurable from utility_cover_inventory_2026.csv (six sweeper units 51.5 to 58.5 ft RMS, 28 others 2.3 to 3.0 ft). The 14 pounds reproduce.

Post-thread changes (ask B, camera miles, dropped; prompt, program 3, data dictionary, manifest and the traversals file rebuilt without the re-run block): the thread's camera-miles rows and its step 6 fix are void and not relied on. The call, the rates and the pounds read files that are byte-identical between the judged zip and the current target/ (detections, covers, inventory, crosswalk, turnback, MMS orders), so the verdict on them stands. The thread's garbled-sentence note is already fixed in the current submission.md. I did not re-run the thread (one pass only).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Program roadway lane-miles | 2,428.9 | 2,441.312 - 12.374 = 2,428.938 (road_inventory_2026.csv, turnback pdf) | yes |
| Unit error | sweepers 52 to 59 ft, others 2 to 3 ft | 51.5 to 58.5 / 2.3 to 3.0 (utility_cover detections vs cover inventory) | yes |
| Distinct potholes | 1,413 | 1,413 (kerbline_detections, k=3 RSS) | yes |
| Rates per ten lane-miles (401..414) | 8,7,8,4,4,7,9,3,8,4,5,3,8,2 | same; unrounded 7.83, 6.78, 7.85, 3.79, 3.95, 6.78, 9.09, 3.27, 7.97, 4.19, 4.84, 3.14, 8.16, 1.92 | yes |
| Designated seven | 401,402,403,406,407,409,413 | same | yes |
| Pounds, 14 sections | 1,400 / 1,575 / 3,770 / 495 / 1,000 / 780 / 4,380 / 690 / 1,710 / 655 / 2,560 / 815 / 1,325 / 325 | same (mms_cold_patch_orders, detections severity) | yes |
| Camera miles | (ask removed) | n/a | void |

## Competing answers that survived
- Pounds, sum every task line of a multi-line order: gives 401 = 1,700, 403 = 10,245, 407 = 11,305. Closed only by the data (81 of 98 repeated-figure orders exceed any single patch of those severities; single-line bands sev 1 = 20 to 40 lb, 2 = 30 to 65, 3 = 60 to 110) and the physical wording "used". No file states the convention. Residual fork on the pounds ask only; asks may carry semantics, the main call does not read it.
- Main call: none survived. Margins thin but clean: Fenwick Gap and Kestrelton 6.78 vs 6.0, Rushmead 4.84.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 | yes |
| Formats | 3+ | 4 (csv, json, xlsx, pdf) | yes |
| Large file | 25,000+ rows | 62,376 detections; 63,343 traversals | yes |
| Distractors in metadata.json | 2+, none labelled by file name | 4 named (pavement_condition, winter_operations, traversals, sessions); names unlabelled | yes |
| Distractors unused yet weighable, none answers a graded quantity | yes | none ranks sections or yields a rate; each ruled out by a shipped fact (metadata why lines) | yes |
| Deliverables | 1 to 3, all in golden | 2 (csv, pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | pounds by 14 sections, "whole numbers", pounds named; the rate is the call | yes |
| Prompt shape and rubric | identifiable, 25+ | designation over every candidate; about 48 criteria (14 rates, 14 verdicts, set, 3 chart parts, 2 files, 14 pounds) per design note | yes |
| Prompt | one paragraph, under 1,000 chars | 611 chars | yes |
| Reads as real | yes | thread found no authoring leak or LLM tell; golden csv has 14 rows | yes |
| target.zip matches target/ | identical | 4 files differ (see Findings 1) | NO, ship-step fix |

## Gate G reconciliation
Thread: mechanism method_or_model_selection (etl_conformance), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no, passes Gate G. Design note and card: strategy identity_resolution, Gate G etl_conformance, Layer 2 estimation_fit, no decoy. They agree in substance; only the label differs (estimation_fit vs method_or_model_selection), same insight. The thread names no declared distractor as the surface read, and none of the four carries the call (distractors are not read by the main call; SF11).

Gate H line: domain: pass, layers: pass, decisive_step: analytical. Matches the card (stump_class analytical; decisive step is estimating each unit's error on surveyed covers and linking within it; Layer 1 is local time, crosswalk, turnback, re-runs, repeated order totals).

## Stump power (Gate F)
Good on the main call: the easy route (one join distance) lands on 5 or 8 sections at every distance, and the data admits no single radius (sweeper error 20x the others, deck potholes 15 to 50 ft apart). The thread reached the golden by measuring error from the covers, a judgment the data settles and no filed rule states; it did not class the step analytical merely because the method is standard. Caveat for the main thread to weigh with the scored readers: a strong model that calibrates from the covers passes the call (stage-4 readers A and B missed it, eight sections each), so ask pressure rests on pounds alone now that ask B is gone.

## Findings, ranked
1. target.zip is stale. Its mtime (02:06:11) predates the rebuilt target/. The judged zip held the old fleet_camera_traversals (65,910 rows, with the re-run block), old spring_patching_program_2027.pdf (still asking camera miles in section 3), old data dictionary and manifest. Current target/ has 63,343 traversals and the updated texts. The call-bearing files are identical, so the verdict stands, but shipping this zip would ship the dropped ask and the wrong row counts. Rebuild the zip from target/ at stage 5.
2. Pounds convention (order total repeated on every line) is inferable from data only, never stated. Residual risk on the pounds ask, not the call.
3. Thin margins on Fenwick Gap and Kestrelton (6.78), robust across every licensed variant tried.
4. Label difference estimation_fit vs method_or_model_selection: cosmetic.

## Next action for the author
Rebuild target.zip from the current target/ (two byte-identical rebuilds), confirm it matches target/ file for file, then proceed to stage 5; no judge re-run is needed because the call-bearing files are unchanged.
