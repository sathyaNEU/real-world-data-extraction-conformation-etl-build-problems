## Tags

**Domain:** Education and learning sciences (learning analytics and early-warning models).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**Set the spring in-class skill builders at 8 problems before the five-problem check.**
At 8 problems Units 4 to 7 are expected to produce about 3,500 failed checks against the 4,100 funded reteach places; 6 problems would produce about 4,500, over the places, and 10 problems about 2,750, longer than the places need. Not the homework record replayed, where students stopped at three right in a row and finished over several evenings, which puts even 6 problems inside the places. Not a learning curve fitted across sittings, which reads the loss between evenings as slow learning and puts every length over the places.

## 2. Critical Components

1. Expected failed checks at 6 problems: **4,500**
2. Expected failed checks at 8 problems: **3,500**
3. Expected failed checks at 10 problems: **2,750**

## 3. Step-by-Step Solution

1. Stacked pellmore_problem_log_2025-26_aug_dec.csv (Eastern local time) with pellmore_problem_log_2026_jan_jun.csv and pellmore_problem_log_2026-27_to_2026-10-23.csv (UTC put on Eastern time), mapped accounts to students through pellmore_student_link.csv (staff test accounts have no link and drop out) and each assignment to its skill builder through pellmore_assignments_2025-2027.csv.
2. Ordered each student's first attempts on each skill builder and split them into sittings, a new sitting starting after a break of more than three hours; for every problem, counted the student's earlier problems in the same sitting and in earlier sittings.
3. Fitted first-attempt correctness on a normal random intercept per student (spread by Laplace maximum likelihood), an easiness per skill builder and, per skill builder, one slope on each of the two counts.
4. For each of the 2,402 seventh graders on roll on 23 October 2026 (grade7_roster_2026-10-23.xlsx) and each of skill builders 4 to 7, computed the chance of fewer than 3 of 5 check problems right after a set of 6, 8 or 10 problems in one sitting (no earlier-sitting problems), averaged over the student's ability given their fall practice, and summed: about 4,500, 3,500 and 2,750 failed checks.
5. Applied spring_2027_grade7_math_plan.docx: the shortest length whose expected failed checks fit the 4,100 places is 8 problems.
6. Counted the problems on skill builders 4 to 7 in pellmore_problem_log_2026_jan_jun.csv by students in pellmore_student_link.csv, by skill builder, at the school sis_archive/enrollment_history_2025-26.csv shows them attending on the Eastern-time day each problem was started (the log's school_code is each account's school when the export ran on 19 October 2026, and problems started between two enrollments count for no school).

## 4. Deliverable Answers

### spring_practice_set_length.xlsx

1. Expected failed checks by set length, Units 4 to 7, nearest 250:
   - 6 problems: 4,500
   - 8 problems: 3,500
   - 10 problems: 2,750
2. Recommended set length: 8 problems
3. Expected failed checks at 8 problems by spring unit, nearest 250:
   - Unit 4 (Percent Problems): 750
   - Unit 5 (Equations and Inequalities): 1,250
   - Unit 6 (Angles, Area and Volume): 750
   - Unit 7 (Probability and Sampling): 750
4. 2025-26 skill-builder problems on each of Units 4 to 7 by the school the student attended that day, whole problems:
   - TCS-304 Elmswade Academy (6-8): Unit 4 4,070, Unit 5 3,842, Unit 6 3,223, Unit 7 3,282
   - TCS-308 Juniper Shoals Middle School: Unit 4 3,670, Unit 5 3,446, Unit 6 2,930, Unit 7 2,751
   - TCS-316 Calderwick Middle: Unit 4 3,584, Unit 5 3,508, Unit 6 2,968, Unit 7 3,026
   - TCS-322 Gorsedale Middle School: Unit 4 3,468, Unit 5 3,404, Unit 6 2,899, Unit 7 2,907
   - TCS-331 Larkmoor Leadership Academy: Unit 4 3,432, Unit 5 3,080, Unit 6 2,956, Unit 7 2,564
   - TCS-338 Arrowmere Middle School: Unit 4 3,580, Unit 5 3,573, Unit 6 3,001, Unit 7 2,828
   - TCS-342 Ivelbrook Middle School: Unit 4 2,595, Unit 5 2,814, Unit 6 2,459, Unit 7 2,302
   - TCS-351 Fallowmere STEM Middle School: Unit 4 3,034, Unit 5 3,029, Unit 6 2,713, Unit 7 2,498
   - TCS-356 Quillon Heights Middle School: Unit 4 2,448, Unit 5 2,091, Unit 6 2,037, Unit 7 1,796
   - TCS-364 Kettlewyn Middle School: Unit 4 3,001, Unit 5 3,089, Unit 6 2,605, Unit 7 2,481
   - TCS-372 Dovering Magnet Middle School: Unit 4 2,982, Unit 5 3,265, Unit 6 2,719, Unit 7 2,587
   - TCS-379 Hollisgrove Middle: Unit 4 3,498, Unit 5 3,473, Unit 6 3,075, Unit 7 2,967

### spring_reteach_memo.docx

1. Recommends 8-problem sets, with about 3,500 expected failed checks against the 4,100 places, and gives 6 and 10 problems at about 4,500 and 2,750.
2. Explains why the homework record is not carried over: the run-of-three stop and the loss between evenings.

### spring_reteach_forecast.png

1. Stacked bars of expected failed checks by unit at 6, 8 and 10 problems, each labelled with its total (about 4,500, 3,500 and 2,750), the 4,100 places as a dashed line, and the 8-problem bar outlined as the recommendation.
