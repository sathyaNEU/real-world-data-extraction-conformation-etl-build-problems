# leak check, task275

**Verdict: REVIEW.** 17 files read, 22 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: observer, observed, unobserved, ground, declared, vessel, scheme, declarations, unwanted, measured, returned, landing, family, decisive, raised, deployment, raising, report, grounds, measurement, effect, readable, terminal, records, changes

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `sales_notes_2025.csv`: golden figure 3,561.4 appears: ...,2025-10-20,Brindlesea,KE 335,CELTIC MIST,HAD,GUT,3,561.4,1.52,853.33,2025-10-21 14:38 BFM/25/05734,RB0437,...
- **REVIEW** `sales_notes_2025.csv`: golden figure 2,332.9 appears: ...-03-15,2025-03-15,Gullsby,GL 93,SINCERITY,NEP,WHL,2,332.9,6.56,2183.82,2025-03-16 17:59 1203-001790,RB1203,...
- **REVIEW** `selectivity_programme_terms_2027.pdf`: golden figure 4.1 appears: ...of the PO's species list. 4. Costs and funding 4.1 Gear and cameras are paid for from the PO's sele...

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `README_files.txt`: 11 of 25 stump-paragraph terms appear (observer, ground, vessel, scheme, declarations, landing); read whether the document names the move
- **REVIEW** `observer_scheme_manual_2025.pdf`: 12 of 25 stump-paragraph terms appear (observer, observed, unobserved, vessel, scheme, returned); read whether the document names the move
- **REVIEW** `selectivity_programme_terms_2027.pdf`: 4 of 25 stump-paragraph terms appear (vessel, returned, landing, report); read whether the document names the move
- **REVIEW** `wcfpo_data_dictionary_2025.pdf`: 12 of 25 stump-paragraph terms appear (observer, observed, ground, declared, vessel, scheme); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Put every segment in segment_discards_2025.xlsx with its 2025 discard share in whole per cent and whether it is designated, the first-sale value of its 2025 landings in thousands of pounds to one decimal place, and its v'

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### Round 1 (target.zip b24d9e4b, readers r275a and r275b, isolated, medium effort)

- Scores (`score_reader.py`, call key `call.designated`): r275a call 0 of 1, ask figures 14 of 32 (the eight days at sea and six designation and share cells the default path shares); r275b call 0 of 1, ask figures 20 of 32 (the eight days at sea and six first-sale values). Both filed NEP alone: r275a the observed trips' DIS share (R1), r275b the DIS ratio to landings raised by every trip's landed weight (R2b); neither set the observed trips' declared BMS against the unobserved trips'.
- Q1 decisive step: both quoted terms 2.1, 3.1 and 3.3 and the manual's one-in-twelve draw, the estimand and the sampling design, not the move. Q2 ranking file: none (both noted the logbook's discards field as a floor). Q3 analyst-only file: the README and the dictionary (orientation). Q4 answer-looking figure: none. Q5 literal sentence: terms 3.3 (every 2025 trip), literal result NEP alone under their raising, which is the easy route, not a fork: the golden's estimand is the same sentence. Q6 what decides: both "an analytical choice", estimating discards for the unobserved trips from the observer sample.
- REVIEW lines: the two sales-note figure hits are a grade field beside a weight field (harmless, both readers); the README, the manual, the terms and the dictionary name the scheme and its fractions, not the move (harmless, both readers).
- Realism: r275b none; r275a none clearly, with a soft tell that the observer weights matched the declarations within 0.3 per cent and every observed haul was sampled. Fixed in the generator: observers miss a haul they cannot attend (52 trips) and estimate each trip's retained catch and BMS with a trip-level spread.
- Asks: both readers placed every VMS report on the vessel its terminal was fitted to that day (days at sea 8 of 8 each); r275b dropped the merchant's lines that repeated a market lot exactly. The copy device was re-sited (the merchant's own weighing and commission-inclusive price, the quay's private sales as twins); the terminal device stays as Ask B's construction (design note, Tried and rejected).

### Round 2 (target.zip d6cd71d9, readers r275c and r275d, isolated, medium effort)

- Scores (`score_reader.py`, call key `call.designated`): r275c call 0 of 1, ask figures 6 of 32 (the six designation and share cells the default path shares; first-sale value 0 of 8 with the merchant's lines kept, days at sea 0 of 8 on the vessel the extract names); r275d call 0 of 1, ask figures 14 of 32 (the eight days at sea and the six shared cells; first-sale value 0 of 8). Both filed NEP alone at 11.7 per cent: r275c the observed trips' DIS ratio to landed weight applied to every trip's landings, r275d the observed trips' DIS over their catch.
- Q1 decisive step: both quoted terms 2.1, 3.1 and 3.3 and the dictionary's line on the logbook's 50 kg discard threshold, and both said the raising itself is not stated. Q2 ranking file: none. Q3 analyst-only file: the dictionary and the README (orientation); the gear declarations and the quota report read as distractors. Q4 answer-looking figure: none. Q5 literal sentence: terms 3.3 (every trip begun in 2025), literal result NEP alone under their raising, the easy route on the golden's own sentence. Q6 what decides: both "an analytical choice", extending the observer sample to the unobserved trips; neither named a planted item, a field reading or a filed procedure.
- REVIEW lines: the sales notes' 2,338.2 (grade 2 beside weight 338.2) and the terms' 4.3 (a clause number) harmless for both; the four documents' scheme vocabulary names the scheme and not the move (both); the prompt's third sentence lists the outputs and names no method (both).
- Realism: r275c none; r275d none at file level, with a soft remark that the observed discard rates are flat by ground and month within a segment.
- Asks: Ask A held for both readers. Ask B leaked to r275d (exit 1 at 43.8 per cent), which read the terminal moves off the dated installation table. Re-sited: the PO's terminal record now holds each vessel's terminal and the one before it, without dates (design note, Tried and rejected).

### Round 3 (target.zip 04c5972e, readers r275e and r275f, isolated, medium effort)

- Scores (`score_reader.py`, call key `call.designated`): r275e call 0 of 1, ask figures 6 of 32 (the six designation and share cells the default path shares; first-sale value 0 of 8 with the merchant's lines kept, days at sea 0 of 8 on the vessel the extract names); r275f the same, 6 of 32. Both exit 0. Both filed NEP alone at 11.7 per cent, the observed trips' DIS ratio to landed weight applied to every trip's landings.
- Q1 decisive step: both quoted terms 2.1, 3.1 and 3.3 and the manual's random draw, and both said nothing states the move. Q2 ranking file: none. Q3 analyst-only file: the README and the dictionary. Q4 answer-looking figure: none (the logbook's declared discards read as the tempting wrong source). Q5 literal sentence: terms 3.3, literal result NEP alone under their raising. Q6 what decides: both "an analytical choice"; neither named a planted item, a field reading or a filed procedure.
- REVIEW lines: the sales notes' 2,338.2 (grade 2 beside weight 338.2) and the terms' 4.3 (a clause number) harmless for both; the four documents and the prompt name the scheme, not the move (both).
- Realism: no file-level tell from either. r275e called one statistical tell, the observer DIS ratio nearly constant within a segment across grounds, time bands and meshes; r275d had remarked the same in round 2. Fixed in the generator after the round: lawful discards now follow each segment's grounds (at least 1.35 times apart) and a seasonal swing, with each segment's year total unchanged, asserted in `checks.py`.
- Asks: both re-sited devices held for both readers. Neither reader saw the terminal moves: r275e counted the swaps as harmless for a distinct-day count, and r275f relied on the vessel the extract names.
