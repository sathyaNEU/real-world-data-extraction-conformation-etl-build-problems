# leak check, task269

**Verdict: REVIEW.** 16 files read, 26 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: branch, departures, network, riders, branches, inbound, branched, record, waiting, method, decisive, boarded, tag-off, standard, golden, architecture, service, beyond, attractive, timetable, route-level, domain, shared, screen, random

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `census_working_pack_contents.txt`: carries 3 of 5 distinctive words of the committed call: 'Give the 2027 headway supervisor teams to routes 3, 7, 31 and 40.'
- **REVIEW** `headway_programme_guidelines_2027.pdf`: carries 4 of 5 distinctive words of the committed call: 'Give the 2027 headway supervisor teams to routes 3, 7, 31 and 40.'
- **REVIEW** `headway_supervision_pilot_plan_2026.pdf`: carries 3 of 5 distinctive words of the committed call: 'Give the 2027 headway supervisor teams to routes 3, 7, 31 and 40.'

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `bus_service_reliability_standard_v4.pdf`: 11 of 25 stump-paragraph terms appear (departures, network, record, waiting, boarded, tag-off); read whether the document names the move
- **REVIEW** `census_working_pack_contents.txt`: 5 of 25 stump-paragraph terms appear (departures, network, standard, service, timetable); read whether the document names the move
- **REVIEW** `headway_programme_guidelines_2027.pdf`: 8 of 25 stump-paragraph terms appear (branch, network, branches, record, standard, service); read whether the document names the move
- **REVIEW** `headway_supervision_pilot_plan_2026.pdf`: 3 of 25 stump-paragraph terms appear (network, record, shared); read whether the document names the move
- **REVIEW** `service_performance_report_august_2026.pdf`: 4 of 25 stump-paragraph terms appear (network, standard, service, timetable); read whether the document names the move

## 7 hidden content (REVIEW 2)
- **REVIEW** `gtfs_pellbrook_2026-07-20.zip`: nested_zip: true
- **REVIEW** `gtfs_pellbrook_2026-08-17.zip`: nested_zip: true

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Two isolated scored readers (Sonnet, medium), each on a fresh copy of `prompt.txt` and `target/`, 2026-10-19. Reader 1 also answered the REVIEW lines after its figures were final (the committed call withheld from its copy of them).

**Scores** (`score_reader.py task269`): reader 1 call 0 of 1, ask figures 20 of 25 (80.0 per cent), exit 1; reader 2 call 0 of 1, ask figures 20 of 25 (80.0 per cent), exit 1. Both filed routes 7, 14, 31 and 40 with route 3 first below (31 at 2.19, 14 at 1.35, 7 at 1.34, 40 at 1.09, 3 at 1.01 over all of a route's departures), the default path. Both landed all eight shifts and all eight costs and the four unbranched routes' excess wait (3 at 1.0, 9 at 0.8, 22 at 0.6, 40 at 1.1); both missed every branched route's excess wait and the first route below.

**Ask paths.** Shifts: payroll rows on the HP posts and the roster app's worked rows, depot posts and cancelled peaks out, the 4 to 15 May overlap counted once (reader 2 through the staff list on person, route, day and peak; reader 1 by a cutover at 15 May). Cost: the plan's $536.80 for each post on each pilot weekday from the route's start to 26 June, public holidays out, plus each month's fee from the plan's table shared by the month's shifts; both said the post charges match the ledger, reader 1 that the 30 June journal and its reversal were not double counted.

**Questions 1 to 8** (both readers, in substance):
1. No sentence states a decisive step; the nearest are the standard's 3.2 and 3.3 and the guidelines' 2.3.
2. No file ranks the routes on excess wait; the August report ranks on-time running on the first release (route 31 worst).
3. `census_working_pack_contents.txt` and `frequent_corridors_2026.xlsx` read as analyst aids but plausible internal documents; reader 2 named the first release, the feedback workbook and the stop changes log as unused context.
4. Nothing reads as the answer.
5. The standard's 2.3 (peaks), 2.4 (default fares count), 3.2 (revised release, last timing point, headways inside the peak, the later of a doubled departure, the timetable in force) and 3.3 (per boarding); the guidelines' 2.1 and 2.2 (corridor, census fortnight); the plan's shift, cancellation, depot and charge clauses. Each executes to the reader's own figures, the route-level reading of the departures.
6. Both: mostly following the stated procedure, with one analytical choice, the random-arrival wait from squared headways less the timetable's. Neither saw the branch structure.
7. No contradiction in the data; the first release against the revised and the ledger's June journal and reversal noted.
8. Realism: round pilot charges and fees, exact shift times, tidy staff list and trip ids, the payroll and roster overlap matching one for one, `.example` domains; reader 2 read the feedback workbook, the stop changes log and the 30 June reversal as staged.

**REVIEW lines (reader 1):** 1 to 3, 5 to 10 harmless; 4, the standard hands over the procedure (revised release, last timing point, in-peak headways, the later departure) as literal rules but not the result.

**Disposition.** The call held twice. The ask layer failed (exit 1 for both): every pilot figure was recomputable from the plan and the timesheets' battery work. Not repaired: the judge's first pass returned SEND_BACK on the departure set, architecture 3 is spent and task269 is retired (`DESIGN_NOTE.md`, `## Retired`).
