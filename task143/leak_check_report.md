# leak check, task143

**Verdict: REVIEW.** 23 files read, 10 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: chance, release, cycles, finished, asserted, fin-rs-, members, shared, effect, predictive, decisive, weakest, variance, structure, nothing, default, golden, forecasting, validation, window, groups, between-tray, genealogy, system, builds

## 2 author vocabulary (REVIEW 3)
- **REVIEW** `extract_note_battery_lab_2026-10-12.txt`: \bthe model\b x2: ...e: Zelvora Cell s.r.o. model_k_genealogy_zc2638.csv Genealogy of the Model K packs built from lot ZC2638, one row per cell Source: Battery P...
- **REVIEW** `fin_rs04_battery_warranty_reserve_policy.pdf`: \bthe model\b x4: ...ery reliability lab releases the lot for shipment. 1.2 It applies to the Model K pack (part 4100-2210, the battery of the K14 and K15 notebooks). Th...
- **REVIEW** `qm07_release_model_rl3_zp4820.pdf`: \bthe model\b x2: ...ce from the 10th to the 100th cycle, in milliohm: F2 = R100 − R10. 4. The model ln N80 = b0 + b1 F1 + b2 F2, N80 the cycles to 80 per cent of rated c...

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `fin_rs04_battery_warranty_reserve_policy.pdf`: golden figure 2.4 appears: ...nt of rated capacity within its first 600 cycles. 2.4 Release: the reliability lab's release of the lo...
- **REVIEW** `extract_note_battery_lab_2026-10-12.txt`: carries 3 of 5 distinctive words of the committed call: "Reserve 400 of lot ZC2638's 7,200 Model K packs at Friday's release."
- **REVIEW** `fin_rs04_battery_warranty_reserve_policy.pdf`: carries 4 of 5 distinctive words of the committed call: "Reserve 400 of lot ZC2638's 7,200 Model K packs at Friday's release."
- **REVIEW** `qm07_release_model_rl3_zp4820.pdf`: carries 3 of 5 distinctive words of the committed call: "Reserve 400 of lot ZC2638's 7,200 Model K packs at Friday's release."

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `extract_note_battery_lab_2026-10-12.txt`: 5 of 25 stump-paragraph terms appear (release, cycles, finished, genealogy, system); read whether the document names the move
- **REVIEW** `fin_rs04_battery_warranty_reserve_policy.pdf`: 7 of 25 stump-paragraph terms appear (release, cycles, finished, fin-rs-, effect, genealogy); read whether the document names the move
- **REVIEW** `model_k_pack_specification_rev_d.pdf`: 4 of 25 stump-paragraph terms appear (release, cycles, weakest, system); read whether the document names the move
- **REVIEW** `qm07_release_model_rl3_zp4820.pdf`: 6 of 25 stump-paragraph terms appear (release, cycles, finished, fin-rs-, validation, system); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 1)
- **REVIEW** `extract_note_service_operations_2026-10-09.txt`: names 3 of 3 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `service_cost_sheet_fy2026.xlsx`: names 3 of 3 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `carrier_statement_inbound_returns_2025-09_2026-10.csv`: names 3 of 3 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

The isolated reader (stage 4, fresh copies of `prompt.txt` and `target/` only; its verdict relayed by the main
session) came back clean: Q1 quotes no sentence announcing the decisive step; Q2 finds no file ranking or scoring the
answer or stating an asked figure; Q4 finds no figure or name reading as the answer; Q6 is an analytical choice; Q3
and Q5 raised no finding. Every REVIEW line is harmless, ruled one by one against the pack rebuilt after the judge's
repair (the two extract notes renamed, their contents kept):

- `extract_note_battery_lab_2026-10-12.txt`, "the model" x2: the fiction's own noun, the Model K pack. Harmless.
- `fin_rs04_battery_warranty_reserve_policy.pdf`, "the model" x4: the Model K pack and the release model RL-3 the
  policy cites. Harmless.
- `qm07_release_model_rl3_zp4820.pdf`, "the model" x2: RL-3, the memo's subject. Harmless.
- `fin_rs04_battery_warranty_reserve_policy.pdf`, "golden figure 2.4": the clause number 2.4 (Release), not a cell
  chance. Harmless.
- `extract_note_battery_lab_2026-10-12.txt`, three of the call's five words: the lot, its packs and its release are
  the note's subject; it states no reserve and no chance. Harmless.
- `fin_rs04_battery_warranty_reserve_policy.pdf`, four of the call's five words: the policy that books the reserve;
  it files the estimand and states no figure. Harmless.
- `qm07_release_model_rl3_zp4820.pdf`, three of the call's five words: the release memo's own words; no reserve and
  no pack chance. Harmless.
- `extract_note_battery_lab_2026-10-12.txt`, five stump terms (release, cycles, finished, extracts, system): the lab's
  vocabulary; it names no shared error, tray effect or joint chance. Harmless.
- `fin_rs04_battery_warranty_reserve_policy.pdf`, six stump terms (release, cycles, finished, fin-rs-, effect,
  system): "effective" on the revision line and the policy's own terms; no method. Harmless.
- `model_k_pack_specification_rev_d.pdf`, four stump terms (release, cycles, weakest, system): the weakest-cell rule
  the default path executes as well; it decides nothing between the routes. Harmless.
- `qm07_release_model_rl3_zp4820.pdf`, six stump terms (release, cycles, finished, fin-rs-, validation, system): the
  model, its features and its validation error, as filed; no error structure. Harmless.
- `extract_note_service_operations_2026-10-09.txt`, the partners beside numbers: country, region and vendor codes; it
  ranks nothing and states no cost. Harmless.
- `service_cost_sheet_fy2026.xlsx`, the partners beside numbers: contract rates for labour, handling and diagnosis,
  one part of an invoice line; no average cost and no ranking. Harmless.

The five ask readings the reader raised: CAP (a capacity replacement) is defined in the service extracts note; the
FX date and the pack-cost date each stay within the euro on every reading; the freight split and the repair month
are the asks' devices, settled by the carrier statement (each consignment billed once, with its pieces) and by the
invoice's service period.

## Solver's-eye read (round 2)

The targeted re-read after the judge's repair (fresh copies of `prompt.txt` and `target/` only; its verdict relayed by
the main session) is clean on Q1 to Q4: no sentence announces the decisive step, no file ranks or scores the answer or
states an asked figure, no file exists only to help the analyst, and no figure or name reads as the answer. Q6 is
analytical: the weakest-cell rule (the pack specification, section 4) and the error's population (FIN-RS-04 3.3, every
finished lot's life tests) are filed WHATs, and the tray-shared error they leave open is the stump. Its one finding,
a realism tell in the two sentences the repair added to `extract_note_service_operations_2026-10-09.txt` (they read
as instructions to the analyst), is fixed: both are reworded in the system owner's field-note voice with the same
content ("Battery scrapped where removed (swollen, or failed the transport check): not shipped, no returns-log row,
no carrier charge; case and invoice line unaffected." and "cycle_count: gauge cycle count when the fault was logged,
the fault's own cycle included."), and no data or figure moved. The thirteen REVIEW lines above are the classes of round 1
(the stump-term counts shift with the design note's own wording: the lab's note now shows genealogy, the policy one
term more) and stay harmless as ruled there: the fiction's own nouns, a clause number and the documents' subjects. The ask readings stay closed: CAP is defined in the service extracts note,
the FX date and the pack-cost date stay within the euro on every reading, and the freight split and the repair month
are the asks' devices, settled by the carrier statement and the invoice's service period.
