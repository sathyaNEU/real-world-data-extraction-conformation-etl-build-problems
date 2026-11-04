# leak check, task314

**Verdict: REVIEW.** 16 files read, 9 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: charge, fenwick, restructuring, prices, account, change, elasticity, marginal, decisive, surcharge, average, reading, estimate, block-price, method, effect, customers, whole-bill, comparison, nothing, history, record, billed, sentence, leaves

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `Agenda Report Stage 2 Drought Rate Options DRAFT 2026-10-27.docx`: carries 14 of 17 distinctive words of the committed call: 'Adopt Option C, the drought surcharge, as the Stage 2 rate measure for summer 2027: it takes about 20 acre-feet off the '
- **REVIEW** `Drought Contingency Plan Rev 2 (2025).pdf`: carries 15 of 17 distinctive words of the committed call: 'Adopt Option C, the drought surcharge, as the Stage 2 rate measure for summer 2027: it takes about 20 acre-feet off the '

## 4 design-note vocabulary (REVIEW 6)
- **REVIEW** `Agenda Report Stage 2 Drought Rate Options DRAFT 2026-10-27.docx`: 6 of 25 stump-paragraph terms appear (charge, fenwick, surcharge, effect, customers, billed); read whether the document names the move
- **REVIEW** `Drought Contingency Plan Rev 2 (2025).pdf`: 6 of 25 stump-paragraph terms appear (charge, fenwick, account, average, customers, billed); read whether the document names the move
- **REVIEW** `RES 2021-44.pdf`: 7 of 25 stump-paragraph terms appear (charge, fenwick, account, reading, effect, customers); read whether the document names the move
- **REVIEW** `RES 2023-12.pdf`: 6 of 25 stump-paragraph terms appear (charge, account, reading, effect, record, billed); read whether the document names the move
- **REVIEW** `RES 2024-17.pdf`: 4 of 25 stump-paragraph terms appear (charge, fenwick, account, record); read whether the document names the move
- **REVIEW** `UBBWCD Notice 2026-07 Dry-Year Allocation 2027.pdf`: 3 of 25 stump-paragraph terms appear (charge, average, customers); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 3)
- **REVIEW** `Agenda Report Stage 2 Drought Rate Options DRAFT 2026-10-27.docx`: names 5 column(s) of the data files verbatim (action, date, facility, gallons, station): confirm it is the organisation's own record and not a note written for the analyst
- **REVIEW** `RES 2021-44.pdf`: names 5 column(s) of the data files verbatim (SERVICE, completed, consumption, gallons, station): confirm it is the organisation's own record and not a note written for the analyst
- **REVIEW** `RES 2023-12.pdf`: names 5 column(s) of the data files verbatim (SERVICE, consumption, date, gallons, station): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 1, on a fresh copy of prompt.txt and target/ (target.zip sha256 e9e0ba523c45556054f6af4ff5950762c7ad46defa8f28616ef51a191e4841fd). Sweep 3's and sweep 4's lines were kept out of the brief and ruled in the main thread (the agenda report carries no recommendation and no saving; Plan 5.3 files the baseline and the accounts, never a price response; no resolution ties the Fenwick Mesa charge to use). Verdict: no leak; question 6 an analytical choice; no realism tell beyond mild uniformity in the meter shop's notes.

# Leak read, task314 (no solving, no figures)

