## Tags

**Domain:** Sociology & Demography (event history and life course analysis).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**About 450 of the 3,081 family child care homes licensed in Allerton on 31 December 2026 will close during 2027, to the nearest 50.**
427 of those homes reach, in 2027, the summer before their provider's youngest own child starts kindergarten, the summer in which 44 per cent of the record's homes in that position closed. Not 300, the forecast from closure rates by years licensed, which puts the 2023 start-up grant round's homes, now in their fourth year, at the closure rate of homes that far into their licence, when most of their providers' youngest children were babies in 2023 and reach kindergarten together in September 2027.

## 2. Critical Components

1. Homes licensed on 31 December 2026: **3,081**.
2. Of those, homes whose provider's youngest own child living in the home starts kindergarten in September 2027 (turns five on or before 1 September 2027, after 1 September 2026): **427**.
3. Homes in the record open on 1 June of the summer before their youngest own child's kindergarten year, 2016 to 2026: **905**, of which **44 per cent** closed by 31 August.

## 3. Step-by-Step Solution

1. Mapped the worksheets filed before 1 July 2019 to current licence numbers through licence_number_crosswalk_2019.csv, read both relationship code sets and date formats, and kept each home's own children living in the home (relationship C or OWN CHILD, lives_in_home Y), one per initials and birth date.
2. Built home-months from January 2016 to December 2026 from fcc_licence_extract_20261231.csv (each home from the month after first issue or January 2016, to its closure month or December 2026), with the home's year of tenure, the provider's age of 63 or more and 68 or more, the June to August months, and whether the month falls in June to August of the year the youngest own child born by then starts kindergarten (the school-age rule in ccap_provider_payment_policy_2026.pdf, section 6).
3. Fitted a monthly Poisson model of closure on those terms: the kindergarten summer, not the years licensed, carries the closures of parent-run homes (401 of 905 such homes closed that summer).
4. Applied the model month by month through 2027 to the 3,081 homes licensed on 31 December 2026, 427 of them in their youngest's kindergarten summer, and summed each home's chance of closing: 450 to the nearest 50.
5. Child-days (ccap_payment_lines_2026.csv): kept SFCC and LFCC lines of remittances not voided, expanded each line to its Monday to Friday days in 2026, and counted each child and day once, since a child who moved home is paid at the home left through its notice days and a child in split care is paid at two homes on the same days.
6. Money (ccap_payment_lines_2026.csv): kept SFCC and LFCC remittances paid in the 2026 runs and not voided, took each remittance once as its number, run date and county office (each county office numbers its remittances afresh in every run, and every child line repeats the remittance's amount), and summed the amounts by the quarter of the run date.
7. Allerton should plan for about 450 homes closing during 2027.

## 4. Deliverable Answers

### fcc_closures_2027.xlsx

1. Homes licensed on 31 December 2026 that will close during 2027, to the nearest 50: 450.
2. Child-days of subsidised care in family child care homes, by region, first half and second half of 2026:
   - Region 1 North: 14,654 and 16,066
   - Region 2 Capital: 53,667 and 56,957
   - Region 3 Valley: 17,906 and 20,791
   - Region 4 South: 21,072 and 23,008
   - Region 5 Lakeshore: 18,639 and 21,127
3. Money the subsidy paid to family child care homes, by region and quarter of the 2026 payment run, nearest dollar, first to fourth quarter:
   - Region 1 North: USD 261,758, 299,144, 308,776, 320,951
   - Region 2 Capital: USD 976,233, 1,060,730, 1,130,314, 1,140,841
   - Region 3 Valley: USD 337,784, 354,141, 389,809, 418,844
   - Region 4 South: USD 386,069, 418,205, 453,653, 455,022
   - Region 5 Lakeshore: USD 364,938, 364,407, 394,196, 423,531
