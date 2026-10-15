# leak check, task257

**Verdict: REVIEW.** 12 files read, 37 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: latent, questions, growth, pearson, dimension, correlation, dropped, asserted, measurement, retention, manager, estimator, decisive, distinct, splits, analyst, random, nothing, golden, analysis, employee, structure, tetrachoric, polychoric, measure

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `survey_reporting_standard_2025.pdf`: 6 of 25 stump-paragraph terms appear (questions, dimension, manager, distinct, employee, measure); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "I need engagement_subscales_2027.xlsx with each item's sub-scale and, for each of the 12 store districts, how many employees answered at least one item before the survey closed and how many of them answered all 30; engag"

## 6 ranking artifacts (INFO 1)
- **INFO** `site_directory_2026-10.csv`: names 5 of 7 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: rounding at the close: no rounding words anywhere; every derived figure needs one, stated once at the end

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## Solver's-eye read

One isolated reader (Sonnet, medium) read fresh copies of `prompt.txt` and `target/` only, before the loop-0 fixes.

1. Decisive step stated: none. The nearest text is the standard's 2.1 and 2.2 ("A sub-scale reports one distinct dimension of employees' views that the survey's items measure", "Each item reports under exactly one sub-scale, the dimension it measures most"), which define the concept with no count, no item lists and no method.
2. A file ranking or grouping the candidates: none. The codebook lists the 30 items in a mixed order with no theme or dimension column; the benchmark is per item with no grouping; the pulse survey holds other items.
3. A file that exists only to help the analyst: none; the benchmark and the pulse results are context a vendor or HR team holds, the paper returns log, kiosk log, HR history and site directory are ordinary operational records.
4. A figure or name reading as the answer: none.
5. Filed sentences fixing the computation: the respondent definition (standard 3.1), the opening-day site (3.4) and Kestrava's "last submission under each token" fix the coverage counts; for the sub-scale count the literal reading is one per distinct dimension the items measure, estimated from the answers, with no method or number fixed by the text.
6. What decides the main answer: an analytical choice (how many dimensions the answers support and where each item loads); not a field reading, a stated rule or a planted item. The coverage counts are rule application, a separate ask.

Review lines: the standard's vocabulary, harmless (generic survey language, no count, grouping or method); the prompt sentence, harmless (the deliverable list; the scree chart is a requested output, not a conclusion); rounding, harmless (every asked figure is a whole count); the site directory, harmless (a site master that ranks nothing).

Realism tells, all fixed in the generator in one pass before ship: the benchmark's 25th and 75th percentile shares ran below 0 and above 100 (now spread on the logit scale, within 1.2 and 98.5); a library item named Brackenmere's own leadership programme (Kestrava's library wording now generic for four items); the French codes were the English ones swapped in adjacent pairs (the French version now has its own item order). Two further notes need no fix: the export's 19 October run date is inside the fiction (the pack's as-of is 20 October 2026), and the pulse results and site directory both cover all 152 sites because the pulse runs at every site.
