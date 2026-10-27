# leak check, task171

**Verdict: REVIEW.** 20 files read, 19 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, clearance, family, population, trough, points, window, decisive, record, inside, cohort, exposure-response, golden, months, driver, worlds, effect, standard, events, median, pooled, forward, default, outcome, change

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `cvn2184_phase3_dose_selection_charter.pdf`: \bthe model\b x2: ...estigator's brochure, section 5). Each forecast is the remission rate the model predicts over the exposure-response analysis set, the dovikizumab pat...

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `cvn2184_phase3_dose_selection_charter.pdf`: golden figure 300 appears: ...end-of-phase-2 meeting. 2. Candidates Dovikizumab 300 mg, 600 mg or 900 mg, given intravenously at week...
- **REVIEW** `dovikizumab_investigators_brochure_section5.pdf`: golden figure 1.02 appears: ...ose across the range (power-model slopes 0.99 and 1.02), with a terminal half-life of 15 to 18 days and...
- **REVIEW** `dovikizumab_investigators_brochure_section5.pdf`: golden figure 300 appears: ...althy volunteers received single IV doses of 100, 300, 600 or 1,200 mg. Maximum concentration and area...
- **REVIEW** `cvn2184_phase3_dose_selection_charter.pdf`: carries 4 of 5 distinctive words of the committed call: 'Corvane should carry dovikizumab 300 mg IV at weeks 0, 4 and 8 into phase 3.'
- **REVIEW** `dovikizumab_investigators_brochure_section5.pdf`: carries 3 of 5 distinctive words of the committed call: 'Corvane should carry dovikizumab 300 mg IV at weeks 0, 4 and 8 into phase 3.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `cvn2184_201_sap_definitions_excerpt.pdf`: 3 of 25 stump-paragraph terms appear (window, record, events); read whether the document names the move
- **REVIEW** `cvn2184_phase3_dose_selection_charter.pdf`: 3 of 25 stump-paragraph terms appear (points, record, exposure-response); read whether the document names the move
- **REVIEW** `dovikizumab_investigators_brochure_section5.pdf`: 3 of 25 stump-paragraph terms appear (clearance, population, effect); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Three isolated Sonnet readers at medium effort, each holding only fresh copies of prompt.txt and target/, one after each document change (zips 9920d79d, e3c93a97, 8ef4cd41). The answers below are the third reader's on the final documents; the first two agreed on every question.

1. Decisive step: no sentence announces it. The nearest is charter 4, "The charter does not prescribe the exposure measure; the analysis records its choice and its reasons", which says a choice exists and names no measure.
2. Ranking or scoring of the candidates: none. The HV-101 workbook is healthy-volunteer NCA only; the topline extract carries a local read and is superseded by the lock.
3. Files that only help the analyst: none (no readme, dictionary or how-to; the SAP excerpt and the run log are source documents).
4. Figure or name reading as the answer: none; the only candidate-like numbers are the prompt's doses and the charter's 5 points.
5. Filed sentence fixing the computation: charter 4 (the model's form and the exposure-response analysis set, the patients with the chosen exposure value) and charter 5 (the lowest candidate within 5 points of the highest, compared unrounded); literal execution leaves the exposure measure open.
6. What decides the main answer: an analytical choice, which exposure measure goes into the model; SAP 6.8's handling and the rejected runs are rule application feeding it.
7. (third reader only) SAP 6.3 says an event's later records are one event and its latest record its current form, without saying how to find a chain; no sentence maps antibody tubes or handsets to patients.

Rulings on the REVIEW lines, read by the readers with figures withheld: "the model" in charter 4, harmless (ordinary protocol wording, defined in the next sentence, no measure or result); the charter's numbers shared with the answer, harmless (the candidate doses and the rule, stated inputs); the brochure's two numbers, harmless (phase 1 facts, not phase 2b outputs); words shared with the recommendation sentence, harmless (the question's own vocabulary). The three stump-vocabulary lines were ruled in the main thread: the SAP excerpt (window, record, events), the charter (points, record, exposure-response) and the brochure (clearance, population, effect) use those words in their own definitions and name no exposure measure; harmless.

Realism tells raised and fixed: the charter's records clause dated after its adoption (now "at its lock, planned for July 2026"); antibody run numbers out of date order (now numbered in run order). Left as is: short excerpts of the brochure and charter (they are excerpts), a tidy run log and lock file (an export's own form).
