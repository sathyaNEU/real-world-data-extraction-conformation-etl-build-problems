# solver round: round 1, plain

**Proxy score 84.9 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 42.9 of 58). Main call LANDED. 4 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: The group ledger will post $951,870 of depreciation on Yacaaba Radiology's assets from January to June 2027.

solver: On the register as it loads at 1 January 2027 (201 assets after the 2 October register is de-duplicated, reconciled to the 9 October 2026 trial balance and verified against the count), the group ledger will post $951,870 of depreciation on Yacaaba's assets from January to June 2027 (951,870.13 to the cent). By site that is Charlestown $447,757, Cessnock $177,711, Raymond Terrace $174,302 and Maitland $152,100. The rebuilt schedules replay every depreciation posting from July 2025 to September 2026, account by account and month by month, to the cent, so all six accounts can load.

tokens matched 3 of 4 (951,870, Yacaaba Radiology's, January, June)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| fa_load_2027-01-01.csv | 1 | 2 | 5 | 40% |
| fa_load_2027-01-01.csv | 2 | 5 | 9 | 56% |
| fa_load_2027-01-01.csv | 3 | 1 | 3 | 33% |
| cutover_signoff.docx | 1 | 3 | 4 | 75% |
| cutover_signoff.docx | 2 | 23 | 26 | 88% |
| cutover_signoff.docx | 3 | 13 | 13 | 100% |
| cutover_signoff.docx | 4 | 13 | 13 | 100% |
| cutover_signoff.docx | 5 | 3 | 3 | 100% |

## Solver's path

1. Removed the six untagged duplicate register lines that repeat an earlier line's invoice (1343, 1344, 1346 and 1349 are furniture and fittings, $14,849.80; 1348 and 1350 are computers, $5,851.04). After that, capitalised in-use cost by category ties to the 3 Oct trial balance for every asset account.
2. Rebuilt the conventions from YCB_asset_register Rates and the FY2025 notes. Each monthly charge is cost / life in months, rounded to the cent and starting in the month of purchase; the last month takes the remainder and the disposal month is charged. Upgrades run to the end of the parent asset's 120-month life, using Existing Asset in the capital approvals file. Computers change prospectively from Jul 2025: NBV at 30 Jun 2025 over (48 - months elapsed). The OPG/CBCT 1072 carries the $38k impairment and then 5,599.67 over 47 months (119.14 a month). The ex-Bremer Voluson 1271 runs at 2,583.89 a month for 20 months from Feb 2026.
3. Replayed the GL depreciation journals: every account in every month from 2025-07 to 2026-09 reproduces to the cent. The opening balances at 1 Jul 2025 also tie to the cent for cost and accumulated depreciation in all 6 accounts.
4. The balance of record is the 9 Oct run of the trial balance. The joinery reclass in it is asset 1120 (cost 47,862.40, accumulated 26,722.95 = 67 x 398.85), so 1120 moves to 1-6140 and to the Leasehold improvements class. Group classes come from the approved v2 mapping.
5. Verification: the count closes at 5pm AEDT on 9 Oct, which is 06:00 UTC, so the 12 scans after that are excluded. Serial scans were matched to Serial No, the Q tags (group loan stock) were dropped, and the signed Raymond Terrace count sheet was used, including its H01660 write-in. Each sighted asset takes the site where it was sighted (12 moves). Of the 15 tagged assets not sighted, 10 have nil book value and are written off; the other 5 (1146, 1221, 1234, 1239, 1264) load at their register site.
6. Projected each schedule to 31 Dec 2026: Oct-Dec ledger depreciation is $617,742.78 and the load is 201 assets with book value $6,417,165.88. Load cost plus write-offs equals the trial balance cost of 27,862,081.93.
7. Applied the standard's section 6 group method: round(NBV / remaining months) each month, with the last month taking the remainder. Jan-Jun 2027 comes to 951,870.13 (the legacy schedule would give 951,870.97). Then aggregated by site of record and by group class.

confidence: high

notes: Asset 1120 is classed Leasehold improvements (v2 mapping, after the reclass) but keeps the 10-year furniture life it was depreciated over, so Jan-Jun is 2,393.10. Re-lifing it over 15 years as leasehold improvement would cut the total by about $1,305; nothing in the folder says the rate was restated. The 5 unsighted assets that still have book value load at their register site and are listed for investigation. Scripts were run inline and not saved under work/, because this session was read-only.

### fa_load_2027-01-01.csv (solver's answers)
- rows that load: 201 assets: 211 capitalised in-use register lines, less 10 unsighted assets with nil book value written off on 31 Dec 2026 (1010, 1012, 1017, 1080, 1084, 1090, 1100, 1141, 1148, 1152; cost $463,590.49). Six duplicate untagged lines (1343, 1344, 1346, 1348, 1349, 1350; $20,700.84) were removed before this.
- total cost: 27,398,491.44 AUD (to the cent). Adding the $463,590.49 written off gives 27,862,081.93, which equals the cost total in the 9 Oct 2026 trial balance.
- total accumulated depreciation at 31 Dec 2026: 20,981,325.56 AUD (to the cent)
- total book value loading: 6,417,165.88 AUD (to the cent)
- total Jan-Jun 2027 charge: 951,870.13 AUD (to the cent). Each asset is charged round(NBV / remaining months) a month, the last month takes the remainder, and the remaining months come from the legacy schedule.
- Jan-Jun 2027 charge by site: CHA 447,757.20; CES 177,711.18; RAY 174,301.95; MAI 152,099.80 AUD (to the cent)
- book value loading by site: CHA 2,650,750.29; RAY 1,812,445.29; MAI 979,452.66; CES 974,517.64 AUD (to the cent)
- group asset class: Classes come from the approved v2 mapping, not the v3 draft. Ultrasound is Clinical equipment. Furniture and fittings and Motor vehicles stay separate classes. Asset 1120 (reception counter and joinery) is in Leasehold improvements because it sits in account 1-6140 after the reclass.
- sites of record that change: 1056, 1068, 1083, 1110, 1217 move to MAI; 1122 moves to RAY (from the count sheet write-in); 1157, 1256, 1271 move to CES; 1179, 1232, 1257 move to CHA
- examples of remaining life and charge: 1271 (Voluson ex Bremer): NBV 23,254.93, 9 months remaining, Jan-Jun 15,503.28. 1072 (impaired OPG/CBCT): charged 119.14 a month. 1120: NBV at the F&F 10-year life, Jan-Jun 2,393.10.

### cutover_signoff.docx (solver's answers)
- headline Jan-Jun 2027 depreciation: $951,870 (whole dollars)
- Charlestown (CHA): Book value 30 Sep 2026 $2,985,940; Oct-Dec ledger depreciation $335,189; book value loading $2,650,750; Jan-Jun 2027 charge $447,757; 28 assets with nothing left to depreciate, original cost $3,787,437
- Maitland (MAI): Book value 30 Sep 2026 $1,083,088; Oct-Dec ledger depreciation $103,636; book value loading $979,453; Jan-Jun 2027 charge $152,100; 24 assets with nothing left to depreciate, original cost $3,304,124
- Cessnock (CES): Book value 30 Sep 2026 $1,063,440; Oct-Dec ledger depreciation $88,922; book value loading $974,518; Jan-Jun 2027 charge $177,711; 5 assets with nothing left to depreciate, original cost $20,223
- Raymond Terrace (RAY): Book value 30 Sep 2026 $1,902,441; Oct-Dec ledger depreciation $89,996; book value loading $1,812,445; Jan-Jun 2027 charge $174,302; 12 assets with nothing left to depreciate, original cost $157,448
- totals across sites: Book value 30 Sep $7,034,909; Oct-Dec $617,743; book value loading $6,417,166; Jan-Jun $951,870; 69 assets with nothing left to depreciate, original cost $7,269,232
- book value loading by group asset class: Imaging equipment $2,877,477; Leasehold improvements $2,826,213; Clinical equipment $438,447; Computer equipment $131,086; Furniture and fittings $122,749; Motor vehicles $21,194; total $6,417,166
- bar chart: Jan-Jun 2027 charge by site, each bar labelled in dollars: CHA $447,757; CES $177,711; RAY $174,302; MAI $152,100. Title: 'January to June 2027 depreciation by site: $951,870'
