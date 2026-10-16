# leak check, task463

**Verdict: REVIEW.** 15 files read, 50 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: change, comparison, comparisons, linked, decisive, points, carries, statistics, method, direct, programme, compiled, rnqvist, linking, harmless, population, twelve, superlative, compiles, choice, weights, leaves, manager, banned, quantity

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `gorsedale_period_sales_fy2026_fy2027.txt`: golden figure 1.4 appears: ...P08|31|411139|5216975145669|BAYBAY FABRIC CONDTNR 1.4L|52|361.40 FY2026|P08|31|411195|5755460145758|BRA...
- **REVIEW** `rpi_transaction_data_introduction_plan_2026.pdf`: golden figure 2.2 appears: ...es Table 1. Items assessed for transaction data. 2.2 Under the data supply agreements signed in 2025...
- **REVIEW** `rpi_transaction_data_introduction_plan_2026.pdf`: golden figure 1.1 appears: ..., Transaction Data Programme Manager. 1. Purpose 1.1 From the January 2027 index the office intends t...
- **REVIEW** `rpi_transaction_data_introduction_plan_2026.pdf`: carries 33 of 35 distinctive words of the committed call: 'Move 13 of the sixteen items to transaction data from the January 2027 index: Bread, Breakfast cereals, Biscuits, Yoghur'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `rpi_transaction_data_introduction_plan_2026.pdf`: 6 of 25 stump-paragraph terms appear (change, points, statistics, programme, compiled, manager); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `gorsedale_fiscal_calendar_fy2026_fy2027.csv`: 29 ISO dates after 2026-10-21, e.g. 2026-10-25, 2026-10-26, 2026-11-01, 2026-11-02, 2026-11-08

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Round 2 (isolated Sonnet reader, medium effort, fresh copy of prompt.txt and target/ after the plan's 3.5 and 3.6 and the prompt changed):

1. Decisive step: none. The plan's 3.4 and 3.5 are procedure, not a hint about a pitfall.
2. Ranking file: none. The published 12-month rates are the comparison figure the prompt asks for.
3. Analyst-only file: a weak candidate, transaction_data_folder_register.csv; "real programmes do keep such registers".
4. Figure reading as the answer: none.
5. Filed sentences: the plan's 3.1 to 3.6. "The text does not fix how a month's index is built": chained month to month or compared directly with September 2025. Flagged as the largest determinism risk.
6. What decides: the pipeline is procedure; "if the weighting or index-form choice is left open and decisive, it is the analytical element, but the text doesn't mark it".

REVIEW lines: all harmless (a pack size in a product description, section numbers, the item names of Table 1, generic plan vocabulary, a fiscal calendar's whole year).

Main thread ruling: the index-form choice is open and decisive (thirteen items against five), so the decisive step is the analytical choice the design intends; the open construction is the judge's ground, and the re-judge returned DETERMINISTIC, APPROVE with the linked index ruled out on the data. Realism tells fixed in the generator: the classification's valid_from dates (now the office's summer 2025 batch dates); a within-supermarket share closed as SF13.
