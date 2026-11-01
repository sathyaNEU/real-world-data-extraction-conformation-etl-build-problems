## Tags

**Domain:** Healthcare Delivery & Health Economics (provider quality and risk adjustment: an integrated care board placing its 2027-28 additional elective lumbar spinal operations on each provider's case-mix adjusted 12-month disability change).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Place 910 of the 1,250 additional 2027-28 operations with five providers (Hethercombe Park Hospital 180, Cragsmoor General Hospital 150, Shelderwick Hospital 260, Ravensholt Royal Infirmary 210, Corriemoor Penderwick House Hospital 110) and hold 340 for in-year commissioning.** Over every eligible 2023-25 operation, with each missing 12-month score filled from the answerers at its provider who shared its emergency readmission status, Thistledene Hospital and Ormsbrook Spine Clinic score 14 points each, under the 14.5-point floor. Not seven providers taking all 1,250 (Ormsbrook Spine Clinic 240, Thistledene Hospital 170), the result of reading the returned questionnaires or filling the rest from the case-mix: patients readmitted as an emergency within 90 days of discharge returned the questionnaire 33% of the time against 68% of the rest, and reported a change 17.5 points below the case-mix expectation.

## 2. Critical Components

1. Eligible operations **8,150**, of which **5,208** have a scored 12-month questionnaire.
2. Patients with an emergency admission within 90 days of discharge returned it **33%** of the time against **68%** of the rest, and their returned change sits **17.5** points below expected.
3. Outcomes over every eligible operation, in points: Hethercombe Park Hospital **17**, Cragsmoor General Hospital **16**, Shelderwick Hospital **15**, Ravensholt Royal Infirmary **15**, Corriemoor Penderwick House Hospital **15**, Thistledene Hospital **14**, Ormsbrook Spine Clinic **14**, Oxlade Treatment Centre **13**, Tannerbrook Surgical Centre **13**, Gorsedene Hospital **13**.
4. The providers at or above the floor offered **910** operations, under the 1,250, so **340** are held.

## 3. Step-by-Step Solution

1. Built the 2023-24 and 2024-25 index operations from apc_spells_lumbar_cohort_2022-26.csv under section 2 of spinal_contracting_policy_2027-28.pdf, keeping each spell's latest submission and treating Penderwick House's two codes in provider_reference_2026-09.csv as one provider.
2. Scored both questionnaire deliveries with the eight-section rule and linked them through mossgill_nhs_number_link_2026-09.csv, with deaths from cohort_deaths_linked_2026-09.csv: 8,150 eligible operations, 5,208 with a 12-month score from 48 to 64 weeks.
3. Took each operation's expected change from Appendix B of the policy; the national expected change over the eligible operations is 16.85 points.
4. Joined each eligible operation to the same patient's later spells in the cohort extract: an emergency admission (methods 21 to 28) within 90 days of discharge marks 1,041 operations, whose patients returned the questionnaire 33% of the time against 68%, so the missing scores are not ignorable on the case-mix.
5. Filled each missing score with the mean observed-minus-expected change of the answerers at the same provider with the same readmission status and took 16.85 plus each provider's mean over all its eligible operations.
6. Applied the 14.5-point floor and offered each provider at or above it its total in spinal_capacity_returns_2027-28.xlsx in descending order of outcome: five providers, 910 placed, 340 held.
7. Took the 31 March 2026 rows of ptl_spinal_month_end_2026-01_to_2026-03.csv, dated each triaged patient's clock from the surgical routing in msk_triage_referrals_2023-06_to_2026-03.json to that site with the same birth year, sex, postcode district and practice up to 10 days before the provider's receipt, dated each transferred patient's clock from the sending trust's record in ptl_spinal_removals_2025-11_to_2026-04.csv, and counted each patient moved on or before 31 March only at the receiving provider.
8. Over the 2025-26 index operations by procedure date, linked each pre-operative questionnaire by NHS number, placed each one without an NHS number on the unlinked operation at its site with the same sex and a birth year the age on admission allows, nearest its booked date, and tested the 90-day window against the hospital record's procedure date.

## 4. Deliverable Answers

### spinal_volume_2027-28.csv

1. One row per provider, outcome in whole points and operations placed:
   - Hethercombe Park Hospital: outcome 17, placed 180
   - Cragsmoor General Hospital: outcome 16, placed 150
   - Shelderwick Hospital: outcome 15, placed 260
   - Ravensholt Royal Infirmary: outcome 15, placed 210
   - Corriemoor Penderwick House Hospital: outcome 15, placed 110
   - Thistledene Hospital: outcome 14, placed 0
   - Ormsbrook Spine Clinic: outcome 14, placed 0
   - Oxlade Treatment Centre: outcome 13, placed 0
   - Tannerbrook Surgical Centre: outcome 13, placed 0
   - Gorsedene Hospital: outcome 13, placed 0
   - Not placed (held for in-year commissioning): 340

### spinal_volume_board_paper.docx

1. Recommendation: place 910 operations with the five providers above and hold 340 for in-year commissioning (section 1 and Table 1).
2. Stacked bar chart of each provider's waiting list on 31 March 2026 split at 52 weeks (Figure 1).
3. Patients waiting more than 52 weeks on 31 March 2026, and the share who had waited 18 weeks or less (whole patients, whole per cent):
   - Corriemoor Penderwick House Hospital: 5; 56%
   - Cragsmoor General Hospital: 3; 46%
   - Gorsedene Hospital: 20; 31%
   - Hethercombe Park Hospital: 11; 56%
   - Ormsbrook Spine Clinic: 25; 54%
   - Oxlade Treatment Centre: 27; 50%
   - Ravensholt Royal Infirmary: 50; 33%
   - Shelderwick Hospital: 25; 49%
   - Tannerbrook Surgical Centre: 18; 55%
   - Thistledene Hospital: 4; 54%
4. 2025-26 pre-operative questionnaire participation (whole per cent):
   - Corriemoor Penderwick House Hospital: 81%
   - Cragsmoor General Hospital: 85%
   - Gorsedene Hospital: 84%
   - Hethercombe Park Hospital: 80%
   - Ormsbrook Spine Clinic: 81%
   - Oxlade Treatment Centre: 84%
   - Ravensholt Royal Infirmary: 84%
   - Shelderwick Hospital: 81%
   - Tannerbrook Surgical Centre: 81%
   - Thistledene Hospital: 80%
