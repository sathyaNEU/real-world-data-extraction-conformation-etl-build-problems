# determinism-check report, task118 (architecture 5), 2026-10-31

Judge thread output: /tmp/determinism-check-task118-20261031183742/verdict.md (one pass, one thread, target.zip 26845106).

## Verdict
NOT_DETERMINISTIC (supplementary ask 5 only); SOLUTION_WRONG on the write-up's step 5. The main recommendation and asks 2, 3, 4, 6, 7, 8 are forced and reproduce.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: forecasting (conditional expected reduction at the design-year peak hour's run day), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Main call forced: Appendix B peak hour (23 Jul 2027 18:00, 114.6F, 1452 MW) is the 4th consecutive OP-7 event day (20 to 23 Jul; 24 Jul is a Saturday). Fourth-day reductions at 18:00 MST: Cool Credit 0.248 kW x 12,307 = 3 MW, Peak Time Rewards 0.0753 x 50,000 = 4, BDP 14.6 kW x 133 = 2, Home Battery Network 2.90 x 2,133 = 6. Margin 6.2 vs 3.8, robust to the estimator.
Ask 5 reproduces all 19 counts only under two rules no shipped file states: IDLE counts as online only from 7 July (an inference from halvern_unreachable_devices), and a device retired before the event hour is excluded even if its last status row is ONLINE. The write-up's step 5 omits the retired rule, giving 9,376 against the golden 9,375 on 6 Aug 2026 (premise 3203514850, device H22RX373A).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Peak hour / run day | 23 Jul 2027 18:00, 4th day | same | yes |
| Cool Credit MW | 3 (0.248 kW) | 3.05 | yes |
| Peak Time Rewards MW | 4 (0.0753 kW) | 3.76 | yes |
| BDP MW | 2 (14.6 kW) | 1.94 | yes |
| HBN MW | 6 (2.90 kW) | 6.2 | yes |
| Ask 5, 19 event days | 8,696 to 9,545 | all 19 only with IDLE-from-7-July and retired rules | yes under unstated rules; step 5 text gives 9,376 on 6 Aug |
| Ask 6 HBN incentive | 132,735 / 399,825 / 248,790 / 9,480 | same | yes |
| Ask 7 cap premises | 2,939 | 2,939 | yes |
| Ask 8 BDP kW | 14,903 / 16,438 / 17,324 / 17,830 | same, with register filter | yes (112 non-register rows are a minor fork) |

## Competing answers that survived
- Ask 5, IDLE never online: 100 to 967 fewer on 16 of 19 days. IDLE always online: +304, +255, +5 on the three June days. IDLE online when not listed unreachable that day: 2 to 24 fewer every day. No retired filter: +1 on 6 Aug. No registry replacement matching: 426 to 523 fewer. No shipped file defines IDLE or the unreachable log, so the golden stands on an inference. This is the one failing fork.
- Ask 8, register filter: without it 17,474 / 19,009 / 19,893 / 20,384. Rated a minor risk by the judge (CBMU meters are 8 digits, 112 rows on 27 sites are 9-digit), but filing the population is cheap.
- Ask 8 latest versus first row, and ask 6/7 UTC date versus MST date: closed by the shipped text (supersession; schedule 2.2 "in all"; OP-7 MST window).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 21 / 4 (csv, pdf, xlsx, json) / 504,000 rows | yes |
| Distractors | 2+ in metadata.json, none by file name | regional_capacity_price_outlook_2025-2027.csv, dr_customer_survey_2026.xlsx; file names do not label them | yes |
| Distractors unused yet weighable | yes | judge also treats cbx_daily_weather as a plausible distractor; the named two are unused by the solution | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, csv), both present | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 19-day, 4-month and 4-month grids; unit and rounding in the prompt's last sentence | yes |
| Prompt shape and 25+ criteria | 25+ | note counts 33 plus two files | yes |
| Reads as LLM generated / golden realism | none | judge found no tell in the files; goldens not re-read by me | yes (judge hygiene PASS) |

## Gate G reconciliation
Thread: mechanism forecasting, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; the stump is the fourth-consecutive-day reading with the naive route on Cool Credit at about 11 MW, strategy `binding_constraint`. These match. The thread names no declared distractor as the surface read, and the naive all-event average (Cool Credit 11 MW) is the intended default path, not a shipped wrong ranking. Gate G passes. One note: the design note intends IDLE as a silent-switch ask device; that is allowed on asks, but the literal reading must still close it (see Findings).

## Gate H line
domain: pass; layers: pass; decisive_step: analytical. Matches the card's domain_test (design-year peak-hour accredited capacity, load-impact estimation) and analyst_test (average or weather-matched reduction files Cool Credit at 11 MW). The asks (IDLE, retired, register filter) are semantics and rule application, which the rules allow on asks.

## Stump power (Gate F)
The judge finds a real stump: reduction falls by run day for Cool Credit (1.12, 0.76, 0.49, 0.25 kW), Peak Time Rewards and BDP, while the battery fleet is flat. A strong analyst averaging over events files Cool Credit (11 vs 6 MW) and loses the call. The decisive step is a run-day state the analyst must recognise, not a reading or rule. No landable-by-method-alone concern was raised. I did not weigh it against the design note's ladder beyond this.

## Findings, ranked
1. Ask 5 is not literal-deterministic: the IDLE rule (offline before 7 July, online from then) and the retired-device exclusion are stated nowhere in the bundle. File the WHAT of "online" (what IDLE means and whether a retired device counts), not the inference method.
2. Solution step 5 is wrong as written: it omits the retired rule and gives 9,376 on 6 Aug against the golden 9,375.
3. Ask 8 population (register meters only) is a minor open fork; file it.

## Next action for the author
Apply the coordinator's planned fix in the generator, then run the one re-judge (not a second pass in this report):
- File the IDLE status meaning and retired devices for ask 5 in the governing document.
- File the register-meter population for ask 8.
- Correct step 5 of the solution so it states the retired rule and reproduces 9,375 on 6 Aug.
- Keep the main call, ladder and graded figures for asks 2, 3, 4, 6, 7 byte-identical. The judge says only the ask 5 and ask 8 runs need a re-read.
Re-check that the new text names the IDLE meaning without stating the date inference as a method. Check also that it matches the golden (IDLE offline before 7 July, online from then), or the golden must change.
