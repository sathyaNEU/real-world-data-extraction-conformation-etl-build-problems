## Tags
**Domain:** Education & Learning Sciences (text analysis: learners' free-text exit comments coded against a manual).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation
**Our 2027 retention budget line should target caring responsibilities.**
Caring responsibilities account for 25.1 per cent of 2025/26 withdrawals against work hours clash at 19.4, a gap of 5.7 points. Not work hours clash, which leads the coded counts at 24.4 per cent only because 14.8 per cent of the comments coded to it are about caring. Not other or not stated, which leads the moderation file's own mix only because every comment coded OT is moderated.

## 2. Critical Components
1. Coded shares of the 17,231 withdrawals: work hours clash **24.4** per cent, caring responsibilities **19.4**
2. Of the moderated comments coded work hours clash, **14.8** per cent belong to caring responsibilities
3. Share of withdrawals that happened for caring responsibilities **25.1** per cent, for work hours clash **19.4**

## 3. Step-by-Step Solution
1. Stacked withdrawals_autumn_winter_2025.csv and withdrawals_spring_summer_2026.json on the spring export's term codes, kept one row per withdrawal reference (the late-keyed winter withdrawals sit in both) and normalised the typed reason codes: 17,231 withdrawals.
2. Counted the withdrawals by coded reason over the four terms: work hours clash 24.4 per cent, caring responsibilities 19.4.
3. Took, within each coded reason in coding_moderation_2025_26.csv, the split of the moderating coder's categories, the return being drawn by code as quality_assurance_procedure.pdf sets out: 14.8 per cent of moderated work hours clash comments belong to caring responsibilities.
4. Carried each code's split onto that code's share of the year's withdrawals and summed by reason: caring responsibilities 25.1 per cent, work hours clash 19.4.
5. Built learner-courses from enrolments_2025_26.csv at the five centres in site_directory.csv on the learner number and the course reference, linking each course that course_catalogue_2025_26.csv plans over winter and spring but which has no spring rows to the one spring course at the same centre whose learners are all its continuing learners (25 links), and summed each learner-course's planned hours once from the catalogue: six area totals.
6. Attributed each learner-course to the centre of its first term's row and counted it completed where any of its rows reads completed: five started counts and five completed shares.
7. Named the reason with the largest share of withdrawals: caring responsibilities, 5.7 points ahead of work hours clash.

## 4. Deliverable Answers

### withdrawal_reason_composition_2025_26.csv
1. Share of 2025/26 withdrawals that happened for each reason, six rows, per cent to one decimal place:
   - Caring responsibilities: 25.1
   - Work hours clash: 19.4
   - Course too difficult: 15.5
   - Travel or transport: 14.7
   - Health: 13.5
   - Other or not stated: 11.8

### retention_target_2027.xlsx
1. Reason the 2027 retention budget line targets: caring responsibilities, 25.1 per cent
2. Runner-up: work hours clash, 19.4 per cent
3. Gap between them: 5.7 points
4. Bar chart of the six shares by reason on the Reason composition sheet, caring responsibilities picked out
5. Planned guided hours of the learner-courses the five centres started in 2025/26, by curriculum area, whole hours:
   - English and maths: 832,566
   - Digital skills: 734,640
   - ESOL: 749,682
   - Health and social care: 756,246
   - Business administration: 726,420
   - Construction skills: 687,663
6. Learner-courses started in 2025/26 and the share of them that completed, by centre, per cent to one decimal place:
   - Cassgrove: 11,468 started, 64.6 completed
   - Hollowdean Learning Hub: 12,849 started, 64.1 completed
   - Northmarket Centre: 17,228 started, 65.5 completed
   - The Lathe Street Building: 15,857 started, 64.7 completed
   - Wyebrook Adult Learning Centre: 11,749 started, 63.9 completed
