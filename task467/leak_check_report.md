# leak check, task467

**Verdict: REVIEW.** 23 files read, 236 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: comparison, series, station, asserted, decisive, change, annual, reflex, arrangement, aggregate, silent, control, different, office, restatement, directions, stations, attribution, program, permanent, population, pattern, carries, design, effect

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `vaa_ground_transportation_fees_bylaw_gt3.pdf`: golden figure 5.75 appears: ...2021 $4.75 2022 $5.00 2023 $5.25 2024 $5.50 2025 $5.75 2026 $6.75 2027 To be set by the Board under sect...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `vaa_finance_policy_fp07_user_fee_revenue.pdf`: 5 of 25 stump-paragraph terms appear (change, annual, arrangement, office, program); read whether the document names the move
- **REVIEW** `velmont_transit_airport_line_service_bulletin.pdf`: 3 of 25 stump-paragraph terms appear (station, change, stations); read whether the document names the move
- **REVIEW** `vfh_trip_records_data_dictionary.pdf`: 3 of 25 stump-paragraph terms appear (change, annual, office); read whether the document names the move

## 6 ranking artifacts (INFO 1)
- **INFO** `vfh_brokerages.csv`: names 6 of 7 answer-set candidates; confirm it does not rank them on the decision question

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

### Round 1 (the pack before the stage-4 fix pass)

1. None states the method. Closest: FP-07 4.3 "the base year's pickups are restated to those the base year would have had under the budget year's arrangement" (states the goal only). GT-3 s.4(1) fixes the fee rule. The Airport Line bulletin (opened 4 Nov 2024, same day as the rank) and the notice give the context only.

2. None. The budget xlsx gives 535,027 but no fee or volume. No file computes a fee, a restated base, or the rank's effect.

3. None clearly. Nearest is vaa_ground_access_survey_2023.pdf (taxi shares), which feeds no step. The transit bulletin reads as a real bulletin.

4. Nothing reads as the answer. Line 12 "Amount assigned to the taxi pickup fee 535027" is context.

5. GT-3 s.2: "fee-liable pickup means a trip a licensed taxi begins at the airport; a trip the taximeter records as voided is not a trip". Literal result: 2025 = 74,724 (zone 1 pickups; the annual file has no voids).
GT-3 s.4(1): lowest multiple of $0.25 with budgeted pickups x fee >= 535,027.
FP-07 4.2: base year = 2025, restated, no growth. 4.4: read from the final annual file.
GT-3 s.3(2): bill to the brokerage affiliated "when the trip begins". 
My calculation, using drop-offs as the control (pickup/drop-off ratio 1.223 before the rank vs 1.18 after): restated about 77,500 to 77,600, share about 4%, fee $7.00 (no restatement would give $7.25).

6. An analytical choice. Nothing filed says how to restate. The Airport Line opened the same day, so total demand fell about 21%, and passengers or pre-period levels overstate the rank's effect (about 24%, fee $5.50). Drop-offs are a control that the rank did not touch. The ledger side (voids, duplicates, affiliation) is rule application and data handling.

7. Mostly plausible. Specifics:
- 33 vehicles move brokerage on exactly 2025-01-01 and 28 on 2026-01-01, with 24 on 2024-01-01; the batches are round.
- The pickup/drop-off ratio is about 1.22 every month before the rank and about 1.18 after, with very little noise.
- 86 exact duplicate store-and-forward records, all in 2026.
- All PDF stamps fall on whole minutes, with no Creator or Producer.
- The passenger-statistics xlsx was created 2023-02-06 but holds data to 2026-08.
- Contact email is velmont.example.

8. Terms that can be read two ways:
(a) Duplicate records. 86 identical records (sf_flag Y) exist in the 2026 monthly files. s.2 "a trip" implies one, but s.3(2) says "as the Vehicle-for-Hire Office's records show them" and nothing says to drop duplicates. OPEN.
(b) Month assignment. 2026 files are in UTC, and 4 to 5 hours of each month's end fall in the next UTC month. s.2 "Days, months and years are reckoned in Velmont local time" settles it. Late arrivals sit in later files, so month comes from meter_on, not the file.
(c) Voids. Settled by s.2 and the dictionary (void and reversal pairs, 2024 and 2026 files).
(d) Brokerage. The 2025 file's brokerage_id differs from the affiliations table on 9,299 rows (12%). s.3(2) "affiliated when the trip begins" settles it. 
(e) Fee per year. s.3(1) fee for the year in which the trip begins. 5.75 for 2025, 6.75 for 2026.

9. Terms:
- Fee-liable pickup: settled by s.2, except the duplicates (OPEN as in 8a).
- 2025 as recorded: FP-07 4.4 (annual file) gives 74,724. If the 2026 monthly files are meant to be consulted, they hold no 2025 trips.
- Restated: FP-07 4.3 states the target but not the counterfactual. The estimator is open: drop-off control gives 77.5k to 77.6k and passenger-based gives about 98.9k. The cap on how it gets chosen is the data, not a filed sentence.
- Share, surplus and shortfall: derive from the restated figure. At $7.00 the surplus is about $8k, rounded to $10,000. At $6.75 the shortfall is about $12k, rounded to $10,000.
- Budget amount: line 12, 535,027. Settled by the xlsx note "(FP-07 2.1)".

