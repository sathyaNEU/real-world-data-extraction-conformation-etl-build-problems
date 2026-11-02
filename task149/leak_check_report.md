# leak check, task149

**Verdict: LEAK.** 13 files read, 11 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: census, forecast, journey, section, lisnagry, review, rejected, decisive, forecasting, decision, weekdays, shares, window, driver, persons, family, factor, method, default, quantity, counts, construction, golden, inside, population

## 1 file names (LEAK 1)
- **LEAK** `vantra_resident_panel_extract_notes.pdf`: a file whose name says it describes the data (extract_notes): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)

## 3 answer figures in the pack (LEAK 1, REVIEW 1)
- **LEAK** `rathgarvan_fbc_demand_refresh_dec2027.pdf`: golden figure 1,400 appears: ...Mill Road) is justified where the station carries 1,400 or more commuter boardings on an average ordinary...
- **REVIEW** `rathgarvan_fbc_demand_refresh_dec2027.pdf`: carries 10 of 14 distinctive words of the committed call: 'Rathgarvan will carry about 1,300 commuter boardings on an average ordinary weekday in 2029 (to the nearest 100), below '

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `lisnagry_opening_review_apr2020.pdf`: 7 of 25 stump-paragraph terms appear (census, forecast, journey, lisnagry, review, weekdays); read whether the document names the move
- **REVIEW** `rathgarvan_fbc_demand_refresh_dec2027.pdf`: 6 of 25 stump-paragraph terms appear (census, journey, lisnagry, review, decision, persons); read whether the document names the move
- **REVIEW** `vantra_resident_panel_extract_notes.pdf`: 3 of 25 stump-paragraph terms appear (window, counts, population); read whether the document names the move

## 6 ranking artifacts (REVIEW 3, INFO 2)
- **REVIEW** `census2022_pow_rathgarvan_catchment.xlsx`: names 4 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `kilcarrow_employment_outlook_2030.docx`: names 4 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rathgarvan_fbc_demand_refresh_dec2027.pdf`: names 4 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `ardnagree_line_station_register.csv`: names 4 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `cell_zone_lookup_v3.csv`: names 4 of 6 answer-set candidates; confirm it does not rank them on the decision question

## 8 column names (REVIEW 2)
- **REVIEW** `mobility_devices_2027w36_w47.csv`: columns a generator names and an organisation does not: device_id
- **REVIEW** `mobility_stays_2027w36_w47.csv`: columns a generator names and an organisation does not: device_id

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (LEAK 1)
- **LEAK** `vantra_resident_panel_extract_notes.pdf`: names 13 column(s) of the data files verbatim: a document that lists the data's columns describes the data whatever its name (dataset-generation section 3); the WHAT belongs in a governing document in the organisation's own genre, which names observables and never the files' fields

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)
