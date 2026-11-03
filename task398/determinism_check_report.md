# determinism-check report, task398, 2026-11-03

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: counterfactual replay of a path-dependent rule on honest data (method_or_model_selection adjacent), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

One isolated thread (general-purpose, sonnet, medium) on target.zip 896bc527, reading only its own unzip of the bundle
and the submission's blocks inlined in its brief.

## Why
Every committed answer was rebuilt from the bundle to the filed rounding. Review terms 2.1 price a change as the replayed
B Accumulation return less the actual return, and 2.3 runs the fund otherwise as its prospectus requires, so the drawdown
rule (prospectus 4.3 and 4.4) is run on each counterfactual price. With the value sleeve as a tracker the price's deepest
fall below its 63-point high is 6.24 per cent, the overlay never fires and the replay removes 830 bp; the higher trigger
removes 519; the gap, 311, sits far outside modelling noise.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| B Acc return over the year | 2.4% | 2.376% | yes |
| Benchmark TR at 12:00 | 12.1% | 12.093% | yes |
| Shortfall | 970 bp | 971.7 bp | yes |
| Drawdown on 2026-03-20 | 8.7% | 8.697% | yes |
| Reduction 2026-03-23 to 2026-06-08 | yes | reduced 03-23 to 06-08, closed 06-09 | yes |
| Value sleeve as a tracker | 830 bp | 830.1 (deepest fall 6.24% on 2026-04-02, never reduced) | yes |
| Higher trigger (12%) | 520 bp | 519.0 | yes |
| Earlier restoration (6%) | 80 bp | 82.4 | yes |
| Growth sleeve as a tracker | -30 bp | -28.7 | yes |
| Equitised liquidity sleeve | -50 bp | -48.2 to -49.4, quarter-end sizing after the transfer | yes, under that convention (closed since, below) |
| Gap to the runner-up | 310 bp | 311.1 | yes |
| Value and growth dividend income, eight quarters | as filed | to the pound, record-date settled holding times rate, Penrose's November final from Holloway, its March final excluded | yes |
| Value and growth dealing costs, eight quarters | as filed | to the pound, trade date two dealing days before settlement, the open trades counted once | yes |
| AIM holdings and shares at four quarter-ends | 10, 11.9 / 10, 12.3 / 9, 9.2 / 8, 7.5 | 11.942 / 12.286 / 9.232 / 7.541 | yes |

## Competing answers that survived
- The equitised liquidity sleeve's quarter-end sizing: sized on the liquidity sleeve after the quarter-end transfer it
  files -50, on the value before the transfer -60 (-55 to -56 unrounded). The monitor's 2026-03-31 row closed it only for
  a solver who checks. Closed after the pass: the review terms' definition of that change now reads "at the last
  valuation point of a calendar quarter the liquidity sleeve's value is taken after the cash moved between the sleeves at
  that valuation point" (SF31, asserted); the figure is unchanged at -50 (-50.1), the other reading prints -57.8.
- The static attribution (the overlay held at its recorded exposure, value tracker 296 against the trigger 519) is the
  intended wrong route, excluded by terms 2.3 and prospectus 4.3, not a surviving answer.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 20 | yes |
| Formats | 3 or more | csv, xlsx, pdf, docx | yes |
| Volume | one file of 25,000 rows or more | holloway_safekeeping_positions_2025-26.csv, 25,766 | yes |
| Distractors | two or more in metadata.json, none named as such | aov_2024-25_published_extract.pdf, larkspur_100_factsheet_sep2026.pdf | yes |
| Deliverables | 1 to 3, present in the golden | change_pricing_2025-26.xlsx, board_review_2025-26.pptx | yes |
| Asks | multi-dimensional, unit and rounding stated | 24 figures in three asks, rounding in the prompt's last sentence | yes |
| Shape and rubric | 25 or more criteria | shape 01, 38 criteria | yes |
| Realism | nothing reads as generated | Files/Hygiene PASS | yes |

## Gate G reconciliation
The thread's mechanism (counterfactual replay), stumping family (analytical_non_defect), surface_read_dependency (no)
and sole_data_defect (no) match the design note's Gate G (decomposition_attribution: every reported figure is correct and
the call turns on assigning the shortfall to the cause that produced it through the rule's response) and the card's
stump_class analytical. Its Gate H line (domain pass, layers pass, decisive_step analytical) matches the leak reader's
question 6 (an analytical choice). No distractor carries the task.

## Stump power (Gate F)
Moderate to good in the thread's words: the additive attribution with the overlay at its recorded exposure files the
higher trigger first (519 against 296); the golden needs the full path-dependent replay and the recognition that the
tracker removes the trigger altogether. One cheap route reaches the call (the replay), as the design note's ladder
records.

## Findings, ranked
1. The equitised change's quarter-end sizing convention (one graded bp figure, not the rank or the call): fixed in the
   terms' own voice for that change only, asserted (SF31).
2. Two ask figures within a pound of a rounding edge (value income October to December, 4,951,499; growth dealing costs
   October to December, 357,849): moved mid-bin in the generator (Wath Energy's November dividend declared at 15.80p,
   Fennick's broker rate 6.2 bp); every graded figure's edge is now asserted at 0.07 of a bin or more, the tightest the
   AIM share at 31 December 2025 at 0.081.

## Next action for the author
None for the call: APPROVE stands. Ship once the leak reader's second pass on target.zip 6749a0ae (the terms changed)
returns clean.