Rulings: Q1 to Q4 nothing quoted. Q5 the literal sentences file the estimand and leave the estimate open (the reader's own estimate sat on the $7.00 rung). Q6 analytical. Fixed in the generator: by-law s.3(2) now bills each month's pickups counting each trip once (the reader's records-against-trips reading and the judge's FIX_NOW), taxis no longer on overlapping trips, the affiliation register gives each spell's reason (the 1 January batches are annual renewals), PDF stamps carry seconds, the dictionary's contact line has no .example address, and pickups and drop-offs lean by season so the monthly ratio is no longer flat. Harmless: the exact copies are memory-sent trips re-sent whole; the passenger workbook created in 2023 and saved in 2026.

### Round 2 (the shipped pack)

1. No file names the decisive step (restating 2025 for the rank). Nearest: vaa_finance_policy_fp07 4.3: "the base year's pickups are restated to those the base year would have had under the budget year's arrangement." It says to restate, not how. Bylaw 4(1) fixes the fee rule ("lowest multiple of $0.25..."). Otherwise none.

2. None. No file computes a 2027 fee, a restated 2025 base or the rank's effect. The budget xlsx gives only $535,027 as "Amount assigned to the taxi pickup fee"; the passenger xlsx holds only passenger and movement counts.

3. None clearly. vfh_od_daily_archive_2023.csv and the budget xlsx read as organisational records. The 2023 survey PDF and the Velmont Transit bulletin are context or distractors, and the survey mentions "forecourt reconstruction" in passing.

4. Nothing reads as the answer. The nearest is the $535,027 budget line, which is an input. Schedule A's 2026 fee, $6.75 against $5.75 in 2025, is context.

5. (a) Bylaw s2: "fee-liable pickup means a trip a licensed taxi begins at the airport; a trip the taximeter records as voided is not a trip". Literal result: pu_zone=1 trips, voids and their reversals excluded. (b) Bylaw 3(2): "counting each trip once". I get 74,753 for 2025. (c) Bylaw 4(1): lowest $0.25 multiple with pickups x fee >= amount. (d) FP-07 4.2: base year is the latest complete fiscal year, no growth. (e) FP-07 4.4: use the "final annual file". The restated figure is not fixed literally. My rough estimate is about 77,000 (pickups-to-drop-offs ratio ~1.21 before the rank, ~1.17 during), which gives a fee near $7.00.

6. An analytical choice. FP-07 4.3 says to restate to the budget-year arrangement but gives no method. The estimand is clear and the estimation is open. The Airport Line opened the same day (4 Nov 2024) as the temporary rank, so the rank effect has to be separated from the line. Drop-offs are an unaffected comparison series. Cleaning (voids, duplicates, UTC) is Layer 1.

7. Realism points. (a) The 2026 monthly files carry a UTC meter_off but a local meter_on once I convert it. (b) The 2026 files hold 59 exact duplicate trips, all sf_flag Y, with a new record_id. (c) 892 voided trips each have a matching negative reversal; the 2025 annual file has none. (d) Store-and-forward records have seconds forced to :00. (e) 2026 column "Airport_Fee" is capitalised differently from the other files. (f) The budget xlsx was created on 2026-09-08, but its as_of in folder_contents is 2026-10-14. (g) The passenger xlsx creator is "Airport Operations". (h) The 2026 fee of $6.75 is a large jump. I found no impossible taxi trips.

8. Terms that can be read two ways. (a) Month boundary: bylaw s2 says "Days, months and years are reckoned in Velmont local time" and the dictionary says the 2026 files are UTC, so this is settled. (b) Voids: settled by s2, and the dictionary says a reversal carries the same vehicle, times and zones. (c) Duplicates: "counting each trip once" settles it. (d) Brokerage: 3(2) says "with which the taxi is affiliated when the trip begins", with effective_from and effective_to dates in the affiliations file. (e) Late records for a closed year: the dictionary says they go into the annual file. (f) Fee in force: "The fee billed is the fee in force, whatever a meter charged." Not settled: what counts as a duplicate (same vehicle, times and zones, different record_id) is not stated.

9. Fee-liable pickup: settled by s2 (zone 1, voids excluded, local time). 2025 recorded: settled by FP-07 4.4 "final annual file". I get 74,753 on the annual file, which has no voids. 2025 restated: OPEN. FP-07 4.3 gives the target but no method or comparator, and the line confound is not addressed. Share the rank cost: this depends on the restated figure and is open in the same way; ratios put it at roughly 3 to 4%. Budget amount: settled as $535,027 (line 12 = line 8 less lines 9 to 11). Surplus at the fee: bylaw 4(1) gives the fee grid, so the surplus follows from the restated figure. Shortfall at 25 cents less: the same, "25 cents less" being clear. Overall, only the restatement method is open.

Rulings: Q1 to Q4 nothing quoted. Q5 every quoted sentence executes to the golden's population and figures (74,753; local months; each trip once; brokerage when the trip begins; the fee in force); the restatement's method is open by design and the reader's estimate again sat on the $7.00 rung. Q6 analytical. Q7: meter_on and meter_off both carry UTC in the 2026 files (the remark came from converting one column); the 59 exact copies, the void pairs, the minute-stamped memory records, the Airport_Fee case, the workbook stamps and the 2026 fee step are the organisations' own records, each harmless. Q8: what makes two records one trip is the data's (same licence, minute, zones and amounts; no licence otherwise starts a trip within 25 minutes of ending one), the population is filed (counting each trip once).
