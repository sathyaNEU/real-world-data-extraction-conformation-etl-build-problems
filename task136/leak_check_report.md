# leak check, task136

**Verdict: REVIEW.** 15 files read, 13 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: campaign, campaigns, forecast, asserted, assessment, network, suburb, owner-occupied, carries, cross-reference, population, pattern, method, carried, connection, letter, nothing, letterbox, dictionary, decisive, transfer, default, window, counts, denominator

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `solar_streets_2027_letter_to_mirrabee.pdf`: golden figure 240 appears: ...Waters, where the letterbox drop will go to all 6,240 residential addresses; • Wattleview, where the l...
- **REVIEW** `yarrabin_hosting_capacity_assessment_2026.pdf`: golden figure 4.22 appears: ...2.17 12.01 12.03 YRB24 26.1 6,695 1.83 2.19 3.93 4.22 YRB25 21.0 6,212 2.20 1.74 7.25 6.75 YRB26 26.5 5...
- **REVIEW** `NPP-114_micro_EG_forecasting_rev3.pdf`: carries 6 of 7 distinctive words of the committed call: 'YRB24 should get the accelerated hosting capacity augmentation in the FY2027-28 capital works program.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `NPP-114_micro_EG_forecasting_rev3.pdf`: 6 of 25 stump-paragraph terms appear (forecast, assessment, network, carried, connection, window); read whether the document names the move
- **REVIEW** `solar_streets_2027_letter_to_mirrabee.pdf`: 7 of 25 stump-paragraph terms appear (campaign, campaigns, network, suburb, connection, letter); read whether the document names the move
- **REVIEW** `yarrabin_hosting_capacity_assessment_2026.pdf`: 4 of 25 stump-paragraph terms appear (forecast, assessment, network, method); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `der_register_extract_yarrabin_20260905.csv`: columns a generator names and an organisation does not: device_type

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Q1 to Q4: none (NPP-114 3.2 and 4.1 name the procedure, not the move; the hosting capacity report's low YRB24 and YRB25 figures are filed inputs; data dictionary and manifest ordinary; no answer-like figure). Q5: NPP-114 2.4, 4.1, 4.2, 5.1 and 6.1. MAIN-CALL READING TO CHECK: the reader took 4.1's "the number of systems that the distributor's records of past programs of the same kind indicate it will bring" as installed systems over homes letterboxed (the summary's footnote defines homes letterboxed), pooled 1.45 per cent, giving 90 and 50 systems (the default path's figures); it did not compute the feeder ranking. The golden rate is per owner-occupied house still without PV (4.58 per cent). Low-risk hint: 3.2's netting of program systems, with program_ref in the applications file. Ask readings: NMI against feeder for the register match (reallocations); what a site is (NMI, connection, multiple devices, decommissioned rows). Realism: the hosting capacity report's 2029 drop of a steady 0.2 to 0.6 MW on every feeder and its tidy columns read a little synthetic. REVIEW lines: all harmless.

Disposition (stage 4 fix): read on the stage 3 pack. The main-call reading is priced and ruled out by the records in the design note's SF16 (asserted); the realism tell is fixed (the assessment's 2026 case now follows each feeder's minimum demand at the report's stated sensitivity, the 2029 case unchanged). Documents changed since this read: data_dictionary.xlsx (the register's status values) and yarrabin_hosting_capacity_assessment_2026.pdf (the 2026 columns).

## Solver's-eye read (targeted, after the FIX_NOW pass)

On the two changed documents (data_dictionary.xlsx, the hosting capacity PDF). Q1: none names the step (NPP-114 3.2, 4.1, 4.2 and the dictionary's field notes say what to count). Q2: none ranks feeders by excess. Q3: the dictionary is the only guide-like file, ordinary for an extract. Q4: none (YRB24's low hosting capacity is an input; a mild pull to a lowest-headroom shortcut, which lands elsewhere). Q5: NPP-114 6.1 with 2.2, 2.4, 3.2, 5.1, 7.1; not computed. Realism: the PDF's demand and capacity moves read inconsistent in sign on some feeders, round route lengths, one page; the dictionary's Withdrawn definition reads complete. Readings: excess signed or floored (the golden's runner-up is positive either way), three whole trend years from 31 August 2026 to 31 August 2029, the program-system base (ruled out by the data, SF16), the DER Register match.

Disposition (ship): nothing quoted for questions 1 to 4. Its realism notes on the assessment (the demand and capacity moves, the round route lengths, the single page) are not acted on, each a change to the document beyond a date for no graded figure (the design note's `## Tried and rejected`); the dictionary, which the re-judge found dated 2 September for the 5 September DER Register extract it lists, is dated 7 September (a date only, in its properties and the manifest). The readings it lists close: excess signed or floored gives the same call and runner-up (YRB22 at 1.5 MW, positive either way); the trend runs three whole years (SF8); the program-system base is priced and refused by the records (SF16); the DER Register match converges under each listed reading (Ask A, asserted). leak.py re-run on the final rebuild: the same seven REVIEW lines, no LEAK, each answered in the design note's Build record.
