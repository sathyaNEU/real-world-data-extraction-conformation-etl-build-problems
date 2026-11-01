# leak check, task147

**Verdict: LEAK.** 20 files read, 20 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: nights, concert, bookings, pickup, extract, asserted, booking, festival, history, nothing, staffing, golden, replayed, night-level, decisive, closing, decision, confirmation, reservation, arrival, events, checks, runner-up, method, default

## 1 file names (LEAK 1)
- **LEAK** `pms_export_notes.txt`: a file whose name says it describes the data (export_notes): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `pms_export_notes.txt`: golden figure 480 appears: ...the reservations in this extract). The hotel has 480 rooms. Fields confirmation_no PMS confirmation...
- **REVIEW** `HK-04_housekeeping_staffing_festival_season.pdf`: carries 14 of 20 distinctive words of the committed call: "Brennock's block should go to the closing week, Monday 23 to Sunday 29 August 2027, forecast at about 400 room-nights ab"

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `HK-04_housekeeping_staffing_festival_season.pdf`: 5 of 25 stump-paragraph terms appear (nights, festival, staffing, confirmation, checks); read whether the document names the move
- **REVIEW** `brennock_framework_agreement_2025.pdf`: 4 of 25 stump-paragraph terms appear (bookings, booking, festival, staffing); read whether the document names the move
- **REVIEW** `pms_export_notes.txt`: 6 of 25 stump-paragraph terms appear (nights, extract, booking, confirmation, reservation, arrival); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 35% of 196 prompts (cap 30%); second-sentence opener 'put' at 36% of 196 prompts (cap 20%); rounding opener 'give' at 46% of 196 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (LEAK 1, REVIEW 1)
- **LEAK** `pms_export_notes.txt`: names 21 column(s) of the data files verbatim, 100% of pms_reservations_extract_2027-07-01.csv: a document that lists the data's columns describes the data whatever its name (dataset-generation section 3); the WHAT belongs in a governing document in the organisation's own genre, which names observables and never the files' fields
- **REVIEW** `brennock_framework_agreement_2025.pdf`: names 8 column(s) of the data files verbatim (Hours, The Weighhouse Hotel, badge, date, festival, hours): confirm it is the organisation's own record and not a note written for the analyst

## 13 task metadata (LEAK 1, REVIEW 2)
- **LEAK** `metadata.json`: title carries a figure from the submission's graded blocks (480)
- **REVIEW** `metadata.json`: title shares the design note's stump vocabulary (nights, concert, festival, staffing): say what the task decides, not how
- **REVIEW** `metadata.json`: subdomain shares the design note's stump vocabulary (nights, bookings, booking, replayed): say what the task decides, not how

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read (round 1)

One isolated read, one agent at medium effort on fresh copies of `prompt.txt` and `target/` only, on the stage 3 cut
(commit cd5abab, target.zip sha256 5c3be492ee795008), before the stage 4 repairs; the verdict as relayed by the build's
coordinator:
- Q1 to Q4 (a decisive-step sentence, a file ranking the candidates or stating the asked figures, a file there only to
  help, a figure or name reading as the answer): none; clean.
- Q6: an analytical choice.
- Readings two ways: its "come next" reading is closed by SF8 (the season's five roster weeks, HK-04 2.1, and the
  prompt's "with its own figure"); its rounding-order reading by SF9 (each week's figure rounded once from unrounded
  nights, the prompt's last sentence).

## Solver's-eye read (round 2)

One isolated read, one agent at medium effort on fresh copies of `prompt.txt` and `target/` only, on the repaired cut
(commit c06e15f, target.zip sha256 daaad09a10319e7e, the shipped pack: the final rebuild changed only the write-up and
the goldens' wording); the verdict as relayed by the build's coordinator:
- Q1 to Q4: none; clean.
- Its literal route on "the book as it stands" lands the concert week: the default path, not a filed answer.
- Q6: an analytical choice.
- Readings two ways: its "come next" reading is closed by SF8.

The last leak.py run (2026-10-16, on the shipped cut) gives the ten REVIEW lines above and no LEAK; each is answered in
the design note's `## Leak review`.
