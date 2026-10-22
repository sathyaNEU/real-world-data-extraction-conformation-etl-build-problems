# leak check, task478

**Verdict: REVIEW.** 16 files read, 33 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: pothole, architecture, latency, detection, direction, covers, detections, decisive, inventory, reader, control, kerbline, camera, population, seconds, readers, scatter, blocked, window, instrument, register, recorded, pattern, patrol, sentence

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `kerbline_pilot_scope_of_work.pdf`: \bthe model\b x1: ...each time it detects it, with its class, its severity for a pothole, the model's confidence, the image and the phone's GPS position. The platform's...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `kerbline_pilot_scope_of_work.pdf`: 6 of 25 stump-paragraph terms appear (pothole, detection, covers, detections, kerbline, camera); read whether the document names the move
- **REVIEW** `spring_patching_program_2027.pdf`: 7 of 25 stump-paragraph terms appear (pothole, detection, inventory, kerbline, camera, recorded); read whether the document names the move
- **REVIEW** `tamsett_pilot_data_dictionary.pdf`: 5 of 25 stump-paragraph terms appear (pothole, detection, direction, inventory, kerbline); read whether the document names the move

## 6 ranking artifacts (INFO 1)
- **INFO** `maintenance_sections.csv`: names 4 of 4 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Two isolated readers (general-purpose, sonnet, medium), each holding only fresh copies of prompt.txt and target/ (pack
of 2026-10-22, before the cold-mix repair, which changed one work order's figures and no document), answered the six
questions and committed their figures (scored with score_reader.py against generator/figures.json).

Reader A: call missed (the five: Holloway Run, Carrow Point, Elmscourt, Thistlebank, Norvelle), detections linked at
0.04 mile where the gaps thin out; rates 9 of 14, cold mix 0 of 14 (each repeated figure taken once).
1. none: "Nothing names a distance tolerance" (program 2.2 says what to count, not how).
2. none.
3. the data notes, the crosswalk and the manifest (they explain the extracts).
4. none: the 6.0 line is a threshold.
5. program 2.1, 2.2, 2.4: the five on its own linkage; "the text does not fix the dedupe method".
6. an analytical choice: collapsing the detections into distinct potholes.
REVIEW lines: all four harmless (export fields, the governing document's estimand, field definitions).

Reader B: call missed (nine: the golden seven with Marlpit and Stonebeck), having fitted a lag per unit of 0.5 to 1.7
seconds from the two directions and the traversals and linked at 10 feet, with its own corrected positions unstable
across 6 to 15 feet; rates 6 of 14, cold mix 0 of 14 (every line summed).
1. none: "Nothing announces the position-lag step."
2. none.
3. the data notes, the manifest and the crosswalk; the traversals "supply speed and direction".
4. none.
5. program 2.2 with 2.1 and 2.4: distinct potholes per ten lane-miles of the roadway at 31 March, which "does not fix"
   the linking.
6. an analytical choice: how to collapse the detections (a direction- and speed-dependent position lag, a linking
   distance); secondary rule application: the turnback and the 6.0 line.
REVIEW lines: all four harmless; the scope of work's "not in the pilot" sentence "states the problem, not the method".

Verdict on the REVIEW lines: harmless, one line each in the design note's pre-ship check. No decisive-step sentence, no
helping file, no main-call fork; question 6 analytical from both readers.
