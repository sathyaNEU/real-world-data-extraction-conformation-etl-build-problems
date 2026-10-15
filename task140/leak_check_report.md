# leak check, task140

**Verdict: REVIEW.** 24 files read, 36 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: storage, busiest, drivers, forecast, history, cell-store, budget, objective, forecasting, running, machine, decision, quantity, reservation, binding, decisive, solved, operations, series, default, compute, struck, regression, residual, together

## 2 author vocabulary (REVIEW 2)
- **REVIEW** `c22_capacity_report_2026Q3.pdf`: \bdesign note\b|\bgenerator\b x1: ...ime (01:40 UTC): UPS B in hall 2 failed to transfer during the weekly generator test. C-22's control nodes lost power for about 40 seconds. Firm and...
- **REVIEW** `mad1_operations_log_2026H2.docx`: \bdesign note\b|\bgenerator\b x3: ...03:40 Hall 2 UPS B failed to transfer during the weekly generator test. C-22 control nodes lost power, about 40 s, and restarted. Worke...

## 3 answer figures in the pack (REVIEW 6)
- **REVIEW** `CS-3_cell_capacity_standard_rev2026-06.pdf`: carries 6 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'
- **REVIEW** `README_capacity_review_files.txt`: carries 4 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'
- **REVIEW** `batch_training_demand_2027H1.pdf`: carries 6 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'
- **REVIEW** `c22_capacity_report_2026Q3.pdf`: carries 4 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'
- **REVIEW** `capacity_memo_2027Q1.docx`: carries 6 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'
- **REVIEW** `chargeback_policy_2026.pdf`: carries 5 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'

## 4 design-note vocabulary (REVIEW 6)
- **REVIEW** `CS-3_cell_capacity_standard_rev2026-06.pdf`: 8 of 25 stump-paragraph terms appear (busiest, forecast, history, budget, machine, reservation); read whether the document names the move
- **REVIEW** `README_capacity_review_files.txt`: 5 of 25 stump-paragraph terms appear (budget, machine, reservation, operations, compute); read whether the document names the move
- **REVIEW** `c22_capacity_report_2026Q3.pdf`: 8 of 25 stump-paragraph terms appear (busiest, cell-store, running, machine, reservation, operations); read whether the document names the move
- **REVIEW** `capacity_memo_2027Q1.docx`: 7 of 25 stump-paragraph terms appear (storage, cell-store, budget, machine, reservation, operations); read whether the document names the move
- **REVIEW** `mad1_operations_log_2026H2.docx`: 4 of 25 stump-paragraph terms appear (cell-store, running, machine, operations); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Give reservations to the nearest 1,000 cores, core-hours to the nearest 100, shares in per cent to two decimals, machine-hours to the nearest 10 and charges in euros to the nearest 100.'

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `c22_hardware_plan_2027Q1_rev2026-12-11.xlsx`: 30 ISO dates after 2026-12-14, e.g. 2026-12-28, 2027-01-01
- **REVIEW** `compute_rate_card.csv`: 1 ISO dates after 2026-12-14, e.g. 2027-01-01

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Q1 to Q4: none (CS-3 4.1 and 3.2 are procedure; no file states a 2027 Q1 reservation or guarantee; the README and dictionary are ordinary; the Q3 report's 57,000 and the ledger's 56,000 read as history). Q5: CS-3 2.1 (726,624 reservable cores), 3.1 and 3.2 (firm 576,972, search-api, pricing and reco-serve held to budget), 4.1 (the busiest-hour use forecast, method open), 5.1 (largest whole thousand left); the reader's own trend forecast of each platform service on its history lands about 121,000 to 122,000 (the default path, 122,000) and it could not reach 109,000: the stump working, the storage coupling unfound. Q6: a mix, the plan read at the quarter start and the budget hold as rule application, the platform forecast as the analytical choice; no sentence names the move. REVIEW lines: all harmless (the weekly generator test, shared domain nouns, future in-service dates, a forward rate). Realism: a dictionary tailored to the Q3 tables (checkpoint committed and write-started definitions, machine-event causes, the Cluster ids sheet); the budgets workbook's Freeze sheet instruction; the Q3 report's "does not carry mid-quarter changes" and "no rows for 19 August from 01:00 to 07:59"; the demand note's closing disclaimer. Readings: Ask C's held-from date (requested or applied by the reconciler) and the September rate split; the preemption table's edge cases (uncommitted checkpoint at preemption, resized runs, runs still running, runs started before 1 July); the machine-hours table's open removals at 30 September, the 19 August outage and re-registered ids; the tenant's C-22 budget line and the cost-centre format.
