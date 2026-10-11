# task132: VPR-340 power supply modules, the last-time buy

## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance: obsolete protection relay spares).
**Analytical objective:** Forecasting & Predictive Modeling (expected module failures over each relay's remaining support, by age band).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Order 17 lots (425 modules) of the VPR340-PSU-02 power supply module in Veldtek's last-time buy, for CAD 835,125.**

With the 29 modules available, 17 lots cover every expected failure to the end of support with a 98.9 per cent chance, and 16 lots reach only 86.2 per cent. Not the last twelve months' failure rate carried forward, which misses the fleet ageing into its high-failure bands. Not age-band rates over relay-years counted from installation, which divide failures recorded only since January 2021 by years in which no failure could have been recorded.

## 2. Critical Components

1. Expected PSU failures from 1 October 2026 to the end of support: **407.5**
2. Modules available at the 30 September 2026 count: **29**
3. Chance that the stock covers all failures with 17 lots: **98.9%** (16 lots: **86.2%**)

## 3. Step-by-Step Solution

1. Took VPR-340 PSU failures from `eam_work_orders_protection_2021-01_2026-09.csv` as AM-PC-014 4.1 defines them (CM or EM, failed component PSU, status COMP or CLOSE), each in the age band of its relay on the first of the failure month.
2. Counted relay-months in service in each band from January 2021, where the work-order history begins (`eam_extract_dictionary.txt`), because a relay-month before then has no work order that could record a failure.
3. Set each in-service relay's end of support from the Approved 2026 sheet of `protection_renewal_programme_2026.xlsx`: its substation's commissioning month, or December 2035 outside the programme period (AM-PC-014 3).
4. Applied the band rates to each relay's relay-months by age band from October 2026 to its end of support: 407.5 expected failures.
5. Counted available modules in `spares_stock_2026-09-30.csv` as serviceable plus at Veldtek repair, quarantine excluded (AM-PC-014 5): 29.
6. Took the smallest number of 25-module lots whose Poisson chance of covering all failures is at least 95 per cent (AM-PC-014 6): 17 lots give 98.9 per cent, 16 lots 86.2 per cent.
7. Priced the order at CAD 1,965 per module from `veldtek_vpr340_eol_notice.pdf`: 425 modules for CAD 835,125.
8. Recommendation: order 17 lots.

## 4. Deliverable Answers

### vpr340_psu_final_buy.xlsx

1. Lots to order: 17 lots, 425 modules, CAD 835,125
2. Chance of covering all failures, per cent to one decimal, and cost of each order:
   - 13 lots: 0.4%, CAD 638,625
   - 14 lots: 8.2%, CAD 687,750
   - 15 lots: 44.5%, CAD 736,875
   - 16 lots: 86.2%, CAD 786,000
   - 17 lots: 98.9%, CAD 835,125
   - 18 lots: 100.0%, CAD 884,250
   - 19 lots: 100.0%, CAD 933,375
3. Expected failures by period, one decimal, with VPR-340 relays still supported on 1 January:
   - October to December 2026: 16.6
   - 2027: 63.7; 1,170 relays supported on 1 January
   - 2028: 63.2; 1,047 relays
   - 2029: 57.9; 927 relays
   - 2030: 51.7; 802 relays
   - 2031: 47.6; 678 relays
   - 2032: 40.8; 545 relays
   - 2033: 29.7; 439 relays
   - 2034: 22.0; 318 relays
   - 2035: 14.2; 201 relays
4. Expected failures to the end of support by operating region, one decimal:
   - North: 176.3
   - Central: 104.5
   - South: 126.6

### psu_last_time_buy_memo.docx

1. Opens on the order of 17 lots and its 98.9 per cent cover, against 86.2 per cent for 16 lots.
2. Bar chart of expected failures by year, October to December 2026 then 2027 to 2035, each bar labelled to one decimal.
