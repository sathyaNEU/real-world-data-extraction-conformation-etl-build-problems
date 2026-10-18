# leak check, task268

**Verdict: REVIEW.** 16 files read, 23 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: survey, industry, county, strata, commuting, presence, carried, counts, method, estimator, workers, decisive, residence, corrisford, synthetic, premises, carries, network, weighted, on-premises, worker, grocer, distribution, national, complete

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `commuting_od_tract_2022_main.csv`: golden figure 15,100 appears: ...3 08202000102,08202022300,116,20,71,25,18,36,62,1,15,100,20250303 08202000102,08202022400,163,44,81,38,32,...
- **REVIEW** `board_paper_pilot_metro_2027.pdf`: carries 5 of 5 distinctive words of the committed call: 'We should put the 2027 weekday dark-store pilot in Tessavon.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `board_paper_pilot_metro_2027.pdf`: 9 of 25 stump-paragraph terms appear (commuting, counts, workers, corrisford, network, weighted); read whether the document names the move
- **REVIEW** `commuting_extract_notes_2022.pdf`: 6 of 25 stump-paragraph terms appear (industry, county, commuting, counts, workers, worker); read whether the document names the move
- **REVIEW** `wls_puf_codebook_2025-26.pdf`: 4 of 25 stump-paragraph terms appear (survey, county, counts, premises); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Stage 4 reader, 2026-10-18 (one isolated agent, Sonnet at medium, reading only fresh copies of `prompt.txt` and `target/`).

1. Decisive step: none named outright; the reader quotes board paper 4.2 and 4.3 as the measure and the codebook (DAYS_PREM, HOMEREL, "Use FINALWT for every estimate") as the only hint that the survey's attendance scales the commuting counts.
2. Ranking file: none.
3. Helper file: none; the commuting notes and the codebook read as ordinary documentation, the launch log, CBP and ACS B08301 as distractors.
4. Answer-like figure or name: none; the board paper names no metro as chosen and gives no figures.
5. Board paper 4.2 and 4.3: executed with residents from B01003, land from ALAND and workers from the commuting table scaled by the survey's FINALWT-weighted DAYS_PREM/5 by industry group and HOMEREL, giving Tessavon 28,805 against Corrisford 21,709.
6. "Following a stated procedure combined with an analytical choice": how to turn the commuting table's jobs into people at work on an average weekday; the reader names the choice of attendance by sector and home relation, "the codebook's HOMEREL definition suggests classifying each flow against the work metro's central, outlying or outside counties".

REVIEW lines: all five harmless (15,100 is three fields of a commuting row run together; the board paper names Tessavon among the six candidates and says the choice is not made in it; the board paper, the commuting notes and the codebook state the measure and the variables and name no move). Realism: nothing generated.

Score (`score_reader.py task268`): the call 5 of 5 (Tessavon, Corrisford, 28,800, 21,700, 7,100); the cores' figures 15 of 18 (the three people-present misses are the judge's HOMEREL 4 fork); asks A and B 0 of 24. Exit 1: the reader landed the call, Gate F failed, architecture 1 spent.
