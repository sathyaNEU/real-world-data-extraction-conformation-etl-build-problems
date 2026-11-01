# leak check, task247

**Verdict: LEAK.** 17 files read, 49 golden figures and 16 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: analysis, reference, filled, anomaly, station, observed, monitoring, regression, method, near-real-time, decisive, overlap, refill, temperature, observation, clear-sky, correction, repeat, provisional, observations, nothing, twelve, sentence, toward, refilling

## 1 file names (LEAK 2)
- **LEAK** `DATA_DICTIONARY.md`: a file whose name says it describes the data (DATA_DICTIONARY): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **LEAK** `README.md`: a file whose name says it describes the data (README): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)

## 4 design-note vocabulary (REVIEW 6)
- **REVIEW** `DATA_DICTIONARY.md`: 6 of 25 stump-paragraph terms appear (analysis, station, near-real-time, temperature, observation, repeat); read whether the document names the move
- **REVIEW** `README.md`: 5 of 25 stump-paragraph terms appear (analysis, station, monitoring, method, near-real-time); read whether the document names the move
- **REVIEW** `post_bleaching_survey_protocol_2023.pdf`: 3 of 25 stump-paragraph terms appear (station, monitoring, repeat); read whether the document names the move
- **REVIEW** `reef_heat_stress_watch_methods_v3.pdf`: 9 of 25 stump-paragraph terms appear (analysis, reference, station, monitoring, method, near-real-time); read whether the document names the move
- **REVIEW** `srao_nrt_sst_user_guide_v3_2.pdf`: 6 of 25 stump-paragraph terms appear (analysis, observed, near-real-time, temperature, observation, observations); read whether the document names the move
- **REVIEW** `srao_reprocessed_sst_release_note_2027-05.pdf`: 4 of 25 stump-paragraph terms appear (analysis, reference, near-real-time, temperature); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 1)
- **REVIEW** `heat_stress_bulletins_2027.xlsx`: names 16 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `watch_sites_register.csv`: names 15 of 16 answer-set candidates; confirm it does not rank them on the decision question

## 8 column names (REVIEW 1)
- **REVIEW** `srao_nrt_sst_extract_watch_pixels_2018-01-01_2027-11-02.csv`: columns a generator names and an organisation does not: obs_flag

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: no data count disclosed: each of the N: "Which of our 16" (a count the data hold is the model's to find; drop it or keep only the decision parameter)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 35% of 196 prompts (cap 30%); reword at the role level, not the verb

## 12 describing content (LEAK 1, REVIEW 1)
- **LEAK** `DATA_DICTIONARY.md`: names 38 column(s) of the data files verbatim, 100% of logger_log_2023-08_2027-04.csv: a document that lists the data's columns describes the data whatever its name (dataset-generation section 3); the WHAT belongs in a governing document in the organisation's own genre, which names observables and never the files' fields
- **REVIEW** `post_bleaching_survey_protocol_2023.pdf`: names 8 column(s) of the data files verbatim (Issued, condition, genus, line, metre, observer): confirm it is the organisation's own record and not a note written for the analyst

## 13 task metadata (REVIEW 2)
- **REVIEW** `metadata.json`: title shares the design note's stump vocabulary (station, near-real-time, temperature): say what the task decides, not how
- **REVIEW** `metadata.json`: subdomain shares the design note's stump vocabulary (monitoring, near-real-time, temperature): say what the task decides, not how

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)


## Solver's-eye read

One isolated reader (Sonnet, medium), the prompt and a fresh copy of the pack only, on the first cut.
1. The decisive step: no sentence names it; the methods note's section 6 and the request say the levels are set on a
   record not yet released, and neither says how to anticipate it.
2. A file ranking the candidates on the question: none; the bulletins rank on the near-real-time record, the declared
   basis the prompt compares against.
3. A file existing only to help the analyst: none (the dictionary's pointer to the flag recode is mild).
4. A figure or name reading as the answer: none.
5. Filed sentences fixing the figure: methods sections 3 to 6 fix the estimand (HotSpots of 1.0 or more above the MMM,
   84 days over 7, the season maximum, the levels at 4 and 8, the declared level as the highest a season bulletin
   gave); the estimator of the 2027 reprocessed record is left open, the design's open method.
6. What decides: an analytical choice, building the expected reprocessed value from the near-real-time record with the
   overlap years. Its attempt filed the bulletins' four (PB06, PB07, PB09, PB10): stumped.

Verdicts on the REVIEW lines: sweep 4 (field nouns, no document names the move), sweep 6 (the bulletins are the
declared basis, not a ranking on the reference record) and sweep 8 (the provider's documented flag column): harmless,
each answered in the design note's Leak check. Realism notes (the 64 and 64 logger model split, a note repeated on a
trip's rows) fixed in the generator; the asks' readings it raised (the colony repeats, the boats' GPS clocks) are the
asks' devices.
