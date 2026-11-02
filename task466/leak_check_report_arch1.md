# leak check, task466

**Verdict: REVIEW.** 16 files read, 29 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: silent, likelihood, report, censored, decisive, guidance, reports, measured, asserted, records, dropped, season, observation, method, agreement, approved, censoring, client, stopped, superintendent, demand, golden, provisional, historical, low-flow

## 3 answer figures in the pack (REVIEW 12)
- **REVIEW** `castlewick_interconnect_offer_2027.pdf`: golden figure 0.1 appears: ...terms: 1. Firm capacity is reserved in blocks of 0.1 million gallons a day, up to 0.8 million gallons...
- **REVIEW** `castlewick_interconnect_offer_2027.pdf`: candidate 'Select Board' sits beside decision vocabulary: ...rations allow. We would be glad to bring the agreement to our Council in January once the Select Board has acted. Sincerely, Darryl Powell Director of Utilities, City of Castlewick...
- **REVIEW** `quillfield_drought_management_plan_2024.pdf`: golden figure 0.91 appears: ...MGD 2025 0.87 0.86 1.41 2026 0.89 0.87 1.43 2027 0.91 0.88 1.45 2028 0.93 0.89 1.47 4. Emergency interc...
- **REVIEW** `quillfield_drought_management_plan_2024.pdf`: golden figure 0.86 appears: ..., MGD Average day, MGD Maximum day, MGD 2025 0.87 0.86 1.41 2026 0.89 0.87 1.43 2027 0.91 0.88 1.45 2028...
- **REVIEW** `quillfield_drought_management_plan_2024.pdf`: golden figure 0.93 appears: ...1.41 2026 0.89 0.87 1.43 2027 0.91 0.88 1.45 2028 0.93 0.89 1.47 4. Emergency interconnect The town will...
- **REVIEW** `quillfield_drought_management_plan_2024.pdf`: golden figure 0.87 appears: ...emand, MGD Average day, MGD Maximum day, MGD 2025 0.87 0.86 1.41 2026 0.89 0.87 1.43 2027 0.91 0.88 1.45...
- **REVIEW** `quillfield_drought_management_plan_2024.pdf`: candidate 'Select Board' sits beside decision vocabulary: ...rought Management Plan Town of Quillfield Water Department. 2024 revision, adopted by the Select Board on May 14, 2024. 1. Supply The town's water comes from the Varrow River at the old mill d...
- **REVIEW** `varrow_river_at_quillfield_daily_values.txt`: golden figure 2.54 appears: ...97.40 1966-08-06 2.84 A SHS 01-2297.40 1966-08-07 2.54 A SHS 01-2297.40 1966-08-08 2.92 A SHS 01-2297.40...
- **REVIEW** `varrow_river_at_quillfield_daily_values.txt`: golden figure 1.89 appears: ...97.40 1963-09-09 2.03 A SHS 01-2297.40 1963-09-10 1.89 A SHS 01-2297.40 1963-09-11 2.37 A SHS 01-2297.40...
- **REVIEW** `varrow_river_at_quillfield_daily_values.txt`: golden figure 1.87 appears: ...97.40 1964-08-17 1.96 A SHS 01-2297.40 1964-08-18 1.87 A SHS 01-2297.40 1964-08-19 1.85 A SHS 01-2297.40...
- **REVIEW** `varrow_river_at_quillfield_daily_values.txt`: golden figure 131 appears: ...297.40 1952-04-06 134 A SHS 01-2297.40 1952-04-07 131 A SHS 01-2297.40 1952-04-08 127 A SHS 01-2297.40...
- **REVIEW** `castlewick_interconnect_offer_2027.pdf`: carries 5 of 6 distinctive words of the committed call: 'Reserve 0.3 MGD (three blocks) of firm capacity on the Castlewick interconnect for 2027.'

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `castlewick_interconnect_offer_2027.pdf`: 3 of 25 stump-paragraph terms appear (agreement, superintendent, demand); read whether the document names the move
- **REVIEW** `quillfield_drought_management_plan_2024.pdf`: 4 of 25 stump-paragraph terms appear (guidance, agreement, superintendent, demand); read whether the document names the move
- **REVIEW** `quillfield_water_works_reports_1894_1950.pdf`: 8 of 25 stump-paragraph terms appear (report, reports, records, season, agreement, stopped); read whether the document names the move
- **REVIEW** `swrb_guidance_wr14_design_drought_flows.pdf`: 5 of 25 stump-paragraph terms appear (likelihood, guidance, records, approved, low-flow); read whether the document names the move
- **REVIEW** `varrow_river_station_description.pdf`: 3 of 25 stump-paragraph terms appear (records, approved, provisional); read whether the document names the move

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

