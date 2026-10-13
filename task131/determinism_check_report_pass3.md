# determinism-check report, task131, 2026-10-13 (pass 3)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: other (demand-response effect estimation at design-day heat, forecasting-family), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread (sonnet, medium, scratch /tmp/determinism-check-task131-pass3-1791887988/, verdict.md) reproduced every committed figure from the bundle using only filed rules. Design C is the only design that lowers the 2027-28 50% POE maximum (214.6 MW); A and B move the peak to the 9 p.m. and 8 p.m. half-hours and raise it. The pass 2 pins (retention date on the households, GST on the bill means) closed the earlier forks: the tables reproduce with no price fork and no denominator fork.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Hot workdays | 7 (43.7 to 45.3 C; next 39.7) | 7, IDCJAC0010 (HM01X agrees) | yes |
| B effect 20:00 / A effect 21:00 | 0.7 / 0.6 kW | 0.73 / 0.64 kW | yes |
| Change to maximum A / B / C | +5 / +20 / -11 MW | +5.10 / +20.04 / -10.99 | yes |
| Home Plan customers, max | 41,860; 214.6 MW | same (forecast xlsx) | yes |
| Status 28 Feb (design; own request; gone) A/B/C | 370;22;7 / 361;29;9 / 374;18;6 | same | yes |
| Charged more, mean diff A/B/C | 123 -$19.64 / 45 -$42.86 / 52 -$31.61 | -19.6402 / -42.8614 / -31.6109 | yes |
| Survey likely share A/B/C | 60.3 / 41.5 / 58.8 | 155/257, 100/241, 147/250 | yes |

## Competing answers that survived
None on the call. Variants (fixed register premise, stayers, 5 or top-3 days, quadratic fit) keep C best with the same sign pattern; only the all-workday average (A, -13 MW) and the in-window cut (B) differ, and neither is licensed by the files. Residual thin fork, ask 2 magnitudes only: a looser heat window ("at least 40 C", 9 days) gives A +1.7 and B +16.3, and a one-day window moves C to -10. The 7-day set is the literal "design-day heat" reading (gap 39.7 to 43.7 C, forecast 44.6 C reference day). Survey Q4 CATI code reversal is documented in trial_survey_instruments_2026-03.pdf and decisive for the survey cells (49.4/44.0/50.4 unreversed). The mover-after-request classification is the one judgement call in table ask 1; "own request" is the only reading fitting the three asked categories.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | CSV, PDF, XLSX | yes |
| Large file | 25,000 rows or more | NEM12 extracts about 90k lines each | yes |
| Distractors | 2 or more in metadata.json, none named in a file | 3 named (zone_substation_loads, rooftop_pv_connections, generation_availability); no file name labels one | yes |
| Distractors unused yet weighable | arithmetic and ruled out by shipped fact | unused by the solution; the judge found no answer to a graded quantity from them. I did not separately rebuild their arithmetic | yes (partial check) |
| Deliverables | 1 to 3, all in golden | 2 (PDF, XLSX), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 3 designs x multiple cuts; MW whole, dollars to the cent incl GST, percent one decimal | yes |
| Prompt shape, rubric 25 or more | identifiable, 25 or more | rubric is generated later; asks give well over 25 gradable cells (about 9 MW/chart plus 18 table cells) | not directly measurable here |
| Not LLM generated, golden realism | | no authoring language found by the judge; golden realism not re-read by me | yes (judge) |

## Gate G reconciliation
Thread: mechanism other (demand-response effect estimation), analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: field_method at the design-day heat over the whole curve, analytical, no surface-read dependency, no sole defect, no decoy. Match. The declared distractors are not the surface read carrying the task; the easy routes (in-window cut files B, pooled average files A) are analyst routes, not shipped numbers. No finding.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Design note `## Three rules`: same (domain test: ex-ante load impact on 50% POE maximum; Layer 1 NEM12 resends, accounts against NMIs, GST bases; Layer 2 half-hourly response at design-day heat over the whole curve; analyst test files B or A). Match.

## Stump power (Gate F)
Moderate to good. The traps are analytical on correct inputs: analyse as assigned and follow movers; condition on design-day heat (effect plateaus near 0.73 kW above 40 C); add the whole-profile pull-down to the design-day curve. Averaging all workdays files A, the in-window cut files B. Strong models may still clear it.

## Findings, ranked
1. Optional, non-blocking: the heat window is unfiled, so ask 2 magnitudes for A and B (not the call) move under a looser or one-day window. Judge suggests the phrase "at the 44.6 degree design-day temperature" in prompt.txt; this would change the prompt, so weigh against the 10/10 rule on filing the WHAT not the HOW (the temperature is a population/window pin, so it is the WHAT).
2. Cross-batch fingerprint not run (other task folders are forbidden to the judge); `guard.py` covers it.

## Next action for the author
Ship as is (APPROVE); optionally pin the design-day temperature in the prompt before the next rebuild if you want ask 2 magnitudes airtight.
