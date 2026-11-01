# determinism-check report, task308, 2026-11-01 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (common-mode availability read from the outage record), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Re-check after the prompt dropped the count ("Which 2027 capacity offer", "every offer's net value"). The data and graded figures did not change, and the judge thread (verdict.md in /tmp/determinism-check-task308-pass2-1793571218/) reproduced every figure by literal execution. All 337 shortfall hours have exactly 0 available Northgate IT peaker share, so Ketchum Ridge removes 0 MWh and Red Willow wins. The stale "four offers" wording in submission.md block 4 is fixed and now matches the prompt.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Fleet EUE | 9,500 | 9,506.7 | yes |
| Ketchum Ridge | 0 / net -23 | 0 / -23 | yes |
| Red Willow | 7,100 / 106 | 7,077.8 / 105.75 | yes |
| Sandhill Draw | 2,000 / 12 | 2,012 / 11.6 | yes |
| Coulee Flats | 400 / -17 | 433 / -17.15 | yes |
| Member energy (8) | as filed | exact to the MWh | yes |
| 12-CP averages (8) | as filed | exact to 0.1 MW | yes |

## Competing answers that survived
1. Ketchum Ridge availability: the offer-sheet EFORd of 4.5% (or the class average) gives net about USD 112 to 115M and would flip the award. RA-3 s.7 ("in that hour, from the evidence the record holds") favours the hour-conditional share. This is the intended analytical step (design note: estimand identification, not a reading fork). The family of constructions that read the class's record in the hour all give 0 MWh.
2. Rounding order: net values from energy already rounded to 100 MWh give Sandhill 11 and Coulee -18. The design note's fork table row 10 files "rounded once at the stated unit". The judge calls it minor; the prompt's unit sentence does not state the order. Optional hardening only.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25k rows | 14 / 4 (csv, xlsx, pdf, parquet) / MDM export 351k rows | yes |
| Distractors | 2+, named, none in a file name | forward curve and member load forecasts named in metadata.json; judge also notes the GADS codes and SF/PO/MO events | yes |
| Distractors unused and relevant | yes | neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 5 asks, units and rounding in the prompt's last sentence | yes |
| Rubric 25+ criteria | 25+ | not re-counted; the prompt shape (4 offers, 8 members x 2 figures) is unchanged from pass 1 | carried from pass 1 |
| No LLM read | yes | judge saw none | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, family analytical_non_defect, surface_read no, sole_data_defect no. Design note: Layer 2 is estimand identification (the new peaker's availability depends on its class in the shortfall hours), the 4.5% EFORd is a true figure and not a planted decoy, and the analyst test files Ketchum Ridge at about USD 115M. These match. The thread names no declared distractor as the surface read. No mismatch. Gate G: CLEAN. No shipped artifact ranks the candidates wrongly, and the distractors are not load-bearing.

## Stump power (Gate F)
Expected to stump. A strong model that takes the EFORd or the class average awards Ketchum Ridge at about 114M against 106M. Only the join of fleet-list gas service, offer gas service and cause 9130 events gives 0 MWh. The kW unit, the revision rule (revision 0 gives 9,160 MWh) and the DST handling add independent failure points. The judge does not class the step as a landable textbook route.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the design note's Three rules (No decoy, Not semantics, Not rule application all present with substantive text).

## Findings, ranked
1. Minor: rounding order is not stated in the prompt, so Sandhill and Coulee could be filed as 11 and -18. Optional; a prompt change would force a rerun.
2. Fixed before this report: stale "four offers" in the submission.md docx block.

## Next action for the author
Ship. Re-run the remaining stage-4 gates on the final cut; no determinism change is needed.
