# determinism-check report, task256 (loop1), 2026-10-14

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated thread (sonnet, medium, scratch path only) reproduced every committed figure from the bundle. ES-12 pins the population (all Bus Operator class, any duty status, 30 Sep 2026, latest DOT physical), the fit rule and the lowest-price-at-95 rule. The per-operator conditional normal and the eye-height offset from the 140 measured operators are forced by the shipped data. H is 97.0 and G is 93.0, so the call sits 2.0 points either side of the line.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Operators (HR roster xlsx) | 2,110 (1,522 M, 588 F) | same | yes |
| Eye offset, Halvard csv (n=140) | +28.0 M, +27.6 F mm | +27.97 (n=102), +27.64 (n=38) | yes |
| Accommodation A to H (Sobol, 32k draws) | 77.6, 80.3, 87.9, 82.6, 90.4, 90.4, 93.0, 97.0 | identical | yes |
| Maintenance totals (work-order csv, TVRTA-billed, closed 2021-2025) | PDL 368,370; RSR 111,523; TEL 74,873; TRK 5,692; HDR 2,793 | identical | yes |
| Bus-years (fleet roster, disposals, retrofit, readme rule) | 1,374.5; 838.5; 445.7; 80.2; 103.4 | identical | yes |
| Cost per bus-year | 268; 133; 168; 71; 27 | identical | yes |
| Twelve-year cost per bus | A 0, B 6,662, C 4,366, D 7,836, E 6,168, F 10,728, G 12,130, H 13,904 | identical, also with unrounded rates | yes |

## Competing answers that survived
None survived as an open fork. The thread tested each rival against a shipped sentence:
- Survey as published, no offset: G 96.4, so G is filed. It ignores the Halvard report's own measurements (report s6).
- Unconditional survey at the roster's sex mix: B 95.6. With offset: D 95.8. Both ignore each operator's recorded stature and weight (ES-12 s3.2).
- Point prediction without spread: E 95.3 with offset, C 95.2 without. ES-12 s3.1 asks whether an operator fits, and the survey gives a joint normal.
- Stature only: B 96.2.
- A clothing adjustment of 1.5 kg either way leaves H at about 96.7 to 97.3 and G at 92.6 to 93.3.

Residual risk, which the thread recorded as not a failure: the files never say in words to average probabilities or to apply the Halvard measurements. The design note's estimand closure and fork table carry this.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | PDF, CSV, XLSX, MD | yes |
| Large file | 25,000 or more rows | work orders 28,746 rows | yes |
| Distractors named, none labelled by file name | 2 or more | operator_comfort_survey_2023.xlsx and workers_comp_claims_transportation_2019-2026.csv, both named in metadata.json; neither file name labels it | yes |
| Distractors unused yet weighable | per spec | Both are unused by the solution. The thread did not test whether either answers a graded quantity, and I did not check it. Left to the leak reader. | partly verified |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, svg); both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | per spec | Shares to one decimal, bus-years to one decimal, money to the dollar, all stated in prompt.txt | yes |
| Prompt shape and 25 or more criteria | per spec | Shape 01 on the card. The count is about 40 from the golden: 8 shares, 8 flags, 8 prices, 15 maintenance figures, 8 twelve-year costs, the call and the chart. The rubric itself is generated and not shipped. | yes, by count |
| Prompt form | one paragraph, under 1,000 characters | 883 characters | yes |
| Not LLM generated, golden reads as real work | per spec | The thread found plausible operational noise and no authoring language. I did not run a golden-realism read. | yes (thread) |

## Gate G reconciliation
Thread: mechanism `statistical_rigor`, stumping_family `analytical_non_defect`, surface_read_dependency `no`, sole_data_defect `no`.

Card: `stump_class: analytical`, `gate_g: method_or_model_selection`, `stump_strategy: composition_mix`. The card's `analyst_test` names B, E or C, and G as the easy routes. The thread found the same four rivals (B 95.6, E 95.3, C 95.2, G 96.4) at the same values the design note gives.

Result: match. Neither declared distractor is named by the thread as the surface read carrying the task. No Gate G finding.

## Stump power (Gate F)
The thread rated it strong. Four different plausible-but-wrong calls are available and none is named in the files. The offset is estimated and tested, not planted. The one borderline point the thread raised is that the offset step reads as "the survey is off for these operators". The survey stays a true description of 2012 workers, and the shift is estimated from the 140 operators at their own stature and weight.

## Gate H
domain: pass; layers: pass; decisive_step: analytical. This matches the card's `domain_test` and `analyst_test` and the design note's `## Three rules`. The decisive step is the conditional-distribution carry with the measured-operator eye calibration. It is not a field reading or an executed rule.

## Findings, ranked
1. None blocking.
2. Low: the closure of "average each operator's probability, and apply the Halvard measurements" rests on the design note's estimand row and the fork table, not on an explicit sentence in the files. The thread judged the rival readings errors an expert would not make.
3. Low: the 140 volunteers come from one division, so the offset's transfer rests on an inference. The thread's residual regression shows no slope on stature or weight, and the offset is about 14 and 8 standard errors from zero.

## Next action for the author
Ship stage: proceed with the card and pre-ship check. No generator change is needed.
