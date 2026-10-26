## Tags

**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (an island statistics unit's provisional long-term immigration by employment sector for the year to 30 June 2026, conformed from its Population Register's current extract and legacy archive, the crosswalk between their registration numbers and two sector classifications, against the Population Policy's sector allowances).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**The Council should cut the 2027 work permit quotas of hospitality and tourism, financial and professional services and digital and e-gaming, the three sectors whose provisional long-term immigration for 2025-26 exceeds its allowance.**
Construction, health and social care and retail and distribution stay under their allowances once each stay still open at the cut is completed on the 2024-25 arrivals of the same sector, migration history and months on the island: the completion that would have predicted the 2024-25 arrivals best a year earlier (mean squared difference 0.155, against 0.172 by sector and months alone). Not those three as well, which the sector-by-months completion gives: returning workers, whose previous stay ended within the year before they arrived, made 31, 26 and 33 per cent of their 2025-26 arrivals against 13, 12 and 18 per cent a year earlier, and in 2024-25 reached twelve months 1, 3 and 0 per cent of the time against 40, 51 and 34 per cent for first arrivals.

## 2. Critical Components

1. 2025-26 arrivals still on the island at the 31 August 2026 cut short of their first anniversary: construction **523**, health and social care **825** and retail and distribution **511**, of which **180**, **239** and **184** are returns (a previous stay under the same registration number ended in the 365 days before the arrival).
2. Of the 2024-25 arrivals in those sectors, returning arrivals reached twelve months **1**, **3** and **0** per cent of the time and first arrivals **40**, **51** and **34** per cent.
3. The methods note's test, on the 2,763 arrivals of 2024-25 still open at 31 August 2025: the completion by sector, history and months scores **0.155**, by sector and months **0.172**, the sector's share of all arrivals **0.190**.

## 3. Step-by-Step Solution

1. Took the ARRIVAL records with an arrival date from 1 July 2025 to 30 June 2026 in population_register_extract_20260930.csv, each sector from its 2014 activity code or 2026 sector code in sector_classification_2026.json: 4,281 arrivals.
2. At the 31 August 2026 cut counted a stay as long-term when its first anniversary had passed with no leaving date before it, and as not when its leaving date fell before its anniversary (the methods note's definitions); the rest are open: construction 523, health and social care 825 and retail and distribution 511.
3. Gave each arrival its migration history from the other stays under the same reg_no: a return when one of them has a leaving date in the 365 days before the arrival date.
4. Scored the candidate completions on the methods note's test, each estimated from the 2023-24 arrivals and given to the 2024-25 arrivals open at 31 August 2025 (leaving notices received by 30 September 2025): by sector, history and whole calendar months on the island 0.155, by sector and months 0.172.
5. Counted each open 2025-26 stay at the share of the 2024-25 arrivals of its sector and history still on the island after its whole months at 31 August 2026 whose stays reached their first anniversary (returns 1, 3 and 0 per cent and first arrivals 40, 51 and 34 per cent overall in construction, health and social care and retail and distribution), and added the stays counted long-term.
6. Compared each unrounded figure with its 2025-26 allowance in Table 1 of population_policy_2024_2028_sector_allowances.pdf: hospitality and tourism, financial and professional services and digital and e-gaming exceed.
7. For the back series, read the archive's day-first dates, gave each TRANSFERRED record the leaving date and notice date of the TRANSFER record its legacy number's reg_no holds in registration_number_crosswalk_2023.csv, kept the archive's own arrival date and activity, counted once any records identical in arrival date, sex, birth year, nationality and activity whose stays ended on the same date on notices received the same day (one stay registered at two parish offices), and added the current extract's ARRIVAL records with arrival dates in each year: the figures below.
8. The Council cuts the 2027 quotas of hospitality and tourism, financial and professional services and digital and e-gaming.

## 4. Deliverable Answers

### provisional_long_term_immigration_2025_26.xlsx

1. Each sector's provisional long-term immigration for 2025-26 against its allowance:
   - Hospitality and tourism: exceeds
   - Agriculture, fishing and food: does not exceed
   - Construction: does not exceed
   - Financial and professional services: exceeds
   - Health and social care: does not exceed
   - Retail and distribution: does not exceed
   - Digital and e-gaming: exceeds
   - Public and other services: does not exceed
2. Arrivals registered for work by sector, persons, for the years 2018-19 to 2022-23:
   - Hospitality and tourism: 2018-19 868, 2019-20 667, 2020-21 665, 2021-22 777, 2022-23 659
   - Agriculture, fishing and food: 2018-19 203, 2019-20 205, 2020-21 171, 2021-22 161, 2022-23 191
   - Construction: 2018-19 571, 2019-20 427, 2020-21 406, 2021-22 499, 2022-23 518
   - Financial and professional services: 2018-19 535, 2019-20 446, 2020-21 443, 2021-22 467, 2022-23 457
   - Health and social care: 2018-19 932, 2019-20 661, 2020-21 756, 2021-22 822, 2022-23 799
   - Retail and distribution: 2018-19 480, 2019-20 403, 2020-21 419, 2021-22 508, 2022-23 491
   - Digital and e-gaming: 2018-19 322, 2019-20 225, 2020-21 227, 2021-22 283, 2022-23 256
   - Public and other services: 2018-19 377, 2019-20 275, 2020-21 285, 2021-22 320, 2022-23 263
3. Final long-term immigration by sector, persons, for the years 2018-19 to 2022-23:
   - Hospitality and tourism: 2018-19 333, 2019-20 266, 2020-21 219, 2021-22 325, 2022-23 243
   - Agriculture, fishing and food: 2018-19 89, 2019-20 91, 2020-21 70, 2021-22 64, 2022-23 91
   - Construction: 2018-19 250, 2019-20 185, 2020-21 171, 2021-22 235, 2022-23 186
   - Financial and professional services: 2018-19 476, 2019-20 394, 2020-21 382, 2021-22 408, 2022-23 400
   - Health and social care: 2018-19 462, 2019-20 302, 2020-21 394, 2021-22 400, 2022-23 327
   - Retail and distribution: 2018-19 138, 2019-20 125, 2020-21 137, 2021-22 159, 2022-23 145
   - Digital and e-gaming: 2018-19 296, 2019-20 196, 2020-21 199, 2021-22 233, 2022-23 228
   - Public and other services: 2018-19 334, 2019-20 250, 2020-21 255, 2021-22 275, 2022-23 225

### long_term_immigration_by_sector_2025_26.png

1. A bar chart of each sector's provisional long-term immigration for 2025-26 against its 2025-26 allowance, the three sectors over their allowances marked.
