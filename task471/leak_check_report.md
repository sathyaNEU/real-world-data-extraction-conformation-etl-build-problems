# leak check, task471

**Verdict: REVIEW.** 17 files read, 57 golden figures and 17 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: anchor, scored, standard, equating, assignment, validity, papers, scores, raters, method, scoring, report, written, asserted, decisive, window, sample, reader, dropped, population, cohort, judged, technical, contractor, measured

## 3 answer figures in the pack (REVIEW 13)
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 70.2 appears: ...(%) WA1 55.5 96.3 3.7 68.0 99.3 WA2 57.2 96.9 3.1 70.2 99.3 WA3 58.2 96.8 3.2 72.2 99.8 4. Equating Form...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 189 appears: ...cale 38 178 93 294 39 182 94 294 40 185 95 295 41 189 96 295 42 192 97 296 43 196 98 296 44 200 99 296...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 153 appears: ...287 27 145 82 287 28 148 83 288 29 151 84 289 30 153 85 290 31 156 86 290 32 159 87 291 33 162 88 292...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 243 appears: ...cale Raw Scale 0 108 55 237 1 109 56 240 2 109 57 243 3 110 58 246 4 111 59 249 5 112 60 251 6 112 61 2...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 249 appears: ...7 1 109 56 240 2 109 57 243 3 110 58 246 4 111 59 249 5 112 60 251 6 112 61 254 7 113 62 256 8 114 63 2...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 111 appears: ...8 55 237 1 109 56 240 2 109 57 243 3 110 58 246 4 111 59 249 5 112 60 251 6 112 61 254 7 113 62 256 8 1...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 115 appears: ...2 60 251 6 112 61 254 7 113 62 256 8 114 63 259 9 115 64 261 10 116 65 263 11 117 66 265 12 118 67 267...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 143 appears: ...283 23 136 78 284 24 138 79 285 25 141 80 286 26 143 81 287 27 145 82 287 28 148 83 288 29 151 84 289...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 107 appears: ...217 104 297 50 221 105 297 51 224 106 298 52 227 107 298 53 231 108 298 54 234...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 185 appears: ...aw Scale Raw Scale 38 178 93 294 39 182 94 294 40 185 95 295 41 189 96 295 42 192 97 296 43 196 98 296...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 117 appears: ...62 256 8 114 63 259 9 115 64 261 10 116 65 263 11 117 66 265 12 118 67 267 13 120 68 269 14 121 69 271...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: golden figure 122 appears: ...265 12 118 67 267 13 120 68 269 14 121 69 271 15 122 70 273 16 124 71 274 17 125 72 276 18 127 73 277...
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: and 4 more golden figures

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `Arcwright_ELI_June2026_Administration_Summary.pdf`: 7 of 25 stump-paragraph terms appear (scored, standard, assignment, scores, raters, scoring); read whether the document names the move
- **REVIEW** `BESL_ELI_Framework_2024.pdf`: 5 of 25 stump-paragraph terms appear (scored, standard, assignment, scoring, written); read whether the document names the move
- **REVIEW** `BESL_OAR_Form26A_Assembly_Memo.pdf`: 9 of 25 stump-paragraph terms appear (anchor, standard, assignment, validity, papers, scores); read whether the document names the move
- **REVIEW** `BESL_Program_Review_Standard_2027.pdf`: 4 of 25 stump-paragraph terms appear (standard, scoring, report, contractor); read whether the document names the move
- **REVIEW** `Pellmore_ELI_Technical_Report_June2025_Form25A.pdf`: 13 of 25 stump-paragraph terms appear (anchor, standard, equating, assignment, validity, papers); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 1)
- **REVIEW** `EPP_Title_II_completers_2025-26.xlsx`: names 16 of 17 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `BESL_EPP_directory_2026.csv`: names 16 of 17 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

### Architecture 2, round 1 (target.zip 14b337c337f9190b)

Two isolated readers (general-purpose, Sonnet, medium effort), each on its own fresh unzip with prompt.txt only, each
scored with score_reader.py before its verdict was read.

**Reader 1a.** Four programs to review (Harrowgate, Linden Valley, Statewide, Tarrance), raw 47.
- It measured the WA2 validity shift (about 0.25 per read), dropped WA2 from the anchor and equated by Tucker on the 20
  shared items.
- It built the 2024-25 sheet on the register's educator IDs.
- score_reader: call 0 of 1, ask 0 of 32, exit 0.
- Answers: 1 none as one sentence (nearest: the memo's equating sentence, the technical report's design, the QC notes);
  2 none; 3 the conversion CSV; 4 none; 5 Rule 8.4.3 to 8.4.5, which fix the population, window and pass line but not the
  equating; 6 an analytical choice.
- REVIEW lines: all harmless.

**Reader 1b.** Three programs to review (Harrowgate, Linden Valley, Statewide), raw 46.
- It took the same drop-WA2 route, choosing 46 because Levine, frequency-estimation and chained equipercentile agreed.
- It used the same ID join for the 2024-25 sheet.
- score_reader: call 0 of 1, ask 0 of 32, exit 0.
- Answers: 1 none; 2 none; 3 the conversion, item map and crosswalk files, and the QC validity sheet and notes line;
  4 none; 5 the rules and the technical report's section 4; 6 an analytical choice, "partly a planted-looking signal".
- REVIEW lines: all harmless.

**Verdict on this pack.** The readers held: both missed the call on the drop-WA2 rung, and both missed every ask figure.
The judge (run v2r1) returned DETERMINISTIC on the main call with disposition SEND_BACK on Gate G (planted_defect_flip,
sole_data_defect yes), so architecture 2 is spent and this pack does not ship.
