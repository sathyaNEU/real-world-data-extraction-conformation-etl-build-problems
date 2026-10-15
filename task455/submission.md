## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**The trustees should release phase two of the Overdose Reduction Initiative: Wendmoor County residents' opioid overdose deaths in 2026 were 24.9 per cent below their 2021 to 2023 average.**

The 2026 outcome is 190 deaths against a baseline of 253 a year, past the 20 per cent Schedule B5 requires. Not the certificates as filed, which fell 6.2 per cent because the coroner lists fentanyl that played no part in stimulant deaths. Not the two-by-two correction with one false-listing rate over all non-opioid deaths, which files 12.1 per cent because that rate moves with the stimulant deaths' growing share.

## 2. Critical Components

1. The 2026 outcome is **190** residents' deaths an opioid caused or contributed to.
2. The 2021 to 2023 baseline is **253** a year (**248**, **262** and **249**).
3. 2026 is **24.9 per cent** below the baseline.
4. The certificates name an opioid on **0.875** of the deaths an opioid caused and on **0.5** of the stimulant deaths, none of the other drug deaths.

## 3. Step-by-Step Solution

1. Read wendmoor_death_records_2019_2026.csv as it stands at the extract (each state file number's latest version, voids dropped) for residents of Wendmoor County wherever they died whose underlying cause is a drug poisoning (Schedule B1 in ori_grant_agreement_2024.pdf): 245, 264, 262 and 241 deaths certified with an opioid in 2021, 2022, 2023 and 2026.
2. Joined ome_drug_death_review_2025.xlsx to the 2025 deaths by state file number and classed each by the drugs it found contributing: 216 opioid, 128 stimulant without an opioid, 64 other.
3. Measured each class's certificate categories: an opioid named on 189 of 216 opioid deaths, on 64 of 128 stimulant deaths (fentanyl present, not contributing) and on none of the 64 other drug deaths.
4. Solved each year's opioid, stimulant and other deaths from its three certificate categories (an opioid named; a stimulant without an opioid; neither) through those rates (Schedule B3): 248, 262, 249 and 190 opioid deaths.
5. Averaged 2021 to 2023 (Schedule B2) and compared 2026: 190 against 253, 24.9 per cent below.
6. Applied Schedule B5: at least 20 per cent below the baseline, so phase two is released.
7. Rebuilt each year's file at its close from the versions in wendmoor_death_records_2019_2026.csv, the out-of-state versions on the day interstate_exchange_receipts_2019_2027.csv shows them received (close dates from vital_records_data_year_status.csv), and split each year's deaths on the file now into those already among them at the close and those that joined since, a death received through the exchange counted once by its sending state's certificate number.
8. Grouped ems_patient_care_reports_2021_2026.csv into patient encounters (each report that does not hand the patient on, with the reports that hand the patient to its unit) and counted those with naloxone or an opioid poisoning code (sixth character 1 to 4) on any report, a Wendmoor home county and no death (Schedule B6).

## 4. Deliverable Answers

### ori_phase_one_outcome_certification_2026.pdf

1. Phase two is released under Schedule B5.
2. 2026 outcome 190; 2021 to 2023 baseline 253; 24.9 per cent below.
3. Bridge, deaths certified with an opioid, plus opioid deaths certified without one, less deaths certified with an opioid that no opioid caused, equals the outcome:
   - 2021: 245, plus 31, less 28, equals 248
   - 2022: 264, plus 33, less 35, equals 262
   - 2023: 262, plus 31, less 44, equals 249
   - 2026: 241, plus 24, less 75, equals 190

### ori_outcome_measures_2019_2026.xlsx

1. Residents' drug overdose deaths on the state's file now, by whether they were among them the day it closed:
   - 2019: 332 among them at the close, 8 joined since
   - 2020: 376 among them at the close, 3 joined since
   - 2021: 383 among them at the close, 4 joined since
   - 2022: 408 among them at the close, 3 joined since
   - 2023: 403 among them at the close, 10 joined since
   - 2024: 404 among them at the close, 5 joined since
2. Non-fatal opioid overdoses of residents treated by EMS, by quarter:
   - 2021 Q1: 360
   - 2021 Q2: 372
   - 2021 Q3: 391
   - 2021 Q4: 376
   - 2022 Q1: 364
   - 2022 Q2: 370
   - 2022 Q3: 369
   - 2022 Q4: 359
   - 2023 Q1: 339
   - 2023 Q2: 360
   - 2023 Q3: 368
   - 2023 Q4: 336
   - 2024 Q1: 334
   - 2024 Q2: 339
   - 2024 Q3: 345
   - 2024 Q4: 318
   - 2025 Q1: 326
   - 2025 Q2: 334
   - 2025 Q3: 332
   - 2025 Q4: 319
   - 2026 Q1: 294
   - 2026 Q2: 310
   - 2026 Q3: 322
   - 2026 Q4: 296
