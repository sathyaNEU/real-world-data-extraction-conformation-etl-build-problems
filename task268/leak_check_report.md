# leak check, task268

**Verdict: REVIEW.** 14 files read, 14 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: survey, logbooks, decisive, halmorie, records, brettach, organisation, stratified, sampling, stations, quantity, sample, re-root, record, method, effort, stratum, industry, probability, rejected, readable, density, locations, counts, nothing

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `stock_recovery_plan_2026.pdf`: golden figure 100 appears: ...l of the six grounds with its depth band (A under 100 m, B 100 m to under 140 m, C 140 m and deeper, fr...
- **REVIEW** `stock_recovery_plan_2026.pdf`: carries 4 of 6 distinctive words of the committed call: "We should close Halmorie Deep to members' towed gear for 2027."

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `autumn_survey_manual_rev3.pdf`: 5 of 25 stump-paragraph terms appear (survey, records, organisation, stations, record); read whether the document names the move
- **REVIEW** `gear_trial_note_2025.pdf`: 5 of 25 stump-paragraph terms appear (survey, records, organisation, stations, record); read whether the document names the move
- **REVIEW** `pack_contents.txt`: 3 of 25 stump-paragraph terms appear (survey, organisation, record); read whether the document names the move
- **REVIEW** `quota_rules_2026.pdf`: 3 of 25 stump-paragraph terms appear (records, organisation, record); read whether the document names the move
- **REVIEW** `stock_recovery_plan_2026.pdf`: 5 of 25 stump-paragraph terms appear (halmorie, brettach, organisation, record, nothing); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `ground_grid_annex_a.csv`: names 6 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `stock_recovery_plan_2026.pdf`: names 6 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

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
