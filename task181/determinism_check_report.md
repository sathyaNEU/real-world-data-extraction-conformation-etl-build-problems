# determinism-check report, task181, 2026-10-12

## Verdict
NOT_DETERMINISTIC (the main call holds; two supplementary answers are not uniquely forced). Failure type: competing_defensible_answer.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call (Tarvik only, 72.4 against 40.0) recomputes exactly from the files. Gate failures: (1) the delay column holds only if slot plans whose ifplid is absent from the FDPS archive are dropped, and no shipped file says so (709 slot rows, 662 plans); read literally all eight values differ at two decimals. (2) The pptx rate table for the seven non-Tarvik sectors holds only under a pooled loss-per-pair ratio; a per-sector ratio moves them (Linmark 25.6 rather than 24.1, Lysvik 24.9 rather than 26.4, and others). The call is unchanged but the "Lysvik next highest at 26.4" figure is open.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| ATM-related SMI (D or I), 1 Jan 2025 to 30 Sep 2026 | 96 | 96 | yes |
| Losses that are crossing pairs in their sector | 96 of 96 | 96 of 96 | yes |
| Crossing pairs in the record | 392,294 | 392,294 | yes |
| Losses per 10,000 pairs, pooled and by sector | 2.45; 2.31 to 2.59 | 2.45; 2.31 to 2.59 | yes |
| Losses per 100,000 hours, whole record | 13.8 to 24.2 | 13.8 to 24.2 | yes |
| Tarvik 2027 pairs / hours | 48,545 / 16,414 | 48,545 / 16,414.1 | yes |
| Forecast rate, Tarvik | 72.4 | 72.4 | yes |
| Forecast rate, others (pooled) | at or under 26.4 | Lysvik 26.4, Hallin 24.9, Mosby 24.8, Karrow 24.2, Linmark 24.1, Grendal 23.5, Sandvik 18.9 | yes, pooled only |
| Forecast rate, others (per-sector ratio) | not claimed | Tarvik 72.5, Linmark 25.6, Lysvik 24.9, Hallin 24.8, Mosby 24.7, Karrow 24.0, Grendal 23.9, Sandvik 19.0 | competing answer |
| Delay/flight (Tarvik, Mosby, Grendal, Linmark, Karrow, Lysvik, Hallin, Sandvik) | 0.53, 0.41, 0.43, 0.16, 0.29, 0.55, 0.27, 0.10 | with ifplid filter: same. Without: 0.59, 0.50, 0.50, 0.19, 0.34, 0.66, 0.32, 0.11 | only under an unfiled filter |
| Hours open as own sector | 1,532.1, 1,310.5, 735.3, 1,202.3, 771.1, 1,410.2, 971.6, 1,301.9 | same | yes |
| ACAS RA encounters (deduplicated) | 8, 9, 10, 7, 4, 7, 3, 2 | same (68 rows to 50 encounters) | yes |

## Competing answers that survived
1. Delay, plans not in FDPS: dropping them gives the golden; keeping them gives 0.59/0.50/0.50/0.19/0.34/0.66/0.32/0.11. 574 of the 709 rows match a flown callsign, date and route under another ifplid (refiled). The extract notes do not close it.
2. Forecast ratio, pooled over eight sectors (golden) or per sector: same call, different rates for seven sectors at one decimal. The design note's fork table row 7 asserts "sector rates give the same set" but that covers the over/under set only, not the printed rates.
3. Minor, literal text favours the golden: five "bandboxed briefly... reopened 5 min later" remarks with no logged change. Deducting them gives Tarvik 1,531.7. The OM says a change takes effect at the logged time, so leave it.
4. Main-call method (judged recoverable, not a fork): no file states crossing pairs. The data separates the candidates (96 of 96 losses are crossing pairs while crossing pairs are about 10 percent of overlapping pairs; loss per pair is flat across sectors). Touching counted as crossing still gives Tarvik alone (69.6 pooled).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 15 | yes |
| Formats | 3+ | 6 (pdf, csv, parquet, json, xlsx, md) | yes |
| Largest file | 25,000+ rows | 1,693,315 (parquet); planning csv 308,913 | yes |
| Distractors | 2+ named in metadata.json, none labelled in file names | controller_roster_summer2026.xlsx, met_cb_activity_summer2026.csv; names carry no label | yes |
| Distractors relevant and unused | same world, ruled out by a shipped fact | judge found two present and not the surface read | yes (judge did not name either as the read carrying the task) |
| Deliverables | 1 to 3 | 2 (pptx, csv) | yes |
| Deliverables present | all named | golden/ holds both | yes |
| Multi-dimensional asks | yes | per-sector rates against the line, delay, hours, ACAS across eight sectors | yes |
| Units and rounding stated | yes | delay two decimals in minutes, hours one decimal, encounters whole; the forecast rate table has no stated rounding or unit in the prompt | NO (prompt asks for "forecast rate" with no unit or rounding) |
| Prompt shape and 25 criteria | shape identifiable, 25+ | shape 01 in metadata.json; rubric is generated at grading and not checked here | shape yes, count not verifiable |
| Realism | no LLM tells, goldens read as work products | judge found no authoring disclosures and realistic orphan ifplids; golden realism not independently reviewed | pass on judge's read |
| Prompt length | one paragraph, under 1,000 characters | 619 | yes |

## Gate G reconciliation
Judge: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; the stump is forecasting from flight hours when losses follow the climbing or descending pairs; "no reported number is wrong". Consistent. The hours-based close-out table is the surface read but does not rank sectors for 2027, so it is not a Gate G artifact. Neither declared distractor was named as carrying the task.
Gate H: domain pass, layers pass, decisive_step analytical. The card's domain_test (controller workload and vertical interaction) matches the judge's.
Note the two failing items are supplementary or presentation determinism, not the stump, so the build reads the same shape from outside as inside.

## Stump power (Gate F)
Likely strong. The natural path (2026 per-hour rate times 2027 hours) gives "no sector" (Mosby 32.0), and the trend path gives Grendal/Hallin on one extra loss each. Reaching Tarvik needs testing what the 96 losses share and rebuilding exposure on the new Brekka climbs and descents (5,520 EXBK flights against 0 in the record). The pair work is heavy, so some failures will be effort rather than analysis. No too-easy signals named.

## Findings, ranked
1. extract_notes_2026-10-12.md: state that slot plans whose ifplid is not in the FDPS archive are not counted as flights, so the delay column is forced. Regenerate the golden only if the filter is stated the other way.
2. Prompt or extract notes: fix the forecast ratio (pooled over the eight sectors) so the printed rates are determinate to one decimal. Alternatively word the table column so only the sector(s) over the line are graded.
3. prompt.txt: give the forecast rate a unit and rounding in the asking sentence (per 100,000 flight hours, one decimal).
4. Optional: one sentence in the notes that the record can be tested for what the losses share, leaving the pair method open. Main call, Tarvik figures, hours-open and ACAS columns stay frozen.
5. Any earlier runs on the delay column and the table's non-Tarvik rates should be regraded or rerun after the pins.

## Next action for the author
Add the ifplid exclusion line to the extract notes and the pooled-ratio plus unit/rounding wording to the prompt or notes, rebuild byte-identically, and re-judge once.
