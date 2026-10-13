# task450 submission

## Tags

**Domain:** Education & Learning Sciences, item response theory and test equating (a new grade-5 form placed on the district's reporting scale through the items it shares with the 2025 form, the two cohorts not equivalent).
**Analytical objective:** Data Extraction & Conformation (ETL) (two years of item-response exports in two layouts, the item bank and its key correction, the student information system's enrollment history and id merges, the platform's registrations and the campus directory conformed into each campus's 2026 results on the reporting scale).

## 1. Final Recommendation

**Place the 2027 mathematics intervention coaches at the 15 campuses where fewer than 40 per cent of tested full-academic-year grade-5 students met the standard: Wolfberry Trail (13.6), Javelina Run (18.2), Arriaga (25.0), Gallardo (28.5), Rosedale Terrace (29.8), Sotol Mesa (30.8), Guayacan Hill (32.0), Elmhurst Avenue (33.6), Old Mill Road (34.3), Agarita Bend (34.5), Caliche Ridge (34.8), Tobar (35.8), Lechuguilla Gap (35.9), Mabry (36.4) and Vance Avenue (37.6) per cent.**

The deciding figure is the 2026 form's passing raw score, 25: linked to the 2025 scale through the 25 items both forms share, which the 2026 cohort answered better (12.58 against 12.14 on average), a 2026 raw score of 25 converts to a scale score of 300 or above. Not the 2025 conversion applied to the 2026 raw scores: it keeps the passing raw score at 27 and designates 30 campuses. Not equating that matches the 2026 score distribution to 2025's: it assumes the two cohorts alike, puts the passing raw score at 26 and designates 21.

## 2. Critical Components

1. The 2026 form's passing raw score is **25**: a raw score of 25 converts to a scale score of 300 or above and 24 to less.
2. **5,727** full-academic-year students tested at the **54** rated campuses and **2,769** met the standard (**48.3** per cent).
3. Tobar Elementary, counted with Delgadillo Elementary's students, is at **35.8** per cent (63 of 176).

## 3. Step-by-Step Solution

1. Scored each 2025 answer with the item bank's 2025 keys and each 2026 answer with its 2026 keys, item M545945 with key C as the notice of 19 May 2026 corrects the bank's D, blank and multiple-marked answers zero (technical report section 3): 6,554 tests in 2025 and 6,341 in 2026.
2. Found the 25 items both forms carry in the same positions (dma_item_bank_grade5_math.xlsx): the 2026 cohort averaged 12.58 on them against 12.14 in 2025 while its mean on the whole form fell from 24.97 to 24.05, so the cohorts differ and the new items are harder.
3. Linked the 2026 form to the 2025 form through the shared items (chained equipercentile; Tucker, Levine, frequency estimation and Rasch true-score linking give the same passing raw score) and converted with the 2025 conversion (141 + 6 x raw score, whole numbers, technical report 4.1): a 2026 raw score of 25 reaches 300, 24 does not.
4. Placed each 2026 test with its student through dma_registrations_2026.csv and each student at a full-academic-year campus through sis_grade5_enrollment_2025-26.csv (designation rule 3): 5,727 tested full-academic-year students.
5. Counted Delgadillo Elementary's students with Tobar Elementary (rule 5) and left Vereda Elementary unrated with 8 students (rule 6): 54 rated campuses.
6. Rated each campus as its students meeting the standard over its students tested (rule 4) and designated those under 40 per cent (rule 7): 15 campuses.
7. For the asks, placed each 2025 test by the campus name grade5_math_responses_2025.csv records (its campus codes are the old system's and name other campuses in campus_directory_2026-27.xlsx) and counted students enrolled in the testing window with no 2026 result once sis_student_id_merges_2026.csv joins each student's ids.
8. Recommendation: place the 2027 coaches at the 15 campuses.

## 4. Deliverable Answers

### intervention_schools_2027.docx

1. The 15 campuses designated for 2027 mathematics intervention coaching, with each one's share of tested full-academic-year grade-5 students meeting the standard:
   - Wolfberry Trail Elementary: 13.6%
   - Javelina Run Elementary: 18.2%
   - Arriaga Elementary: 25.0%
   - Gallardo Elementary: 28.5%
   - Rosedale Terrace Elementary: 29.8%
   - Sotol Mesa Elementary: 30.8%
   - Guayacan Hill Elementary: 32.0%
   - Elmhurst Avenue Elementary: 33.6%
   - Old Mill Road Elementary: 34.3%
   - Agarita Bend Elementary: 34.5%
   - Caliche Ridge Elementary: 34.8%
   - Tobar Elementary: 35.8%
   - Lechuguilla Gap Elementary: 35.9%
   - Mabry Elementary: 36.4%
   - Vance Avenue Elementary: 37.6%
2. Bar chart of every rated campus's share against the 40 per cent line, the 15 designated campuses in dark bars, on page 1 of the memo.

### grade5_math_results_2026.xlsx

3. Every rated campus's full-academic-year students tested and meeting the standard, and the share, in the workbook's order:
   - Agarita Bend Elementary: 116 tested, 40 met, 34.5%
   - Alameda Park Elementary: 138 tested, 67 met, 48.6%
   - Arriaga Elementary: 132 tested, 33 met, 25.0%
   - Ashe Juniper Elementary: 129 tested, 58 met, 45.0%
   - Barrow Street Elementary: 103 tested, 63 met, 61.2%
   - Bramble Ford Elementary: 130 tested, 54 met, 41.5%
   - Caliche Ridge Elementary: 66 tested, 23 met, 34.8%
   - Cenizo Flat Elementary: 105 tested, 58 met, 55.2%
   - Chinaberry Lane Elementary: 149 tested, 65 met, 43.6%
   - Cottonwood Draw Elementary: 90 tested, 74 met, 82.2%
   - Coyote Tank Elementary: 145 tested, 94 met, 64.8%
   - Dewberry Terrace Elementary: 124 tested, 54 met, 43.5%
   - Elmhurst Avenue Elementary: 137 tested, 46 met, 33.6%
   - Encino Grove Elementary: 106 tested, 48 met, 45.3%
   - Fairlane Elementary: 75 tested, 33 met, 44.0%
   - Farias Elementary: 75 tested, 33 met, 44.0%
   - Gallardo Elementary: 137 tested, 39 met, 28.5%
   - Granjeno Crossing Elementary: 112 tested, 48 met, 42.9%
   - Guayacan Hill Elementary: 103 tested, 33 met, 32.0%
   - Hackberry Slough Elementary: 108 tested, 49 met, 45.4%
   - Hargis Elementary: 138 tested, 79 met, 57.2%
   - Horsemint Meadow Elementary: 97 tested, 41 met, 42.3%
   - Huisachito Elementary: 100 tested, 77 met, 77.0%
   - Indigo Prairie Elementary: 113 tested, 64 met, 56.6%
   - Ironwood Point Elementary: 109 tested, 47 met, 43.1%
   - Javelina Run Elementary: 55 tested, 10 met, 18.2%
   - Jessamine Elementary: 68 tested, 41 met, 60.3%
   - Kidneywood Knoll Elementary: 74 tested, 46 met, 62.2%
   - Lantana Loop Elementary: 121 tested, 88 met, 72.7%
   - Larkin Street Elementary: 146 tested, 78 met, 53.4%
   - Lechuguilla Gap Elementary: 64 tested, 23 met, 35.9%
   - Mabry Elementary: 140 tested, 51 met, 36.4%
   - Mustang Grape Elementary: 143 tested, 105 met, 73.4%
   - Nopalito Vista Elementary: 71 tested, 31 met, 43.7%
   - Northgate Elementary: 126 tested, 96 met, 76.2%
   - Old Mill Road Elementary: 143 tested, 49 met, 34.3%
   - Orozco Elementary: 74 tested, 39 met, 52.7%
   - Pinto Mesa Elementary: 76 tested, 50 met, 65.8%
   - Retama Hollow Elementary: 126 tested, 68 met, 54.0%
   - Riojas Elementary: 87 tested, 61 met, 70.1%
   - Rosedale Terrace Elementary: 114 tested, 34 met, 29.8%
   - Sandbur Flat Elementary: 82 tested, 46 met, 56.1%
   - Sotol Mesa Elementary: 65 tested, 20 met, 30.8%
   - Switchgrass Bend Elementary: 82 tested, 40 met, 48.8%
   - Tasajillo Draw Elementary: 65 tested, 31 met, 47.7%
   - Tepeguaje Draw Elementary: 131 tested, 63 met, 48.1%
   - Tobar Elementary: 176 tested, 63 met, 35.8%
   - Upland Prairie Elementary: 55 tested, 37 met, 67.3%
   - Ursuline Avenue Elementary: 67 tested, 29 met, 43.3%
   - Vance Avenue Elementary: 117 tested, 44 met, 37.6%
   - Windmill Hill Elementary: 100 tested, 52 met, 52.0%
   - Wolfberry Trail Elementary: 132 tested, 18 met, 13.6%
   - Ximenez Elementary: 92 tested, 65 met, 70.7%
   - Yucca Bloom Elementary: 98 tested, 71 met, 72.4%
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
