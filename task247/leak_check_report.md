# leak check, task247

**Verdict: REVIEW.** 16 files read, 18 golden figures and 16 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: analysis, reference, filled, anomaly, station, observed, monitoring, regression, method, near-real-time, decisive, overlap, refill, temperature, observation, clear-sky, correction, repeat, provisional, observations, nothing, twelve, sentence, toward, refilling

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `post_bleaching_survey_protocol_2023.pdf`: 3 of 25 stump-paragraph terms appear (station, monitoring, repeat); read whether the document names the move
- **REVIEW** `reef_heat_stress_watch_methods_v3.pdf`: 9 of 25 stump-paragraph terms appear (analysis, reference, station, monitoring, method, near-real-time); read whether the document names the move
- **REVIEW** `srao_nrt_sst_user_guide_v3_2.pdf`: 6 of 25 stump-paragraph terms appear (analysis, observed, near-real-time, temperature, observation, observations); read whether the document names the move
- **REVIEW** `srao_reprocessed_sst_release_note_2027-05.pdf`: 4 of 25 stump-paragraph terms appear (analysis, reference, near-real-time, temperature); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 1)
- **REVIEW** `heat_stress_bulletins_2027.xlsx`: names 16 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `watch_sites_register.csv`: names 15 of 16 answer-set candidates; confirm it does not rank them on the decision question

## 8 column names (REVIEW 1)
- **REVIEW** `srao_nrt_sst_extract_watch_pixels_2018-01-01_2027-11-02.csv`: columns a generator names and an organisation does not: obs_flag

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: no data count disclosed: each of the N: "Which of our 16" (a count the data hold is the model's to find; drop it or keep only the decision parameter)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 36% of 196 prompts (cap 30%); reword at the role level, not the verb

## 12 describing content (REVIEW 1)
- **REVIEW** `post_bleaching_survey_protocol_2023.pdf`: names 8 column(s) of the data files verbatim (Issued, condition, genus, line, metre, observer): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)


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

### Reship read, 2026-11-02 (the c4e68804 cut; the final cut a84fab8e changed two data files and no document or prompt)

One isolated reader on prompt.txt and target/ only, nothing computed.
1. Decisive step: none stated. Methods section 6 and the request file the estimand (each site's season maximum as the
   reprocessed record will give it); no file names a back-test, a bias model or a correction of the near-real-time
   record against the reprocessed one.
2. Ranking file: none. The bulletins are the declared record (methods section 5), not the reprocessed-basis answer.
3. Explanatory files: none. The methods note, the product guide, the release note and the registers read as the
   organisation's and the provider's own documents; no readme, dictionary or "how to read" sheet.
4. Answer-like figure or name: none.
5. Filed sentences: the HotSpot, DHW, threshold, season and declared-level definitions; they file the estimand, not
   the estimator.
6. What decides: an analytical choice, estimating 2027 on the reprocessed basis from the near-real-time record and
   the overlap years.
Supplementary: the logger hours largely settled; no shipped sentence says which site a deployment belongs to when a
tag and the register disagree, and the reader saw no disagreement (the device silent); the one undefined item it named,
the logger clock zone, is closed on the final cut by the log's own UTC mark on the Cozumel II's GPS times.
Realism notes: zip entry dates, tidy parameterised file names, near-arithmetic pixel ids, the boats' regular daily
staggering; read as acceptable, none exclusion-level. Verdict: clean.
