# leak check, task482

**Verdict: REVIEW.** 15 files read, 51 golden figures and 11 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: position, architecture, calibrated, carried, unique, section, report, difficulty, positions, readers, reader, condition, decisive, field-test, reflex, method, attempts, effect, difficulties, anchor, population, window, census, parameter, weighted

## 3 answer figures in the pack (REVIEW 10)
- **REVIEW** `qpi_data_dictionary_2027.pdf`: golden figure 091 appears: ...ollege Algebra; 131C Corequisite College Algebra; 091 Developmental Mathematics Northgate Assess attemp...
- **REVIEW** `qpi_data_dictionary_2027.pdf`: golden figure 131 appears: ...mber of scored items answered correctly placement 131 College Algebra; 131C Corequisite College Algebra...
- **REVIEW** `qpi_data_dictionary_2027.pdf`: candidate 'College Algebra' sits beside decision vocabulary: ...re no option was chosen raw_score number of scored items answered correctly placement 131 College Algebra; 131C Corequisite College Algebra; 091 Developmental Mathematics Northgate Assess attempt...
- **REVIEW** `qpi_data_dictionary_2027.pdf`: candidate 'Corequisite College Algebra' sits beside decision vocabulary: ...n raw_score number of scored items answered correctly placement 131 College Algebra; 131C Corequisite College Algebra; 091 Developmental Mathematics Northgate Assess attempts (northgate_attempts_2026-07-01_t...
- **REVIEW** `qpi_technical_report_2027.pdf`: golden figure 091 appears: ...pport course) and Developmental Mathematics (MATH 091). Each form has two placement scores, and System...
- **REVIEW** `qpi_technical_report_2027.pdf`: golden figure 031 appears: ...ite College Algebra (MATH 131 taken with the MATH 031 support course) and Developmental Mathematics (MA...
- **REVIEW** `qpi_technical_report_2027.pdf`: golden figure 131 appears: ...f three mathematics levels: College Algebra (MATH 131), Corequisite College Algebra (MATH 131 taken wit...
- **REVIEW** `bpccs_mathematics_placement_policy_4-12.pdf`: carries 6 of 9 distinctive words of the committed call: 'Form 27A should place students into College Algebra from a raw score of 30 and into Corequisite College Algebra from 19.'
- **REVIEW** `qpi_data_dictionary_2027.pdf`: carries 7 of 9 distinctive words of the committed call: 'Form 27A should place students into College Algebra from a raw score of 30 and into Corequisite College Algebra from 19.'
- **REVIEW** `qpi_technical_report_2027.pdf`: carries 9 of 9 distinctive words of the committed call: 'Form 27A should place students into College Algebra from a raw score of 30 and into Corequisite College Algebra from 19.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `qpi_data_dictionary_2027.pdf`: 9 of 25 stump-paragraph terms appear (position, calibrated, unique, section, report, difficulty); read whether the document names the move
- **REVIEW** `qpi_technical_report_2027.pdf`: 10 of 25 stump-paragraph terms appear (position, calibrated, carried, unique, report, difficulty); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 3)
- **REVIEW** `math_course_outcomes_fall_2026.xlsx`: names 7 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `qpi_technical_report_2027.pdf`: names 4 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `bpccs_fall_2026_headcount_by_college.csv`: names 7 of 11 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `qpi_data_dictionary_2027.pdf`: names 4 of 11 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `qpi_testing_centres.csv`: names 7 of 11 answer-set candidates; confirm it does not rank them on the decision question

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

Two isolated readers (general-purpose, sonnet, medium), each holding only fresh copies of prompt.txt and target/ (pack
of 2026-10-22), answered the six questions and committed their figures (scored with score_reader.py against
generator/figures.json).

Reader A: call missed (seven: AV, BM, CV, GS, KB, MR, RG, against the golden's AC, AV, CV, DM, GS, KB, MR), from
medians per area and dwelling type weighted by the census stock's type shares; changes 0 of 16, purchases 0 of 16,
paid 0 of 16 (every line of a sale counted).
1. methodology note section 1, "measures the change in the market value of the area's dwelling stock, the dwellings the
   2022 census counts there": "It points at stock weighting but does not say how."
2. none.
3. the data dictionary and the extract manifest (field descriptions).
4. none: the 8 per cent is the threshold.
5. circular section 1 and note section 1 (the window, the years taken whole, the census stock); "The main figure's
   method (stratified, stock-weighted) is not fixed to a statistic literally."
6. an analytical choice: a stock-weighted, type-mix-adjusted index rather than raw medians.
REVIEW lines: the circular harmless; the note "a mild leak of the approach; it does not give the method or a figure".

Reader B: call missed (the same seven), from a log-price regression per area with type-specific year effects, floor
area and age, the type effects weighted by the census stock's counts (no location term); changes 1 of 16 (KB 11.2),
purchases 0 of 16, paid 0 of 16 (every line of a sale counted).
1. the same sentence of the note; "no sentence states the step outright".
2. none.
3. "none really"; the dictionary and the manifest help with field reading.
4. none.
5. note section 1 with the full-market-price rule: "a stock-weighted (census type shares) price change on
   full-market-price sales, not the change in average sale price".
6. an analytical choice: a stock-weighted, mix-adjusted index against the naive average of what sold; the VAT, the
   overlap and the area mapping are cleaning.
REVIEW lines: the circular harmless; the note "leak (mild) ... it does not give a figure or the weighting method, so
borderline harmless-context".

Verdict on the REVIEW lines: harmless. The note's sentence is the filed estimand (the change in the market value of
the census stock), which determinism-check section 1 requires filed; it names no method, and both readers executing it
with their own methods landed on the same wrong seven, missing the location shift inside RG, BM, AC and DM. No
decisive-step sentence, no helping file, no main-call fork; question 6 analytical from both readers.
