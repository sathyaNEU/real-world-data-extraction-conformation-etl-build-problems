## Tags

**Domain:** General Statistics & Data Science (exploratory data analysis and distribution assessment).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Place 59 of the 60 relief positions (Harlan Road Correctional Facility 9, Avesford Correctional Facility 8, Thornmere Women's Correctional Center 7, State Police Communications Center North 6, State Police Communications Center South 6, Fennimore Forensic Hospital, Security Nursing 7, Oxbow Bend Maintenance Garage 10, Kettle Pass Maintenance Garage 6) and return one to the Governor's reserve.**
The positions are filled from the July 2027 entry classes, whose holders will be in their first year on post through FY2028, and the July 2025 classes were off post 7.8 per cent of their scheduled hours in that year against 14.5 per cent for the units' holders. Not the title's average holder, which leaves a relief position 32.4 to 35.3 hours on post a week and needs 63 positions, three short; not FY2026's weeks as they stood with its separations' vacant lines, 62; not the annual relief factor the standard replaced, 38.

## 2. Critical Components

1. The FY2028 need carries the **14** lines the position control holds vacant on 1 July 2027, in full until their first shifts on post (fiscal weeks **10** to **40**).
2. FY2026's **11,968** hours of vacant line-shifts, lines vacated by separation, stay out of the FY2028 need (Budget Instruction 2024-07, 2.4).
3. A relief position's holder is read as an entry-class graduate in the first year on post: the July 2025 classes were off post **7.8** per cent of their FY2026 scheduled hours, the units' holders **14.5** per cent.

## 3. Step-by-Step Solution

1. Took Budget Instruction 2024-07 (2.1 to 3.4) with the Director's memo: each unit's complement is the smallest whole number of relief positions whose hours on post in an average FY2028 week reach its fifth-heaviest FY2028 week of backfill need, the positions filled from the July 2027 entry classes.
2. Summed each unit's off-post hours by fiscal week of FY2026 from merrimont_shift_rosters_fy2026.csv (the latest export of each line and date, both systems' codes through timekeeping_status_codes.csv, training off post), leaving out the 11,968 hours of vacant line-shifts (2.4).
3. Added the 14 lines position_control_fy2028_round_the_clock_units.csv carries vacant: eight hours on each scheduled day (days_off left out) before first_shift_on_post, and from it the new holder's off-post share of those hours.
4. Rated a relief position at 40 hours less the off-post share of the July 2025 classes over FY2026 (academy_class in hr_employee_extract_2026-10-01.csv), by title: 7.8 per cent off post overall.
5. For overtime worked, summed the OT lines' hours and the CTE lines' credited hours over their credit (1.5 under MOU 14.2; hour for hour for the Forensic Security Aides, outside its unit) for FY2026 work dates, each piece once (a later check paying the same employee, work date, start_time and hours again is a second payment), at the unit overtime_offer_log_fy2026.csv posted it at, else the line's timekeeping_location (SL-0410 is Thornmere); OTN and OTR lines carry pay only.
6. For people at each unit, counted once everyone with an OT or CTE piece dated in FY2026 placed at the unit as in step 5, joining each employee whose seniority_date precedes the hire_date to the separated record with the same seniority_date and title.
7. For people over 600 hours, summed overtime worked as in step 5 over each joined person and counted those over 600 hours under the title held in FY2026.
8. Cut each unit's 52 weekly needs at the fifth-heaviest and divided by its title's relief hours, rounding up: Harlan Road Correctional Facility 9, Avesford Correctional Facility 8, Thornmere Women's Correctional Center 7, State Police Communications Center North 6, State Police Communications Center South 6, Fennimore Forensic Hospital, Security Nursing 7, Oxbow Bend Maintenance Garage 10, Kettle Pass Maintenance Garage 6, 59 of the 60, one returned to the reserve.

## 4. Deliverable Answers

### fy2028_relief_positions_by_unit.xlsx

1. Relief positions placed for FY2028 (whole positions):
   - Harlan Road Correctional Facility: 9
   - Avesford Correctional Facility: 8
   - Thornmere Women's Correctional Center: 7
   - State Police Communications Center North: 6
   - State Police Communications Center South: 6
   - Fennimore Forensic Hospital, Security Nursing: 7
   - Oxbow Bend Maintenance Garage: 10
   - Kettle Pass Maintenance Garage: 6
   - All units: 59 of the 60; 1 returned to the Governor's reserve
2. Overtime hours worked at each unit in FY2026 (nearest hour):
   - Harlan Road Correctional Facility: 7,984
   - Avesford Correctional Facility: 8,144
   - Thornmere Women's Correctional Center: 6,824
   - State Police Communications Center North: 7,616
   - State Police Communications Center South: 5,320
   - Fennimore Forensic Hospital, Security Nursing: 9,216
   - Oxbow Bend Maintenance Garage: 5,502
   - Kettle Pass Maintenance Garage: 5,019
3. People who worked overtime at each unit in FY2026:
   - Harlan Road Correctional Facility: 66
   - Avesford Correctional Facility: 66
   - Thornmere Women's Correctional Center: 62
   - State Police Communications Center North: 44
   - State Police Communications Center South: 44
   - Fennimore Forensic Hospital, Security Nursing: 23
   - Oxbow Bend Maintenance Garage: 38
   - Kettle Pass Maintenance Garage: 39
4. People who worked more than 600 hours of overtime in FY2026, by the title they held that year:
   - Correctional Officer: 13
   - Police Communications Operator: 6
   - Forensic Security Aide: 7
   - Highway Maintenance Worker: 2

### fy2028_weekly_backfill_need.png

1. Eight panels, one a unit, of the FY2028 weekly backfill need against the hours the unit's relief positions work on post a week, the weeks above that line (four at most a unit) highlighted.
