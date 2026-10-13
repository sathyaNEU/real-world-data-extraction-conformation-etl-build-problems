# leak check, task229

**Verdict: REVIEW.** 14 files read, 31 golden figures and 27 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: outlook, talbot, decisive, inside, corriston, ratings, canyon, regulated, operating, windows, release, spread, network, register, golden, steady, default, extrapolation, monthly, schedule, freshet, generation, inflow, peaking, minimum

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `hydrometric_data_standard_ed2.pdf`: golden figure 3.2 appears: ...the record of one station for one calendar month. 3.2 A station-month meets grade B when the mean of th...
- **REVIEW** `rating_book_issue2_2026.pdf`: golden figure 1.4 appears: ...ation h = 0.4 m h = 0.6 m h = 0.8 m h = 1.0 m h = 1.4 m h = 1.8 m h = 2.4 m C101 0.3493 1.958 4.55 7.99...
- **REVIEW** `rating_book_issue2_2026.pdf`: candidate 'Lake Ashlin' sits beside decision vocabulary: ...Rating In force from C e (m) b Gauged range (m3/s) Top gauged on C101 Ashlin River above Lake Ashlin C101-R6 1 Apr 2026 14.2 0.284 1.72 1.32 to 24.9 21 Jun 2024 C102 Lake Ashlin at the outle...
- **REVIEW** `rating_book_issue2_2026.pdf`: candidate 'Ashlin River' sits beside decision vocabulary: ...ed to. Station Name Rating In force from C e (m) b Gauged range (m3/s) Top gauged on C101 Ashlin River above Lake Ashlin C101-R6 1 Apr 2026 14.2 0.284 1.72 1.32 to 24.9 21 Jun 2024 C102 Lake A...
- **REVIEW** `rating_book_issue2_2026.pdf`: candidate 'Mattin Creek' sits beside decision vocabulary: ...C122. Station Name Rating In force from C e (m) b Gauged range (m3/s) Top gauged on C110 Mattin Creek at the gravel pit C110-R4 1 Apr 2026 6.62 0.233 1.78 0.484 to 10.9 1 Jun 2024 Rating tabl...

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `corriston_hydro_operating_plan_2027.pdf`: 13 of 25 stump-paragraph terms appear (talbot, inside, corriston, canyon, operating, windows); read whether the document names the move
- **REVIEW** `data_plan_2027.docx`: 8 of 25 stump-paragraph terms appear (outlook, talbot, corriston, ratings, canyon, operating); read whether the document names the move
- **REVIEW** `flood_frequency_update_2025.pdf`: 3 of 25 stump-paragraph terms appear (corriston, canyon, network); read whether the document names the move
- **REVIEW** `hydrometric_data_standard_ed2.pdf`: 6 of 25 stump-paragraph terms appear (corriston, ratings, network, register, steady, extrapolation); read whether the document names the move
- **REVIEW** `rating_book_issue2_2026.pdf`: 5 of 25 stump-paragraph terms appear (talbot, corriston, ratings, canyon, network); read whether the document names the move

