## Tags

**Domain:** Human Factors & Ergonomics (anthropometric design fit).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**We should specify Pennick Coachbuild on FD35 for the 2027 front-line ambulance order.**
It fails 166 of our rostered drivers, 153 fewer than the runner-up, Ostrel Vehicle Conversions on FD35, at 319. Not Wrenfold Bodies on FD35, whose longer stated seat travel fits more drivers on paper but whose forward bulkhead stops the backrest of its tall drivers short of their posture, so it fails 450. Not the two RD43 cabs, which fail 399 and 435.

## 2. Critical Components

1. Pennick Coachbuild on FD35 fails **166** rostered drivers.
2. Ostrel Vehicle Conversions on FD35 fails **319**.
3. Wrenfold Bodies on FD35 fails **450** once each driver's backrest is placed against its bulkhead, against **109** on its stated travel and vision alone.

## 3. Step-by-Step Solution

1. Took every staff number on front_line_driving_roster_2026-10-01.csv (the cab fit standard's section 2), joined each to its latest measurement in cab_fit_measurements_2025_26.xlsx through vennerley_staff_number_crosswalk.xlsx for former Vennerley numbers, the Vennerley paper forms converted from inches, stones and pounds: 2,658 drivers.
2. Placed each driver in each shortlisted cab with the hip point, torso angle and eye point equations in driver_posture_model_ellisand_2025.pdf, taking H30, the H-point travel, the bulkhead trim face and the chassis sight points from the package data, package_drawing_data_wrenfold.pdf's dimensions moved from each cab's stated SgRP to the heel point.
3. Set the seat to that posture: the hip point inside the cab's H-point travel, and the backrest at the predicted torso angle with its top rear corner (30.31 in along and 3.74 in behind the torso line, seat_dimension_sheet_brevin_as7.pdf) not behind the bulkhead trim face line at the corner's height.
4. Checked the eye point against the 11 degree upward and 5 degree downward sight lines to the chassis points (section 4) and counted the drivers each cab fails: the figures in block 4.
5. Rebuilt each 2025-26 front-line vehicle from front_line_fleet_register_2026-10-01.xlsx, vehicle_disposals_2025_26.xlsx and vennerley_asset_list_2025-06-27.xlsx (renumbered Vennerley vehicles from their original in-service dates), and gave each job, telematics unit and off-road spell to the vehicle holding its fleet number on its date, reused numbers resolved through the disposals.
6. Counted seat and cab-structure jobs (B12, B30 and their Vennerley codes in workshop_code_map.xlsx) by the quarter first raised, a Vennerley job carried into workshop_jobs_2025_26.csv on 1 July 2025 counted once at its Vennerley date; took miles as each unit's distance while fitted per telematics_unit_changes.xlsx; and days off the road as the calendar days in the union of each vehicle's spells: the converter and chassis figures in block 4.
7. Specified the cab the fewest drivers fail (section 7): Pennick Coachbuild on FD35.

## 4. Deliverable Answers

### cab_fit_2027.xlsx

1. Rostered drivers each shortlisted cab fails to fit, whole drivers:
   - Pennick Coachbuild on FD35: 166, of whom 160 women
   - Ostrel Vehicle Conversions on FD35: 319, of whom 305 women
   - Pennick Coachbuild on RD43: 399, of whom 359 women
   - Wrenfold Bodies on RD43: 435, of whom 121 women
   - Wrenfold Bodies on FD35: 450, of whom 109 women
2. Recommended: Pennick Coachbuild on FD35; runner-up Ostrel Vehicle Conversions on FD35, which fails 153 more drivers.
3. Seat and cab-structure defect jobs raised in 2025-26 by quarter, miles run that year to the nearest hundred and jobs per 100,000 miles to two decimals:
   - Pennick Coachbuild: Q1 76, Q2 74, Q3 85, Q4 81; 2,231,700 miles; 14.16 jobs per 100,000 miles
   - Ostrel Vehicle Conversions: Q1 40, Q2 38, Q3 30, Q4 50; 1,280,400 miles; 12.34 jobs per 100,000 miles
4. Days off the road in 2025-26 by quarter, vehicle-years in service and days off the road per vehicle-year, to one decimal:
   - FD35: Q1 901, Q2 875, Q3 933, Q4 906; 109.9 vehicle-years; 32.9 days per vehicle-year
   - RD43: Q1 422, Q2 457, Q3 524, Q4 523; 52.6 vehicle-years; 36.6 days per vehicle-year

### cab_fit_2027.pdf

5. One bar per shortlisted cab giving the drivers it fails to fit, each bar labelled with its count, the Pennick FD35 bar in blue and marked Recommended.
