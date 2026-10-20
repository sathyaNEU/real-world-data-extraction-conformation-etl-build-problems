# determinism-check report, task250 (architecture 2), 2026-10-20

One report per build, replaced in place at each pass. Passes on architecture 2: pass 2 FIX_NOW (the visit left to the
reader, asks 3 and 4); pass 3 SEND_BACK (cancelled orders with readings and lost orders, asks 3 and 4), the ask layer
rebuilt as v3; pass 4 SEND_BACK (a drift's growth after its check left unfiled), section 9 filed; pass 5 FIX_NOW (the
plan's visit pinned as a check in place, a step against the spring round); pass 6 below, on the shipped pack.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (censoring-corrected forward projection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Gate H line: domain: pass, layers: pass, decisive_step: analytical.

Judge thread: one pass, sonnet, medium, isolated at /tmp/determinism-check-task250-pass6/ (verdict.md there). target.zip sha256 19727806195dcfb76610c8656ec1a2d43c334929bcca6429ae2d7559a32c4ecd.

## Why
Every committed answer reproduces from the shipped files. QC-02 s7 (most sensitive setting whose yearly alerts fit the 28 visits), s9 (an uncorrected drift keeps growing) and the sensor history force the call. A plain re-run on the 131-station network gives 23 at 3.5, which fits 28. Adding the 30 drifts the record's own 3.0 alerts repaired before the 3.5 limit was reached gives 33, which does not fit. 4.0 gives 18 and fits. The choice of 4.0 survived every operationalisation the judge tried.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Kept network | 131 | 131 (148 less 17 baja_prevista 2027-12-31), registro_estaciones.xlsx | yes |
| Re-run alerts a year at 3.0/3.5/4.0/4.5 | 66, 23, 7, 3 | 197, 69, 21, 8 over three years = 65.7, 23.0, 7.0, 2.7 | yes |
| Repaired drifts at kept stations | 35 | 35 of 38 (Historial sensor T) | yes |
| Drifts never reached by the re-run | 10, 30, 33, 34 | 10, 30, 33, 34 | yes |
| Alerts a year | 69, 33, 18, 14 | 69, 33, 18, 14 | yes |
| 2027 drift-alert visits / days by district (8 districts) | 3/9, 6/25, 7/26, 5/25, 9/34, 2/4, 3/8, 5/16 | identical (40 visits, 147 days) | yes |
| 2027 breakdown visits at kept stations by district | 14, 15, 20, 14, 23, 12, 12, 5 | identical (115) | yes |

## Competing answers that survived
No fork changes the call or a graded figure except as follows.
- Peak-year rather than three-year mean for "alerts a year": the setting is still 4.0, but the figure would be 23 instead of 18. The judge rates this weak (prompt and plan read as a mean).
- Window end at the alert day rather than the adjustment day: 3.0 and 3.5 cells move to 74 and 34, and 4.0 and 4.5 are unchanged. The adjustment day is the correct end because the repair stops the growth. Small risk on two graded cells.
- Closed by the files: limit sd from the re-run statistic (s6 and the dictionary say recorded), and visit day = order visit_date (contradicted by the calibration readings and the in-air check in the plan).
- Plain re-run (3.5, 23) is the intended wrong route, excluded by s9 and the 35 repaired drifts.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, one 25,000+ rows | 12 files, 6 formats, estaciones_diario 160,279 rows | yes |
| Distractors | 2+ named in metadata.json, none in a file name | entregas_plataforma_2027.csv, boletin_et0_2027.csv; neither name labels a distractor | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | judge: relevant to the setting, unused | yes (not separately tested for a graded-quantity answer) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | whole numbers stated in the prompt; per-district cuts | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 04 per metadata; criterion count not generated at this stage | not verifiable here |
| Not LLM-reading, realistic goldens | yes | judge found work-order notes, duplicates, decimal commas real | yes |

## Gate G reconciliation
Thread: mechanism forecasting, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: the stump is the analyst's reading of the record as censored by its own repairs; Not semantics, Not rule application and No decoy lines are present and agree with the thread (the plain re-run and the replay both file 3.5; the 2027 summary counts only 3.0 alerts, which every route reproduces). The thread did not name the declared distractors as carrying the task. No mismatch.

## Stump power (Gate F)
Moderate to good. A solver who does not see that 3.0 alerts cut drifts short lands on 3.5 and 23. The s9 sentence hints at the mechanism, which may lower difficulty. The bath-reading exclusion in the visit-day rule is demanding and inferable from the plan's in-air check and the tmin/tmax columns. Not a textbook-method case: the correction is not a filed or standard procedure.

## Findings, ranked
1. None blocking.
2. Optional: file "alerts a year" as the three-year mean to close the peak-year reading (23 vs 18).
3. Optional: note the window end (adjustment day) so the 69 and 33 cells are not disputed. Both would be edits to a verified build; they are not required.
4. data_dictionary.md is a solver-facing aid but names no trap.

## Next action for the author
Proceed to stage 5 (ship); no re-judge is needed.
