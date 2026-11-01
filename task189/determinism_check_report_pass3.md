# determinism-check report, task189, 2026-11-01 (pass 3)

## Verdict
NOT_DETERMINISTIC (the main call reproduces; supplementary answers 2 and 3 do not)
**Disposition:** SEND_BACK (the judge's; the fix is a filing change, so a FIX_NOW in the generator followed by one re-judge is the practical route)
**Stumping type:** mechanism: statistical_rigor (left-censored data), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The MCPA call of 4 (Cloonfad, Glasheen, Kilcrohane, Owenbeg) reproduces, with every method that keeps a bounded result bounded agreeing and the closest water body about 11 to 13 percent clear. The ortho-phosphate counts in the return and the chart do not. Read literally (regulations 4.2 and 7.6: every sample at a programme point inside its programme dates, latest approved version per 7.5, crosswalk applied), all 13 water bodies differ from the golden (Aghavannagh 25/13 against 22/10, Ballynure 59/35 against 46/22, Carrowbeg 41/24 against 28/11). The golden reproduces only when an OPO4 row is kept just if its point, date and time equal a pesticide visit at that point, a convention no shipped file or prompt sentence states. 59 approved rows are dropped by it: 24 Tirneevin bottles booked as ARWA-BN-22 and ARWA-CB-41, and 35 off-visit bookings. Label: answer_contradicts_files, with underspecified_objective in flavour.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| MCPA compliance samples, 37 points, 13 water bodies | 427 | 427 (export, FIELD, version 1 or latest approved) | yes |
| MCPA results below a limit | 276 | 276 | yes |
| Limits | 0.005 ug/l (Tirneevin), 0.10 ug/l (Kilgarron) | same (method schedule, export) | yes |
| Non-compliant, bounded estimates | 4 | 4 under censored lognormal fill, Kaplan-Meier, sensitive-method fill and lognormal mean | yes |
| Half-limit, limit, zero fill | 7, 11, 3 | 7, 11, 3 | yes |
| Bounded counts Ballynure, Derryvore, Tirneevin Stream | 35, 25, 20 | 35, 25, 20 | yes |
| OPO4 samples / below limit, 13 water bodies | 22/10 ... 29/11 (total 413) | literal 25/13 ... 32/14 (472 in dates); the golden reproduces only with the visit-identity filter | NO, all 13 |
| Chart bars (13) | same pairs | inherit the same counts | NO |

## Competing answers that survive
- (a) All in-window approved FIELD OPO4 bookings at programme points, which is the literal reading of "how many compliance samples the year holds an approved result for" (472 in total; Aghavannagh 25/13).
- (b) One booking per point and month, from the 12-rounds statement in the programme workbook, with no rule for which of two bookings survives.
- (c) The golden (visit-identity filter, 413 in total).
- No shipped sentence closes the fork between them. The Tirneevin Q3 report lists the ARWA-BN-22 pair as approved results at a client point, which supports (a) over (c).
- Residual fork on the main call: half the reporting limit gives 7. Regulation 7.2's "figure the results it holds support" closes it only by implication.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, json) | yes |
| Large file | 25,000 rows or more | 25,315 row export | yes |
| Distractors | 2 or more in metadata.json, no file name labels one | 5 named (flow, sales returns, two quarterly reports, abstraction register) | yes |
| Distractor behaviour | unused, weighable, ruled out by a shipped fact | stated rules (7.2 equal weighting, issue dates) rule them out; none reproduces a graded quantity except the quarterly reports, which list one quarter only | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | per-water-body table and chart, whole numbers stated | yes |
| Prompt shape and 25 or more rubric criteria | identifiable, 25 or more | shape identifiable; the criteria count was not checked here (the rubric is generated downstream) | not verified |
| Reads as LLM generated / golden realism | none | judge found no authoring language and the goldens are business-like | yes |

## Gate G reconciliation
Gate G: no wrong ranking shipped; metadata declares no wrong-basis distractor (`declared_wrong_basis_distractor: null`), and the judge names none as the surface read carrying the task. `surface_read_dependency: no`. The judge's mechanism (censored-data estimation against a standard) and family (analytical_non_defect) match the design note's Not-semantics, Not-rule-application and No-decoy lines. No Gate G mismatch.

## Gate H (three rules)
domain: pass; layers: pass; decisive_step: analytical. The field's censored-data estimate of an annual mean decides the main call, and the half-limit route files 7 (or 11) instead of 4. The design note's Three rules lines agree for the main call. The ortho-phosphate counts are semantics and rule application, which the asks are allowed to be. The defect is that the visit identity is not filed, not that the asks use it.

## Stump power (Gate F)
The main call is a genuine trap: substituting half the limit gives 7, zero gives 3, and only treating a bounded result as unknown under its own limit gives 4. The judge records that a strong model plausibly fails it. Supplementary 2 and 3 fail solvers on an unfiled convention rather than on analysis, so their stump power is not an analytical one.

## Findings, ranked
1. Supplementary answers 2 and 3 (13 OPO4 count pairs and the chart) are not forced by the shipped files, in all 13 water bodies. This is the blocking finding.
2. The design note intends the visit identity as the silent device of the ask. A silent decisive rule against a literal reading is exactly what the judge treats as an open fork. Filing the WHAT (one bottle per point and visit, the bottle filled on the visit that took the pesticide sample) is permitted, and the asks are free of the three-rules ban.
3. The Tirneevin operational bottles (ARW-2122 and ARW-2241, booked as ARWA-BN-22 and ARWA-CB-41): the crosswalk gives the codes to ARW-0322 and ARW-1041, so a literal join counts them as compliance samples. The judge reports that no shipped file says otherwise, so the crosswalk, the programme or the prompt has to.
4. Minor: residual half-limit fork on the main call, closed only by the wording of 7.2. "The district's water bodies" is closed by the register's network column.

## Next action for the author
In the generator, file the identity of a compliance nutrient sample (one bottle per point and visit, the bottle filled on the visit that took that point's pesticide sample, and the operational points' bottles not compliance samples), or ship a visit id or equivalent field in the export, or drop the off-visit and operational-bottle rows. Keep the main call and Critical Components 1 to 5 as shipped, then rebuild twice byte-identically and re-judge once.
