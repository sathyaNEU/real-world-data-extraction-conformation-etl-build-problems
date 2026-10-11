# solver round: round 3

**Proxy score 37.0 / 100** (recommendation 1.0 of 35, instruction 7.0 of 7, asks 29.0 of 58). Main call missed. 1 of 6 ask items cracked (80 per cent of tokens).

## Main call

golden: Order 13 lots (325 modules) of the VPR340-PSU-02 power supply module in Veldtek's last-time buy, for CAD 638,625.

solver: Order 19 lots of VPR340-PSU-02 (475 modules, $933,375 at the $1,965 last-time-buy price): with 15 usable modules (12 serviceable + 3 at Veldtek under open RMA, 7 quarantined excluded) against 431.4 expected failures to end of support, 19 lots gives 99.7% Poisson cover while 18 lots gives only 94.8%, below AM-PC-014's 95% threshold.

tokens matched 1 of 5 (13, 325, 638,625, Order, Veldtek's)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| vpr340_psu_final_buy.xlsx | 1 | 3 | 4 | 75% |
| vpr340_psu_final_buy.xlsx | 2 | 41 | 46 | 89% |
| vpr340_psu_final_buy.xlsx | 3 | 14 | 24 | 58% |
| vpr340_psu_final_buy.xlsx | 4 | 4 | 7 | 57% |
| psu_last_time_buy_memo.docx | 1 | 1 | 5 | 20% |
| psu_last_time_buy_memo.docx | 2 | 0 | 2 | 0% |

## Solver's path

1. eam_work_orders + asset register: CM/EM, status COMP/CLOSE, failed_component PSU, VPR-340 asset -> 210 failures; matched 1:1 on removal_wo to the 210 FAILED removals in psu_rotating_item_history
2. Banded each failure by module age (completed years from fitted_date) on the first of the reported month: bands 0-9/10-14/15-19/20-24/25+ = 15/49/68/66/12
3. Module-months Jan 2021-Sep 2026: module fitted on the 1st to an in-service relay = 34870/25253/16049/6676/489; rates per year 0.00516/0.02328/0.05084/0.11863/0.29448
4. 1,178 in-service VPR-340 relays joined by sub_code+bay to the 'Approved 2026' sheet (bay ranges expanded, stage by bay): 1,075 supported to their commissioning month (exclusive), 103 'Not in program period' supported through Dec 2035
5. Projected each relay's current module month by month from Oct 2026 at band rate/12: 77,531 module-months, 431.373 expected failures; split by period and by substations.csv current region (North 174.3, South 179.9, Central 77.2); relays supported on 1 Jan 2027-2035 counted from the monthly grid
6. spares_stock_2026-09-30: 12 serviceable + 3 AT REPAIR = 15 usable; 7 quarantined excluded per AM-PC-014 section 7
7. EOL notice: 25 per lot at $1,965; Poisson CDF(15+25n; 431.373): n=18 94.85% (fails), n=19 99.74% (passes) -> 19 lots, 475 modules, $933,375

confidence: Medium-high; the 18 vs 19 lot choice depends on the usable-module count.

notes: PS02-99-21775 returned by Veldtek on 29 Sep 2026 does not appear separately in the 30 Sep stock count; used the count as filed.

### vpr340_psu_final_buy.xlsx (solver's answers)
- lots to order: 19 lots
- modules bought: 475 modules
- cost at LTB price: $933,375 (CAD, nearest dollar)
- cover % and cost for 8-22 lots: 8: 0.0%, $393,000; 9: 0.0%, $442,125; 10: 0.0%, $491,250; 11: 0.0%, $540,375; 12: 0.0%, $589,500; 13: 0.0%, $638,625; 14: 0.1%, $687,750; 15: 2.3%, $736,875; 16: 22.3%, $786,000; 17: 67.2%, $835,125; 18: 94.8%, $884,250; 19: 99.7%, $933,375; 20: 100.0%, $982,500; 21: 100.0%, $1,031,625; 22: 100.0%, $1,080,750
- expected failures Oct-Dec 2026 and per year 2027-2035: Oct-Dec 2026: 11.7; 2027: 48.2; 2028: 52.3; 2029: 55.0; 2030: 58.0; 2031: 57.8; 2032: 53.2; 2033: 44.8; 2034: 32.4; 2035: 18.0 (total 431.4)
- VPR-340 relays supported on 1 January 2027-2035: 2027: 1163; 2028: 1094; 2029: 973; 2030: 884; 2031: 783; 2032: 695; 2033: 564; 2034: 373; 2035: 201
- expected failures to end of support by region: North 174.3; South 179.9; Central 77.2

### psu_last_time_buy_memo.docx (solver's answers)
- opening lot count and cover: 19 lots (475 modules, $933,375) giving 99.7% cover; 18 lots gives only 94.8%
- expected failures by year chart: Oct-Dec 2026 11.7; 2027 48.2; 2028 52.3; 2029 55.0; 2030 58.0; 2031 57.8; 2032 53.2; 2033 44.8; 2034 32.4; 2035 18.0
- basis figures: expected failures to end of support 431.4; usable modules 15 (12 serviceable + 3 at repair)
