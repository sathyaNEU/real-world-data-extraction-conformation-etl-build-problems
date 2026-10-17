## Tags

**Domain:** Education & Learning Sciences (test equating and linking: a retiring state reading test's grade 8 scores placed on the new test's scale through a single-group bridge study).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Fund Kessick Public Schools (1,113), Varlow City Schools (870), Brenmoor County Schools (503), Calderidge Unified School District (472), Garnet Hills School District (372) and Elmorrow Public Schools (368).**
Each count is the applicant's grade 9 and 10 students on the October 1, 2026 roll whose latest grade 8 result is at Level 1, with the 2025 retiring-test scores placed on the new scale by a concordance that matches the two tests' score distributions in the bridge study (retiring scores of 241 and below at Level 1). Harlenbrook, the first left out at 353, trails Elmorrow by 15. Not the slate that places each 2025 score at its regression prediction (231 and below), which funds Harlenbrook in Elmorrow's place: the regression line is flatter than the line linking the scales, so it puts 11.1 per cent of the bridge students at Level 1 against 15.7 per cent on the new test itself.

## 2. Critical Components

1. Retiring-test grade 8 scores placed at Level 1 on the new scale: **241 and below** (the new test's Level 2 begins at 2415).
2. Students at Level 1 in Elmorrow, the sixth: **368**; in Harlenbrook, the first left out: **353**; the gap: **15**.
3. Bridge students at Level 1 on the new test: **15.7** per cent; placed by the regression: **11.1** per cent.

## 3. Step-by-Step Solution

1. Took the spells in enrollment_october_2026_grades_9_12.csv covering October 1, 2026 (entry on or before it, exit blank or on or after it) in grades 9 and 10 of the fourteen applicants in alp_2027_grant_rules.pdf.
2. Took every grade 8 session with a score from glra_2025_student_results.csv (SCR rows, make-ups included, blank state identifiers filled from calderwood_examinee_id_crosswalk_2025.csv) and slm_2026_student_results.csv (Scored rows), and kept each student's latest.
3. Linked the two scales with the 3,968 pairs of glra_slm_bridge_study_2026.csv by equipercentile matching of the two score distributions; linear linking and every percentile convention give the same placement: retiring scores of 241 and below at Level 1 (new-test scores below 2415).
4. Counted each applicant's students at Level 1 and ranked them; Elmorrow is sixth with 368 and Harlenbrook first left out with 353.
5. Rejected the regression of the new score on the retiring score: placed by it only 11.1 per cent of the bridge students reach Level 1 against 15.7 per cent on the new test, and it funds Harlenbrook.
6. For grade 7, took each applicant's own middle schools from district_directory_2026.xlsx (rows from nonpublic schools in nonpublic_schools_registry_2026.csv left out), the Scored grade 7 rows of slm_2026_student_results.csv, and Level 1 below the grade 7 cut of 2390 adopted in sbe_resolution_2026_22_slm_cut_scores.pdf, not the file's performance level, reported before the Board set the grade 7 cuts.

## 4. Deliverable Answers

### alp_grants_2027.xlsx

1. The six districts funded: Kessick Public Schools, Varlow City Schools, Brenmoor County Schools, Calderidge Unified School District, Garnet Hills School District and Elmorrow Public Schools.
2. Each applicant's grade 9 and 10 students on the October 1, 2026 roll at Level 1:
   - Kessick Public Schools: 1,113
   - Varlow City Schools: 870
   - Brenmoor County Schools: 503
   - Calderidge Unified School District: 472
   - Garnet Hills School District: 372
   - Elmorrow Public Schools: 368
   - Harlenbrook County Schools: 353
   - Dunstree Area Schools: 320
   - Ivelstone Public Schools: 283
   - Jasperton Unified School District: 280
   - Marrowby School District: 264
   - Pemberwick County Schools: 262
   - Saltmarrow Public Schools: 182
   - Ashgrove-Fenley Consolidated Schools: 122
3. The first district left out: Harlenbrook County Schools, 353 students, 15 below Elmorrow Public Schools.
4. Each applicant's grade 7 students at Level 1 in spring 2026 and their share of its grade 7 students with a score:
   - Kessick Public Schools: 532 students, 19.8 per cent
   - Varlow City Schools: 371 students, 17.3 per cent
   - Brenmoor County Schools: 230 students, 16.2 per cent
   - Calderidge Unified School District: 225 students, 16.7 per cent
   - Garnet Hills School District: 168 students, 16.4 per cent
   - Elmorrow Public Schools: 131 students, 7.1 per cent
   - Harlenbrook County Schools: 185 students, 23.5 per cent
   - Dunstree Area Schools: 139 students, 15.5 per cent
   - Ivelstone Public Schools: 137 students, 14.4 per cent
   - Jasperton Unified School District: 149 students, 16.6 per cent
   - Marrowby School District: 136 students, 18.4 per cent
   - Pemberwick County Schools: 89 students, 14.4 per cent
   - Saltmarrow Public Schools: 73 students, 14.2 per cent
   - Ashgrove-Fenley Consolidated Schools: 69 students, 16.2 per cent
5. A horizontal bar chart of the fourteen applicants' students at Level 1 on the Chart sheet, the six funded in dark green and the rest in grey, a dashed line under Elmorrow labelled with the sixth's 368 and the first left out's 353.

### alp_conformed_grade8_reading_2026.csv

1. One row for each of the 31,896 counted students (grade 9 or 10 on an applicant's October 1, 2026 roll with a grade 8 result): the state identifier, district, school, grade, the test and year of the latest grade 8 result, its scale score and its level on the new scale.
2. Students at each level: Level 1 5,764, Level 2 12,448, Level 3 8,700, Level 4 4,984.
