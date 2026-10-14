# task450 submission

## Tags

**Domain:** Education & Learning Sciences, item response theory and test equating (a new grade-5 form placed on the district's reporting scale through the items it shares with the 2025 form, the shared items screened for a change in difficulty between the two cohorts before the link, the cohorts not equivalent).
**Analytical objective:** Data Extraction & Conformation (ETL) (two years of item-response exports in two layouts, the item bank and its key correction, the student information system's enrollment history and id merges, the platform's registrations and the campus directory conformed into each campus's 2026 results on the reporting scale).

## 1. Final Recommendation

**Place the 2027 mathematics intervention coaches at the 15 campuses where fewer than 40 per cent of tested full-academic-year grade-5 students met the standard: Wolfberry Trail (12.9), Javelina Run (16.4), Arriaga (25.0), Sotol Mesa (27.7), Rosedale Terrace (28.1), Gallardo (29.9), Caliche Ridge (33.3), Old Mill Road (33.6), Agarita Bend (33.6), Ursuline Avenue (34.3), Lechuguilla Gap (34.4), Tobar (34.7), Guayacan Hill (35.9), Mabry (36.4) and Vance Avenue (36.8) per cent.**

The deciding figure is the 2026 form's passing raw score, 25: linked to the 2025 scale through the 22 shared items whose difficulty held between the cohorts (the 2026 cohort averaged 11.08 on them against 10.69), a 2026 raw score of 25 converts to a scale score of 300 or above. Items 3, 11 and 35, written to TEKS 5.4F, are set aside: the 2026 students answered them correctly 79.1, 75.1 and 77.4 per cent of the time against 51.3, 45.8 and 47.4 in 2025, while the other 22 rose from 48.6 to 50.4 per cent. Not the link through all 25 shared items: it credits those three items' rise to the whole cohort, puts the passing raw score at 24 or below, depending on the method, and designates 13 or fewer campuses. Not the 2025 conversion applied to the 2026 raw scores: it keeps the passing raw score at 27 and designates 32. Not equating that matches the 2026 score distribution to 2025's: it assumes the two cohorts alike, puts the passing raw score at 26 and designates 23.

## 2. Critical Components

1. The 2026 form's passing raw score is **25**: a raw score of 25 converts to a scale score of 300 or above and 24 to less.
2. The link runs through **22** of the 25 shared items: items **3, 11 and 35** (TEKS 5.4F) are set aside, every standard screen flagging the same three.
3. **5,727** full-academic-year students tested at the **54** rated campuses and **2,745** met the standard (**47.9** per cent).
4. Tobar Elementary, counted with Delgadillo Elementary's students, is at **34.7** per cent (61 of 176).

## 3. Step-by-Step Solution

1. Scored each 2025 answer with the item bank's 2025 keys and each 2026 answer with its 2026 keys, item M547961 with key B as the notice of 19 May 2026 corrects the bank's C, blank and multiple-marked answers zero (technical report section 3): 6,554 tests in 2025 and 6,341 in 2026.
2. Found the 25 items both forms carry in the same positions (dma_item_bank_grade5_math.xlsx) and compared each one's difficulty across the years (the change in Rasch difficulty, Mantel-Haenszel and the delta plot agree): items 3, 11 and 35, all TEKS 5.4F, rose from 51.3, 45.8 and 47.4 to 79.1, 75.1 and 77.4 per cent correct while the other 22 rose from 48.6 to 50.4, so those three are set aside.
3. On the 22 that held, the 2026 cohort averaged 11.08 against 10.69 in 2025 while its mean on the whole form fell from 24.97 to 24.07, so the cohorts differ and the new items are harder; linked the 2026 form to the 2025 form through them (chained equipercentile; Tucker, Levine, frequency estimation and Rasch true-score linking give the same passing raw score) and converted with the 2025 conversion (141 + 6 x raw score, whole numbers, technical report 4.1): a 2026 raw score of 25 reaches 300, 24 does not.
4. Placed each 2026 test with its student through dma_registrations_2026.csv and each student at a full-academic-year campus through sis_grade5_enrollment_2025-26.csv (designation rule 3): 5,727 tested full-academic-year students.
5. Counted Delgadillo Elementary's students with Tobar Elementary (rule 5) and left Vereda Elementary unrated with 8 students (rule 6): 54 rated campuses.
6. Rated each campus as its students meeting the standard over its students tested (rule 4) and designated those under 40 per cent (rule 7): 15 campuses.
7. For the asks, placed each 2025 test by the campus name grade5_math_responses_2025.csv records (its campus codes are the old system's and name other campuses in campus_directory_2026-27.xlsx) and counted students enrolled in the testing window with no 2026 result once sis_student_id_merges_2026.csv joins each student's ids.
8. Recommendation: place the 2027 coaches at the 15 campuses.

## 4. Deliverable Answers

### intervention_schools_2027.docx

1. The 15 campuses designated for 2027 mathematics intervention coaching, with each one's share of tested full-academic-year grade-5 students meeting the standard:
   - Wolfberry Trail Elementary: 12.9%
   - Javelina Run Elementary: 16.4%
   - Arriaga Elementary: 25.0%
   - Sotol Mesa Elementary: 27.7%
   - Rosedale Terrace Elementary: 28.1%
   - Gallardo Elementary: 29.9%
   - Caliche Ridge Elementary: 33.3%
   - Old Mill Road Elementary: 33.6%
   - Agarita Bend Elementary: 33.6%
   - Ursuline Avenue Elementary: 34.3%
   - Lechuguilla Gap Elementary: 34.4%
   - Tobar Elementary: 34.7%
   - Guayacan Hill Elementary: 35.9%
   - Mabry Elementary: 36.4%
   - Vance Avenue Elementary: 36.8%
2. Bar chart of every rated campus's share against the 40 per cent line, the 15 designated campuses in dark bars, on page 1 of the memo.

### grade5_math_results_2026.xlsx

3. Every rated campus's full-academic-year students tested and meeting the standard, and the share, in the workbook's order:
   - Agarita Bend Elementary: 116 tested, 39 met, 33.6%
   - Alameda Park Elementary: 138 tested, 63 met, 45.7%
   - Arriaga Elementary: 132 tested, 33 met, 25.0%
   - Ashe Juniper Elementary: 129 tested, 59 met, 45.7%
   - Barrow Street Elementary: 103 tested, 63 met, 61.2%
   - Bramble Ford Elementary: 130 tested, 56 met, 43.1%
   - Caliche Ridge Elementary: 66 tested, 22 met, 33.3%
   - Cenizo Flat Elementary: 105 tested, 59 met, 56.2%
   - Chinaberry Lane Elementary: 149 tested, 62 met, 41.6%
   - Cottonwood Draw Elementary: 90 tested, 74 met, 82.2%
   - Coyote Tank Elementary: 145 tested, 94 met, 64.8%
   - Dewberry Terrace Elementary: 124 tested, 56 met, 45.2%
   - Elmhurst Avenue Elementary: 137 tested, 57 met, 41.6%
   - Encino Grove Elementary: 106 tested, 45 met, 42.5%
   - Fairlane Elementary: 75 tested, 32 met, 42.7%
   - Farias Elementary: 75 tested, 34 met, 45.3%
   - Gallardo Elementary: 137 tested, 41 met, 29.9%
   - Granjeno Crossing Elementary: 112 tested, 47 met, 42.0%
   - Guayacan Hill Elementary: 103 tested, 37 met, 35.9%
   - Hackberry Slough Elementary: 108 tested, 48 met, 44.4%
   - Hargis Elementary: 138 tested, 79 met, 57.2%
   - Horsemint Meadow Elementary: 97 tested, 42 met, 43.3%
   - Huisachito Elementary: 100 tested, 75 met, 75.0%
   - Indigo Prairie Elementary: 113 tested, 63 met, 55.8%
   - Ironwood Point Elementary: 109 tested, 47 met, 43.1%
   - Javelina Run Elementary: 55 tested, 9 met, 16.4%
   - Jessamine Elementary: 68 tested, 39 met, 57.4%
   - Kidneywood Knoll Elementary: 74 tested, 46 met, 62.2%
   - Lantana Loop Elementary: 121 tested, 89 met, 73.6%
   - Larkin Street Elementary: 146 tested, 74 met, 50.7%
   - Lechuguilla Gap Elementary: 64 tested, 22 met, 34.4%
   - Mabry Elementary: 140 tested, 51 met, 36.4%
   - Mustang Grape Elementary: 143 tested, 106 met, 74.1%
   - Nopalito Vista Elementary: 71 tested, 31 met, 43.7%
   - Northgate Elementary: 126 tested, 97 met, 77.0%
   - Old Mill Road Elementary: 143 tested, 48 met, 33.6%
   - Orozco Elementary: 74 tested, 33 met, 44.6%
   - Pinto Mesa Elementary: 76 tested, 49 met, 64.5%
   - Retama Hollow Elementary: 126 tested, 65 met, 51.6%
   - Riojas Elementary: 87 tested, 60 met, 69.0%
   - Rosedale Terrace Elementary: 114 tested, 32 met, 28.1%
   - Sandbur Flat Elementary: 82 tested, 46 met, 56.1%
   - Sotol Mesa Elementary: 65 tested, 18 met, 27.7%
   - Switchgrass Bend Elementary: 82 tested, 36 met, 43.9%
   - Tasajillo Draw Elementary: 65 tested, 34 met, 52.3%
   - Tepeguaje Draw Elementary: 131 tested, 61 met, 46.6%
   - Tobar Elementary: 176 tested, 61 met, 34.7%
   - Upland Prairie Elementary: 55 tested, 35 met, 63.6%
   - Ursuline Avenue Elementary: 67 tested, 23 met, 34.3%
   - Vance Avenue Elementary: 117 tested, 43 met, 36.8%
   - Windmill Hill Elementary: 100 tested, 54 met, 54.0%
   - Wolfberry Trail Elementary: 132 tested, 17 met, 12.9%
   - Ximenez Elementary: 92 tested, 67 met, 72.8%
   - Yucca Bloom Elementary: 98 tested, 72 met, 73.5%
4. Grade-5 students who took the 2025 test and the share who met the standard, by learning community:
   - North: 1,431 took it, 56.8%
   - Central: 1,408 took it, 41.2%
   - East: 1,184 took it, 38.2%
   - South: 1,172 took it, 36.2%
   - West: 1,359 took it, 49.3%
5. Grade-5 students enrolled at some time in the 2026 testing window with no 2026 result:
   - North: 18
   - Central: 25
   - East: 18
   - South: 19
   - West: 18
   - District: 98
