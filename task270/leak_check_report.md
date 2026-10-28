# leak check, task270

**Verdict: REVIEW.** 15 files read, 31 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: reader, architecture, status, station, record, minute, readers, network, reading, bookings, golden, location, landed, places, points, reflex, patients, rotation, effect, pelmarsh, lesson, decisive, screens, window, replay

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `cabinet_report_crmp_2027_2031.pdf`: carries 9 of 10 distinctive words of the committed call: 'The 2027 to 2031 plan should name Wrenfold and Pelmarsh, the only districts whose 2026 cover fell below the 75 per cent '

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `cabinet_report_crmp_2027_2031.pdf`: 3 of 25 stump-paragraph terms appear (station, minute, pelmarsh); read whether the document names the move
- **REVIEW** `emergency_cover_standard_2027.pdf`: 4 of 25 stump-paragraph terms appear (status, record, minute, network); read whether the document names the move
- **REVIEW** `oncall_duty_system_policy.pdf`: 4 of 25 stump-paragraph terms appear (status, station, minute, effect); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

One isolated reader (Sonnet, medium) on fresh copies of prompt.txt and target/ from target.zip 5dc16901, 2026-10-28; it read the pack for leaks and did not solve it.

- Q1 decisive step: none. The closest sentence is the standard's "A district's cover for a year is the share of its homes covered, averaged over every minute of the year", which defines the estimand and does not coach the method.
- Q2 ranking file: none. The cabinet report leaves "Appendix B. Response review: districts below the emergency cover standard (to follow)".
- Q3 analyst-only file: none as such. The code list's Mapping sheet is a crosswalk a service holds after a code change; the cabinet report's Appendix A defines the plan's two risk-profile terms (non-domestic premises, false alarms from fire alarm apparatus) and fits a council report.
- Q4 answer-like figure: none.
- Q5 sentences fixing the computation: the standard's sections 2 to 6 (homes, the minute test, free, turnout, the drive, the year, the line) and the policy's crewing rule and promotion date for the asks. Two readings were raised: where an engine stands when away from base, which the standard leaves to the log (the decisive step); and whether a status message timed on a minute's first second is in force at that minute's start.
- Q6 what decides: an analytical choice, the time-varying state of each engine replayed minute by minute; no decoy or memo argues an answer.
- Q7 realism: re-sent statuses at 00 seconds in a large share; location speeds on six values; 80.9 per cent of incident durations in whole minutes; booking edges uniform in the tail; one LGV date repeated; one promotion per station, March to September; establishments of 56, 28 or 12; output-area populations in a narrow band; UPRNs in a regular sequence.
- Flagged item, cabinet_report_crmp_2027_2031.pdf: harmless; it restates the standard's measure and the districts' list and defers the named districts to Appendix B.

Ruled in the main thread: the minute-start reading converges (every district within 0.008 points and at the same whole per cent; SF16, asserted). Every realism tell was fixed in the generator: re-sends timed four hours after an engine's last message, Left base a few seconds after the move, GPS speeds with traffic and drift, closing times to the second, LGV dates spread over 2005 to 2025, promotions spread over the year, re-booking trims skewed to the quarter hour, drivers and BA wearers varying by station, establishments and populations with their spread, and UPRNs by district council range with later builds from a newer range. The documents under target/ and the prompt did not change, so the reader was not re-run.
