# leak check, task270

**Verdict: REVIEW.** 10 files read, 33 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: census, population, reader, architecture, deaths, estimated, golden, estimates, single, resident, single-year, inside, reading, readers, decisive, and-over, published, bookings, record, counts, window, landed, primary, registered, reflex

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `late_life_frailty_program_guidelines_2028_2030.pdf`: candidate 'Wolfram Ranges' sits beside decision vocabulary: ...netmouth, Kestrelmoor, Mallowmere, Merriwold, Saltwick Shoals, Spraymouth, Windermoor and Wolfram Ranges. The program goes to the whole of each area it names. 3 Which areas the program goes to 3...
- **REVIEW** `late_life_frailty_program_guidelines_2028_2030.pdf`: candidate 'Saltwick Shoals' sits beside decision vocabulary: ...Cobbleton, Coldwater Plains, Dunesford, Gannetmouth, Kestrelmoor, Mallowmere, Merriwold, Saltwick Shoals, Spraymouth, Windermoor and Wolfram Ranges. The program goes to the whole of each area it...
- **REVIEW** `late_life_frailty_program_guidelines_2028_2030.pdf`: carries 18 of 19 distinctive words of the committed call: 'The 2028 to 2030 late-life frailty program should go to Windermoor, Coldwater Plains, Dunesford and Saltwick Shoals, the'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `late_life_frailty_program_guidelines_2028_2030.pdf`: 7 of 25 stump-paragraph terms appear (population, deaths, estimated, single, resident, primary); read whether the document names the move

## 6 ranking artifacts (REVIEW 5, INFO 2)
- **REVIEW** `bdm_death_registrations_tidewell_2016_2027.csv`: names 3 of 3 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `census2021_sa2_age_sex_ur.csv`: names 3 of 3 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `erp_lga_age_sex_2016_2026.xlsx`: names 3 of 3 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `interstate_deaths_tidewell_residents_2016_2027.xlsx`: names 3 of 3 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `late_life_frailty_program_guidelines_2028_2030.pdf`: names 3 of 3 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `asgs2021_sa2_to_lga2023.csv`: names 3 of 3 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `falls_injury_hospitalisations_65plus_lga_2024_25.csv`: names 3 of 3 answer-set candidates; confirm it does not rank them on the decision question

## 8 column names (REVIEW 1)
- **REVIEW** `asgs2021_sa2_to_lga2023.csv`: columns a generator names and an organisation does not: BMOS_NULL_FLAG

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

One isolated reader (general-purpose, Sonnet, medium) on fresh copies of `prompt.txt` and `target/` (target.zip 26b6eb80, 2026-10-28). The prompt and the guidelines PDF it read are byte-identical in the shipped pack; only data files changed since, in the realism fixes below.

1. Decisive step: none stated. Nearest text: guidelines 3.2 ("The rates run by single year of age from 85 to 94, with 95 and over as the last group"), read by the reader as the estimand's definition, not a move. **Ruling: pass.**
2. No file ranks or scores the areas on life expectancy at 85; the falls table is a different measure. **Ruling: pass.**
3. No analyst-aid file: no readme, dictionary or manifest; the TableBuilder header and footer and the ERP Contents sheet are the publishers' own packaging. **Ruling: pass.**
4. No figure or name reads as the answer. **Ruling: pass.**
5. Quoted from the guidelines: 3.1 (the seven-year line, the 2024 to 2026 window), 3.2 (single years 85 to 94, 95 and over), 3.3 (usual residents' deaths at each age in completed years, wherever registered, over the sum of the estimated resident population of that age at the three 30 Junes), 3.4 (named on the unrounded figure), section 4 (the 2023 area of the 2021 SA2 by the correspondence), section 5 (aged 85 and over on the day of the visit, the area of the residence attended). **Ruling: each executes to the golden; none says how the single-year population inside the published 85-and-over estimate is obtained, so no literal reading files the easy answer, and the census and state splits execute the same sentences to other sets.**
6. The reader judged the call "mostly rule application" from the files, and named the open single-year split of each area's 85-and-over estimate as an analyst's method choice that "may be" the decisive step, if it moves the call; it computed nothing. **Ruling: analytical, by measurement on the pack: the state split names Coldwater Plains and Windermoor, the census split Coldwater Plains, Spraymouth and Windermoor, the census rebuild with each birth window's deaths Coldwater Plains, Dunesford, Saltwick Shoals and Windermoor (`checks.py` LADDER rows). The reader's account is a route, the ladder is the measurement (`determinism-check` §1).**
7. Realism tells, all mild: the after-hours times shared one seconds value across request, arrival and departure; the correspondence's 44 ratios are all 1.000000 and Good; the aged care list used few street names and recurring providers; the ERP 85-and-over series had near-flat runs (three identical years); the interstate registration numbers looked random. **Ruling: fixed in the generator (independent seconds for each time, a wider street list and varied providers with distinct names and sizes, a published estimate's own error on each ERP cell, each state's registration number format), except the correspondence, harmless: every SA2 of the region nests in one area, which the ABS file records as 1.000000 and Good.**

Sweep lines: (a) the guidelines' section 2 lists the twelve areas, generic, harmless; (b) to (f) registers, census counts, estimates and the service list name areas beside counts with no rate, rank or score on the question, harmless; (g) BMOS_NULL_FLAG, empty on all 44 rows, a column the ABS correspondences carry, harmless.

### Re-read on target.zip 8e02e3d3 (2026-10-28)

Guidelines 3.2 changed in the determinism judge's fix pass (it now files how a rate becomes years lived), so one fresh isolated reader (general-purpose, Sonnet, medium) read fresh copies of `prompt.txt` and `target/` again.

1. Nothing announces the decisive step; the reader quoted 3.2 (now with the half-year and last-group sentence), 3.3 and section 4 as the estimand and its conventions. **Ruling: pass.**
2. No file ranks the areas on life expectancy at 85, on qualifying or on the visits. **Ruling: pass.**
3. The state's single-year estimates read to the reader as a possible helper for splitting the 85-and-over band, and plausible context; the falls table and the aged care list as distractors. **Ruling: harmless; the state file is a declared distractor (the R1 route, unused by the golden), and its split names Coldwater Plains and Windermoor only.**
4. Nothing reads as the answer. **Ruling: pass.**
5. 3.1, 3.2, 3.3, 3.4, sections 2, 4 and 5 quoted, each with what it makes a solver do. **Ruling: each executes to the golden; none says how the single-year population inside the published band is obtained.**
6. The reader again judged the call largely procedural and named turning the 85-and-over band into single-year populations as the remaining analytical load, with nothing planted. **Ruling: analytical by measurement (the state split, the census split and the census rebuild name three different sets), as judge pass 1's Gate H also read it.**
7. Nothing generated-looking: no duplicate registration numbers, real-looking TableBuilder and ABS packaging, no tool signature. The repeated case and clinician pairs it noted are returns by the same clinician (990 rows) and co-arrivals; no row repeats a case, clinician and arrival time. **Ruling: harmless.**

Sweep lines a to g: harmless, as in the first read (BMOS_NULL_FLAG matches the ABS correspondence headers).
