## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**At its 2026 release the works would not keep under the 85 kg annual mercury load that applies from 2028: it released 151 kg (kiln 1 68 kg, kiln 2 83 kg), 66 kg over, so it needs carbon injection.** Not the 2026 stack tests carried over the kiln hours (about 70 kg), which every test measured with the raw mill running and so leave out what the kilns released in direct operation.

## 2. Critical Components

1. Kiln 1 released **68 kg** of mercury to air in 2026: its raw materials and fuels less what left in clinker and in the filter dust it bled to silo S7.
2. Kiln 2 released **83 kg**: its raw materials and fuels less what left in clinker.
3. The works released **151 kg**, **66 kg** over the 85 kg load.

## 3. Step-by-Step Solution

1. Read condition 5.6 of IEL-1186-03_conditions_consolidated_2026.pdf (the load counts every hour each kiln fires, in compound and in direct operation) and stack_tests_Hg_2024-2026.pdf (every run with the raw mill in operation), so the tested rate covers compound operation only.
2. Took each kiln's year of mercury in: every month's raw material tonnes (dry) and fuel tonnes (as fired) in production_ledger_2026.xlsx times that month's composite in QC_lab_composites_2026.xlsx on the same basis (sand and slag: the quarter's composite).
3. Subtracted the mercury that left in clinker (the ledger's clinker times its monthly composite) and, for kiln 1, in the ledger's filter dust to silo S7 times the month's filter dust composite: kiln 1 68 kg, kiln 2 83 kg, works 151 kg against 85 kg.
4. Rebuilt each kiln's state through 2026 from DCS_event_journal_2026.txt, starting from the state at the start of the log: on feed from each KILN FEED ON until its next FEED OFF or MAIN BURNER TRIP (the burner trip stops the feed with it), and the raw mill stopped from each STOP or TRIP until its next START, with times read as Irish local time and the repeated hour of 25 October placed after the logged clock change.
5. Summed by local quarter (condition 6.5): hours on feed, kiln 1 1,542, 2,107, 2,116 and 2,176, kiln 2 1,637, 2,168, 2,126 and 2,106; hours in direct operation (on feed with the raw mill stopped), kiln 1 288, 345, 379 and 380, kiln 2 352, 452, 469 and 458.
6. Took NOx from PI_historian_K1K2_2026_30min.csv, each half-hour's concentration at 10% oxygen restated to the measured oxygen and times the dry flow, and the half-hours the historian lacks in May from CEMS_logger_A1-1_A1-2_May2026.csv, whose concentrations are already at the measured oxygen: kiln 1 932 t, kiln 2 605 t.
7. The works is 66 kg over the load at its 2026 release, so carbon injection goes into the 2027 capital round.

## 4. Deliverable Answers

### kiln_mercury_memo_2026.pdf

1. At its 2026 release the works would not keep under the 85 kg load; it needs carbon injection.
2. Over the load by 66 kg (151 kg against 85 kg).
3. Mercury released to air in 2026: kiln 1 68 kg, kiln 2 83 kg.
4. Bar chart of each kiln's hours in direct operation by month of 2026, on the memo's first page.

### kiln_emissions_2026.xlsx

1. Mercury released to air in 2026: kiln 1 68 kg, kiln 2 83 kg.
2. Hours on feed, 2026:
   - Kiln 1: Q1 1,542, Q2 2,107, Q3 2,116, Q4 2,176
   - Kiln 2: Q1 1,637, Q2 2,168, Q3 2,126, Q4 2,106
3. Hours in direct operation, 2026:
   - Kiln 1: Q1 288, Q2 345, Q3 379, Q4 380
   - Kiln 2: Q1 352, Q2 452, Q3 469, Q4 458
4. NOx to air in 2026: kiln 1 932 t, kiln 2 605 t.
