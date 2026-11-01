# leak check, task157

**Verdict: REVIEW.** 15 files read, 32 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: minutes, timetable, journey, record, journeys, drivers, departure, asserted, departures, sentence, driver, nothing, forecasting, published, window, running, arrival, relieved, converges, timing, registered, decisive, control, pieces, winter

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `franchise_lot2_schedule7_performance_regime.pdf`: carries 9 of 13 distinctive words of the committed call: 'Name routes 27, 41 and 58 in the Thornsby Bridge Disruption Notice: each is forecast below the 80 per cent punctuality f'
- **REVIEW** `marsh_lane_closure_2025_closeout.pdf`: carries 10 of 13 distinctive words of the committed call: 'Name routes 27, 41 and 58 in the Thornsby Bridge Disruption Notice: each is forecast below the 80 per cent punctuality f'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `franchise_lot2_schedule7_performance_regime.pdf`: 12 of 25 stump-paragraph terms appear (minutes, timetable, journey, record, journeys, departure); read whether the document names the move
- **REVIEW** `marsh_lane_closure_2025_closeout.pdf`: 5 of 25 stump-paragraph terms appear (minutes, journey, record, journeys, running); read whether the document names the move
- **REVIEW** `thornsby_bridge_closure_tmp_v2.pdf`: 6 of 25 stump-paragraph terms appear (minutes, timetable, journey, running, timing, registered); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 2)
- **REVIEW** `control_room_log_sep_dec_2026.csv`: names 3 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `gcr_lot2_timetable_winter2026_txc.xml`: names 3 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `service41_fare_stages.csv`: names 4 of 7 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `thornsby_bridge_closure_tmp_v2.pdf`: names 3 of 7 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `gcr_lot2_timetable_winter2026_txc.xml`: 14 ISO dates after 2026-12-11, e.g. 2026-12-18, 2027-01-05, 2027-02-12, 2027-02-22, 2027-03-25
- **REVIEW** `street_works_permits_2027q1.csv`: 92 ISO dates after 2026-12-11, e.g. 2027-01-04, 2027-01-07, 2027-01-09, 2027-01-11, 2027-01-12

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Reader: one isolated agent (Sonnet, medium) on fresh copies of `prompt.txt` and `target/` only, 2026-11-01. It
read the pack for leaks and solved nothing.

