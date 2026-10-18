## Tags

**Domain:** Healthcare Delivery & Health Economics (utilization, access and demand forecasting).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The C7 order should carry 2,690,000 bottles of TLD.** Each child under 15 moves onto TLD at the first scheduled weighing that reads 30 kg or more, and because a weighing scatters more than a kilogram around the child's growth line, that reading comes months before the line itself reaches 30 kg; forecast that way, the children's switches came within a tenth of what the register shows on every window it has closed. Not an order that moves each child when its fitted growth line reaches 30 kg, which waits for the line and fell short by two thirds or more on every closed window. Not the register's switch rates by recorded weight band or its recent switch count carried forward, which carry over what other children did at other points of their growth rather than when these children will be weighed.

## 2. Critical Components

1. Patients aged 15 and over at the count or starting treatment after it consume **3,142,937** bottles from September 2026 to June 2027, and their maximum stock is **1,908,822** bottles.
2. Usable stock at the count is **1,376,018** bottles and confirmed shipments due by 30 June 2027 are **1,072,992** bottles.
3. **3,348** children under 15 were on TLD at the count and **12,232** were on a paediatric first-line regimen.

## 3. Step-by-Step Solution

1. Summed the national row of art_patient_projection_2026-09_2027-06.xlsx from September 2026 to June 2027 (SOP QP-04, 4.1 and 4.2) and took six months of June 2027 as the maximum stock (3.2): 3,142,937 and 1,908,822 bottles.
2. Took the usable batches at both warehouses and the lots with a confirmed delivery date from cms_stock_status_2026-08-31.xlsx (SOP 2.1, 3.1 and 3.3): 1,376,018 and 1,072,992 bottles.
3. Read the register's two layouts as one history: legacy ART numbers linked to the national identifier through art_number_crosswalk_2024-06.csv, legacy regimen lines coded with national_regimen_codes_2025.csv, the June 2024 visits kept once and EPR rows re-sent after a failed sync dropped.
4. Took the children born after 31 August 2011 with no outcome entered in paed_register_patients_2026-09-02.csv: 3,348 on TLD and 12,232 on a paediatric first-line regimen.
5. Fitted a straight line in kilograms to each first-line child's weighings since January 2023 and scheduled its visits to June 2027 from its next appointment at its months-dispensed interval; the residual standard deviation around the lines, two parameters fitted per child, is 1.28 kg.
6. Took each scheduled visit as weighed at the register's share of clinical visits over the last 12 months, the reading scattered around the child's line at that spread, moved the child onto TLD at its first reading of 30.0 kg or more (Annex 7, 7.1 and 7.2), and kept every child at the register's exit rates of the last 12 months for children under 12 and over 12.
7. Stood the same forecast at 31 August 2025 over 12 months and at 31 December 2025 and 28 February 2026 over 6 months: within a tenth of the bottle-months the register shows for those children each time, while moving each child when its line reaches 30 kg fell short by two thirds or more each time.
8. Counted one bottle for each child on TLD at each month's end with six months of June 2027 (SOP 4.1 and 3.2), added the patients aged 15 and over, netted the stock and shipments and rounded to the nearest 5,000: 2,690,000 bottles.

## 4. Deliverable Answers

### c7_tld_order.xlsx

1. The C7 order is 2,690,000 bottles of TLD 30s.
2. For patients aged 15 and over at the count or starting treatment after it, consumption is 3,142,937 bottles and maximum stock 1,908,822 bottles.
3. The order nets 1,376,018 bottles of usable stock and 1,072,992 bottles of confirmed shipments.
4. Bottles delivered by CMS to each region's ART facilities, dated by when they were signed for, and bottles those facilities reported dispensing, whole bottles:
   - Capital: delivered 329,436 in C4 and 317,316 in C5; dispensed 336,471 in C4 and 336,512 in C5
   - Central: delivered 364,920 in C4 and 348,504 in C5; dispensed 362,261 in C4 and 365,990 in C5
   - Northern: delivered 198,312 in C4 and 185,136 in C5; dispensed 193,540 in C4 and 191,023 in C5
   - Eastern: delivered 344,436 in C4 and 333,036 in C5; dispensed 344,519 in C4 and 350,111 in C5
   - Southern: delivered 314,808 in C4 and 303,096 in C5; dispensed 318,155 in C4 and 322,329 in C5
   - Western: delivered 299,148 in C4 and 272,820 in C5; dispensed 287,524 in C4 and 284,111 in C5

### c4_c5_tld_flows.png

1. Two panels, C4 and C5: for each region a bar of the bottles CMS delivered and a bar of the bottles its facilities reported dispensing, each labelled with its figure in the table above.
