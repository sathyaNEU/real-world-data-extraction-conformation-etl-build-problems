# determinism-check report, task478 (run r4e, re-judge without the yard stores file), 2026-10-22

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (sensor-latency calibration against fixed references, then dedup), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread isolation: one cold thread on a fresh unzip (md5 c402f80cb434a6f48f1214c09b7bc0cf, 16 files); derivation.md written before blocks.md was opened. Its pre-blocks pass missed the latency and read the dedup as an unpinned-radius fork; after opening blocks.md it re-derived everything from the shipped files only and recorded that as a labelled addendum. Weigh this: a solver who does not find the latency from the cover survey and traversals gets the wrong set, which is the intended stump, but it is also the d4-type Gate A risk (no file mentions latency).

## Why
With each unit's latency estimated from its utility_cover detections (0.47 to 1.74 s, residual 1.5 to 1.9 ft) and each pothole detection moved back along its pass, repeated detections collapse into clean runs: gaps are 0 to 6 ft within a pothole and none from 6 to 20 ft. Any join threshold in that band gives 1,441 potholes, 1,427 after the turnback. That forces the rates, the seven designated sections and, with the data dictionary's closed-together rule and Program S3's roadway basis, the pounds.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Lane-miles | 2,428.9 | 2,428.9 | yes |
| Potholes | 1,427 | 1,427 (1,441 before turnback) | yes |
| Latency range | 0.47 to 1.74 s | same | yes |
| Rates (401 to 414) | 8,7,8,4,4,7,9,3,8,4,5,3,8,2 | 8.14, 6.90, 8.00, 3.71, 4.06, 7.09, 9.13, 2.96, 8.15, 3.98, 4.95, 3.14, 7.93, 2.03 | yes |
| Designated | 401,402,403,406,407,409,413 | same | yes |
| Cold mix lb, all 14 | 1,705 / 1,255 / 4,135 / 625 / 1,155 / 1,485 / 4,445 / 615 / 2,150 / 395 / 3,335 / 1,115 / 1,420 / 690 | exact under the dictionary rule | yes |

## Competing answers that survived
Ask 3 only, weaker, each closed by a shipped sentence: (a) the order table's crew section instead of the roadway section moves 44 lines (401 1,720; 407 3,895; 405 1,245), closed by Program S3 "cold patches made in March on the section's roadway"; (b) equal-pounds dedupe instead of the finished-stamp test moves 16 orders (401 1,725; 412 975), closed by the dictionary ("closes all of an order's lines together ... enters the order's pounds once"); (c) raw sum (401 3,255), closed by the same dictionary sentence. The prompt's own phrase "its March cold patches" is a little looser than S3. Inert readings tested: sessions window, cover proximity, 2025 ids, DST, segment-assignment rule, join threshold 6 to 20 ft, turnback in or out.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, json, xlsx, pdf | yes |
| Large file | 25,000 rows | 103,162 and 62,800 | yes |
| Distractors | 2 or more, named in metadata.json, unused by solution | winter operations, pavement condition, sessions declared earlier; thread confirms they are present and uncarrying (cover inventory is calibration, not declared) | yes (metadata.json not re-read this pass) |
| Deliverables | 1 to 3 | 2 | yes |
| Asks | multi-dimensional, unit and rounding | whole numbers stated | yes |
| Rubric | 25 or more | about 45 items (estimate) | yes |
| Reads real | yes | no authoring leakage | yes |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. It matches the design note's stump (directional instrument latency; easy path clustering at one distance, 11 to 14 sections instead of 7). The declared distractors are not the surface read. Gate G line: PASS.

## Stump power (Gate F)
Good. Raw rows (69,417) or radius clustering give 7 to 100+ per ten lane-miles and 11 to 14 designations; the correction is found from the covers and traversals and confirmed by the clean gap. The method is a recognised calibration step with the data separating the candidates, not a filed procedure.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical.

## Findings, ranked
1. Optional: prompt phrase "cold patches made on its roadway in March" would close the crew-section reading without relying on Program S3 (would require a rerun; not needed to pass).
2. The r4d thread could not find the latency path and r4e only found it after reading the blocks; weigh with the scored readers' result.

## Next action for the author
None required; proceed to ship. Optionally tighten the ask 3 wording only if you accept a rerun.
