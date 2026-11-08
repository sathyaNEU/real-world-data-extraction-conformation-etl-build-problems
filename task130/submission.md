## Tags

**Domain:** Economics & Econometrics (discrete choice and limited dependent variable modelling).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**No: Redbud's field employees will record about 255 recordable injuries on Pinewater work in 2027, a rate of 3.57 per 200,000 hours on the 2027 work plan, above the 3.0 limit of CS-4, so the plan puts Redbud in enhanced oversight for 2027.** The deciding figure is the rate the crews record in the first 35 days of their HR-14 recognition counts, where an award is far off, carried onto every 2027 crew hour once the programme ends on 31 December 2026. Not the recorded rate of 2.46 carried forward, which gives 176 recordables inside the limit, because crews leave injuries they can hide off the log as each count nears its award.

## 2. Critical Components

1. From 2021 to 2026 the crews recorded **2.55** recordables per 200,000 hours and the technicians, outside HR-14, **1.92**; carried onto the 2027 plan that record gives **176** recordables, a rate of **2.46**.
2. Read against each crew's own 90-day count, the crews record **3.85** per 200,000 hours in days 0 to 14, **3.84** in days 15 to 34, **3.07** in days 35 to 49, **1.38** in days 50 to 64 and **1.01** in days 65 to 89.
3. With no award at stake in 2027, the crews' rate in days 0 to 34 (**3.84**) on 12,258,000 crew hours and the technicians' **1.92** on 2,030,000 hours give **255** recordables: **60**, **66**, **67** and **62** by quarter, each a rate of **3.57**.
4. The limit of 3.0 allows about **214** recordables on the plan's **14,288,000** hours, so the forecast is over it.

## 3. Step-by-Step Solution

1. Stacked ehs_case_log_2021-2024.csv and the Cases sheet of case_management_export_2024-2026.xlsx, kept each case's latest revision and the new system's copy of each migrated case, and dropped first aid, linked recurrences and mutual-aid (MA-) work.
2. Placed each case on the worker's crew or team on its injury date from crew_assignments_2020-2026.csv, with the crews recoded in March 2025 carried under their new codes (crew_register_2026.xlsx).
3. Took hours worked from timesheet_hours_by_pay_period_2021-2026.csv as regular plus overtime hours, each prior-period adjustment in the pay period it corrects, and spread each pay period's crew hours over its working days.
4. Rebuilt each crew's HR-14 count day by day from 11 January 2021, restarting it the day after a recordable injury to any member and the day after each 90th day (crew_safety_recognition_programme.docx), and computed the crews' recordables per 200,000 hours by day of the count.
5. Applied the crews' rate in days 0 to 34 of their counts and the technicians' recorded rate to the crew and technician hours of work_plan_hours_2027.xlsx, quarter by quarter.
6. For the first-aid cases, counted each injury once: a Nurse line case is the injury of the Supervisor case for the same worker dated up to three days before its call, and a Nurse line case with none is an injury of its own; counted first-aid injuries on Pinewater work from 5 January to 27 September 2026 by the calendar quarter of the injury date and the district of the worker's crew or team on that day.
7. Compared the 2027 rate with the limit of 3.0 in pinewater_contractor_safety_standard_cs4.docx.

## 4. Deliverable Answers

### safety_plan_recordables_2027.docx

1. Within the 3.0 limit in 2027: No.
2. 2027 recordable injuries: 255, a rate of 3.57 per 200,000 hours.
3. By quarter of 2027:
   - Q1: 60 recordables, 3.57
   - Q2: 66 recordables, 3.57
   - Q3: 67 recordables, 3.57
   - Q4: 62 recordables, 3.57

### recordables_by_quarter_2027.png

4. The four quarters' forecast recordables (60, 66, 67 and 62) against the count the 3.0 limit allows in each quarter.

### recordables_forecast_2027.xlsx

5. First-aid cases on Pinewater work, 5 January to 27 September 2026:
   - Blue Ridge: Q1 36, Q2 44, Q3 19, in all 99
   - Piedmont: Q1 38, Q2 34, Q3 32, in all 104
   - Lakes: Q1 45, Q2 46, Q3 30, in all 121
   - Coastal: Q1 52, Q2 51, Q3 33, in all 136
