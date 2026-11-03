# leak check, task398

**Verdict: REVIEW.** 20 files read, 25 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: exposure, overlay, attribution, replay, trigger, manager, decisive, root-cause, nothing, prospectus, accumulation, holding, counterfactual, published, recorded, drawdown, changed, tracker, sentence, penrose, reports, target, question, return, linked

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `aov_2024-25_published_extract.pdf`: 7 of 25 stump-paragraph terms appear (exposure, overlay, manager, accumulation, holding, published); read whether the document names the move
- **REVIEW** `aov_2025-26_review_terms.docx`: 9 of 25 stump-paragraph terms appear (exposure, overlay, trigger, manager, prospectus, accumulation); read whether the document names the move
- **REVIEW** `thornbury_mruke_prospectus_extract_2026.pdf`: 7 of 25 stump-paragraph terms appear (exposure, overlay, manager, prospectus, accumulation, drawdown); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `corporate_actions_feed_20261016.csv`: 49 ISO dates after 2026-11-03, e.g. 2026-11-04, 2026-11-05, 2026-11-06, 2026-11-09, 2026-11-10

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### Pass 1, target.zip 896bc527 (isolated, sonnet, medium; prompt.txt and target/ only)

1. Decisive step: none. The closest is aov_2025-26_review_terms.docx 2.1, "A change is priced as the part of the accounting year's shortfall against the benchmark that it would have removed: the return of the fund's B Accumulation shares over the accounting year had the change been in force ... less the return of those shares over the accounting year as it ran, in basis points." It defines the estimand and does not say how to get there, and 2.3 ("The market and dealing in the fund's shares are taken as they were") adds scope only.
2. Ranking/scoring of candidates: none. fennick_quarterly_review_q3_2026.pdf and ashcombe_mandate_report_sep2026.xlsx report each sleeve against its own style index (not the benchmark, and not the board's changes). merrow_overlay_daily_monitor_2025-26.xlsx shows the overlay as it ran, and no change is priced anywhere.
3. Files existing only to help: none. Nothing is a guide or hint. The Larkspur 100 factsheet, the 2024-25 published extract, the liquidity fund yield file and the security master are context or distractors, not helpers.
4. Figure or name reading as the answer: none. The Fennick "Twelve months ... -6.60" and Ashcombe "0.99" lines are each sleeve against its own style index, a different quantity from the fund's shortfall against the All-Share, so they read as context. The 2024-25 extract says the overlay did not reduce exposure that year, which is background only.
5. Sentence fixing the figure: aov_2025-26_review_terms.docx 2.1 and 2.2: "the return of the fund's B Accumulation shares over the accounting year had the change been in force from the 12:00 valuation point on 30 September 2025, less the return of those shares over the accounting year as it ran" and "The accounting year runs from the 12:00 valuation point on 30 September 2025 to the 12:00 valuation point on 30 September 2026. The benchmark is the Larkspur UK All-Share Index (total return) taken at the fund's valuation point." Read literally: the shortfall is the B Acc share return over that window against the All-Share total return at the 12:00 level; each change's figure is the counterfactual B Acc return (change in force from the start) minus the actual B Acc return, in basis points, with the market and dealing taken as they were and the sub-adviser sleeve kept if not replaced. The tracker changes are fixed by "taken to earn the benchmark's total return between valuation points", and the overlay thresholds by the stated 12/6 per cent in place of 8/4. The prospectus 4.3-4.4 and 5.2 file the overlay and sleeve rules. The quarterly asks are filed by the prompt (ex-dividend date, paid or to be paid, cash or new shares; trade date; AIM at the custodian's prices at quarter-end).
6. What decides the main answer: an analytical choice. Counterfactual re-run of the fund path (B Acc return with the sleeves, overlay and rebalancing restated) with the filed terms leaving the modelling of the overlay interplay, sleeve flows and the chosen change to the analyst. No sentence announces the decisive step. Nothing planted is signposted; the asks lean on reading fields across the Holloway and Northcote custodians (date bases, ISIN against SEDOL, scrip alternatives), which are Layer 1 and ask-side only.

7. Realism: none found. Workbooks and PDFs carry plausible office authorship (Word for Microsoft 365, named people), the Fennick and Ashcombe reports have uneven monthly figures, and the CSVs have custodian-style formats (dd/mm/yyyy at Holloway, ISO at Northcote). Minor note only: the Merrow xlsx creator is a named person, not a library.
8. Data-describing file: none. No readme, dictionary or manifest. aov_2025-26_review_terms.docx and the prospectus extract are governing documents, not descriptions of the data.
9. World invented: none. All names are fictional (Thornbury, Larkspur, Holloway) but nothing states or implies this.

Sweep flag:
- corporate_actions_feed_20261016.csv, 49 ISO dates after 2026-11-03: harmless. They are payment_date values (2026-11-04 to 2026-11-10) on CONFIRMED dividends with ex dates in September 2026, in a feed dated 2026-10-16; this is ordinary forward payment dates on a feed cut before payment, matching the prompt's "paid or still to be paid". They hold no post-setting information beyond the feed's own date and give nothing away.

### Pass 2, target.zip 6749a0ae, after the review terms gained the equitised change's quarter-end clause

1. Decisive step stated: none. aov_2025-26_review_terms.docx 2.1 defines the pricing ("the return of the fund's B Accumulation shares over the accounting year had the change been in force ... less the return of those shares over the accounting year as it ran, in basis points") and 2.3 ("The market and dealing in the fund's shares are taken as they were, ... the fund is otherwise run as its prospectus requires"). These file the estimand and the counterfactual, not a step that says what to catch.

2. Ranking or scoring of candidates on the question: none. The Fennick PDF (12-month difference -6.61) and the Ashcombe sheet (+0.99) are sub-adviser returns against their own mandate benchmarks (Growth and Value indices), not against the All-Share benchmark, and do not rank the board's changes. The Merrow monitor and the share class price file show the as-run overlay, not any alternative.

3. Files that exist only to help the analyst: none as such. The security master gives market_segment (AIM/Main) and a cancelled status, which is needed for the AIM ask but is an ordinary reference file. Presumed distractors (own-benchmark sub-adviser reports, Larkspur 100 factsheet, 2024-25 AoV extract, liquidity fund yield) are plausible context, not helpers.

4. Figure or name reading as the answer: none. Closest: "Twelve months ... -6.61" in the Fennick PDF and "+0.99" in the Ashcombe sheet, but both are against a different benchmark and sleeve-level, so they read as context.

5. Literal sentence: aov_2025-26_review_terms.docx 2.1 plus 2.2 ("The accounting year runs from the 12:00 valuation point on 30 September 2025 to the 12:00 valuation point on 30 September 2026. The benchmark is the Larkspur UK All-Share Index (total return) taken at the fund's valuation point."). Literal result in words: the shortfall is the fund's B Acc price return between those two 12:00 points compared with the All-Share TR 12:00 level return over the same dates, in basis points; each change's figure is the B Acc return with that change in force from the start minus the as-run B Acc return, with the market and dealing taken as they were and the fund otherwise run per the prospectus (sections 3.2, 4.2 to 4.5, 5.1). Prospectus 4.3/4.4 file the overlay triggers (8 per cent, 63 valuation points, 4 per cent) literally, which also fixes the path under each variant.

6. Decider: an analytical choice, the counterfactual re-run of the fund through the prospectus mechanics (overlay trigger path, quarterly rebalancing, tracker sleeves, equitised liquidity) rather than a read-off or a one-line adjustment. Quoted: terms 2.3 "a sleeve the change leaves with its sub-adviser keeps that sub-adviser's holdings, and the fund is otherwise run as its prospectus requires" and prospectus 4.3. Not a field/unit reading as the main step and no planted item seen, though the asks (ex-date quarters, trade date vs settlement, AIM at custodian prices, scrip handling) are data-semantics and rule-application in nature, which is allowed for asks.

7. Generated-looking tells: none decisive. Minor: aov_2025-26_review_terms.docx has docProps timestamps 1980-01-01 in the zip and an empty-count app.xml (Words 0, Pages 1), a python-docx style template (Normal.dotm, stylesWithEffects.xml); author "Carol Rowe" is set. The PDFs claim Microsoft Word as producer, consistent. Merrow workbook creator "Julia Parry" matches the sheet text. Round contract values are plausible.

8. Files describing the data: none. The AoV terms docx and prospectus extract are governing documents, not a readme or dictionary; no data-dictionary or manifest sheets (each workbook has a single visible sheet, no comments).

9. World stated as invented: none (no words such as synthetic, fictional or exercise in the CSVs or documents).

Sweep flag:
- corporate_actions_feed_20261016.csv, 49 ISO dates after 2026-11-03: harmless. They are all payment_date values (up to 2026-11-30) on CONFIRMED events whose ex_date is on or before 2026-10-15 and record date on or before 2026-10-16, in a feed dated 2026-10-16; a future pay date for an already-declared dividend is normal. No ex, announcement or effective date is after the setting date.

### Ruling

Both passes: question 1 none, questions 2 to 4 none, question 6 an analytical choice, no describing file and nothing saying the world is invented. Pass 2's question 7 (the review terms carried the writing library's default-template properties: Words 0 and Pages 1 in docProps/app.xml, a stylesWithEffects part, a blank thumbnail) is fixed in the generator's scrub of every Office file's properties, asserted in checks.py; the shipped cut is target.zip 4d9a7a57, whose word/document.xml is byte-identical to 6749a0ae's and whose only other changed parts are that file's docProps, the styles part, its relationship and its content-types override, so no third pass is owed. The sweep 4 lines are the fund's own governing words, ruled in the design note; the sweep 9 dates are payment dates on declared dividends, ruled harmless by both passes.

### Determinism judge

Pass 1 on target.zip 896bc527: DETERMINISTIC, APPROVE; Gate G analytical_non_defect, no surface read, no sole data defect; Gate H domain pass, layers pass, decisive_step analytical (task398/determinism_check_report.md). Its two residual points are fixed: SF31 filed in the review terms, every graded figure at least 0.07 of a bin from its rounding edge.
