# leak check, task272

**Verdict: REVIEW.** 12 files read, 46 golden figures and 32 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: income, household, calendar, months, quarter, region, percent, application, seasonal, applications, policy, twelve-month, twelve, yearly, households, applied, period, factor, record, poverty, records, determinations, architecture, season, denial

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `contents.txt`: carries 3 of 5 distinctive words of the committed call: 'The FY2027 budget should carry 16 Decision Coaching Grants, $1,024,000, for H02, H08, H10, H11, H12, H14, H15, H17, H20,'
- **REVIEW** `fac_decision_coaching_criteria_fy2027.pdf`: carries 4 of 5 distinctive words of the committed call: 'The FY2027 budget should carry 16 Decision Coaching Grants, $1,024,000, for H02, H08, H10, H11, H12, H14, H15, H17, H20,'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `contents.txt`: 4 of 25 stump-paragraph terms appear (region, application, applications, determinations); read whether the document names the move
- **REVIEW** `fac_data_guide_2024_2025_extracts.pdf`: 15 of 25 stump-paragraph terms appear (income, household, calendar, months, region, percent); read whether the document names the move
- **REVIEW** `fac_decision_coaching_criteria_fy2027.pdf`: 13 of 25 stump-paragraph terms appear (income, household, calendar, months, percent, application); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `fac_member_hospitals_2025.xlsx`: names 31 of 32 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `state_charity_care_filings_fy2025.xlsx`: names 31 of 32 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Isolated readers (stage 4)

- Architecture 1 (target.zip 90774da6): two scored readers, each on fresh copies of `prompt.txt` and `target/`. Reader 1 (r272a) corrected each counsellor-day's contrast by shuffling the day's determinations; reader 2 (r272b) fitted counsellor-day fixed effects and subtracted the null of 150 within-day permutations per hospital, naming the short-queue bias unprompted. Both named the golden 11. Asks: r272a 0 of 62 (every write-off line summed; code 1 for the whole year), r272b 31 of 62 (Ask A whole; Ask B code 1 for the whole year). `score_reader.py --call-key call.qualify` FAIL on both (the call): Gate F failed and the architecture is spent.
- Architecture 2 (target.zip 66ca10c7): two scored readers, each on fresh copies of `prompt.txt` and `target/`. Reader C (r272c) fitted a smoothed seasonal profile for each hospital and kind of work; reader D (r272d) by kind of work, hospital group and month; each validated it on households seen twice and named the golden 16. Asks: both 0 of 31 on Ask A (every write-off line summed), 1 of 31 on Ask B (the H20 tie). Part 4: both read the four sweep items as harmless (reader C called criteria 2.3's twelve months a mild hint at most). `score_reader.py --call-key call.qualify --call-key call.count` FAIL on both (the call): Gate F failed and the architecture is spent.
