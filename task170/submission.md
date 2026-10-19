## Tags

**Domain:** Healthcare Delivery & Health Economics (utilization, access and demand forecasting).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Line 2 of the C7 order should carry 11 pallets of TLD 30s (88,704 bottles) for the children in the paediatric register.** A child on a paediatric first-line regimen moves onto TLD at the first clinic weighing that reads 30 kg or more, and a weighing scatters more than a kilogram around the child's growth line, so most of those readings come months before the line itself reaches 30 kg; forecast from each child's scheduled weighings at the child's own dispensing interval, the children's need to June 2027 with six months of June's falls in the eleventh pallet. Not 10 pallets, which is what moving each child when its fitted line reaches 30 kg gives: on every window the register has closed, under the band then in force, that route fell short by 52 to 73 per cent. Not the register's own switch history either, its switch rates by recorded weight or its recent count of switches, because those switches came under the 35 kg band and the monthly visits that the 2026 guidelines changed in March.

## 2. Critical Components

1. Line 1 is **342 pallets (2,757,888 bottles)**: patients aged 15 and over at the count or starting treatment after it consume **3,138,377** bottles from September 2026 to June 2027 with a maximum stock of **1,903,818**, less **1,159,770** bottles of usable stock and **1,124,544** bottles of confirmed shipments.
2. **4,527** children under 15 were on TLD at the count and **7,151** were on a paediatric first-line regimen.

## 3. Step-by-Step Solution

1. Summed the national row of art_patient_projection_2026-09_2027-06.xlsx from September 2026 to June 2027 (SOP QP-04, 4.1 and 4.2) with six months of June 2027 as the maximum stock (3.2), and took the usable batches at both warehouses and the lots with a confirmed delivery date from cms_stock_status_2026-08-31.xlsx (2.1, 3.1 and 3.3): line 1 is 2,757,881 bottles before rounding, 342 pallets (4.3 and 4.4).
2. Read the register's two layouts as one history: legacy ART numbers linked to the national identifier through art_number_crosswalk_2024-06.csv, legacy regimen lines coded with national_regimen_codes_2026.csv, the June 2024 visits kept once and EPR rows re-sent after a failed sync dropped.
3. Took the children born after 31 August 2011 with no outcome entered in paed_register_patients_2026-09-02.csv: 4,527 on TLD and 7,151 on a paediatric first-line regimen.
4. Fitted a straight line in kilograms to each first-line child's weighings since January 2023 and scheduled its visits to June 2027 from its next appointment at its months-dispensed interval; the residual standard deviation around the lines, two parameters fitted per child, is 1.29 kg.
5. Took each scheduled visit as weighed at the register's share of clinical visits over the last 12 months, the reading scattered around the child's line at that spread, and moved the child onto TLD at its first reading of 30.0 kg or more (Annex 7, 7.1 and 7.2), or at the next weighed visit for the 9.5 per cent of the 2,919 such readings since 1 March 2026 that the register shows held back; every child was kept at the register's exit rates of the last 12 months for children under 12 and 12 and over (SOP 4.1).
6. Stood the same forecast at three month ends the register has closed, under the band then in force (35 kg), followed for twelve months from the first two and six from the third (2024-08-31, 2025-02-28, 2025-08-31): it came within 13 per cent of the bottle-months the register shows each time, while moving each child when its line reaches the band fell short by 52 to 73 per cent.
7. Counted one bottle for each child on TLD at each month's end with six months of June 2027 (SOP 4.1, 4.3), 87,984 bottles on this construction, and rounded to the nearest pallet of 8,064 bottles (4.4): 11 pallets.

## 4. Deliverable Answers

### c7_tld_order.xlsx

1. Line 2 of the C7 order is 11 pallets of TLD 30s (88,704 bottles).
2. Line 1 is 342 pallets (2,757,888 bottles): consumption 3,138,377 bottles and maximum stock 1,903,818 bottles for patients aged 15 and over at the count or starting treatment after it, netting 1,159,770 bottles of usable stock and 1,124,544 bottles of confirmed shipments.
3. 4,527 children under 15 were on TLD at the count and 7,151 on a paediatric first-line regimen.
4. Bottles delivered by CMS to each region's ART facilities, dated by when they were signed for, and bottles those facilities reported dispensing, whole bottles:
   - Capital: delivered 332,616 in C4 and 313,068 in C5; dispensed 328,751 in C4 and 329,253 in C5
   - Central: delivered 386,916 in C4 and 373,512 in C5; dispensed 382,391 in C4 and 388,240 in C5
   - Northern: delivered 193,728 in C4 and 175,008 in C5; dispensed 185,338 in C4 and 186,134 in C5
   - Eastern: delivered 368,856 in C4 and 333,012 in C5; dispensed 351,415 in C4 and 352,878 in C5
   - Southern: delivered 306,216 in C4 and 299,400 in C5; dispensed 313,714 in C4 and 316,861 in C5
   - Western: delivered 301,788 in C4 and 260,400 in C5; dispensed 282,859 in C4 and 283,634 in C5

### c4_c5_tld_flows.png

1. Two panels, C4 and C5: for each region a bar of the bottles CMS delivered and a bar of the bottles its facilities reported dispensing, each labelled with its figure in the table above.
