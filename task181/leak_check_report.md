# leak check, task181

**Verdict: REVIEW.** 11 files read, 9 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: exposure, steriliser, window, architecture, decisive, excess, family, reflex, records, sentence, theatre, infection, department, export, counts, barangays, shared, system, reading, shipped, sector, surveillance, resource, exposed, procedure

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `haisc_outlier_notice_kooralong_2027q2.pdf`: 3 of 25 stump-paragraph terms appear (infection, surveillance, procedure); read whether the document names the move
- **REVIEW** `haisc_outlier_response_guide_2027.pdf`: 5 of 25 stump-paragraph terms appear (theatre, infection, counts, surveillance, procedure); read whether the document names the move
- **REVIEW** `haisc_procedure_rates_2026.pdf`: 3 of 25 stump-paragraph terms appear (infection, surveillance, procedure); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "For the record behind it, ssi_review_figures_2027.csv should give each consultant's procedures and the infections after them in each year from 2022 to 2024."
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Procedures and infections are whole numbers.'

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Architecture 6, read 1 on target.zip 2ba1a563 (isolated Sonnet reader, a fresh copy of prompt.txt and target/ only).

1. Decisive step: no sentence states it; the nearest is the Centre's guide section 2 (the response names the
   consultants whose own practice raised their patients' risk above the limit), a purpose and not a method.
2. Ranking file: none; the Centre's rates table scores categories and risk indices, not consultants.
3. Helping file: none; the guide and the rates table are the Centre's own governing documents.
4. Answer figure or name: none; the notice's 120 against 59.9 expected and the limit of 76 are the hospital's trigger.
5. Population sentences: guide sections 3 and 4 (one count per procedure, the responsible consultant, 30 or 90 days,
   the expected count from the Centre's rates and the Poisson 97.5th centile); their literal result is the golden's.
6. What decides: an analytical choice (each consultant against a risk-adjusted expectation, and which procedures and
   infections are the consultant's); the CSSD material read as context for the hospital-level excess, no decoy.

Sweep lines: the guide's surveillance nouns and the equipment log's routine work orders harmless.

Realism: the reader found the equipment log's work orders in fixed steps and its sign-off times rising three minutes
a row, which made the steriliser 3 repair's 14:40 stand out; the log now numbers work orders unevenly with the calendar
and signs jobs off through the day, and its workbook was created at the start of the 2026 log; no figure moved
(target.zip 329c3bfb).