1. Decisive step: no sentence or file announces it. The nearest are Schedule 7 7.6.1 ("the Authority's forecast
   of that Route's Punctuality over the whole Disruption, every day of it, on the Registered Timetable for those
   days") and the plan's "Service 41 is the only bus service that crosses Thornsby Bridge": together they point
   at forecasting every route, and nothing says which other routes move.
2. No file ranks or scores the routes on the forecast. The published monthly punctuality is a baseline with
   provisional and final rows for the same month, ordinary mess.
3. No dictionary, readme or manifest. The cause code list and the fare stage list are plain operator lookups.
4. Nothing reads as the answer. The close-out's "Route 14's forecast punctuality for the closure was 72.9 per
   cent" is the 2025 precedent.
5. 7.6.1 read literally: each route's punctuality forecast over 11 January to 28 March 2027, every day, on the
   registered timetable; a route is named if below 80 per cent. It files the population and the outcome and
   leaves the method open. Main thread: this is the golden's estimand, not the easy answer; no main-call fork.
6. The decision is an analytical choice (how to project each route's punctuality onto the closure from the AVL
   history, the timetable, the plan's added running times and the Ring Road delay). Field readings (the on-time
   window, the clock, the excused codes) are needed and decide nothing alone; nothing looks planted and no file
   argues for a wrong answer. No rule 3 finding.

Answers a and b: Schedule 7 and the close-out are harmless (contract wording; a precedent naming route 14 for a
different closure); the control room log and the TXC rank nothing. Answer c: the TXC's later dates are its
registration period and school terms, the permits are advance-granted works.

Main thread rulings on the REVIEW lines:
- Sweep 3, Schedule 7: harmless; clause 7.6 defines the Disruption Notice the call is about and names no route.
- Sweep 3, close-out: harmless; the 2025 notice for Marsh Lane names route 14 for another closure.
- Sweep 4 (ruled here, never sent to the reader), Schedule 7, the close-out and the plan: harmless; the words are
  punctuality definitions, journey time comparisons and the diversion's running times, and none names a crew or
  relief link (`checks.py` R3c: the plan and the close-out carry no crew word, Schedule 7 only "duty" in the
  records it keeps).
- Sweep 6, the control room log and the TXC: harmless; an event log and a timetable, neither ranks the routes.
- Sweep 9, the TXC and the permits: harmless; forward-dated by nature (a registration valid to 3 April 2027 with
  its school terms, permits granted for January to March 2027).

Main thread rulings on the reader's realism notes:
- AVL times "a uniform offset from the aimed time": not reproduced. The steady gap in the first rows is the UTC
  clock against local aimed times; lateness grows along each journey (the first journey: 0:44, 5:48, 6:12, 11:30).
- Control room remarks templated: reproduced (83 forms over 559 rows, one fixed sentence per kind). Fixed in the
  generator: the log is written in three controllers' hands by shift, from a stream of its own; 172 forms, the
  commonest 2 per cent of rows; figures.json byte-identical.
- TR on the turn-shorts: harmless; the code list's TR is traffic and late running, which is why a controller turns
  a late bus short.
- The two distractors read as filler: each now carries its register's own fields (the permit's USRN, works
  category and status, cancelled permits included; the counter's seven-day mean and heavy goods share); neither is
  read by any golden figure (`checks.py`).
- The plan's timetable sentence read as written for the task: rewritten as the outcome agreed at the bus liaison
  meeting of 25 November 2026, the same fact. The contract's numbered clauses are its own form.
- The close-out's "within half a minute of the AVL record" supports the plan's minutes as filed: intended, it
  closes the fork on those minutes (`checks.py` SF10: scaled to the close-out, the same call).

### Second read, after the plan's timetable sentence changed

Reader 2: a fresh isolated agent (Sonnet, medium) on fresh copies of `prompt.txt` and `target/`, 2026-11-01, after
the plan's bus liaison sentence, the control room log's wording and the distractors' columns changed.

1. No sentence or file announces the decisive step; 7.6.1 states the estimand, not a method.
2. No file ranks the routes on the question; the published monthly series is calendar-month history with
   provisional and final rows, and the close-out gives one route's 2025 figures.
3. No helper file; the code list and fare stage list read as operational reference tables.
4. Nothing reads as the answer; route 14's 2025 figures belong to another closure.
5. 7.6.1 (each route's departures, every day of 11 January to 28 March 2027, on the registered timetable,
   punctuality), 7.2.1 (the on-time window, unrecorded departures left out), 7.4.2 with 7.5 (reliability, the
   closed excused list), the plan's section 3 (the three unserved stops) and its bands. Main thread: each executes to
   the golden's definition; none files how the forecast is built.
6. An analytical choice, with one doubt: whether applying the plan's per-band minutes is rule application, the
   close-out's plan-against-AVL table supporting those minutes. Main thread ruling: harmless. The minutes are a
   filed input every method uses (Critical Component 1); executed as filed, on route 41 and the Ring Road routes,
   they give the default path, route 41 alone, which is wrong; the call turns on the departures the minutes reach
   through the drivers the duty schedule relieves off route 41, which no file states. No rule 3 finding.

Answers a to c: the same as the first read (Schedule 7 and the close-out hand over nothing for this closure; the
log and the TXC rank nothing; the TXC and the permits are natural forward-dated records, the permits now with 27
granted, 11 granted with conditions and 8 cancelled). Realism: the control room remarks read as real (mixed hands
and shorthand); the provisional and final rows read as normal release mess; every file has a plausible role, none
reads as filler. The close-out's "within half a minute" was raised again as a nudge toward the plan's minutes:
intended, as ruled above.

### Third read, after the boardings ask's pin in the prompt

Reader 3: a fresh isolated agent (Sonnet, medium) on fresh copies of `prompt.txt` and `target/`, 2026-11-01. No
sentence announces the decisive step (7.6.1 and the plan's timetable sentence file the target quantity); no file
ranks the routes; no readme, manifest or notes sheet (the code list and fare stage list are operator lookups); no
figure reads as the answer; questions 5 and 6 as the earlier reads (the estimand filed, the method open, the
deciding work an analytical choice); question 7, no phrase of the prompt says how to compute anything or which
field to use. Main thread rulings on its notes: the plan's minutes and the close-out's comparison are inputs, ruled
as in the second read; the code-to-clause mapping on the reliability ask is rule application on an ask, which the
asks may carry; the realism notes are harmless (the blank causes are the log's NOTE and LATE rows; the sparse WX
and BD rows are what a season holds; the ticket machine's out-of-order rows are its upload mess; the fare stages
match the plan because both describe the same stops) or did not reproduce (the October provisional and final rows
carry different release dates, 5 and 7 November, the final reissued after the late AVL uploads).
