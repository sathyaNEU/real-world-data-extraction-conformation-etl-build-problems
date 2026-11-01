# leak check, task458

**Verdict: LEAK.** 16 files read, 143 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: member, full-year, enrolled, window, identified, prevalence, counts, months, observed, decisive, design, golden, seasonal, enrollment, population, ratios, october, identifies, sensitivity, yakima, question, generator, reader, policy, estimate

## 1 file names (LEAK 2, REVIEW 1)
- **LEAK** `extract_manifest_2026-11-12.csv`: a file whose name says it describes the data (manifest): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **LEAK** `network_analytics_data_dictionary.xlsx`: a file whose name says it describes the data (data_dictionary): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **REVIEW** `network_analytics_data_dictionary.xlsx`: a sheet named 'Columns': confirm it is the organisation's own notes and does not describe the data's columns or files

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `np31_prescriber_service_area_designation.pdf`: golden figure 3.2 appears: ...ber in the contract year. Threshold: 68 per cent. 3.2 A county fails a standard when its value is belo...
- **REVIEW** `np31_prescriber_service_area_designation.pdf`: carries 10 of 11 distinctive words of the committed call: 'The board should designate Adams, Douglas, Franklin, Grant and Okanogan for the 2027 Prescriber Service Award Pilot.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `np31_prescriber_service_area_designation.pdf`: 11 of 25 stump-paragraph terms appear (member, enrolled, counts, months, design, enrollment); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Put the designation in prescriber_pilot_county_scorecard_2027.xlsx with, for each of the ten counties, its practising prescribers, its adult members with a serious mental illness and with an opioid use disorder, whether '

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: no data count disclosed: each of the N: "Which of our ten"; each of the N: "each of the ten"; each of the N: "each of the three"; the N things: "our ten counties"; the N things: "the ten counties"; the N things: "the three standards" (a count the data hold is the model's to find; drop it or keep only the decision parameter)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 35% of 196 prompts (cap 30%); second-sentence opener 'put' at 36% of 196 prompts (cap 20%); reword at the role level, not the verb

## 13 task metadata (REVIEW 1)
- **REVIEW** `metadata.json`: subdomain shares the design note's stump vocabulary (member, enrolled, prevalence, enrollment, ratios): say what the task decides, not how

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)
