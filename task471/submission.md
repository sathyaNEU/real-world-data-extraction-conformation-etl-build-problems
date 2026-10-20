## Tags

**Domain:** Education & Learning Sciences (item response theory and test equating: a licensing board conforms two scoring contractors' results, its attempt history and its programs' completer lists onto the 2025 reporting scale, equating the 2026 form to the 2025 form through a mixed-format anchor whose rater-scored assignment is put back on the 2025 rating standard).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Five of the sixteen programs fall below 70 per cent and go to formal review in 2027: Eastridge State University (69.0), Harrowgate Teacher Academy (58.1), Linden Valley College (58.5), Statewide Teacher Residency (61.6) and Tarrance University (64.5). The other eleven do not.**  
Their 2025-26 completers' first-attempt pass rates run from 58.1 to 69.0 per cent; the lowest rate among the programs that stay off review is Delacourt University's 72.0. The Form 26A raw passing score is 49. Not the eight programs the anchor gives as Arcwright's raters scored it (raw 52: Delacourt, Marisford and Riverbend added), because WA2, the anchor's written assignment, was read in 2026 by a new scoring team that read its validity papers, June 2025 responses, 0.25 points per read below the scores the 2025 reads gave them, which makes the 2026 cohort look weaker on the anchor than it is; nor the list the twenty shared multiple-choice items alone give (raw 46 or 47: Eastridge comes off it), because the 2026 candidates' weaker writing, which WA2 shows even on the 2025 standard and the shared items do not, is part of the difference the anchor has to carry.

## 2. Critical Components

1. WA2 on the 2025 standard: Arcwright's raters read the 120 WA2 validity papers, June 2025 responses whose two 2025 reads agreed, 958 times, **0.25** points per read below the 2025 score, so each 2026 WA2 score moves up by **0.49** and each 2026 anchor score by **0.98**.
2. The Form 26A raw passing score: **49**. At raw 49 every method's equated Form 25A score is 55.88 to 56.02, which rounds to 56 (scale 240); at raw 48 it is 54.90 to 55.13, which rounds to 55.
3. The programs on review, passers over completers counted: Eastridge State University **160** of **232** (**69.0** per cent); Harrowgate Teacher Academy **50** of **86** (**58.1** per cent); Linden Valley College **31** of **53** (**58.5** per cent); Statewide Teacher Residency **114** of **185** (**61.6** per cent); Tarrance University **107** of **166** (**64.5** per cent); the nearest program above the line, Delacourt University, **149** of **207** (**72.0** per cent).

## 3. Step-by-Step Solution

1. Matched the June 2026 registrations in arcwright_ELI_June2026_scores.csv to educator records through BESL_arcwright_registration_crosswalk_2026.csv and dated each educator's first attempt from BESL_ELI_attempt_history_2019-2026.csv, voided attempts left out (Rule 8.4.3): 3,035 first attempts on Form 25A in June 2025 and 3,215 on Form 26A in June 2026.
2. Scored each first attempt's anchor: the 20 items both forms carry (matched by item ID in ELI_item_maps_25A_26A.xlsx; Form 25A's from the ITEM_SCORES positions in pellmore_ELI_June2025_scores.csv, Form 26A's from arcwright_ELI_June2026_item_responses.csv) plus twice its WA2 score (the two reads summed, or twice a resolution read).
3. Measured Arcwright's raters against the 2025 raters on WA2: the VALIDITY reads of the WA2 papers in arcwright_ELI_June2026_written_assignment_reads.csv against each paper's score on file in arcwright_ELI_June2026_scoring_QC.xlsx (June 2025 responses, the score both 2025 reads gave), 0.25 points per read below it; moved every 2026 WA2 score (two reads) up by 0.49, so the anchor's 2026 reads keep their own rater-to-rater spread and sit at the 2025 standard, as the 2025 anchor scores do.
4. Equated Form 26A to Form 25A on the two first-attempt samples through that anchor (Tucker and Levine at each synthetic-population weight, chained linear and chained equipercentile agree), rounded each equated score and converted it with ELI_Form25A_raw_to_scale.csv: raw 49 is the lowest Form 26A score at a scale score of 240.
5. Took each program's 2025-26 completers from EPP_Title_II_completers_2025-26.xlsx: elementary pathways only, completion dates July 1, 2025 to June 30, 2026, each educator once (Rule 8.4.2).
6. Gave each completer's first attempt at or before June 13, 2026 its result: a June 2026 first attempt passes at raw 49 or more, an earlier one keeps its reported result; completers with no attempt are not counted (8.4.4); programs under 70 per cent go to review (8.4.1).
7. For the 2024-25 completers, took the elementary pathways of program year 2024-25 in BESL_completer_register_2019-20_to_2024-25.csv and matched each to the history by educator ID, and where that record has no attempts, by name and birth date (a completer the program entered under a new educator record); counted first attempts at or before June 14, 2025 and their results.
8. Charted the sixteen 2026 rates against the 70 per cent line, the programs on review highlighted.

## 4. Deliverable Answers

### eli_2027_program_review.xlsx

1. Programs that go to formal review in 2027: **5**: Eastridge State University, Harrowgate Teacher Academy, Linden Valley College, Statewide Teacher Residency and Tarrance University.
2. Form 26A raw passing score: **49**.
3. Each program's 2025-26 completers counted, passers on first attempt and first-attempt pass rate (per cent, one decimal):
   - Ostrander State University: 309 completers, 249 passed, 80.6
   - Whitcombe College: 90 completers, 79 passed, 87.8
   - Delacourt University: 207 completers, 149 passed, 72.0
   - Penhallow College: 80 completers, 62 passed, 77.5
   - Marisford State University: 260 completers, 189 passed, 72.7
   - Quillan College: 61 completers, 54 passed, 88.5
   - Tarrance University: 166 completers, 107 passed, 64.5
   - Hollis Creek College: 67 completers, 53 passed, 79.1
   - Eastridge State University: 232 completers, 160 passed, 69.0
   - Saint Aldric University: 111 completers, 97 passed, 87.4
   - Corriden University: 122 completers, 89 passed, 73.0
   - Linden Valley College: 53 completers, 31 passed, 58.5
   - Statewide Teacher Residency: 185 completers, 114 passed, 61.6
   - Riverbend Teaching Fellows: 129 completers, 98 passed, 76.0
   - Harrowgate Teacher Academy: 86 completers, 50 passed, 58.1
   - Brightwater College: 72 completers, 60 passed, 83.3
4. Each program's 2024-25 completers with a first attempt by June 14, 2025, and their first-attempt pass rate (per cent, one decimal):
   - Ostrander State University: 243 completers, 87.7
   - Whitcombe College: 89 completers, 96.6
   - Delacourt University: 143 completers, 76.2
   - Penhallow College: 60 completers, 85.0
   - Marisford State University: 202 completers, 79.7
   - Quillan College: 40 completers, 80.0
   - Tarrance University: 148 completers, 69.6
   - Hollis Creek College: 52 completers, 69.2
   - Eastridge State University: 188 completers, 70.2
   - Saint Aldric University: 115 completers, 78.3
   - Corriden University: 117 completers, 86.3
   - Linden Valley College: 41 completers, 56.1
   - Statewide Teacher Residency: 153 completers, 75.8
   - Riverbend Teaching Fellows: 113 completers, 72.6
   - Harrowgate Teacher Academy: 65 completers, 53.8
   - Brightwater College: 61 completers, 86.9

### eli_2026_program_pass_rates.png

5. Bar chart of the sixteen programs' 2026 first-attempt pass rates against the 70 per cent line, the five programs on review highlighted.
