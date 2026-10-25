# leak check, task166

**Verdict: REVIEW.** 16 files read, 8 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: region, mortgage, posted, credit, balances, payoffs, balance, blended, report, planning, decisive, december, senior, incentive, million, stacks, record, policy, purchase, refinancing, lock-in, behind, mortgages, repeat, decision

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `alm_report_2026_q3.pdf`: 8 of 25 stump-paragraph terms appear (mortgage, posted, credit, balance, report, planning); read whether the document names the move
- **REVIEW** `data_dictionary.txt`: 11 of 25 stump-paragraph terms appear (region, mortgage, posted, credit, balance, report); read whether the document names the move
- **REVIEW** `lending_policy_7-4_he_payoff_forecast.pdf`: 11 of 25 stump-paragraph terms appear (region, mortgage, posted, credit, balance, report); read whether the document names the move

## 9 dates after the setting (REVIEW 4)
- **REVIEW** `first_mortgage_servicing_2026-11.csv`: 3707 ISO dates after 2026-12-03, e.g. 2026-12-06, 2026-12-22, 2027-01-13, 2027-01-23, 2027-02-22
- **REVIEW** `heloc_lines_2026-11.csv`: 1800 ISO dates after 2026-12-03, e.g. 2026-12-05, 2026-12-06, 2026-12-12, 2026-12-14, 2026-12-26
- **REVIEW** `payoff_statement_log_2025-10_2026-11.csv`: 48 ISO dates after 2026-12-03, e.g. 2026-12-04, 2026-12-07, 2026-12-08, 2026-12-09, 2026-12-10
- **REVIEW** `planning_cycle_2027_rates.xlsx`: 36 ISO dates after 2026-12-03, e.g. 2027-01-01, 2027-02-01, 2027-03-01, 2027-04-01, 2027-05-01

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

Two isolated readers on f022d2a9 (`target.zip` sha256 f022d2a94b534aad60cf312d47530b6b1cb007572ec9d90e47adf0788f48bdf2), each holding the pack, `prompt.txt` and the flat `figures.json` key paths to fill.

### Reader A (Sonnet, medium)

`score_reader`: PASS (call 0 of 3, asks 0 of 36)

### Reader answers

1. Decisive step: no file states it. The nearest pointer is lending_policy_7-4_he_payoff_forecast.pdf, 7.4.3: "Rates: the planning cycle's base case, which states the credit union's posted rates as monthly averages for each month from December 2026 to December 2027." It says which rates to use, not how payoffs respond. The first-mortgage link is only visible in he_lending_file (senior_lien_* fields; data_dictionary.txt: "The senior lien fields are the first mortgage tradeline on the applicant's credit report at application.").
2. Ranks or scores the candidates: none. (alm_report_2026_q3.pdf gives portfolio totals only, no per-center payoffs.)
3. Exists only to help the analyst: data_dictionary.txt and export_manifest.csv ("This list"). Quote: "Loan numbers changed at the conversion and the conversion cross-reference links them." (policy 7.4.4), which core_conversion_xref.csv serves.
4. Reads as the answer rather than context: none. Closest is county_region_map.csv (assigns centers) and the policy sentence "The pilot opens in the regional lending center whose members are forecast to pay off the most fixed-rate home equity principal in calendar 2027." (7.4.2), which is the criterion, not an answer.
5. Sentences that fix the estimand: "Outcome: principal paid ahead of schedule, which is the principal retired when a loan is paid in full before its maturity date and any principal paid in a month above that month's scheduled principal." and "Population: the fixed-rate closed-end home equity loans on the books at the close of business on 30 November 2026." and "Window: payments posted from 1 January 2027 to 31 December 2027." Literal result: 8,813 active loans, 2027 ahead-of-schedule principal by center (my model) Lakeshore about 24.6, Grand Rapids 18.4, Muskegon 13.2, Kalamazoo/Battle Creek 13.1 (USD M). Nothing fixes how the forecast is computed (method open).
6. An analytical choice. Nothing is quoted as deciding it; the policy only fixes the estimand. The deciding work is building the payoff-timing model: payoffs are driven by the first-mortgage refinance incentive (senior lien rate minus the mortgage rate), not by the home equity loan's own rate or by recent run rate, then running it on the base-case rate path. A trailing run rate (2026 payoffs) picks Kalamazoo and Battle Creek instead.

