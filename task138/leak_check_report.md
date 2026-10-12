# leak check, task138

**Verdict: REVIEW.** 18 files read, 39 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: orders, record, winter, asserted, forecast, october, procedure, station, requests, rebuilt, closed, balance, replays, register, request, reader, decision, delivered, decisive, delivery, nothing, january, quantity, window, method

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `KBID_Water_Order_Procedure_rev2025.pdf`: \bthe model\b x1: ...with the loss allowances of Section 4. 3 The crop water model 3.1 The model keeps a daily balance for each field of the water in its root zone, a...

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `kbid_meter_book_2026.csv`: golden figure 37,270 appears: ...,9227.19,DR-04, Route 2,2-43,P26075,09/08/2026,13:37,270.39,DR-04, Route 2,2-44,P27119,09/08/2026,15:37,38...
- **REVIEW** `KBID_Water_Order_Procedure_rev2025.pdf`: carries 10 of 11 distinctive words of the committed call: 'Kestrel Bend Irrigation District should order 202,700 acre-feet from the Tolan Valley Project for the 2027 season.'
- **REVIEW** `README_order_working_files.txt`: carries 8 of 11 distinctive words of the committed call: 'Kestrel Bend Irrigation District should order 202,700 acre-feet from the Tolan Valley Project for the 2027 season.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `KBID_Water_Order_Procedure_rev2025.pdf`: 13 of 25 stump-paragraph terms appear (orders, record, october, procedure, station, requests); read whether the document names the move
- **REVIEW** `README_order_working_files.txt`: 10 of 25 stump-paragraph terms appear (orders, record, october, procedure, station, requests); read whether the document names the move
- **REVIEW** `TVWA_2027_initial_allocation_notice.pdf`: 3 of 25 stump-paragraph terms appear (orders, october, quantity); read whether the document names the move
- **REVIEW** `kbid_canal_operations_log_2026.docx`: 5 of 25 stump-paragraph terms appear (orders, winter, station, closed, january); read whether the document names the move

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

## Solver's-eye read

Pass 1 (12 October 2026), on the pack as it stood before the stage 4 fix pass, verbatim:

Q1 to Q4: none. WOP 2.3 and 2.4 state the order rule and the replay as procedure, with no hint of a shortcut; no file holds per-year requirements, a monthly schedule or lateral loss shares; the data dictionary is the only guide-like file, ordinary for an extract (mild); the 241,000 af contract quantity and the 100 percent allocation read as context. Q5: WOP 6.2 fixes the population (619 accepted request rows; 46 superseded and 10 withdrawn out), WOP 2.3 with 2.4, 3.1 to 3.5, 4.1 and 5.1 fix the arithmetic (24th smallest of 30 replay requirements, rounded up to the hundred); not executed. Readings raised: the start state on 1 February is not filed (the decisive rung, R3, by design: the data force it); turnouts 05-045 to 05-058 on Lateral 6 after the 15 June connector (register against the operational feed); request acres against GIS acres (closed by 6.2); pre-2014 ETo and missing yard days (closed by 6.1 and the dictionary); the order of operations within a day; the leap day (closed by 2.4); Ask A's Lateral 5 and 6 inflows after the connector; Ask B's head with boards in (gauge less crest, or less boards too); a tie for the year that sets the order (unlikely). Realism: random-looking registers on newly installed meters; mostly blank weir remarks with stray quote characters in a few, templated request remarks; an evenly spaced operations log. REVIEW lines: all harmless (the procedure's "The crop water model" heading, a meter-book time and reading run together as 13:37,270.39, domain nouns, the logger's Flag column).

Since pass 1 the stage 4 fix pass changed two documents, `kbid_data_dictionary.xlsx` (station 39's entry now reads "millimetres (25.4 millimetres to the inch)") and `kbid_canal_operations_log_2026.docx` (each entry dated the day it happened, where six had logged later events in advance; a time and initials column; 12 routine entries; Check 2's gate named as the overshot gate the structures workbook lists; 38 entries against 20), and three data files, `kbid_meter_shop_log_2026.xlsx` (a New or rebuilt column; new meters go in at 0.00), `kbid_meter_book_2026.csv` (the new meters' reads from zero) and `kbid_water_requests_2027.xlsx` (the remarks). `leak.py` above is the run on the changed pack (the same REVIEW lines as pass 1, no LEAK). The reader's re-read of the changed pack is pending.
