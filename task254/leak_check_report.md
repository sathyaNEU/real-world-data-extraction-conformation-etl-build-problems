# leak check, task254

**Verdict: REVIEW.** 25 files read, 16 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: segment, period, rejected, architecture, decisive, construction, carries, golden, walked, dropped, re-root, counts, vehicle, reading, segments, midpoint, travel, second, default, device, cutover, reliability, planning, setting, profile

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `trelvane_export_readme.txt`: golden figure 264 appears: ...age: I-65 between Exit 121 and Exit 136 and the I-264 interchange, both directions, KY-480 at Exit 12...
- **REVIEW** `chestnut_garage_closure_notice.pdf`: carries 6 of 7 distinctive words of the committed call: 'The 2027 staff shuttle should leave the Cedar Grove park-and-ride lot at 7:05 a.m.'
- **REVIEW** `shuttle_service_budget_note_2027.docx`: carries 5 of 7 distinctive words of the committed call: 'The 2027 staff shuttle should leave the Cedar Grove park-and-ride lot at 7:05 a.m.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `shuttle_service_budget_note_2027.docx`: 3 of 25 stump-paragraph terms appear (counts, vehicle, planning); read whether the document names the move
- **REVIEW** `staff_shuttle_service_standard.docx`: 5 of 25 stump-paragraph terms appear (counts, vehicle, travel, planning, setting); read whether the document names the move
- **REVIEW** `trelvane_export_readme.txt`: 6 of 25 stump-paragraph terms appear (segment, vehicle, segments, travel, second, planning); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `hr_holiday_calendars.xlsx`: 9 ISO dates after 2026-10-16, e.g. 2027-01-01, 2027-01-18, 2027-05-31, 2027-06-18, 2027-07-05

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

First pass (Sonnet, medium, on the pack as first built; the budget note, the readme and the export changed afterwards, see the second pass).

1. Decisive step: none announced. The nearest sentences are the standard's 2.4 ("A trip runs from the departure at the boarding bay to arrival at the campus stop, along the route in the route file, with the route file's fixed legs.") and 2.5 ("Trip times use the passenger-vehicle travel times in the vendor's export."); they say what to sum, not how to carry the segment times along the trip, and nothing says not to add up one epoch's times.
2. Ranking or scoring file: none. The Route 40X timetable is another service's schedule.
3. File only there to help: none obvious; the commute survey and the 40X timetable read as distractors.
4. Answer-like figures: none.
5. Literal sentences: standard 2.1 (at least 90 per cent of the working weekdays of the latest twelve months, by 8:00), 2.2 (working weekday: Monday to Friday less the HR calendar's holidays), 2.3 (every working weekday counts), 2.4 (the route file's segments and fixed legs), 2.5 (passenger class), 2.6 (the five-minute grid); the budget note's late arrivals (late working weekdays, each counting every rider), service days (the HR 2027 calendar) and convoy (a seat a rider); the closure notice's riders (8:00 starters, granted HR spaces, less opt-outs), "cross-keyed via the HR extract (employee_no vs payroll_id)". Every one executes to the golden's construction.

Mechanical items: 264 is the I-264 road name (harmless); the closure notice and budget note share the call's nouns but carry no departure time (harmless); the standard, the budget note and the readme name no move (harmless); the 2027 dates are the 2027 holiday sheet the budget note uses (harmless).

Realism tells: the budget note read somewhat like a brief; each monthly export was a complete grid with no epoch missing; the two start-time formats read as deliberate; the opt-out dates run past "the extract", which is the probe export's delivery date, not the workbook's.

## Solver's-eye read (second pass)

Second pass (Sonnet, medium) on the final pack, after the budget note was rewritten and the readme gained its sentence on epochs left out.

1. Decisive step: none stated as a method. The nearest is standard 2.4 ("A trip runs from the departure at the boarding bay to arrival at the campus stop, along the route in the route file, with the route file's fixed legs."); the documents define the quantity and never say how to evaluate it, and the reader names both a trip chained through the epochs it reaches and every segment taken at the departure epoch as open to the analyst.
2. Ranking or scoring file: none. The 40X timetable gives another service's scheduled times.
3. File only there to help: none clearly; the readme reads as a vendor data dictionary and the deadhead route as an operator's file.
4. Answer-like figure or name: none; 7:05 appears in no file.
5. Literal sentences: standard 2.1 to 2.6, the route file's release note, the readme's release rule, its density C fill and its epochs left out, the budget note's late arrivals, operator charges, service days and convoy, and the closure notice's riders. Every one executes to the golden's construction; the epochs left out never touch the route's working-weekday rows.

Mechanical items: all seven harmless (I-264 is a road; the notice and budget note give no time; the standard, budget note and readme name no move; the 2027 dates are the 2027 holiday sheet the budget note cites).

Realism tells: none needing a fix. The reader reads the probe files as uniform and complete (they are complete on the route's working-weekday rows by design, with 1,664 epochs left out elsewhere), the 40X timetable as a clean grid, the request numbers as sequential in date order and the permit roll as sorted by permit number, which is how such exports come out.
