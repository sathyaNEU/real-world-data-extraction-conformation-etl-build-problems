# task123 · Northern Heat Assistance Grant 2026-27 county split

## Tags

**Domain:** Survey Research & Official Statistics (official time-series production: a calendar-month county series of residential gas use built from billing-period returns).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Split the $18,640,000 Northern Heat Assistance Grant for 2026-27 as Brennock $2,380,000, Rennick $2,145,000, Pellow $1,905,000, Halvern $1,840,000, Ashwell $1,710,000, Farrish $1,685,000, Tillery $1,525,000, Merrion $1,310,000, Ottercreek $1,230,000, Keswin $1,125,000, Sauvain $910,000 and Wynnell $875,000.**

Each award is the county's share of the region's 10,260,000 therms of residential use on the gas days of January 2026, with every bill read on a cycle or every second month spread over its service period by the AMI meters' daily use. Not day-proration of each bill, which treats use inside a bill as flat when the AMI meters used 2.4 times as much gas a day in the cold snap at the end of January as over its first eighteen days. Not the bills read in January, which are a billing month, not January's gas days. Not a monthly-average shape, which flattens the cold snap inside January. Not the AMI accounts' January scaled to every premise, which carries their newer, smaller homes to every county.

## 2. Critical Components

1. The region's residential natural gas use on the gas days of January 2026 is **10,260,000 therms**
2. Brennock's January 2026 residential use, the largest county's, is **1,310,000 therms**
3. Tillery's January 2026 residential use, Pine Harbor's and Kestrel Valley's premises together, is **840,000 therms**

## 3. Step-by-Step Solution

1. Read every residential bill with its service period (standard 2.4) and its therms as billed (2.5) from KVG_RES_BILLING_EXTRACT_20260415.csv (each CNCL netting its original under the same BILL_NO), NNG_R1_READS_BIMONTHLY_20260415.txt (layout in RHEF_data_notes_utility_extracts_2026-04.docx) and PHE_RESIDENTIAL_BILLS_202510_202604.csv: every January gas day of every account falls in exactly one bill.
2. Averaged usage_ccf over the meters reporting each gas day in PHE_MDMS_DAILY_RES_20251006_20260414.parquet as the daily shape of residential use: 2.4 times as high in the cold snap of 19 to 31 January as in 1 to 18 January.
3. Spread each bill touching January over the gas days of its service period in proportion to that shape (Pine Harbor's CALENDAR bills fall wholly in their month) and summed the January part by the premise's COUNTY in service_points_northern_region_2026-04-15.csv (standard 2.6): the region's January is 10,260,000 therms, Tillery's 840,000 from Pine Harbor and Kestrel Valley premises.
4. Split $18,640,000 in proportion to the unrounded county totals (standard 3.3), each award rounded to $5,000: Brennock $2,380,000 the largest, Wynnell $875,000 the smallest.
5. Counted residential disconnections for nonpayment completed in January (standard Appendix B): Kestrel Valley's completed NP turn-off orders in KVG_SERVICE_ORDERS_20251201_20260203.csv with the jobs in Northline_KVG_collections_jobs_Jan2026.xlsx, each disconnection once by account and day; Northbank's completed DNP activities by COMPLETED_AT in NNG_CREW_COMPLETIONS_DEC25_FEB26.csv; Pine Harbor's completed Collections Shutoff work orders in PHE_WORK_ORDERS_DEC25_FEB26.json with its NP VALVE_CLOSE events in PHE_HES_METER_EVENTS_DEC25_FEB26.csv on their Eastern date: Halvern's 14 is the most.
6. Counted residential accounts on a low-income payment plan on 31 January (Appendices A and B): Kestrel Valley's WCP enrollments in force that day at the county of the account's premise in the billing extract, Northbank's HHAP premises in NNG_HHAP_PREMISES_20260131.csv where the account holding the premise at PROGRAM_START_DT in NNG_ACCOUNT_PREMISE_HISTORY_20260415.csv still held it on 31 January, and Pine Harbor's IBPP arrangements in force on accounts linked to a meter that day in PHE_METER_ACCOUNT_HISTORY_20260415.csv: Brennock's 384 is the most.
7. Recommendation: award the twelve counties the amounts in heating_grant_split_2026_27.xlsx, Brennock $2,380,000 down to Wynnell $875,000.

## 4. Deliverable Answers

### jan2026_county_gas_series.csv

1. Twelve rows in county-code order: January 2026 residential therms to the nearest 10,000, residential disconnections for nonpayment completed in January, residential accounts on a low-income payment plan on 31 January 2026:
   - Ashwell: 940,000 therms, 13 disconnections, 217 accounts
   - Brennock: 1,310,000 therms, 13 disconnections, 384 accounts
   - Farrish: 930,000 therms, 9 disconnections, 198 accounts
   - Halvern: 1,010,000 therms, 14 disconnections, 270 accounts
   - Keswin: 620,000 therms, 5 disconnections, 176 accounts
   - Merrion: 720,000 therms, 11 disconnections, 215 accounts
   - Ottercreek: 680,000 therms, 8 disconnections, 211 accounts
   - Pellow: 1,050,000 therms, 13 disconnections, 344 accounts
   - Rennick: 1,180,000 therms, 12 disconnections, 282 accounts
   - Sauvain: 500,000 therms, 8 disconnections, 141 accounts
   - Tillery: 840,000 therms, 12 disconnections, 252 accounts
   - Wynnell: 480,000 therms, 8 disconnections, 154 accounts

### heating_grant_split_2026_27.xlsx

1. The twelve 2026-27 awards to the nearest $5,000, summing to $18,640,000:
   - Ashwell: $1,710,000
   - Brennock: $2,380,000
   - Farrish: $1,685,000
   - Halvern: $1,840,000
   - Keswin: $1,125,000
   - Merrion: $1,310,000
   - Ottercreek: $1,230,000
   - Pellow: $1,905,000
   - Rennick: $2,145,000
   - Sauvain: $910,000
   - Tillery: $1,525,000
   - Wynnell: $875,000

### heating_grant_split_2026_27.png

1. Twelve bars from largest to smallest, each labelled with its award: Brennock, Rennick, Pellow, Halvern, Ashwell, Farrish, Tillery, Merrion, Ottercreek, Keswin, Sauvain, Wynnell
