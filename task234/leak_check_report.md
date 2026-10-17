# leak check, task234

**Verdict: REVIEW.** 11 files read, 31 golden figures and 12 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: positivity, laboratories, county, report, testing, asserted, epidemic, counts, patients, default, decisive, message, baseline, golden, linear, surveillance, messages, weekly, positives, change, season, sentence, seasonal, fitted, denominator

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `DATA_DICTIONARY.md`: 8 of 25 stump-paragraph terms appear (laboratories, county, report, message, surveillance, weekly); read whether the document names the move
- **REVIEW** `FCP-2_feed_completeness_protocol.pdf`: 7 of 25 stump-paragraph terms appear (laboratories, county, report, counts, surveillance, weekly); read whether the document names the move
- **REVIEW** `README.md`: 8 of 25 stump-paragraph terms appear (laboratories, county, report, message, surveillance, messages); read whether the document names the move

## 6 ranking artifacts (INFO 1)
- **INFO** `respiratory_stream_register.xlsx`: names 10 of 12 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

### Pass 1 (isolated reader, fresh copy of prompt.txt and target/, before the round-1 fix)

1. Decisive step: none named. Nearest is FCP-2 s.4, "The escalations are set that Monday, before the week's aggregate reports are due, so that a laboratory losing results is called while the week's results can still be resent", which says week 3's denominator is not yet filed; "No sentence says how to estimate week 3's denominator."
2. Ranking or scoring file: none (the register lists streams with no numbers; the reports are history).
3. Helper files: elr_result_codes.csv ("read with RV-FLUB as one influenza test"); the change log and the dictionary mildly.
4. Answer-like figure or name: none.
5. FCP-2 s.3 executed literally gives the week-2 percentages from the extract and the reports of record; for week 3 it gives nothing, the denominator not yet existing; it fixes the population and window, not the method.
6. "Mostly an analytical choice": the week-3 denominator has to be estimated from earlier weeks' reports.

REVIEW rulings: DATA_DICTIONARY.md harmless (column definitions); FCP-2 harmless (the governing rules; s.4's timing is a process fact, not a method); README.md harmless (a file index); respiratory_stream_register.xlsx harmless (no counts, rates or ranking).

Realism notes and their disposition: receipt before release in 57 per cent of rows (the pre-migration county clock, the week-2 device, kept); "visible" in the sheet names (the reader's printout of the sheet state, no change); identical in_protocol_from dates (replaced by each stream's test codes); a sparse change log (enriched with routine entries).

### Pass 2 (isolated reader, fresh copy of the rebuilt pack)

1. Decisive step: "no single sentence announces it"; nearest FCP-2 s.3 and s.4, which say week 3's report is not yet filed but not what to use as the denominator.
2. Ranking or scoring file: none.
3. Helper files: README.md, DATA_DICTIONARY.md, elr_result_codes.csv.
4. Answer-like figure or name: none.
5. FCP-2 s.3 and s.4 literally: no week-3 denominator; week 2 computable from the extract and the week-2 reports of record.
6. An analytical choice: "The solver must estimate an expected week 3 denominator ... No file or sentence tells them how."

REVIEW rulings: DATA_DICTIONARY.md, FCP-2 and README.md harmless.

Realism notes (mild, kept): the migration and firewall entries in the change log, the six-hour receipt inversion before the migration (both the week-2 device's evidence), the dictionary's county-time note, the register's 29 rows matching the change log.
