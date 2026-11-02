# determinism-check report, task202, 2026-11-02

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: other (inflow placement in a stratified lake, then credited reductions on the part reaching 0 to 5 m), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judged bundle: target.zip md5 3af09b6d (17 files, zipped at the archive root). The pass was run on the fresh unzip at /tmp/determinism-check-task202-582671/target/. The earlier-cited af127f28 was a different zip layout (nested target/) of the same 17 files. One thread, one pass, no retry. The judge's verdict is /tmp/determinism-check-task202-582671/verdict.md.

## Why
Rule 2.2 of the fund rules credits a programme only with phosphorus its source added to the 0 to 5 m surface water. The Lenning's daily mean is denser than the 0 to 5 m buoy mean on 122 of 122 June-to-September days in each of 2024, 2025 and 2026 (also true with the 5 m sensor alone, minimum margin 1.9 degC), so A and B keep out 0 kg. Hollinsby effluent (1.8 to 2.2 degC warmer in all 12 months) and the Mill Beck outfall (warmer on every day) are in the surface water, giving C 222 kg and D 36 kg, a margin of 186 kg under either rounding order. The literal reading of every filed rule lands the golden; no cost, eligibility or date constraint reorders it.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Lenning denser days, Jun-Sep, 2024/25/26 | 122 of 122 each | 122/122 each (thermistor + validated/provisional) | yes |
| C season figures, mean | 229, 221, 216; 222 | 229.0, 221.2, 216.1; 222.1 (returns xlsx x 71%) | yes |
| D season figures, mean | 36, 37, 36; 36 | 35.7, 37.1, 36.0; 36.3 (Mill Beck Monthly loads x 50%) | yes |
| Margin | 186 | 185.8 | yes |
| Winter inflow Oct 2023 to Apr 2024 | 51.4 million m3 | 51.419 | yes |
| Winter load | 5,200 kg | 5,213.6 (5,202 to 5,204 under 1 h shift) | yes |
| North basin 2025 TP, chl | 29.9, 8.0 | 29.89, 7.99 (SWL01) | yes |
| North basin 2026 TP, chl | 29.2, 7.9 | 29.20, 7.89 (SWL01) | yes |
| Connect Right found / fixed / not | 126 / 39 / 87 | 126 / 39 / 87 (visit-ref date, blocks expanded via register) | yes |

## Competing answers that survived
Main call: none. The only competitor, crediting river phosphorus to the surface (B about 359 kg beats C), is the intended wrong route, not a defensible alternative; the conductivity profile supports zero entrainment, though rule 2.2 does not state it in words.

Asks only (none touches the call):
- Ask 3 (north basin site): NB throughout gives 41.8/11.9 and 41.0/11.8; pooling gives 35.9/9.9; golden SWL01 from 1 April 2025 (29.9/8.0 and 29.2/7.9). No file says NB moved; closure is by the sampling protocol (20 m bottle). Prompt does not name the site.
- Ask 4 (date used): by the Uploaded column the result is 36 fixed and 90 not, against 39 and 87 by visit-ref date. The ref date is the confirmation date, but its encoding is undocumented.
- Ask 1 (flow): station alone gives 43.6 million m3 and 4,400 kg; exact gauge identities force the reconstruction (Lenning Bridge to 1 June 2024, plus Brankell Beck after).
These are the judge's optional hardening items. Pinning them would hand the device away (supplemental-stumping 1.1c), so I leave them as the author's call, not a send-back.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, eml) | yes |
| Large file | 25,000 rows or more | regulator_gauged_flows_hourly.csv 52,944; thermistor 29,328 | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | hollinsby_beach_bathing_results.csv, lenning_farm_yard_survey_2025.xlsx; file names do not label them | yes |
| Distractors unused yet weighable | yes | unused by the solution; relevant (farm survey to programme A, bathing to the bloom). I did not separately test whether either reproduces a graded quantity | yes, with that caveat |
| Deliverables | 1 to 3, all in golden, no family required | 2 (pdf, xlsx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 9 figures across 4 sets; prompt gives units and rounding | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | shape 18, 31 criteria per the design note's Ask sheet (the generated rubric was not read) | yes |
| Reads as real | no LLM tells | judge found no provenance leakage, realistic noise, coherent dates | yes |

## Gate G reconciliation
Judge: mechanism other (inflow placement then credited reduction), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: strategy and gate_g `decomposition_attribution`, official_decoy false, decisive_rule_filed false. These agree: every pack figure is correct, no shipped artifact ranks the candidates wrongly, and the difficulty survives deleting every wrong number. The judge names no declared distractor as the surface read carrying the task (the distractors are the farm survey and the bathing results). The judge's borderline note that the call approaches a single conceptual flip (load into the lake against load into the surface layer) is derived by computation, not by catching a defect, which matches the card. No mismatch.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Judge's decisive step is the density and plunge-depth comparison of the river with the lake's profile; the design note's `## Three rules` names the same step, field_method. Layer 1 (UK clock to UTC, validated/provisional overlap, station move, block UPRNs, NB/SWL01 key change) matches the note and does not carry the call.

## Stump power (Gate F)
The judge rates it plausible: the largest-load route files B (359 kg) over C (222 kg), and catching the plunge needs a daily density comparison across 366 days against the lake profile. The method is not a filed rule, and the field's standard load budget is the default path and files the wrong programme. The judge's caution is that strong models can skip the step if they take rule 2.2 at face value. The design note's ladder (rung 1 B, decisive rung C) answers that on paper. The main thread should weigh whether a strong solver, reading rule 2.2 and the lake's stratified profile, reaches the density comparison unprompted; the portal measures it.

## Findings, ranked
1. Rule 2.2 never says in words that a plunging inflow adds nothing to the surface layer (the judge's residual risk 1). This is a design choice (no decoy, no withheld rule), supported by the 5 m against 10 m conductivity records. It does not block approval.
2. Asks 3 and 4 rest on inferences the files support but do not state (site code, date basis). They affect asks, not the call. Per the asks-free-of-rules doctrine they stay as built devices.
3. Housekeeping: the stump text in pipeline.json says "about 340 kg a season" for B against the design note's 359 kg, and the zip md5 handed to this stage (af127f28) differs from the judged zip (3af09b6d). Reconcile the pipeline stump line and record 3af09b6d as the shipped zip.

## Next action for the author
Proceed to stage 5. Re-run the final gates on the zip that is actually shipped (3af09b6d), and correct the stale 340 kg figure in pipeline.json.
