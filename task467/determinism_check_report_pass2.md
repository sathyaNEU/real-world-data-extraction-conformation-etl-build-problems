# determinism-check report, task467, 2026-10-17 (pass 2, run r2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One thread (sonnet, medium) saw only a fresh unzip at /tmp/determinism-check-task467-r2/target/ and the inlined blocks. It recomputed every load-bearing value from the bundle. By-law GT-3 s.4 (25-cent steps), FP-07 4.2/4.3 (restatement for loading-arrangement changes only, so the Airport Line is not restated away) and budget line 12 ($535,027) fix the estimand. The data then separate the candidates: the station-zone and other-zone pickup-to-drop-off ratios fall 10.6 and 11.0 per cent, giving 83,855 restated pickups (84,000 to the nearest thousand), an 11 per cent rank share and a fee of $6.50. The $6.50 step holds for a restated base of 82,312 to 85,603. All 120 ledger rows matched an independent rebuild. No decisive fact is missing.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2025 recorded pickups (pu_zone=1, annual 2025 file) | 74,753 | 74,753 | yes |
| Budget line 12 | 535,027 | 653,185.8 - 74,350 - 31,480 - 12,328.8 = 535,027 | yes |
| Station-zone drop-offs, 12 months to 3 Nov 2024 vs 2025 | about -one third | -32% (zones -31.7% to -33.1%); other zones +0.2% to +5.4% | yes |
| Ratio change, station / other zones | -10.6% / -11.0% | -10.6% / -11.0% | yes |
| Restated 2025 | 84,000 | 83,855 (55,955 + 27,900) | yes |
| Rank share | 11% | 10.85% (11.0% on 84,000) | yes |
| Fee | $6.50 | 535,027 / 83,855 = $6.38, lowest step $6.50 | yes |
| Surplus at $6.50 | $10,000 | 10,031 (10,973 on 84,000) | yes |
| Shortfall at $6.25 | $10,000 | 10,933 (10,027 on 84,000) | yes |
| Ledger, 120 rows (pickups and fees) | as filed | all 120 matched (affiliation by trip date, UTC to America/New_York, 315 void pairs and 1,741 re-sent copies removed, fee at the year's rate) | yes |

## Competing answers that survived
Only one residual fork, judged not decisive. Pickups to non-station zones only with no growth control gives 81,578 and a fee of $6.75. It survives only by ignoring the +3% growth in drop-offs and passengers, which FP-07 4.3 does not license, and it falls to -11.3% once growth is controlled. The judge's optional hardening (state that the restatement is net of other changes in the period) is not needed. All the other readings are closed by shipped text:

| Reading | Restated | Fee | Closed by |
|---|---|---|---|
| Recorded | 74,753 | $7.25 | FP-07 4.3 |
| Whole 22% fall | about 95,700 | $5.75 | FP-07 4.2 (the line is not a loading arrangement) |
| Pooled ratio, all drop-offs | 77,418 | $7.00 | mix shift across groups |
| Passenger-based ratio | about 98,800 | $5.50 | line diversion left in |
| Window variants | 83.8k to 83.9k | $6.50 | robust |

The pass 1 FIX_NOW fork is not visible in the pass 2 recomputation. I did not read the pass 1 report for this pass.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 23 (the judge counted 21; I counted 23 in the unzip and in target/) | yes |
| Formats | 3 or more | parquet, csv, pdf, xlsx | yes |
| Large file | 25,000 or more rows | 2024 annual 169,753 rows; 2025 annual 138,055 | yes |
| Distractors | 2 or more, in metadata.json, not in file names | vaa_passenger_statistics_2023_2026.xlsx and vaa_ground_access_survey_2023.pdf; names are neutral | yes |
| Distractor unused yet weighable, ruled out by a shipped fact | yes | the passenger-based ratio gives $5.50 and reproduces arithmetically; the line's diversion in the bulletin rules it out | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 120-cell ledger plus the docx figures; prompt states the rounding for each | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 07 grid, 120 ledger cells plus 4 figures and the chart | yes |
| Reads as real, not LLM generated | yes | judge found no authoring or provenance leakage, and the dates are consistent | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g decomposition_attribution, stump_class analytical, stump_strategy composition_mix. They match. The thread named no declared distractor as the surface read carrying the task; the passenger statistics file is a weighing alternative only, and the call survives its deletion. No mismatch.

## Stump power (Gate F)
Plausible but not guaranteed. The easy routes are $7.25, $5.75 and $7.00, each clean and wrong. The pooled-ratio route yields a small 3 per cent effect that may tempt partial solvers. A strong model that notices the line must still stratify by station zone and control for drop-off growth. The ledger asks add independent traps (affiliation by trip date, UTC, voids, re-sends, the fee in force).

## Gate H
domain: pass, layers: pass, decisive_step: analytical. The thread's Layer 2 is the stratified ratio against an unaffected control. The design note's decisive step and the card's analyst_test and domain_test say the same, so there is no mismatch.

## Findings, ranked
1. None blocking.
2. Minor and optional: the 2024 annual file still carries voids, which the dictionary says only the 2025 file excludes; this is determinate.
3. Minor and optional: the residual pickups-only $6.75 fork could be closed by wording FP-07 4.3 as restatement net of other changes. The judge did not require it and I agree.

## Next action for the author
Proceed to ship (stage 5) from the current rebuild; no change to the generator, prompt or submission is needed.
