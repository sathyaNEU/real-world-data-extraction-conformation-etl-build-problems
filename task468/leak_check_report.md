# leak check, task468

**Verdict: REVIEW.** 15 files read, 2 golden figures and 13 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: review, service, events, decisive, guidance, device, departure, weighted, record, on-time, shares, golden, design, unmatched, bus-day, schedule, sentence, silent, riverside, sample, repeats, lowest, reader, counts, bus-days

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `dot_ftc_program_guidance_fy2027.pdf`: carries 6 of 6 distinctive words of the committed call: 'Nominate Routes 2, 4, 6, 17 and 22 to the Frequent Transit Corridors Program for FY2027.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `dot_ftc_program_guidance_fy2027.pdf`: 9 of 25 stump-paragraph terms appear (service, guidance, departure, record, on-time, design); read whether the document names the move
- **REVIEW** `quinnell_cutover_export_notes.pdf`: 8 of 25 stump-paragraph terms appear (review, service, events, departure, design, unmatched); read whether the document names the move
- **REVIEW** `service_quality_trip_matching_review_2026.pdf`: 8 of 25 stump-paragraph terms appear (review, service, events, record, bus-day, schedule); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "Which of Larkhaven Transit's eleven candidate routes should the City nominate to the state's Frequent Transit Corridors Program for FY2027, at most five, on its buses' departures from each route's designated stop from Ja"

## 6 ranking artifacts (REVIEW 3, INFO 1)
- **REVIEW** `farebox_revenue_by_route_2026h1.xlsx`: names 8 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `ridership_by_route_2026h1.xlsx`: names 8 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `title_vi_service_monitoring_2025.pdf`: names 8 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `ftc_candidate_routes_fy2027.csv`: names 8 of 13 answer-set candidates; confirm it does not rank them on the decision question

## 7 hidden content (REVIEW 2)
- **REVIEW** `larkhaven_gtfs_20260101.zip`: nested_zip: true
- **REVIEW** `larkhaven_gtfs_20260405.zip`: nested_zip: true

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: rounding at the close: no rounding words anywhere; every derived figure needs one, stated once at the end

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## Solver's-eye read

Round 4 (2026-10-19, target.zip d79138b03f492a10, one isolated reader at medium on a fresh unzip, neutral brief).

1. Decisive step: nothing quoted beyond guidance 3.4 ("the agency reports its estimate of each route's departures") and the review memo's procedure (400 bus-days, one event each); neither names a weighting. For the shelters it quoted the work-order sheet's line that shelters move only under a work order. Harmless (procedure as every audit states it).
2. Ranking file: none (the ridership report is the cap's filed order).
3. Helper files: the cutover notes, the fleet roster's tag map, the review memo and log (the systems' own documentation). Harmless.
4. Answer-like figure: none.
5. Filed sentences: guidance 3.3 and 5.1, executed to the golden's estimand (125 days, the hourly minimum, the cap by boardings). Golden.
6. What decides: an analytical choice (the review weighted by its sampling design). Rule 3 holds.

Its figures, scored by score_reader.py (exit 1): the call landed (Routes 2, 4, 6, 17 and 22, Route 11 left out), every verdict right, the shelter counts 0 of 11 (13, 14, 6, 4, 7, 8, 10, 6, 5, 10, 12, the inventory on stop code carried by the work orders, exactly the ceiling script's cracker). The device held; the call landed, as in rounds 1 to 3.

Realism notes, each answered: work orders against inventory flags lag by inspection date (the inventory's annual cycle, by design); two July shelters inspected days later (the hazard); a relocation work order carries the stop's code (the stop's identity, as Capital Projects files it); the review tally recomputing exactly, interlined buses, 600-second headways on the frequency route, smooth ridership (answered in rounds 1 to 3).
