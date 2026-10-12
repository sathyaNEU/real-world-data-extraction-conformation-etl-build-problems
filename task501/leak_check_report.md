# leak check, task501

**Verdict: REVIEW.** 19 files read, 20 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: eigenvalue, immunity, method, matrix, susceptible, survey, immune, contact, million, population, structure, standard, national, contacts, health, weighted, average, architecture, sentence, threshold, cohort, client, golden, scenario, nearest

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `mmr_catch_up_options_autumn_2027.pdf`: carries 8 of 11 distinctive words of the committed call: "We should fund option B, the MMR catch-up for those born 2008 to 2012: it is the only option that brings measles' reprod"
- **REVIEW** `ps07_measles_winter_planning_standard.pdf`: carries 9 of 11 distinctive words of the committed call: "We should fund option B, the MMR catch-up for those born 2008 to 2012: it is the only option that brings measles' reprod"

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `immunisation_guidelines_ch12_mmr_excerpt.pdf`: 3 of 25 stump-paragraph terms appear (immune, national, health); read whether the document names the move
- **REVIEW** `mmr_catch_up_options_autumn_2027.pdf`: 7 of 25 stump-paragraph terms appear (immunity, susceptible, immune, national, health, cohort); read whether the document names the move
- **REVIEW** `national_mmr_uptake_report_2027q1.pdf`: 3 of 25 stump-paragraph terms appear (national, health, cohort); read whether the document names the move
- **REVIEW** `ps07_measles_winter_planning_standard.pdf`: 7 of 25 stump-paragraph terms appear (immunity, immune, population, standard, national, health); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `mmr_stock_return_2027-06-30.csv`: 26 ISO dates after 2027-07-12, e.g. 2027-10-27, 2027-11-10, 2027-11-17, 2027-11-28, 2027-12-22

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read (architecture 4)

Q1 to Q4: none (standard ps07 3.6 gives the decision rule, not the step; the options paper's columns are inputs, though its expected-made-immune column leans toward B without ranking on the reproduction number; extract notes and field lists are plausible; the uptake report and stock return read as distractors). Q5: ps07 3.1 to 3.5 fix the inputs, not the method; the reader's own next-generation-matrix reconstruction gives no catch-up 1.2, A 1.2, B 0.9, C to E 1.2, so B (the golden). Readings raised: matrix orientation, age bands and population weighting; spreading made-immune over birth years; paper People against projection counts; "living in the region" (active flag, current address, de-duplicated); dose validity, merged registrations; confirmed and imported cases, rash onset against notification date. Realism: the options paper dated 9 June cites July extracts it does not use; ps07 v3.0 superseding v2.1; option E repeats D's rows; the NSCS national population column's trailing digits read generated. REVIEW lines: all harmless.

Ruled by the build session at the stage-4 fix (generator, one pass): the options paper now lists option E on one row with its split in the note under the table and says in 4.3 that invitation lists will be drawn from the register for the option funded (the paper cited no extract; 4.3 was the only register sentence); Table 1 of the survey now carries the statistics office's populations by group, Table 2 unchanged; ps07 v3.0 superseding v2.1 kept (a dated revision note). Both documents changed, so the reader re-reads them. REVIEW lines: harmless, answered in the design note's Build record.
