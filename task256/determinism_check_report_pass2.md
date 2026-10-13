# determinism-check report, task256, pass 2, 2026-10-13

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread judged the fresh unzip (target.zip sha256 starts 3822ece866774b65) cold. ES-12 fixes the population (2,110 Bus Operators, all duty statuses) and the rule (lowest price at 95 per cent or more). Averaging each operator's conditional-normal probability of fit reproduces all eight shares and G (96.4) is the cheapest at or above the line. Asks 3 and 4 reproduce from the work orders, roster, disposals and retrofits. The thread found no measurement-convention fork on the shares this time (the physical used per operator reproduced with no conflicting same-date duplicates).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Operators (hr_roster, BUS OPERATOR) | 2,110 (1,522 M / 588 F) | same | yes |
| Shares A-H | 79.4, 82.3, 90.1, 82.6, 93.2, 92.9, 96.4, 97.2 | same | yes, all 8 |
| Maintenance PDL / RSR / TEL / TRK / HDR | 368,370 / 111,523 / 74,873 / 5,692 / 2,793 | same | yes |
| Bus-years | 1,374.5 / 838.5 / 445.7 / 80.2 / 103.4 | same (day-boundary variants move PDL, RSR by 0.1-0.3) | yes |
| Cost per bus-year | 268 / 133 / 168 / 71 / 27 | same | yes |
| Twelve-year cost A-H | 0, 6,662, 4,366, 7,836, 6,168, 10,728, 12,130, 13,904 | same | yes |
| Rival B (survey workers, our sex mix) | 95.6 | 95.6 | yes |
| Rival C (point-imputed) | 95.2 | 95.17 | yes |
| Rival E (stature only) | 95.1 | not recomputed | no (rival only, not graded) |

## Competing answers that survived
- Naive routes B (95.6), C (95.2), E (95.1) are analytical errors, not licensed readings; ES-12 s3.2 defines accommodation as the share of these operators it fits.
- Gate C residual (low): no shipped text says "average the probability"; regression-imputing and counting gives C. Statistically biased; the design note's Estimand/decisive step intends this as the analytical step (filing the HOW would turn it into rule application, so leave it).
- Bus-month day-boundary (disposal on the 1st, retrofit completed on the 1st) moves only one-decimal bus-years of PDL and RSR (1,374.8 / 838.7 or 1,374.4); costs per bus-year and all twelve-year costs unchanged. Minor; readme wording "until it leaves the fleet" supports the golden. Optional: state the boundary day in the readme.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | 4 (pdf, csv, xlsx, md) | yes |
| Large file | 25,000+ rows | work orders 28,746 lines | yes |
| Distractors | 2+ in metadata.json, none named by file | operator_comfort_survey_2023.xlsx, workers_comp_claims (neutral file names) | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | thread did not inspect in depth; design note says they score no fit figure | yes (not independently tested) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 8 configs x share/price/flag, 5 options x 3 measures, 8 twelve-year costs; roundings in the prompt | yes |
| Prompt shape and 25 criteria | identifiable, 25+ | shape identifiable; criterion count not checked by me | not verified |
| Reads as real work product | yes | no LLM artefacts seen by the thread | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card agree: stump is estimand identification (survey joint distribution carried to each operator through the within-sex conditional given stature and weight, residual spread kept, averaged), call moves B/C/E to G. The declared distractors (comfort survey, claims) were not named as carrying the task. No mismatch. Gate G: pass.

Gate H line: domain: pass, layers: pass, decisive_step: analytical. Matches the design note's Three rules (domain test, Layer 1 mess in vendor exports/keys/fleet reuse, analyst test, no decoy, not semantics, not rule application).

## Stump power (Gate F)
High. B, C and E each land within 0.6 points of the line and file the wrong configuration; true margin G 96.4 against E 93.2 and F 92.9.

## Findings, ranked
1. Optional, low: no text states the probability-averaging estimator (Gate C residual); leaving it is consistent with the rule against filing HOW.
2. Optional, minor: state the bus-month boundary day for the bus-years of PDL and RSR.
3. Rubric criterion count (25+) not verified in this pass.

## Next action for the author
Proceed to ship (stage 5); optionally add the boundary-day sentence to exports_readme_fleet_maintenance.md and re-cut only if you accept a new zip.
