# leak check, task245

**Verdict: REVIEW.** 13 files read, 11 golden figures and 12 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: network, record, counts, bearing, decisive, percentile, scaling, quality, monitoring, source, driver, operator, background, losses, concentration, missing, section, population, analyser, decision, sentence, outcome, rebuilt, rebuild, procedure

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `tbc_aq_network_qaqc_procedure_v4.pdf`: carries 23 of 25 distinctive words of the committed call: 'Three stations go into the 2027 Annual Status Report with the data-capture note: North Gate (TBT1), Harbour Walk (TH3) a'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `DATA_DICTIONARY.md`: 8 of 25 stump-paragraph terms appear (network, record, source, operator, background, section); read whether the document names the move
- **REVIEW** `README.md`: 7 of 25 stump-paragraph terms appear (network, record, quality, monitoring, operator, background); read whether the document names the move
- **REVIEW** `asr2027_table_a3_no2_2026.pdf`: 4 of 25 stump-paragraph terms appear (quality, monitoring, background, concentration); read whether the document names the move
- **REVIEW** `tbc_aq_network_qaqc_procedure_v4.pdf`: 12 of 25 stump-paragraph terms appear (network, record, counts, quality, monitoring, source); read whether the document names the move

## 5 announcements (REVIEW 1)
- **REVIEW** `tbc_aq_network_qaqc_procedure_v4.pdf`: Where that count is 35 or fewer but the station's result for the year is more than 35, the station's result carries the data-capture note: the station cannot be reported as meeting the objective.

## 6 ranking artifacts (REVIEW 5, INFO 3)
- **REVIEW** `aq_network_service_log_2027.xlsx`: names 11 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `tbc_aq_network_qaqc_procedure_v4.pdf`: names 12 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `tbt_deposit_gauge_results_2027.xlsx`: names 5 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `tbt_pm10_permit_monitoring_2027.xlsx`: names 5 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `thornmouth_council_aq_hourly_2027.csv`: names 6 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `asr2027_table_a3_no2_2026.pdf`: names 6 of 12 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `tbt_dust_management_monitoring_plan_rev3.pdf`: names 5 of 12 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `thornmouth_aq_station_register.csv`: names 11 of 12 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Three isolated reads (Sonnet, medium, prompt.txt and target/ only), the first on the first cut and the second and third
after the one fix pass.

- Read 1, first cut. Q1: section 5.1 read as the move and found ambiguous (a day with no valid mean could count as an
  exceedance or as nothing). Q2 to Q4 none. Q5 and the fork notes: 5.1's lost days; Market Street's NO2 capture under
  75 per cent with the works, against last year's table's annualising note; the terminal's statuses against section
  2.4. Realism: the procedure a bare rule sheet, the service log templated, the deposit cells text, the terminal's
  quarters split on GMT. All fixed in the generator (5.1 now: such a day counts if the concentration at the station
  that day exceeded 50, and not otherwise; Market Street's NO2 analyser runs through the works; section 2.2 and the
  dictionary give the terminal's statuses as ratified; the procedure has document control, a calibration section, a
  station annex and a history; the log's notes vary; the deposit cells are numbers; the quarters follow the logger's
  clock).
- Read 2, after the fix. Q1 none beyond the estimand, Q2 to Q4 none, Q5 the estimand closed and the method open, Q6 an
  analytical choice; every REVIEW line harmless, section 5.2 a low-severity note on the call's shape (the stated
  criterion, not the stump). Realism: the register's tidy offsets from the stockyard; fixed (Ordnance Survey grid
  references with surveyed scatter, the background map on national grid squares, the plan's stockyard reference).
- Read 3, the final pack. Q1 none ("No sentence names it"), Q2 none, Q3 none (the background map a mild candidate, a
  named distractor and an ordinary ASR input), Q4 none, Q5 the population and window closed and the lost days'
  estimate open, Q6 an analytical choice. Every REVIEW line harmless: the procedure's vocabulary and 5.2 definition are
  its own subject; the dictionary, README and last year's table name no move; the service log, deposit results,
  workbook, export and the procedure's annex list stations and readings and rank nothing.
