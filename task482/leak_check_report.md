# leak check, task482

**Verdict: REVIEW.** 18 files read, 27 golden figures and 15 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: oxidizer, architecture, outlet, control, efficiency, captured, reader, reflex, readers, window, destroyed, operating, destruction, decisive, returns, dilute, population, product, census, calendar, device, measured, airflow, sentence, carrow

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `cantrell_bend_waste_profiles_2026.pdf`: \bdesign note\b|\bgenerator\b x2: ...each plant's waste analysis reported. Issued 8 January 2027. Profile Generator Waste Generating process VOC, % by weight Waste codes Form CB-0213-01...

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `deq_rule_18-4_draft_2027-02-19.pdf`: golden figure 2.0 appears: ...pture and control, or use only press materials of 2.0 pounds of VOC per gallon or less, less water and...
- **REVIEW** `cantrell_bend_waste_profiles_2026.pdf`: carries 12 of 15 distinctive words of the committed call: 'Rule 18-4 covers Ashcombe Flexible Packaging, Carrow Gravure, Kelvedon Laminates, Merrion Flexibles and Ravensbrook Grav'
- **REVIEW** `oxidizer_performance_tests_2017_2026.pdf`: carries 11 of 15 distinctive words of the committed call: 'Rule 18-4 covers Ashcombe Flexible Packaging, Carrow Gravure, Kelvedon Laminates, Merrion Flexibles and Ravensbrook Grav'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `deq_information_request_2027-01-12.pdf`: 6 of 25 stump-paragraph terms appear (oxidizer, efficiency, operating, returns, product, calendar); read whether the document names the move
- **REVIEW** `deq_rule_18-4_draft_2027-02-19.pdf`: 6 of 25 stump-paragraph terms appear (oxidizer, control, destroyed, operating, calendar, device); read whether the document names the move
- **REVIEW** `oxidizer_performance_tests_2017_2026.pdf`: 5 of 25 stump-paragraph terms appear (oxidizer, outlet, destruction, product, carrow); read whether the document names the move

## 6 ranking artifacts (REVIEW 4)
- **REVIEW** `cantrell_bend_waste_profiles_2026.pdf`: names 10 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `deq_printing_plants_register_2027-02.xlsx`: names 14 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `oxidizer_performance_tests_2017_2026.pdf`: names 9 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `press_material_use_2026.csv`: names 14 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

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

## Solver's-eye read

Architecture 7, round 1 (zip md5 5ab18e48, 2026-10-23), two isolated readers (Sonnet, medium) on fresh copies of
prompt.txt and target/.

Reader A. Q1: none (rule 18-4-3(b) defines the quantity, not how destruction is computed). Q2: none. Q3: none that
exists only to help (the test summary is the calibration a solver needs). Q4: none. Q5: rule 18-4-3(a) and (b), read
literally, leave how destroyed VOC is computed open. Q6: an analytical choice: the test tables show the outlet at a
floor of about 45 ppmv as carbon when the inlet is low (Ashcombe "Average 1040.8 45.61 ... 95.62" against "Average
1886.5 44.93 ... 97.62"), so it rebuilt each hour's outlet as max(45, 1.8 per cent of the inlet). It filed the golden
five (score_reader: call 1 of 1; 58 of 58 graded figures, every press VOC, cleaning VOC and gallon figure).

Reader B. Q1: none. Q2: none. Q3: none. Q4: none (the tests' destruction column would mislead if applied flat). Q5:
rule 18-4-3(a) and (b), which do not fix the method. Q6: an analytical choice, read from the test tables (outlet steady
while the inlet moves) and the register's fan-drive column: each fixed-fan unit's test outlet carried to every hour's
air. It filed six plants, Larkmoor in (score_reader: call 0 of 1; 53 of 58 graded figures, both asks 28 of 28).

Every REVIEW line: harmless to both readers. Verdict: architecture 7 spent (reader A landed the call); the ask devices
sat on both readers' paths.
