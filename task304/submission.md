## Tags

**Domain:** Epidemiology & Public Health (screening and diagnostic policy evaluation: a hepatitis C find-and-treat programme placed and sized by the people it starts on treatment).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**The van should work the needle exchange pharmacies' new registrants in 2027, where it would start about 50 people on hepatitis C treatment, 20 more than at Fenwold Recovery's new entrants (about 30).**
Not the approved premises, where a quarter of arrivals test antibody positive: more than half of those positives had been cured inside prison by Corvane Health before they arrived, and the van would start about 10 there. Not Fenwold Recovery's new entrants, the largest intake: nearly half of their positives had already been cured by the network's clinics. Not the city hostels, about 20.

## 2. Critical Components

1. The van's rates from the 2018-19 pilot: it tested **0.65** of arrivals and started **0.74** of the people with RNA detected within twelve weeks
2. Approved premises arrivals the peer team found antibody positive who had been cured inside prison before they arrived, on Corvane's workbook and not the network's register: **more than half**
3. People started on treatment in 2027: **needle exchange registrants 50**, Fenwold Recovery new entrants 30

## 3. Step-by-Step Solution

1. Counted each setting's distinct arrivals in each plan year (October to September) in setting_arrivals_2023-10_to_2026-09.csv and averaged the two years to 30 September 2026, as the van plan counts a year's arrivals.
2. From van_pilot_2018-19_caseload.csv took the share of arrivals the van tested (937 of 1,450) and the share of people with RNA detected who started within twelve weeks of the test (160 of 215).
3. Matched each valid test in peer_testing_log_2024-10_to_2026-09.csv to its person's arrival in the two years (by pseudonym, the test within 60 days of the arrival) and took each setting's share reactive.
4. For each reactive arrival read the records before the test: a course with a twelve-week result not detected in hcv_treatment_register_2015-2026.csv or corvane_hcv_courses_2017-2026.xlsx counts as cured and inactive unless a later RNA test before the peer test detected it; a course running at the test counts as neither found nor started; otherwise the latest RNA result (virology_hcv_results_2015-01_to_2026-09.csv or the workbook's reception tests) decides; with no record the person counts at the first-positive share 0.74.
5. Multiplied each setting's arrivals by the test share, the reactive share and the mean of step 4 for active infections, then by the start share for people started: needle exchange registrants 50, Fenwold Recovery new entrants 30, city hostels 20, approved premises 10.
6. Clinic outcomes: a course in hcv_treatment_register_2015-2026.csv ended on its last dose (the planned end, or the date it stopped, as the pathway puts it) in the half-year, and is a confirmed cure when its keyed twelve-week result is not detected or, where none is keyed, the first Fenwold Pathology RNA test taken twelve weeks or more after the last dose is not detected, read under every pseudonym Fenwold Pathology holds for the same patient (its lims_patient_id).
7. Placed the van with the needle exchange pharmacies' new registrants, 50 starts against 30.

## 4. Deliverable Answers

### van_2027_trustee_paper.docx

1. The van's setting: the needle exchange pharmacies' new registrants, about 50 people started on treatment in 2027.
2. People with an active infection the van would find in 2027:
   - Approved premises: 10
   - City hostels: 30
   - Fenwold Recovery new entrants: 40
   - Needle exchange new registrants: 70
3. People it would start on treatment in 2027:
   - Approved premises: 10
   - City hostels: 20
   - Fenwold Recovery new entrants: 30
   - Needle exchange new registrants: 50
4. A horizontal bar chart of the people each setting would start, largest first, the needle exchange registrants' bar marked "Van, 2027".

### van_2027_funnel.xlsx

1. Confirmed cures among the courses each clinic ended, by half-year:
   - Hospital hepatology clinic, Oct 2024 to Mar 2025: 15
   - Hospital hepatology clinic, Apr to Sep 2025: 11
   - Community hepatitis clinic, Oct 2024 to Mar 2025: 9
   - Community hepatitis clinic, Apr to Sep 2025: 26
   - Fenwold Recovery clinic, Oct 2024 to Mar 2025: 43
   - Fenwold Recovery clinic, Apr to Sep 2025: 33
   - Pharmacy-led clinic, Oct 2024 to Mar 2025: 3
   - Pharmacy-led clinic, Apr to Sep 2025: 11
   - Outreach nurse clinic, Oct 2024 to Mar 2025: 30
   - Outreach nurse clinic, Apr to Sep 2025: 55
