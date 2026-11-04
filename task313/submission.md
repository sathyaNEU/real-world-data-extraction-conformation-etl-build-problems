## Tags

**Domain:** Healthcare Delivery & Health Economics (patient flow, beds and workforce optimisation).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Give Kellingworth University Hospital 9 of the 30 outreach posts, Ravensby Royal Infirmary 7, Sedgefold Hospital 6, Wennby Community Hospital 5 and St Aldric's Hospital 3; the service will avoid about 325 readmissions in 2027/28.**
The posts follow the readmissions a nurse can still reach: about a quarter of Ravensby Royal's and St Aldric's eligible readmissions happen before the community midwifery office receives the discharge notification, against almost none at Kellingworth and Sedgefold. Not the trial's 57 per cent on every eligible readmission (8, 8, 5, 4 and 5 posts and about 375 avoided), which credits the two units whose notifications reach the office a day or more after discharge with readmissions no nurse could have prevented.

## 2. Critical Components

1. Eligible babies discharged home 1 October 2025 to 30 September 2026: **2,803, 2,419, 1,908, 1,514 and 1,639** at Ravensby Royal, Kellingworth, Sedgefold, St Aldric's and Wennby
2. The Copperfield trial's cut in 28-day readmission after its first call: **57 per cent**
3. Readmissions avoided across the five units in 2027/28: **325**

## 3. Step-by-Step Solution

1. Read rk_maternity_postnatal_discharges_2024-04_2026-10.csv and the three sheets of sw_maternity_postnatal_discharges.xlsx and kept babies discharged home 1 October 2025 to 30 September 2026 with the risk flag, twins included (SS-MAT-027 sections 3 and 8): 2,803, 2,419, 1,908, 1,514 and 1,639 eligible babies.
2. Keyed neonatal_paediatric_admissions_2024-04_2026-10.csv to them by NHS number, through mpi_baby_hospital_numbers.csv where the NHS number is blank, keeping emergency admissions (methods 21, 22 and 28, and a transfer inside the stay) within 28 days of discharge, once per baby (section 5).
3. Took each baby's first Discharge home notification from community_midwifery_notifications_2024-04_2026-10.csv, converted from UTC, matched on the hospital number where the NHS number fails its check digit; the earliest the outreach line can reach the family is that receipt, or 08:00 when it arrived outside 08:00 to 19:00, the hours in which copperfield_outreach_contacts.csv shows a receipt called the same day.
4. Kept each unit's eligible readmissions that came after that point; the others happened before any nurse could call and the service cannot avoid them.
5. From copperfield_trial_randomisation_final.xlsx and the same linkage, with Copperfield's postnatal-ward readmissions filed under the mother's NHS number mapped to her baby, the trial's risk ratio after the first call is 0.43, a 57 per cent cut, the same as over the whole 28 days; the final report finds no interaction by gestation, feeding or primary risk reason, so one pooled effect carries.
6. Applied 57 per cent to each unit's reachable readmissions and split the 30 posts by section 7, whole posts then largest remainders: 7, 9, 6, 3 and 5, with about 325 readmissions avoided.
7. For the trial's reason table, counted each analysed baby under every reason on its SW discharge record (newborn_risk_reasons.csv) and its readmissions as in step 5, including the rows filed under the mother at Copperfield.
8. For the contact table, read copperfield_outreach_contacts.csv once per contact_id, mapped calls under a mother's NHS number to her baby, left out NA and TNA rows and the short HV and TEL attempts filed before those codes came into use on 6 January 2025 (outreach_contact_types.csv), and kept contacts in the 28 days after discharge.

## 4. Deliverable Answers

### outreach_posts_2027-28.xlsx

1. Posts from 1 April 2027, by unit:
   - Ravensby Royal Infirmary: 7
   - Kellingworth University Hospital: 9
   - Sedgefold Hospital: 6
   - St Aldric's Hospital: 3
   - Wennby Community Hospital: 5
2. Readmissions avoided in 2027/28, to the nearest 25: 325
3. Copperfield trial, babies analysed, by risk reason: usual-care 28-day readmission rate and risk ratio for outreach:
   - Late preterm (35 to 36 weeks): 8.5 per cent, 0.35
   - Breastfed first baby: 6.1 per cent, 0.64
   - Discharged under 18 hours: 6.6 per cent, 0.40
   - Weight loss 8% or more: 6.2 per cent, 0.29
   - Visible jaundice at discharge: 7.9 per cent, 0.49
   - Sibling needed phototherapy: 5.7 per cent, 0.65
4. Copperfield trial, outreach arm, by risk reason: home visits made and telephone calls that reached the family per baby in the 28 days after discharge:
   - Late preterm (35 to 36 weeks): 1.80 visits, 2.93 calls
   - Breastfed first baby: 1.24 visits, 2.81 calls
   - Discharged under 18 hours: 1.20 visits, 2.60 calls
   - Weight loss 8% or more: 1.53 visits, 3.02 calls
   - Visible jaundice at discharge: 1.48 visits, 2.54 calls
   - Sibling needed phototherapy: 1.33 visits, 2.59 calls

### outreach_posts_by_unit.svg

5. Horizontal bar chart of the posts by unit, largest first, each bar labelled with its posts and Kellingworth highlighted, with the readmissions avoided in the subtitle.
