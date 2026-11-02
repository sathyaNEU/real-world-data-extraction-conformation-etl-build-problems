## Tags

**Domain:** Healthcare Delivery & Health Economics (utilization, access and demand forecasting).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The 2027/28 plan should carry 400 emergency admissions with gallstone disease on NEL-GS-07.** The central expectation is 407.7, of which 47.8 are admissions of patients waiting for a cholecystectomy, on the list the elective capacity plan leaves in 2027/28. Not the 611.4 from age and sex rates on all admissions, which carries the list at the size it held from 2022 to 2026 although the Wyecross Elective Centre has cut it to about a fifth before the plan year.

## 2. Critical Components

1. Patients already on the cholecystectomy list were admitted as emergencies at **0.0211** a patient-month on the list.
2. The capacity plan leaves **2,270** patient-months on the cholecystectomy list in 2027/28.
3. Admissions in 2027/28 of patients waiting for a cholecystectomy: **47.8**.

## 3. Step-by-Step Solution

1. Rebuilt the NEL-GS-07 spells from pas_inpatient_episodes_2021_2026.csv on the activity definitions (first episode, emergency methods, the gallstone codes), mapping Fennick's PAS numbers through fennick_pas_to_epr_number_map.csv.
2. Laid each spell against admitted_ptl_snapshots_2021_2026.parquet: a spell is a listed patient's when a cholecystectomy pathway added before the admission is on the month-end list of the admission month or the month before.
3. Divided the listed patients' spells from April 2022 to October 2026 by the month-end patients on the cholecystectomy list in those months: 0.0211 a patient-month.
4. Carried the other spells' 2024/25 to 2026/27 age and sex rates (April to October annualised) on the 2022-based mid-2027 population in population_projections_2022_based.xlsx, with out-of-area spells in the counts and the two districts' population as the base: about 360.
5. Multiplied the rate by the 2,270 patient-months in the planned month-end lists for April 2027 to March 2028 (elective_capacity_plan_2027_28_general_surgery.pdf, section 3): 47.8, a central expectation of 407.7, submitted as 400 to the nearest 50.
6. Rebuilt each general surgery pathway's clock from the e-Referral Service referral date where the pathway carries a UBRN (ers_referrals_general_surgery_2019_2026.csv), gave a pathway opened on the day its predecessor for the same patient and operation left the list (a re-listing after a cancelled admission) its predecessor's clock, carried a moved patient's clock to the Marlstead pathway, and counted waits of 364 days or more at each quarter end over the list of step 7.
7. Counted hernia repairs (T20.2, T20.4, T24.1) on each month-end list, dropping Fennick rows of pathways for the same patient and operation that Marlstead added later (patients moved to Marlstead's lists) and keeping both sides of a patient listed for two repairs.

## 4. Deliverable Answers

### gallstone_nel_plan_2027_28.xlsx

1. NEL-GS-07 plan figure for 2027/28: **400** emergency admissions with gallstone disease (central expectation 407.7).
2. Built from admissions of patients not on the cholecystectomy list at 2024/25 to 2026/27 age and sex rates (about 360) and 47.8 of patients on it (0.0211 a patient-month on 2,270 planned patient-months).

### rtt_baseline_general_surgery_2025_26.csv

1. Waits of 52 weeks or more from referral, whole numbers:
   - 2025-06-30, Marlstead General: 739
   - 2025-06-30, Fennick: 461
   - 2025-09-30, Marlstead General: 757
   - 2025-09-30, Fennick: 427
   - 2025-12-31, Marlstead General: 792
   - 2025-12-31, Fennick: 389
   - 2026-03-31, Marlstead General: 791
   - 2026-03-31, Fennick: 375
2. Hernia repairs patients were waiting for, whole numbers:
   - 2025-06-30, Marlstead General: 368
   - 2025-06-30, Fennick: 161
   - 2025-09-30, Marlstead General: 389
   - 2025-09-30, Fennick: 137
   - 2025-12-31, Marlstead General: 418
   - 2025-12-31, Fennick: 105
   - 2026-03-31, Marlstead General: 430
   - 2026-03-31, Fennick: 79
