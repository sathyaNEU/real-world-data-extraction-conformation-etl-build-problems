## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Commerce should designate Eskwell, Dunrath and Quarrin as Formation Counties for 2027 to 2029.**
Their 2026 establishment birth rates are 11.3, 9.8 and 9.5 births per 100 establishments; Caldmere is the first county left out at 7.8, 1.7 below Quarrin. Not Caldmere or Tolbeck, second and third on new employer accounts per 100 establishments, whose 29 and 27 set-aside accounts continue businesses that operated before under another account (stores a buyer re-registered and restaffed, businesses that moved into Tolbeck's enterprise park).

## 2. Critical Components

1. New 2026 employer accounts that continue a business that operated before: **128** of **702** (**56** with a filed transfer, **72** shown by the workforce).
2. 2026 births: Eskwell **86**, Dunrath **121**, Quarrin **82**, Caldmere **55**.
3. Establishments employing in the fourth quarter of 2025: Eskwell **759**, Dunrath **1,236**, Quarrin **863**, Caldmere **702**.
4. 2026 birth rates per 100: Eskwell **11.3**, Dunrath **9.8**, Quarrin **9.5**, Caldmere **7.8**.

## 3. Step-by-Step Solution

1. In qcew_private_establishments_2024q4_2026q4.csv, found each account's first month with employment: 702 accounts first reported employment in 2026 and none before (the guideline's birth definition).
2. Set aside the 56 of them whose row in ui_employer_register_extract_2027-05-14.csv names a predecessor account.
3. In ui_wage_records_2024q4_2026q4.txt, set aside the 72 others that continue a business: an account whose last month with employment came before the new account's first month had more than half of the workers it paid in its last quarter with employment on the new account's payroll that quarter or the next. Read from the old account's side, this keeps as continuations the take-overs whose new owner hired from the first day and counts as births the start-ups staffed from a large closed payroll.
4. Counted the 574 births by the register's county (where the worksite lies, per the guideline) and divided by each county's establishments with employment in a month of the fourth quarter of 2025 (the guideline's base), 6,894 in the region.
5. Ranked the rates unrounded, as the guideline says: Eskwell 11.3, Dunrath 9.8, Quarrin 9.5, then Caldmere 7.8, 1.7 below Quarrin.
6. Counted 2025 births as 2026's are, from steps 1 to 3 on 2025, taking only accounts whose register liability date (first payroll) is in 2025: 542 births, over 6,895 establishments with employment in the fourth quarter of 2024 counted by the county where the worksite lies (the register's geocoded county).
7. Counted 527 deaths in 2025: last month with employment in 2025, none in 2026, and the business not gone on under another account: not a register predecessor, and not an account more than half of whose last-quarter workers one other account, new or established, paid the next quarter.
8. Designated Eskwell, Dunrath and Quarrin.

## 4. Deliverable Answers

### formation_county_designation_2027.pdf

1. Designation: Eskwell, Dunrath and Quarrin.
2. 2026 by county (births; new accounts set aside as businesses that operated before; birth rate per 100):
   - Eskwell: 86 births; 12 set aside; 11.3
   - Dunrath: 121 births; 14 set aside; 9.8
   - Quarrin: 82 births; 8 set aside; 9.5
   - Caldmere: 55 births; 29 set aside; 7.8
   - Tolbeck: 44 births; 27 set aside; 7.2
   - Brennock: 113 births; 23 set aside; 7.0
   - Fennamore: 73 births; 15 set aside; 6.6
3. First county left out: Caldmere at 7.8, 1.7 below Quarrin.
4. Chart: paired bars of each county's 2025 births and deaths, labelled with their counts, on page 2.

### lornock_establishment_births_2026.xlsx

1. Each of the 702 new 2026 accounts with its county and whether it is a birth (sheet New accounts 2026).
2. The 2026 county figures as in the memo (sheet Designation 2026).
3. 2025 births (birth rate per 100 establishments employing in the fourth quarter of 2024):
   - Brennock: 118 (7.3)
   - Caldmere: 52 (7.4)
   - Dunrath: 104 (8.5)
   - Eskwell: 77 (10.4)
   - Fennamore: 81 (7.3)
   - Quarrin: 63 (7.1)
   - Tolbeck: 47 (7.7)
4. 2025 deaths (death rate per 100 establishments employing in the fourth quarter of 2024):
   - Brennock: 110 (6.8)
   - Caldmere: 54 (7.7)
   - Dunrath: 88 (7.2)
   - Eskwell: 53 (7.2)
   - Fennamore: 80 (7.2)
   - Quarrin: 96 (10.8)
   - Tolbeck: 46 (7.5)
