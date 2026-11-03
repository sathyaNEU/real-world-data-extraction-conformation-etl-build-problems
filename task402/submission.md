## Tags

**Domain:** Psychology and behavioral science (mediation, moderation and process modelling).
**Analytical objective:** Root-cause analysis.

## 1. Final Recommendation

**Commit the 2026-27 improvement fund to change A, the agency high-intensity therapists on 12-week assignments: they cost the service about 250 recoveries in 2025-26.**
Not C, the waiting list, whose wait-band shortfall sits on the same courses the cover held. Not B, D or E, each of which moved recovery by far less.

## 2. Critical Components

1. Step 3 courses ending in 2025-26 that an agency therapist's lapsing assignment broke off: **733**, of which **114** recovered
2. Recoveries those courses would have had: **371.3**
3. Recoveries change A cost in 2025-26: **250** to the nearest 50

## 3. Step-by-Step Solution

1. Joined care_contacts_2023-10-02_to_2025-10-12.csv and appointments_2025-10-13_to_2026-05-06.parquet, mapped legacy therapist codes to user IDs through clinical_system_users_2026-05-06.xlsx and summed the item scores in outcome_measures_items_2023-10-02_to_2025-10-12.csv: recoveries on the plan's annex measure were 4,355 in 2024-25 and 4,583 in 2025-26 by discharge date.
2. Matched agency users by name to agency_bookings_psychological_therapies_2025-26.xlsx and took each booking's last line end as the assignment end.
3. Flagged step 3 courses ending in 2025-26 whose attended treatment began with an agency therapist and whose next appointment after that therapist's assignment end was with another therapist: 733 courses, 114 recovered.
4. Gave each flagged course the recovery rate of the year's other step 3 referrals that attended at least as many treatment appointments as it had before the lapse: 371.3 expected, a cost of 257.3, 250 to the nearest 50.
5. Counted step 3 patients waiting at each month end from the waiting list snapshots, removing those whose first attended treatment appointment fell on or before the month end in the appointment files.
6. Inferred each Steadyway module's sections from the content IDs seen for users who began before and after 5 January 2026 separately, and counted a module finished when all its sections were completed.
7. Left out the long-standing locum's 2023 booking, took the later of two agency portal timesheets for a week before 1 August 2025 and added e-rostering adjustment lines from then, spread each week over the therapist's working days (a 30-hour booking's four days read from its appointments) and a late first claim over the weeks it covers, and costed each day at its booking line's rate.
8. Change A has the largest cost: fund fixed-term high-intensity posts.

## 4. Deliverable Answers

### improvement_case_2026-27.pptx

1. Change named: A, agency high-intensity therapists on 12-week assignments
2. Its cost: 250 recoveries
3. Slide 3: line chart of recoveries by month of discharge, April to March, 2025-26 against 2024-25

### review_evidence_2025-26.xlsx

1. Step 3 patients waiting at each month end, whole patients:
   - April 2025: 1,907
   - May 2025: 1,955
   - June 2025: 1,787
   - July 2025: 1,271
   - August 2025: 877
   - September 2025: 800
   - October 2025: 763
   - November 2025: 761
   - December 2025: 718
   - January 2026: 716
   - February 2026: 754
   - March 2026: 812
2. Patients who began on the new digital platform and finished at least four modules within eight weeks, whole patients:
   - September 2025: 30
   - October 2025: 25
   - November 2025: 26
   - December 2025: 27
   - January 2026: 27
   - February 2026: 27
3. Agency therapists brought in for the waiting list, hours to the nearest hour and cost to the nearest 100 pounds:
   - May 2025: 757 hours, GBP 44,600
   - June 2025: 2,578 hours, GBP 151,200
   - July 2025: 4,819 hours, GBP 282,700
   - August 2025: 3,594 hours, GBP 210,800
   - September 2025: 2,416 hours, GBP 142,300
   - October 2025: 965 hours, GBP 57,000
