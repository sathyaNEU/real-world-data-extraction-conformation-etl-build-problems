# leak check, task182

**Verdict: REVIEW.** 11 files read, 57 golden figures and 20 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: reference, network, levels, logger, reading, climate, measures, written, drawdown, killed, family, nothing, fitted, record, monthly, asserted, objective, organisation, outside, decisive, analyst, basalt, alluvium, coal-measure, harmless

## 3 answer figures in the pack (REVIEW 15)
- **REVIEW** `MG-02_bore_assessment_and_make_good.pdf`: golden figure 2.4 appears: ...r air pressure, over the day in Queensland time. 2.4 A bore's assessment level is the mean of its sta...
- **REVIEW** `MG-02_bore_assessment_and_make_good.pdf`: golden figure 1.1 appears: ...ger, Kelvale Mine March 2028 1 Purpose and scope 1.1 This procedure sets how Kelvale Mine assesses la...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 238.12 appears: ...12:00:00,238.11,24.44 2041956,2017-08-25 13:00:00,238.12,24.44 2041956,2017-08-25 14:00:00,238.104,24.45 2...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 204.86 appears: ...1:00:00,204.889,24.76 2041881,2018-09-20 12:00:00,204.86,24.75 2041881,2018-09-20 13:00:00,204.913,24.75 2...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 241.33 appears: ...0:00:00,241.307,24.23 2041902,2020-08-07 11:00:00,241.33,24.23 2041902,2020-08-07 12:00:00,241.316,24.24 2...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 203.49 appears: ...6:00:00,203.439,24.76 2041881,2018-10-27 07:00:00,203.49,24.75 2041881,2018-10-27 08:00:00,203.396,24.76 2...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 199.16 appears: ...8:00:00,199.209,24.64 2041873,2018-07-27 19:00:00,199.16,24.64 2041873,2018-07-27 20:00:00,199.15,24.64 20...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 209.84 appears: ...9:00:00,209.757,24.63 2041873,2015-06-30 20:00:00,209.84,24.62 2041873,2015-06-30 21:00:00,209.796,24.62 2...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 243.13 appears: ...3:00:00,243.234,24.05 2041925,2020-07-20 00:00:00,243.13,24.05 2041925,2020-07-20 01:00:00,243.217,24.05 2...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 195.44 appears: ...7:00:00,195.579,24.35 2041890,2019-06-05 18:00:00,195.44,24.34 2041890,2019-06-05 19:00:00,195.373,24.34 2...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 209.61 appears: ...9:00:00,209.657,24.61 2041873,2015-06-05 10:00:00,209.61,24.62 2041873,2015-06-05 11:00:00,209.662,24.61 2...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 202.33 appears: ...1:00:00,202.222,24.35 2041890,2017-09-29 22:00:00,202.33,24.34 2041890,2017-09-29 23:00:00,202.364,24.35 2...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 201.88 appears: ...07:00:00,201.83,24.64 2041873,2018-05-05 08:00:00,201.88,24.64 2041873,2018-05-05 09:00:00,201.971,24.64 2...
- **REVIEW** `logger_pressure_2015-2026.parquet`: golden figure 209.51 appears: ...7:00:00,209.518,24.62 2041873,2015-06-06 08:00:00,209.51,24.62 2041873,2015-06-06 09:00:00,209.447,24.61 2...
- **REVIEW** `logger_pressure_2015-2026.parquet`: and 5 more golden figures

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `MG-02_bore_assessment_and_make_good.pdf`: 8 of 25 stump-paragraph terms appear (reference, network, levels, logger, reading, measures); read whether the document names the move
- **REVIEW** `monitoring_network_notes.md`: 11 of 25 stump-paragraph terms appear (reference, network, levels, logger, reading, climate); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `landholder_bore_register.xlsx`: names 20 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `landholder_contact_log_2026.xlsx`: names 13 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt form (clean)

## Solver's-eye read

Pass 1: one isolated reader on Sonnet, 2026-10-11, relaunched after a session restart.

1. **none.** The nearest is MG-02 4.1, "A decline with another cause is not the mine's." It restates the prompt's
   "decline the mine's take has caused". No file says how to separate the mine's share from the rainfall response,
   or that the coal measures lag rainfall by years.
2. **none.** The register "holds no current water levels and no assessment results", and no file ranks the bores or
   states a level, change, decline or yes/no.
   - The coordinates allow only a proximity guess.
   - The five bores nearest the mine-bore ring (LB12, LB04, LB05, LB07, LB10) are the five its rough model finds
     impaired.
3. **`monitoring_network_notes.md`**, "the only file that exists to brief the analyst". It carries the field
   dictionary, the ft/m rule, the pump-off rule, the pressure-to-level recipe and the two measuring-point changes.
4. **none.** The nearest is "pump lowered by the landholder's contractor in July" (contact log, Saltbush Flat,
   6 Aug), the kind of line a real log carries.

**Plan (summarised).**
- Clean the site spellings and the feet rounds, and drop pumped dips.
- Take levels from the measuring point in force on the day, and compensate the loggers hour by hour in Queensland
  days.
- Fit each bore's record before dewatering (to June 2022) to a lagged, smoothed rainfall departure, and take
  modelled minus observed as the mine's decline. Check it on the reference bores and LB16.
- Its rough run:
  - 6.5 to 7.9 m at LB04, LB05, LB07 and LB10;
  - 3.6 to 4.0 m at LB12;
  - 0 to 1.6 m elsewhere.
- The raw change since baseline flags a different eight.

**REVIEW lines: all six harmless.**
- 2.4 and 1.1 in MG-02 are clause numbers.
- The kPa readings coincide with levels by chance, among about 1M rows.
- MG-02 and the notes use their own procedure and network vocabulary and never name the counterfactual.
- The register and the contact log hold inputs and complaints, and rank nothing.

**Realism notes (deferred to stage 6b or the hardening brief).**
- **Loggers:**
  - the MB03 logger is typed 0-300 kPa but reads up to 589.7;
  - logger temperatures are constant (25.40 and 25.70 C) and logger levels show no drift;
  - there is one outage only;
  - an LB05 battery comment is contradicted by the data.
- **Dips:**
  - feet rounds in 2012;
  - remarks drawn from a short fixed list ("windmill turning" on bores without a windmill).
- **Water quality:** sample_ids climb in steps of 7, there are no non-detects, and nothing moves at the pit bores.
- **Dewatering:** the meters have no outages, and AD03 and AD04 start later than the notes say.
- **Contact log:**
  - entries on weekends;
  - lines repeated verbatim;
  - a count of complainants that runs ahead of the log;
  - a dip the dips file does not hold.
- **MG-02:** effective on a Sunday, with a 08:30:00 creation stamp and no Water Act references.
- **Workbooks:** openpyxl signatures under an app.xml that says Excel, and a line in the register saying what it
  lacks.
