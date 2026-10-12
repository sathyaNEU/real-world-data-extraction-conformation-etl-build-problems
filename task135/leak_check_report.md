# leak check, task135

**Verdict: REVIEW.** 18 files read, 28 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: default, decisive, mandate, returns, golden, prices, valuation, design, market, samples, measured, reflex, holding, report, sentence, co-movement, correction, architecture, polish, periods, analyst, generator, target, sample, smearing

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `wrexford_investment_policy_2025-12.pdf`: golden figure 4.3 appears: ...olicy weights for the growth share under review. 4.3 The two years are divided into return periods of...
- **REVIEW** `wrexford_investment_policy_2025-12.pdf`: carries 7 of 11 distinctive words of the committed call: "Set the 2027 growth share at 60 per cent: it is the largest of the policy's steps whose expected volatility stays inside"

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `brackenfold_export_notes_2026-12-02.txt`: 4 of 25 stump-paragraph terms appear (valuation, design, market, holding); read whether the document names the move
- **REVIEW** `fernside_quarterly_report_2026-q3.pdf`: 3 of 25 stump-paragraph terms appear (returns, holding, report); read whether the document names the move
- **REVIEW** `kestwick_charity_funds_key_facts_2026.pdf`: 3 of 25 stump-paragraph terms appear (returns, prices, valuation); read whether the document names the move
- **REVIEW** `wrexford_finance_procedure_07_budget_2026-10.docx`: 4 of 25 stump-paragraph terms appear (mandate, valuation, market, holding); read whether the document names the move
- **REVIEW** `wrexford_investment_policy_2025-12.pdf`: 9 of 25 stump-paragraph terms appear (mandate, returns, prices, valuation, design, measured); read whether the document names the move

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `brackenfold_income_entitlements_by_lot_2025-11_2026-11.csv`: 26 ISO dates after 2026-12-02, e.g. 2026-12-15, 2026-12-17, 2026-12-18, 2026-12-24, 2026-12-30
- **REVIEW** `market_calendars_2024-2027.csv`: 846 ISO dates after 2026-12-02, e.g. 2026-12-03, 2026-12-04, 2026-12-07, 2026-12-08, 2026-12-09

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

Reader (Sonnet, medium) on the stage 3 cut, prompt.txt and target/ only. Questions 1 to 4: none (the nearest are policy 4.2 and 4.3, the method rules, which name no trap; the single-holding volatilities in the Fernside report and the Kestwick factsheets are holding-level, not portfolio figures; no helping file; no answer-like figure). Question 5: policy 3.4, 4.1, 4.4 with 2.1 to 2.3, and finance procedure 7.2 to 7.6 for the asks; not executed by the reader. REVIEW lines: all harmless (clause number 4.3, policy vocabulary, the entitlements' pay dates for events already ex, the forward holiday calendar). Realism: nothing reads machine-made. Readings raised: the number of equal periods (policy 4.3 says at least 100); "the last month-end valuation before the review" (30 November 2026 by the export date, not stated outright); whether the capital release is capped at the expendable endowment's value (policy 6.2).
