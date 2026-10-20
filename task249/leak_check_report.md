# leak check, task249

**Verdict: REVIEW.** 13 files read, 14 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: reader, rising, readers, discharge, architecture, method, regression, decisive, selection, relation, calibration, golden, report, readable, webkit, regime, decision, surrogate, rounds, device, release, points, procedure, season, record

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `suspended_sediment_loads_2027.pdf`: golden figure 433 appears: ...elvi glacier-fed 71 0.1527 1.0311 1.0067 0.985 30,433 FND Fonnadalselvi ved Bruhaug glacier-fed 61 -0.0...
- **REVIEW** `SMP-03_surrogate_load_procedure_v3.pdf`: carries 4 of 7 distinctive words of the committed call: 'Re-issue the published 2027 loads of four stations, SKB, JVB, FND and ESK, all over by more than 15 per cent; the other '

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `SMA_quality_statement_2027.pdf`: 3 of 25 stump-paragraph terms appear (method, report, rounds); read whether the document names the move
- **REVIEW** `SMP-03_surrogate_load_procedure_v3.pdf`: 8 of 25 stump-paragraph terms appear (discharge, regression, calibration, report, surrogate, rounds); read whether the document names the move
- **REVIEW** `data_dictionary.md`: 6 of 25 stump-paragraph terms appear (discharge, regression, calibration, surrogate, procedure, record); read whether the document names the move
- **REVIEW** `suspended_sediment_loads_2027.pdf`: 4 of 25 stump-paragraph terms appear (regression, report, regime, procedure); read whether the document names the move

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

Two isolated readers (Sonnet, medium), each on a fresh copy of prompt.txt and the unzipped target.zip 9dd86516,
scored with score_reader.py: both exit 1 (call 2 of 2, asks 28 of 28).

1. Decisive step announced: none quoted by either ("nothing mentions hysteresis or rising limbs").
2. Ranking file: none; both noted the report's R-squared column (0.866 to 0.870 at SKB, JVB, ESK) as a hint.
3. Helping files: the dictionary and the request (orientation); precipitation and reservoirs read as distractors.
4. Answer-like figures: none; the low R-squared beside the large glacier loads named.
5. Literal sentence: section 8 (the tolerance) and section 7 (the load sum); both read section 6 executed literally as
   reproducing the published loads and re-issuing none.
6. Decides: an analytical choice in both (the samples over-represent rising water).
7. Realism: the rising-water multiplier constant per station with a residual scatter near 0.025 in log10; identical
   noise structure across stations; smooth hydrographs at three significant figures; 1,470 exact re-sent rows; the
   undocumented G, O, K letters; fouled spans of round lengths; visits at near-identical hours.

Verdict: the architecture is spent at Gate F (both readers landed the call).
