# leak check, task127

**Verdict: REVIEW.** 16 files read, 43 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: equipment, nights, patient, wendlebury, marchford, cleeve, feeder, decisive, holmford, restart, opportunity, sizing, feeders, sentence, delivery, architecture, determinism, record, states, golden, orders, control, neighbourhood, installs, generator

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `winter_discharge_fund_2026-27.pdf`: carries 17 of 19 distinctive words of the committed call: 'Give Royal Marchford Hospital 508 packages, Wendlebury Hospital 350, Holmford Infirmary 120, Cleeve Park Hospital 222 an'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `acute_extract_notes.txt`: 3 of 25 stump-paragraph terms appear (nights, patient, restart); read whether the document names the move
- **REVIEW** `ices_export_notes.txt`: 5 of 25 stump-paragraph terms appear (equipment, marchford, delivery, record, orders); read whether the document names the move
- **REVIEW** `winter_discharge_fund_2026-27.pdf`: 7 of 25 stump-paragraph terms appear (nights, patient, wendlebury, marchford, cleeve, holmford); read whether the document names the move

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
