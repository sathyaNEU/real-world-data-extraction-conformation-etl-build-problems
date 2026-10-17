## Tags

**Domain:** Sociology & Demography, event history and life course analysis (how many of Quenlow County Community College's nine associate-degree programs go into review in June 2027, by each program's three-year completion share for its fall 2023, 2024 and 2025 entering students, estimated as the cumulative incidence of the degree with transfer out and withdrawal as competing endings and the admissions still open censored).
**Analytical objective:** Descriptive & Distribution Analysis (how each program's entering students are distributed across the ways their admission ends, and when, over the nine terms after entry).

## 1. Final Recommendation

**Six of the nine programs go into review in June 2027: General Studies, Biological Sciences, Business Administration, Psychology, Medical Assisting and Early Childhood Education.**
Their three-year completion shares are 20.9, 24.9, 22.2, 25.9, 26.2 and 19.5 per cent, below the policy's 30 per cent floor, while Criminal Justice (32.5), HVAC-R Technology (44.4) and Nursing (36.7) are above it. Not one program, Early Childhood Education alone, from one minus a Kaplan-Meier curve of the time to the degree, which censors students who transferred out or withdrew as if they could still earn it and puts the transfer-oriented programs at 35 to 41 per cent. Not seven with Criminal Justice (26.8 per cent), from the fall 2023 class alone, which leaves out the two classes the policy includes. Not eight, from degrees so far over all entrants, which counts the students still enrolled as non-completers.

## 2. Critical Components

1. General Studies **20.9 per cent**, Biological Sciences **24.9 per cent**, Business Administration **22.2 per cent** and Psychology **25.9 per cent** of entering students with an associate degree within nine terms, transfer out and withdrawal ending the admission without it
2. Medical Assisting **26.2 per cent** and Early Childhood Education **19.5 per cent**
3. Criminal Justice **32.5 per cent**, HVAC-R Technology **44.4 per cent** and Nursing **36.7 per cent**

## 3. Step-by-Step Solution

1. Stacked the three sheets of ir_fall_entering_students_2023-2025.xlsx (5,292 students) on the current system's numbers, program codes and term codes, fall 2023's legacy ones carried through sis_conversion_student_id_map_2024.txt, program_register_2026-27.xlsx and term_calendar_2018-2027.xlsx, each student in the program entered (the policy, section 3).
2. Took each student's admission at entry from sis_admissions_exits_202410-202720.csv: the exit term and reason (GR degree, TO transfer out, WD withdrawal) or no exit for an admission still open at the end of spring 2027, and removed the 5 students who died (DC).
3. Counted terms from the fall of entry (term 1, summer terms included) to the exit term; the fall 2024 class is observed to its eighth term and the fall 2025 class to its fifth.
4. Estimated each program's cumulative incidence of the degree to the ninth term, term by term the degrees over the admissions still open times the share still open, with TO and WD as competing endings and open admissions censored after spring 2027: General Studies 20.9, Biological Sciences 24.9, Business Administration 22.2, Psychology 25.9, Medical Assisting 26.2, Early Childhood Education 19.5, Criminal Justice 32.5, HVAC-R Technology 44.4 and Nursing 36.7 per cent.
5. Sent the programs below 30 per cent into review (the policy, section 3): six.
6. Summed each fall2026_census_registrations.csv row registered at the census (RE, RW and WC) at its section's Cr Hrs in fall2026_section_schedule.xlsx (laboratory, shop and clinical sections carry none), by the student's program in effect for fall 2026 in program_of_record_history.csv, and divided by 15 (the policy, section 4).
7. Counted each program's classes from the active sections of the subjects the register's Subjects sheet gives it, sections with one instructor, days and start time taken as one class with their census registrations added, and kept those under ten (the policy, section 4).

## 4. Deliverable Answers

### program_completion_review_2027.xlsx

1. Each program's three-year completion share and whether it goes into review:
   - General Studies: 20.9 per cent, goes into review
   - Biological Sciences: 24.9 per cent, goes into review
   - Business Administration: 22.2 per cent, goes into review
   - Psychology: 25.9 per cent, goes into review
   - Medical Assisting: 26.2 per cent, goes into review
   - Early Childhood Education: 19.5 per cent, goes into review
   - Criminal Justice: 32.5 per cent, stays out of review
   - Heating, Ventilation, Air Conditioning and Refrigeration Technology (HVAC-R): 44.4 per cent, stays out of review
   - Nursing: 36.7 per cent, stays out of review
2. Each program's full-time-equivalent enrolment at the fall 2026 census:
   - General Studies: 1,164.1
   - Biological Sciences: 358.0
   - Business Administration: 531.7
   - Psychology: 404.0
   - Medical Assisting: 386.6
   - Early Childhood Education: 343.6
   - Criminal Justice: 397.1
   - HVAC-R Technology: 274.5
   - Nursing: 538.3
3. Each program's classes of its own courses that ran in fall 2026 with fewer than ten students at the census:
   - General Studies: 1
   - Biological Sciences: 14
   - Business Administration: 5
   - Psychology: 5
   - Medical Assisting: 9
   - Early Childhood Education: 3
   - Criminal Justice: 3
   - HVAC-R Technology: 13
   - Nursing: 78

### completion_review_board_paper_2027.pdf

1. The board paper recommending the six programs for review, with a step chart of each program's share of entering students holding an associate degree by term over the nine terms after entry and the 30 per cent floor marked as a dotted line.
