# leak check, task134

**Verdict: REVIEW.** 13 files read, 42 golden figures and 9 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, natural, building, notice, infill, beside, architecture, method, certificates, forecasting, dredged, quantity, depths, decisive, nothing, feasibility, permits, target, in-situ, surveys, sentence, rezoning, permit, housing, asserted

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `deepening_2027_maintenance_planning_basis.docx`: carries 4 of 5 distinctive words of the committed call: 'Year 1 of the 2027-30 maintenance contract should be tendered at 1,750,000 m3 in situ.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `deepening_2027_maintenance_planning_basis.docx`: 4 of 25 stump-paragraph terms appear (notice, certificates, quantity, depths); read whether the document names the move
- **REVIEW** `marine_licence_L2021-00317-2.pdf`: 3 of 25 stump-paragraph terms appear (notice, dredged, quantity); read whether the document names the move
- **REVIEW** `notice_to_mariners_03-2026.pdf`: 3 of 25 stump-paragraph terms appear (notice, depths, surveys); read whether the document names the move

## 6 ranking artifacts (REVIEW 3)
- **REVIEW** `maintenance_dredging_certificates_2016-2026.xlsx`: names 6 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `notice_to_mariners_03-2026.pdf`: names 6 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `sediment_sampling_2025-2026.xlsx`: names 6 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (Leak reader, round 1 (2026-11-02, isolated, Sonnet at medium effort, on target.zip 456d4b72))

1. Decisive step: none stated; the closest is the planning basis's estimand ("the in situ volume of material, as the contractor's monthly certificates measure it, that will settle in the maintained areas between 1 October 2027 and 30 September 2028 ... through a year of average conditions as the licence years 2016-17 to 2025-26 averaged them"); no file says deepening changes siltation or how to scale it.
2. Nothing ranks or scores anything (the certificates list historical volumes; the basis gives no per-part numbers).
3. Ordinary reference or correction material only (the certificates' area-code sheet, the dry-solids revision file, the sampling station plan).
4. Nothing reads as the answer (14.3 m and the berth depths are in the prompt and the notice; no year-1 volume anywhere).
5. The planning basis's estimand (the certified in situ volume settling in each maintained area in the contract year at the deepened geometry, berths at present depths, North Quay Berth 2 excluded, an average year over the ten licence years, summed); it does not say how deepening changes the rate.
6. An analytical choice: how settlement at 14.3 m differs from settlement at 12.3 m, needing the surveys, the tide gauge and the flows; area scope is stated openly; the method is left open.
Sweep flags: all harmless (the basis defines the estimand and gives no volume; the licence holds the disposal and returns rules for the asks; the notice gives scope, not method).
Realism: none clearly generated; minor: the certificates' identical yearly layout fits a contractor template; the basis is a clean brief; later file dates fit the forward-looking setting.

## Solver's-eye read (Leak reader, round 2 (2026-11-02, isolated, Sonnet at medium effort, on target.zip 890c87d8))

1. Decisive step: none; the planning basis's Year 1 quantity paragraph names the quantity and the baseline window (the in situ volume, as the certificates measure it, settling in the maintained areas from 1 October 2027 to 30 September 2028 through a year of average conditions as the licence years 2016-17 to 2025-26 averaged them), not how deepening to 14.3 m changes it.
2. Nothing ranks or scores (the certificates hold monthly volumes per area).
3. Nothing exists only to help the analyst (the dry-solids revision file and the area-code sheet read as ordinary organisational artefacts).
4. Nothing reads as the answer (14.3 m appears in the prompt and as Berth 5's maintained depth in the notice).
5. Licence 5.3 to 5.5 fix the supplementary placement and metals procedures (quarter by the date of placement in UK civil time; wet tonnes from dry solids over the latest completed campaign's fraction for the loading area; samples by actual position with field duplicates averaged into their primaries); the planning basis fixes the main volume's population, window and unit, not the deepening effect.
6. An analytical choice: estimating how deepening to 14.3 m changes settlement, from the surveys, tide and flows; the mess (the 2021 code change, the survey datum change, the dry-solids revision, moved sampling positions) is separate.
Sweep flags: the planning basis is harmless (no volume or method; its average-conditions clause fixes the baseline); the reworded licence clauses fix supplementary procedures only and give no figures; the notice is a geometry and depth table; the 2026 area summary reads as a sampler's own summary with campaign dates and fractions, consistent with the lab results.
Realism: none generated.
