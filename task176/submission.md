## Tags

**Domain:** Sociology & Demography (event history and life course analysis).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**About 450 of the 3,051 family child care homes licensed in Allerton on 31 December 2026 will close during 2027, to the nearest 50.**
428 of those homes reach, in 2027, the summer before their provider's youngest own child starts kindergarten, the summer in which 51 per cent of the record's homes in that position closed. Not 300, the forecast from closure rates by years licensed, which puts the 2023 start-up grant round's homes, now in their fourth year, at the closure rate of homes that far into their licence, when most of their providers' youngest children were babies in 2023 and reach kindergarten together in September 2027.

## 2. Critical Components

1. Homes licensed on 31 December 2026: **3,051**.
2. Of those, homes whose provider's youngest own child living in the home starts kindergarten in September 2027 (turns five on or before 1 September 2027, after 1 September 2026): **428**.
3. Homes in the record open on 1 June of the summer before their youngest own child's kindergarten year, 2016 to 2026: **903**, of which **51 per cent** closed by 31 August.

## 3. Step-by-Step Solution

1. Mapped the worksheets filed before 1 July 2019 to current licence numbers through licence_number_crosswalk_2019.csv, read both relationship code sets and date formats, and kept each home's own children living in the home (relationship C or OWN CHILD, lives_in_home Y), one per initials and birth date.
2. Built home-months from January 2016 to December 2026 from fcc_licence_extract_20261231.csv (each home from the month after first issue or January 2016, to its closure month or December 2026), with the home's year of tenure, the provider's age of 63 or more and 68 or more, the June to August months, and whether the month falls in June to August of the year the youngest own child born by then starts kindergarten (the school-age rule in ccap_provider_payment_policy_2026.pdf, section 6).
3. Fitted a monthly Poisson model of closure on those terms: the kindergarten summer, not the years licensed, carries the closures of parent-run homes (459 of 903 such homes closed that summer).
4. Applied it month by month through 2027 to the 3,051 homes licensed on 31 December 2026, 428 of them in their youngest's kindergarten summer, and summed each home's chance of closing; the same terms as logit, with tenure as a line or left out, fitted from 2020 or 2022, read as rates, or as annual rates give 437 to 464, centred on 450 to the nearest 50.
5. Money (ccap_payment_lines_2026.csv): kept SFCC and LFCC remittances paid in the 2026 runs and not voided, took each remittance once as its number, run date and county office, and credited it to the region of the home that gave the care (licence extract county). A remittance carrying homes in more than one region was shared by its lines' pay (the section 5 rate prorated by the line's days over the month's Monday to Friday days), which sums to its amount, each home paid the amounts of its own lines; summed by the half of the run date.
6. Meals (cacfp_home_claims_2026.csv): kept the home sites' claims, took each claim once at its latest filing as its sponsor and claim number (each sponsor numbers its claims in its own sequence, a revision keeps the number, and a home whose tier changed in the month has two claims), and summed breakfasts, lunches, suppers and snacks by the site's region and the half of the claim month.
7. Split care (ccap_payment_lines_2026.csv): a child paid at two homes for the same days is in split care when one home's days for the child lie within the other's; a child who moved has the home left paid through its notice days while the next home starts, at the full rate, which the remittance amounts confirm against the half rate of split care.
8. Allerton should plan for about 450 homes closing during 2027.

## 4. Deliverable Answers

### fcc_closures_2027.xlsx

1. Homes licensed on 31 December 2026 that will close during 2027, to the nearest 50: 450.
2. Money the subsidy paid to family child care homes, by the region of the home and half of the 2026 payment run, nearest dollar, first and second half:
   - Region 1 North: USD 642,814 and 690,799
   - Region 2 Capital: USD 1,858,868 and 1,811,135
   - Region 3 Valley: USD 621,586 and 684,310
   - Region 4 South: USD 874,959 and 925,906
   - Region 5 Lakeshore: USD 698,708 and 798,228
3. Meals and snacks claimed through the food program at family child care homes, by region and half of 2026 by month of service:
   - Region 1 North: 379,629 and 386,596
   - Region 2 Capital: 1,184,702 and 1,182,405
   - Region 3 Valley: 487,331 and 490,405
   - Region 4 South: 543,358 and 556,773
   - Region 5 Lakeshore: 475,902 and 476,875
4. Children whose subsidised care was split between two family child care homes, by region and half of 2026:
   - Region 1 North: 16 and 23
   - Region 2 Capital: 37 and 55
   - Region 3 Valley: 13 and 21
   - Region 4 South: 21 and 31
   - Region 5 Lakeshore: 16 and 26
