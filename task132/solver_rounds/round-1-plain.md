# solver round: round 1, plain

**Proxy score 85.0 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 43.0 of 58). Main call LANDED. 4 of 6 ask items cracked (80 per cent of tokens).

## Main call

golden: Order 17 lots (425 modules) of the VPR340-PSU-02 power supply module in Veldtek's last-time buy, for CAD 835,125.

solver: Order 17 lots of VPR340-PSU-02 from Veldtek, which is 425 modules for CAD $835,125 at $1,965 per module ($49,125 per lot). Added to the 29 usable modules on hand (23 serviceable plus 6 at Veldtek under open RMA; the 7 quarantined are left out), that gives 454 modules. Expected VPR-340 PSU failures from October 2026 to the end of support under the approved 2026 Protection Renewal Programme are 407.5. Under Poisson demand, 454 modules cover all failures with 98.9% probability. 16 lots would give only 86.2%, below the AM-PC-014 95% test.

tokens matched 4 of 5 (17, 425, 835,125, Order, Veldtek's)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| vpr340_psu_final_buy.xlsx | 1 | 4 | 4 | 100% |
| vpr340_psu_final_buy.xlsx | 2 | 16 | 22 | 73% |
| vpr340_psu_final_buy.xlsx | 3 | 22 | 24 | 92% |
| vpr340_psu_final_buy.xlsx | 4 | 7 | 7 | 100% |
| psu_last_time_buy_memo.docx | 1 | 4 | 5 | 80% |
| psu_last_time_buy_memo.docx | 2 | 0 | 2 | 0% |

## Solver's path

1. AM-PC-014 rules
2. stock 29 available
3. 1,240 relays, 1,177 in service
4. 284 failures CM/EM PSU COMP/CLOSE; 12 CANC and 128 LOG excluded
5. Exposure covers EAM history from go-live, Jan 2021 to Sep 2026 (per eam_extract_dictionary.txt): 83,182 relay-months; band rates 0.0040 0.0122 0.0287 0.0741 0.1538 0.1616
6. Approved 2026 programme, 71,231 forward relay-months, expected failures 407.47
7. Poisson: 16 lots 86.2%, 17 lots 98.9%

confidence: high

notes: 

### vpr340_psu_final_buy.xlsx (solver's answers)
- Lots to order: 17 lots
- Modules the order buys: 425 modules (17 x 25). With the 29 available, 454 modules in total
- Cost at last-time-buy price: $835,125 (CAD, to the nearest dollar)
- Cover and cost for orders of 15 to 21 lots: 15 lots: 44.5%, $736,875; 16 lots: 86.2%, $786,000; 17 lots: 98.9%, $835,125; 18 lots: 100.0% (99.97), $884,250; 19 lots: 100.0%, $933,375; 20 lots: 100.0%, $982,500; 21 lots: 100.0%, $1,031,625
- Expected failures by period (to one decimal): Oct-Dec 2026: 16.6; 2027: 63.7; 2028: 63.2; 2029: 57.9; 2030: 51.7; 2031: 47.6; 2032: 40.8; 2033: 29.7; 2034: 22.0; 2035: 14.2; total to end of support: 407.5
- VPR-340 relays still supported on 1 January: 2027: 1,170; 2028: 1,047; 2029: 927; 2030: 802; 2031: 678; 2032: 545; 2033: 439; 2034: 318; 2035: 201
- Expected failures to end of support by operating region: Central: 104.5; North: 176.3; South: 126.6 (total 407.5)

### psu_last_time_buy_memo.docx (solver's answers)
- Opening: lot count and the cover it gives: Buy 17 lots (425 modules); with the 29 available modules covers all expected failures with 98.9% probability; 16 lots gives 86.2%
- Chart: expected failures by year: Oct-Dec 2026: 16.6; 2027: 63.7; 2028: 63.2; 2029: 57.9; 2030: 51.7; 2031: 47.6; 2032: 40.8; 2033: 29.7; 2034: 22.0; 2035: 14.2
