# determinism-check report, task478, 2026-10-20

## Verdict
NOT_DETERMINISTIC, plus SOLUTION_WRONG (per-fleet charge asked, one total answered)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor (detection-corrected prevalence by capture-recapture, capture occasion = distinct unit), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main recommendation (seven sections designated) and asks 1, 2, 3, 5 and the service-day counts are forced. One supplementary ask is not.
- Ask 4, pounds of cold mix: the data dictionary says "cold_mix_lb is the pounds of cold mix recorded on the line", so the literal grain is per line and the literal sum is 29,835 lb. The golden (19,520 lb) counts a multi-line order once when every line carries the same figure. No shipped file states that convention; only a statistical pattern supports it (48 of 80 multi-line orders repeat one figure; their per-line average matches single-line orders). All 14 pounds values move. Label: answer_contradicts_files.
- PDF ask 3: the prompt asks the March charge for each of the four fleets; the golden gives one total ($8,832). Per-fleet charges are $3,798, $1,628, $1,628, $1,779 (sum $8,833, so the total and the fleet sum differ by a dollar).
- Minor: the sessions export alone gives 345/147/148/161 days; the 350/150/150/164 golden needs the union with detection-only days. Every other evidence source agrees on the golden, so it is derivable.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Program lane-miles | 2,428.9 | 2,428.938 | yes |
| Confirmed potholes | 1,080 | 1,080 | yes |
| Own-unit re-find / other-unit find | 99.5% / 54.2% | 99.7% / 54.24% | yes |
| Potholes per ten lane-miles, 401 to 414 | 8,7,8,4,4,7,9,3,8,4,5,3,8,2 | same | yes |
| Designated | 401,402,403,406,407,409,413 | same | yes |
| Patched potholes | 20,27,70,8,13,13,85,2,21,3,47,12,9,5 | same | yes |
| Pounds | 1255,1540,3770,360,775,1085,4840,85,1090,130,2735,700,805,350 | line sum gives 2375,1605,5055,690,840,1370,5085,140,2670,190,6690,1530,1160,435 | only under the unfiled order-once rule |
| Camera miles | 2084,1787,7732,1771,2510,1656,6741,1820,1868,2049,13257,2254,1789,1774 | same | yes |
| Service days | 350,150,150,164 | same (sessions plus detection-only days) | yes |
| Charge | $8,832 total | $3,798 / $1,628 / $1,628 / $1,779 per fleet | total yes, per fleet not given |

## Competing answers that survived
1. Pounds (ask 4): line sum 29,835 versus order-once 19,520. Closing rule meant: none filed (the design note's device D6 relies on the data pattern alone). Open.
2. Charge: one total versus four fleet charges; the prompt wording "for each of the four fleets ... the March charge" reads per fleet. Open.
3. Service days from the sessions file alone (345/147/148/161) versus the union (350/150/150/164): closed by detections and traversals agreeing; low risk.
Closed forks (no action): unrecorded potholes (recorded-only or pass-level gives 2 sections, unit-level gives 7, the data pins the unit); patched potholes with OPEN orders excluded; miles over installed units.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, pdf, xlsx, json | yes |
| Large file | 25,000 rows or more | traversals 65,867; detections 37,995 | yes |
| Distractors | 2 or more, in metadata.json, no file name labels one | pavement_condition_2026.csv, winter_operations_2027-03.csv | yes |
| Distractor relevance | unused, weighs, ruled out by a shipped fact | relevant to damage, not a March count; neither reproduces a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (csv, pdf), both present | yes |
| Asks | multi-dimensional, unit and rounding stated | per-section grids; "whole numbers" stated once at the end | yes (the charge ask is ambiguous, see above) |
| Prompt shape and rubric | identifiable, 25 or more criteria | design note counts 81 figures | yes |
| Reads as real | no LLM feel, goldens realistic | judge found nothing; golden memo reads as a district work product | yes |

## Gate G reconciliation
Judge: mechanism statistical_rigor (capture-recapture over distinct units), family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note stump sentence: the pass-level independent-chance path designates only Carrow Point and Elmscourt, while the distinct units are the independent chances (each finding 54 per cent), giving seven. These match. No shipped artifact ranks the candidates wrongly, and the declared distractors do not carry the call. The card file was not found in the tree, so `stump_class` / `analyst_test` / `domain_test` were compared against the note's `## Three rules` only. Gate G: pass.

## Stump power (Gate F)
Strong. The recorded-only and pass-level routes land on 2 designated sections against 7. The cue is in the program text (the population includes potholes no unit recorded) but the persistence per unit is not announced. The method is a recognisable capture-recapture and a strong solver may reach it by noticing the undercount; the blind readers' result should weigh that. Gate H: domain pass, layers pass, decisive_step analytical. The swap test fails for any other field's nouns, since this is the pavement-management detection-corrected prevalence estimate. The pounds, days and miles asks are semantics or rule application, which asks may be.

## Findings, ranked
1. Pounds convention is unfiled and the dictionary's line grain contradicts it (ask 4, 14 values).
2. The charge is asked per fleet but answered as one total, and the fleet charges do not sum to the total.
3. Sessions-file-only readers diverge on service days (minor, derivable).

## Next action for the author
Run /fix-determinism: add one dictionary sentence that on a multi-line order cold_mix_lb repeats the order's total on every line, or ask for pounds per work order. Add the four fleet charges to the PDF answer and state the half-dollar rounding. Keep the main call, the estimator and every other figure frozen, then re-judge once.
