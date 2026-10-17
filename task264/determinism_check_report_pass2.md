# determinism-check report (pass 2), task264, 2026-10-17

Judge thread: one, sonnet, medium, isolated to /tmp/determinism-check-task264-r2-1792231383/target/. The export manifest's page count for the levy papers has since been corrected to 2 (the judge's one hygiene note); no graded figure moved.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Resolution 14/2026 (levy_papers, App. A paras 1-6) counts residents once each, and the fieldwork note says every eighth adult leaving was approached, so an adult's chance of interview rises with visits (Q9). Weighting each interview by stratum weight / Q9 and summing by council gives the golden: 50.6% for Keldmere, Ravenwick and Snelgarth, and levies summing to 7,416,300. The competing estimators (visits share 85.09%, visits / weighted mean Q9 24.94%, unweighted 1/Q9 53.41%) each fail the stated estimand. No gate A-E failure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Interviews (wave1.xlsx + wave2.csv, weights joined) | 4,470 | 4,470, no missing weights, weights sum 2,349,510 | yes |
| Placed to a member council | 3,973 | 3,973 (473 OUT, 24 NK) | yes |
| Residents total (sum w/Q9) | 271,900 | 271,888.0 (KDM 45,837.5; RVW 55,919.4; SNG 35,823.9; LKS 26,294.5; GRB 27,272.0; HNM 23,834.5; CHD 20,157.5; WDS 18,818.8; FNC 17,930.0) | yes |
| Nine levies | golden | 1,250,310; 1,525,314; 977,169; 717,236; 743,901; 650,135; 549,836; 513,321; 489,078; sum 7,416,300 (levy_papers: 10,349,900 less 2,933,600) | yes |
| Top-three share | 50.6% | 50.60%, 3,752,793 | yes |
| Parking income net of VAT (GF, DW, LM, TH) | golden | 439,313; 543,124; 449,759; 400,761 (1,832,957.06) | yes |
| Vehicles (GF, DW, LM, TH) | golden | 171,505; 134,156; 166,487; 126,385 | yes |
| 2025-26 levy collection | golden | all paid in full except Chaldale: paid 510,932, owed 3,455 | yes, by value date |

## Competing answers that survived
None licensed by the shipped text. Forks the judge tested and closed:
- Cap or drop the 7 Q9 values above 365: levies move by 1 to 150 pounds, residents to the hundred unchanged; no text licenses a cap.
- Round residents to the hundred before apportioning: levies move by up to about 1,300; the prompt's rounding governs the reported figure and the resolution apportions on "its number".
- Posting date instead of value date for "paid by 31 March 2026": every council would owe its 4th instalment; the manifest defines Value date and the 31 March remittance advices agree.
- App income read as VAT-inclusive: wrong, sessions x charge / 1.2 equals stated income on every line.
Pass 1's open forks (bank cut-off basis, hundreds-rounding, register placements) are now closed by shipped text or data.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 19 | yes |
| Formats | 3 or more | 3 (csv, xlsx, pdf) | yes |
| Large file | 25,000 or more rows | pay_machine_transactions 246,404 rows (counts file 53,063) | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | 3 (annual_permits, population_estimates, supplier_payments); the 2026-27 population levy (Appendix B) is a further in-file distractor; no file name labels one | yes |
| Distractors relevant yet unused, ruled out by a shipped fact | yes | population basis and permits weigh on "who visits"; each ruled out by the resolution and the survey (judge: unused by the solution) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 9 councils x 2 figures, 4 parks x 2, 9 councils x 2; units and rounding stated once for all asks in the closing sentence, not inside each ask sentence | yes (minor note) |
| Prompt shape and 25 or more criteria | identifiable, 25 or more | shape 05 (allocation to a fixed total); about 40 gradable figures plus call and instruction items; the rubric is portal-generated, count not verified here | yes (expected) |
| Prompt form | one paragraph, under 1,000 chars | 803 chars, one paragraph | yes |
| Reads as real, not LLM generated | yes | judge found no authoring or benchmark language; dates coherent; real towns sit as OUT beside the fictional valley | yes |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: analytical, estimation_fit family, decisive step weight/own Q9, default path ends on 24.9%, no planted element. Match. The declared distractors are not the surface read carrying the task; the judge names visits share, visits / mean Q9 and unweighted 1/Q9 as the easy routes, which are the design note's R1 to R3. No Gate G breach: no shipped artifact ranks the councils wrongly.

Gate H: domain pass, layers pass, decisive_step analytical. Agrees with the note's Three rules (No decoy, Not semantics, Not rule application). Semantics and rule application sit only in the asks.

## Stump power (Gate F)
Moderate to good. A strong model that reads the "every eighth adult leaving" sentence can reach 50.6%, so the risk is model-dependent. Independent ETL failure surface in the asks (PM-2103 and C-07 relocations, C-09 doubling, 728 duplicates, value-date cut-off, shared-service split, net app income) holds the rubric. The note's pair ceiling of 29.0 is still to be rerun on the generated rubric.

## Findings, ranked
1. None blocking.
2. Resolved: export_manifest levy_papers page count (now 2, as the PDF).
3. Optional, not needed: prompt pins "apportion from unrounded estimates" and "paid means value date"; they would change what solvers see and need a rerun.
4. Note: the cross-batch clone check was outside the judge's isolation.

## Next action for the author
Proceed to ship (stage 5); no re-judge is needed for the manifest page-count edit.
