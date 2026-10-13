# leak check, task187

**Verdict: REVIEW.** 14 files read, 14 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: turbulence, shortfall, warranted, record, decisive, ten-minute, comparison, default, partial-load, matched, standard, erosion, eroded, nacelle, generator, spread, exchange, sentence, normal, operation, inside, capped, effect, repeated, recovers

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `OM-07_blade_campaigns_and_lost_production.pdf`: carries 11 of 13 distinctive words of the committed call: 'Book the summer 2027 leading-edge repair campaign on CH04; the repaired blades should recover 100 MWh (to the nearest 50'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `OM-07_blade_campaigns_and_lost_production.pdf`: 6 of 25 stump-paragraph terms appear (warranted, record, ten-minute, standard, normal, operation); read whether the document names the move
- **REVIEW** `TSA_schedule_3_warranted_power_curve.pdf`: 3 of 25 stump-paragraph terms appear (warranted, ten-minute, standard); read whether the document names the move
- **REVIEW** `extract_notes_2026-10-09.txt`: 5 of 25 stump-paragraph terms appear (warranted, record, ten-minute, standard, nacelle); read whether the document names the move

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

Isolated reader (Sonnet, medium) on prompt.txt and an unzip of target.zip only.

1. No sentence tells the decisive step. OM-07 2.4 and 2.5 fix the estimand (normal operation, the as-new counterfactual in the same winds, the blade-set window) and leave the as-new reference open; they point at no turbine.
2. No file ranks the turbines on the campaign. lost_production_2024_25.xlsx ranks last year's downtime and curtailment, a different question (a declared distractor); the monthly production report is energy only.
3. None exists only to help the analyst.
4. Nothing reads as the answer; the CH09 rotor exchange in the crane log and work orders is context for OM-07 2.5.
5. OM-07 2.4 to 2.6 with 3.1: each turbine's state 10 and 20 intervals in the twelve months, CH09 from its pool rotor, the as-new reference left to the analyst.
6. An analytical choice decides (the as-new baseline); 2.5 and 3.1 are rule-following on lower rungs. Clause 4.6's mast-wind potential is scoped to downtime and curtailment intervals.

REVIEW verdicts: R1 (OM-07 carries the call's vocabulary) harmless, the governing standard names no turbine or figure. R2 (domain words in OM-07, the schedule and the notes) harmless, none names a move.

Realism findings, fixed in the generator: a hub serial shared by CH08 and CH09; CH09's register blades outside the farm's series; serials running too evenly; one summary on every corrective work order; a blade-condition note in the crane log; an OM-07 revision entry naming clause 2.5.

## Solver's-eye read (second pass, the changed files)

The crane log, the asset register, OM-07 and the work orders after the fixes: no decisive-step sentence and no pointer to a turbine; no repeated serial (hubs and blades in commissioning batches, the pool rotor outside the range); no text written by someone who knows the answer. Remaining minor note: every turbine shares one commissioning date, kept (one project, one handover).