#### Mechanical scan items
- first_mortgage_servicing_2026-11.csv, 3707 dates after 2026-12-03: harmless. These are maturity_date values of mortgages (2027 to 2056), not events after the pull.
- heloc_lines_2026-11.csv, 1800 dates: harmless. draw_period_end dates, contractual future dates.
- payoff_statement_log_2025-10_2026-11.csv, 48 dates: harmless. good_through_date on statements issued in Nov 2026, a date the quoted amount is good to; no outcome information.
- planning_cycle_2027_rates.xlsx, 36 dates: harmless. The month labels of the scenario rates (Dec 2026 to Dec 2027, three sheets); they are the forecast inputs the policy tells you to use.

#### How I reached the answer
Asks: from the statement log I kept ISSUED and UPDATED rows (dropped VOID), dropped HELOC (L-numbers) and mortgage (M-numbers) references, mapped legacy loan numbers through core_conversion_xref, converted issued_utc to Eastern time to assign quarters (no row moved quarter in practice), added the hand-prepared March 2026 statements for "Home equity loan" and "1st mortgage + home equity" (matched by property address to the lending file; dropped HELOC and first-mortgage-only rows), counted each loan once per quarter, assigned the center by property county, and counted payoff as PIF in the core trial balance with CloseDate on or before 30 Nov 2026 (MAT/charge-offs not counted).

Forecast: I built a loan-month panel from the legacy master (2019 to Aug 2024) and the core trial balance (to Nov 2026), about 363k loan-months and 5,264 paid-in-full events. Hazard of payoff turned out to depend almost entirely on the first-mortgage refinance incentive: the senior lien note rate (given for purchase loans; for others backed out of the senior balance and original amount, because about 5 percent of reported senior payments look escrow-inflated) minus the posted 30 year (15 year for 180 month senior terms) rate. Annual hazard is about 5 percent when the senior loan is out of the money and rises along a logistic curve to about 60 percent once the senior rate is roughly 1 point above market; the curve is the same in 2019-2021 and 2024-2026. Rate lagged one month fit best. Own home equity rate gap, center, season, HPI, credit score, CLTV and loan age added essentially nothing once this was in. A mild loan-size effect on the baseline was kept. Partial prepayments (about 3.1 percent of loan-months, about 0.16 percent of balance a month) were added on survivors. I ran the 8,813 loans active at 30 Nov 2026 through 2027 with the planning base case (30 year falling from 6.62 to 5.20), with survival and amortisation by loan. Back-test on 2026 (Dec 2025 book, actual rates): predicted 34.9 vs 33.3 actual USD M in total, centers within about 20 percent. Alternatives: trailing run rate (favours Kalamazoo/Battle Creek because of a 2023 campaign cohort already in the money), HE-rate-gap model (fits poorly), +/-100 bp scenarios (Lakeshore stays first, though much less so in rates up). Lakeshore leads because its 2025-26 purchase-money loans carry 6.6 to 7 percent first mortgages that come into the money in 2027; Kalamazoo/Battle Creek's 2023 cohort is mostly gone already. Principal for the Lakeshore is about USD 24.6 M, which rounds to 20 (nearest 10); the rounding is close to the 30 boundary only in the lag-0 variant (25.4).

Odd things: Aug-Nov 2023 spike of about 1,740 small loans in Kalamazoo/Battle Creek; escrow-inflated senior payments on some non-purchase liens; the statement system outage 9 to 20 March 2026 covered by the manual workbook; the first mortgage servicing payoffs coincide to the day with payoffs of home equity loans whose senior lien is the credit union; the planning cycle's December 2026 rate differs from the November 2026 posted rate; ALM loan count (8,567) differs slightly from the trial balance.

