# leak check, task133

**Verdict: REVIEW.** 13 files read, 28 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: borrower, register, scenario, record, volume, division, asserted, industry, permit, stressed, length, decisive, payload, credit, credits, stress, nothing, million, average, limits, september, scaling, full-bunk, default, sentence

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `cartage_planning_basis_FY2028.docx`: candidate 'Port Kowhai' sits beside decision vocabulary: ...rris, Logistics Manager. Version 2, 6 October 2026. For Harvest Planning, Finance and the Port Kowhai log yard. Background The FY2028 export cartage contract goes to tende...
- **REVIEW** `cartage_planning_basis_FY2028.docx`: carries 9 of 9 distinctive words of the committed call: 'The FY2028 harvest plan needs 29,000 export log loads to Port Kowhai under the 50MAX route limits.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `50MAX_route_approval_RDC-2026-114.pdf`: 3 of 25 stump-paragraph terms appear (permit, limits, september); read whether the document names the move
- **REVIEW** `cartage_planning_basis_FY2028.docx`: 11 of 25 stump-paragraph terms appear (register, record, volume, permit, length, payload); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `fleet_register_2026-06-30.xlsx`: names 6 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `harvest_plan_FY2028.xlsx`: names 3 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (the isolated leak reader, two rounds)

Every REVIEW line above is ruled harmless by the reader in each round; neither round found a decisive-step sentence, a ranking file, a helper file or a figure that reads as the answer, and both answered question 6 with an analytical choice (each unit's FY2028 payload as the lesser of its weight room and its bunks at the load's density).

### Leak reader, architecture 4 round 1 (2026-11-01, isolated, Sonnet at medium effort, on target.zip e53d1a72)

1. Decisive step: none stated; the nearest is the planning basis 3.1 ("FY2028 loads for a grade are the harvest plan's export tonnes for that grade divided by the average payload that grade's FY2026 port loads would carry on the same units in FY2028"), which fixes the estimand and the payload basis, not how to derive a unit's payload.
2. Nothing ranks grades, units or carriers on loads.
3. No helper file clearly (the grade specification and the 50MAX approval are context the solution uses).
4. Nothing reads as the answer (no load count anywhere).
5. 3.1 with 3.2 (50 t gross for permit units, 44 t otherwise); 4.1 cartage by the carrier whose unit hauled the load, net of credit notes; 4.2 domestic deliveries by delivery date.
6. An analytical choice: recomputing each load's payload as the new gross limit less tare, capped by the load's own volume or fill, against scaling by 50/44 or historical mean tonnes; part rule application (3.2's limits). Its caution: 3.1 nearly spells out the counterfactual-payload construction; how the cap works is not written down.
Sweep flags: all harmless (the planning basis files the estimand, not the volume cap, tare or unit match; the approval names no computation; the register and the plan rank nothing).
Realism: mild generated feel in fleet_register_2026-06-30.xlsx (tares and full-bunk volumes in narrow uniform bands, units grouped neatly by carrier prefix, permit exactly equal to 9-axle, "Previous registration" blank but for two entries); port weighbridge net tonnes very tight (mean 25.48, sd 0.67); the planning basis's short numbered sections with a change record read slightly as task-summary prose.

### Leak reader, architecture 4 round 2 (2026-11-01, isolated, Sonnet at medium effort, on target.zip 4a9ed312)

1. Decisive step: the planning note's "FY2028 loads are the harvest plan's export tonnes for the grade divided by the average payload that grade's FY2026 port loads would carry on the same units in FY2028" names the payload-by-unit logic but no trap; nothing says payload is limited by the bunks before the weight limit; the fleet sentence ("each with the tare, 50MAX permit and full-bunk volume for each log length") points to the inputs.
2. Nothing ranks or scores anything on loads.
3. No helper file (prices, vessel calls, road closures and mill weighbridge logs read as distractors; the grade specification is legitimate lookup context).
4. Nothing reads as the answer (no load count anywhere).
5. The planning note's sizing sentence fixes the estimand (each grade's plan tonnes over the mean payload its FY2026 port loads would carry on the same units under the FY2028 limits); how payload is computed (volume against weight cap, density, weighting) is left open, "which is acceptable".
6. An analytical choice decides it: each unit's payload as the lower of its volume-limited and weight-limited loads, applied to the FY2026 mix and aggregated correctly; the easy route (50/44 times current tonnes, or a flat payload) is wrong; the re-registered units and the ticket joins are Layer 1 mess.
Sweep flags: all harmless (the note files the WHAT and names no weight-against-volume step, no tonnes per JAS m3 and no unit matching; the council letter states the limits and the permit condition; the register and the plan rank nothing).
Realism: none clearly generated; mild: the register's bunk volumes and tares near uniform bands, the harvest plan's tonnes all round hundreds (a planning step), and the note's "What we are sizing" and "How we get" headings slightly summary-like.

