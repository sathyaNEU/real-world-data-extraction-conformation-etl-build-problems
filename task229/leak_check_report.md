# leak check, task229

**Verdict: REVIEW.** 18 files read, 18 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: population, decisive, counts, record, accrual, moment, architecture, checks, construction, estimand, corderoy, control, accuracy, routine, history, logistics, method, stand-down, measurement, resets, carries, exception, weighted, builds, missing-data-censoring-measurement-error

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `Thornacre_SCS-07_peak_stock_record_standard_v3.pdf`: golden figure 97.0 appears: ...en its record accuracy at the measurement time is 97.0 per cent or more, and is supervised otherwise. 5....

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `Corderoy_CP-THN-04_perpetual_count_programme.docx`: 9 of 25 stump-paragraph terms appear (counts, record, corderoy, control, routine, history); read whether the document names the move
- **REVIEW** `Thornacre_SCS-07_peak_stock_record_standard_v3.pdf`: 7 of 25 stump-paragraph terms appear (record, moment, control, accuracy, history, logistics); read whether the document names the move
- **REVIEW** `extract_notes_LF_20261207.txt`: 5 of 25 stump-paragraph terms appear (record, corderoy, history, logistics, stand-down); read whether the document names the move

## 9 dates after the setting (REVIEW 6)
- **REVIEW** `THN_store_replen_forecast_run_20261123.csv`: 120624 ISO dates after 2026-12-07, e.g. 2026-12-08, 2026-12-09, 2026-12-10, 2026-12-11, 2026-12-12
- **REVIEW** `THN_store_servicing_map.csv`: 48 ISO dates after 2026-12-07, e.g. 2026-12-26, 2026-12-27
- **REVIEW** `THN_store_trading_calendar_2026_27.csv`: 1625 ISO dates after 2026-12-07, e.g. 2026-12-24, 2026-12-25, 2026-12-26, 2026-12-31, 2027-01-01
- **REVIEW** `WMS_batch_register_THN_20261207_0600.csv`: 8345 ISO dates after 2026-12-07, e.g. 2027-03-07, 2027-03-08, 2027-03-09, 2027-03-10, 2027-03-11
- **REVIEW** `WMS_stock_by_location_THN_20261207_0600.csv`: 8345 ISO dates after 2026-12-07, e.g. 2027-03-07, 2027-03-08, 2027-03-09, 2027-03-10, 2027-03-11
- **REVIEW** `goods_in_bookings_summary_7Dec_3Jan.csv`: 520 ISO dates after 2026-12-07, e.g. 2026-12-08, 2026-12-09, 2026-12-10, 2026-12-11, 2026-12-12

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Read 1 (2026-10-11, Sonnet at medium effort, design 2), verbatim:

1. Decisive step: none. No sentence announces it. The nearest is SCS-07 4.5: "Where the 3PL does not count every in-scope location at the measurement time it estimates record accuracy from its count records, and the estimate is the one a full count at the measurement time would be expected to bear out." That sentence states the estimand and leaves the method open. CP-THN-04 s.3 and s.6, and the extract notes, only describe the cycle and the stand-down.

2. Ranking or scoring file: none. No file scores or ranks the eight centres on record accuracy. The count history, location master and stock-by-location files are raw rows. The labour plan and the goods-in summary are about volumes.

3. Existence only to help: none. The extract notes (extract_notes_LF_20261207.txt) read as a BI analyst's hand-over note. The one that comes closest is corderoy_thornacre_centre_register.csv (site, depot, instance, shared_site), but a 3PL would plausibly keep it. The extract note about other clients' faces in the location master is a data caveat, not a pointer to the method.

4. Answer-like figure or name: none in the documents. The 97.0 is the filed line, which the request already asks us to show beside each share. The "96.0 per cent" in the v2 history is an old line. No centre is named as qualifying or failing anywhere.

5. Basis sentence: SCS-07 4.3: "Record accuracy at a time is the number of in-scope locations whose record a full count at that time would find correct, divided by the number of in-scope locations at that time, as a percentage." This is read with 4.1 (in scope = a pick face holding a slot for a Thornacre line on the location master at that time, not on quality hold or recall), 4.4 (the time is 06:00 on 7 December 2026) and 4.5 (estimate from count records if not every location is counted). A literal execution asks for the following. Take the pick faces in scope at 06:00 on 7 December. Ask what proportion of them a full count at that moment would find correct, which is a population-level estimate at that moment and not the raw share of matched count tasks. Divide correct by in-scope, per centre.

