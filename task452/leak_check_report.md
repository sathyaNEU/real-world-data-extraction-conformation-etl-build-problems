# leak check, task452

**Verdict: REVIEW.** 11 files read, 13 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: reference, sample, points, design, forest, stratum, deforestation, report, hectares, agreement, preliminary, strata, period, emission, payment, estimator, laboratory, clinker, monitoring, method, decisive, balance, ledger, reporting, nearest

## 1 file names (REVIEW 1)
- **REVIEW** `DCS_event_journal_2026.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `IEL-1186-03_conditions_consolidated_2026.pdf`: 9 of 25 stump-paragraph terms appear (reference, points, report, period, emission, laboratory); read whether the document names the move
- **REVIEW** `stack_tests_Hg_2024-2026.pdf`: 7 of 25 stump-paragraph terms appear (reference, report, emission, laboratory, clinker, monitoring); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (the isolated leak reader, two rounds)

Every REVIEW line above is ruled harmless by the reader in each round; neither round found a ranking file, a helper file or a figure that reads as the answer, and both answered question 6 with an analytical choice. Both named licence condition 5.6's two operating modes as the nearest pointer, a mild vocabulary hint that stays as the filed WHAT.

### Leak reader, round 1 (2026-11-01, isolated, Sonnet at medium effort, on target.zip sha256 3c2e3b88)

1. Decisive step: partly, in one filed sentence: licence condition 5.6 ("The mass is the mercury released over every hour each kiln fires, in compound operation and in direct operation"), with 1.4 and 1.5 defining the modes and 6.4 ("determined for every hour of the year"); they tell the analyst direct hours count, not that direct-operation mercury differs; the stack tests, all at "Raw mill: in operation", show only that the tested condition is compound.
2. Nothing ranks or scores kilns or options; no file gives a carbon-injection verdict.
3. No helper file (distractors or genuine inputs only).
4. Nothing reads as the answer (85 kg is the licence limit; the stack tests' g/h are compound-mode context).
5. Condition 5.6 (both kilns' mercury over every firing hour, both modes, the calendar year, against 85 kg), 6.4 and 1.7 fix the population and window, not how direct-mode mercury is estimated.
6. An analytical choice: how mercury is estimated for the direct hours the stack tests never sampled (the pack gives the mercury inputs and outputs); its caution: 5.6 and the mode definitions come close to announcing that direct hours matter, without saying what to compute.
Sweep flags: the DCS journal reads as an operator-station archive export (harmless); the licence carries the strongest hint (a mild one, licence wording, no method); the stack test report is harmless (plain lab format).
Realism: none (system-export features throughout; the ledger's two half-year layouts differ as a real organisation's would).

### Leak reader, round 2 (2026-11-01, isolated, Sonnet at medium effort, on target.zip sha256 3b551682)

1. Decisive step: hinted, not announced: licence condition 5.6 (mercury over every hour each kiln fires, in compound and in direct operation), 1.4 and 1.5 (the modes), 6.4 (every hour of the year); the stack tests all at "Raw mill: in operation"; the prompt's "hours in direct operation" ask.
2. Nothing ranks or scores anything.
3. No help-only file (context and distractors).
4. Nothing reads as the answer (the stack tests' g/h are context).
5. Condition 5.6 (both kilns' mercury over every firing hour, compound plus direct, the calendar year, against 85 kg), 1.8 (hours as summed elapsed time), 1.7 (Irish local time), 6.5 (hours of operation as producing clinker).
6. An analytical choice: seeing that the compound-operation level does not hold when the raw mill stops, so a flat extrapolation of the tests is wrong; 5.6 states the population, not how to estimate direct-operation mercury; the hours and NOx asks turn on definitions and data semantics, asks only.
Sweep flags: the DCS journal harmless (an operator-station export, raw events only); the licence a mild leak by vocabulary (it defines the modes and says the cap covers both: the WHAT, not the HOW; acceptable); the stack test report harmless.
Realism: the DCS journal slightly mechanical (raw mill stops near 17:00 and starts near 19:00 almost daily, plausible peak-tariff practice; tidy feed lines at 06:00 and 18:00); the rest reads as exports (the ledger's two half-year layouts read as genuine mess).

