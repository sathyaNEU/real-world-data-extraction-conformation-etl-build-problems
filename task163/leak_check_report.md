# leak check, task163

**Verdict: LEAK.** 16 files read, 31 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: applications, closed, formations, months, cohorts, standard, formation, application, reform, release, window, comparison, filing, carried, go-live, business, decisive, latest, ordinary, estimand, statistics, quarters, nothing, regression, quantity

## 1 file names (LEAK 2, REVIEW 2)
- **LEAK** `pack_manifest.csv`: a file whose name says it describes the data (manifest): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **LEAK** `plan_pack_field_guide.xlsx`: a file whose name says it describes the data (field_guide): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **REVIEW** `plan_2027_workbook.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `plan_pack_field_guide.xlsx`: a sheet named 'Fields': confirm it is the organisation's own notes and does not describe the data's columns or files

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `plan_2027_sizing_standard.docx`: golden figure 100 appears: ...the line, which goes into the plan to the nearest 100. Sales operations keeps the share tab: each...
- **REVIEW** `plan_2027_sizing_standard.docx`: carries 10 of 11 distinctive words of the committed call: "Put 2,500 new first-time employers in the 2027 plan's first-time-employer line for the twelve core states."

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `plan_2027_sizing_standard.docx`: 10 of 25 stump-paragraph terms appear (applications, formations, months, formation, application, release); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: second-sentence opener 'put' at 36% of 196 prompts (cap 20%); reword at the role level, not the verb

## 13 task metadata (REVIEW 2)
- **REVIEW** `metadata.json`: title shares the design note's stump vocabulary (formation, application, filing): say what the task decides, not how
- **REVIEW** `metadata.json`: subdomain shares the design note's stump vocabulary (applications, formation, reform, filing, business): say what the task decides, not how

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)
