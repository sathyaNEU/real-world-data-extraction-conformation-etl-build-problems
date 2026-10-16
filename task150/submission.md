## Tags

**Domain:** Sociology & Demography (population estimation and demographic projection: each attendance area's October K-5 pupils projected grade by grade over the school years 2028-29 to 2032-33, with exits and moves between areas rated on the area a pupil leaves and arrivals from outside the district as counts).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Place the 24 classrooms at Prairie Rose 7, Lincoln 6, Fifth Street 5, Bluestem 4 and Kessler 2, and none at Ortega or North Fork.**
Projected flow by flow, the five schools need 7, 6, 5, 4 and 3 classrooms (26 with North Fork's 1), so the 24 run out at Kessler, which is placed the 2 that remain. Not Bluestem 7, Fifth Street 3, Lincoln 6 and Prairie Rose 8 with none at Kessler, which five-year grade progression ratios give by striking Fifth Street's and Prairie Rose's steady stream of arrivals on classes of the past size and Ortega's transfers on Bluestem's and Kessler's classes; run from 2019, those ratios came out 8.2 per cent low at Fifth Street and 8.3 per cent high at Prairie Rose by 2026.

## 2. Critical Components

1. Classroom need: Prairie Rose **7**, Lincoln **6**, Fifth Street **5**, Bluestem **4**, Kessler **3**, North Fork **1**, Ortega **0** (**26** in all against the program's 24)
2. Order above rated capacity: Prairie Rose, Lincoln, Fifth Street, Bluestem, Kessler, North Fork; Ortega's five-year average is below its rated capacity

## 3. Step-by-Step Solution

1. Linked every pupil's October records from membership_oct2013-oct2018.txt and october_membership_2019-2026.csv through student_number_crosswalk_2019.csv and school_codes.csv (Southeast is Kessler): 76,597 pupil rows on 14 count days.
2. Counted each of the 13 transitions from one October to the next by the school a pupil left (exits, moves by destination, repeats) and the pupils new to the roll: Fifth Street took 66 to 89 arrivals into grades 1 to 5 a year and Prairie Rose 61 to 81 while their K-4 pupils went from 741 to 639 and from 532 to 752, and Ortega sent Bluestem 58 to 93 a year, 9.3 to 11.8 per 100 Ortega K-4 pupils.
3. Projected each grade with repeats rated on that grade's pupils, moves and exits rated on the K-4 pupils of the school left, arrivals at each school's average count per grade, and kindergartners as new kindergartners per resident birth five years earlier (brandt_county_births_by_attendance_area_2008-2025.csv, births for 2026 and 2027 at the 2023-25 average), all over the 13 transitions.
4. Back-tested from 2019 (fitted on the transitions to 2019, run from the 2019 count with the births on file): the projection misses each school's 2026 count by 5.0 per cent or less, while five-year progression ratios come out 8.2 per cent low at Fifth Street and 8.3 per cent high at Prairie Rose.
5. Rolled every school from the October 1, 2026 count to 2032 and averaged 2028 to 2032 against rated capacity in facilities_capacity_report_2026-09.xlsx: above capacity by 152 pupils at Prairie Rose, 131 at Lincoln, 109 at Fifth Street, 89 at Bluestem, 60 at Kessler and 10 at North Fork, and 92 below at Ortega.
6. Classroom need under BP_FEA-R2_elementary_classroom_placement.pdf 2(e) (excess over 24, rounded up): 26 in all.
7. Placed under FEA-R2 3 in that order, the need or eight until 24: Prairie Rose 7, Lincoln 6, Fifth Street 5, Bluestem 4, Kessler 2.

## 4. Deliverable Answers

### classroom_placement_2028-33.xlsx

1. Classrooms each school's projected enrollment calls for (its classroom need) and classrooms placed:
   - Fifth Street Elementary: need 5, placed 5
   - Lincoln Elementary: need 6, placed 6
   - Ortega Elementary: need 0, placed 0
   - Bluestem Elementary: need 4, placed 4
   - Prairie Rose Elementary: need 7, placed 7
   - Kessler Elementary: need 3, placed 2
   - North Fork Elementary: need 1, placed 0
2. Homeroom classes meeting on October 1, 2026:
   - Fifth Street Elementary: 17 in kindergarten to grade 2, 17 in grades 3 to 5
   - Lincoln Elementary: 19 in kindergarten to grade 2, 15 in grades 3 to 5
   - Ortega Elementary: 19 in kindergarten to grade 2, 13 in grades 3 to 5
   - Bluestem Elementary: 15 in kindergarten to grade 2, 20 in grades 3 to 5
   - Prairie Rose Elementary: 21 in kindergarten to grade 2, 20 in grades 3 to 5
   - Kessler Elementary: 15 in kindergarten to grade 2, 17 in grades 3 to 5
   - North Fork Elementary: 13 in kindergarten to grade 2, 13 in grades 3 to 5
3. Preschool on October 1, 2026:
   - Fifth Street Elementary: 88 children enrolled, 4 classrooms
   - Ortega Elementary: 94 children enrolled, 4 classrooms
   - Kessler Elementary: 51 children enrolled, 3 classrooms
   - North Fork Elementary: 35 children enrolled, 3 classrooms

### enrollment_vs_capacity_2026-33.png

1. One panel per school: October K-5 enrollment 2013 to 2026 from the membership snapshots, the projection to 2032, rated capacity across the panel and capacity with the placed classrooms from 2028.
