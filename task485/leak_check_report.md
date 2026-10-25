# leak check, task485

**Verdict: REVIEW.** 17 files read, 42 golden figures and 20 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: scrubber, removal, limestone, balance, consumed, removed, design, register, returns, reagent, reader, architecture, inventory, directorate, nothing, delivery, performance, reports, permit, annual, candrigg, decisive, bypass, tested, guarantee

## 3 answer figures in the pack (REVIEW 7)
- **REVIEW** `scrubber_guarantee_schedules.pdf`: golden figure 13.9 appears: ...ar Tannery Main boiler 85,000 4,520 94.0 271 1.03 13.9 1.35 520 10.4 Signed for Kellfold Process Systems...
- **REVIEW** `scrubber_guarantee_schedules.pdf`: golden figure 160 appears: ...03 Umbgarth District Heating Main boiler 85,000 3,160 95.0 158 1.05 12.7 1.25 670 14.8 For Lundsett Abs...
- **REVIEW** `scrubber_guarantee_schedules.pdf`: golden figure 390 appears: ...neral Hospital Energy Centre Main boiler 94,000 3,390 95.0 170 1.05 12.0 1.30 670 13.7 NPA/CB/0607 Hask...
- **REVIEW** `scrubber_guarantee_schedules.pdf`: golden figure 320 appears: ...Main boiler 48,000 3,440 94.0 206 1.07 11.1 1.59 320 6.9 NPA/CB/0496 Kirlgate Maltings Main boiler 39,...
- **REVIEW** `scrubber_tests_2026_iverstow.pdf`: golden figure 160 appears: ...067 68,700 2,550 149 94.2 IET/26/070 31,000 2,320 160 93.1 Table 2. Results at 6 per cent oxygen, dry....
- **REVIEW** `scrubber_tests_2026_iverstow.pdf`: golden figure 320 appears: .../26/067 68,700 2,550 149 94.2 IET/26/070 31,000 2,320 160 93.1 Table 2. Results at 6 per cent oxygen, d...
- **REVIEW** `so2_inventory_guidance_2026.pdf`: golden figure 3.3 appears: ...64.066 tonnes for every 32.065 tonnes of sulphur. 3.3 Each boiler is compiled on its own, including a b...

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `scrubber_guarantee_schedules.pdf`: 9 of 25 stump-paragraph terms appear (removal, limestone, removed, design, directorate, performance); read whether the document names the move
- **REVIEW** `scrubber_tests_2026_iverstow.pdf`: 6 of 25 stump-paragraph terms appear (removal, limestone, performance, permit, annual, candrigg); read whether the document names the move
- **REVIEW** `scrubber_tests_2026_jarrness.pdf`: 4 of 25 stump-paragraph terms appear (removal, performance, permit, tested); read whether the document names the move
- **REVIEW** `so2_inventory_guidance_2026.pdf`: 9 of 25 stump-paragraph terms appear (removed, register, returns, inventory, directorate, delivery); read whether the document names the move
- **REVIEW** `so2_order_2027_schedule_note.pdf`: 7 of 25 stump-paragraph terms appear (removal, register, returns, inventory, directorate, permit); read whether the document names the move

## 6 ranking artifacts (REVIEW 10, INFO 1)
- **REVIEW** `ash_contractor_customers.csv`: names 11 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `boiler_returns_2026.xlsx`: names 16 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `coal_deliveries_2026.csv`: names 12 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `coal_supplier_customers.csv`: names 16 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `limestone_certificates_2026.xlsx`: names 16 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `permitted_boilers_register_2026.xlsx`: names 16 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `scrubber_guarantee_schedules.pdf`: names 15 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `scrubber_tests_2026_iverstow.pdf`: names 7 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `scrubber_tests_2026_jarrness.pdf`: names 8 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `whinmoss_invoice_lines_2026.xlsx`: names 7 of 20 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `carnhope_jobs_2026.csv`: names 10 of 20 answer-set candidates; confirm it does not rank them on the decision question

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

Round 1 on zip 9263b80dcd8ccb1c8722ce81d63f66d3 (architecture 3), two isolated scored readers (sonnet, medium, fresh
copies of the prompt and target/ only).

- Question 1 (the decisive step announced): none from both. Nearest quoted: the guidance's section 3.1 ("less the sulphur
  dioxide its abatement plant removed over the year") and the permit register's condition C5 ("so far as practicable").
- Question 2 (a ranking on the prompt's question): none from both.
- Question 3 (a file existing only to help): the guidance and the Order's note; the certificates workbook's Delivery
  points and Notes sheets and the two customer cross-references as keys.
- Question 4 (an answer read as context): none; both named the register's design removal and the tests' removals as the
  tempting shortcut rather than an answer.
- Question 5 (the literal sentence): the guidance's 3.1, 4.2 and 6.1; both read 3.1's "over the year" as leaving the
  removal's measurement open and the limestone records as the only year-covering source.
- Question 6: both, an analytical choice (the year's removal from the limestone consumed rather than the design or the
  one-day test).
- Question 7 (generated look): load weights in narrow bands (coal 27.5 to 32 tonnes, limestone 26.0 to 29.6), one analysis
  shared by every truck under a certificate, the weekly carbonate in a narrow band, evenly spaced tests, and Whinmoss's
  repeated 26.0 tonne lines; nothing called conclusive.
- Part 3: every flagged line harmless on both reads.

Outcome: both readers landed the call (the golden six, 18 of 18 boiler tonnes and listings; score_reader FAIL on both);
ask A held at 1 of 32 on both. The architecture is spent at stage 4; see the design note's architecture 3 record.
