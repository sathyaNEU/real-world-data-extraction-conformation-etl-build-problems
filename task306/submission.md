## Tags

**Domain:** Pharmacology, Pharmacoepidemiology & Safety (benefit-risk assessment: a GP federation choosing the deprescribing review its pharmacist team runs, by the serious harm each would avoid).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Run review B, benzodiazepines and Z-drugs in people aged 65 and over: it would take about 290 patients off their medicine and avoid about 12 serious harms a year, 4 more than review C, gabapentinoids taken with an opioid, the runner-up at 8.** Not review A, antipsychotics in people aged 65 and over: its pilot off rate is the highest (40.0 per cent), but a specialist service started 86 per cent of its patients in scope and the pilot took only 4 of 96 such patients off, so it avoids about 6. Not review C as the first choice: it takes the most patients off (about 340), but its medicines carry the least harm per patient-year.

## 2. Critical Components

1. Patients in scope on 31 December 2026: A **612**, B **1,239**, C **1,636**.
2. Pilot patients off at six months, medicine started by the practice: A **63 of 136**, B **68 of 276**, C **65 of 192**; started by a specialist service: A **1 of 24**, B **1 of 24**, C **2 of 48**.
3. Patients in scope whose medicine a specialist service started: A **86%**, B **6%**, C **44%**.
4. Patients off at six months and serious harms avoided a year: A **about 60** and **6**, B **about 290** and **12**, C **about 340** and **8**.

## 3. Step-by-Step Solution

1. Ran protocols A, B and C (deprescribing_review_protocols_2026.pdf) on 31 December 2026 over prescribing_issues_2025-07_2026-12.parquet, problem_list_extract_2026-12-31.csv and patient_registrations_2020-2026.parquet for patients registered outside the Clun Valley network (programme specification, section 3): 612, 1,239 and 1,636 patients in scope.
2. Marked a patient's medicine as started by a specialist service when trust_medicine_letters_feed_2019-2026.csv (patients without a pseudonym resolved through trust_hospital_number_lookup.csv) holds a letter naming a medicine of the review's class dated in the 60 days before the first issue of the patient's earliest course of that class in repeat_medication_courses_2026-12-31.csv: 86%, 6% and 44% of patients in scope.
3. Split the six-month rows of deprescribing_pilot_outcome_log_2026.csv the same way: practice-started 63 of 136, 68 of 276 and 65 of 192 off; specialist-started 1 of 24, 1 of 24 and 2 of 48.
4. Gave each patient in scope the pilot rate for their review and way of starting, times the table 1 harm rate at their age on 31 December 2026, and summed (programme specification, section 3): about 60, 290 and 340 patients off; 6, 12 and 8 serious harms a year.
5. Recommended review B, 4 harms a year ahead of review C.
6. Letters: one per letter reference in the feed, a Marches Mental Health letter dated 7 April 2026 with the same patient, service, encounter date and lines as an earlier letter counted as that letter; each letter's half and practice from its first receipt in practice_document_workflow_2026.csv (programme specification, section 4), found by its sender reference or, for a Wrekinside letter with none there (GP Connect from October 2026), as the first Wrekinside receipt for the same patient that carries no letter's reference, was received on or within 21 days after the letter date and was not taken by an earlier letter, a letter with no receipt by the 6 January 2027 extract not received in 2026; the receiving practice's network; per 1,000 on registered_list_sizes_2026.csv at 1 January and 1 July.
7. Consultations: attended one-to-one rows of pharmacist_hub_appointments_2026.csv (UTC to UK time), the rows of clinical_system_pharmacist_activity_2026.csv except each hub appointment's record by the same pharmacist for the same patient on the day or the next working day, and each attended patient in hub_group_session_register_2026.xlsx (programme specification, section 4); the network of the patient's practice on the day; per 1,000 on the list at the start of the quarter.

## 4. Deliverable Answers

### medicines_safety_review_2027.pdf

1. Recommendation: run review B, benzodiazepines and Z-drugs in people aged 65 and over.
2. Runner-up: review C, gabapentinoids taken with an opioid.
3. Gap: 4 serious harms a year.
4. Patients off their medicine at six months, nearest 10:
   - Review A: 60
   - Review B: 290
   - Review C: 340
5. Serious harms avoided a year, whole numbers:
   - Review A: 6
   - Review B: 12
   - Review C: 8
6. Chart (figure 1): each review's patients off at six months beside the serious harms avoided a year, review B highlighted.
7. Hospital medicine letters received per 1,000 registered patients, one decimal:
   - Clun Valley PCN: January to June 46.0, July to December 43.3
   - Severn Gorge PCN: January to June 43.5, July to December 40.4
   - Teme Valley PCN: January to June 45.7, July to December 40.6
   - Wrekinside Central PCN: January to June 42.3, July to December 37.4
   - Wrekinside North PCN: January to June 43.0, July to December 41.7

### pharmacist_consultations_2026.csv

1. Patient consultations per 1,000 registered patients, one decimal:
   - Clun Valley PCN: Q1 12.8, Q2 13.3, Q3 13.4, Q4 13.4
   - Severn Gorge PCN: Q1 11.9, Q2 10.0, Q3 13.0, Q4 11.9
   - Teme Valley PCN: Q1 13.8, Q2 12.8, Q3 13.7, Q4 12.3
   - Wrekinside Central PCN: Q1 11.2, Q2 10.4, Q3 10.6, Q4 10.4
   - Wrekinside North PCN: Q1 12.5, Q2 11.6, Q3 11.7, Q4 11.4