1. Decisive step: none states it. Closest is Plan Section 5.3 (Drought Contingency Plan Rev 2 (2025).pdf): "The reduction a Stage 2 rate measure achieves is the fall it brings about in the water billed to single-family residential accounts on the June to September bills of the year it applies, from what those bills would have carried at the rates otherwise in force." The pack gives no method for that fall (no response to price is filed).
2. Ranking/scoring of the options: none. The agenda report says "The sizing and the recommendation will be added for the hearing." Its tables only list rates.
3. File existing only to help the analyst: none clearly. Context or distractor candidates: state_pws_water_use_2025.xlsx, conservation_rebates_2022-2026.csv, meter_shop_completed_work_orders_2025-2026.xlsx, bvw03 weather, UBBWCD notice, RES 2021-44 (superseded). All read as the organisations' own records.
4. Name or figure reading as the answer: none. Option labels A/B/C and the rates are inputs. Nothing states a saving, a winner or a gap.
5. Literal sentences fixing the estimand: Plan 5.3: "Each account's use without the measure is its baseline: for each of the four bill months, the average of the use billed to the account on that month's bills in the two preceding years. The accounts are the single-family residential accounts billed in each of the eight June to September bill months of those two years. Reductions are stated in acre-feet." Fixes: population = SFR (W10) accounts billed in all eight June-Sept bill months of 2025 and 2026 (the "two preceding years" for 2027 bills), window = June-Sept 2027 bill months, unit = acre-feet, comparison = reduction against each account's per-bill-month two-year-average baseline, at rates otherwise in force. Agenda report: options apply to SFR bills issued May 1 to October 31, 2027; Option A/B/C are additions to Resolution 2023-12 rates. Plan 1.2 defines "Bill month" as the month the bill is issued. For the City-measure ask, the report says targets come from "the 2026 June to September figures for the bulk fill station and the City facility meters", and RES 2021-44/2023-12 s.2 gives "each hundred cubic feet is billed as 748.052 gallons". Nothing files how usage responds to the rate change.
6. What decides it: an analytical choice. The pack supplies baseline and rates but no filed response rule, so the call rests on how the analyst models customers' behavioural response to each charge structure, a method the pack leaves open. The deciding text is the question itself plus Plan 5.3 ("the fall it brings about"). A strong analyst who executes the baseline and the rates mechanically (static bill arithmetic) would miss the fall. The unit and cohort rules (5.3, 748.052 gal/CCF, bill month) are stated, so they are context. No planted element seen.

## Flagged items
a. Harmless, because the agenda report is explicitly a draft with sizing and recommendation "to be added", lists only rate tables, and the Plan's Section 5.2 just says options, sizing and a recommendation will be brought; neither recommends, ranks, or carries any saving.
b. Harmless, because they read as the City's own documents: council resolution form, WHEREAS clauses, vote rolls, mayor/clerk/attorney signature blocks, exhibits of rates; the report is a standard council agenda report. Column names (rate_code W10, capital_recovery_charge, FENWICK MESA, service area code) are billing-system vocabulary the City's own documents would use, not analyst notes. The Resolution 2024-17 wording "identified in the City billing system by the service area code FENWICK MESA" is the slightly data-pointing sentence but is natural for an ordinance defining an area.
c. None. Neither the resolutions nor the plan say how use responds to a charge, price or rate change. The Plan's "demand reduction sought" percentages are targets, not responses; 4.2 measures are non-price. (Closest is the Plan's sentence on a reduction "met by all of the stage's measures together", which is a target.)

## Realism
Mostly none. Observations:
- Drought Contingency Plan Rev 2 (2025).pdf: PDF metadata Author "chaley" (the named Water Resources Manager, Clifford Haley), Word 2019, created 2025-03-27, two days after adoption on 2025-03-25: credible. Revision block, page "X of 5", headers, appendices are credible. The prepared/approved lines are blank, which is slightly odd for an adopted plan but plausible for a posted copy. Resolution No. 2025-08 cited but not shipped (fine).
- Resolutions: author "bsheppard" matches clerk Beth Sheppard; Word 365; dates match adoption days; numbering sequence plausible; signature lines blank (unsigned copies), plausible. Council names consistent across 2021 and 2023 and 2024 with absences varying. Possible tell: RES 2024-17 signature block orphaned alone on page 2 of 3 (looks like a real layout accident). In RES 2021-44 Julie Bowers absent but in 2023 present: fine.
- Agenda report docx: author Tami Weaver matches named author, revision 4, TotalTime 37, Normal.dotm, footer "draft for department review": credible. Very clean for 552 words, and its "Other Stage 2 measures" paragraph is a little prompt-shaped (it names the exact quantities, bulk fill and facility meters), but it reads as ordinary staff-report text.
- UBBWCD notice: different toolchain (Acrobat PDFMaker/Adobe PDF Library), author Sylvia Chavez the signing GM, fits a different organisation. Allocation table arithmetic is clean (78 per cent each member), perhaps uniform but natural for a pro-rata allocation.
- State xlsx, Corvane BWS xlsx (vendor header "Bulk Water Station Manager", generated stamp), CIS csv (KGAL, 8-digit bill no), city facility csv (mm/dd/yyyy, mixed GAL/CCF), fill station csv (ISO with -07:00 offsets) and meter shop xlsx do read as different systems with different date/unit conventions.
- Possible too-uniform: meter_shop work-order notes are a small closed set of reasons plus test-result strings; fill station account names and the card numbers are tidy; city facility reads by three readers with 08:51-style random times. None strong enough to flag as machine-built.
