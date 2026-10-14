# determinism-check report, task452, 2026-10-14 (pass 2, rebuilt pack, reference level 89,950 ha a year)

## Verdict
DETERMINISTIC (the thread's SOLUTION_WRONG flag is a wording slip in SOLUTION_STEPS step 7, no figure is wrong)
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (design note: method_or_model_selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed answer reproduced from the fresh unzip: 224 deforestation points, weights 329/2,469/4,785, 122,882.7 ha stated 122,900, interval 100,000 to 140,000, 89,410,300 / 61,081,300 / 28,329,000 t, 23,229,780 t, USD 116,148,900, twelve district areas, 12 x 3 patch counts (30,548 / 12,206 / 3,221), workbook class counts. Plan 4.1 and agreement 4(2) pin the activity data to the reference-sample estimate; the design PDF pins the strata. Every plausible estimator (design weights 122,882.7; rounded weights 122,916; post-stratified 122,934) rounds to 122,900. The adjudication changes no class.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Deforestation points | 224 | 224 | yes |
| Weights (ha/point) | 329 / 2,469 / 4,785 | 328.8 / 2,469.2 / 4,785.3 | yes |
| Area | 122,900 | 122,882.7 | yes |
| 90% interval | 100,000 to 140,000 | 102.8k to 143.0k (variants 103.6k to 142.3k) | yes |
| Reference level emissions | 89,410,300 t | 89,950 x 2 x 497.0 | yes |
| Monitored / ER | 61,081,300 / 28,329,000 t | same | yes |
| Offered / payment | 23,229,780 t / USD 116,148,900 | same | yes |
| EF 497.0, RL 89,950 | stated | 719,600/8 from RL summary PDF | yes |
| District areas | 12 values, sum 122,900 | same | yes |
| Patch counts | 30,548 / 12,206 / 3,221 and 12 districts | same | yes |
| Class counts | 224/2,491/1,285 and 216/2,516/1,268 | same | yes |

## Competing answers that survived
None. Closed by plan and agreement: final-map pixel area 73,225 ha (offer 43.5 Mt), final map as strata with unweighted proportions 171.6k ha (3.38 Mt), unweighted share (zero), unrounded area (art. 4(2)).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 | yes |
| Formats | 3+ | 5 (csv, json, parquet, pdf, xlsx) | yes |
| Large file | 25,000+ rows | parquet 48,947; NFI 39,122 | yes |
| Distractors | 2+ named in metadata, not by file name | nfi_tree_measurements, fire_hotspots; unused by solution | yes |
| Distractor weighs but does not answer | relevant, ruled out | inventory and hotspots carry no deforestation estimate (judge and note agree) | yes |
| Deliverables | 1 to 3 | 2, both in golden | yes |
| Asks | multi-dimensional, unit and rounding stated | 7 asks, rounding in prompt | yes |
| Rubric | 25+ criteria | about 39 patch counts plus 12 areas plus figures, well over 25 | yes |
| Reads as real work product | no LLM tell | judge found none | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (pass 1 line): method_or_model_selection, analytical_non_defect, no surface read, no sole defect. Same family and same decisive step (which strata the estimator uses); only the mechanism label differs in vocabulary. The declared distractors were not named as carrying the task. No mismatch.
Gate H: domain pass, layers pass, decisive_step analytical; matches the note's Three rules (R3a 3,382,582 t easy route, R3b 23,229,780 t).

## Stump power (Gate F)
Moderate. The main call is on the easy side for a solver who reads the design PDF closely (strata table and the stratum column are in plain sight); the asks (patch counting by area share, LT-05 plus LT-06 into La Esperanza, district contribution) carry added weight.

## Findings, ranked
1. Low: SOLUTION_STEPS step 7 says "LT-05 and LT-06 both La Esperanza, the highland districts outside the accounting area"; the concordance marks LT-05 and LT-06 as `program` and the outside districts are SR-01 to SR-06. Reword in submission.md; no figure moves.
2. Low: interval sits about 2.0k from the rounding edges (105k, 145k); stable across variants, no fork.
3. Cosmetic: 1,012 image_2025 dates after 2025-12-01 (60 loss points dated January 2026); classes unaffected.
4. Verdict.md consistency: the file read as it stands is internally consistent (header, tables and Fix agree; counts 7+5+2+1+1 = 16). Its only odd point is flagging SOLUTION_WRONG alongside APPROVE, which is the step 7 wording slip. Nothing indicates the on-disk change altered a conclusion.
5. Not inspected by the thread: provenance and licence (metadata.json lists CC0-1.0 constructed; fine on its face).

## Next action for the author
Reword step 7 in submission.md so LT-05 and LT-06 are described as the 2019 La Esperanza codes inside the accounting area; then proceed to SHIP.
