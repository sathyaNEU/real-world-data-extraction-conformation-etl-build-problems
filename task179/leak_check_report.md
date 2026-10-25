# leak check, task179

**Verdict: REVIEW.** 15 files read, 6 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: repeat, intake, entrant, classes, record, window, classmates, sentence, family, nothing, section, decisive, registry, golden, interval, quantity, projection, cutover, forward, forecasting, student, planning, default, population, fictional

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `arc_cutover_notes_registry.pdf`: carries 7 of 11 distinctive words of the committed call: 'Plan for about 3,250 of the 8,659 first-time entrants enrolled at the 1 October 2026 census not to be enrolled at the 1 '
- **REVIEW** `continuing_enrolment_projection_conventions_2027.pdf`: carries 11 of 11 distinctive words of the committed call: 'Plan for about 3,250 of the 8,659 first-time entrants enrolled at the 1 October 2026 census not to be enrolled at the 1 '
- **REVIEW** `data_dictionary.txt`: carries 9 of 11 distinctive words of the committed call: 'Plan for about 3,250 of the 8,659 first-time entrants enrolled at the 1 October 2026 census not to be enrolled at the 1 '

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `arc_cutover_notes_registry.pdf`: 7 of 25 stump-paragraph terms appear (entrant, classes, record, section, registry, cutover); read whether the document names the move
- **REVIEW** `continuing_enrolment_projection_conventions_2027.pdf`: 6 of 25 stump-paragraph terms appear (intake, entrant, classes, projection, student, planning); read whether the document names the move
- **REVIEW** `data_dictionary.txt`: 9 of 25 stump-paragraph terms appear (intake, entrant, family, section, registry, projection); read whether the document names the move

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

Determinism repair, portal round 3 (2026-10-25), one isolated reader on zip c8032390 (`scratchpad/leak-task179r3`),
scored with `score_reader.py`: the call missed (2,250 against 3,250, from attribute models with each entrant's count of
classes in each size band), 0 of 20 ask cells, exit 0.

1. The decisive step: the conventions' lowest-AIC sentence, "the only sentence on how the forecast is computed"; no
   sentence names the count, its form or its effect.
2. A file that ranks or scores the candidates: none.
3. A file that exists only to help the analyst: data_dictionary.txt and the cutover notes (systems, codes, the
   identifier mapping and the class-enrolment semantics).
4. A figure that reads as the answer: none (the timetable's Enrolled at Census reads as a ready size and does not
   match the class lists).
5. Filed sentences read literally: CALL_PIN and ENROLLED_PIN fix the population and the outcome; GROUP_PIN fixes the
   group table. None fixes how the forecast is computed.
6. What decides the main answer: an analytical choice. The reader quoted section 6's comparability sentence as the
   cue for the group counts and wrote that section 6 "does hint that the 2026 class-size profile may differ, but it
   does not say how that matters".

REVIEW lines (answer-figure sweep, files only): arc_cutover_notes_registry.pdf harmless (systems, codes, the mapping,
no figure or method); continuing_enrolment_projection_conventions_2027.pdf harmless (the filed spec, names no
covariate); data_dictionary.txt harmless (fields only). The stump-vocabulary lines are ruled in the main thread: the
three documents share the pack's own words (entrant, classes, record, section, registry, cutover, projection) and
none of the decisive step's (D2).
