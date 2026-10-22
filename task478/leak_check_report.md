# leak check, task478

**Verdict: REVIEW.** 16 files read, 31 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, pothole, latency, detection, direction, covers, detections, decisive, reader, inventory, control, kerbline, camera, population, seconds, sentence, readers, scatter, blocked, window, office, instrument, register, recorded, pattern

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `kerbline_pilot_scope_of_work.pdf`: \bthe model\b x1: ...each time it detects it, with its class, its severity for a pothole, the model's confidence, the image and the phone's GPS position. The platform's...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `kerbline_pilot_scope_of_work.pdf`: 6 of 25 stump-paragraph terms appear (pothole, detection, covers, detections, kerbline, camera); read whether the document names the move
- **REVIEW** `spring_patching_program_2027.pdf`: 6 of 25 stump-paragraph terms appear (pothole, detection, inventory, kerbline, camera, recorded); read whether the document names the move
- **REVIEW** `tamsett_pilot_data_dictionary.pdf`: 5 of 25 stump-paragraph terms appear (pothole, detection, direction, inventory, kerbline); read whether the document names the move

## 6 ranking artifacts (INFO 1)
- **INFO** `maintenance_sections.csv`: names 4 of 4 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

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

Rounds 2 and 3 (packs of 2026-10-22 rebuilt for the cold-mix repairs; no main-call file changed), four more isolated
readers on the same brief:

Reader C: call missed (eleven), from clustering on GPS position per route and direction; rates 1 of 14; cold mix 14 of
14 (lines of one order closed together read as the order's total). Questions 1 to 6: none, none, the data notes, none,
program 2.2 and 2.4 ("fixes the unit of count and the population but not how repeated, noisy sightings are merged"),
an analytical choice. REVIEW lines harmless.

Reader D: call missed (the five), detections chained within 0.04 mile; rates 11 of 14; cold mix 0 of 14 (every repeated
figure taken once). Questions: none, none, the data notes and the crosswalk, none, program 2.2 with 2.4, an analytical
choice. REVIEW lines harmless.

Reader E (round 3, with the section yards' stores, since removed): call missed (eleven), from the most detections any
single pass made inside a cluster; rates 0 of 14; cold mix 14 of 14, checked against the stores (each crew-day's use
rounded up to the bag reproduced every net draw: the stores file worked as an oracle and was removed). Questions: none,
none, the data notes and the manifest, none, program 2.2 and 2.4, an analytical choice. REVIEW lines harmless.

Reader F (round 3): call landed (the golden seven, every rate and every count), having fitted each unit's lag by
regressing the detections' offsets inside rough clusters on the pass's signed speed (0.5 to 1.7 seconds), then
re-clustered on corrected positions (1,441 potholes, 1,427 after the turnback); cold mix 0 of 14 (every repeated figure
taken once). Questions: none ("no file mentions the position lag or any way to link detections"), none, the data notes
and the manifest, none, program 2.2 (WHAT, not how), an analytical choice. REVIEW lines harmless; the data notes'
milepost direction "a mild pointer that direction matters" without naming the lag.

Across architecture 4, eight of nine cold threads missed the call (six readers and the first derivations of three judge
threads); reader F's route is the latency correction itself, found from the data. No decisive-step sentence, no helping
file, no main-call fork from any reader.

Round 4 (target.zip c402f80c: the stores file removed, the order entry filed in the data notes, the program listing
the cold patches on the section's roadway), two more isolated readers:

Reader G: call missed (twelve, Halverton and Pyke Hill out), from single-link GPS clustering within severity; rates 1 of
14; cold mix 14 of 14 (each line placed by route and milepost, an order closed together counted once). Questions: program
2.2 ("names the dedupe but not how to match repeated noisy detections"), none, the data notes, none, program 2.4 with
2.2, an analytical choice. REVIEW lines harmless; the data notes' order-entry sentence "a semantics hint on the pounds
ask, not the call".

Reader H: call missed (eleven), from gap clustering per route and direction at 0.02 mile; rates 1 of 14; cold mix 14
of 14 (each patch on the section of its ext_ref detection's segment, an order closed together counted once). Questions:
program 2.2 (the estimand, "the dedup method is not given"), none, the crosswalk and the data notes, none, program 2.2
read literally (distinct potholes, not detections), an analytical choice. REVIEW lines harmless.

Over the four rounds, seven of eight readers missed the call, and every reader found the main call's decisive step
unstated. With the order entry filed, the cold-mix ask holds only readers who neither read the data notes nor place a
patch on its roadway.
