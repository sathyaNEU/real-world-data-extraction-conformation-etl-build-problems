# leak check, task268

**Verdict: REVIEW.** 13 files read, 25 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: registry, patient, gullhaven, fennick, follow-up, censoring, record, decisive, kaplan-meier, deaths, survey, estimator, recorded, product-limit, linkage, carried, followed, estimand, nothing, brenmoor, crosswalk, weighted, manual, reader, clinical

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `hf_early_diagnosis_programme_charter_2027.pdf`: carries 7 of 8 distinctive words of the committed call: 'Host the 2027 heart failure early-diagnosis programme at Gullhaven Hospital.'
- **REVIEW** `pack_contents.txt`: carries 7 of 8 distinctive words of the committed call: 'Host the 2027 heart failure early-diagnosis programme at Gullhaven Hospital.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `hf_early_diagnosis_programme_charter_2027.pdf`: 3 of 25 stump-paragraph terms appear (registry, patient, manual); read whether the document names the move
- **REVIEW** `hf_registry_manual_v5.pdf`: 11 of 25 stump-paragraph terms appear (registry, patient, follow-up, record, deaths, recorded); read whether the document names the move
- **REVIEW** `pack_contents.txt`: 6 of 25 stump-paragraph terms appear (registry, patient, record, deaths, linkage, manual); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 1)
- **REVIEW** `echo_lab_activity_2025.xlsx`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `hospital_reference.xlsx`: names 5 of 6 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `hf_clinic_sessions_2026.csv`: 41 ISO dates after 2026-04-14, e.g. 2026-12-18

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Stage 4 reader, architecture 2, 2026-10-18 (one isolated agent, Sonnet at medium, reading only fresh copies of `prompt.txt` and `target/` from target.zip md5 b3e1bf737de8fdd5473b64363c88e918).

1. Decisive step: none named outright; the reader quotes plan 4.2 ("A ground's haddock stock in a year is the weight of haddock on its stock area") with the manual's "Each band has the same number of stations" as what sets it up.
2. Ranking file: none.
3. Helper file: the survey manual (station design, equal stations per band), the contents list and the two lookups (conversion factors, members' list), each read as ordinary documentation.
4. Answer-like figure or name: none; the plan's Annex A table of cells and areas read as context.
5. Plan 4.1 with 4.2: executed on the survey, the estimand is a stock over the whole area, giving Halmorie Deep at 63 per cent.
6. An analytical choice: the survey samples the three depth bands equally while the grounds' cells are not spread equally across them (Halmorie Deep 54 of 80 cells in band A), so the bands are weighted by area; the reader names plan 4.2 and the grid file as what set it up.

REVIEW lines: all nine harmless (the 100 is the band limit "A under 100 m"; the plan names the grounds and the closure rule and chooses none; the manual, gear trial note, rules and contents list use generic survey words and name no move; the grid and the plan's Annex A list cells and areas and rank nothing). Realism: nothing generated; the reader notes the survey's flat 216 tows a year and every tow at 30 minutes as fitting a fixed-station survey.

The reader never weighed the members' logbooks as a stock measure: it went to the survey first and took the area weights from the plan's estimand and the manual's equal allocation, rejecting the plain mean of the tows (Brettach Bank first) in passing.

Score (`score_reader.py task268`): the call 5 of 5 (Halmorie Deep, Brettach Bank, 63, 52, 11); every ground's fall 6 of 6; asks A and B 0 of 13 (each port's tonnes and value high by the re-issued notes, each pool high by its pool-level allocation). Exit 1: the reader landed the call, Gate F failed, architecture 2 spent.

## Solver's-eye read

Round 1 (2026-10-19, the pack before the stage-4 fix pass; one isolated reader, cold, medium effort).
- Q1 (decisive step): the charter's 3.2 ("Every patient newly diagnosed at the hospital in those years counts, including patients the registry no longer follows") with the manual's 4.3 and 4.4 ("the registry holds nothing on them after it"); neither names a method. Harmless: the estimand, filed by design.
- Q2 (a file ranking the candidates): none.
- Q3 (files only to help the analyst): pack_contents.txt, the hospital reference's Notes sheet (the North Campus's specimens go to the main laboratory), the crosswalk. Harmless: an index and two ordinary registers of a health system.
- Q4 (a figure reading as the answer): none.
- Q5 (literal reading): the charter's 3.2 read with no death on file as alive gives Fennick (the crude rung, R0); the manual's 4.3 and 4.4 say the registry holds nothing after a loss, so silence is not survival.
- Q6 (what decides): an analytical choice, how to treat the patients who left follow-up.
- Q7 (realism): none; the exchange file and the re-enrolments read as tidy but consistent.
- REVIEW lines: all six harmless (the charter and contents list name the programme, the manual names no method, the echocardiography workbook ranks nothing on survival, the 2026 timetable is a forward schedule).
- Its figures: the call missed (Fennick, Kaplan-Meier); Ask A none of ten; Ask B ten of ten (the re-enrolments found through the crosswalk); four of five survival figures. Fixed in one generator pass (design note, Build record): Ask B's primary re-sited, Brenmoor's mix moved so the default path's gap prints 1.
