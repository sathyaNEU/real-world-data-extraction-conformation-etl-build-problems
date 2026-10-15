# determinism-check report (pass 2), task460, 2026-10-15

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated thread (sonnet, medium) read only the fresh unzip of the rebuilt target.zip plus the inlined blocks. It reproduced all 8 stores' avoided t/MWh, metered use, share supplied and price paid. The 0.31 t/MWh gap to Halvane held under every hour-resolved first-difference variant it tried (grouping by hour only, month x hour, 24-hour differences, regressing on demand, excluding solar). The determinism block's earlier finding (invoice rebills, Ardley wholesale quantity, tax lines) now reproduces from the filed data dictionary. No gate A to E failure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Gorsefield avoided t/MWh | 0.89 | 0.891 | yes |
| Halvane | 0.58 | 0.579 | yes |
| Tennaford / Brackwell / Quillbury / Kestrel / Faraview / Ostlemere | 0.41 / 0.40 / 0.39 / 0.39 / 0.39 / 0.39 | 0.408 / 0.402 / 0.390 / 0.389 / 0.388 / 0.388 | yes |
| Gap to Halvane | 0.31 | 0.310 to 0.312 | yes |
| Use MWh (Gors, Halv, Tenn, Brack, Quill, Kest, Fara, Ostl) | 2,589 / 2,506 / 2,468 / 2,381 / 2,368 / 2,472 / 1,984 / 2,862 | identical | yes |
| Share % | 28.3 / 27.1 / 26.9 / 26.5 / 22.7 / 27.5 / 23.9 / 30.2 | identical | yes |
| Price $/MWh | 145 / 142 / 136 / 155 / 184 / 226 / 123 / 169 | identical | yes |
| Brackwell average rate | 0.85 t | 1876.2 lb | yes |
| Quillbury non-baseload rate | 1.11 t | 2453.5 lb | yes |
| Single all-hours marginal rate, Tennaford | 0.83 | about 0.83 | yes |
| Plant register CO2 vs hourly sum | tie | within about 0.003% | yes |

## Competing answers that survived
No fork moves the main call. Three weak forks, none closed by a filed sentence:
- Fossil-rate fork: one area fossil output rate instead of the fuel-specific coal/gas/oil rates makes Tennaford first (about 1.06). The workbook publishes fuel rates and the hourly data carries fuel generation, so this is a weak alternative.
- Level-regression fork: CO2 on net-generation levels by hour puts Faraview (about 0.64) above Halvane as first left out. It is seasonally confounded and is not the charter's "one MWh less" counterfactual.
- No-intercept slope: 0.96 vs 0.68, gap 0.29. Not a standard estimator.
The estimator (differences, with intercept, fuel-specific CO2) is not filed; the design note's fork table closes it by method (the charter's counterfactual). Optional tightening, only if a portal finding arrives: file the WHAT (CO2 from each fuel's published 2025 rate; change-on-change estimate), not the grouping.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | 70,080 (hourly data, array model) | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | edc_generation_emission_rates_2024.xlsx, ardley_power_content_label_2025.pdf. The file names do not call them distractors. | yes |
| Distractors unused yet weighable | yes | Both unused by the solution. The 2024 rates carry stale numbers and the Ardley label gives one 826 lb figure for every store. The data dictionary and the edition years rule them out. | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | eight stores times five figures, with unit and rounding in the sentence | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 01; the design note counts about 40 arithmetic criteria. The rubric is generated downstream, so this is not verifiable here. | yes (design count) |
| Not LLM-generated / realism | yes | the thread found no authoring language | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note declares Gate G method_or_model_selection and the stump a margin estimated from hourly changes, weighted by array output. The thread's wrong routes are the published average rate (Brackwell), the non-baseload rate (Quillbury), one pooled marginal rate (Tennaford) and hour-misaligned bins. These match the design note's analyst-test list. The thread did not name either declared distractor (2024 workbook, Ardley label) as carrying the task. Match.
One observation: the 2025 workbook's average and non-baseload rates are wrong-basis figures for the decision. They are published agency inventory figures that the workbook's own notes define and that rank the stores by the wrong measure. They are not listed as distractors in metadata.json, and the design note treats them as "correct numbers for another question". The thread treated them as analytical wrong routes and not as a Gate G breach, because they are not a shipped artifact that answers the decision question.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. This matches the card's analytical stump class and the design note's `## Three rules` (decisive step: season x hour marginal rate from hour-to-hour changes, weighted by array output).

## Stump power (Gate F)
Moderate to good. The charter points toward a marginal concept without naming it, so a strong model may reach it. The pulling wrong routes are Brackwell (average), Quillbury (non-baseload), Tennaford (pooled margin) and clock misalignment. Many wrong sites, 2-decimal ranking and the invoice asks (rebills, loss-adjusted Ardley quantity, tier summing, proration, gas exclusion) add independent failure room. Risk of too easy: moderate.

## Findings, ranked
1. Estimator not filed (fuel-specific CO2, differences with intercept). Three weak forks, none moves the call. No action unless the portal raises it.
2. Minor dating inconsistency: the pack files (corvane_pilot_store_sites.csv and others) are stamped as of 2026-10-23, after the charter's 15 September 2026 approval that cites them. Today is 2026-10-15, so the stamp is also in the future. The thread flagged it as non-exclusionary.
3. The hourly slopes are very clean step functions, which reads as designed. It is not disclosed anywhere.
4. Neither the thread nor I checked rubric criterion counts.

## Next action for the author
Proceed to stage 5 (ship). Optionally align the pack's as-of date with the charter's approval timeline before shipping.
