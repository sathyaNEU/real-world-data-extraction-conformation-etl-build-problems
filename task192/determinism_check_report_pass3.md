# determinism-check report, task192 (pass 3, architecture 4), 2026-11-04

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: other (fault-signature recurrence plus index reconstruction), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One fresh judge thread (sonnet, medium) on a fresh unzip of target.zip (sha256 dbbb2dce...eb140) at /tmp/determinism-check-task192-v4p3-1793781823/, with no sight of earlier reports. DRP-04 5.2 to 5.4 plus the SOE, relay and recloser logs force one reading: MLR-F2-52, phase C, 11 faults at 1,423 to 1,448 A on separate days since 1 Aug; R-3114 (SYC-3) 7; no other device above 5. The stretch is the breaker zone to R-2207 (5.4). All 48 index figures (SAIDI, MAIFI-E, CEMI-2 for 16 feeders) were rebuilt independently from raw OMS, SOE, relay, recloser and topology data and matched. The thread's one discrepancy (CTR-3 SAIDI 0.1) was its own date-normalisation bug, fixed on re-run.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| MLR-F2-52 phase C faults, current band | 11, 1,423-1,448 A | 11 on 11 separate local days, same band | yes |
| R-3114 faults | 7 at 996-1,005 A | 7 (phase A via terminal map) | yes |
| Next highest device | 5 | BLV-F3-52 phase B 5 at 2,034-2,104 A | yes |
| Customers MLR-2 breaker / R-3114 | 2,625 / 863 | 2,625 / 863 | yes |
| Major event days | 19 May, 27 Jun (threshold 38.03, 35,404 customers) | 618.6 and 1405.4; next day 21.1 | yes |
| SAIDI x16 | ask 4 | all within 0.1 min | yes |
| MAIFI-E x16 | ask 5 | all within 0.01 | yes |
| CEMI-2 x16 | ask 6 | all exact | yes |

## Competing answers that survived
Three residual forks, none changes a committed answer under the literal reading.
1. Second choice against clustering width: the plus or minus 2 per cent (4 per cent spread) is not filed. At a 10 per cent window BLV-3 phase B ties SYC-3 at 7, at 20 per cent it reaches 8. MLR-2 stays at 11 and first at every width tested (4, 10, 20, 30 per cent). Data closes it (MLR-2 spreads 1.8 per cent, SYC-3 0.9, BLV-3 currents run 1,266 to 3,085 A). Only the second choice is not literally forced. Low weight.
2. Legacy child tickets (Q1 2026): golden times a child from the parent's Out to the child's Energized; matches SOE breaker closes and the post-April steps-sheet pattern, so derivable. The alternative reading is contradicted by the SOE.
3. Momentary exclusion window: 1 minute (golden) against 5 minutes moves CTR-2 MAIFI-E from 37.42 to 37.35. The 1 minute reading fits 2.5 and 2.7 literally.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (csv 9, xlsx 2, pdf 1, geojson 1) | yes |
| Large file | 25,000 rows or more | 35,909 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 3 named (line_clearance_work, blinking_lights_contacts, lightning_strokes); names neutral | yes |
| Distractor behaviour | unused by solution, weighs, shipped fact rules out | feed the squirrel, damp-morning, storm routes; none gives a graded figure; vegetation shows a full-circuit MLR-2 clearing Mar-Apr 2026 | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ (xlsx sheets: Patrol assignment, Feeders, Repeat faults, Notes) | yes |
| Asks | multi-dimensional, unit and rounding stated | 16 feeders x 3 indices plus the plot, unit and rounding in the prompt (minutes one decimal, events two decimals); CEMI-2 is a count | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | main call, stretch, second choice and reason, 48 index figures, plot: well over 25 | yes |
| Reads as real, not LLM generated | clean | judge found operational-export mess, no authoring text | yes |

## Gate G reconciliation
Thread: mechanism other (fault-signature recurrence plus index reconstruction), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g decomposition_attribution; design note stump sentence: a competent solver counting momentary events, setting storm days aside, normalising by overhead miles and comparing with 2025 lands on NYD-3 while the answer is MLR-2's recurring phase C current. These agree in substance (no defect, no surface-read rejection; the thread's label is a free-text variant of decomposition into a repeating source). The declared distractors are not named by the thread as the surface read carrying the task; they are the wrong-route feeders' explanations (squirrels, wet limbs, taps' phase), ruled out by shipped records. The card's mechanism, stumping_family and decisive_step fields are null, so there is no declared field to mismatch; the label should be set to match on the next card edit.

## Gate H line
Thread: domain pass, layers pass, decisive_step analytical. Card: stump_class analytical, analyst_test and domain_test present and consistent (locate the failing component from fault current falling with distance; the easy route files NYD-3). Match. The thread did not class the step analytical merely because the method is standard: the recurrence signature is not filed anywhere in DRP-04 and the filed-rule family never ranks MLR-2 first or second.

## Stump power (Gate F)
Strong on the judge's read. The default path (indices, momentary rate, rise per mile) lands on NYD-2, NYD-3 or SYC feeders; locating a repeating source by phase and current needs the analyst to choose the grouping. The 48 graded figures require a long reconstruction (dated topology, MED screen, step restorations, SOE-only lockouts, continuation merges), where partial credit fails. Weighing note for the main thread: second choice SYC-3 leans on the unfiled width (fork 1) and a ranking by count over recency that no shipped rule dictates; MLR-2 itself is robust.

## Findings, ranked
1. Fork 1, clustering width unfiled, bounds only the second choice (ask 2 and 3 wording). Low.
2. Fork 2 and 3, conventions derivable from the data and the filed rules. Low.
3. Card gate_g/mechanism fields not populated in the judge's vocabulary. Bookkeeping.

## Next action for the author
Proceed to ship; no regeneration is needed. Optionally, if a free one-line edit is acceptable on a later pass, file that "one current" means a tight cluster (a few per cent), which would close fork 1.