## 6 ranking artifacts (REVIEW 5, INFO 2)
- **REVIEW** `flood_frequency_update_2025.pdf`: names 17 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rating_book_issue2_2026.pdf`: names 27 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `station_register.xlsx`: names 27 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `telemetry_migration_2026.xlsx`: names 27 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `water_supply_outlook_2027.xlsx`: names 27 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `corriston_hydro_operating_plan_2027.pdf`: names 5 of 27 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `data_plan_2027.docx`: names 3 of 27 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (read 1, 2026-10-13, the 22-station cut)

# Reader answers (task229 bundle)

Method: read prompt and 14 files. I did not solve the main call exactly; the figures in Q5 are a rough literal execution (my own 1-minute hydrograph model for peaking days, rating curve applied to the instantaneous level versus the level averaged over the day).

1. Decisive step sentence. No single sentence names it. The pieces that together carry it:
   - hydrometric_data_standard_ed2.pdf 3.2: "A station-month meets grade B when the mean of the station's published daily discharges for the month is within 5 per cent of the month's true mean discharge, the mean over the month's days of the discharge that passed the station."
   - data_dictionary.csv: discharge_m3s is "the day's discharge, from water_level_m through the station's rating in force on the date", and water_level_m is "the day's mean water level".
   - corriston_hydro_operating_plan_2027.pdf section 3: "On a peaking day a plant generates in two windows, 06:00 to 10:00 and 16:00 to 21:00 local time ... Between the windows it holds its minimum release."
   - water_supply_outlook_2027.xlsx Method sheet: "Each plant releases a day's inflow within the day ... so the monthly flow past those stations is the natural flow."
   - rating_book_issue2_2026.pdf: Q = C (h - e)^b (convex, b>1).
   Nothing says "average the level, then apply the rating, so the published value is biased low under peaking". The solver has to see it. Closest announcement: standard 3.2 plus the phrase "true mean ... the discharge that passed the station".

2. Ranking or scoring file: none. The outlook gives monthly mean flows, not grades. flood_frequency_update_2025.pdf is a ranking of nothing relevant (return periods). Section 2 of data_plan_2027.docx says the review expects station-months graded C "on the flows that the 2027 water supply outlook ... and Corriston Hydro's 2027 operating plan put past each station", which names the inputs, not the result.

3. Exists only to help the analyst: none clearly. Weakest candidates: water_quality_grab_samples_2026.csv (no relation to anything asked, plausibly a real archive) and flood_frequency_update_2025.pdf (plausible distractor). The Method sheet sentence in the outlook ("so the monthly flow past those stations is the natural flow") reads like a pre-emptive line written to set up the trap, but it is a plausible forecast-method note.

4. Reads as the answer: none. No file names a station or month as short of grade B. The top-gauged column in the rating book and the 1.5x rule are context, not a result.

5. Filed sentences fixing the figure or population, with literal execution:
   - Standard 3.2/3.3/3.4 (quoted above) plus "A station-month graded C is published with the qualifier below grade B." Literal: grade is by error of the published monthly mean against the true mean.
   - Standard 4: "A station-month whose mean discharge exceeds one and a half times the largest discharge gauged at the station is graded C whatever its error ... The largest discharge gauged at a station is the top of the gauged range printed under its rating in the rating book." Executing against the outlook monthly means: only C107 trips (top 4.21, limit 6.315; May 8.65, Jun 9.44). So C107 from May. No other station of the 22 trips it (the 22 are C101-C109, C111-C123; C110 closed, so 22 active; the "27 candidates" in the sweep counts station-month-style items, not my concern).
   - data_plan_2027.docx section 2: "From the first month of 2027 in which the review expects a station-month to be graded C, the network publishes that station's daily discharge with the qualifier below grade B". Literal: the flag starts at the first C month.
   - Operating plan sections 2 to 4 give modes by month: Talbot Canyon peaking Jan to Apr and Jul to Dec, continuous May and Jun; Merrin Falls continuous June, peaking Jul to Dec; Fenn Creek run-of-river.
   My rough execution: published value = rating(daily mean level) understates the true mean discharge on peaking days by about 15 to 32 percent at C104, C105 (Jan to Apr, Jul to Dec) and C112, C113 (Jul to Dec), far beyond 5 percent. So: C104 and C105 from January (the plant is peaking in Jan, flagged from month 1); C112 and C113 from July (June continuous, so no error); C107 from May (extrapolation); all other stations never, including C109 (run-of-river). Caveat: C112 sits below Merrin Falls, so I treated it as fully affected; C113 as well. My model is crude (no routing, local inflow = outlook minus forebay inflow).

6. What decides the main answer: an analytical choice (the nonlinear rating applied to a daily-mean level versus a mean of rated instantaneous discharge, the Jensen-type bias under peaking, which the standard's "true mean" definition makes the target), with a rule-application layer on top (the 1.5x extrapolation rule for C107 and the mode table for when each plant peaks). Deciding sentences: standard 3.2 ("true mean discharge, the mean over the month's days of the discharge that passed the station") with the dictionary's "the day's mean water level". The mode table and the 1.5x rule are executed rules; a solver who just reads the rules gets C107 plus naive "regulated stations" and would still need the 5 percent test, which needs the sub-daily computation. Risk: a solver who flags every station below a plant from the plan's mode table, without computing, reaches the same list, so the quantification step may be skippable.

## Mechanical REVIEW lines

- standard 3.2 "golden figure 3.2": harmless, it is the clause number "3.2", not a figure.
- rating book "1.4": harmless, a rating-table value (C101 at some level), part of the ordinary extract; it also happens to equal h = 1.4 m column text.
- rating book Ashlin River / Lake Ashlin beside decision vocabulary (ratings table): harmless, station names in a rating table.
- rating book Mattin Creek (closed-sites line): harmless, record of a closure.
- operating plan 13 of 25 terms: harmless; the plan states modes, windows and ramps, which a real operating plan would, and it never states the rating bias or any grade. It does set out the sub-daily operating shape, which is needed input, not the move.
- data_plan_2027.docx 8 of 25: harmless, it names the review inputs only.
- flood_frequency_update_2025.pdf 3 of 25: harmless, generic nouns.
- standard 6 of 25: harmless, the grading and extrapolation clauses are the rules, not the move.
- rating book 5 of 25: harmless.
- flood_frequency_update names 17 of 27 candidates beside numbers: harmless, return-period flows, no grading.
- rating_book names 27 of 27: harmless, ratings and gauged ranges; the "top gauged" column is the input to rule 4 and is a quantity, not a verdict.
- station_register.xlsx 27 of 27: harmless, attributes only.
- telemetry_migration_2026.xlsx 27 of 27: harmless, cut-over dates.
- water_supply_outlook_2027.xlsx 27 of 27: harmless, forecast flows; it gives no grade.

## Realism tells (up to five)

1. water_supply_outlook Method sheet: "Each plant releases a day's inflow within the day (Corriston Hydro's operating plan), so the monthly flow past those stations is the natural flow." Reads as a sentence placed to justify the outlook, slightly over-explanatory for a hydrologist's method note.
2. Operating plan section 3: "Output moves between the minimum release and the generating rate over 30 minutes at the start and at the end of each window, inside the window." Unusually exact mathematical specification for an issued operating plan.
3. Rating book "Top gauged on" column and the 2019 / refit narrative are tidy; ratings for every station refitted on the same date (1 Apr 2026) with Q = C(h-e)^b for all 22 stations looks uniform.
4. station_register: every cut-over exactly one day before the next, goes_slot_utc stepping in exact 5-minute increments (02:04, 02:09, 02:14 ...), and one cut-over per station on distinct days; looks synthetic.
5. data_plan_2027.docx: a short plan whose sections map one-to-one to the prompt's asks ("how many station-days it holds a measured water level for, month by month, and how each station's gaugings stood against the ratings"). Reads as written to the task.

**Main thread's rulings on read 1.** Q1 to Q4: none to fix. Q5 and Q6: the reader's literal run reaches the golden; the analytical step is the within-day construction through the rating. The risk it names (a blanket flag on every station below a peaking plant reaches the list) is answered by Merrin Creek near the mouth (C124), added below the ungauged Vardy River, which holds grade B. Realism tells fixed: the outlook's method sentence trimmed, the ramp sentence tied to the licence's ramping condition, GOES slots reassigned out of station order, the data plan's section 3 rewritten. All REVIEW lines harmless.

## Solver's-eye read (read 2, 2026-10-13, the 23-station cut)

# Reader answers, task229

1. Decisive step. No single sentence states it. The material that decides it:
- hydrometric_data_standard_ed2.pdf 3.2: "A station-month meets grade B when the mean of the station's published daily discharges for the month is within 5 per cent of the month's true mean discharge, the mean over the month's days of the discharge that passed the station."
- data_dictionary.csv, discharge_m3s: "the day's discharge, from water_level_m through the station's rating in force on the date" (water_level_m is "the day's mean water level").
- operating plan section 3: "Each day's inflow is released within the day ... Between the windows it holds its minimum release."
Together they say the published figure is a rating applied to a mean level while the true figure is the mean of the passed discharge. Nothing in the files says that these two differ under peaking. The solver has to work that out. The task_plan sentence closest to a signpost is data_plan_2027.docx section 2: "on the flows that the 2027 water supply outlook ... and Corriston Hydro's 2027 operating plan put past each station."

2. Ranking or scoring file. None. water_supply_outlook_2027.xlsx gives monthly mean flows, and the rating book gives gauged ranges. Neither grades a station-month.

3. Existing only for the task. The nearest is data_plan_2027.docx. Its section 2 ("From the first month of 2027 in which the review expects a station-month to be graded C, the network publishes that station's daily discharge with the qualifier below grade B") is the prompt restated. Section 4 also points at the operating plan. flood_frequency_update_2025.pdf and water_quality_grab_samples_2026.csv are plausible real records but have no use in the call, so they read as distractors. The Method sheet of the outlook workbook (stations below plants carry the plant inflow plus the drainage between) is a helper line.

4. Answer-like figure or name. None. The closest are Merrin Falls "1 June 2027" in the operating plan, and the "Top gauged" and "Gauged range" values in the rating book, which set the 1.5x extrapolation limit in standard section 4. They read as context.

5. Sentences that fix the computation or the population:
- Standard 3.2, quoted above. Executed literally: per station and month, compare the mean of the published daily Q with the true monthly mean, and flag if the error exceeds 5%.
- Standard 3.3 and 3.4: if grade B is not met, the month is graded C and published "below grade B".
- Standard 4: "A station-month whose mean discharge exceeds one and a half times the largest discharge gauged at the station is graded C whatever its error ... the top of the gauged range printed under its rating in the rating book." Executed literally against the outlook means: C107 (4.21 x 1.5 = 6.3) is flagged from May (8.65), and no other station looks flagged this way on the outlook means.
- Standard 2: the day is local standard time (UTC-8), year-round.
- Operating plan section 3: the two windows, minimum release between them, 30-minute ramps, and continuous generation when inflow exceeds what the windows can pass. Section 4: continuous from 1 May to 30 June.
- Data plan 2: "From the first month of 2027 in which the review expects a station-month to be graded C" fixes "from which month".
- Data plan 1: "No station changes platform or rating in 2027." The rating is the fixed rating-book curve Q = C(h-e)^b (standard 6.1).
Literal execution I can foresee: downstream stations of peaking plants (C104 and C105 below Talbot Canyon, C112/C113/C124 below Merrin Falls from June or later) are flagged where convex-rating bias from sub-daily flow swings exceeds 5%. Run-of-river and spring stations are not flagged except by clause 4. I did not compute the months.

6. What decides it. The kind is an analytical choice. A solver has to see that the mean of Q over the day differs from the rating applied to the mean level, which is strongest under peaking, and then model the within-day release shape and the ramps against the nonlinear rating. That modelling is the deciding step, and no filed sentence tells the solver to do it. Clause 4 (extrapolation) and the 5% test are stated rules, so they are the rule-application part and cover few stations. Nothing looks planted. The 2026 telemetry cut-overs (UTC day versus local day) and the field_unit L/s versus m3/s are data-semantics chores that relate to the two asks, not to the main call.

## REVIEW lines

- "3.2" clause number and "1.4" water level: harmless. 3.2 is a section number, and 1.4 is a column header (h = 1.4 m) in the rating table. Neither is a graded figure.
- Station names (Ashlin River, Lake Ashlin, Mattin Creek) beside the rating book's tables: harmless. They are the station-name column of a rating register.
- Hydrometric vocabulary (talbot, release, windows, canyon, outlook, ratings, steady, extrapolation, network) in the plan, data plan, flood update, standard, rating book: mostly harmless, as ordinary domain words and plant names. One note: "extrapolation" is the standard's own clause 4 heading and "windows" is the operating plan's peaking windows. These are the real content of those documents, not announcements of the trap, since neither document says the mean-level-through-rating bias exists.
- Station names beside numbers in the flood update, rating book, register, migration tracker and outlook: harmless. They are identifier columns. The outlook's monthly means are inputs, not grades.

## Realism tells

1. flood_frequency_update_2025.pdf: every station has "9" years of record, even those established in 1979 to 1998 in the register, and the rows all share one format. It looks filled in uniformly.
2. telemetry_migration_2026.xlsx: every row has installed = day before, first_day_new = next day, goes_removed = day after, with no slips or exceptions. Stations C101 to C124 are also cut over in a neat sequence.
3. export_manifest.csv: all 14 files carry the identical export date 2026-11-06, including a PDF dated 2025 and one issued 19 October 2026.
4. data_plan_2027.docx: "Daily values are transmitted and processed in 2027 as the data dictionary describes" and "No station changes platform or rating in 2027" read as added to close loopholes.
5. rating_book_issue2_2026.pdf: header says ratings are "refitted to each station's 2016 to 2026 gaugings" yet every "In force from" is 1 Apr 2026 and every rating name carries a clean R-number. The Gauged range "Top gauged on" values cluster in June and July for most stations.

**Main thread's rulings on read 2.** Q1, Q2, Q4: none. Q3: the data plan is the organisation's plan for the inspector and carries the review's basis and the flag policy, which a real plan files; its 2027 processing sentence is the pin SF3 rests on and stays. Q5 and Q6: analytical, as designed. Realism tells fixed as data-only changes, checked by leak.py: the manifest dates each file by its own date, the migration tracker's installation dates follow the crews' schedule, and the flood frequency update gives each station's record length from its establishment; the rating book's common in-force date is the database move and stays. All REVIEW lines harmless.
