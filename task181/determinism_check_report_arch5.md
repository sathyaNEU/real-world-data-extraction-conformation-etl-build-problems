# determinism-check report, task181, 2026-10-31

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG on one critical component (CC4 and Step 3 name an NNLS "inversion of Table 4" that does not reproduce as written).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no (borderline), sole_data_defect: no

## Why
Plan 4.3 counts cases infected in the barangay; no file records place of infection, so the count is estimated. Every estimator that uses the data's own control group (the working-age share of the rise against each barangay's 2022 to 2026 ratio) gives San Roque, Bagumbayan, Maligaya in and the other 33 out. The six barangays beside the estate are almost all working-age (e.g. Silangan 57 of 58), so the excess is imported; Table 4 and the PSGC estate remark put it in San Roque. Bagumbayan and Maligaya are all-age home outbreaks. Residual risk: the estimator is unfiled, so crude ones flip the marking. Verdict file: /tmp/determinism-check-task181-20261031185304/verdict.md

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Home-address counts, 8 barangays 40+ (San Roque 14) | CC2 | Bagumbayan 86, Maligaya 66, Silangan 58, Kanluran 55, Pulong Bayabas 54, Burol 54, Tabing-Ilog 48, Malinta 47 | yes |
| Placement at f 0.5 to 1.0 | 3 in | f=0.5 San Roque 55.8, Bagumbayan 76.9, Maligaya 62.0, best other 36.8 | yes |
| Excess-based placements | 3 in | same set | yes |
| CC4 "inversion of Table 4" (NNLS) | 3 in | full-matrix NNLS puts 7 in (Silangan 47, etc.); only off-diagonal NNLS gives the golden | no (partial) |
| DMC admissions wk33-40 | 54,65,68,79,80,68,53,60 | same | yes |
| DDH admissions net of transfers | 33,31,58,39,42,27,40,32 | same | yes |
| House index, 12 rounds | listed | all 12 | yes |
| NS1 / IgM wk35-40 | 52,60,52,57,68,31 / 7,10,9,10,10,5 | same | yes |

## Competing answers that survived
1. f-model with f below about 0.45: 7 barangays in. f is unfiled. Rejected on the data (no non-working-age excess at home), not by a shipped sentence. Kanluran is 38.2 at f=0.5 without the merge, a margin under 2.
2. Full-matrix NNLS: 7 in. Incoherent fit, but unfiled.
3. Ask 5 lab person key: patient_ref instead of initials+DOB+sex gives IgM 11,13,16,13,18,9. No shipped sentence files the key. Moderate fork on one ask.
4. Chart bar heights are estimator-dependent (San Roque 56 to 284); only in/out, red bars and the line at 40 are determinate.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 12 | yes |
| Formats | 3+ | 4 (CSV, XLSX, PDF, JSON) | yes |
| Large file | 25,000+ rows | line list 26,205 | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | 3 (vcu_operations, rainfall gauge, lbilhz update); names are neutral | yes |
| Distractor weighing | unused, arithmetic alone does not answer | judge: bulletin total 3,627 contradicts the line list; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | yes in prompt | yes |
| Rubric 25+ criteria | 25+ | not countable from the bundle; design note lists the shape (barangay marks, 12 house indices, 8+8+6+6 figures give well over 25) | yes (inferred) |
| Not LLM-read | | judge: two realism watch items (CBMS jumps Table 1 to 3, plan PDF very tidy) | pass, watch |

## Gate G reconciliation
Thread: decomposition_attribution, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g decomposition_attribution, stump_class analytical, layer2 estimand_identification. Match. The declared distractors (VCU log, rainfall, zone bulletin) were not named as the surface read; the naive read is the home-address count, which is no shipped ranking. No mismatch.
Gate H: domain pass, layers pass, decisive_step analytical. Matches the card's analyst_test and domain_test and the note's Three rules (day-biting vector, exposure place). Note the design note files the NNLS inversion in its enumerated family, so the same Table 4 inversion claim needs correcting there too.

## Stump power (Gate F)
Moderate to good. Easy route is a clean home-address count (8 in, wrong on 7 of 36). Too-easy signals: the PSGC estate remark and the "place of work" table title make the trap discoverable. Placement is not a textbook route that lands itself; crude estimators mis-mark it. Asks add independent difficulty.

## Findings, ranked
1. SOLUTION_WRONG: CC4 and Step 3 claim an NNLS inversion of Table 4 that, as a full-matrix fit, yields 7 barangays in. Fix: rewrite to a placement that reproduces (off-diagonal NNLS with the own-barangay column excluded, or the f-model with the 0.5 to 1.0 range stated); drop "inversion" otherwise; apply the same to the design note's R-family line and to the assert in checks.py if it asserts that variant.
2. Unfiled placement share (f): the live fork below 0.45. Fix: state in the write-up that the data (absence of non-working-age excess) rules out low f; no file change needed per judge, but consider whether the Maligaya/Kanluran margin of under 2 needs a design-note row.
3. Chart heights are estimator-dependent. Fix: state in the write-up/rubric that only marks, red bars and the line at 40 are graded.
4. Lab person key unfiled (IgM fork on ask 5). Fix: note in the rubric, or accept as imperfect-key Layer 1 mess; do not weight IgM heavily beyond that.
5. Realism watch: CBMS table numbering gap and an over-tidy plan PDF.

## Next action for the author
Rewrite Step 3 and CC4 (and the matching design-note and checks.py wording) to the off-diagonal or f-model placement, mark the chart heights as ungraded, then re-judge once per the FIX_NOW rule.
