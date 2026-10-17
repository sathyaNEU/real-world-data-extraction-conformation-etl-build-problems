# leak check, task263

**Verdict: REVIEW.** 13 files read, 26 golden figures and 15 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: samples, sample, balance, sources, average, pumping, mixture, collection, source, inventory, blends, results, records, entry-point, decisive, beside, proportions, asserted, environmental, mixtures, mixing, blanks, service, nothing, golden

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `iup_2027_draft_section6_pfas_design_grants.pdf`: candidate 'Torvik Water Utility' sits beside decision vocabulary: ...FAS priority list Rank PWS ID System County Population served Priority points 1 4626844 Torvik Water Utility Hedstrom 6,538 92 2 4664327 City of Halvorsen Water Department Engvall 8,917 88 3 4...
- **REVIEW** `iup_2027_draft_section6_pfas_design_grants.pdf`: carries 13 of 18 distinctive words of the committed call: 'The $36 million reaches 16 of the 20 systems on the 2027 PFAS priority list, Torvik Water Utility through Valdahl Sanita'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `data_request_notes_2026-09-02.txt`: 8 of 25 stump-paragraph terms appear (samples, sample, sources, collection, source, results); read whether the document names the move
- **REVIEW** `iup_2027_draft_section6_pfas_design_grants.pdf`: 6 of 25 stump-paragraph terms appear (average, source, inventory, records, environmental, nothing); read whether the document names the move
- **REVIEW** `pfas_initial_monitoring_sampling_guide_rev2.pdf`: 13 of 25 stump-paragraph terms appear (samples, sample, sources, pumping, collection, source); read whether the document names the move

## 6 ranking artifacts (REVIEW 5, INFO 1)
- **REVIEW** `iup_2027_draft_section6_pfas_design_grants.pdf`: names 15 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `monthly_operating_reports_2025.csv`: names 15 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `pfas_entry_point_results_2024-2026.csv`: names 15 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `pfas_field_collection_records_2024-2026.csv`: names 15 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `source_facility_inventory_2026.xlsx`: names 15 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `wholesale_connections_2026.csv`: names 8 of 15 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Two isolated readers (Sonnet, medium effort), each with a fresh copy of prompt.txt and target/ and nothing else.

### Loop 1 (the first cut)

1. Decisive step: none stated. The plan's 6.3 ("A well's own water is the water the well itself pumps") and the
   guide's record fields name what a solver works from; the reader had to work out for itself that every result is
   an entry-point blend and each well's level has to be separated from the blends.
2. Ranking file: none. Table 6-1 orders the systems by priority points (the funding order the plan files); no file
   gives a grant, a reach or a well's level.
3. Analyst-only file: the department's transmittal note is the likeliest, and the reader judged it plausible as a
   real cover note.
4. Reads as the answer: nothing; the $36 million, $2.4 million per MGD and $6 million cap are inputs.
5. Literal sentence: 6.3 with 6.4; its literal execution is the golden's procedure (active wells, each analyte's own
   level over 4.0, rated capacity to MGD, the cap, the walk with a stop). The open points it named (non-detects, the
   averaging, the estimator) all converge on the same wells (checks SF3, SF14, SF16, convergence).
6. What decides: an analytical choice, unmixing each entry point's blends rather than giving a well the entry-point
   result.
Realism notes acted on: one style of invented name throughout, six counties statewide, priority points falling one or
two at a time, a percentage in the plan implying an unexplained base (all fixed, no graded figure moved).

### Loop 2 (after the fix pass)

The same six answers: no decisive-step sentence, no ranking file, nothing reading as the answer, the literal sentence
executing to the golden's procedure, Q6 analytical. Realism notes acted on: four stock remarks on the field records
(varied field notes added), every register row active (six closed systems added), every connection dated the first
of a month (days varied). Notes left as they are: samplers writing in their own style (each sampler's habit), sampler
ids rather than names (the department's export), facility ids issued in sequence, wells named Well 1 to Well n,
meter readings carrying over month to month (each is what the systems' own records hold).

### Verdicts on the REVIEW lines

- 3, the plan names the candidates beside decision words, and carries 13 of 18 words of the call: Table 6-1 is the
  list itself (rank, PWS id, system, county, population, points); it states no grant, wells or reach. Harmless.
- 4, stump-paragraph terms in the notes, the plan and the guide: domain words (samples, sources, collection,
  average); neither reader found a sentence naming the move. Harmless.
- 6, data files naming every candidate beside numbers: exports and the inventory at their own grain, no ranking on
  the decision. Harmless.

Verdict after the read: no LEAK; the decisive step is not stated anywhere in the pack; the deciding step is analytical
in both loops.
