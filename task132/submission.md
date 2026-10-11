# task132: VPR-340 power supply modules, the last-time buy

## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance: obsolete protection relay spares).
**Analytical objective:** Forecasting & Predictive Modeling (expected module failures over each relay's remaining support, by module age band).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Order 13 lots (325 modules) of the VPR340-PSU-02 power supply module in Veldtek's last-time buy, for CAD 638,625.**

With the 15 modules available, 13 lots cover every expected failure to the end of support with a 99.1 per cent chance, and 12 lots reach only 83.2 per cent. Not the present module's band rate carried through every remaining month, which keeps a module in the relay after it has probably failed when its replacement starts again in the 0-9 band. Not rates by relay age from installation dates, which ignore the modules already replaced before the count.

## 2. Critical Components

1. Expected PSU failures from 1 October 2026 to the end of support: **298.9**
2. Modules available at the 30 September 2026 count: **15**
3. Chance that the stock covers all failures with 13 lots: **99.1%** (12 lots: **83.2%**)

## 3. Step-by-Step Solution

1. Took VPR-340 PSU failures from `eam_work_orders_protection_2021-01_2026-09.csv` as AM-PC-014 5.1 defines them, each in the age band of the module it removed, aged from that module's fitted date in `psu_rotating_item_history_2021-01_2026-09.csv` on the first of the reported month (5.2).
2. Counted module-months in service in each band from January 2021, where the work-order history begins (`eam_extract_dictionary.txt`), and divided to get the band rates (5.3).
3. Set each in-service relay's end of support from the Approved 2026 sheet of `protection_renewal_program_2026.xlsx` by its bay, taking the stage that replaces the bay in staged schemes, or December 2035 outside the program period (AM-PC-014 4).
4. Aged each relay's present module month by month to its end of support, counting its band rate over twelve while it is likely to survive and the 0-9 band rate for the new module that replaces it after a failure (AM-PC-014 6): 298.9 expected failures.
5. Counted available modules in `spares_stock_2026-09-30.csv` as serviceable plus at Veldtek repair, quarantine excluded (AM-PC-014 7): 15.
6. Took the smallest number of 25-module lots whose Poisson chance of covering all failures is at least 95 per cent (AM-PC-014 8): 13 lots give 99.1 per cent, 12 lots 83.2 per cent.
7. Priced the order at CAD 1,965 per module from `veldtek_vpr340_eol_notice.pdf`: 325 modules for CAD 638,625.
8. Recommendation: order 13 lots.

## 4. Deliverable Answers

### vpr340_psu_final_buy.xlsx

1. Lots to order: 13 lots, 325 modules, CAD 638,625
2. Chance of covering all failures, per cent to one decimal, and cost of each order:
   - 8 lots: 0.0%, CAD 393,000
   - 9 lots: 0.0%, CAD 442,125
   - 10 lots: 2.5%, CAD 491,250
   - 11 lots: 31.6%, CAD 540,375
   - 12 lots: 83.2%, CAD 589,500
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
   - October to December 2026: 11.4
   - 2027: 45.6; 1,162 relays supported on 1 January
   - 2028: 45.2; 1,085 relays
   - 2029: 43.7; 999 relays
   - 2030: 40.1; 909 relays
   - 2031: 34.2; 796 relays
   - 2032: 29.4; 669 relays
   - 2033: 23.3; 565 relays
   - 2034: 17.0; 381 relays
   - 2035: 8.9; 218 relays
4. Expected failures to the end of support by operating region, one decimal:
   - North: 87.2
   - Central: 122.1
   - South: 89.6

### psu_last_time_buy_memo.docx

1. Opens on the order of 13 lots and its 99.1 per cent cover, against 83.2 per cent for 12 lots.
2. Bar chart of expected failures by year, October to December 2026 then 2027 to 2035, each bar labelled to one decimal.
