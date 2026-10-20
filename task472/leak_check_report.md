# leak check, task472

**Verdict: REVIEW.** 19 files read, 20 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: window, millrace, saltworks, counterfactual, decisive, nothing, sailing, silent, record, readiness, objective, decision, quantity, halyard, architecture, domain, operating, sailings, closed, binding, directions, windows, driver, differentiated, candidate

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `salt_point_tide_predictions_2025_2026.txt`: golden figure 257 appears: ...t 04:37 AM -3.2 -99 L 2025/06/14 Sat 10:54 AM 8.4 257 H 2025/06/14 Sat 05:05 PM -2.8 -85 L 2025/06/14 S...
- **REVIEW** `crane_replacement_program_rules.pdf`: carries 4 of 5 distinctive words of the committed call: 'Ternmouth should place the six 2027 replacement cranes at Millrace.'
- **REVIEW** `data_dictionary.txt`: carries 3 of 5 distinctive words of the committed call: 'Ternmouth should place the six 2027 replacement cranes at Millrace.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `crane_replacement_program_rules.pdf`: 5 of 25 stump-paragraph terms appear (millrace, saltworks, record, halyard, closed); read whether the document names the move
- **REVIEW** `data_dictionary.txt`: 10 of 25 stump-paragraph terms appear (window, millrace, saltworks, sailing, record, halyard); read whether the document names the move
- **REVIEW** `harbor_masters_general_directions_2025.pdf`: 5 of 25 stump-paragraph terms appear (millrace, saltworks, sailing, sailings, directions); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 1)
- **REVIEW** `crane_maker_service_timesheets_fy2026.xlsx`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `crane_replacement_program_rules.pdf`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `data_dictionary.txt`: names 4 of 4 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `berth_windows_fy2027.csv`: 7 ISO dates after 2026-10-06, e.g. 2027-01-05

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Two scored readers on target.zip sha256 f939e7b04094cb6a, 2026-10-20. **Both landed the call: architecture 1 is spent.**

- Reader 1, question 1: rule 2.4 of crane_replacement_program_rules.pdf, "A call's berth hours lost to crane breakdowns are the hours by which breakdowns of the cranes working it, taken together, lengthened its stay alongside." Read as the critical-path counterfactual: Pine Neck 263, Halyard 184, gap 79. Question 7: the critical-path totals and the bridged moored totals all land on whole hours. Ask A exact on all six terminals; ask B off (union per crane, DMG orders kept).
- Reader 2, question 1: none, "the closest is rule 2.4"; question 6: "the deciding text is rule 2.4's 'lengthened its stay'". Pine Neck 263, Halyard 184, gap 79. Ask B exact on all six terminals; ask A off (raw stretches). Question 7: near-integer terminal totals; the 2 November repeated hour the dictionary names does not appear in the crane extract.
- score_reader.py exit 1 on both (call landed).
