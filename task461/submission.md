## Tags

**Domain:** General Statistics & Data Science (data integration: the battery node's short day-ahead price record extended over the North Hub's eight-year record through their overlap).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Load a 2027 cycling threshold of $20 per MWh into Redrock Draw's trading system.**
At $20 the battery is expected to cycle on 275 days of 2027, within the warranty's 300 Full Cycles; at $15, the next setting down, it would cycle on 323. The node's own 336 days since MPI first priced it are one windy stretch: their average spread is ordinary, but 34 per cent of the hub's 2026 days had a spread under $8 against 11 to 16 per cent in an ordinary year, so the node's own days set $15 (266 expected days), too low for 2027. The North Hub's record from 2019, carried to the node at the ratio its 323 overlapping days show (the node's spread 2.21 times the hub's), gives the expected days at each setting. Not $10, the hub's record taken for the node's, and not $30, the hub plus the node's average spread premium ($19.96), which lifts every flat day by the same amount.

## 2. Critical Components

1. Expected 2027 cycling days at $20: **275**, within the 300 limit.
2. At $15, the next setting down: **323** expected cycling days, over the limit.
3. The node's daily spread is **2.21** times the hub's over the **323** days MPI priced it at its own settlement point.

## 3. Step-by-Step Solution

1. Read mpi_dam_settlement_point_prices_north_hub_2019_2026.csv (dates MM/DD/YYYY and hours 01:00 to 24:00 to 2021, ISO dates and hours 1 to 24 from 2022) and mpi_dam_settlement_point_prices_redrock_2025_2026.csv, joining RDRW_ESS1_RN and REDROCK_ESS_RN through mpi_settlement_point_list_2026.csv, each operating day on Central prevailing time with its 23 or 25 hours as they are.
2. Computed each operating day's spread as the policy defines it (the average of the four highest hourly day-ahead prices less the average of the four lowest): 2,863 hub days and 336 node days.
3. Set aside the node's first 13 days, which MPI priced at the hub's prices, and took the ratio of the node's total spread to the hub's over the 323 days left: 2.21, the relationship running through the origin.
4. Compared the hub's years: its 2026 average spread ($16.90) sits inside the 2019 to 2025 range ($16.17 to $19.14), but 34 per cent of its 2026 days were under $8 against 11 to 16 per cent in 2019 and 2021 to 2025 (31 in 2020, falling back to 14 in 2021): the node's own days are a windy stretch, not an ordinary year.
5. Extended the node's record over the hub's 2,863 days (the node's own spread where MPI priced it, 2.21 times the hub's on every other day) and took the expected 2027 cycling days at each setting as 365 times the share of days at or above it; the extension's other estimators agree on the call (the full years 2019 to 2025 alone give 282 days at $20 and 330 at $15).
6. Picked the lowest setting within 300: $20 (275 days); $15 gives 323.
7. Counted 2026's Full Cycles as warranty Schedule 4 does: the BMS's DC discharge for each hour in contract months on Central prevailing time; for the 27 hours (in 11 runs) in which the meter recorded the battery discharging while the BMS export shows zero energy with its last state held, the meter's delivered energy over 0.975, as the warranty's data clause has it; both capacity tests left out (2026-03-12, logged TEST, and 2026-09-14, logged MAINT after the June firmware update).
8. Took the day-ahead net from the latest statement line for each hour and charge type (a final statement restates the day; 20 and 21 July were repriced between initial and final), reversed MPI's sign and counted the administrative fee once per operating day, the export carrying the day's fee on every hour line.
9. Divided the January to October net by the Full Cycles: $31,339 per cycle.

## 4. Deliverable Answers

### redrock_draw_2027_cycling_threshold.xlsx

1. Threshold for 2027: $20 per MWh; the next setting down, $15, is over the limit.
2. Expected 2027 cycling days at each setting:
   - $5: 365
   - $10: 355
   - $15: 323
   - $20: 275
   - $25: 224
   - $30: 176
   - $35: 138
   - $40: 113
3. Full Cycles the warranty counts in each month of 2026:
   - January: 7.95
   - February: 2.98
   - March: 4.97
   - April: 5.99
   - May: 9.01
   - June: 11.02
   - July: 18.06
   - August: 14.03
   - September: 11.01
   - October: 2.99
   - January to October: 88.01
4. Day-ahead net after MPI's fees in each month of 2026, thousands of dollars:
   - January: 268.9
   - February: 113.9
   - March: 325.2
   - April: 132.9
   - May: 252.9
   - June: 257.9
   - July: 671.7
   - August: 409.0
   - September: 262.3
   - October: 63.5
   - January to October: 2,758.1
5. Day-ahead net per Full Cycle, January to October: $31,339.
6. Chart: the cumulative 2026 Full Cycles at each month's end (88.01 at the end of October) against the pace to 300 by 31 December, on the Cycle chart sheet.

### redrock_draw_daily_spreads_conformed.csv

1. 3,199 rows, one per settlement point and operating day: the North Hub from 2019-01-01 and the node, under REDROCK_ESS_RN, from 2025-12-02, both to 2026-11-02, with the hours in the day, the spread in dollars per MWh and whether MPI set the node's price at the hub's.
