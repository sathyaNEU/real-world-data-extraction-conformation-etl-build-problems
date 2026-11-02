# leak check, task149

**Verdict: REVIEW.** 18 files read, 44 golden figures and 20 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: standard, exposure, worked, method, standards, engineered, twelve, asserted, injury, window, decisive, history, population, nothing, latest, months, schedule, readable, golden, rejected, decision, forecasting, burden, planned, shifted

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `lindqvist_program_agreement_fy2027_draft.pdf`: golden figure 140 appears: ...edule B - Program Fee B1 The Program Fee is USD 2,140 per Forecast Recordable Case. B2.1 Forecast Recor...
- **REVIEW** `export_notes.txt`: carries 5 of 8 distinctive words of the committed call: 'The twenty ergonomics program DCs will log about 1,000 recordable cases in fiscal 2027 under the FY2027 operating plan.'
- **REVIEW** `lindqvist_program_agreement_fy2027_draft.pdf`: carries 7 of 8 distinctive words of the committed call: 'The twenty ergonomics program DCs will log about 1,000 recordable cases in fiscal 2027 under the FY2027 operating plan.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `EHS-RK-01_osha_recordkeeping_procedure_rev7.pdf`: 3 of 25 stump-paragraph terms appear (worked, injury, schedule); read whether the document names the move
- **REVIEW** `lindqvist_program_agreement_fy2027_draft.pdf`: 4 of 25 stump-paragraph terms appear (twelve, injury, history, schedule); read whether the document names the move

## 6 ranking artifacts (REVIEW 6, INFO 1)
- **REVIEW** `ehs_legacy_case_export_fy21_2024-06-30.csv`: names 20 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `ehs_platform_cases_2024-07-01_2026-11-02.json`: names 20 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `fy2027_operating_plan_v3.xlsx`: names 20 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `ie_engineered_labor_standards.xlsx`: names 20 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `lindqvist_program_agreement_fy2027_draft.pdf`: names 20 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `wc_loss_run_valued_2026-09-30.xlsx`: names 20 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `site_register_2026-11-02.csv`: names 20 of 20 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `fy2027_operating_plan_v3.xlsx`: 24 ISO dates after 2026-11-02, e.g. 2026-12-27, 2027-01-23, 2027-01-24, 2027-02-20, 2027-02-21

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Three rounds by an isolated reader at medium effort, each on a fresh copy of `prompt.txt` and `target/` only.

- **Round 1, the stage 3 cut (bc83c300).** Clean: no sentence or file names the decisive step, nothing ranks the twenty
  DCs on fiscal 2027 cases, no figure reads as the answer. Q6 analytical (the forecast turns on modelling the rate per
  hour against pace, not on a field, a rule or a plant).
- **Round 2, targeted re-read of the repair cut (eaec660f).** No leak, Q6 analytical. It flagged text that read as
  authored and made the asks easier: Schedule B 2.2's "volumes and labor hours" tail, B3's fee sentence, a data-request
  clause that listed exactly the two asked tables, EHS-RK-01 sections 5 to 7 and its revision line, and the Rockford
  re-numbering told in three places. All of it was rewritten in the generator for the realism cut.
- **Round 3, targeted re-read of the realism cut (b45b1fc0).** Clean: no leak, no ranking, no answer figure. Q6
  analytical.

Rulings on the REVIEW lines and the readers' notes:
- EHS-RK-01 sections 8 and 9 and the agreement's clause 4 data list are ordinary procedure and procurement text. They
  name no method; harmless.
- The thin rev 7 procedure is a residual realism risk, accepted.
- The ask readings close in shipped files, and the judge reproduced each: days are counted through 10/31/2026 inclusive
  under EHS-RK-01 section 9; the fiscal calendar comes from the WFM notes (fiscal years end on the last Saturday of
  December); period 11 is week 44 only (the export notes' line on the SKU pick file).
- The sweep 3, 4, 6 and 9 lines above are answered one by one in the design note's `## Leak review`; all are harmless.
