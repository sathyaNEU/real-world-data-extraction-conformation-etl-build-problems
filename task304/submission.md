## Tags

**Domain:** Epidemiology & Public Health (screening and diagnostic policy evaluation: a hepatitis C find-and-treat van placed and sized by the people it starts on treatment).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**The van should work with Fenwold Recovery's new entrants in 2027, where it would start about 70 people on hepatitis C treatment, 20 more than at the needle exchange pharmacies' new registrants.**
Not the needle exchange registrants, where the van found the most infections per test in 2026: pharmacist test and treat reaches every needle exchange pharmacy on 1 April 2027, and at the three pharmacies already running it the van found 3 in 120 tests. Not the city hostels, where the van had already tested 737 of the 905 residents in 2026, so it would start about 40. Not the approved premises, at about 20.

## 2. Critical Components

1. The van's 2026 yield per test at the three needle exchange pharmacies running pharmacist test and treat, the rate every pharmacy carries from April 2027: **0.025**, against 0.168 at the other 21
2. City hostel residents on the 30 September 2026 lists the van had already tested in 2026: **737 of 905**, leaving 168 untested
3. People started on treatment in 2027: **Fenwold Recovery new entrants 70**, needle exchange new registrants 50, city hostels 40, approved premises 20

## 3. Step-by-Step Solution

1. From van_tests_2026-01_to_2026-09.csv, each contact_ref once, took each setting's share of people offered who took a test and the found per test, and from hcv_treatment_register_2015-2026.csv the share of people found by 8 July 2026 who started within 84 days: approved premises 0.86, 0.080, 0.50; hostels 0.95, 0.120, 0.81; Recovery hub 0.82, 0.073, 0.62; pharmacies 0.70, 0.140, 0.72.
2. Sized each 2027 pool as the plan's section 5 sets it: approved premises 102 residents and 485 arrivals (approved_premises_returns_2023-10_to_2026-09.csv), hostels 905 residents on hostel_residents_2026-09-30.xlsx and 264 arrivals (hostel_occupancy_returns_2023-10_to_2026-09.csv), 1,872 new treatment episodes (fenwold_recovery_new_episodes_2023-10_to_2026-09.csv) and 1,861 first registrations, each client_code's earliest row in nsp_registrations_2019-04_to_2026-09.csv.
3. Pharmacies: fenwold_icb_commissioning_intentions_2027-28.pdf (PH-12) puts test and treat at every needle exchange pharmacy from 1 April 2027; the register's pharmacist-prescribed courses show FW318, FK207 and FN562 doing it since 2025, where the van found 3 of 120 tested; January to March 2027 at each pharmacy's own 2026 rate and April to December at those three's gives 68.8 people found.
4. Hostels: joined the residents lists to the van's 2026 tests by pseudonym, 737 of 905 tested (89 of them found); the 168 untested and the 264 arrivals at the 2026 found per test, and the 648 who tested negative at the homeless health clinic's new infections per person-year in virology_hcv_results_2015-01_to_2026-09.csv, 2 in 1,559, gives 49.9 people found.
5. Multiplied each setting's people found by its start share: Recovery new entrants 68.7, pharmacies 49.3, hostels 40.5, approved premises 20.2 people started.
6. Cures: took each course's last dose as its last pack in daa_dispensing_2024-04_to_2026-09.csv plus 27 days (the register's end_date is the course's planned end), followed a course open at the 1 October 2024 go-live through migrated_from as one course, and counted a confirmed cure where an RNA result Not detected sits 84 days or more after that last dose and before any later course, per the pathway's section 3: the ten counts in block 4.
7. Placed the van with Fenwold Recovery's new entrants, 70 people started against 50.

## 4. Deliverable Answers

### van_2027_trustee_paper.docx

1. Setting for 2027: Fenwold Recovery's new entrants
2. People with an active infection the van would find in 2027, nearest 10: approved premises 40; city hostels 50; Fenwold Recovery's new entrants 110; needle exchange pharmacies' new registrants 70
3. People the van would start on treatment in 2027, nearest 10: approved premises 20; city hostels 40; Fenwold Recovery's new entrants 70; needle exchange pharmacies' new registrants 50
4. Bar chart of the four settings' 2027 starts on page 1, Fenwold Recovery's new entrants marked in blue as the setting chosen

### clinic_cures_2024-25.xlsx

1. Confirmed cures among courses that ended in each half-year, whole counts:
   - Fenwold Royal Infirmary hepatology clinic: October 2024 to March 2025 66; April to September 2025 35
   - Kestle Road community hepatitis clinic: October 2024 to March 2025 44; April to September 2025 36
   - Fenwold Recovery hub clinic: October 2024 to March 2025 38; April to September 2025 29
   - Riverside homeless health clinic: October 2024 to March 2025 21; April to September 2025 23
   - Fenwold sexual health clinic: October 2024 to March 2025 18; April to September 2025 23
