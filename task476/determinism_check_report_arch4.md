# determinism-check report, task476 (architecture 4), 2026-11-04

## Verdict
DETERMINISTIC (the main call reproduces and is forced by the stem-map evidence).
**Disposition:** SEND_BACK (Gate H, decisive step planted)
**Stumping type:** mechanism: etl_conformance (de facto planted_defect_flip on the tag join), stumping_family: surface_read_rejection (borderline), surface_read_dependency: yes, sole_data_defect: yes

## Why
Executing Policy 7.4 section 2 literally, with the 371 re-tagged trees recognised through the 2021 stem map, gives CF-112 27.0, CF-138 59.0, CF-152 34.3 per cent, next stand 5.6. Every stand share, BA/ac and volume/ac reproduces. The whole difficulty is one identity break (371 trees coded M with an N record on the same spot): a tag join files eight stands. On clean data with no re-tags the tag join already gives the three stands, so nothing stumps. Source: judge thread verdict at /tmp/determinism-check-task476-v4-1793780500/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2021 live trees | 6,859 | 6,859 | yes |
| Re-tagged (M with N within 2 ft) | 371 | 371 (max 1.84 ft, next nearest 6.5 ft) | yes |
| Double entries / new trees | 160 / 604 | 160 / 604 | yes |
| 2026 fates | 6,278 L, 330 D, 237 missing, 14 C | same | yes |
| Shares CF-112 / 138 / 152 / 118 | 27.0 / 59.0 / 34.3 / 5.6 | 27.03 / 59.02 / 34.29 / 5.58 | yes |
| BA per acre, 22 stands | table | pooled ratio matches all | yes |
| Volume per acre, 22 stands | table | matches to 10 bf | yes |
| CF-138 "set aside would read 8.2" | 8.2 | 8.23 only under one reading (6.26, 2.74 otherwise) | partly (side claim, not graded) |

## Competing answers that survived
1. Per-acre estimator on the BA and volume asks: pooled ratio (golden) against the mean of condition-level values (CF-104 205.8 v 202.4, CF-115 184.4 v 179.1, CF-174 221.1 v 228.2). The manual does not pin it. Open fork on the asks, not on the call.
2. Re-tag identity: a literal reader trusting the crew's M code gets eight stands; closed only by inference from the stem map.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10 / 3 / 25,000 rows | 12 / 4 (sqlite, xlsx, csv, pdf) / tree_meas 27,106 | yes |
| Distractors | 2+ in metadata.json, none named in a file name | aerial_detection_survey_2025.csv, delivered_log_prices_2026q3.csv | yes |
| Distractor relevance | unused, weighed, ruled out by a shipped fact | prices ruled out by Policy 7.4 (basal area); survey predates the remeasurement | yes |
| Deliverables | 1 to 3 | 2 (csv, pdf), all in the golden | yes |
| Asks | multi-dimensional, unit and rounding stated | stand table of three columns across 22 stands, units and rounding in the prompt | yes (estimator fork aside) |
| Prompt | plain paragraph, under 1,000 chars | yes | yes |
| Rubric 25+ criteria | 25+ | not verifiable here; the 22-stand table and 6,859-row fate file imply it | not checked |
| Reads as real work | yes | judge found no authoring language | yes |

## Gate G reconciliation
Thread: mechanism etl_conformance, stumping_family surface_read_rejection (borderline), surface_read_dependency yes, sole_data_defect yes. Card: gate_g etl_conformance, stump_class analytical, layer2_family estimation_fit. The mechanism label matches. The class does not: the card calls the stump analytical and the thread classes it a planted identity defect. The declared distractors (aerial survey, price sheet) are not the surface read carrying the task; the pull toward eight stands comes from the tag join, with the 2024 burn reports supplying plausibility. Burn reports are not a named distractor. Gate G itself: the wrong answer is produced by the naive join of the shipped files, not by a shipped artifact ranking the stands, so no Gate G ranking finding. MISMATCH on stump_class.

## Gate H line
domain pass (CFI remeasurement and growth and loss is real forestry work); layers: Layer 1 present, Layer 2 missing; decisive_step planted. Card analyst_test and domain_test both describe a failure that exists only because tags were corrupted.

## Stump power (Gate F)
The tag join would catch strong solvers who trust the M code; a solver who checks the stem map clears it. The recommended calls (CF-138 by fire, CF-112 and CF-152 by beetle) are easy to find. Plausible stump, but for a data-semantics reason, which rule 3 bans as the decisive step. The design note's own claim that matching is spread-zero over 48 tolerance settings means there is no judgment the data have to settle once the idea is had.

## Findings, ranked
1. Gate H: decisive step is a planted identity defect. SEND_BACK.
2. Estimator fork on BA and volume asks (pooled v mean of conditions): pin in the manual.
3. Critical component 3, the "8.2" parenthetical, reproduces under one of three readings: drop or restate.
4. Card analyst_test and layer2 label do not survive the clean-truth test (below).

## Answers to the coordinator
1. The failed gate is H (the stump class: planted, with Layer 2 missing). G passes in the sense of no shipped ranking; C/E has a secondary exposure on the asks' estimator, which alone would be a FIX_NOW, not the send-back.
2. The re-tagging is Layer 1 mess carrying the stump. Tag loss from bole char is plausible field structure, and spatial record linkage is a real method, which is the best counter-argument and the main thread should weigh it against the ETL objective. But the test fails on the generator's clean truth: with no re-tags the tag join is exactly right and files the three stands, so the easy route is wrong only because of the corrupted identifier. Once the idea of stem-map matching is had, there is no estimate, no uncertainty, no choice among methods (spread zero), only a deterministic match. Cleaning the data makes the call easy, which is the CLAUDE.md signal that the stump was Layer 1. The card's analyst_test describes the corrupted data, not the clean truth, and the design note's own Not-semantics line ("no field says which added trees stood in 2021") concedes a data-recovery step. The note's No decoy line is also strained, since the burn reports and the stand table's underburn flags give the wrong eight their plausibility.

## Next action for the author
Re-root with the stump moved into the analysis (a loss or rate estimand where the easy route is wrong on clean, correctly keyed data), and keep the stem-map relinking only as Layer 1 if at all. Whatever ships, pin the per-acre estimator in one sentence of the manual.
