## Tags

**Domain:** Survey Research & Official Statistics (official time-series production: a city's police-recorded aggravated assault series restated across the department's move from summary (Return A) to incident-based (NIBRS) reporting, from the three months in which every victim carries both classifications, and conformed with the NIBRS extract, the Domestic Violence Unit's case log, the shooting log and the Medical Examiner's list into the scorecard's crime chapter).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**On the NIBRS basis Ellsmere's aggravated assaults rose 1 per cent from 2024 to 2025: 5,254 victims in 2025 against about 5,200 in 2024 restated.**
The rise in the published figures is mostly the change in counting: 2024 as NIBRS would have counted it is about 5,200, well above the total Return A published, because NIBRS counts the assault victims the hierarchy rule hid, counts as aggravated the simple assaults with a weapon or force or serious injury, most of them domestic, and counts as simple the hands-and-feet assaults Return A scored aggravated for minor injuries. Restated at the October to December 2024 rate for each Return A line, 2024 would be about 5,400 and 2025 a fall of 3 per cent from it, because that rate carries October to December's share of domestic victims among other assaults (35.8 per cent, against 29.1 per cent in January to September) into the rest of the year.

## 2. Critical Components

1. 2024 as published from Return A (lines 4a to 4d, actual offenses): **4,829**; 2025 counted from the department's extract: **5,254**.
2. October to December 2024, the share of each Return A line's victims NIBRS counted aggravated: other assaults (4e) **21.2 per cent** for domestic victims and **0.31 per cent** for the rest; hands and feet (4d) **32.4 per cent**; firearm, knife and other weapon (4a to 4c) **100.0 per cent**.
3. Domestic victims' share of other assaults (4e): **35.8 per cent** in October to December 2024, **29.1 per cent** in January to September (4,756 of 16,321).
4. From the published 2024 total to the restated one, to the unit: 4,829, plus **202** victims the hierarchy rule left unscored, plus **1,400** victims of other assaults NIBRS counts aggravated, less **1,238** victims of aggravated assault NIBRS counts simple: **5,193**, about **5,200** to the nearest hundred.

## 3. Step-by-Step Solution

1. Counted the 13A rows of epd_nibrs_offense_extract_2024-10_to_2026-09.csv by the month reported in Ellsmere local time (report_datetime_utc is UTC): 5,254 in 2025, and October to December 2024 the same way.
2. Took each month's actual offenses (column 4) from return_a_2024.xlsx; lines 4a to 4d sum to 4,829 for 2024.
3. In October to December 2024 (ucr_summary_class filled) took for lines 4a to 4d the share of each line's victims coded 13A, for robbery and homicide the 13A victims marked NS per Return A robbery incident and per homicide victim, and for line 4e the share coded 13A separately for victims whose relationship_1 is a family or intimate partner code and for the rest.
4. For each month of January to September 2024 counted the domestic victims of line 4e from dvu_case_log_2021_2026.csv (ucr_line 4E, report_date in the month, case_status not UNFOUNDED) and took the rest of line 4e as the month's other victims.
5. Restated January to September at those rates, line by line and month by month, and added October to December as counted: 5,193, about 5,200 to the nearest hundred; to 2025, +1 per cent.
6. Shootings: kept the rows of gvr_shooting_log_2023_2026.csv struck in an ASSAULT with outcome WOUNDED; left out every block the log marks N in any row (the North Ellsmere Township blocks, which it marks Y before October 2024), and dropped the people the Medical Examiner's list shows died of the wound (same date of injury, block, age and sex, place in Ellsmere); counted each person once (report number, time, age and sex) by the quarter shot, and a shooting as the people struck at one block and minute.
7. Wrote ellsmere_aggravated_assault.xlsx.

## 4. Deliverable Answers

### ellsmere_aggravated_assault.xlsx

1. 2024 restated on the NIBRS basis, to the nearest hundred: 5,200; 2025: 5,254; change: +1 per cent.
2. Non-fatal shooting victims and the shootings they were hurt in, by quarter: 2023 Q1 110 victims in 105 shootings; 2023 Q2 160 victims in 148 shootings; 2023 Q3 153 victims in 140 shootings; 2023 Q4 129 victims in 120 shootings; 2024 Q1 121 victims in 110 shootings; 2024 Q2 164 victims in 151 shootings; 2024 Q3 169 victims in 153 shootings; 2024 Q4 100 victims in 96 shootings; 2025 Q1 109 victims in 103 shootings; 2025 Q2 157 victims in 144 shootings; 2025 Q3 159 victims in 150 shootings; 2025 Q4 126 victims in 115 shootings.
