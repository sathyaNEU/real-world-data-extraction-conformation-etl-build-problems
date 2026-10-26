## Tags

**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (an island statistics office's workplace retail employment for 31 designated town centres in March 2022 and March 2026, conformed from the tax authority's PAYE returns in two layouts, the 2017 and 2023 rating lists, six district councils' business rates accounts in six layouts and the companies register).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**15 of Torvasay's 31 designated town centres meet the 2027 Town Centre Renewal Fund's test: Dorrstead, Ingmouth, Fenmoss, Kellgarth, Quengate, Ravthwaite, Molwold, Ravbeck, Molscar, Vaskhope, Tormoss, Vaskrigg, Quenstead, Ravwold and Tavscar.**
Once each multi-site employer's PAYE staff are placed at its premises by floor area times the staff per square metre its premises' description holds among single-site employers, the smallest fall among them between March 2022 and March 2026 is 9.9 per cent and the largest among the other centres 6.4 per cent. Not the 19 centres a share by floor area names (adding Rookgate City Centre, Glenskarn, Neshdale, Skelrigg and Halmoss and dropping Ravbeck): the chains' new retail park units and warehouses hold far fewer staff per square metre than their shops. Not the scheme postcodes, which put the chains' staff at their head offices and agents.

## 2. Critical Components

1. Retail employers in the PAYE returns: **3,545** in March 2022 and **3,319** in March 2026, of which **45** in each March occupied more than one premises, employing **10,279** and **10,990**.
2. Workplace retail employment in the 31 centres together: about **27,000** in March 2022 and **25,000** in March 2026, to the nearest thousand.
3. Centres whose workplace retail employment fell by 8 per cent or more: **15**.

## 3. Step-by-Step Solution

1. Conformed paye_returns_m12_2021-22.csv (layout 3) and paye_returns_m12_2025-26.csv (layout 4) into one table of schemes, kept SIC 2007 division 47 and added up each company's schemes: 3,545 retail employers in March 2022 and 3,319 in March 2026.
2. Resolved each sheet of business_rates_accounts_2017-2026.xlsx to UARNs through the two rating list extracts and matched each account liable on 31 March to its employer by company number, else by registered or previous name in companies_register_extract_20260501.csv, else by initials and surname; a letting company held by a retail employer's parent holds that employer's premises.
3. Took each premises' description and floor area from the list entry in force on that 31 March (rating_list_2017_extract_20220404.csv for 2022, rating_list_2023_extract_20260413.csv for 2026): 45 retail employers occupied more than one premises in each March, employing 10,279 and 10,990.
4. Measured each description's staff per square metre as the single-site retail employers' total employees over their total floor area, March by March.
5. Placed each multi-site employer's employees at its premises in proportion to floor area times its description's staff per square metre, and summed the employees at premises whose list postcode is in each centre's rows of town_centre_schedule_2026.csv, terminated codes included: about 27,000 in March 2022 and 25,000 in March 2026.
6. Applied the prospectus's 3.3 to the unrounded figures: 15 centres fell by 8 per cent or more.
7. Counted, in each district's centres, the shop premises in force on each 31 March whose account that day was an owner's, one on empty property relief or in the name of a company the register classes 68209 (letting its own real estate) or 41100 (developing building projects), a premises with no account being in occupation as the accounts' contents note says, and dated each empty spell from the first of the consecutive owners' accounts on its UARN: 321 empty at 31 March 2022 (193 of them for twelve months or more) and 429 at 31 March 2026 (305).
8. The 2027 fund's eligible centres are the 15 that fell by 8 per cent or more: Dorrstead, Ingmouth, Fenmoss, Kellgarth, Quengate, Ravthwaite, Molwold, Ravbeck, Molscar, Vaskhope, Tormoss, Vaskrigg, Quenstead, Ravwold and Tavscar.

## 4. Deliverable Answers

### town_centre_fund_2027_eligibility.xlsx

1. Workplace retail employment by centre, nearest 50, and its change, whole per cent (sheet Eligibility schedule, in the schedule's order):
   - TC01 Rookgate City Centre: 2,550 in March 2022, 2,400 in March 2026, -6 per cent, does not meet the test
   - TC02 Dorrstead: 950 in March 2022, 850 in March 2026, -13 per cent, meets the test
   - TC03 Glenskarn: 1,650 in March 2022, 1,550 in March 2026, -6 per cent, does not meet the test
   - TC04 Ingmouth: 1,200 in March 2022, 1,100 in March 2026, -10 per cent, meets the test
   - TC05 Neshdale: 1,350 in March 2022, 1,250 in March 2026, -6 per cent, does not meet the test
   - TC06 Skelrigg: 1,850 in March 2022, 1,750 in March 2026, -6 per cent, does not meet the test
   - TC07 Bromgate: 850 in March 2022, 950 in March 2026, +10 per cent, does not meet the test
   - TC08 Fenmoss: 800 in March 2022, 700 in March 2026, -10 per cent, meets the test
   - TC09 Halmoss: 950 in March 2022, 900 in March 2026, -5 per cent, does not meet the test
   - TC10 Kellgarth: 1,500 in March 2022, 1,250 in March 2026, -17 per cent, meets the test
   - TC11 Quengate: 950 in March 2022, 850 in March 2026, -11 per cent, meets the test
   - TC12 Ravthwaite: 900 in March 2022, 750 in March 2026, -18 per cent, meets the test
   - TC13 Lundgate: 400 in March 2022, 450 in March 2026, +15 per cent, does not meet the test
   - TC14 Molwold: 650 in March 2022, 550 in March 2026, -18 per cent, meets the test
   - TC15 Quenmouth: 750 in March 2022, 800 in March 2026, +5 per cent, does not meet the test
   - TC16 Ravbeck: 800 in March 2022, 700 in March 2026, -10 per cent, meets the test
   - TC17 Kellholm: 800 in March 2022, 800 in March 2026, +3 per cent, does not meet the test
   - TC18 Tavmoss: 850 in March 2022, 900 in March 2026, +8 per cent, does not meet the test
   - TC19 Bromwold: 900 in March 2022, 900 in March 2026, +3 per cent, does not meet the test
   - TC20 Molscar: 850 in March 2022, 700 in March 2026, -15 per cent, meets the test
   - TC21 Lundstead: 500 in March 2022, 500 in March 2026, +8 per cent, does not meet the test
   - TC22 Orrstead: 350 in March 2022, 350 in March 2026, -3 per cent, does not meet the test
   - TC23 Vaskhope: 600 in March 2022, 450 in March 2026, -21 per cent, meets the test
   - TC24 Skelgate: 600 in March 2022, 650 in March 2026, +8 per cent, does not meet the test
   - TC25 Tormoss: 650 in March 2022, 550 in March 2026, -14 per cent, meets the test
   - TC26 Orrwold: 450 in March 2022, 500 in March 2026, +11 per cent, does not meet the test
   - TC27 Vaskrigg: 400 in March 2022, 350 in March 2026, -13 per cent, meets the test
   - TC28 Quenstead: 400 in March 2022, 350 in March 2026, -14 per cent, meets the test
   - TC29 Vaskstow: 550 in March 2022, 600 in March 2026, +6 per cent, does not meet the test
   - TC30 Ravwold: 650 in March 2022, 550 in March 2026, -14 per cent, meets the test
   - TC31 Tavscar: 450 in March 2022, 350 in March 2026, -23 per cent, meets the test
2. Shop premises in each district's designated centres empty at each 31 March, and of those the ones empty for twelve months or more (sheet Vacancy annex):
   - Rookgate: 100 at 31 March 2022, 52 of them for twelve months or more; 153 at 31 March 2026, 114 of them for twelve months or more
   - Dorrstead: 38 at 31 March 2022, 25 of them for twelve months or more; 51 at 31 March 2026, 29 of them for twelve months or more
   - Glenskarn: 55 at 31 March 2022, 34 of them for twelve months or more; 56 at 31 March 2026, 40 of them for twelve months or more
   - Ingmouth: 46 at 31 March 2022, 29 of them for twelve months or more; 56 at 31 March 2026, 41 of them for twelve months or more
   - Neshdale: 48 at 31 March 2022, 31 of them for twelve months or more; 65 at 31 March 2026, 48 of them for twelve months or more
   - Skelrigg: 34 at 31 March 2022, 22 of them for twelve months or more; 48 at 31 March 2026, 33 of them for twelve months or more

### town_centre_retail_employment_2022_2026.png

1. Horizontal bar chart of every centre's change from March 2022 to March 2026, sorted, with the 8 per cent line labelled, the 15 qualifying centres in blue and each bar labelled with its change; the title states that 15 of the 31 centres lost 8 per cent or more.
