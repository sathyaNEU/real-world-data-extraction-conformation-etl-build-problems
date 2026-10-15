# leak check, task138

**Verdict: REVIEW.** 19 files read, 37 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: stations, efficiency, asserted, record, january, station, readings, method, converges, records, converge, weather, readable, fields, reading, register, replay, default, depletion, stands, october, monitored, parameter, delivered, fitted

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `KBID_Water_Order_Procedure_rev2025.pdf`: \bthe model\b x1: ...with the loss allowances of Section 4. 3 The crop water model 3.1 The model keeps a daily balance for each field of the water in its root zone, a...

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `kbid_groundwater_levels_2016-2026.csv`: golden figure 13,110 appears: ...24,2023-02-26,107.5,steel tape,, KB-MW-24,2023-10-13,110.8,steel tape,, KB-MW-24,2024-02-13,104.2,steel ta...
- **REVIEW** `kbid_meter_book_2026.csv`: golden figure 17,370 appears: ...39.21,AF,DR-06, Route 4,4-29,P50731,05/28/2026,13:17,370.64,AF,DR-06, Route 4,4-30,P54858,05/28/2026,14:56...
- **REVIEW** `KBID_Water_Order_Procedure_rev2025.pdf`: carries 10 of 11 distinctive words of the committed call: 'Kestrel Bend Irrigation District should order 212,000 acre-feet from the Tolan Valley Project for the 2027 season.'
- **REVIEW** `README_order_working_files.txt`: carries 8 of 11 distinctive words of the committed call: 'Kestrel Bend Irrigation District should order 212,000 acre-feet from the Tolan Valley Project for the 2027 season.'
- **REVIEW** `kbid_canal_operations_log_2026.docx`: carries 7 of 11 distinctive words of the committed call: 'Kestrel Bend Irrigation District should order 212,000 acre-feet from the Tolan Valley Project for the 2027 season.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `KBID_Water_Order_Procedure_rev2025.pdf`: 13 of 25 stump-paragraph terms appear (efficiency, record, january, station, method, records); read whether the document names the move
- **REVIEW** `README_order_working_files.txt`: 9 of 25 stump-paragraph terms appear (stations, record, january, station, records, weather); read whether the document names the move
- **REVIEW** `kbid_canal_operations_log_2026.docx`: 5 of 25 stump-paragraph terms appear (stations, record, january, station, reading); read whether the document names the move

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

## Solver's-eye read (round 3)

One isolated reader at medium effort on fresh copies of `prompt.txt` and `target/` (the stage 3 cut, `target.zip` sha256 50c887dca427e7ad); it sampled the three large CSVs and the two large workbooks by header and first rows and did not compute. Q1: it quoted WOP 2.3 (the 24-of-30 order rule) and 2.4 (each replay run "from its root zone as it stands at the end of 31 January") as handing over the procedure; the prompt says nothing of the method. Q2: none (nothing ranks or states the order, the thirty requirements or the lateral figures; the Authority's notice and WOP 1.1's 241,000 acre-foot contract quantity are a ceiling). Q3: the working-files note (a file index) and the data dictionary (field definitions that settle readings), both mild. Q4: none (the contract quantity, the allocation and Table 5's allowances read as inputs). Q5: WOP 2.3, 2.4, 3.1 to 3.5, 4.1, 6.1 and 6.2; not run. Q6: it read the filed replay and order procedure (WOP 2.3 to 3.5) as rule application, the rest as data semantics, nothing as planted. Ruling: the procedure is the order's machinery, which the default path executes as well; the decisive step is the unfiled estimate of the start state (WOP 2.4 files only what the state is; the reader's own last note says the state "has to come from the soil moisture network, the rain record or the January weather" and that nothing says how), and executing every filed rule with Table 4 read across files 215,000 (SF35), as the rule 3 re-audit (PASS) and the judge (DETERMINISTIC, Gate H analytical) confirm. Q3 ruling: the note is the working papers' index WOP 7.1 files with the Board, and the dictionary holds field semantics only, never how the state is built; harmless.

Sweep lines, the reader's verdict and the ruling: "the model" in the procedure, harmless (its section heading); 13,110 and 17,370, harmless (chance substrings); the procedure's 10 of 11 call words and 15 of 25 stump terms, marked leak by the reader as the governing method document: harmless, the governing procedure's own vocabulary (district, project, order, season, efficiency, the weather record's station switch, the orders), with no figure and no move named, consistent with the judge; the note's 8 and 9 and the operations log's 7 and 5, harmless (a file index and operational prose); the prompt's chart sentence, marked a mild leak for naming thirty replayed seasons and the order across them: harmless, the chart's named parts and the procedure's own replay, giving nothing WOP 2.3 and 2.4 do not file; the yard logger's `Flag`, harmless (its export's missing-day code). Realism notes, left as they are (the pack ships as built): estimate rows for each heading logger outage in the operations log (the Water Master's standing practice, the estimates Ask 2 reads); the working-files index and a thorough dictionary; every file time stamped 1 February 2027 (the export date); weir crests of 3 to 6 feet with one coefficient of 3.33 (the sharp-crested weir's standard); the weir remarks' "set 2in brd" shorthand. Readings it raised, each closed: whole thousands (WOP 2.3, the smallest that covers); the share not delivered as a share of the water put in (the prompt's "of that water"), season totals for 2026; the tail weir's season (the canal is dry from November to January, WOP 2.1); deliveries through rollovers, hundred-cubic-foot registers, meter swaps and the Lateral 5 to 6 connector (the asks' devices).
