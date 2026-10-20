# leak check, task270

**Verdict: REVIEW.** 15 files read, 33 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: patient, sitting, sittings, thurlwick, quarndale, change, second, reader, record, completed, window, mosswick, random, penwardine, recorded, asserted, period, decisive, produces, nothing, claims, architecture, slopes, checks, routes

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `contents.txt`: carries 4 of 7 distinctive words of the committed call: 'The Research Committee should name Quarndale and Thurlwick as the recruiting sites for ARV-1102.'
- **REVIEW** `site_selection_paper_RC-26-11.pdf`: carries 7 of 7 distinctive words of the committed call: 'The Research Committee should name Quarndale and Thurlwick as the recruiting sites for ARV-1102.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `arvenna_site_feasibility_questionnaire.pdf`: 4 of 25 stump-paragraph terms appear (patient, record, random, recorded); read whether the document names the move
- **REVIEW** `contents.txt`: 3 of 25 stump-paragraph terms appear (patient, record, recorded); read whether the document names the move
- **REVIEW** `mas_data_guide_2026.pdf`: 4 of 25 stump-paragraph terms appear (patient, record, completed, recorded); read whether the document names the move
- **REVIEW** `site_selection_paper_RC-26-11.pdf`: 10 of 25 stump-paragraph terms appear (patient, thurlwick, quarndale, change, record, completed); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Isolated readers (stage 4)

- Round 1 (target.zip e137a4a3, the outcome unfiled): two scored readers, both missed the call (Thurlwick and Penwardine by the slope through every sitting) and Ask A; both took Ask B 16 of 16 (`score_reader.py` exit 1 on the first clinic below and on 50 per cent of the ask figures). Repaired in one pass.
- Round 2 (target.zip d6f415d7, 3.1 filing that a change the test itself produces is not part of the rate): both readers landed the call, Quarndale and Thurlwick, each estimating the one-time gain of a second completed sitting within patients over the whole record at about 2.5; reader 3 Ask B 16 of 16 and Ask A 0 of 16, reader 4 32 of 32. `score_reader.py` FAIL on both (the call): Gate F failed, architecture 3 spent, task270 retired.
