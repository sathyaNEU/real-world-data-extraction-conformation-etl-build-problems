# leak check, task501

**Verdict: LEAK.** 21 files read, 20 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: diaries, matrix, survey, contacts, school, contact, eigenvalue, method, regime, term-time, million, decisive, susceptible, immune, public, periods, season, window, golden, reflex, population, next-generation, summer, fieldwork, standard

## 1 file names (LEAK 3, REVIEW 1)
- **LEAK** `nds_case_export_fields.txt`: a file whose name says it describes the data (nds_case_export_fields): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **LEAK** `nscs_2023_public_file_codebook.xlsx`: a file whose name says it describes the data (codebook): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **LEAK** `register_extract_notes_2027-07.docx`: a file whose name says it describes the data (extract_notes): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **REVIEW** `nscs_2023_public_file_codebook.xlsx`: a sheet named 'About': confirm it is the organisation's own notes and does not describe the data's columns or files

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `mmr_catch_up_options_autumn_2027.pdf`: carries 8 of 11 distinctive words of the committed call: "We should fund option B, the MMR catch-up for those born 2008 to 2012: it is the only option that brings measles' reprod"
- **REVIEW** `ps07_measles_winter_planning_standard.pdf`: carries 9 of 11 distinctive words of the committed call: "We should fund option B, the MMR catch-up for those born 2008 to 2012: it is the only option that brings measles' reprod"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `mmr_catch_up_options_autumn_2027.pdf`: 4 of 25 stump-paragraph terms appear (school, susceptible, immune, public); read whether the document names the move
- **REVIEW** `ps07_measles_winter_planning_standard.pdf`: 5 of 25 stump-paragraph terms appear (immune, public, season, population, standard); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 35% of 196 prompts (cap 30%); second-sentence opener 'put' at 36% of 196 prompts (cap 20%); rounding opener 'give' at 46% of 196 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (LEAK 2)
- **LEAK** `nds_case_export_fields.txt`: names 13 column(s) of the data files verbatim, 100% of nds_measles_cases_oriel_2019-2027.csv: a document that lists the data's columns describes the data whatever its name (dataset-generation section 3); the WHAT belongs in a governing document in the organisation's own genre, which names observables and never the files' fields
- **LEAK** `register_extract_notes_2027-07.docx`: names 16 column(s) of the data files verbatim, 100% of register_people_active_born_1993-2017.csv: a document that lists the data's columns describes the data whatever its name (dataset-generation section 3); the WHAT belongs in a governing document in the organisation's own genre, which names observables and never the files' fields

## 13 task metadata (REVIEW 1)
- **REVIEW** `metadata.json`: subdomain shares the design note's stump vocabulary (matrix, eigenvalue, next-generation): say what the task decides, not how

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Q1 to Q4: none (PS-07 3.1 and 3.2 define the reproduction number and R0 without a method; the options paper ranks nothing on R and its "expected made immune" figures are filed inputs; every file reads as an office file or licensed reference data). Q5: PS-07 3.3 to 3.6; read literally with population-average mixing the reader got R 0.72 with no catch-up (no catch-up needed), the R0-times-susceptible-share rung, below the golden: it did not build the age-structured matrix. Q6: an analytical choice (how R is computed, homogeneous or age-structured, and which immunity goes in). Readings: the method for R is unfiled (by design: the data and the field's method force it; the judge to rule); the profile's open-ended bands; option E's overlap with D on the chart; residents at 30 June against moved-away records still active; imported against import-related; migrated duplicate cases. Realism: the options paper's budget sentence slightly editorial; uniform stock-return batch numbers; a docx thumbnail and customXml part to scrub. REVIEW lines: all harmless (shared vocabulary, future vaccine expiry dates).
