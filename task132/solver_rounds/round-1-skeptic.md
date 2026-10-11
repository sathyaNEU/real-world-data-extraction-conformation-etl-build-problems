# solver round: round 1, skeptic

**Proxy score 85.4 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 43.4 of 58). Main call LANDED. 4 of 6 ask items cracked (80 per cent of tokens).

## Main call

golden: Order 17 lots (425 modules) of the VPR340-PSU-02 power supply module in Veldtek's last-time buy, for CAD 835,125.

solver: Order 17 lots (425 VPR340-PSU-02 modules) at the last-time-buy price of CAD 835,125. Added to the 29 usable modules (23 serviceable at Central Stores, North Depot and South Depot, plus 6 at the Veldtek repair centre under open RMA; the 7 in quarantine are excluded), that gives 454 modules. Under AM-PC-014 the Poisson chance of covering every expected failure is 98.9 per cent. The expected failures are 407.5 across the 1,177 in-service VPR-340 relays, from October 2026 to each substation's commissioning month in the approved 2026 Protection Renewal Programme, or to December 2035 for the 9 substations outside the programme period. 16 lots would give only 86.2 per cent, below the 95 per cent test.

tokens matched 4 of 5 (17, 425, 835,125, Order, Veldtek's)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| vpr340_psu_final_buy.xlsx | 1 | 4 | 4 | 100% |
| vpr340_psu_final_buy.xlsx | 2 | 17 | 22 | 77% |
| vpr340_psu_final_buy.xlsx | 3 | 22 | 24 | 92% |
| vpr340_psu_final_buy.xlsx | 4 | 7 | 7 | 100% |
| psu_last_time_buy_memo.docx | 1 | 4 | 5 | 80% |
| psu_last_time_buy_memo.docx | 2 | 0 | 2 | 0% |

## Solver's path

1. Read AM-PC-014 rev 3 to fix the method.
2. Counted exposure only over the work-order history, Jan 2021 to Sep 2026 (69 months from EAM go-live), not whole life since installation.
3. Poisson cover P(D <= 29 + 25L) with mean 407.47; 17 lots is the smallest order at or above 95%.

confidence: high

notes: 

### vpr340_psu_final_buy.xlsx (solver's answers)
- Lot call, modules and cost: lots to order = 17; modules bought = 425 (29 available + 425 = 454 cover stock); cost = CAD 835,125 (17 x CAD 49,125, to the nearest dollar); cover at 17 lots = 98.9%
- Cover chance and cost for each order from 15 to 21 lots: 15 lots: 44.5%, $736,875; 16 lots: 86.2%, $786,000; 17 lots: 98.9%, $835,125; 18 lots: 100.0% (99.97), $884,250; 19 lots: 100.0%, $933,375; 20 lots: 100.0%, $982,500; 21 lots: 100.0%, $1,031,625 (per cent to 1 dp; CAD to the nearest dollar)
- Expected failures by period (to 1 dp): Oct-Dec 2026: 16.6; 2027: 63.7; 2028: 63.2; 2029: 57.9; 2030: 51.7; 2031: 47.6; 2032: 40.8; 2033: 29.7; 2034: 22.0; 2035: 14.2; total to end of support: 407.5
- VPR-340 relays still supported on 1 January: 2027: 1,170; 2028: 1,047; 2029: 927; 2030: 802; 2031: 678; 2032: 545; 2033: 439; 2034: 318; 2035: 201 (relays)
- Expected failures to end of support by operating region (to 1 dp): Central: 104.5; North: 176.3; South: 126.6 (total 407.5)

### psu_last_time_buy_memo.docx (solver's answers)
- Opening lot count and cover: 17 lots (425 modules) giving 98.9% chance of covering all failures to end of support; cost CAD 835,125; based on 29 available modules and 407.5 expected failures (16 lots would give only 86.2%)
- Chart of expected failures by year: Oct-Dec 2026: 16.6; 2027: 63.7; 2028: 63.2; 2029: 57.9; 2030: 51.7; 2031: 47.6; 2032: 40.8; 2033: 29.7; 2034: 22.0; 2035: 14.2 (expected failures, 1 dp)
