# leak check, task138

**Verdict: REVIEW.** 18 files read, 38 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, refill, january, default, fields, winter, weather, delivered, replay, balance, requirement, deficit, replays, decisive, forecast, readable, orders, efficiency, asserted, depletion, quantity, rebuilt, working, decision, capacity

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `KBID_Water_Order_Procedure_rev2025.pdf`: \bthe model\b x1: ...with the loss allowances of Section 4. 3 The crop water model 3.1 The model keeps a daily balance for each field of the water in its root zone, a...

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `kbid_groundwater_levels_2016-2026.csv`: golden figure 13,110 appears: ...24,2023-02-26,107.5,steel tape,, KB-MW-24,2023-10-13,110.8,steel tape,, KB-MW-24,2024-02-13,104.2,steel ta...
- **REVIEW** `kbid_meter_book_2026.csv`: golden figure 17,370 appears: ...39.21,AF,DR-06, Route 4,4-29,P50731,05/28/2026,13:17,370.64,AF,DR-06, Route 4,4-30,P54858,05/28/2026,14:56...
- **REVIEW** `KBID_Water_Order_Procedure_rev2025.pdf`: carries 10 of 11 distinctive words of the committed call: 'Kestrel Bend Irrigation District should order 215,000 acre-feet from the Tolan Valley Project for the 2027 season.'
- **REVIEW** `README_order_working_files.txt`: carries 8 of 11 distinctive words of the committed call: 'Kestrel Bend Irrigation District should order 215,000 acre-feet from the Tolan Valley Project for the 2027 season.'
- **REVIEW** `kbid_canal_operations_log_2026.docx`: carries 7 of 11 distinctive words of the committed call: 'Kestrel Bend Irrigation District should order 215,000 acre-feet from the Tolan Valley Project for the 2027 season.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `KBID_Water_Order_Procedure_rev2025.pdf`: 14 of 25 stump-paragraph terms appear (record, january, fields, weather, replay, balance); read whether the document names the move
- **REVIEW** `README_order_working_files.txt`: 6 of 25 stump-paragraph terms appear (record, january, fields, weather, orders, working); read whether the document names the move
- **REVIEW** `kbid_canal_operations_log_2026.docx`: 4 of 25 stump-paragraph terms appear (record, january, winter, orders); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "Put the order in kbid_order_2027.xlsx and draw kbid_order_2027.svg with the thirty replayed seasons' headgate requirements from smallest to largest and the order across them."

## 8 column names (REVIEW 1)
- **REVIEW** `kbid_station_daily_2014-2027.csv`: columns a generator names and an organisation does not: Flag

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (round 2)

Q1: the reader quoted WOP 2.3 and 2.4 (the 24-of-30 order rule, and each replay run "from its root zone as it stands at the end of 31 January") as the main call stated as a rule. Q2 to Q4: none (meter, heading and weir records are raw inputs; the tables hold coefficients; the README and dictionary are plausible working-paper files; the contract quantity and allocation are a cap). Q5: WOP 2.3, 2.4, 3.1 to 3.5, 4.1, 6.1 and 6.2; not computed. Q6: the reader leaned to rule application because the replay is filed; it did not compute and so did not reach the open step, how the 31 January state is built (2.4 files only the WHAT; the record run of 2026's applied water against the last set taken as a refill is the analytical choice, asserted on the clean truth: 209,000 against 215,000). REVIEW lines: harmless (the procedure's order basis is its own rule; coincidental digit strings; a logger Flag column); the prompt's "thirty replayed seasons ... smallest to largest" gives the chart's structure, no figure. Realism: the operations log's near-identical sensor failure and recovery pairs with Water Master estimate lists read templated; every meter, flume and sheet repair is neatly dated; the 15 June connector entry is clean prose. Readings: the west spur's lateral before and after 15 June for the 2026 lateral figures; water put in with the Water Master's estimates on logger-down days; the weir head with boards set; meter swaps and CCF against AF (the asks' devices).
