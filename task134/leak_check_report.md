# leak check, task134

**Verdict: REVIEW.** 14 files read, 18 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, conversion, months, admission, golden, asserted, person, hazard, points, release, decisive, returns, counts, puerto, window, payment, default, deaths, extract, district, method, history, definitions, assessment, return

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `care_home_budget_definitions_2027-28.docx`: carries 8 of 12 distinctive words of the committed call: 'Budget for 760, 770, 780 and 790 council-funded long-stay care home residents on 30 June, 30 September and 31 December 2'
- **REVIEW** `extract_notes_2027-01-18.txt`: carries 9 of 12 distinctive words of the committed call: 'Budget for 760, 770, 780 and 790 council-funded long-stay care home residents on 30 June, 30 September and 31 December 2'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `care_home_budget_definitions_2027-28.docx`: 5 of 25 stump-paragraph terms appear (person, counts, payment, extract, definitions); read whether the document names the move
- **REVIEW** `charging_policy_2026-27.pdf`: 3 of 25 stump-paragraph terms appear (person, payment, assessment); read whether the document names the move
- **REVIEW** `extract_notes_2027-01-18.txt`: 7 of 25 stump-paragraph terms appear (admission, person, payment, deaths, extract, definitions); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `charging_assessments_2021-2026.csv`: 36 ISO dates after 2027-01-18, e.g. 2027-01-19, 2027-01-20, 2027-01-21, 2027-01-22, 2027-01-24

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Reader (Sonnet, medium) on the stage 3 cut, prompt.txt and target/ only.

1. Decisive step: none stated. Closest: definitions 2.4 (counted once, whenever admitted, hospital and out-of-area included) and 1.2 (a decision recorded after a date but effective on or before it counts on that date); the extract notes' "The cut" paragraph (dates after 31 December 2026 blank). No sentence says how to forecast the four dates.
2. Ranking or stated figures: none. The national rate tables and the draft 2027-28 offer carry rates only.
3. Helping files: none outright; the NRS death linkage reads slightly purpose-built; care-at-home hours, inspectorate grades and the draft offer read as distractors.
4. Answer-like figure: none.
5. Literal population: definitions 2.4 with 2.1 to 2.3; executed on PERM episodes in place on 31 December 2026 before merges and deaths, 747. No filed sentence fixes the forecast method.

REVIEW lines: all harmless (the definitions and the notes mirror the call's vocabulary, no figure or method); the 36 post-as-of dates are `effective_from` on assessments completed before the run date (definitions 1.2). Mild: the notes' "The cut" and NRS paragraphs say recent admissions and deaths are incomplete.

Ask-level readings the reader raised: placement locality against the home's postcode locality; fee less contribution against the national rate; free personal and nursing care in the net cost; NIL contributions in the average; care-type changes inside a stay; ordering on rounded or unrounded values.

Realism tells: odd-step placement ids; hand-stated row counts in the notes; patterned service numbers; only 110 NIL rows; a tidy version table in the docx.

Since this read (stage 4 fix pass, 2026-10-12, no graded figure moved, freeze.py determinism PASS): placement and assessment numbers reissued as one shared sequence each (gaps of one or more, issued in the order episodes were keyed and assessments opened); the one NIL row carrying a contribution (0.83, a review effective 18 January 2027) now reads ASSESSED; the version table removed from the definitions; the row counts removed from the extract notes' file list. NIL rows left as they are (109 of 7,919, 41 people). Service numbers left as they are. The two changed documents wait on a re-read.

## Solver's-eye read (targeted, after the stage 4 fix pass)

Read on the two changed documents (care_home_budget_definitions_2027-28.docx, extract_notes_2027-01-18.txt) with the rest of the pack as context. Questions 1 to 4: none (the closest sentences are definitions 1.2 and the notes' cut paragraph, which name no step; no ranking, helping file or answer-like figure). Question 5: definitions 2.4 with 2.1, 2.3, 3.1 and 3.2 fix the population and the cost; the forecast method is not filed, which is the design (the judge ruled it forced by the data). Realism: the docx reads clean and complete; the notes' structure is even but plausible. No fix needed.
