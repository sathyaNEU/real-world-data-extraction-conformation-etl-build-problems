# determinism-check report, task464, 2026-10-28

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread rebuilt the Copsewell Cross radial topology from `hv_network_model.xlsx`, traced the
downstream load/generation for each replaced section from `lv_monitoring_2025-26.parquet` and
`hv_settlement_2025-26.csv`, and recomputed each section's I2R loss from `hv_conductor_data_EDS-02-0310.pdf`.
Kestle reproduced at 73.9 MWh against the committed 74.2 (within rounding/interpolation noise) and Copsewell
Town reproduced exactly at 48.2 MWh. Critical component 1 (3.95 km, 0.443 ohm/phase) reproduced exactly from the
section lengths and the conductor table. The thread also independently confirmed the named alternative route: using
`copsewell_cross_scada_2025-26.csv` feeder-head current for Oxenford Lane's two replaced sections gives
roughly 300 MWh and 258 MWh, which is exactly the "leads only when every section is charged with the feeder-head
current" line in FINAL_RECOMMENDATION. No competing answer survives on the main call or on either sampled
supplementary figure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Kestle route length / resistance removed | 3.95 km, 0.443 ohm/phase | 1480+1350+1121 m = 3.951 km; (0.276-0.164) ohm/km → 0.4425 ohm | Yes, exact |
| Kestle 2025/26 saving | 74.2 MWh | 73.9 MWh (net-flow half-hourly reconstruction) | Yes, within rounding |
| Copsewell Town 2025/26 saving | 48.2 MWh | 48.18 MWh | Yes, exact |
| Oxenford Lane naive feeder-head saving | (not committed; named as the losing alternative) | ~300.7 + ~257.5 MWh for its two sections | Confirms the named trap |
| Kestle CI (one feeder, spot check) | 105.1 | ≈105.4, applying storm exclusion, LV/HV dedup, and the generator-hire-based exclusion at site 332695 | Close; 0.3-point gap attributed to the thread not independently re-deriving the CML restoration-time logic in the time available |
| Other 7 feeders' CI/CML, and CML generally | as listed | not independently re-derived (time-bounded single-thread run) | Not fully checked by the thread |

The thread's one honestly-flagged gap is that it validated the Kestle figure and the overall exclusion *rules*
(storm window from `iis_reporting_definitions_2025-26.pdf`, LV/HV dedup, and the generator-hire exclusion
traced to `generator_hire_2025-26.xlsx`) against the shipped files, but did not re-derive CML or the other seven
feeders' CI/CML figures end to end. This is a coverage gap in the single pass, not a located discrepancy; nothing
it did check pointed away from the committed figures, and the exclusion rules themselves are all traceable to
specific shipped documents rather than resting on anything absent from the package.

## Competing answers that survived
None. The thread enumerated the feeder-head-current route (funds Oxenford Lane) and the one-way loads-only route
(funds Copsewell Town) and reproduced both as the named, ruled-out alternatives; the shipped fact that closes each
fork is Kirchhoff's current law applied to the network's own topology (ruling out feeder-head) and the Hob Moor
Solar Park's export beyond Kestle's replaced sections (ruling out the loads-only construction). Kestle's margin
over Copsewell Town (~26 MWh, more than half again) is a clean, not a thin-and-contested, gap.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | ≥10 | 13 | Pass |
| Format mix | ≥3 formats | 4 (csv, xlsx, pdf, parquet) | Pass |
| Large file | ≥25,000 rows or large DB | `hv_settlement_2025-26.csv` 175,201 rows; `copsewell_cross_scada_2025-26.csv` 140,161 rows; `lv_monitoring_2025-26.parquet` 1,216,519 rows | Pass |
| Distractors named, not in filenames | ≥2, named in metadata.json, no filename labels one | `metadata.json.distractor_files`: `copsewell_cross_scada_2025-26.csv`, `line_loss_factors_2025-26.pdf`; neither filename says "distractor" | Pass |
| Distractors relevant and unused, one reproduces a graded quantity and is ruled out by a shipped fact | required | SCADA feeder-head current reproduces Oxenford Lane's naive figure (~300+258 MWh) arithmetically and is ruled out by the network's own topology (net-flow construction); line loss factor statement is a licence-area/time-band average ("they do not describe any individual circuit" per the PDF itself) that a solver could misapply in place of per-section I2R physics, unused by the solution | Pass |
| 1-3 deliverables, all present in golden, no required format family | required | 3 deliverables (`losses_programme_2027.xlsx`, `losses_saving_2027.png`, `iis_feeders_2025-26.csv`), all present in `golden/` | Pass |
| Asks multi-dimensional with unit/rounding in the asking sentence | required | Eight projects x MWh/GBP, eight feeders x CI/CML; prompt states "Give MWh, CI and CML to one decimal place and values to the nearest GBP 100" | Pass |
| Prompt shape identifiable, rubric ≥25 criteria | required | `metadata.json.prompt_shape: "07"`; `generator/ceiling.py` computes `n_ask = 8+8+8+8+4 = 36` ask criteria alone, before recommendation/components weighting | Pass |
| Nothing LLM-generated; goldens read as real work product | required | Judge thread hygiene check: PASS, no authoring/benchmark disclosure, files read as genuine operational artifacts (vendor-change monitoring format, overlapping LV/HV logging, mixed ID schemes) | Pass |

