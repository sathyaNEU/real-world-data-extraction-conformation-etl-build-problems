## Tags

**Domain:** Education & Learning Sciences (item response theory and test equating).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Form 27A should place students into College Algebra from a raw score of 30 and into Corequisite College Algebra from 19.**
A student at the College Algebra standard is expected to reach 29.5 of the form's 60 scored items and a student at the Corequisite College Algebra standard 18.5, once each unique item is carried from the field-test section it was calibrated in to the positions it takes on Northgate Assess. Not 29 and 18, the scores the bank difficulties give as filed (28.2 and 17.5), which hold every unique item as hard as it was at positions 61 to 70.

## 2. Critical Components

1. Position term of the Rasch model fitted to the 2026 attempts, from the field-test section's mean position (65.5) to Form 27A's (45.5): **0.15** logits
2. Expected raw score on Form 27A at the College Algebra standard (0.20 logits): **29.5**
3. Expected raw score on Form 27A at the Corequisite College Algebra standard (-0.70 logits): **18.5**

## 3. Step-by-Step Solution

1. Converted the Itemstore assembly pool's difficulties from bank units to logits (QPI-TR-2027 section 4) and took Form 27A's anchor block and 40 unique items from qpi_form_27A_assembly.csv.
2. Scored every 2026 response: the Kestrel Testing Suite's response strings against the keys at their version's positions in qpi_forms_26A_26B_layout.csv, and Northgate Assess's item responses at their delivered seq.
3. Fitted the Rasch model with a linear position term to all 2026 responses by marginal maximum likelihood, the anchor block fixed at its bank difficulties and every other item free: 0.15 logits over the 20 positions from the field-test section's mean to Form 27A's.
4. Carried each unique item from the old platform's field-test section (mean position 65.5) to each of positions 21 to 70 on Northgate Assess and averaged its expected score over the shuffle; the anchor block, calibrated in place, kept its bank difficulties.
5. Summed the 60 expected scores at each standard: 29.5 at College Algebra and 18.5 at Corequisite College Algebra.
6. Matched each student across both platforms and both student identifiers on birth date, sex, high school code and registration date, and left out the attempts in sessions qpi_session_review_log_2026.xlsx leaves invalidated.
7. Placed each student on their higher level (the later sitting on a tie) at the college their placing sitting's automatic score report went to in qpi_score_reports_2026-03-01_to_2027-01-31.csv: 8,970 students placed, 3,387 into College Algebra and 2,705 into Corequisite College Algebra, 775 of them sat twice.
8. Set the placement scores at the lowest whole raw scores at or above the expected raw scores (QPI-TR-2027 section 7): College Algebra from 30, Corequisite College Algebra from 19.

## 4. Deliverable Answers

### qpi_placement_review_2027.xlsx

1. Placement scores: College Algebra 30, Corequisite College Algebra 19.
2. Expected raw score at the standard: College Algebra 29.5, Corequisite College Algebra 18.5.
3. Each college from 1 March 2026 to 31 January 2027, whole students (placed; College Algebra; Corequisite College Algebra; sat twice):
   - 01 Ashgrove: 1,155 placed, 488 College Algebra, 356 Corequisite College Algebra, 116 sat twice
   - 02 Bramblewood: 978 placed, 348 College Algebra, 297 Corequisite College Algebra, 89 sat twice
   - 03 Calder Flats: 866 placed, 280 College Algebra, 272 Corequisite College Algebra, 88 sat twice
   - 04 Dellwood: 821 placed, 372 College Algebra, 231 Corequisite College Algebra, 71 sat twice
   - 05 Embervale: 743 placed, 275 College Algebra, 227 Corequisite College Algebra, 61 sat twice
   - 06 Fennimore Ridge: 700 placed, 273 College Algebra, 226 Corequisite College Algebra, 50 sat twice
   - 07 Gorseway: 639 placed, 177 College Algebra, 203 Corequisite College Algebra, 55 sat twice
   - 08 Hartmoor Creek: 599 placed, 250 College Algebra, 158 Corequisite College Algebra, 38 sat twice
   - 09 Iverton Prairie: 554 placed, 191 College Algebra, 170 Corequisite College Algebra, 54 sat twice
   - 10 Juniper Lake: 518 placed, 201 College Algebra, 151 Corequisite College Algebra, 38 sat twice
   - 11 Knollwood: 471 placed, 153 College Algebra, 141 Corequisite College Algebra, 38 sat twice
   - 12 Lowland Mesa: 379 placed, 186 College Algebra, 99 Corequisite College Algebra, 23 sat twice
   - 13 Marlow Fork: 308 placed, 96 College Algebra, 93 Corequisite College Algebra, 32 sat twice
   - 14 Nettlefield: 239 placed, 97 College Algebra, 81 Corequisite College Algebra, 22 sat twice
   - System: 8,970 placed, 3,387 College Algebra, 2,705 Corequisite College Algebra, 775 sat twice

### qpi_form27a_score_conversion.csv

4. Raw scores 0 to 18 Developmental Mathematics (MATH 091), 19 to 29 Corequisite College Algebra (MATH 131 with MATH 031), 30 to 60 College Algebra (MATH 131).

### qpi_form27a_expected_score_curve.svg

5. Form 27A's expected raw score against ability in logits, the two standards marked (0.20 and -0.70) with their expected raw scores (29.5 and 18.5) and placement scores (30 and 19), and the curve from the bank difficulties as filed dashed.
