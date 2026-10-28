# leak check, task179

**Verdict: REVIEW.** 12 files read, 15 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: victim, record, golden, linked, records, routes, hazard, driver, window, victimization, recent, victims, measured, booking, summer, family, district, screen, violent, textbook, months, back-test, spread, summers, rejected

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `directive_26-07_gps_placement.pdf`: carries 8 of 12 distinctive words of the committed call: "Reserve 500 GPS enrolments in Region 4's 2027 Belvantis order: 500 people on the 31 December 2026 caseload will be booke"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `belvantis_service_schedule_2025.pdf`: 3 of 25 stump-paragraph terms appear (record, records, booking); read whether the document names the move
- **REVIEW** `directive_26-07_gps_placement.pdf`: 6 of 25 stump-paragraph terms appear (victim, record, records, victims, booking, violent); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `cms_supervision_episodes_2018-2026.csv`: 11040 ISO dates after 2027-01-08, e.g. 2027-01-09, 2027-01-10, 2027-01-11, 2027-01-12, 2027-01-13

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read (stage 4, architecture 5)

Each leak reader worked on its own fresh copy of `prompt.txt` and `target/`, read the pack for leaks and solved
nothing (no figure, answer or score), under the STOP rule in `CLAUDE.md`. The stump-vocabulary lines were ruled by the
main thread and never shown to a reader.

- Round 1, on 570c2a77: questions 1 to 4 none (the recidivism brief is statewide, all-offence context; the conversion
  table and the crosswalk are lookups the work needs); question 5 the directive's definitions fix the population and
  the qualifying bookings, Schedule C the days and section 4 the zones; question 6 an analytical choice, named as
  exposure bounded by the remaining supervision and one count per person, the victim records never mentioned. The
  sweep 3 and sweep 9 lines harmless. Its realism tells (device notes one to one with event types, a Schedule C.2
  sentence that explained too much, episodes closing a day before expiry, a one-value crosswalk note) were fixed in
  the generator.
- Round 2, on b8a231ab: questions 1 to 4 none; question 6 an analytical choice, how to project 2027 person-level
  bookings with exposure cut at the end of supervision; both scan lines harmless. Its one tell that read as
  constructed, the conversion table covering almost exactly the booked statutes, was fixed (55 unused former sections
  added, none to Category V); C.4 and the directive's definitions stay as the pins the judge relies on.
- Main thread on the stump-vocabulary lines: `belvantis_service_schedule_2025.pdf` and the directive carry the field's
  own nouns (record, booking, victim, violent); the directive names victims only in its exclusion-zone clause, which is
  what the zone ask reads, and no document links a supervisee's own victimisation to a booking. Harmless.
