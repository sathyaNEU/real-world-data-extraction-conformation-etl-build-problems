# leak check, task473

**Verdict: LEAK.** 18 files read, 48 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: drivers, tested, agencies, arrest, guidelines, untested, corwin, ossian, asserted, surviving, hatchell, decisive, records, agency, center, complete, patrol, killed, certifies, unarrested, sheriffs, manual, result, pruett, readable

## 1 file names (LEAK 2, REVIEW 3)
- **LEAK** `crs_extract_notes_2025.pdf`: a file whose name says it describes the data (extract_notes): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **LEAK** `stl_extract_notes.txt`: a file whose name says it describes the data (extract_notes): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **REVIEW** `dmv_licensed_drivers_by_county_2025.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `dot_county_dvmt_2023_2025.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `fcc_agency_directory.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `ghso_fy2028_county_task_force_guidelines.pdf`: carries 8 of 12 distinctive words of the committed call: 'Corwin, Hatchell, Ossian and Tanager are high-range for the FY2028 County Impaired Driving Task Force grants.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `crs_extract_notes_2025.pdf`: 4 of 25 stump-paragraph terms appear (records, agency, center, killed); read whether the document names the move
- **REVIEW** `fcc_reference_manual_2024_ed.pdf`: 14 of 25 stump-paragraph terms appear (drivers, tested, arrest, corwin, ossian, surviving); read whether the document names the move
- **REVIEW** `ghso_fy2028_county_task_force_guidelines.pdf`: 10 of 25 stump-paragraph terms appear (drivers, tested, agencies, arrest, guidelines, records); read whether the document names the move
- **REVIEW** `stl_extract_notes.txt`: 6 of 25 stump-paragraph terms appear (arrest, records, agency, center, patrol, result); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: no data count disclosed: each of the N: "Which of our 14"; the N things: "our 14 counties"; the N things: "the 14 rates" (a count the data hold is the model's to find; drop it or keep only the decision parameter)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 35% of 196 prompts (cap 30%); rounding opener 'give' at 46% of 196 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (LEAK 3)
- **LEAK** `crs_extract_notes_2025.pdf`: names 27 column(s) of the data files verbatim, 100% of crs_reports_2025.csv: a document that lists the data's columns describes the data whatever its name (dataset-generation section 3); the WHAT belongs in a governing document in the organisation's own genre, which names observables and never the files' fields
- **LEAK** `fcc_reference_manual_2024_ed.pdf`: names 58 column(s) of the data files verbatim, 100% of fcc_2023_crash.csv: a document that lists the data's columns describes the data whatever its name (dataset-generation section 3); the WHAT belongs in a governing document in the organisation's own genre, which names observables and never the files' fields
- **LEAK** `stl_extract_notes.txt`: names 15 column(s) of the data files verbatim, 93% of stl_specimen_extract_2023_2025.csv: a document that lists the data's columns describes the data whatever its name (dataset-generation section 3); the WHAT belongs in a governing document in the organisation's own genre, which names observables and never the files' fields

## 13 task metadata (REVIEW 1)
- **REVIEW** `metadata.json`: subdomain shares the design note's stump vocabulary (drivers, tested, agencies, arrest, surviving): say what the task decides, not how

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)