### Round 1 (the pack before the stage-4 fix pass)

1. Decisive step: none names it. The nearest is WR-14 section 3 ("the mean and standard deviation of the logarithms are estimated by maximum likelihood from the river's record at the intake: the complete climatic years of the approved record of a streamgage at or near the intake and, for earlier years, the records of the river kept at the site") with the plan's section 4 reservation rule; the transcription states the agreement's level and that the reports give a flow only in seasons the pumps stopped. Nothing says censored or how a silent year enters a fit.
2. Ranking or computing file: none. No file ranks the blocks or computes the design low flow or the reservation; the offer, plan and permit give inputs only.
3. Helping file: none. The regional regression report closes itself off ("They are not used at gaged sites, where the gage's record governs"); the dictionary and contents list are ordinary inventories.
4. Reads as the answer: none. The plan's 2027 Stage 2 demand (0.91) and the offer's block ladder are context.
5. Literal reading of WR-14 section 3 with the climatic-year definition: the gauge's climatic years 1951 to 2024 (74, climatic year 2025 incomplete and provisional) and the report years 1894 to 1950; measured years as values (gallons a day converted, second-feet as printed); "No stoppage" years as 7-day low flows at or above about 3.09 cfs, each contributing that probability; the three missing reports left out. Ruled: the golden reading.
6. Decides the main answer: an analytical choice (how the silent years enter the fit); the method for them is left to the solver. Ruled: analytical, no rule 3 finding.

REVIEW verdicts: every line harmless (the offer's block size and wording are its terms; the plan's demand table is an input; the daily values are single days; "Select Board" is the forum; the documents' stump terms describe their own subjects, the reports stating what the records contain, not how to handle "No stoppage").

Realism tells, ruled and fixed in the generator (nothing graded moving): two declarations quoting a reading at or above the level they cite, and templated notice wording (fixed: each declaration quotes a provisional reading below its level, asserted, and the wording varies); the reports' repeated note on seasons stopped twice (varied); the export retrieved at 07:12 holding that day's mean (now retrieved the morning after); the dictionary and contents list dated after the data (the folder now assembled on 16 October); the dictionary's qualifier definition (now naming A:e). Left as they are: the notices register named for 2012 to 2026 with its first notice in 2014; transcribed flows to the nearest 10,000 gallons.

### Round 2 (after the fix pass; the reports, dictionary, register and notices changed)

1. Decisive step: none quoted. The reader named the plan's section 4 and WR-14 sections 2 and 3 as the filed method (the reservation rule, the design statistic, the distribution, the skew and maximum likelihood); nothing names the treatment of the silent years.
2. Ranking or computing file: none.
3. Helping file: none.
4. Reads as the answer: none (the permit's 1.40 MGD and 0.50 cfs, the offer's blocks and the 0.91 MGD demand are inputs).
5. Literal reading: the plan's section 4 executed on WR-14's population (the climatic years of the approved gauge record and the 1894 to 1950 reports, the "No stoppage" years at or above the 2 MGD level, about 3.09 cfs): the golden reading.
6. Decides the main answer: an analytical choice, estimating the 50-year low flow from a pre-gauge record that is censored; a solver using the gauge alone or dropping the silent years files a wrong figure; nothing looks planted. The rule-application part it noted is the ask (the Stage 2 periods from the notices), which the 10/10 rules leave free.

Realism tells, ruled: the notices' readings just under each level (inherent: a stage is declared when the 7-day mean falls below its level, and the notice quotes the reading that did it); the plant's winter finished water steady around 0.65 to 0.69 MG (a small town's base demand) and the Stage 2 demand table's even steps (a planning projection) left as they are; the operator log's single repeated note (fixed in the generator: routine notes and one-off events now vary, a data-only change, figures.json and submission.md byte-identical).