`reader.json`:

```json
{
 "call.center": "The Lakeshore",
 "call.principal_2027_musd": 20,
 "call.second": "Grand Rapids",
 "steps.forecast_musd.Grand Rapids": 18.4,
 "steps.forecast_musd.The Lakeshore": 24.6,
 "steps.forecast_musd.Kalamazoo and Battle Creek": 13.1,
 "steps.forecast_musd.Muskegon and the North": 13.2,
 "asks.Grand Rapids|2025Q4.quoted": 43,
 "asks.Grand Rapids|2025Q4.paid_in_full": 36,
 "asks.Grand Rapids|2026Q1.quoted": 57,
 "asks.Grand Rapids|2026Q1.paid_in_full": 47,
 "asks.Grand Rapids|2026Q2.quoted": 46,
 "asks.Grand Rapids|2026Q2.paid_in_full": 41,
 "asks.Grand Rapids|2026Q3.quoted": 60,
 "asks.Grand Rapids|2026Q3.paid_in_full": 45,
 "asks.Kalamazoo and Battle Creek|2025Q4.quoted": 118,
 "asks.Kalamazoo and Battle Creek|2025Q4.paid_in_full": 117,
 "asks.Kalamazoo and Battle Creek|2026Q1.quoted": 95,
 "asks.Kalamazoo and Battle Creek|2026Q1.paid_in_full": 90,
 "asks.Kalamazoo and Battle Creek|2026Q2.quoted": 79,
 "asks.Kalamazoo and Battle Creek|2026Q2.paid_in_full": 71,
 "asks.Kalamazoo and Battle Creek|2026Q3.quoted": 88,
 "asks.Kalamazoo and Battle Creek|2026Q3.paid_in_full": 84,
 "asks.Muskegon and the North|2025Q4.quoted": 44,
 "asks.Muskegon and the North|2025Q4.paid_in_full": 37,
 "asks.Muskegon and the North|2026Q1.quoted": 38,
 "asks.Muskegon and the North|2026Q1.paid_in_full": 30,
 "asks.Muskegon and the North|2026Q2.quoted": 37,
 "asks.Muskegon and the North|2026Q2.paid_in_full": 29,
 "asks.Muskegon and the North|2026Q3.quoted": 50,
 "asks.Muskegon and the North|2026Q3.paid_in_full": 36,
 "asks.The Lakeshore|2025Q4.quoted": 65,
 "asks.The Lakeshore|2025Q4.paid_in_full": 60,
 "asks.The Lakeshore|2026Q1.quoted": 64,
 "asks.The Lakeshore|2026Q1.paid_in_full": 55,
 "asks.The Lakeshore|2026Q2.quoted": 43,
 "asks.The Lakeshore|2026Q2.paid_in_full": 37,
 "asks.The Lakeshore|2026Q3.quoted": 71,
 "asks.The Lakeshore|2026Q3.paid_in_full": 60
}
```

### Reader B (Opus, medium)

`score_reader`: exit 1 (call 3 of 3, asks 0 of 36)

### Reader answers

1. **Decisive step stated anywhere?** None. `lending_policy_7-4_he_payoff_forecast.pdf` 7.4.3 defines the population, outcome, window, region and rates, but no file says what drives a loan's payoff or how to model it.

2. **File that ranks or scores the candidates on the question?** None. `alm_report_2026_q3.pdf` gives only portfolio totals ("Fixed-rate home equity loans stood at $424.2 million across 8,567 loans") and has no split by center.

3. **File that exists only to help the analyst?** `data_dictionary.txt` ("Files pulled on 3 December 2026 for the 2027 home equity payoff forecast."), plus `export_manifest.csv`. Both are ordinary documentation and describe fields only. Neither hints at a method.

4. **Figure or name that reads as the answer?** None.

