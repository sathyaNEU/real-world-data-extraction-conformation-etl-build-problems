## Tags

**Domain:** Education and learning sciences, learning analytics and early-warning models.  
**Analytical objective:** Forecasting and predictive modeling.

## 1. Final Recommendation

**Plan for about 3,250 of the 8,659 first-time entrants enrolled at the 1 October 2026 census not to be enrolled at the 1 October 2027 census, to the nearest 250.**
The figure reads each entrant's chance at the number of other entrants met in two or more of the entrant's own Semester 1 classes, and 3,778 of the 2026 entrants meet no other entrant twice. Not an early-warning model on entrant attributes and week-6 ratings alone, validated on intakes in which most full-time entrants shared three classes with the same 27 others. Not the earlier intakes' rate, for the same reason.

## 2. Critical Components

1. First-time entrants enrolled at the 1 October 2026 census: **8,659**
2. 2026 entrants who meet no other entrant in two or more of their classes: **3,778**

## 3. Step-by-Step Solution

1. Took each intake's first-time entrants (Entry Basis First-time) from admissions_entrants_2019_2026.xlsx with an enrolled attempt at their own census in census_enrolments_2019_2026.csv: 8,659 in 2026.
2. Marked each 2019 to 2025 entrant not enrolled at the next census when no EN or Enrolled attempt is there (leave is not enrolled, per the conventions), the 2025 intake through sirius_arc_student_crosswalk.csv.
3. Counted for every entrant the other entrants of the same intake met in two or more of the entrant's Semester 1 classes (sirius_fy_cohort_classes_2019_2025.csv by term and class number, arc_s1_2026_first_year_classes.csv by class code): 3,778 of the 2026 entrants meet none.
4. Fitted a logistic model of not being enrolled at the next census on the 2019 to 2025 entrants: ASC points, first in family, part-time, aged 21 or over, hardship grant, mean week-6 rating (Satisfactory 0, Some concern 1, At risk 2), living-learning community, hall, offer acceptance day, faculty, and that count in bands of 0, 1, 2, 3, 4 to 5, 6 to 8, 9 to 14, 15 to 21 and 22 or more.
5. Counted Semester 1 2026 teaching groups in s1_2026_class_timetable.xlsx: active classes meeting in the same room on the same day, start and teaching weeks are one group whatever teacher of record each lists, a group's size is its classes' census enrolments added, by owning faculty.
6. Counted students in year of study 2 or later with an enrolled attempt at the 2026 census once each: a student whose two attempts match a transfer in programme_transfers_2025_2026.csv is in the transfer's new programme, other two-attempt students are conjoint and go to the combination's first-listed programme in programme_catalogue_2026.csv.
7. Applied the model to the 2026 entrants and summed their probabilities: 3,269.3, about 3,250 to the nearest 250.

## 4. Deliverable Answers

### continuing_enrolment_2027.xlsx

1. First-time entrants enrolled at the 1 October 2026 census not enrolled at the 1 October 2027 census: **3,250** (nearest 250)
2. Semester 1 2026 teaching groups and groups of more than 30 students at the census, by faculty:
   - Arts and Social Sciences: **703** groups, **82** of them over thirty students
   - Business and Law: **325** groups, **84** of them over thirty students
   - Science: **315** groups, **76** of them over thirty students
   - Engineering and Computing: **250** groups, **65** of them over thirty students
   - Health Sciences: **269** groups, **62** of them over thirty students
3. Students in their second, third, and fourth or later year of study enrolled at the 1 October 2026 census, by faculty:
   - Arts and Social Sciences: second year **1,734**, third year **1,401**, fourth year or later **429**
   - Business and Law: second year **1,621**, third year **1,426**, fourth year or later **666**
   - Science: second year **1,517**, third year **1,253**, fourth year or later **351**
   - Engineering and Computing: second year **1,121**, third year **1,029**, fourth year or later **803**
   - Health Sciences: second year **1,336**, third year **1,147**, fourth year or later **351**

### s1_2026_teaching_groups.png

1. One stacked bar per faculty, groups of 30 students or fewer and groups of more than 30, each segment labelled with its count as in answer 2 above.
