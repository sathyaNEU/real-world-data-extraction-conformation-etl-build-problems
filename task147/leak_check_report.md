# leak check, task147

**Verdict: REVIEW.** 16 files read, 15 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: nights, concert, bookings, pickup, asserted, extract, booking, history, night-level, golden, replayed, decisive, nothing, closing, festival, runner-up, confirmation, arrival, method, weekends, default, decision, checks, back-test, events

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `HK-04_housekeeping_staffing_festival_season.pdf`: carries 14 of 20 distinctive words of the committed call: "Brennock's block should go to the closing week, Monday 23 to Sunday 29 August 2027, forecast at about 400 room-nights ab"

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `HK-04_housekeeping_staffing_festival_season.pdf`: 4 of 25 stump-paragraph terms appear (nights, festival, confirmation, checks); read whether the document names the move

## 9 dates after the setting (REVIEW 5)
- **REVIEW** `compset_rate_shop_2027-06-30.xlsx`: 35 ISO dates after 2027-07-01, e.g. 2027-07-26, 2027-07-27, 2027-07-28, 2027-07-29, 2027-07-30
- **REVIEW** `festival_programme_dates.json`: 3 ISO dates after 2027-07-01, e.g. 2027-08-05, 2027-08-06, 2027-08-29
- **REVIEW** `pms_amendment_log_2027-07-01.csv`: 378 ISO dates after 2027-07-01, e.g. 2027-07-02, 2027-07-03, 2027-07-04, 2027-07-05, 2027-07-06
- **REVIEW** `pms_reservations_extract_2027-07-01.csv`: 17739 ISO dates after 2027-07-01, e.g. 2027-07-02, 2027-07-03, 2027-07-04, 2027-07-05, 2027-07-06
- **REVIEW** `sales_events_diary_2022-2027.xlsx`: 8 ISO dates after 2027-07-01, e.g. 2027-08-05, 2027-08-13, 2027-08-14, 2027-08-29, 2027-09-18

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 36% of 196 prompts (cap 30%); second-sentence opener 'put' at 35% of 196 prompts (cap 20%); rounding opener 'give' at 44% of 196 prompts (cap 20%); reword at the role level, not the verb

## 1 file names (clean)

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

### Reship read (2026-11-02, Sonnet at medium, fresh copy of prompt.txt and target.zip d05e2f56, the export notes and the folder list no longer shipped, the last-season table's second ask cut)

1 none states the move (HK-04's 4.1 and 4.2 file the estimand, the week with the most room-nights above capacity forecast on the book as it stood); 2 none; 3 no dictionary, readme, manifest or folder list, HK-04 the governing standard and the code lists a plain crosswalk; 4 none; 5 HK-04's 2.1 to 2.4, 3.1, 3.2, 4.1 and 4.2 and the festival dates, each executed as written, the forecasting method left open; 6 an analytical choice. It did not find the last-season table's device (the lent logins, shown only by the door record); the readings it raised (the supervisor notes, the payroll references' dates) are the old devices, kept as hazards, each one reading per judge pass 3. Its realism notes (the agency timesheet's uniform shifts, the batch-created tasks) are on files whose structure this reship did not change.
