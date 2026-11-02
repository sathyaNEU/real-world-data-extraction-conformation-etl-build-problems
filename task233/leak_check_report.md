# leak check, task233

**Verdict: REVIEW.** 14 files read, 26 golden figures and 12 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: agreement, regions, change, re-collection, back-check, register, frequency, database, points, silent, prices, outlet, halbrook, recorded, decisive, quantity, recording, golden, collector, sentence, measure, collectors, chance, netting, back-checks

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `pcqs_price_collection_quality_standard_v3.pdf`: 8 of 25 stump-paragraph terms appear (agreement, back-check, prices, outlet, recorded, collector); read whether the document names the move
- **REVIEW** `pcsa_schedule4_collection_fees.pdf`: 3 of 25 stump-paragraph terms appear (agreement, outlet, halbrook); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 2)
- **REVIEW** `cpi_outlet_register_2026-10.xlsx`: names 10 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `cpi_regional_indices_2026-06_2026-09.csv`: names 10 of 12 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `pcsa_schedule4_collection_fees.pdf`: names 10 of 12 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `nso_collection_calendar_2026.csv`: 3 ISO dates after 2026-10-16, e.g. 2026-10-26, 2026-11-10, 2026-12-08

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read (Leak reader, architecture 3 round 1 (2026-11-02, isolated, Sonnet at medium effort, on target.zip 62987245))

1. Decisive step: none announced; the nearest is PCQS 3.2 ("Items the officer cannot find are left out"), the standard's own definition.
2. Nothing ranks or scores the regions on collection quality (the back-check register is raw rows; the regional indices are price indices).
3. Nothing exists only to help the analyst (status codes and calendar are office reference tables).
4. Nothing reads as the answer (Schedule 4 fees and the contractor's activity counts only).
5. PCQS 3.1 read literally: a region's accuracy is the share of all prices its collectors recorded in the quarter that were the offered price at the time of recording, replacements included; 3.2 makes the back-check sample the estimate; 3.3 applies the bands unrounded; the estimator (how a disagreement or a missing item is treated) is not given.
6. An analytical choice: estimating the population quantity from the back-check sample; secondary asks follow stated rules (timeliness windows and takeover, replacement acceptance).
Sweep flags: the standard and the fee schedule are harmless; the outlet register lists outlets and regions with no rank; the contractor's return states activity counts only ("as uploaded from the handhelds before NSO validation"); the calendar's later dates are index days and a public holiday.
Realism finding (sent to the builder before the judge reads it): the outlet register's Kind column reads as randomly assigned against outlet names (pharmacies as butchers, a bakery as a greengrocer); rows mildly mechanical in order.

## Solver's-eye read (Leak reader round 1 realism fix (2026-11-02, on target.zip edd35bde))

The round 1 reader's one finding (outlet names drawn independently of their kind in the outlet register) was fixed in the generator: names now come from each kind's own templates, the register runs in code order, and assertions Z11 to Z13 hold; no graded figure moved. The judge read the fixed cut.
