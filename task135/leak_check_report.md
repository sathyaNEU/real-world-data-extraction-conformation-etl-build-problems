# leak check, task135

**Verdict: REVIEW.** 18 files read, 28 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: returns, valuation, decisive, prices, co-movement, sentence, struck, default, golden, covariance, twelve-month, holdings, mandate, covariances, ladder, measured, finance, forecasting, nothing, december, charity, report, november, same-dated, market

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `wrexford_investment_policy_2025-12.pdf`: golden figure 4.3 appears: ...olicy weights for the growth share under review. 4.3 The returns are daily, one for each business day...
- **REVIEW** `wrexford_investment_policy_2025-12.pdf`: carries 7 of 11 distinctive words of the committed call: "Set the 2027 growth share at 60 per cent: it is the largest of the policy's steps whose expected volatility stays inside"

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `brackenfold_export_notes_2026-12-02.txt`: 6 of 25 stump-paragraph terms appear (valuation, finance, december, charity, november, market); read whether the document names the move
- **REVIEW** `fernside_quarterly_report_2026-q3.pdf`: 3 of 25 stump-paragraph terms appear (returns, holdings, report); read whether the document names the move
- **REVIEW** `kestwick_charity_funds_key_facts_2026.pdf`: 5 of 25 stump-paragraph terms appear (returns, valuation, prices, charity, november); read whether the document names the move
- **REVIEW** `wrexford_finance_procedure_07_budget_2026-10.docx`: 6 of 25 stump-paragraph terms appear (valuation, mandate, finance, december, november, market); read whether the document names the move
- **REVIEW** `wrexford_investment_policy_2025-12.pdf`: 10 of 25 stump-paragraph terms appear (returns, valuation, prices, holdings, mandate, measured); read whether the document names the move

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

One isolated reader (Sonnet, medium) on fresh copies of `prompt.txt` and the re-cut `target/` (`target.zip` 0c031ac5), 2026-10-13. Its answers, condensed; the main thread's ruling follows each.

1. **The decisive step.** None stated. The reader took the hard part to be the mandate's daily time-weighted return from the custody files, and the shortcuts to be Fernside's 15.3 per cent and the factsheets' volatilities. It never named the striking times. Ruling: harmless; the decisive rung stays silent.
2. **A file ranking the steps.** None: nothing gives a volatility, an income or an answer by step. Ruling: harmless.
3. **A file that exists only to help.** None obviously. The export notes are a custodian's data dictionary, and the market calendars read as the least organic file, though a custodian or vendor supplies one. Ruling: harmless; the calendars are Layer 1 (the holiday days), shipped since the first cut.
4. **An answer-like figure.** None. The annex's 80 per cent is last year's setting, and Fernside's and the factsheets' volatilities are per holding. Ruling: harmless.
5. **Sentences fixing the main figure.** Policy 3.4 (not more than 10 per cent), 4.1 (the standard deviation of the twelve-month total return), 4.2 (the holdings' own prices and income, time-weighted, the two years to the last month-end valuation, the policy weights in every period), 4.3 (daily returns, one for each business day, equally weighted), 4.4 (before rounding), 2.3 (the mandate's cash). Read literally: a daily, equally weighted estimate over the window, "silent on the annualisation factor". Ruling: the literal execution is the golden's estimand. The step from a day's covariance to a year's variance is the open method, which the data force; it is not a reading.
6. **What decides.** "An analytical choice, with a data-structure element." The reader placed it in the mandate's return construction. Ruling: the decisive step is analytical, but it is not the one the reader names. The return construction is Layer 1 and every handling of it keeps the call (asserted). The reader not finding the striking-time step is the silence the design wants.

**Realism.** Plausible for a small UK charity, its custodian, a segregated equity manager and a charity fund range. The reader flagged details that might read as generated. Ruling on each: left as they are, all on files unchanged since the first cut.
- The Kestwick range's tidy symmetry: four funds launched together on 3 April 2009, the Japan fund on 1 October 2012, five factsheets in one manager's template, and charges that differ by fund.
- Distributions on set days, as a fund manager pays them.
- The short Fernside letter.
- The custodian's export run of 2 December, after the 30 November valuation.

**REVIEW lines, ruled.** The policy's clause number 4.3 and the call's vocabulary in the policy: a clause and the decision's own words. The generic stump-paragraph words in the export notes, Fernside's report, the key facts, procedure 7 and the policy: none of these documents names a period length, a lag or an estimator. The dates after 2 December: income pay dates for dividends that went ex by 30 November, and the market calendars through 2027, forward-looking by nature. All harmless.
