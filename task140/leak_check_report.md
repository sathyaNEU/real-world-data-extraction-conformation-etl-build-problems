# leak check, task140

**Verdict: REVIEW.** 24 files read, 36 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: storage, busiest, drivers, forecast, history, cell-store, budget, objective, forecasting, running, operations, series, machine, decision, quantity, reservation, binding, decisive, solved, residual, default, compute, struck, regression, together

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `mad1_operations_log_2026H2.docx`: \bdesign note\b|\bgenerator\b x3: ...03:40 Hall 2 UPS B failed to transfer during the weekly generator test. C-22 control nodes lost power, about 40 s, and restarted. Worke...

## 3 answer figures in the pack (REVIEW 6)
- **REVIEW** `CS-3_cell_capacity_standard_rev2026-06.pdf`: carries 6 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'
- **REVIEW** `README_capacity_review_files.txt`: carries 4 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'
- **REVIEW** `batch_training_demand_2027H1.pdf`: carries 6 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'
- **REVIEW** `c22_capacity_report_2026Q3.pdf`: carries 4 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'
- **REVIEW** `capacity_memo_2027Q1.docx`: carries 6 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'
- **REVIEW** `chargeback_policy_2026.pdf`: carries 5 of 6 distinctive words of the committed call: 'C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.'

## 4 design-note vocabulary (REVIEW 6)
- **REVIEW** `CS-3_cell_capacity_standard_rev2026-06.pdf`: 8 of 25 stump-paragraph terms appear (busiest, forecast, history, budget, operations, machine); read whether the document names the move
- **REVIEW** `README_capacity_review_files.txt`: 5 of 25 stump-paragraph terms appear (budget, operations, machine, reservation, compute); read whether the document names the move
- **REVIEW** `c22_capacity_report_2026Q3.pdf`: 7 of 25 stump-paragraph terms appear (busiest, cell-store, operations, machine, reservation, compute); read whether the document names the move
- **REVIEW** `capacity_memo_2027Q1.docx`: 7 of 25 stump-paragraph terms appear (storage, cell-store, budget, operations, machine, reservation); read whether the document names the move
- **REVIEW** `mad1_operations_log_2026H2.docx`: 4 of 25 stump-paragraph terms appear (cell-store, running, operations, machine); read whether the document names the move
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

## Solver's-eye read (targeted, after the stage 4 fix pass)

On the seven changed documents. Q1 to Q4: none (CS-3 3.2, 4.1 and 5.1 state the rules, not the step; no file states the 2027 Q1 guarantee or an asked figure; the Q3 and Q4 figures read as history; the dictionary and README read as helpers). Q5: the literal chain gives reservable 726,624 and the budget-held firm reservations; the reader did not compute the guarantee. Q6: rule application for the reservations plus one analytical choice, the platform services' busiest-hour forecast (the decisive step, storage solved with the guarantee it serves; the judge's Gate H ruled it analytical). Realism: CS-3's June 2026 additions are the rules used; chargeback 2.2's "applied" points at the reconciler file (the asks' basis, filed at the judge's request); the memo's tenant and freeze statements; the demand note's 0.6 factor and queue lines (a declared distractor); the dictionary's field set; the September budget bumps on three cost centres. Readings: nearest thousand against largest whole thousand (5.1, SF38); the platform method (open by design); R114 against R117 (the January rate); a reservation above the request (held to the budget only caps); the asks' preemption basis, resized cores, machines out at quarter end, the 19 August event, UTC months (fork rows SF19 to SF37).

Disposition (ship): nothing quoted for questions 1 to 4; the realism notes are recorded and left (each further rewording of a filed document risks reopening a closed fork for no graded figure).

## Solver's-eye read (re-read after the realism repair, 2026-10-15)

Q1 to Q4: no file states a 2027 Q1 guarantee, a storage forecast or a method. The reader read the two notes the realism repair added as signposts or a decoy: the dictionary's `cores_in_use` sentence on late daemon samples (a bias mechanism explained in a field definition) and the operations log's 7 July reminder of the Tuesday 03:00 to 05:00 UTC rolling restart ("no action needed"), and wondered whether the Tuesday dip decides the busiest-hour forecast (it does not: the restart hours left out, the low hours left out, a Huber fit and hour-of-week terms all keep 2.94, 0.208, 1.208, 38,000 and 109,000, asserted). It also flagged the Q3 report's "which holds 2,201 of the quarter's 2,208 hours" and the 19 August minute-by-minute account told in both the Q3 report and the operations log.

Disposition (fixed in the generator): the dictionary's `cores_in_use` is now the terse "Cores in use, hourly average, as the collector received them."; the restart reminder is an ordinary on-call line (7 July 07:04 Madrid time, "cell-store rolling restart on C-22 done, all daemons back."); the Q3 report drops the hours-held clause and gives 19 August one line with its PIR number, the operations log keeping the account. The texture in the data is unchanged; only these three documents and the golden workbook's residual note moved; no graded figure, `figures.json` value or rung moved.

## Solver's-eye read (round 3)

Targeted re-read on target.zip 5823a2b7, after the realism notes were trimmed (the cell-store telemetry, the data dictionary, the operations log and the Q3 capacity report, the rest of the folder as context). Q1 to Q4: none; the trimmed dictionary line, the on-call restart line and the shortened Q3 report no longer steer. Q5: CS-3 2.1, 3.2, 4.1 and 5.1 execute to the golden's inputs with the forecast method open. Q6: the platform forecast, an analytical choice; the reader's own route on the storage service's history landed about 120,000 to 122,000 against the golden 109,000. Realism: one note, the operations log's 2026-12-11 line on the refresh racks ("C-22 hardware plan revised: refresh racks in service from 28 December.") read as slightly steering because it repeats the plan.

Disposition (ship): harmless. It is the plan revision's own log entry, written by fleet and hardware on the day the plan's revision is dated (rev2026-12-11), as the log records every rack handover; it repeats a fact the plan states and names no method, driver or figure. Left as built; no change to `target/`.
