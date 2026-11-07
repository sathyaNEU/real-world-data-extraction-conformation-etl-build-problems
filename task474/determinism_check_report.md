# determinism-check report, task474 (architecture 7), 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, sonnet, medium, scratch /tmp/determinism-check-task474-a7/ (verdict.md there). target.zip sha256 1fc4d13f...00b4d.

## Why
AP-3 section 2 files the estimand (lowest raw mark that no larger share of an equivalent group reaches than reaches 65 on Brindle's scale). The 1,164 candidates who failed their single Brindle sitting and sat Harrowgate next are the only group measured on both papers. Brindle's own first-sitting-fail resits matched on first score give their expected 65+ share, 28.0%. Harrowgate: 37 reaches 32.2%, 38 reaches 25.3%, so 38. Margins are clean (2.7 points above 38, 4.2 below 37). Every committed answer reproduced from the shipped files.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cross-switchers | 1,164 | 1,164 | yes (brindle csv, harrowgate json, register) |
| Matched resit share at 65+ | 28.0% | 28.02% (14,503 resitters) | yes |
| Harrowgate share at 37 / 38 | 32.2 / 25.3 | 32.2 / 25.3 (39: 19.4, 40: 13.7) | yes |
| Ask 3, nine months of first-time / resitting | as filed | all nine match | yes |
| Ask 4, 2021-25 first sat / passed | as filed | all five match | yes |
| theory_results_2026.csv rows | not filed | 16,388 (3,585 Brindle SAT + 12,803 Harrowgate cleared/released) | n/a |

## Competing answers that survived
None on the main call. Rivals: 40 (2025 first-time rate carried over, the declared default path), 39 (all sittings), 35 (resitters only), 36 (cross-switchers against 47.2%), 37 (unmatched pooled resit rate, 34.6%). Variants of the Brindle side all give 38 (resit windows 2020-25, 2020-24, 2024-25, 2025 only; gaps; 5-point bins; score-only or sitting-and-score matching). Only first sittings after Oct 2025 alone give 36, a censoring artifact the judge did not accept as a rival.
Advisory forks, graded-file only, not the main call:
- "the person's board number" is undefined when a person holds two. The earliest registration is the natural pick but no file states it.
- The chart population (sittings or distinct people) is open; only the 38 line is checkable.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 10 files, 5 formats (csv, json, xlsx, pdf, eml); Brindle csv 88,912 rows, register 63,659 | yes |
| Distractors | 2+ in metadata, none labelled by file name | harrowgate_item_statistics_2026-09.csv, candidate_feedback_2026.xlsx; names carry no label | yes |
| Distractors unused yet weighable, none answers a graded quantity | yes | item stats has check-key notes on Q20/Q29 but no response data; survey decides nothing | yes |
| Deliverables | 1-3, all in golden | 2 (pdf, csv), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | monthly and yearly grids; "every figure is a whole number of candidates or marks" | yes |
| Prompt shape and 25+ criteria | yes | shape 15; design note records 29 ask criteria | yes (relies on design note count) |
| No LLM tell / goldens read as work products | yes | judge found none; messy-system data coherent | yes (golden realism not re-read here) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g method_or_model_selection, stump_class analytical, layer2 estimation_fit. Match. Neither distractor is named as the surface read; the declared trap is the 2025 first-time pass rate (40). Gate H (thread): domain pass, layers pass, decisive_step analytical. Matches the design note's Three rules and the card's analyst_test and domain_test.
Minor discrepancy: the design note's ladder gives 41 for the cross-switchers side by side, and the thread's cross-switchers-against-47.2% variant gave 36. These are different constructions, both off 38, so no effect on the call. The note's rung 2 label is worth a glance.

## Stump power (Gate F)
Judge: good, for an analytical reason. Landing 38 takes two ideas, the cross-switch group as the equivalent group and the retest gain handled through Brindle's matched resits. The thread flags a mild risk that a strong run goes straight to the cross-switch group and gets it right. The thread did not class this decisive step as textbook-landable; the main thread should weigh the risk against the note's ladder.

## Findings, ranked
1. No blocking finding.
2. Advisory: "the person's board number" is not filed (CSV only). Fix: optional one-clause pin (earliest board number registered) in prompt.txt, which changes what solvers see, so only if the author accepts a rerun; otherwise leave.
3. Advisory: chart population is open between sittings and distinct people. Fix: none needed; only the pass-mark line is gradable.
4. Advisory: ladder rung 2 (41) differs from the thread's side-by-side result (36); check the note's rung is a different construction. Fix: reconcile the note wording, no pack change.

## Next action for the author
Proceed to ship; optionally add the earliest-board-number clause to the CSV ask only if willing to rerun the judge.