5. **Filed sentence that fixes the population or the computation?** `lending_policy_7-4_he_payoff_forecast.pdf` 7.4.3: "Population: the fixed-rate closed-end home equity loans on the books at the close of business on 30 November 2026." Read literally, it gives 8,813 ACTIVE loans in the 30 Nov 2026 trial balance, USD 436.9M of principal (Grand Rapids 3,108 / 178.6M, Muskegon and the North 2,095 / 132.5M, The Lakeshore 2,396 / 82.1M, Kalamazoo and Battle Creek 1,214 / 43.7M). The outcome sentence ("principal paid ahead of schedule, which is the principal retired when a loan is paid in full before its maturity date and any principal paid in a month above that month's scheduled principal") fixes what is counted. It does not fix how payoffs are forecast.

6. **What decides the main answer?** An analytical choice: what drives payoff, and therefore what the payoff model is built on. No rule or field reading decides it. The data that settle it are the senior-lien tradeline fields in `he_lending_file_2009-2026.csv` together with the 30-year rate path in `planning_cycle_2027_rates.xlsx`. The two easy routes give different answers. Ranking by book size, or modelling on the HE note rate against the posted HE rate, puts Grand Rapids first. Modelling on the first-mortgage rate alone puts The Lakeshore first. Modelling on the cash-out-refinance incentive (the balance-weighted rate of the first mortgage plus the HE loan, against the 30-year rate) puts Muskegon and the North first. That last model fits best in sample and out of sample.

#### Mechanical scan

- `first_mortgage_servicing_2026-11.csv` (3,707 dates after 2026-12-03): harmless. These are `maturity_date` values of active mortgages, which are naturally in the future.
- `heloc_lines_2026-11.csv` (1,800 dates): harmless. These are `draw_period_end` dates of open lines. The file is also a distractor.
- `payoff_statement_log_2025-10_2026-11.csv` (48 dates): harmless. These are `good_through_date` values on statements issued in late November 2026. Every `issued_utc` is on or before 30 Nov 2026.
- `planning_cycle_2027_rates.xlsx` (36 dates): harmless. These are the plan's month labels (Jan to Dec 2027 on each of the three scenario sheets). They are the forecast inputs the policy requires.

#### How I reached the main answer

**What I modelled.** I built a loan-month panel from 2019-01 to 2026-11. It joins the legacy master (closes coded PIF) to the new core trial balance through the conversion cross-reference. I tagged each loan with its center using the lending file's county. I then fitted a monthly logistic payoff hazard.

**What drives each loan's payoff in the model.** The cash-out refinance incentive. For each month I computed the balance-weighted blended rate of the member's first mortgage and the HE loan, and subtracted the posted 30-year rate lagged one month. The first-mortgage rate is exact for purchase-money loans. For the others I solved it from the tradeline's original amount, opening month, balance and as-of month by amortisation; where the term was blank I chose 180 or 360 by the payment that fits. These solved rates match the servicing file's note rates for in-house firsts on 99.9 per cent of loans. Where the first is already paid off, the blended rate is the HE rate alone.

**The projection.** I projected December 2026 to December 2027 with the base-case 30-year path and survival-weighted amortising balances. I added curtailments at the core's observed rate (about 1.95 per cent a year of balance). Scheduled principal and payoffs in December 2026 are excluded from the 2027 figure.

**Result.** Muskegon and the North USD 36.4M, The Lakeshore 24.4M, Grand Rapids 16.5M, Kalamazoo and Battle Creek 13.4M.

**Alternatives I considered.**
- The HE-rate incentive alone. Its shape in the history is weak once the first-mortgage incentive is controlled for, and it ranks Grand Rapids first at about 60M.
- The first-mortgage rate alone, with or without a purchase-loan flag. This ranks The Lakeshore first at about 25M. It leaves a systematic gap between purchase and non-purchase loans, which the blended rate removes. The binned log-likelihood improved by about 335.
- Fitted on 2019 to 2022 and tested on 2023 to 2026, the blended model also predicts better. Even so, it still under-predicts Muskegon, so 36.4M is if anything low.
- Variants (lag 0 or 1, spline or binned curve) give Muskegon 37.0 to 38.4M and The Lakeshore 24.1 to 25.2M. A lag of 2 months gives 33.5M but fits worse.

