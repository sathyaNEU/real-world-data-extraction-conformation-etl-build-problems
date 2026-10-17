# determinism-check report, task469, 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium) recomputed every graded figure from a fresh unzip of target.zip. All reproduced. SFG-3 2.2, 2.4, 3.1, 3.3 and the delay-code grouping file fix the estimand (population, left-censored need, 20 per cent bar, five-minute steps). The closest decision gap is 6 points. Subset-estimator and reverse Kaplan-Meier variants, and window, uncoded-delay and remote-stand variants, move no decision. No fork survived.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Peak turns, six relationships | 2731/1114/2398/1023/930/1016 | same | yes |
| Share needing longer than filing | 27/6/7/26/31/1 | 26.9/6.3/7.0/26.3/30.6/0.7 | yes |
| Shortest acceptable | 40/40/30/45/35/30 | same | yes |
| Week 12-18 Jul 2027 turns/short | 213/42, 84/21, 189/42, 105/28, 91/28, 77/21 | same | yes |
| Naive overrun route | max under 9 per cent | 8.6 | yes |
| Naive stand-time route | at least 74 per cent | 74 to 97 | yes |

## Competing answers that survived
None. Examined and closed: accepted-filing "shortest" for Grayling Air (35 vs 30; the prompt and 3.3 give 30), DEI 050 meaning (operating flight named in data field), code 93 (code file groups it as not ready). Optional wording pin: say whether an accepted relationship's shortest is the standard's step.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10 / 3 / 25,000 rows | 16 / 4 (csv, xlsx, pdf, ssim) / 28,392 rows | yes |
| Distractors in metadata, not in file names | 2+ | punctuality workbook, staffing file (file names do not label them) | yes |
| Distractor unused yet weighable | yes | rank nothing on turn need; neither answers a graded quantity | yes (staffing file is the weaker one) |
| Deliverables | 1-3 | 1 xlsx, present in golden (4 sheets, 1 chart) | yes |
| Asks multi-dimensional, unit and rounding stated | yes | whole minutes and whole turns stated | yes |
| Prompt shape / 25+ criteria | identifiable, 25+ | shape 14 named; the rubric is generated later, so 25+ is not verified here | shape yes, count not checked |
| Not LLM-looking, golden realistic | yes | judge found none; I did not audit realism | yes (judge) |

## Gate G reconciliation
Thread: mechanism statistical_rigor, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical; analyst_test (overrun route accepts all six, stand-time route sends all six back); domain_test (left-censored tail probability). Design note stump sentence and `## Three rules` match: the same easy routes, the same censoring decisive step. Neither declared distractor is named as the surface read carrying the task. No mismatch. Gate G: pass; no shipped artifact ranks the candidates wrongly, and the difficulty survives deleting every wrong number.

## Stump power (Gate F)
Judge estimate: about half of strong runs stumped. Both natural routes give opposite wrong answers; the shipped data does not pre-disarm the trap. No model responses were tallied; portal evidence only.

## Findings, ranked
1. None blocking.
2. Optional: pin "shortest acceptable" for accepted filings (30 for Grayling Air).
3. Rubric criteria count (25+) is unverified at this stage.

## Next action for the author
Proceed to ship; optionally add the one-clause pin on the accepted-relationship shortest time, which would need a re-judge.
