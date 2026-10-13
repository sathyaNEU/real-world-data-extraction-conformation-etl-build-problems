# determinism-check report, task256, 2026-10-13

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (optional; APPROVE if the author accepts the small share-fork risk)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
ES-12 fixes the population (2,110 Bus Operator-class employees on the 30 Sep 2026 roster, any duty status), the fit test (all five dimensions inside the envelope) and the rule (lowest price at 95 per cent or more). Only stature and weight are measured, so accommodation is the average over operators of the probability that the five unmeasured dimensions fall inside the envelope, from the Brennard within-sex joint normal. That gives G (96.4), with E 93.2 and F 92.9 below the line. The call is the same under every population or measurement variant tried. One unfiled convention remains: the prompt and ES-12 never say "latest" DOT physical, so the graded one-decimal shares move (G 96.3 to 96.9) under earliest, mean-of-physicals, active-only or clothing-adjusted readings. The call and the yes/no flags do not move.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Operators (M/F) | 2,110 (1,522/588) | 2,110 (1,522/588), roster Sex | yes |
| Shares A to H | 79.4, 82.3, 90.1, 82.6, 93.2, 92.9, 96.4, 97.2 | 79.41, 82.31, 90.12, 82.62, 93.21, 92.91, 96.41, 97.18 | yes |
| PDL total, bus-years, per bus-year | $368,370, 1,374.5, $268 | same | yes |
| RSR | $111,523, 838.5, $133 | same | yes |
| TEL | $74,873, 445.7, $168 | same | yes |
| TRK | $5,692, 80.2, $71 | same | yes |
| HDR | $2,793, 103.4, $27 | same | yes |
| Twelve-year cost A to H | 0, 6,662, 4,366, 7,836, 6,168, 10,728, 12,130, 13,904 | same (rounding order immaterial) | yes |

## Competing answers that survived
- Call: none. Plug-in files C (95.2), unconditional survey share files B (95.6); both are wrong by the filed rule and are the intended easy routes.
- Graded shares only: "latest" physical against earliest (G 96.9), mean of physicals (96.7), weight less 4 lb (96.7), active-only (96.3). The design note's fork SF4 closes this as "same call", which holds for the call but not for the one-decimal shares. Not closed by a shipped sentence.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | 4 (csv, pdf, xlsx, md) | yes |
| Large file | 25,000+ rows | work orders 28,746 | yes |
| Distractors in metadata.json | 2+, none labelled by file name | comfort survey, workers' comp claims; names neutral | yes |
| Distractor relevance | unused, weighs, ruled out by shipped fact | judge: unused, no fit figure (not otherwise stress-tested by me) | yes |
| Deliverables | 1 to 3 in golden | 2 (xlsx, svg), both in golden | yes |
| Asks | multi-dimensional, unit and rounding stated | 8 configs x 3 fields, 5 options x 3, 8 costs; unit and rounding in prompt | yes |
| Prompt shape and rubric | identifiable, 25+ criteria | per-candidate and per-option grading, well over 25 by count of figures | yes |
| Not LLM-looking | real work products | judge found no authoring language; I did not review the goldens separately | yes |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: the decisive step is carrying the survey's joint distribution to each operator through the conditional given stature and weight, with the residual spread kept; no decoy; easy routes B, E and C. These match. The declared distractors (comfort survey, claims) are not named by the judge as the surface read carrying the task. No mismatch.

Gate G: PASS. No shipped artifact ranks the candidates and gets it wrong; distractors carry no fit figure.

## Stump power (Gate F)
Moderate to good. The plug-in route (C, 95.2) and the unconditional route (B, 95.6) are natural and both cross 95 on the wrong configuration; the exact method puts C at 90.1. The failure is analytical, not noise.

## Findings, ranked
1. Minor: "latest DOT physical" is not filed in the prompt or ES-12, so the one-decimal shares in ask 2 are open to alternative measurement conventions (file the WHAT: which measurement, not how the probability is computed).
2. Note: SF4 in the design note claims closure by "same call"; that does not cover the graded shares.

## Next action for the author
Add "at each operator's latest DOT physical" to prompt.txt (883 characters now, so there is room under 1,000), re-run voice-check, and update SF4's closure. Alternatively accept the risk and approve.