**What looked odd in the files.**
- Kalamazoo and Battle Creek has run about 2 per cent a month in payoffs since 2024, because its 2023 purchase firsts are in the money.
- Some tradeline payments include escrow, and some senior-lien terms are blank.
- Twenty tradelines show a zero first-mortgage balance.
- St. Joseph County is on the map from 2019 but has no loans.
- The log mixes legacy and new loan numbers, HELOC line numbers and mortgage numbers.
- There is a hand-kept sheet covering the 9 to 20 March 2026 outage. All 53 HE rows matched a loan by street and ZIP.
- The ALM report's 8,567 loans is a different count from the trial balance's 8,662 at 30 Sep 2026.

**Ask counts.** These are distinct loans per quarter (Detroit local time). They exclude VOID requests, HELOC lines and mortgages, and add the manual-sheet HE quotes. "Paid in full" means core status PIF closed by 30 Nov 2026.

`reader.json`:

```json
{
 "call.center": "Muskegon and the North",
 "call.principal_2027_musd": 40,
 "call.second": "The Lakeshore",
 "steps.forecast_musd.Grand Rapids": 16.5,
 "steps.forecast_musd.The Lakeshore": 24.4,
 "steps.forecast_musd.Kalamazoo and Battle Creek": 13.4,
 "steps.forecast_musd.Muskegon and the North": 36.4,
 "asks.Grand Rapids|2025Q4.quoted": 43,
 "asks.Grand Rapids|2025Q4.paid_in_full": 36,
 "asks.Grand Rapids|2026Q1.quoted": 57,
 "asks.Grand Rapids|2026Q1.paid_in_full": 47,
 "asks.Grand Rapids|2026Q2.quoted": 46,
 "asks.Grand Rapids|2026Q2.paid_in_full": 41,
 "asks.Grand Rapids|2026Q3.quoted": 60,
 "asks.Grand Rapids|2026Q3.paid_in_full": 45,
 "asks.Kalamazoo and Battle Creek|2025Q4.quoted": 118,
 "asks.Kalamazoo and Battle Creek|2025Q4.paid_in_full": 117,
 "asks.Kalamazoo and Battle Creek|2026Q1.quoted": 95,
 "asks.Kalamazoo and Battle Creek|2026Q1.paid_in_full": 90,
 "asks.Kalamazoo and Battle Creek|2026Q2.quoted": 79,
 "asks.Kalamazoo and Battle Creek|2026Q2.paid_in_full": 71,
 "asks.Kalamazoo and Battle Creek|2026Q3.quoted": 88,
 "asks.Kalamazoo and Battle Creek|2026Q3.paid_in_full": 84,
 "asks.Muskegon and the North|2025Q4.quoted": 44,
 "asks.Muskegon and the North|2025Q4.paid_in_full": 37,
 "asks.Muskegon and the North|2026Q1.quoted": 38,
 "asks.Muskegon and the North|2026Q1.paid_in_full": 30,
 "asks.Muskegon and the North|2026Q2.quoted": 37,
 "asks.Muskegon and the North|2026Q2.paid_in_full": 29,
 "asks.Muskegon and the North|2026Q3.quoted": 50,
 "asks.Muskegon and the North|2026Q3.paid_in_full": 36,
 "asks.The Lakeshore|2025Q4.quoted": 65,
 "asks.The Lakeshore|2025Q4.paid_in_full": 60,
 "asks.The Lakeshore|2026Q1.quoted": 64,
 "asks.The Lakeshore|2026Q1.paid_in_full": 55,
 "asks.The Lakeshore|2026Q2.quoted": 43,
 "asks.The Lakeshore|2026Q2.paid_in_full": 37,
 "asks.The Lakeshore|2026Q3.quoted": 71,
 "asks.The Lakeshore|2026Q3.paid_in_full": 60
}
```
