## Tags

**Domain:** Education & Learning Sciences, multilevel classroom and school research (Strathcorrie Council's S1 to S3 mathematics, the same June common papers in 2025 and 2026, read within each pupil across the units of the paper).  
**Analytical objective:** Root-Cause Analysis (which of five 2025-26 changes cost S1 to S3 pupils the most marks in June 2026).

## 1. Final Recommendation

**Reverse the homework platform switch, Mathsbridge in place of Corvella (change B).** It cost the most marks across the pupils who sat in June 2026: within each pupil, the units they got most wrong in their first homework fell further behind their other units in June 2026 than in June 2025, once review stopped following each pupil's errors and every pupil in a class got the same review. Not the new framework, whose rewritten units fell by less and are four of twelve, nor the asymmetric week, the support bases or the shared posts, each of which reached far fewer pupils.

## 2. Critical Components

1. The fall: the mean mark went from **32.3** to **30.3** out of 60 (4,346 and 4,426 pupils sat), and the share at 36 or more from **42%** to **36%**.
2. The framework and the platform switch began the same day for every pupil, so no comparison between groups of pupils separates them; within each pupil, the units first got most wrong widened their shortfall against the pupil's other units by more than the rewritten units widened theirs, across every school and year group.
3. The partial changes reached far fewer pupils: the asymmetric week **1,491** S3 pupils, the support bases **241** pupils referred to a base, the shared posts **587** pupils in split classes (pupils who sat in June 2026).

## 3. Step-by-Step Solution

1. Pupils who sat each June paper (Attendance P in june_common_paper_marks_2025.csv by Pupil Ref, Status Present in june_common_paper_marks_2026.csv by SCN) joined to the two pupil rolls; marks summed by topic through common_paper_and_unit_map.xlsx, five marks a topic.
2. First-attempt accuracy on each unit's first homework: Corvella Homework rows (CorrectFirstAttempt over Questions, skill to unit through the Corvella skills sheet) and Mathsbridge Unit rows (score_pct, glow_id to SCN through the roll).
3. Each pupil's weak units are their bottom third by that accuracy; per pupil, the share of marks on weak units less the share on the other units, averaged over pupils in each year; the switch's cost is the widening of that shortfall, summed over each pupil's weak units, in marks, over the pupils who sat in 2026.
4. The framework: the rewritten units in section 4 of the change register, the same within-pupil contrast against the other units in each year, its widening in marks over every rewritten unit a sitting pupil took.
5. The week, the bases and the shared posts: June totals adjusted for P7 numeracy (a flag where missing) and free school meals by least squares in each year; reached less not reached (S3 also less the same gap in 2025), over the pupils reached (Base_Referrals above 0; the classes in section 5 of the register); the switch is the largest of the five.
6. Base lessons: sign-ins resolved to S1 to S3 pupils by SCN or by typed name and year (the base's schools where a name repeats), each pupil's own school; the periods from time in to time out on the school's bells (no time out: back at the next bell); maths periods of the class the pupil was in that day on the timetable valid that day, each pupil and period once. The roll and Mathsbridge give the class from January; before it, a pupil's class is the June class most held by the pupils who were set the same review in every autumn week.
7. Teachers per class: timetable codes by term to names on the staff code sheets, names to holders on the establishment (a job-share post's two holders both teach its classes; a leaver on the establishment and the starter after them are two teachers; a name no 2025-26 holder carries is the same teacher as the code that took all its classes in January).

## 4. Deliverable Answers

### maths_change_review.docx

1. Change to reverse: the homework platform switch, Mathsbridge in place of Corvella (18 August 2025).
2. Why each other change cost fewer: the framework's rewritten units fell less than each pupil's weak units and are four of twelve; the asymmetric week reached S3 only; the bases cost the most a pupil but reached 241 pupils; the shared posts reached 587 pupils, from January.
3. Mean June mark: 32.3 (June 2025) and 30.3 (June 2026); share at 36 of 60 or more: 42% and 36%.
4. Chart: each school's mean mark in both years:
   - Ardcorrie Academy: 32.1 and 30.3
   - Balmorran High School: 30.4 and 28.3
   - Glenwhinnie Academy: 33.3 and 31.6
   - Kilbraith Academy: 29.6 and 28.2
   - Lochbrannie High School: 34.9 and 32.2
   - Muirlees High School: 33.7 and 31.2
   - St Moluag's High School: 32.3 and 30.5
   - Torranbrae High School: 32.3 and 30.2

### support_and_staffing_by_school.csv

1. Maths lessons S1 to S3 pupils missed while signed in to a support base, and maths classes with more than one teacher in the session:
   - Ardcorrie Academy: 24 lessons, 6 classes
   - Balmorran High School: 20 lessons, 5 classes
   - Glenwhinnie Academy: 22 lessons, 9 classes
   - Kilbraith Academy: 19 lessons, 7 classes
   - Lochbrannie High School: 15 lessons, 3 classes
   - Muirlees High School: 27 lessons, 12 classes
   - St Moluag's High School: 24 lessons, 3 classes
   - Torranbrae High School: 18 lessons, 5 classes
