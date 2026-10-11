# task132: VPR-340 power supply modules, the last-time buy

## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance: obsolete protection relay spares).
**Analytical objective:** Forecasting & Predictive Modeling (expected module failures over each relay's remaining support, by module age band).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Order 13 lots (325 modules) of the VPR340-PSU-02 power supply module in Veldtek's last-time buy, for CAD 638,625.**

With the 15 modules available, 13 lots cover every expected failure to the end of support with a 99.1 per cent chance, and 12 lots reach only 83.6 per cent. Not the present module's band rate carried through every remaining month, which keeps a module in the relay after it has probably failed when its replacement starts again in the 0-9 band. Not rates by relay age from installation dates, which ignore the modules already replaced before the count.

## 2. Critical Components

1. Failure rates per module-year by age band: **0.0052** (0-9), **0.0233** (10-14), **0.0508** (15-19), **0.1186** (20-24), **0.2945** (25 and over)
2. Expected PSU failures from 1 October 2026 to the end of support: **298.6**
3. Modules available at the 30 September 2026 count: **15**
4. Chance that the stock covers all failures with 13 lots: **99.1%** (12 lots: **83.6%**)

## 3. Step-by-Step Solution

1. Took VPR-340 PSU failures from `eam_work_orders_protection_2021-01_2026-09.csv` as AM-PC-014 5.1 defines them, each in the age band of the module it removed, aged from that module's fitted date in `psu_rotating_item_history_2021-01_2026-09.csv` on the first of the reported month (5.2).
2. Counted module-months in service in each band over the period the work-order history covers, from January 2021 (AM-PC-014 5.3, `eam_extract_dictionary.txt`), and divided to get the band rates.
3. Set each in-service relay's end of support from the Approved 2026 sheet of `protection_renewal_program_2026.xlsx` by its bay, taking the stage that replaces the bay in staged schemes, or through December 2035 for a station with no scheme in the program period (AM-PC-014 4).
4. Aged each relay's present module month by month to its end of support, each month adding the chance it is still fitted times its band rate over twelve plus the chance it has already failed times the 0-9 band rate over twelve, because a failed module is replaced from the buy and a module's age runs from its own fitted date (AM-PC-014 1, 3, 6.1 and 6.2): 298.6 expected failures.
5. Counted available modules in `spares_stock_2026-09-30.csv` as serviceable plus at Veldtek repair, quarantine excluded (AM-PC-014 7): 15.
6. Took the smallest number of 25-module lots whose Poisson chance of covering all failures is at least 95 per cent (AM-PC-014 8): 13 lots give 99.1 per cent, 12 lots 83.6 per cent.
7. Priced the order at CAD 1,965 per module from `veldtek_vpr340_eol_notice.pdf`: 325 modules for CAD 638,625.
8. Recommendation: order 13 lots.

## 4. Deliverable Answers

### vpr340_psu_final_buy.xlsx

1. Lots to order: 13 lots, 325 modules, CAD 638,625
2. Chance of covering all failures, per cent to one decimal, and cost of each order:
   - 8 lots: 0.0%, CAD 393,000
   - 9 lots: 0.0%, CAD 442,125
   - 10 lots: 2.6%, CAD 491,250
   - 11 lots: 32.2%, CAD 540,375
   - 12 lots: 83.6%, CAD 589,500
   - 13 lots: 99.1%, CAD 638,625
   - 14 lots: 100.0%, CAD 687,750
   - 15 lots: 100.0%, CAD 736,875
   - 16 lots: 100.0%, CAD 786,000
   - 17 lots: 100.0%, CAD 835,125
   - 18 lots: 100.0%, CAD 884,250
   - 19 lots: 100.0%, CAD 933,375
   - 20 lots: 100.0%, CAD 982,500
   - 21 lots: 100.0%, CAD 1,031,625
   - 22 lots: 100.0%, CAD 1,080,750
3. Expected failures by period, one decimal, with VPR-340 relays still supported on 1 January:
   - October to December 2026: 11.6
   - 2027: 45.1; 1,163 relays supported on 1 January
   - 2028: 44.7; 1,094 relays
   - 2029: 42.9; 973 relays
   - 2030: 40.6; 884 relays
   - 2031: 36.1; 783 relays
   - 2032: 30.0; 695 relays
   - 2033: 23.9; 564 relays
   - 2034: 16.0; 373 relays
   - 2035: 7.8; 201 relays
4. Expected failures to the end of support by operating region, one decimal:
   - North: 117.5
   - Central: 54.7
   - South: 126.4

### psu_last_time_buy_memo.docx

1. Opens on the order of 13 lots and its 99.1 per cent cover, against 83.6 per cent for 12 lots.
2. Bar chart of expected failures by year, October to December 2026 then 2027 to 2035, each bar labelled to one decimal.
