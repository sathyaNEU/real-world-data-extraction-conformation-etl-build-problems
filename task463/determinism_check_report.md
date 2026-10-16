# determinism-check report, task463, 2026-10-16 (pass 2, replaces the first pass's report)

Judged cut: target.zip sha256 prefix 08f6b738bb357228 (fresh unzip at /tmp/determinism-check-task463-p2/target/). The shipped cut differs from the judged cut only in statistics_kellesay_product_classification.csv (valid_from dates moved from 1 January 2019 to the office's summer 2025 batch dates, which no figure reads). Thread verdict: /tmp/determinism-check-task463-p2/verdict.md.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Applying plan sections 3.1 to 3.6 and 4.1 literally to the shipped feeds reproduces all sixteen rates, the 13/3 split and asks 1 to 4. The nearest moving item is Breakfast cereals (0.82 against the 1.5 line), the nearest staying item Pasta and rice (2.32). Direct Törnqvist, direct Fisher and GEKS over 13 months give the same sixteen rates to one decimal. The two ask-level forks from pass 1 (unit of days, CSV scope) are closed by the prompt pins.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Product-month rows / lines / lines compared | 14,364 / 1,172 / 1,012 | same | yes |
| Lines per item | 62, 75, 67, 77, 66, 62, 43, 87, 60, 50, 87, 37, 41, 56, 43, 99 | same | yes |
| 12-month rates (direct Törnqvist) | 1.4, 2.6, 4.7, 2.7, 1.7, -0.2, 1.4, -0.3, 5.6, 1.7, 2.2, 0.6, 1.7, 2.6, 2.6, 2.5 | same (Fisher, GEKS agree to 1 dp) | yes |
| Published rates, sheet 12-month rates | 1.1, 1.8, 2.4, 2.6, 1.4, 2.7, 1.4, 2.5, 5.8, 1.4, 2.3, 0.7, 1.2, 2.6, 2.5, 2.4 | same | yes |
| Differences | 0.3, 0.8, 2.3, 0.1, 0.3, -2.9, 0.0, -2.8, -0.2, 0.3, -0.1, -0.1, 0.5, 0.0, 0.1, 0.1 | same (round-first agrees) | yes |
| Move / stay | 13 / 3 | 13 / 3 | yes |
| Days to completeness | 2.0 / 8.0 / 8.6 | 2.0 / 8.0 / 8.615 | yes |
| 2025 coverage (whole %) | 68, 58, 67, 77, 55, 69, 59, 73, 59, 62, 57, 60, 58, 60, 66, 73 | same | yes |

## Competing answers that survived
1. Chained monthly Törnqvist (5 movers: Bread, Pasta and rice, Yoghurt, Butter and spreads, Fruit juice) against direct (13). Plan 3.5 says "compiled monthly" without naming direct or linked; 3.6 defines the rate as the change over the year, and the data rule the chain out (9 items end below every line's own change, which no price change can do). This is the intended method choice, not a semantic gap. The thread's optional pin ("comparing each month with September 2025") is declined by the author because it would file the HOW (the index construction, the decisive step) as a rule; consistent with the file-the-WHAT rule, the residual is accepted.
2. Calderby UTC against local dates (8.3 against 8.6): forced by the dictionary. Wrenfold negative lags kept signed per the filed definition. Gorsedale Trade rows excluded per "retail sales". All closed by shipped text.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 15 / 5 (csv, xlsx, txt, sqlite, pdf) / 287,409-row sqlite | yes |
| Distractors in metadata.json, none labelled by file name | 2+ | rpi_field_quotes_2025_2026.csv, kellesay_retail_sales_index_2025_2026.xlsx | yes |
| Distractors unused yet weighable, ruled out by a shipped fact | yes | field quotes are the published index's inputs; retail sales index is a neighbouring statistic; neither reproduces a graded quantity (thread found no use) | yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, png, csv), all present in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | 16 items x 5 fields, 3 supermarkets, 16 coverages; one decimal / whole per cent stated | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 10 (scorecard); 16 rows x several fields plus days, coverage, chart, CSV gives well over 25 gradable figures (rubric itself not generated here) | yes |
| Reads as real, not LLM generated | yes | thread found operational artifacts, no authoring language | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note stump sentence: default path links twelve monthly Törnqvist comparisons and moves five; direct or 13-month comparison moves thirteen. These match. The declared distractors (field quotes, retail sales index) were not named by the thread as carrying the task. No mismatch. The card was not found in the repo by name search, so card fields (stump_class, analyst_test, domain_test) were reconciled only against the design note's Three rules, which agree. Gate H: domain pass, layers pass, decisive_step analytical (index-number method choice with drift diagnosis; domain is official price statistics, swap test fails).

## Stump power (Gate F)
Real. A strong model linking monthly comparisons (the standard chain, invited by "compiled monthly") files five movers instead of thirteen, Breakfast cereals at -3.6 against 1.8. Detecting it needs checking the index against its lines' own changes. The asks add independent traps (UTC conversion, resends and v2 file, fiscal weeks, Wrenfold 2025 codes, Trade rows, GST).

## Findings, ranked
1. Low: residual direct-versus-chain wording fork on the main call (plan 3.5), excluded by the data; deliberately not pinned.
2. Note: classification CSV changed after the judged cut (valid_from dates only); not re-judged, no figure reads it. Author should confirm the rebuilt target.zip reproduces the same 1,012 lines.

## Next action for the author
Ship: rebuild with the valid_from change, confirm figures_check and byte-identical rebuilds still pass, then proceed to stage 5.
