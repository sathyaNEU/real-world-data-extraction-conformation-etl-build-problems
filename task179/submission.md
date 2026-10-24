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
4. Fitted logistic models of not being enrolled at the next census on the 2019 to 2025 entrants (ASC points, first in family, part-time, aged 21 or over, hardship grant, mean week-6 rating with Satisfactory 0, Some concern 1 and At risk 2, living-learning community, hall, offer acceptance day, faculty) with that count in several forms, and kept the lowest Akaike information criterion, per the conventions: a flag for meeting 10 or more other entrants twice.
5. Applied it to the 2026 entrants and summed their probabilities: 3,253.0, about 3,250 to the nearest 250.
6. Counted Semester 1 2026 teaching groups at 200 level and above from s1_2026_class_timetable.xlsx: each distinct set of active classes meeting together in one room on the same day, start and teaching weeks is one group however often it meets, so two classes that share only one of their meetings make three groups (the two at the shared meeting and each at its own); a group's size is the students its classes list in arc_s1_2026_class_enrolments.csv who hold an enrolled programme attempt at the 2026 census in the census history, so places still held by students on approved leave or with no 2026 attempt are not counted (ARC Scheduling's Enrolled at Census counts them, and shows a combination's two classes together on each).

## 4. Deliverable Answers

### continuing_enrolment_2027.xlsx

1. First-time entrants enrolled at the 1 October 2026 census not enrolled at the 1 October 2027 census: **3,250** (nearest 250)
2. Semester 1 2026 teaching groups by faculty and level, with 30 students or fewer and with more than thirty at the census:
   - Arts and Social Sciences, 200 level: **14** with thirty or fewer, **40** with more than thirty
   - Arts and Social Sciences, 300 level and above: **20** with thirty or fewer, **45** with more than thirty
   - Business and Law, 200 level: **15** with thirty or fewer, **39** with more than thirty
   - Business and Law, 300 level and above: **22** with thirty or fewer, **46** with more than thirty
   - Science, 200 level: **15** with thirty or fewer, **39** with more than thirty
   - Science, 300 level and above: **22** with thirty or fewer, **38** with more than thirty
   - Engineering and Computing, 200 level: **18** with thirty or fewer, **33** with more than thirty
   - Engineering and Computing, 300 level and above: **25** with thirty or fewer, **34** with more than thirty
   - Health Sciences, 200 level: **17** with thirty or fewer, **36** with more than thirty
   - Health Sciences, 300 level and above: **25** with thirty or fewer, **32** with more than thirty

### s1_2026_teaching_groups.png

1. One stacked bar per faculty and level, groups of 30 students or fewer and of more than 30, each segment labelled with its count as in answer 2 above.
