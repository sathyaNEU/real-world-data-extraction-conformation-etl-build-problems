# leak check, task124

**Verdict: REVIEW.** 17 files read, 62 golden figures and 12 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: unknown, verified, galvanized, services, decisive, copper, district, streets, verification, shares, record, sample, schedule, replaced, inventory, carried, expected, records, golden, shipped, street, era-wide, driver, architecture, default

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `HFRWD_LSLR_plan_rev2_2026-10.pdf`: carries 9 of 13 distinctive words of the committed call: 'At $25.4 million a year from 2027 every zone in the plan is finished inside the deadline: the last, RZ-06 Wexley, is fin'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `HFRWD_LSLR_plan_rev2_2026-10.pdf`: 14 of 25 stump-paragraph terms appear (unknown, verified, galvanized, copper, district, streets); read whether the document names the move
- **REVIEW** `LSLR_progress_report_2026.pdf`: 8 of 25 stump-paragraph terms appear (unknown, verified, district, verification, record, schedule); read whether the document names the move
- **REVIEW** `lsl_extract_field_notes_2027-01.md`: 12 of 25 stump-paragraph terms appear (unknown, verified, galvanized, copper, district, verification); read whether the document names the move

## 6 ranking artifacts (REVIEW 4, INFO 2)
- **REVIEW** `HFRWD_LSLR_plan_rev2_2026-10.pdf`: names 9 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `LSLR_progress_report_2026.pdf`: names 3 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `change_orders_2026.xlsx`: names 3 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `unit_cost_schedule_2027.xlsx`: names 8 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `contracts_2026.csv`: names 3 of 12 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `lsl_extract_field_notes_2027-01.md`: names 3 of 12 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (round 3)

On the round-3 cut (target.zip sha256 8ef783ab336726f5), one isolated reader on the prompt and `target/` only. Q1 to Q4: none (no sentence names the decisive step, no file ranks the zones on the deadline or states a cost, a finish year, a share or a schedule, no file exists only to help the analyst, no figure or name reads as the answer). Q6: an analytical choice; the reader read the decisive step as the selection of the verified sample (the verified lines are not the lines still unknown) and found nothing filed that corrects for it. Sweep line "the plan carries 9 of 13 words of the call": harmless, generic vocabulary (zone, programme year, finished, deadline and the zone name in the priority table); the call sentence is not in the plan and the plan states no finish year, cost or share. The other REVIEW lines are answered in the design note's leak review (the stump-paragraph terms are the inventory's own nouns; the zone lists are the priority order, unit prices and contractor counts). Ask readings the reader raised are each governed by a shipped file, as the determinism judge ruled on the same cut: quarters in Eastern time (progress report section 2), a reclosing replaces the first closing (field notes), Tri-County's two vendor numbers are one contract (progress report section 5 and the contracts file), E-SIGNED counts as signed (field notes and the outreach tracker). No leak; no fork on the main figure.