Fork line. Two readings of the main figure are open, and the documents do not rule out all of them.
- Population and membership: the 4.1 "at a time" wording against the location master's effective dates, and the shared-site rows in the location master, whose client code is not THN (extract notes: "their client code is not THN"). 4.1 says "a pick face holding a slot for a Thornacre line", and CP-THN-04 s.1 says "Every pick face holding a Thornacre line" with "no Thornacre pick face holds a weighed line". These point the same way, so this is not really a fork.
- Basis of the share: 4.3 ("a full count at that time would find correct") against 4.5 ("estimates ... from its count records"). One reading is the proportion of count tasks, or of the latest count per face, that matched. The other is a figure for all in-scope faces at the measurement moment, which means accounting for faces counted long before or not yet counted. Their routine cycles (CP-THN-04 s.2: 28, 56 and 91 days) make the last count stale for some faces. 4.3 and 4.5 together favour the second reading ("the estimate is the one a full count at the measurement time would be expected to bear out"). They do not strictly rule out the first, since 4.5 does not say how the estimate is built. The documents do not rule out the naive reading in so many words.
- Moment: 4.4 fixes 06:00 on 7 December, and the extract notes give the UTC and local trading-day convention (clocks went back on 25/10, and the 02:00-05:30 window belongs to the previous trading day). That leaves little room for a time fork. Count-window UTC offsets are a mess point, not an ambiguity.
- Correct record: 4.2 says correct is equal to a count in the stock unit, and the WMS `result` is "confirmed against system quantity". The history carries first_count, recount and confirmed quantities. Whether first count or confirmed count defines "correct" is not stated in 4.2. CP-THN-04 s.5 says the confirmed count is posted as the record, which favours the confirmed count. This reading is not explicitly excluded.
- Rounding: the request says whole per cents, and the line is 97.0. Rounding a share (for example 96.6 to 97) against the 97.0 line is not addressed. The standard tests "97.0 per cent or more", which implies the unrounded share. The request's whole-per-cent display could be read against it. This is a mild fork.
- Stock value: the request says "the Thornacre stock value on the faces the gate covers". The cost price list (28/11) against the P10 cost changes (effective 2026-12-06, so before 7 December) is a possible cost-basis fork. The documents do not state which cost applies at 06:00 on 7 December. Units are cases against eaches, which the line master's Stock Unit and Case Size columns settle.
- Forecast cases: the forecast is the 23/11 run, the "last full run before the freeze". The freeze window is 06:00 7 Dec to 06:00 4 Jan. The servicing map has valid-from and valid-to dates, so the depot for a store can change mid-window. The trading calendar has closed days. Whether to cut forecast rows on closed days is not stated. The forecast unit is CS or EA by category (the category table gives units_per_case), so the conversion to cases is derivable. Dates beyond the freeze or before it are a window question the standard answers (the freeze dates).
- Chart: the request defines it fully (largest first, labelled, title naming the centre with the most). No fork.

Verdicts on the ten flagged lines:
- SCS-07 pdf, golden figure 97.0: harmless. It is the filed line in the standard, shown in the request as "the standard's line". It is not a result.
- CP-THN-04 docx, 9 of 25 terms: harmless. The terms are generic (counts, record, control, routine, history). It describes the cycle and the stand-down and does not name the move.
- SCS-07 pdf, 7 of 25 terms: harmless. Same reason. The terms are in the definitions, and the standard states the estimand (4.3, 4.5) without naming a method.
- extract_notes_LF, 5 of 25 terms: harmless. It records file provenance, timestamps and the UTC convention. It gives no method.
- THN_store_replen_forecast_run_20261123.csv, dates after 2026-12-07: harmless. A forecast run naturally covers future trading dates, and the freeze runs to 4 January.
- THN_store_servicing_map.csv, dates after 07/12: harmless. These are valid-from and valid-to dates of servicing changes (26/12 and 27/12), which are plausible schedule data.
- THN_store_trading_calendar_2026_27.csv, dates after 07/12: harmless. It is a forward trading calendar for Christmas and New Year.
- WMS_batch_register, dates after 07/12: harmless. These are best-before dates, which sit in the future by nature.
- WMS_stock_by_location, dates after 07/12: harmless. The same best-before dates.
- goods_in_bookings_summary_7Dec_3Jan.csv, dates after 07/12: harmless. The file name states the forward booking window, and the bookings are plans.
