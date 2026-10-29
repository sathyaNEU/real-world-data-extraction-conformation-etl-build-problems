# leak check, task168

**Verdict: LEAK.** 14 files read, 27 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: demand, pooled, bookings, decisive, completion, holdout, sell-out, sold-out, sentence, changes, section, censored, network, planning, family, months, agency, domain, season, capacity, estimand, record, close-out, asserted, records

## 1 file names (LEAK 2, REVIEW 1)
- **LEAK** `data_dictionary_rev5.pdf`: a file whose name says it describes the data (data_dictionary_rev5): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **LEAK** `export_manifest.csv`: a file whose name says it describes the data (manifest): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **REVIEW** `summer2026_capacity_plan_v3.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `planning_basis_NP-PB-26S_issue2.pdf`: golden figure 232 appears: ...es move from the A319 (144 seats) to the A321neo (232 seats) from the season start, except Brindisi and...
- **REVIEW** `planning_basis_NP-PB-26S_issue2.pdf`: carries 7 of 8 distinctive words of the committed call: 'The nine Linate routes will carry about 175,000 more passengers in summer 2026 than they carried in summer 2025.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `data_dictionary_rev5.pdf`: 6 of 25 stump-paragraph terms appear (bookings, family, agency, record, close-out, records); read whether the document names the move
- **REVIEW** `planning_basis_NP-PB-26S_issue2.pdf`: 7 of 25 stump-paragraph terms appear (changes, section, network, planning, season, capacity); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)
