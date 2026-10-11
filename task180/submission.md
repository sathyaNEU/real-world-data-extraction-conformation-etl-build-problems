# task180: which Q3 signal the registries support

## Tags

**Domain:** Pharmacology, Pharmacoepidemiology & Safety (safety-signal detection: refining three spontaneous-report signals in a national medicines agency's registry extracts).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Open the formal assessment on corinurad (Uralexa) and acute kidney injury.**

In days 1 to 30 after a new user's first dispensing, admissions with acute kidney injury run at 2.52 times the rate in the same people's days 61 to 180 (95% CI 1.92 to 3.31), and on the same comparison falls with tasorexant sit at 1.01 and acute pancreatitis with velaglutide at 0.98. Not tasorexant and falls, which leads every comparison of its starters with other people only because tasorexant is started by people who were already being admitted for falls before they took it. Not velaglutide and acute pancreatitis, which no comparison supports.

## 2. Critical Components

1. Corinurad and acute kidney injury, days 1 to 30 against the same people's days 61 to 180: rate ratio **2.52** (95% CI 1.92 to 3.31), and 2.36 to 2.62 against any other control period
2. Tasorexant and falls on the same comparison: **1.01** (95% CI 0.84 to 1.22)
3. Velaglutide and acute pancreatitis on the same comparison: **0.98** (95% CI 0.51 to 1.85)

## 3. Step-by-Step Solution

1. Linked `prescription_registry_2018-2026.parquet`, `patient_registry_contacts_2018-2026.parquet`, `patient_registry_diagnoses_2018-2026.parquet` and `civil_registration_extract.csv` on the pseudonymised personal number (SOP-PV-14 3.1).
2. Took new users per SOP-PV-14 5.1 to 5.4: 365 days without the substance under any ATC code it has carried (corinurad M04AX02, then M04AB06 from 2024, per `atc_ddd_index_2026.csv`), resident for those 365 days, returned dispensings not counted: the new-user counts below.
3. Made admissions from contacts linked by transfer (4.2) and applied annex A on action diagnoses: falls an emergency or inpatient admission with an injury action diagnosis (DS00 to DT14) and a fall code (DW00 to DW19), acute kidney injury an inpatient admission with DN17 as action diagnosis, acute pancreatitis one with DK85.
4. Against matched non-users (`matched_comparators.csv`) and against new users of zopiclone, allopurinol and orlistat, tasorexant and falls leads, but in the year before the start tasorexant's new users were already admitted for falls far more often than either comparison group, and corinurad's new users had fewer kidney injury admissions than allopurinol's: the medicines are started by different people, so these comparisons cannot answer SOP-PV-14 1's question.
5. Compared each new user's days 1 to 30 (6.1) with the same person's days 61 to 180, observation ending at death, emigration or 30 June 2026 (7.1), by conditional Poisson regression with each start its own stratum: corinurad 2.52 (1.92 to 3.31), tasorexant 1.01 (0.84 to 1.22), velaglutide 0.98 (0.51 to 1.85).
6. Counted the acute kidney injury admissions in days 1 to 30 among people who started corinurad in 2025, the last full calendar year (8.1): 21, of which 21 x (2.52 - 1) / 2.52 = 13 caused by corinurad (8.2).
7. Recommendation: open the formal assessment on corinurad and acute kidney injury.

## 4. Deliverable Answers

### signal_refinement_note.docx

1. The signal for the formal assessment: corinurad (Uralexa) and acute kidney injury.
2. Rate ratio for the month after the start: 2.52 (95% CI 1.92 to 3.31), days 1 to 30 against the same people's days 61 to 180; 2.36 to 2.62 against the other control periods of the same comparison (days 31 to 180, 61 to 365, all time after day 30, or all observed time).
3. People who started corinurad in 2025 had 21 admissions with acute kidney injury in days 1 to 30.
4. Of those, 13 caused by corinurad (12 or 13 across those control periods).

### new_users_by_year.csv

1. New users, one row per medicine and calendar year:
   - tasorexant 2022: 1,946
   - tasorexant 2023: 3,895
   - tasorexant 2024: 4,546
   - tasorexant 2025: 4,625
   - corinurad 2022: 11,182
   - corinurad 2023: 12,903
   - corinurad 2024: 13,712
   - corinurad 2025: 13,461
   - velaglutide 2022: 6,153
   - velaglutide 2023: 18,338
   - velaglutide 2024: 21,376
   - velaglutide 2025: 20,070
