# determinism-check report, task124 (loop 1), 2026-10-13

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor per the judge (design note: forecasting, method_or_model_selection supporting), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (sonnet, medium) read only the fresh unzip and the inlined blocks. Every committed figure reproduced from the bundle. The decisive step is the share among the Lead Status Unknown lines (plan 4.3 / 6.1): the whole-main share scaled to the district's no-tap-card lines, less the lead already found, over the lines still unknown (0.497, 0.279, 0.075), giving 10.79 programme years and RZ-10 finished in 2037. The judge found the whole-main set separated cleanly (78 mains; any threshold from 0.5 to 1.0 gives the same lines), the targeted visits depleted of lead, and every competing estimator shown by the data to be wrong.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Verified no-tap pre-1989 lines | 4,911 | 4,911 | yes |
| Whole-main segments | 78 | 78 | yes |
| Whole-main shares | 0.556/0.316/0.083 | 440/792, 96/304, 14/168 | yes |
| Unknown-pool shares | 0.497/0.279/0.075 | 0.4972/0.2789/0.0751 | yes |
| Plan cost, years | $274.1M, 10.79 | $274.07M, 10.790 | yes |
| Zone lines, costs, finish years (12) | as golden | all match | yes |
| 2026 payments (12 values) | as golden | match to the dollar | yes |
| Signed agreements by zone (12) | as golden | match | yes |

## Competing answers that survived
None on the main call. Alternatives each give a different year and each is ruled out by a shipped fact: straight whole-main carry-over (2038, 11.20 years), pooled whole-main share 0.435 (2039), all verifications (2040). Margin of the 2037 call to the 2038 line is about $5.3M (1.9% of cost), thin but stable under the judge's variants (10.73 to 10.79).
Minor wording risk, on an ask only: "lines we will replace" could be read as the classified Lead+GRR count rather than the expected replacements. Optional tightening: "lines we expect to replace".

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 16 files, 5 formats, 87,410-row inventory | yes |
| Distractors in metadata.json | 2+, none named by file name | lcr_tap_samples_2025_2026.csv, ami_meter_exchanges_2023_2025.csv; unused by the solution | yes |
| Distractor weighs but is ruled out | relevant, ruled out by a shipped fact | judge confirms unused; I did not separately test that either one reproduces a graded quantity | yes, with a note |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | 12-zone x 3 fields, 3 contractors x 4 quarters, 12 zones; rounding stated | yes |
| Prompt shape, rubric 25+ | identifiable, 25+ | shape 06 in metadata; rubric not generated yet, so 25+ is not verifiable here | not checked |
| No LLM tells, goldens realistic | yes | judge found none; I did not review the golden files | yes (judge only) |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: mechanism forecasting (method_or_model_selection supporting), analytical_non_defect, no, no. Family, surface read and defect match exactly. The mechanism label differs in name only (estimator choice under selection in both). The declared distractors are not the surface read and carry nothing. No shipped artifact ranks the zones or schedules the plan. No send-back signal.

Gate H: domain pass, layers pass, decisive_step analytical. This matches the card (stump_class analytical) and the design note's Three rules (domain test, Layer 2 = estimand identification under selection, analyst test files 2040 or 2038).

## Stump power (Gate F)
Moderate to good. Easy routes file 2040, 2039 or 2038 and each flips the call to "not finished by 2037". The 2038 route is the hardest to reject. The asks carry their own devices (reclosings, change-order repeats, zone drift).

## Findings, ranked
1. None blocking.
2. Thin cost margin (about 1.9%) on the 2037 call. Stable, so no action.
3. Optional ask-1 wording tightening ("expect to replace").
4. The design note says executing the filed text literally leaves the estimator open, while the judge reads plan 4.3 as closing it. Both land on the golden; this is a point for the stump sentence, not a fork.

## Next action for the author
Proceed to ship with no rerun. Optionally apply the ask-1 wording tweak if prompt.txt is reopened anyway.
