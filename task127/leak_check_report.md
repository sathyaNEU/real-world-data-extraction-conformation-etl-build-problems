# leak check, task127

**Verdict: REVIEW.** 16 files read, 41 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: equipment, nights, patient, cleeve, wendlebury, marchford, covered, decisive, delivery, holmford, default, determinism, generator, counterfactual, analytical, dependency, sentence, warehouse, record, asserted, closed, service, allocation, removed, reader

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `winter_discharge_fund_2026-27.pdf`: carries 17 of 19 distinctive words of the committed call: 'Give Royal Marchford Hospital 508 packages, Wendlebury Hospital 350, Holmford Infirmary 120, Cleeve Park Hospital 222 an'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `acute_extract_notes.txt`: 3 of 25 stump-paragraph terms appear (nights, patient, warehouse); read whether the document names the move
- **REVIEW** `council_extract_notes.txt`: 4 of 25 stump-paragraph terms appear (patient, record, closed, service); read whether the document names the move
- **REVIEW** `ices_export_notes.txt`: 6 of 25 stump-paragraph terms appear (equipment, patient, marchford, delivery, record, service); read whether the document names the move
- **REVIEW** `winter_discharge_fund_2026-27.pdf`: 8 of 25 stump-paragraph terms appear (nights, patient, cleeve, wendlebury, marchford, covered); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 2)
- **REVIEW** `bed_census_daily_2024-12_2026-09.xlsx`: names 8 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `brokerage_referrals_2024-12_2026-09.csv`: names 9 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `ward_reference.csv`: names 8 of 10 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `winter_discharge_fund_2026-27.pdf`: names 7 of 10 answer-set candidates; confirm it does not rank them on the decision question

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

Two reader passes, each one Sonnet reader at medium effort on a fresh copy holding only `prompt.txt` and the bundle.

**Pass 1** (the bundle as first cut).
- The REVIEW lines, all harmless. The allocation note carries the call's words because it is the fund's own note naming the five hospitals and the packages; it carries no split, value or bed-day figure. The notes files and the note use the stump terms as field definitions and as the filed estimand, and none of them names the move. The census and the brokerage referrals sit beside candidate names as a daily bed count for every age and a referral log, and neither ranks the hospitals on packages or bed-days.
- Questions 1 to 4: none. The reader executed the valuation sentence as the nights from the discharge ready date to discharge, which is the default path's rung and not a filed reading; the records contradict the inference that nothing else held the patient.
- Realism, fixed in the generator: the census sat at its open beds on 99.5 per cent of nights; the reablement shares were unrounded floats and the quarters were labelled "2025 Q4". Kept: finance's BRK reference against the brokerage's BR numbers (the finance system's own key, an ask hazard), the outward-code districts and the one-page note.

**Pass 2** (the bundle the pass-2 judge read).
- The same REVIEW lines and the same calls: harmless. Questions 1 to 4: none. On the decisive step the reader wrote: "Nothing says the value falls as packages are added; that is left to the analyst."
- Forks it raised, both closed. (a) "the warehouse keeps every submission" does not say which submission counts. The same sentence says a trust "corrects a spell" by submitting it again, so the latest submission is the corrected spell, and both readers kept the latest. No covered spell was resubmitted (SF9, asserted), so the call is the same under every reading, and on the delayed bed-days chart the resubmissions are the ask's device. (b) Which statuses count as "the referrals for home care the brokerage took". Only a started referral carries a start date, and every spot purchase is a closed referral, both asserted, so no reading of the statuses moves a cell.
- Realism tells. Fixed in the generator:
  - The census escalation beds averaged the same at every site. Each site now has its own winter ceiling, asserted to differ by site.
  - Patients aged 65 and over held at most 80 per cent of every ward's beds. The share now follows the ward's specialty and moves week to week, asserted with no ward over its beds at midnight and no common ceiling.
  - The postcode lookup held exactly 70 postcodes a ward. It now lists every unit postcode in each ward (30 to 120), including postcodes that no record in the pack carries. No referral or patient postcode changes district.
  - The PDF and workbook stamps sat on round minutes. They now sit off the minute, asserted.

  Kept as they are:
  - The two date styles in the ward stays, which follow the trust (one style a trust, asserted).
  - The spaced NHS numbers in the two council systems.
  - The weekly return as published.
  - The ward codes out of sequence.
- After the fixes, `figures.json` is identical, 27,095 assertions pass, the verifier is green and the rebuild is byte-identical. Only six files changed: the ward stays, the census, the postcode lookup, the reablement workbook's stamp, the note's stamp and the golden workbook's stamp. No document text and no graded figure moved, so the pack needs no further read and no further judge pass.

**Pass 3** (loop 1 of 2026-10-16, on the cut with the equipment notes' route definition, before the realism re-cut of the waits; one Sonnet reader at medium effort on a fresh copy of `prompt.txt` and the bundle).
- Questions 1 to 4: none. No sentence or file names the move, nothing ranks the hospitals on packages or bed-days, no file exists only to help, no figure reads as the answer.
- Question 5: the note's sections 3 and 4 fix the population, the window, the cap and the greedy fill; the reader judged that the value cannot be the raw nights after the ready date, and that "the nights by which a package would have shortened their stay" has to be built.
- Question 6: an analytical choice. The reader names the counterfactual saving per hospital, built across the warehouse and the equipment service's deliveries, as what decides, and writes that no sentence states it and no field answers it. The equipment notes' new route definition read as a plain description of the route ("depot and route descriptions that name no analytical step").
- The seven REVIEW lines: all harmless (the note names the hospitals and the packages but no figure; the notes define fields; the census and the brokerage export rank nothing on the decision).
- Realism. Fixed in the generator: the covered patients' nights after the ready date ran only 3 to 14, a flat block with a hard floor; every wait is now drawn right-skewed (the covered nights now run 1 to 36 with a long tail). Answered, no fix: hospital referrals with a start "months before the referral" do not exist in the file (no referral starts before it was received, checked); the reader's join by NHS number alone had matched other referrals of the same person. Kept: the bird and tree ward names and a ward code out of sequence, finance's BRK references, the request log's exact row counts (the log is the System Flow team's own).
- The re-cut changed data only. After the re-cut judge, one line went into the acute notes ("A patient counts as delayed in a month when at least one of these nights is dated in that month"), closing the judge's optional fork on the chart's patient counts, so the pack was read once more (pass 4).

**Pass 4** (loop 1, on the cut with the acute notes' sentence on when a patient counts as delayed in a month; one Sonnet reader at medium effort on a fresh copy; the REVIEW line quoting the call was given without its figures).
- Questions 1 to 4: none (the acute notes and the ward reference are ordinary field notes and a lookup, not helper files).
- Question 5: the note's sections 3 and 4 give a greedy fill on a value whose construction the text does not give; the reader names that gap as the analytic step.
- Question 6: an analytical choice: the shortened-stay value is a counterfactual estimate, not a field read off a column; the semantics in the pack (resubmissions, closed practices, restarts) are cleaning, not the decider; nothing planted.
- The six REVIEW lines: all harmless.
- Realism. Fixed in the generator: no week in the data (care starts, deliveries and discharges flat across the week, deliveries even peaking on Saturday); the services now keep a working week, each turned-down weekend day redrawn from the service's own waits. Answered, no fix: "all statuses Started" is not the file (Started 11,768, Closed 1,871, Cancelled 373, Open 13 at that cut, checked); the bed census and the weekly return are complete because they are the system coordination centre's and the trusts' own complete returns (both distractors).
- The final cut changed data only (no document text, no prompt), so no further read; `leak.py` gives the same REVIEW lines.
