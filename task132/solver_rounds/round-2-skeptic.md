# solver round: round 2, skeptic

**Proxy score 36.8 / 100** (recommendation 1.0 of 35, instruction 7.0 of 7, asks 28.8 of 58). Main call missed. 1 of 6 ask items cracked (80 per cent of tokens).

## Main call

golden: Order 13 lots (325 modules) of the VPR340-PSU-02 power supply module in Veldtek's last-time buy, for CAD 638,625.

solver: Order 18 lots (450 VPR340-PSU-02 modules) for $884,250 at the last-time-buy price. With the 14 modules we can use (12 serviceable plus 2 at Veldtek under open RMA), that gives 464 modules against 411.9 expected failures to the end of support, a 99.5% chance of covering every failure. 17 lots gives only 91.2%.

tokens matched 1 of 5 (13, 325, 638,625, Order, Veldtek's)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| vpr340_psu_final_buy.xlsx | 1 | 3 | 4 | 75% |
| vpr340_psu_final_buy.xlsx | 2 | 42 | 46 | 91% |
| vpr340_psu_final_buy.xlsx | 3 | 13 | 24 | 54% |
| vpr340_psu_final_buy.xlsx | 4 | 4 | 7 | 57% |
| psu_last_time_buy_memo.docx | 1 | 1 | 5 | 20% |
| psu_last_time_buy_memo.docx | 2 | 0 | 2 | 0% |

## Solver's path

1. Failures: 197 CM/EM PSU COMP/CLOSE on VPR-340; 10 CANC and 128 LOG excluded; matches 197 FAILED removals.
2. Failure age from fitted_date on the 1st of the reported month: 5 / 51 / 61 / 66 / 14 by band.
3. Exposure: module-months Jan 2021 to Sep 2026 for modules fitted to in-service relays: 83,180, equal to relay-months; 30,811 / 26,740 / 17,007 / 7,944 / 678.
4. Rates per module-year: 0.00195, 0.0229, 0.0430, 0.0997, 0.2478.
5. Support by bay from the Approved 2026 sheet; 87 relays to Dec 2035.
6. Projection: aged each relay's current module forward with no replacement: 411.95 expected failures.
7. Available 14; quarantine excluded.
8. Cover: 17 lots 91.16%, 18 lots 99.45%: order 18 lots, $884,250.

confidence: high

notes: Residual risk: AM-PC-014 6.2 'module-months expected in each band' read as ageing the current module with no allowance for replacement; a renewal model gives about 298 and 13 lots, but the procedure does not state it.

### vpr340_psu_final_buy.xlsx (solver's answers)
- Lots to order, modules and cost: 18 lots; 450 modules; $884,250
- Cover and cost, 8 to 22 lots: 8: 0.0%, $393,000; 9: 0.0%, $442,125; 10: 0.0%, $491,250; 11: 0.0%, $540,375; 12: 0.0%, $589,500; 13: 0.0%, $638,625; 14: 0.9%, $687,750; 15: 13.4%, $736,875; 16: 55.3%, $786,000; 17: 91.2%, $835,125; 18: 99.5%, $884,250; 19: 100.0%, $933,375; 20: 100.0%, $982,500; 21: 100.0%, $1,031,625; 22: 100.0%, $1,080,750
- Expected failures by period: Oct-Dec 2026: 11.4; 2027: 48.6; 2028: 52.8; 2029: 56.1; 2030: 56.1; 2031: 51.7; 2032: 47.9; 2033: 39.9; 2034: 30.9; 2035: 16.5 (total 411.9)
- VPR-340 relays still supported on 1 January: 2027: 1,162; 2028: 1,085; 2029: 999; 2030: 909; 2031: 796; 2032: 669; 2033: 565; 2034: 381; 2035: 218 (1,176 at the stock count)
- Expected failures to end of support by operating region: Central 164.1; North 114.0; South 133.9

### psu_last_time_buy_memo.docx (solver's answers)
- Opening: lot count and cover: 18 lots (450 modules, $884,250), with a 99.5% chance of covering all failures (464 usable modules against a mean of 411.9 failures)
- Chart: expected failures by year: Oct-Dec 2026 11.4; 2027 48.6; 2028 52.8; 2029 56.1; 2030 56.1; 2031 51.7; 2032 47.9; 2033 39.9; 2034 30.9; 2035 16.5
