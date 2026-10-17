## Tags

**Domain:** General Statistics & Data Science (data integration: two state surveys that each measured one of a programme's two eligibility traits, fused through the county and income band they share with a utility's screening pilot that asked both).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Staff 38 Home Energy Medical Assistance caseworkers for 2027: Northern 2, Lakeshore 3, River Valley 4, High Plains 4, Central 4, Southern Hills 3, Southwest 7, North Metro 6 and South Metro 5.**
Each division's 2025 eligible households fuse the energy survey's high-burden share and the health survey's equipment share in each income band with the screening pilot's odds ratio between the two traits inside the band (3.49 under $25,000, 3.47 from $25,000 to $49,999). Not the 26 caseworkers that multiplying the two surveys' shares staffs: inside each band the pilot's high-burden homes report the equipment about three times as often as the rest (10.7 against 3.3 per cent under $25,000, 11.7 against 3.7 per cent from $25,000 to $49,999), so treating the traits as independent undercounts every division.

## 2. Critical Components

1. In the pilot's complete screens the equipment is reported in **10.7** per cent of high-burden homes against **3.3** per cent of the rest under $25,000, and in **11.7** against **3.7** per cent from $25,000 to $49,999.
2. The pilot's odds ratio between high energy burden and the equipment inside each band: **3.49** under $25,000 and **3.47** from $25,000 to $49,999.
3. Caseworkers in total: **38**.

## 3. Step-by-Step Solution

1. Took each division's counties from callowmere_service_divisions.csv and each county's households in the two eligible bands from household_estimates_county_income_2025.xlsx (county rows, not the region and state rows).
2. From heas_2025_household_puf.csv, computed each household's annual home energy cost (ELEC_AMT times 12 where ELEC_BASIS is M, plus GAS_AMT and OTHER_AMT) and its band from HHINC, and took each division and band's WT_FINAL-weighted share with costs above 6 per cent of income.
3. From shs_2025_household_file.csv, nested INCCAT 1 to 3 and 4 to 5 into the two bands, matched CNTYFIPS to the register's three-digit codes, and took each division and band's HH_WT-weighted share with MEDEQUIP 1 among answers 1 and 2.
4. From hema_screening_pilot_2025.csv, kept each address's latest complete screen, computed its burden from HH_INCOME, ELEC_12M and OTHER_FUELS_12M, and tabulated burden against MED_EQUIPMENT (Yes or No) in each band: odds ratios 3.49 and 3.47.
5. Raked each band's pilot table to each division and band's two survey shares and multiplied the share with both traits by the households; a Mantel-Haenszel odds ratio, each pilot division's own odds ratio or the pilot's equipment rate ratio puts every cell on the same hundred. Multiplying the two shares, as if independent inside the cell, was not used: the pilot rejects independence in both bands, and it staffs 26.
6. Staffed each division at one caseworker for every 400 eligible households or part of that number, from the unrounded counts: 38 in all.
7. Joined accounts into households through PRIOR_ACCOUNT_NO in medical_baseline_enrolment_2026.csv and counted the households with a spell open on October 31, 2026 (START_DATE on or before it, END_DATE blank or on or after it), each in its premise county's division.
8. Counted the households (accounts joined the same way) with a Completed order in battery_placement_work_orders_2026.csv whose COMPLETED_UTC falls from January 1 to October 31, 2026 on Central Time, each in its premise county's division.

## 4. Deliverable Answers

### hema_caseworkers_2027.xlsx

1. Each division's eligible households in 2025 (nearest hundred) and caseworkers for 2027:
   - Northern: 700 eligible households, 2 caseworkers
   - Lakeshore: 900 eligible households, 3 caseworkers
   - River Valley: 1,400 eligible households, 4 caseworkers
   - High Plains: 1,300 eligible households, 4 caseworkers
   - Central: 1,500 eligible households, 4 caseworkers
   - Southern Hills: 900 eligible households, 3 caseworkers
   - Southwest: 2,500 eligible households, 7 caseworkers
   - North Metro: 2,300 eligible households, 6 caseworkers
   - South Metro: 1,800 eligible households, 5 caseworkers
   - Total caseworkers: 38
2. Each division's households on the medical baseline rate at the end of October 2026:
   - Northern: 933
   - Lakeshore: 821
   - River Valley: 1,506
   - High Plains: 1,359
   - Central: 1,313
   - Southern Hills: 1,181
   - Southwest: 3,500
   - North Metro: 3,320
   - South Metro: 3,391
3. Each division's households given a backup battery from January to October 2026:
   - Northern: 202
   - Lakeshore: 161
   - River Valley: 283
   - High Plains: 255
   - Central: 237
   - Southern Hills: 219
   - Southwest: 603
   - North Metro: 641
   - South Metro: 635
4. A horizontal bar chart of eligible households by division, each bar labelled with its caseworkers, on the Caseworkers 2027 sheet.

### hema_eligible_households_2025.csv

1. Eligible households in 2025 by division and income band (nearest hundred):
   - Northern, under $25,000: 500
   - Northern, $25,000 to $49,999: 200
   - Lakeshore, under $25,000: 600
   - Lakeshore, $25,000 to $49,999: 300
   - River Valley, under $25,000: 900
   - River Valley, $25,000 to $49,999: 500
   - High Plains, under $25,000: 1,000
   - High Plains, $25,000 to $49,999: 300
   - Central, under $25,000: 1,000
   - Central, $25,000 to $49,999: 500
   - Southern Hills, under $25,000: 600
   - Southern Hills, $25,000 to $49,999: 300
   - Southwest, under $25,000: 1,700
   - Southwest, $25,000 to $49,999: 800
   - North Metro, under $25,000: 1,300
   - North Metro, $25,000 to $49,999: 1,000
   - South Metro, under $25,000: 1,200
   - South Metro, $25,000 to $49,999: 600
