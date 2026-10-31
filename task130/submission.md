## Tags

**Domain:** Psychology & Behavioral Science (decision-making and computational behavioral modeling).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Add the third return-inspection officer for 2027: the routine inspections in the 2027 schedule are forecast to produce about 700 unsatisfactory inspections, above the plan's 540.** The deciding figure is each scheduled inspection read at the number of earlier visits its named inspector will have made to the establishment, since 1,277 of the 5,512 are first visits. Not the risk-category rates, about 437, which average over years when fewer than one routine inspection in ten was a first visit; not each establishment's own record (458) or one rate per inspector (451), which read the same familiar pairs.

## 2. Critical Components

1. The 2027 schedule carries **5,512** routine inspections, and **1,277** of them fall to an inspector with no earlier inspection of the establishment on the record since January 2019, against fewer than one in ten in every year from 2022 to 2026.
2. In 2022 to 2026 a first visit was marked unsatisfactory in **14.4**, **28.2** and **32.4** per cent of routine inspections in risk categories 1, 2 and 3, against **2.9**, **4.8** and **8.4** per cent at a third or later visit.
3. The 2027 forecast is **693.4** unsatisfactory routine inspections, about **700**, against the plan's **540**.

## 3. Step-by-Step Solution

1. Stacked inspections_2019-01_2024-03.csv and inspections_2024-03_2026-12.csv, matched the legacy inspector initials to the names in food_program_staff_roster.xlsx, converted inspected_at_utc to Pacific time, and classed every routine inspection made since January 2019 by its inspector's earlier inspected visits of any type to the permit (closed-premises calls are not inspections) as a first, second, or third or later visit.
2. Took the unsatisfactory share (UNSAT, IHH CLOSURE, Unsatisfactory, Closed - imminent health hazard) of the 2022 to 2026 routine inspections in each risk category and class: first visits 14.4, 28.2 and 32.4 per cent, second 5.6, 10.2 and 18.9, third or later 2.9, 4.8 and 8.4.
3. Read each routine inspection in routine_inspection_schedule_2027.xlsx at the class its district's inspector in Table 1 of food_safety_program_plan_2027.pdf will have reached, counting that inspector's earlier inspections of the permit and the schedule's own earlier 2027 ones (1,277 first, 1,031 second, 3,204 later), and summed the rates: 693.4, about 700, over the 540 of section 3.
4. For ask A, dated each return-team inspection the new export dates on or before 15 September 2026 by the earliest unused entry of the same officer and street address in the Day sheet log of return_team_capacity_report_2026.xlsx dated up to 20 days earlier, and counted weekdays outside county_holidays_2025-2027.json from each 2026 unsatisfactory routine inspection to the first return inspection that inspected the premises, where that return fell in 2026.
5. For ask B, measured each 2026 complaint investigation from the earliest report in complaints_2024-03_2026-12.csv for its permit received after the permit's previous investigation, to the inspector's arrival.
6. For ask C, added the closed-premises calls dated by the RV-NA letters in correspondence_log_2026.csv to each 2026 unsatisfactory routine inspection's return visits (day-sheet dates as in step 4), and charged every 2026 visit after the first under environmental_health_fee_schedule_2026.pdf at the rate in force on the day of the visit (USD 152, then USD 168 from July).
7. Recommended adding the third return-inspection officer for 2027, the forecast of about 700 exceeding the two officers' 540.

## 4. Deliverable Answers

### return_officer_memo_2027.pdf

1. Recommendation: add the third return-inspection officer for 2027.
2. The 2027 routine inspections that will be marked unsatisfactory, nearest hundred inspections: 700, against the plan's 540.
3. One page: the call in its first sentence, the forecast against 540, why 2027 runs above 2026, how the forecast was built, and a table of scheduled inspections, first visits and the forecast for each 2027 district.

### return_inspections_2027.xlsx

4. Median return timeliness for the 2026 unsatisfactory routine inspections that had their first return inspection in 2026, working days to one decimal:
   - District 1: 10.0
   - District 2: 10.0
   - District 3: 9.0
   - District 4: 9.0
   - District 5: 11.0
   - District 6: 8.5
   - District 7: 10.0
   - District 8: 9.0
   - District 9: 9.0
   - District 10: 8.5
   - District 11: 13.0
5. Median complaint response time for the 2026 complaint investigations, hours to one decimal:
   - District 1: 71.9
   - District 2: 89.8
   - District 3: 80.2
   - District 4: 69.1
   - District 5: 124.6
   - District 6: 60.3
   - District 7: 98.4
   - District 8: 63.1
   - District 9: 155.5
   - District 10: 63.3
   - District 11: 66.3
6. Return visit fees due for the 2026 visits that followed each district's 2026 unsatisfactory routine inspections, dollars:
   - District 1: 1,416
   - District 2: 2,624
   - District 3: 2,544
   - District 4: 3,200
   - District 5: 4,376
   - District 6: 2,576
   - District 7: 2,024
   - District 8: 3,792
   - District 9: 2,528
   - District 10: 2,544
   - District 11: 2,424
