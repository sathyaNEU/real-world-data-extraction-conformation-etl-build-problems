# solver round: round 2, plain

**Proxy score 87.4 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 45.4 of 58). Main call LANDED. 4 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: The group ledger will post $951,870 of depreciation on Yacaaba Radiology's assets from January to June 2027.

solver: Sign off the Yacaaba cutover: on the register as it loads (201 assets, net book value $6,417,166 at 31 Dec 2026), the group ledger will post $951,870 of depreciation from January to June 2027. By site that is Charlestown $447,757, Cessnock $177,711, Raymond Terrace $174,302 and Maitland $152,100.

tokens matched 3 of 4 (951,870, Yacaaba Radiology's, January, June)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| fa_load_2027-01-01.csv | 1 | 2 | 5 | 40% |
| fa_load_2027-01-01.csv | 2 | 5 | 9 | 56% |
| fa_load_2027-01-01.csv | 3 | 2 | 3 | 67% |
| cutover_signoff.docx | 1 | 3 | 4 | 75% |
| cutover_signoff.docx | 2 | 23 | 26 | 88% |
| cutover_signoff.docx | 3 | 13 | 13 | 100% |
| cutover_signoff.docx | 4 | 13 | 13 | 100% |
| cutover_signoff.docx | 5 | 3 | 3 | 100% |

## Solver's path

1. Read prompt.md, the email thread, the extract notes, FIN-STD-014, FIN-PRO-022, FIN-SPEC-009, the FY2025 notes and the mapping log. Balances of record are the trial balance run of 9 Oct, which is the last run before lock and includes the joinery reclass of 1120 ($47,862.40 cost and $26,722.95 AD moved from 1-6150 to 1-6140). The mapping to use is v2 (approved); v3 is only issued for review.
2. Register: kept Capitalised=Y only. Six untagged duplicate lines share an invoice (and serial) with a tagged line: 1343, 1344, 1346, 1348, 1349, 1350. Dropping them makes register cost agree with the GL opening balance and the 30 Sep cost in every account. Computer was $5,851.04 over and F&F $11,628.71 over (plus $3,221.09 from Sep 2025) before the drop.
3. Rebuilt per-asset schedules and matched all 90 account-months of GL depreciation (Jul 2025 to Sep 2026), the opening AD in each account and all 13 disposal AD journals, all to the cent. Rules: life-based monthly = cost/life rounded half-up; a full month in the month of purchase; the month of disposal is charged; the last month takes the remainder. Lives: imaging 120 months, options 60, ultrasound 72, leasehold 180, F&F 120, motor vehicles 72. Equipment upgrades run to the end of the host system's 120-month life (hosts taken from the approvals text). Computers: 36 months up to Jun 2025, then the NBV at 30 Jun 2025 over 48 minus months elapsed. 1072: $38,000 impairment in Jun 2025, then the remaining NBV over the rest of its 120 months ($119.14 a month). 1271: $134,362.28 AD brought forward, then 20 months at $2,583.89 from Feb 2026.
4. Rolled the schedules to 30 Sep 2026. Cost and AD by account match TB run 2 exactly, with 1120 sitting in 1-6140. Projected the legacy Oct-Dec 2026 charges on the same rules.
5. Verification: count window closes 5:00 pm AEDT on 9 Oct 2026 = 06:00 UTC, because daylight saving started 4 Oct. That excludes 12 late scans and leaves seven assets sighted only late (1012, 1080, 1084, 1090, 1148, 1221, 1239). Matched serial-only scans to the register serial; the duplicate 1350 is excluded, so 1106 is sighted at MAI. Q tags ignored as loan stock. RAY count sheet ticks used, plus the two write-ins: H01660 (1122, which moves to RAY) and H01847 (not capitalised). Twelve assets take the site where they were sighted.
6. Assets not sighted (15 tagged): 10 have nil NBV at 31 Dec 2026, are written off and do not load. 1146, 1221, 1234, 1239 and 1264 load at their register site. Untagged components and software load as the register records them. Result: 201 rows.
7. Group charge (FIN-STD-014 s6): monthly = NBV at 31 Dec 2026 / remaining months, rounded half-up; Jan-Jun = 6 months, or the whole NBV where 6 or fewer months remain. Total 95,187,013 cents = $951,870.13. Summed by load site and by v2 class from 1-6xxx accounts at the balances of record (1120 counts as Leasehold improvements).

confidence: high: the rebuild matches every GL depreciation posting and the TB run 2 balances to the cent; the remaining uncertainty is limited to the 1120 life and 1271 remaining-months judgement calls

notes: Judgement calls: (1) 1120 takes the Leasehold improvements class but stays on its legacy 120-month F&F life (50 months left), because the reclass moved AD across unchanged at 67 x $398.85. (2) 1271's NBV runs over 9 more months on the ledger's $2,583.89 pace (to Sep 2027), not over Bremer's original end of Aug 2027. Per-site figures cover loaded assets only. The 10 written-off assets had nil NBV and no Oct-Dec charge, so they change nothing. The two future replacements, QIG-CX-2436 and QIG-CX-2438, are not reflected because nothing is bought or sold after cutover. Scripts were run inline rather than saved to work/, because this session was read-only.

### fa_load_2027-01-01.csv (solver's answers)
- rows that load: 201 asset rows (one per asset that loads)
- total cost: 2,739,849,144 cents ($27,398,491.44)
- total accumulated depreciation at 31 Dec 2026: 2,098,132,556 cents ($20,981,325.56)
- total book value loading: 641,716,588 cents ($6,417,165.88)
- total Jan-Jun 2027 charge: 95,187,013 cents ($951,870.13)
- rows with 0 remaining months: 69 rows, nil book value, original cost 726,923,196 cents
- sample rows: 1271 Voluson E10 (ex Bremer): CES, Clinical equipment, cost 18,604,000 cents, AD 16,278,507, NBV 2,325,493, 9 months left, Jan-Jun 1,550,328 cents. 1072 OPG/CBCT: CES, Imaging equipment, NBV 345,515, 29 months, Jan-Jun 71,484. 1120 Reception counter and joinery: CHA, Leasehold improvements, NBV 1,994,290, 50 months, Jan-Jun 239,316. 1036 CT 64-slice: MAI, NBV 1,395,306, 2 months, Jan-Jun 1,395,306.
- excluded from the load: Six duplicate untagged register lines (1343, 1344, 1346, 1348, 1349, 1350). 57 items never capitalised. 22 disposed assets. Ten assets not sighted that have nil book value at cutover and are written off: 1010, 1012, 1017, 1080, 1084, 1090, 1100, 1141, 1148, 1152 (cost $463,590.49).
- loaded but listed for investigation (not sighted): 1146, 1221, 1234, 1239, 1264, each loaded at its register site
- site-of-record moves: 1056 to MAI, 1068 to MAI, 1083 to MAI, 1110 to MAI, 1122 to RAY, 1157 to CES, 1179 to CHA, 1217 to MAI, 1232 to CHA, 1256 to CES, 1257 to CHA, 1271 to CES

### cutover_signoff.docx (solver's answers)
- headline figure: $951,870 group-ledger depreciation, January to June 2027
- Charlestown (CHA): 72 assets. Book value at 30 Sep 2026 $2,985,940. Legacy charge Oct-Dec 2026 $335,189. Book value loading $2,650,750. Jan-Jun 2027 charge $447,757. 28 assets with nothing left to depreciate, original cost $3,787,437.
- Maitland (MAI): 53 assets. Book value at 30 Sep 2026 $1,083,088. Legacy charge Oct-Dec 2026 $103,636. Book value loading $979,453. Jan-Jun 2027 charge $152,100. 24 assets with nothing left to depreciate, original cost $3,304,124.
- Cessnock (CES): 37 assets. Book value at 30 Sep 2026 $1,063,440. Legacy charge Oct-Dec 2026 $88,922. Book value loading $974,518. Jan-Jun 2027 charge $177,711. 5 assets with nothing left to depreciate, original cost $20,223.
- Raymond Terrace (RAY): 39 assets. Book value at 30 Sep 2026 $1,902,441. Legacy charge Oct-Dec 2026 $89,996. Book value loading $1,812,445. Jan-Jun 2027 charge $174,302. 12 assets with nothing left to depreciate, original cost $157,448.
- all sites combined: Book value at 30 Sep 2026 $7,034,909. Oct-Dec 2026 $617,743. Book value loading $6,417,166. Jan-Jun 2027 $951,870. 69 assets with nothing left to depreciate, original cost $7,269,232.
- book value loading by group asset class (approved v2 mapping): Imaging equipment $2,877,477. Leasehold improvements $2,826,213. Clinical equipment $438,447. Computer equipment $131,086. Furniture and fittings $122,749. Motor vehicles $21,194. Total $6,417,166.
- bar chart: Jan-Jun 2027 charge by site, bars labelled CHA $447,757, CES $177,711, RAY $174,302, MAI $152,100. Title: 'Jan-Jun 2027 depreciation by site: total $951,870'. The rounded bars add to the rounded total.
