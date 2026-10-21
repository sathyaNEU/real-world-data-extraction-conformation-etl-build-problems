# leak check, task272

**Verdict: REVIEW.** 12 files read, 63 golden figures and 32 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: counsellor, points, reordering, within-day, chance, benchmark, determination, queues, working, comparison, dependence, session, approval, length, decisive, effect, application, family, screen, excess, counsellor-day, control, initiative, approving, pooling

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `contents.txt`: carries 3 of 5 distinctive words of the committed call: 'The FY2027 budget should carry 11 Decision Coaching Grants, $704,000, for H03, H06, H09, H10, H17, H19, H20, H21, H22, H'
- **REVIEW** `fac_decision_coaching_criteria_fy2027.pdf`: carries 4 of 5 distinctive words of the committed call: 'The FY2027 budget should carry 11 Decision Coaching Grants, $704,000, for H03, H06, H09, H10, H17, H19, H20, H21, H22, H'

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `contents.txt`: 3 of 25 stump-paragraph terms appear (counsellor, determination, application); read whether the document names the move
- **REVIEW** `fac_data_guide_2025_extracts.pdf`: 6 of 25 stump-paragraph terms appear (counsellor, determination, working, approval, application, screen); read whether the document names the move
- **REVIEW** `fac_decision_coaching_criteria_fy2027.pdf`: 11 of 25 stump-paragraph terms appear (counsellor, points, chance, determination, queues, working); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "How many Decision Coaching Grants should the foundation's FY2027 budget carry, one for each Fair Assistance Collaborative hospital that meets the coaching criteria on its counsellors' 2025 determinations?"
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "The board's scorecard in the workbook also needs, for each hospital, the assistance its counsellors' 2025 approvals wrote off, net of the reversals posted by 31 March 2026, and how many of its counsellors' 2025 denials w"

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
