# determinism-check report, task166, 2026-11-02

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium) recomputed every committed answer from a fresh unzip of target.zip and reproduced them. The main call lands on 1.80M (filed 1.75M) with hardbacks 1.075M (filed 1.0M); asks 3 to 5 reproduce exactly (504,983 copies, the 24 channel-by-quarter cells, every write-off share). The decisive segment, hardbacks whose own paperback follows within 8 months, is cleanly separated in the data (matched gaps 126 to 161 days against 350 to 427 days, nothing between), so any cut-off from about 5 to 11 months gives the same segment. The terms of trade and policy PDFs file every rule the golden uses.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Allowance | 1,750,000 | 1,801,556 (rounds to 1.75M) | yes |
| Hardback part | 1,000,000 | 1,075,403 (rounds to 1.0M) | yes |
| Copies received in window | 504,983 | 504,983 | yes |
| 24 channel-by-quarter cells | filed grid | identical | yes |
| Channel write-off shares | 5.7 / 10.2 / 6.8 / 12.0 / 4.6 / 8.8 | 5.665 / 10.150 / 6.770 / 11.955 / 4.564 / 8.792 | yes |
| Format shares | 6.5 / 7.2 / 6.6 | 6.539 / 7.169 / 6.596 | yes |
| Hardbacks within 8 months of paperback | segment | 51 of 605 (550 matched) | yes |

Online 10.1501 sits a hair above the 10.15 boundary but is exact from the files.

## Competing answers that survived
- Easy route (one hardback curve by format and channel): 1.358M / 0.632M, filed 1.25M / 0.75M. It does not survive: the data show the close segment developing at 0.54 ultimate for Chain against 0.21 for general hardbacks.
- Expected ultimate less credits already given: about 1.92M / 1.14M (bins 2.0M / 1.25M). The thread flagged this as the one residual method fork. Since the verdict it is closed in the design note as fork-table row SF15, asserted in generator/checks.py: struck at 31 October 2025 that estimator overshoots the credits that followed by 14.2 per cent against 0.2 per cent for the golden's construction (2024: 1.1 against 0.6). The record refutes it. This closure is cited from the coordinator and the design note; the thread did not see it and I did not re-run checks.py.
- Line-level clipped variant: 2.23M, unsound method. Restocking value netted off: contradicted by the terms ("whatever its condition").
- Pattern and chain-ladder variants (format-only, pooled channels, maturity 400 to 500 days, quarter-cohort chain ladder): all round to the golden except the easy-route family. Margin to the rounding line is about 4 per cent on both figures, thin but not contested (every valid variant stays in band).
- Known limit: the 51 close hardbacks are mostly autumn 2026 titles with little mature history, so the segment curve rests on the earlier close-paperback hardbacks.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | 4 (sqlite, csv, xlsx, pdf) | yes |
| Large file | 25,000 rows or large DB | sqlite ledger 342,911 rows, 32 MB | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | print_orders and stock_on_hand named; UK consumer panel is a third, unnamed, unused | yes |
| Distractor quality | unused, weighs, ruled out by a shipped fact, none reproduces a graded quantity | judge found all three plausible and unused; the stump never depends on them | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 24-cell grid, channel and format shares, nearest 250,000, one decimal | yes |
| Prompt shape and 25 or more criteria | identifiable, 25 or more | shape identifiable (every cell and share is graded); the criteria count is generated downstream and I did not count it | not verified |
| Not LLM-looking, goldens realistic | yes | judge found mixed date formats, legacy ids, hyphenated ISBNs, system-like; golden realism not independently reviewed by me | yes (pack) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Forecasting, analytical stump (develop the autumn 2026 hardbacks on their own paperback-timing pattern, not the history's). These agree (the note's forecasting/reserving is the thread's segment-development method selection). Neither names a declared distractor as the surface read: the thread's easy route is the general hardback curve, not print orders or stock on hand. No planted defect carries the main call; the duplicated-delivery rule is an ask-level element only. Gate G passes.

## Stump power (Gate F)
Moderate to good. The easy route (one hardback curve by channel, or a trailing rate) back-tests well at 2024 and 2025 and files 1.25M / 0.75M, one band low on both figures. Finding the segment needs a fuzzy contributor-and-title match on the title master that no file hints at, and the effect is invisible without it because the close hardbacks are mostly new. One caution for the main thread: the thread did not class the decisive step analytical merely because chain ladder is the field's method; it reached the golden by finding a driver the data had to settle (the match), so this is not a landable textbook route. Argue the ladder against the design note's rungs as usual.

submission.md step 5 now states the golden construction's own back-test (0.6% below at 31 October 2024, 0.2% above at 2025, figures in generator/figures.json, figures_check 65 of 65). Added after the verdict; it moves no graded figure or pack file.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test fails to carry over (a discharged patient has no successor edition; the deciding quantity is a returns development by age and segment, the reserving analyst's own estimate). Layer 1: format codes, legacy account numbers, hyphenated ISBNs, date formats, a re-sent export, repeated deliveries, surname-first names. Layer 2: segment the development pattern on the paperback timing and project remaining returns by age. Easy route: one hardback curve gives 1.36M / 0.63M, filed 1.25M / 0.75M, against the golden 1.75M / 1.0M. Design note's `## Three rules` (No decoy, Not semantics, Not rule application) matches the thread's reading. Sub-point for the main thread: the title match is a data-join step, but it builds the estimand's segmentation rather than deciding by reading a field, and the 18-versus-60 development families in the note show the step, not rule execution, moves the answer.

## Findings, ranked
1. None failing. Hygiene PASS (11 files, 4 formats, nothing exclusion-level).
2. Residual SF15 fork closed by the record (see above); optional: none required.
3. Margin about 4 per cent to the 250k rounding line on both main figures; robust across variants.
4. Rubric 25-criteria count not checked by me.

## Next action for the author
Proceed to ship; re-run the free gates on the final cut as stage 5 requires.
