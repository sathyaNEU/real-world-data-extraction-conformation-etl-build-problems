# determinism-check report, task466, pass 2, 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (censored-data frequency analysis), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium) read a fresh unzip of the re-cut target.zip (16 files) and the five graded blocks. Executed literally, the filed text gives the golden. WR-14 fixes the log-Pearson III, skew -0.30, maximum likelihood and the record. The 1893 agreement quoted in the reports makes "No stoppage" a 7-day flow at or above 2 MGD (3.09 cfs). The permit fixes the 0.50 cfs passby and the 1.40 MGD cap. The plan fixes the 0.91 MGD demand and the smallest-block rule, and the Castlewick offer fixes the 0.1 MGD grid. No graded figure moved since pass 1. The two pass 1 metadata items (the 2026-10-16 dating of folder, dictionary and index, and the Hollow Road totalizer in service 2010-06-08) are closed. The judge found the file dates coherent with the 2026-10-16 snapshot and the only hygiene remark was the "EDT" label on the retrieval stamp, which it called plausible.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Gauged climatic years | 74 | 74, no missing dates | yes |
| Report years measured / no stoppage / not found | 14 / 40 / 3 | 14 / 40 / 3 (1909, 1918, 1944) | yes |
| Censor threshold | 3.09 cfs | 3.094 cfs | yes |
| 10/25/50/100-yr 7-day low flow (cfs) | 2.54/1.89/1.55/1.29 | 2.542/1.889/1.549/1.290 | yes |
| Permit withdrawal (MGD) | 1.32/0.90/0.68/0.51 | 1.32/0.898/0.678/0.510 | yes |
| Stage 2 shortfall (MGD) | none/0.01/0.23/0.40 | 0/0.012/0.232/0.400 | yes |
| Block | 0.3 MGD | 0.3 MGD | yes |
| Stop-covering recurrence | 65 yr (1.44 cfs) | 64.84 yr (1.444 cfs) | yes |
| Eight Stage 2 periods (average, highest) | as filed | all 16 figures match to 2 decimals | yes |

## Competing answers that survived
None. Forks tested and not licensed by the text:
- Gauge only: 1.87 cfs, 0.025 MGD shortfall, 0.1 MGD block (ignores the "earlier years" clause).
- Gauge plus the 14 measured years, dropping the 40: 1.31 cfs, 0.38 MGD, 0.4 MGD block.
- No-stoppage years as point values at 3.09 cfs: 1.23 cfs, 0.44 MGD, 0.5 MGD block (contradicts "above").
- Quantile method (exact Pearson III against Wilson-Hilferty): within 0.001 cfs, same 65-year stop.
- Totalizer credited to day D, D-1 or split: no 2-decimal figure moves.
- Climatic year 2025 included: 1.538 cfs, same block, but a 63-year stop. Closed by WR-14 ("complete climatic years of the approved record"), the station description (approval through 2025-09-30) and the prompt's 1894 to 2024 span. Low residual risk.
The 0.3 block holds for any 50-year flow from 1.444 to 1.599 cfs, so the golden at 1.549 has clean margin.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 16 / 4 (pdf, csv, txt, xlsx) / 27,592-row daily file | yes |
| Distractors in metadata.json, none labelled by file name | 2+ | 2 named (regional regression 2019, 2NW precipitation); neither name labels a distractor | yes |
| Distractor unused and weighing | yes | regression report states it is not used at gaged sites; its figure would differ; precipitation unused | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, csv), both in golden/; no format family required | yes |
| Asks multi-dimensional, unit and rounding stated | yes | scenario table, flip point, chart, 8 periods x 2 figures; units and rounding in the prompt | yes |
| Prompt shape and 25+ criteria | shape 13, 25+ | shape 13 identified in metadata. The rubric is generated at ship and was not in the folder. The design note plans 18 ask criteria plus the main block. Not verified here. | open |
| Reads as real work product, not LLM generated | yes | judge found real-world irregularity and no authoring disclosure; the PDF golden was not independently realism-checked by me | yes (judge) |

## Gate G reconciliation
The judge read the stump as censored-data frequency analysis (analytical_non_defect, no surface-read dependency, no sole data defect). It matches the card: `stump_class: analytical`, and the `analyst_test` names the 14-measured-year fit (1.31 cfs, 0.4 MGD against 0.3 MGD), which the judge reproduced. The design note's four-way spread (0.1, 0.4, 0.5, 0.3 MGD) matches the judge's fork table. The declared distractors do not carry the task: nothing was named as the surface read. **Gate G: pass.**
**Gate H:** domain: pass, layers: pass, decisive_step: analytical. This agrees with the card's `domain_test`. The judge's residual risk is that reading "No stoppage" as an above-2-MGD statement draws on the agreement text, so a grader might call it semantics. The estimator choice after that reading carries the stump.

## Stump power (Gate F)
The easy routes (gauge only, or gauge plus the 14 measured years) file 0.1 or 0.4 MGD. The shortfall of 0.232 MGD sits away from the block edges at 0.2 and 0.3, so a miss is not noise. No shipped file names the method.

## Findings, ranked
1. None blocking.
2. Open, not a determinism item: the 25-plus rubric count is unverified here and rests on the ship-time rubric run.
3. Optional, no rerun: state in the solution that climatic year 2025 is excluded because it is provisional, and state the chart's plotting-position convention (graded loosely).

## Next action for the author
Proceed to ship: confirm the generated rubric reaches 25 or more criteria, then cut and ship. No rerun of the judge is needed.
