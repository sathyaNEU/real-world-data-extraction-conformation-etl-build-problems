# determinism-check report, task183, 2026-10-12

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (no FIX_NOW items; no rerun needed)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge recomputed from target/ that Quarry Hill 21 is the only feeder with in-service sections that have already failed twice or more (17). The section-year hazard is 0.0224 / 0.0201 / 0.311 / 0.578 per year after 0 / 1 / 2 / 3+ failures, so the rate after two failures is 15.4x the rate after one. Carried onto the in-service stock, QH21 leads with 14.9 expected 2027 failures (HR12 9.85, HR14 8.25, ML07 7.88, SP05 7.55). The naive routes land elsewhere: ML07 on the five-year in-service count, SP05 on the trailing 12 months or on insulation and age, HR12 on the filed table 6.1 or all sections ever. All 24 SAIFI, SAIDI and CEMI4 figures reproduce exactly, and none is near a rounding edge. Gates A to E pass.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cable failures INS/SPL/TRM on GIS status IS | counted as stated | 1,055 WOs; 647 on IS sections, 408 on RET | yes |
| QH21 in-service sections with 2+ failures | 17, others none | 17 (5+3+4+1+2+2); all other feeders 0 | yes |
| Hazard ratio, 2 failures vs 1 | more than 10x | 15.4x | yes |
| Expected 2027 failures, QH21 first | QH21 first | QH21 14.9 first; QH22 5.52 last | yes |
| SAIFI, 8 feeders | 1.40 1.97 1.73 1.31 1.58 1.52 2.23 1.53 | 1.399 1.967 1.730 1.312 1.582 1.520 2.230 1.532 | yes |
| SAIDI, 8 feeders | 71.3 131.4 88.2 85.7 92.4 73.5 139.7 125.5 | 71.29 131.38 88.19 85.67 92.39 73.51 139.72 125.51 | yes |
| CEMI4, 8 feeders | 108 1,163 445 485 262 44 1,812 65 | identical | yes |
| MEDs | 2026-01-25, 2026-07-28 | 34.2 and 55.1 min against a 13.69 threshold; the next day is 9.3 | yes |
| Chart | QH21 tallest bar | top bar QH21 under every model variant that includes the prior-failure count, except count plus a feeder fixed effect (HR12 21.8) | yes (top bar only graded) |

## Competing answers that survived
None survive on the committed answers. Residual forks, none of which flips a graded figure under the literal text:
1. **CEMI4 and MEDs.** The prompt's "both with major event days left out" binds the two indices. TVE-RS-04 clause 6.1 keeps MEDs in the count, which is the golden. The excluded reading would give HR12 57, HR14 354, ML03 170, ML07 412, QH21 85, QH22 44, SP05 59, SP09 65. This is the weakest wording point and the shipped clause closes it. Watch it if the portal shows a CEMI4 split.
2. **The 412 customers moved from ML03 to ML07 on 2026-06-14.** Clause 4.2 (the device feeder at the time of the outage) gives the golden. Last-day attribution would give ML03 1.43 / 57.8 and ML07 1.62 / 117.6. The stale CIS labels are a distractor.
3. **Chart bars other than QH21.** Their order is method-dependent (6 distinct orders across 10 variants, per the design note). Only the top bar is graded.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 6 (csv, pdf, xlsx, parquet, json, md) | yes |
| Largest file | 25,000 rows or more | connectivity_meter_points.parquet 37,008 rows; CIS csv 28,221 | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | vault_manhole_inspections_2022-2026.csv and feeder_peak_loading_2021-2026.xlsx; neither name labels it | yes |
| Distractors relevant but unused | same world, unused by the solution | both are same-world asset and loading files; the judge named neither as a surface read carrying the task. The judge's fuller distractor list (filed table 6.1, CIS labels, published MED list, OMS cust_minutes) is wrong-basis material that shipped facts rule out | yes |
| Deliverables | 1 to 3 | 2 (xlsx, png), both present in golden/ | yes |
| Asks | multi-dimensional | the call plus 8x3 per-feeder indices plus the chart | yes |
| Units and rounding stated | in the asking sentence | two decimals, one decimal and whole numbers all stated | yes |
| Prompt shape and 25 criteria | 25 or more | shape 01; 1 call + 24 index cells + chart reaches 25 or more | yes |
| Prompt length | under 1,000 characters | 829, one paragraph | yes |
| Realism | no LLM tells | the judge found system-export irregularities (cp1252/CRLF, banner rows, legacy against ADMS clocks), no authoring disclosure | yes (the golden's visual realism was not judged here) |

## Gate G reconciliation
The judge says forecasting / analytical_non_defect / surface_read_dependency no / sole_data_defect no. The design note and card say mechanism forecasting, Gate G forecasting, strategy composition_mix. They match. The design note's stump sentence (14 sections, 6.4 expected) is the planned figure. Its built-state section records QH21 at 5 + 12 = 17 sections in service with 2+ failures and 15.0 expected, which matches the judge's 17 and 14.9 (the design note's 15.0 is not independently reproduced here). Metadata distractors (vault inspections, peak loading) are not named by the judge as carrying the answer, so no too-load-bearing finding.

## Stump power (Gate F)
The judge rates it moderate to good. The easy routes are the five-year in-service count (ML07), the trailing-12-month count and the insulation-and-age model (SP05), and the filed table (HR12). The stump is conditioning the hazard on each section's own prior-failure count. The 17 QH21 sections are all 1986 XLPE in conduit, so a solver who reads work orders section by section can find the cluster. The judge names no too-easy signal.

## Gate H (the three rules)
domain: pass, layers: pass, decisive_step: analytical. The field's own analysis is a repeat-failure hazard for underground cable sections, plus IEEE 1366-style indices for the asks. Layer 1 is time zones, OMS against ADMS, dated meter rows, repeated bank totals, REPL successor sections and the moved lateral. Layer 2 is the hazard conditioned on prior failures. The easy route a strong analyst takes with every field read correctly is a recent-count or attribute forecast, which files ML07 or SP05 instead of QH21.

## Findings, ranked
1. No blocking finding.
2. Optional, wording only: the CEMI4 clause could say "(major event days left in)". The judge does not recommend it. It changes what solvers see and invalidates prior runs, and clause 6.1 closes the fork.

## Next action for the author
Ship. Take the CEMI4 wording fork to the portal only if the portal result shows a CEMI4 split.

Note: the judge ran from `/tmp/determinism-check-task183-030137/judge_brief.md` as one sonnet thread. Its output is `/tmp/determinism-check-task183-030137/verdict.md`.
