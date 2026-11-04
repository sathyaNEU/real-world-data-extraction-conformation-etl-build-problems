# leak check, task210

**Verdict: REVIEW.** 18 files read, 5 golden figures and 16 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, passes, sentence, excess, driver, default, golden, position, window, morning, nothing, highest, weekdays, family, correctly, computed, recorder, expected, normals, evening, shipped, readable, freeze, ladder, repair

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `SRM-07_seasonal_restricted_speed_orders.pdf`: candidate 'Juniper Line' sits beside decision vocabulary: ...hazard control under the Agency Safety Plan. 2. Scope Every revenue track section of the Juniper Line and the Foundry Line, in each direction of travel, as listed in the current streetcar tra...
- **REVIEW** `january_2027_pick_timetable.pdf`: candidate 'Juniper Line' sits beside decision vocabulary: ...Line Section From To Outbound s Inbound s Juniper Line J1 Mesa Park Laurel Street 217 209 Juniper Line J2 Laurel Street Civic Center 166 173 Juniper Line J3 Civic Center Market Square 156 161...
- **REVIEW** `january_2027_pick_timetable.pdf`: carries 22 of 30 distinctive words of the committed call: 'Place the four restricted-speed slots for the weekday peaks of 4 January to 26 February 2027 on J4 outbound in the AM pe'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `SRM-07_seasonal_restricted_speed_orders.pdf`: 7 of 25 stump-paragraph terms appear (record, passes, highest, weekdays, recorder, expected); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 1)
- **REVIEW** `january_2027_pick_timetable.pdf`: names 16 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `streetcar_track_survey_2025.geojson`: names 16 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `SRM-07_seasonal_restricted_speed_orders.pdf`: names 5 of 16 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `school_district_calendar_2026-27.csv`: 154 ISO dates after 2026-11-02, e.g. 2026-11-03, 2026-11-04, 2026-11-05, 2026-11-06, 2026-11-09

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

### Round 1 (stage 4, target.zip 1c38083e, one isolated reader at medium effort), and the main thread's rulings

- Q1 none: the closest are SRM-07 5.1 (slots on the section-direction peaks with the highest expected rates) and 4.1
  (the rate the pick's passes are expected to see at its scheduled times in normal weather), which file the selection
  criterion and the estimand, not how the expected rate is built. Ruling: no decisive-step sentence.
- Q2 none: the dashboard gives line-level monthly rates, no section-direction-peak ranking.
- Q3 none outright; the adjacent-agency records read as ordinary distractors. Q4 none.
- Q5 SRM-07 3.3 to 3.7 and 4.1 fix the unit, window, outcome and denominator; the expectation's estimation stays open.
  Ruling: the estimand is filed and the method stays open where the data separate the candidates.
- Q6 an analytical choice (how the autumn rise is attributed and projected to the winter pick). Ruling: rule 3 holds;
  the judge's Gate H reads the same.
- Q7 mild regularities (flat monthly event counts, the defect cards' entry hours). Ruling: kept, system output.
- Q8 and Q9 the asks' terms (two-car applications, depot tests, revenue service, the card's day, holidays): carried to
  the judge, whose round-1 Gate C findings on the same terms the fix pass closed in the world (SRM-07 6.2, the yard
  sheets' times, the cards dated uniquely, the run sheets' timetable column, the asking sentence's WHAT).
- REVIEW lines: harmless, as ruled in the design note's Leak sweep rulings.

The fix pass changed the prompt and documents a figure reads, so round 2 reads again on target.zip 0d608249.

### Round 2 (stage 4, target.zip 0d608249, one isolated reader at medium effort), and the main thread's rulings

- Q1 none: SRM-07 5.1 and 4.1 as before, the criterion and the target, not the route. Ruling: no decisive-step sentence.
- Q2 to Q4 none. Q5 the same filed WHAT; the projection stays open. Q6 an analytical choice. Ruling: rule 3 holds.
- Q7 nothing conclusive (operator cards only on weekday-timetable days, read as the operating pattern).
- Q8 and Q9: each term settled by SRM-07 3.4 and 6.2, the yard sheets' out and in times, the run sheets' timetable
  column and the asking sentence; the reader's open points (an after-midnight pull-in carries no date, a month-end
  application, the entry date read as the writing day) were resolved by the round-2 judge, which reproduced the seven
  monthly applications and the six card counts exactly, the cards' writing day forced by each card's car and block.
- Q10 the changed sentences and columns state WHAT counts and name no step of the main call. Ruling: harmless.
