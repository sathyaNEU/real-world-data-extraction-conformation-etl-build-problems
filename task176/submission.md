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
5. Child-days (ccap_payment_lines_2026.csv): kept SFCC and LFCC lines of remittances not voided, expanded each line to its Monday to Friday days in 2026, and counted each child and day once.
6. Money (ccap_payment_lines_2026.csv): kept SFCC and LFCC remittances paid in the 2026 runs and not voided, took each remittance once as its number, run date and county office, and summed the amounts by the quarter of the run date. Every child line repeats the remittance's amount; one number recurs in other county offices in the same run with other amounts; and one remittance can carry several homes' children, so the amount on a home's lines can exceed what its own lines earn at the section 5 rates.
7. Allerton should plan for about 450 homes closing during 2027.

## 4. Deliverable Answers

### fcc_closures_2027.xlsx

1. Homes licensed on 31 December 2026 that will close during 2027, to the nearest 50: 450.
2. Child-days of subsidised care in family child care homes in Allerton, a child counted once on a day: first half of 2026 125,938, second half 137,949.
3. Money the subsidy paid to family child care homes, by region and quarter of the 2026 payment run, nearest dollar, first to fourth quarter:
   - Region 1 North: USD 261,758, 299,956, 308,387, 323,302
   - Region 2 Capital: USD 975,519, 1,059,175, 1,135,102, 1,137,021
   - Region 3 Valley: USD 337,012, 353,636, 391,204, 421,264
   - Region 4 South: USD 387,659, 418,645, 450,405, 455,636
   - Region 5 Lakeshore: USD 365,521, 362,977, 400,530, 418,584
