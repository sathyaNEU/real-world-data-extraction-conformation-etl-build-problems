# determinism-check report, task268, 2026-10-31

## Verdict
NOT_DETERMINISTIC (one supplementary answer only: deck item 4, the loose-coffee kilogram grid). The main call, the overlap CSV and the multibuy grid are forced and reproduce. No SOLUTION_WRONG.
**Disposition:** FIX_NOW (the counter ask only; the home and overlap data and the stump stay frozen). If the counter payments have to be regenerated, the repair is still confined to the counter ask.
**Stumping type:** mechanism: etl_conformance (entity resolution of the unit of analysis), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread verdict: /tmp/determinism-check-task268-20261031184538/verdict.md (one pass, one thread, target.zip 8783d495).

## Why
Oro Rosso 1,857 / 741 / 40%, Nordhavn 1,568 / 764 / 49%, gap 9 points, is forced by a long but determinate join: till receipt to Faircourt SALE row on terminal, amount and time, then card_ref to home. Refund netting, order date, order version, STORE cards, REPLACED folding and cancelled orders leave the ranking and percentages unchanged. The unit "home" is named in the prompt, and card_ref is the only cross-key shipped.

Ask 4 (kg to one decimal per guest roaster per quarter) fails Gate C (underspecified_objective / competing_defensible_answer). The files do not fix which label-to-payment assignment is the sale.
1. 122 of 178 unresolved card sales have both a label-containing and an accessories-only decomposition with the same total (for example 10.20 = a 10.20 label, or gift box 6.00 + filter papers 4.20). Another 14 have two equal-size label sets. The 25-minute label window is in no shipped file.
2. Cash lines (4,481) match labels by price with no filed window (observed lag 5 to 95 minutes). 114 have two same-priced candidate labels.
3. The scale 2 re-dating offset is a window (248,110 to 248,113 minutes), not a value. The quarter result does not move on it.
With every ambiguity pushed to its low or high reading, the grid spans 6 to 13 kg per roaster-quarter. The golden (Glenmore 514.0 / 503.0 / 521.2 / 541.9) sits near the top of the band, and a consistent rule lands 0.2 to 0.8 kg off most cells.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Card receipts matched to one SALE row | 50,047 | 50,047, unique | yes |
| Homes that bought coffee | 3,802 | 3,802 | yes |
| Oro Rosso | 1,857 / 741 / 40% | same | yes |
| Nordhavn | 1,568 / 764 / 49% | same | yes |
| Halloran's, Cafetto, Bellvale, Kinvara, Westquay | 51, 52, 52, 56, 79% | same | yes |
| Gap | 9 points | 9 | yes |
| Multibuy grid (20 cells) | as filed | same; 4 cells need 7 ADJ lines on two-deal receipts resolved by value and quantity | yes |
| Loose coffee grid (12 cells) | as filed | band 6 to 13 kg wide, golden inside it | NO |

## Competing answers that survived
- Ask 4 fork: labels paid by card as the label-containing set against accessories alone (and the equal-size label sets). The shipped rule meant to close it is absent: the 25-minute window and the unpaid-label convention are filed nowhere. Open.
- Main call: none survives. The card or account unit files Nordhavn (16.5%), and cards only or cards plus unlinked online files Westquay (25.6%). The brief's "home" and Rewards terms 2.1 and 2.2 rule these out (design SF1). Residual note: no file states that a shared card_ref marks one home.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 6 (pdf, csv, xlsx, parquet, json, docx) | yes |
| Large file | 25,000 rows or more | settlement 257,557; till lines 73,375 | yes |
| Distractors | 2 or more, in metadata, no file name labels one | catchment_households_census2022.csv and coffee_brand_tracker_2026.xlsx in metadata.json; names do not label them | yes |
| Distractors unused yet weighable; none answers a graded quantity | required | Thread found them unused by the solution. I did not re-run the check that none reproduces a graded quantity arithmetically. | partial |
| Deliverables | 1 to 3, all in golden | 2 (pptx, csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | the prompt's last sentence states them; asks are grids | yes |
| Prompt shape and rubric 25 or more criteria | identifiable; 25 or more | The shape is a per-rival, per-roaster-quarter, per-supplier-quarter grid. The rubric is generated downstream and was not available to count. | not verified |
| Reads as real work product | required | no authoring language found by the thread; golden realism not re-judged | yes |

## Gate G reconciliation
The thread's decisive step is analytical, with the easy route being the per-card or per-account share (Nordhavn at 17%). It names no distractor as the surface read, so the distractors are not too load-bearing. It gives mechanism etl_conformance and stumping_family analytical_non_defect. The design note and card agree on the substance:
- the card has `stump_class: analytical`, with an analyst_test and domain_test that match the thread's easy route;
- the ladder's R1 (Nordhavn at 16.5%) and R3 (Oro Rosso at 39.9% against Nordhavn at 48.7%) match the thread's figures exactly;
- the card carries no mechanism, stumping_family, surface_read_dependency or sole_data_defect values to compare against.
No mismatch. The thread flags one risk: home linking is an inference no file states, so a reviewer may read it as a hidden rule. SF1 closes it with the brief's "anyone in it" and the terms' one-member cards.

Gate H line: domain pass, layers pass, decisive_step analytical. This is the duplication-of-purchase table at the household unit, which is the field's market-structure method. It is not a standard-method pass, because the household assembly via the bank-card match is the judgment the data must settle.

## Stump power (Gate F)
Moderate to good. The card-level route needs no settlement join and files Nordhavn. A solver who does the join but links cards only files Westquay at about 26%. Only the full home build lands Oro Rosso. The ask-4 defect does not touch the call.

## Findings, ranked
1. Ask 4 (the loose-coffee grid) is not determinate at one decimal. The labels-versus-accessories decomposition is ambiguous, the 25-minute window is unfiled, cash-line matching has no window, and the band is 6 to 13 kg wide. Fix: rebuild the counter payments so that every card sale decomposes into exactly one label set. That means no label price equals an accessory sum inside the window, and no two same-priced labels share a window. File the convention in coffee_counter_price_board_2026.pdf or the brief: labels paid by card within N minutes, cash lines within M minutes, unpaid labels not sold. Then restate the grid from the rebuilt pack. Rounding to whole kilograms does not help because the band exceeds 0.5 kg.
2. The scale 2 re-dating offset is a window, not a value. This is minor because no quarter moves. Fix: pin the offset, or make the S2 label dates recoverable by one rule in the price board PDF.
3. Optional: no file states that a shared card_ref marks one home. Fix: leave it, since adding a sentence lowers stump power. Keep SF1's closure.
4. The design note's fork table has no row for the counter ask. Fix: add the forks above (with their closures) to the fork table and assert them in checks.py after the rebuild.

## Next action for the author
Run /fix-determinism on ask 4 only. Regenerate the counter payments so each card sale has a unique label decomposition, file the label and cash windows and the unpaid-label rule in the price board PDF, and re-state the loose-coffee grid. Keep the home, overlap and multibuy data byte-identical, then re-judge once.
