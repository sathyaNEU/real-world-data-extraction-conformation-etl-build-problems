# leak check, task240

**Verdict: REVIEW.** 12 files read, 65 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: weights, published, variance, sampling, weighting, post-stratified, population, decisive, estimator, standard, residuals, strata, method, nothing, totals, adults, design, default, linearisation, asserted, golden, regions, calibration, question, outcome

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `ssb_qs7_statistical_quality_standard.pdf`: golden figure 20.0 appears: ...heir strata. 3.3 A published estimate whose CV is 20.0 per cent or more carries the low-reliability warn...
- **REVIEW** `ssb_qs7_statistical_quality_standard.pdf`: golden figure 2.2 appears: ...describes. Estimates are published in thousands. 2.2 Estimates are published for the twelve health reg...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `hrs27_fieldwork_closeout.docx`: 3 of 25 stump-paragraph terms appear (weights, population, outcome); read whether the document names the move
- **REVIEW** `hrs27_weighting_note.docx`: 7 of 25 stump-paragraph terms appear (weights, weighting, post-stratified, population, strata, adults); read whether the document names the move
- **REVIEW** `ssb_qs7_statistical_quality_standard.pdf`: 11 of 25 stump-paragraph terms appear (weights, published, sampling, weighting, standard, strata); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 40% of 196 prompts (cap 30%); reword at the role level, not the verb

## 12 describing content (REVIEW 1)
- **REVIEW** `ssb_qs7_statistical_quality_standard.pdf`: names 4 column(s) of the data files verbatim (adults, proxy, question, region): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)


## Solver's-eye read

One isolated read (Sonnet, medium, the prompt and the twelve files only), 2026-11-01 re-check.

1. Decisive step: none. Closest quoted: QS-7 3.2 (Taylor linearisation over the strata and PSUs, with replacement), read as the standard's general method, not a hint.
2. Ranking or scoring file: none.
3. File that exists only to help the analyst: none; the questionnaire workbook reads as the organisation's own instrument.
4. Figure or name reading as the answer: none.
5. Filed sentences: QS-7 2.1, 2.3, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3; the reader noted that 3.2 does not say how the post-stratification enters the variance, the step left to the analyst.
6. An analytical choice (whether the variance reflects the post-stratification of the weights); the asks are rule application, which the asks are allowed to be.

REVIEW lines: the standard's two figures are its own parameters (harmless); the "which" quota is corpus-level (harmless); the standard names four headers as ordinary words in the Branch's own standard (harmless). Stump-vocabulary lines (sweep 4) ruled in the main thread: the weighting note, the standard and the close-out use the words of how the weights were made and what is published, and none names the variance step (asserted in checks.py). Realism: the close-out read as slightly templated; nothing placed to be caught. Ambiguities raised (addresses with no outcome row, not-asked codes, children on the rosters) each close in QS-7 4.2, the questionnaire's "asked of" column and the weighting note.