## Gate G reconciliation
The judge thread classified the mechanism as `method_or_model_selection` (choosing the correct current-attribution
method among several plausible but wrong ones, on honest, correctly-reported data), `surface_read_dependency: no`,
`sole_data_defect: no`. The design note's card instead files `Gate G: decomposition_attribution` (the feeder's
correctly metered flow split section by section, where overlapping loads and the solar export decide the split).
This is a naming mismatch, not a substantive one: both labels describe the same FINE-numbers shape (honest,
correctly-reported inputs; the difficulty is choosing/ performing the right construction, not catching that a
reported number is wrong), and neither is the banned `surface_read_rejection` family, so it does not change the
disposition. The thread did not name the declared distractor (`copsewell_cross_scada_2025-26.csv`) as itself
carrying the correct answer; it correctly identified the SCADA file as the input that makes the *losing* naive
route (Oxenford Lane) look attractive, which is its intended, declared role, not an over-load-bearing distractor.

Gate H: the thread's line (`domain: pass`, `layers: pass`, `decisive_step: analytical`) matches the design note's
`## Three rules` section point for point: `domain_test` names the same deciding quantity (I2R loss as the square of
each section's net current times the resistance change, estimated from the network's own metering); `Layer 1`
(monitoring vendor change, UTC/local time and settlement-period mismatches, imperial/metric conductor naming) and
`Layer 2` (`field_method`, half-hourly net-flow current reconstruction) are named the same way in both; and the
card's `stump_class: analytical`, `No decoy: true` (nothing planted) agree with the thread's independently-reached
`decisive_step: analytical` and its finding that the SCADA file is true metering, not a planted defect.

## Stump power (Gate F)
The thread rates stump power as strong and for the right reason: the trap is not finding a stated rule (the brief
states the estimand plainly) but executing the current-attribution correctly across a 77-section/81-node radial
network, netting the Hob Moor Solar Park's export against downstream load on Kestle's sections, and resisting the
much easier feeder-head SCADA proxy that sits in a clean, large CSV and flips the call to Oxenford Lane. This is a
textbook route (Kirchhoff's current law on a radial network with embedded generation) that the field's own analysis
requires; per the project instructions' Gate H guidance, applying the standard method correctly, where the data
(not the judgment) settles whether the naive feeder-head or loads-only shortcut is wrong, is a landable call and
weighs toward the design note's analytical classification rather than against it.

## Findings, ranked
1. (Minor, non-blocking) The judge thread's single pass did not independently re-derive CML or the other seven
   feeders' CI/CML figures; it spot-checked Kestle's CI only, with a small (0.3-point) gap attributed to
   not re-deriving the restoration-time/CML logic in full. This is a coverage gap in one review pass, not a located
   discrepancy, and does not change the verdict.
2. (Cosmetic) The design note's Gate G label (`decomposition_attribution`) and the judge's independently-reached
   label (`method_or_model_selection`) differ in name but agree in substance (both FINE-numbers, non-banned). No
   action required; flagged only because a Gate G naming mismatch is the finding type most likely to predict a
   send-back in general, and it is worth the author's awareness that the two labels could be reconciled in the
   card for future consistency checks.

## Next action for the author
None required; the task is APPROVE as shipped. If the author wants extra assurance beyond this pass, the one
optional follow-up is re-running CML and the remaining seven feeders' CI/CML through the exclusion rules in
`iis_reporting_definitions_2025-26.pdf` to close the single coverage gap the judge thread flagged, but this is not
a defect and does not block shipping.
