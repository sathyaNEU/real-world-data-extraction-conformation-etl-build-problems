# leak check, task179

**Verdict: REVIEW.** 15 files read, 6 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: repeat, intake, entrant, classes, record, window, sentence, classmates, family, section, nothing, decisive, registry, golden, interval, quantity, projection, cutover, forward, forecasting, student, planning, default, unchanged, population

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `continuing_enrolment_projection_conventions_2027.pdf`: carries 11 of 11 distinctive words of the committed call: 'Plan for about 3,250 of the 8,659 first-time entrants enrolled at the 1 October 2026 census not to be enrolled at the 1 '
- **REVIEW** `data_dictionary.txt`: carries 9 of 11 distinctive words of the committed call: 'Plan for about 3,250 of the 8,659 first-time entrants enrolled at the 1 October 2026 census not to be enrolled at the 1 '

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `arc_cutover_notes_registry.pdf`: 6 of 25 stump-paragraph terms appear (record, section, registry, cutover, student, unchanged); read whether the document names the move
- **REVIEW** `continuing_enrolment_projection_conventions_2027.pdf`: 6 of 25 stump-paragraph terms appear (intake, entrant, classes, projection, student, planning); read whether the document names the move
- **REVIEW** `data_dictionary.txt`: 9 of 25 stump-paragraph terms appear (intake, entrant, family, section, registry, projection); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

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

### Portal round 4 rework (zip 01124ef4): scored readers leak-task179r4a and leak-task179r4b

**Reader A** (score_reader.py: the call missed, ask figures 20 of 20 hit)

1. Decisive step: the conventions pdf, section 4: "Each distinct set of classes meeting together in one room on the same day, start and teaching weeks is one group however often it meets, so two classes that share only one of their meetings make three groups". For the forecast: "Where several models of the same outcome are fitted to the same intakes, the projection uses the one with the lowest Akaike information criterion." and "how many of the 2026 intake will not be enrolled ... to the nearest 250".
2. None. No file ranks candidates. The timetable's "Enrolled at Census" column pre-computes group sizes, but it is overstated for about 100 classes.
3. data_dictionary.txt and the cutover notes PDF (ID, code and date conventions, crosswalk use).
4. None for the forecast. The timetable's "Enrolled at Census" column reads like a ready size answer but disagrees with the class enrolment extract.
5. "A group belongs to the faculty that owns its paper, and its size is the number of students enrolled at the census whom it teaches. A cancelled class is not a teaching group." Result: 575 groups, with sizes from enrolled students only. Also "A student on approved leave is not enrolled" and "The first-year intake ... first-time bachelor's entrants with an enrolled programme attempt". Result: 8,659 intake, with non-returners about 2,140 and so 2,250.
6. The group counts are decided by following a stated rule: the section 4 definition plus the ARC extract. The forecast is a fairly flat analytical estimate, and the stability of the rate makes the method largely immaterial. I saw nothing planted. The candidate pitfalls are the stale timetable size column, leave students, and ID mapping.
7. continuing_enrolment_projection_conventions_2027.pdf: it gives away the group-counting rule and the AIC selection rule, but not any figure. It is a filed spec and reads as intended context (borderline, since it states the method). data_dictionary.txt: harmless, since it only lists fields and files and gives no method or figure.

**Reader B** (score_reader.py: the call missed, ask figures 0 of 20 hit)

1. Which sentence tells the decisive step? Conventions pdf s4: "Each distinct set of classes meeting together in one room on the same day, start and teaching weeks is one group however often it meets, so two classes that share only one of their meetings make three groups". s3: "Where several models of the same outcome are fitted to the same intakes, the projection uses the one with the lowest Akaike information criterion." These fix the group count rule and the model selection.
2. Which file already ranks or scores the candidates? none (no file ranks models; the timetable has an Enrolled at Census column per class but it does not give group sizes).
3. Which file exists only to help the analyst? data_dictionary.txt (column glossary) and arc_cutover_notes_registry.pdf (code and ID mapping notes).
4. Which figure or name reads as the answer? none. (Closest: the timetable "Enrolled at Census" column, which is not the group size.)
5. Filed sentence fixing the computation: "The projection reports how many of the 2026 intake will not be enrolled at the 1 October 2027 census, to the nearest 250." with "Where several models of the same outcome are fitted to the same intakes, the projection uses the one with the lowest Akaike information criterion." Literal result for me: lowest-AIC model gives about 2,141, i.e. 2,250. For groups: "A group belongs to the faculty that owns its paper, and its size is the number of students enrolled at the census whom it teaches. A cancelled class is not a teaching group." gives the 20 counts in reader.json.
6. Decider for the main answer: an analytical choice (which covariates, AIC model selection over the historical cohorts, and recognising the week-6 progress checks as a predictor); the written model-selection rule makes part of it rule following. Quote: "the projection uses the one with the lowest Akaike information criterion." For the group counts the decider is rule application (the group definition in conventions s4).
7. continuing_enrolment_projection_conventions_2027.pdf: harmless, it states the estimand, group definition and AIC rule but not the figure or the covariates. data_dictionary.txt: harmless, it only describes columns and files, with no method or number.

Main thread's rulings: neither reader quotes a sentence naming the classmate count; both name SELECT_PIN and GROUP_PIN, which are the filed selection criterion and the asks' own rule. The answer-figure sweep's two lines (conventions, dictionary) carry the request's words and no figure: harmless. The stump-vocabulary sweep's three lines (cutover notes, conventions, dictionary) share the pack's own words (record, registry, entrant, intake, classes) and name no move: harmless. Reader A's 20 of 20 came from joining the class lists to the census history (412 listed students on leave or with no 2026 attempt), the device's own remedy; reader B took the extract's ENROLLED status and kept 0 of 20. The same ask files scored 18 per cent on the portal in round 3.
