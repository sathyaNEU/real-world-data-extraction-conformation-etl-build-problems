# task132: VPR-340 power supply modules, the last-time buy

## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance: obsolete protection relay spares).
**Analytical objective:** Forecasting & Predictive Modeling (expected module failures over each relay's remaining support, by age band).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Order 19 lots (475 modules) of the VPR340-PSU-02 power supply module in Veldtek's last-time buy, for CAD 933,375.**

With the 39 modules available, 19 lots cover every expected failure to the end of support with a 98.3 per cent chance, and 18 lots reach only 84.2 per cent. Not the last twelve months' failure rate carried forward, which misses the fleet ageing into its high-failure bands. Not age-band rates over relay-years counted from installation, which divide failures recorded only since January 2021 by years in which no failure could have been recorded.

## 2. Critical Components

1. Expected PSU failures from 1 October 2026 to the end of support: **467.8**
2. Modules available at the 30 September 2026 count: **39**
3. Chance that the stock covers all failures with 19 lots: **98.3%** (18 lots: **84.2%**)

## 3. Step-by-Step Solution

1. Took VPR-340 PSU failures from `eam_work_orders_protection_2021-01_2026-09.csv` as AM-PC-014 4.1 defines them (CM or EM, failed component PSU, status COMP or CLOSE), each in the age band of its relay on the first of the failure month.
2. Counted relay-months in service in each band from January 2021, where the work-order history begins (`eam_extract_dictionary.txt`), because a relay-month before then has no work order that could record a failure.
3. Set each in-service relay's end of support from the Approved 2026 sheet of `protection_renewal_programme_2026.xlsx`: its substation's commissioning month, or December 2035 outside the programme period (AM-PC-014 3).
4. Applied the band rates to each relay's relay-months by age band from October 2026 to its end of support: 467.8 expected failures.
5. Counted available modules in `spares_stock_2026-09-30.csv` as serviceable plus at Veldtek repair, quarantine excluded (AM-PC-014 5): 39.
6. Took the smallest number of 25-module lots whose Poisson chance of covering all failures is at least 95 per cent (AM-PC-014 6): 19 lots give 98.3 per cent, 18 lots 84.2 per cent.
7. Priced the order at CAD 1,965 per module from `veldtek_vpr340_eol_notice.pdf`: 475 modules for CAD 933,375.
8. Recommendation: order 19 lots.

## 4. Deliverable Answers

### vpr340_psu_final_buy.xlsx

1. Lots to order: 19 lots, 475 modules, CAD 933,375
2. Chance of covering all failures, per cent to one decimal, and cost of each order:
   - 15 lots: 0.6%, CAD 736,875
   - 16 lots: 9.4%, CAD 786,000
   - 17 lots: 44.2%, CAD 835,125
   - 18 lots: 84.2%, CAD 884,250
   - 19 lots: 98.3%, CAD 933,375
   - 20 lots: 99.9%, CAD 982,500
   - 21 lots: 100.0%, CAD 1,031,625
3. Expected failures by period, one decimal, with VPR-340 relays still supported on 1 January:
   - October to December 2026: 17.2
   - 2027: 68.2; 1,171 relays supported on 1 January
   - 2028: 68.7; 1,052 relays
   - 2029: 68.5; 926 relays
   - 2030: 61.9; 800 relays
   - 2031: 59.3; 692 relays
   - 2032: 50.6; 571 relays
   - 2033: 39.7; 445 relays
   - 2034: 23.5; 321 relays
   - 2035: 10.2; 208 relays
4. Expected failures to the end of support by operating region (from April 2024), one decimal:
   - North: 230.5
   - Central: 105.3
   - South: 132.0

### psu_last_time_buy_memo.docx

1. Opens on the order of 19 lots and its 98.3 per cent cover, against 84.2 per cent for 18 lots.
2. Bar chart of expected failures by year, October to December 2026 then 2027 to 2035, each bar labelled to one decimal.
