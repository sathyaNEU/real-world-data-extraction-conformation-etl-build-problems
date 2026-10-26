## Tags

**Domain:** Healthcare Delivery & Health Economics (provider quality and risk adjustment).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Fund a 2027 hand hygiene coaching nurse on five wards: AMU, ESSU, 4A, 7A and 9B.**
Carried across every AM and PM shift by how far the shift's worked nursing hours fell short of its patients' required care hours, the gold auditors' moments put these five below 80 per cent and every other ward above it. Not 9B alone, which the audits as they stand give (9B 77.0 per cent, every other ward 82.8 or above): the auditors audited almost only on shifts whose hours covered the care, and staff performed hand hygiene less often where they did not. Not the AM and PM audit shares weighted by care hours, nor the audits carried across every shift by its care hours, which also leave 9B alone: the audited shifts carry the same care hours as the rest, and only the worked hours set against them separate the two.

## 2. Critical Components

1. The audits as they stand put 9B at **77.0** per cent and every other ward at **82.8** per cent or above.
2. **5.3** per cent of the audited AM and PM moments were on shifts whose patients' required care hours exceeded the nurses' worked hours by more than 10 per cent, against **18.8** per cent of the wards' required care hours on AM and PM shifts.
3. On the audited shifts, staff performed hand hygiene at **58.9** per cent of the moments on those shifts and **87.1** per cent on the rest.

## 3. Step-by-Step Solution

1. Took the terms in hand_hygiene_coaching_grant_terms_2027.pdf, section 2: a ward is funded below 80 per cent of the hand hygiene moments on its AM and PM shifts from 1 July 2025 to 30 June 2026, a shift's moments in proportion to its patients' required care hours, at most six wards.
2. Built every ward's AM and PM shifts: required care hours from acuity_patient_shifts_2025_26.csv, worked hours from the rostered rows of nursing_roster_actuals_2025_26.csv (supernumerary rows left out, per acuity_and_roster_extract_notes.txt), S1A read as 6A from 2 February 2026 per ward_and_area_reference.xlsx.
3. Placed each ward session of hand_hygiene_audit_moments_2025_26.csv on the roster shift it began in (no session begins in an overlap; the sessions begun on a night shift, after midnight included, left out): the audits as they stand put 9B at 77.0 per cent and every other ward at 82.8 or above.
4. Set the audited shifts against all shifts: 5.3 per cent of audited moments sat on shifts whose required care hours exceeded worked hours by more than 10 per cent, against 18.8 per cent of required care hours, with compliance there 58.9 per cent against 87.1.
5. Fitted whether hand hygiene was performed on the audited moments by ward and by the shift's ratio of required care hours to worked hours (bands at 1.05, 1.15, 1.25 and 1.35, logistic), and carried each ward's fit across all its AM and PM shifts weighted by required care hours: AMU, ESSU, 4A, 7A and 9B fall below 80 per cent.
6. Ask A: linked each culture in blood_culture_isolates_2025_26.csv to its admission in blood_culture_patient_admissions_2025_26.csv by record number, or by date of birth and sex for a record number the admissions do not hold (to the patient with an admission covering the collection); applied hobsi_surveillance_definitions_v3.pdf, a stay in the hospital running on through an admission that began at the minute the patient's previous admission ended, and an episode being the patient's across admissions; attributed each episode to the ward the patient was on at collection, rebuilt from the admitting ward and ward_transfers_2025_26.csv (a culture's location is the ward that requested it); rates over midnight_census_2025_26.csv.
7. Asks B and C: summed the bottles in store_issues_hand_hygiene_2025_26.csv issued to each ward's cost centre less returns (hand rub: a pump 0.5 L, a carton 2.4 L; soap: a pump 0.5 L) and the refills in dispenser_rounds_2025_26.csv on the ward's dispensers of each type, one refill or cartridge a record (a hand rub refill 1 L, a soap cartridge 0.8 L; a terminal clean's job carries the job's cartridges on each of its records), leaving out the records a handheld sent a second time (a dispenser's record at the same minute of the day as one of its records in the twenty days before); rates over the midnight census.
8. Funded the five wards below 80 per cent, within the cap of six: AMU, ESSU, 4A, 7A and 9B.

## 4. Deliverable Answers

### coaching_wards_2027.xlsx

1. Wards funded for a 2027 coaching nurse: AMU, ESSU, 4A, 7A and 9B.
2. Hospital-onset bloodstream infections 2025-26 and their rate per 10,000 occupied bed days, every ward:
   - AMU: 29, 37.4
   - ESSU: 14, 35.7
   - 4A: 31, 28.6
   - 7A: 32, 34.3
   - 5A: 29, 31.4
   - 6A: 22, 23.3
   - 6B: 18, 23.0
   - 7B: 35, 45.9
   - 8A: 34, 39.9
   - 9A: 13, 12.6
   - 9B: 25, 24.8
   - PCU: 11, 21.0
   - CCU: 17, 52.4
   - ICU: 41, 67.7
3. Alcohol-based hand rub put out in 2025-26, litres and litres per 1,000 occupied bed days, every ward:
   - AMU: 404.6, 52.2
   - ESSU: 181.6, 46.3
   - 4A: 444.6, 41.0
   - 7A: 391.3, 41.9
   - 5A: 303.7, 32.8
   - 6A: 279.4, 29.6
   - 6B: 283.5, 36.2
   - 7B: 324.6, 42.6
   - 8A: 453.9, 53.3
   - 9A: 262.8, 25.5
   - 9B: 321.4, 31.9
   - PCU: 118.5, 22.6
   - CCU: 244.0, 75.2
   - ICU: 701.5, 115.9
4. Liquid hand soap put out in 2025-26, litres and litres per 1,000 occupied bed days, every ward:
   - AMU: 125.0, 16.1
   - ESSU: 66.7, 17.0
   - 4A: 121.1, 11.2
   - 7A: 130.1, 13.9
   - 5A: 119.3, 12.9
   - 6A: 103.6, 11.0
   - 6B: 86.0, 11.0
   - 7B: 110.0, 14.4
   - 8A: 146.6, 17.2
   - 9A: 132.6, 12.9
   - 9B: 144.1, 14.3
   - PCU: 74.8, 14.3
   - CCU: 60.4, 18.6
   - ICU: 154.1, 25.5

### ward_compliance_2025_26.png

1. Bar chart with one bar per ward, its 2025-26 compliance over its AM and PM shifts together, against a dashed 80 per cent line, the five funded wards (AMU, ESSU, 4A, 7A and 9B) in orange and the rest in blue.
