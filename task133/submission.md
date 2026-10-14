# task133: Bellbird personal loans, the 30 September 2026 ECL allowance

## Tags

**Domain:** Banking, Credit & Financial Risk (expected credit loss provisioning: unsecured personal loans).
**Analytical objective:** Forecasting & Predictive Modeling (12-month and lifetime expected credit losses on the performing book).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Book a collective expected credit loss allowance of AUD 13.2 million on the PL36 and PL60 personal loans at 30 September 2026.**

Stage 1 carries AUD 10.6 million and stage 2 AUD 2.6 million. Not default and repayment rates that count every loan in the loan record from its drawdown, which puts the loans taken over at the October 2019 go-live among those at risk in months the record never saw, when the earlier platform's loans that defaulted or were repaid in those months never came across. Not a default rate with repayment treated as censoring, which lets a loan repaid in full go on defaulting. Not rates by risk grade, which CRM-ECL-04 7.1 rules out.

## 2. Critical Components

1. Loans in stage 2 at 30 September 2026: **3,266**
2. Probability-weighted PD multiplier from the approved scenarios: **1.06**
3. Stage 1 allowance **AUD 10.6 million**; stage 2 allowance **AUD 2.6 million**

## 3. Step-by-Step Solution

1. Staged `personal_loan_book_2026-09-30.csv` under CRM-ECL-04 sections 1 and 2 (90 or more days past due to stage 3; 30 or more days past due, a hardship arrangement in force on 30 September in `hardship_register_2026-09-30.xlsx`, or a 60-point fall in the v4 score after converting v3 origination scores with `scorecard_v4_migration_note.pdf`, to stage 2): 3,266 loans in stage 2.
2. Took each loan's month on book at 30 September in calendar months from its drawdown month, and its remaining term from the repayments fallen due by then, pause dates included and one month for a loan past maturity (CRM-ECL-04 3.2).
3. From `loan_record_2026-09-30.parquet`, for each product and month on book, took the loans open and not in default at its start and the shares of them that first defaulted in it and that closed without a default, counting a loan taken over at the 1 October 2019 go-live only from its first month on book after September 2019, because the record holds none of the earlier platform's loans that defaulted or closed before then.
4. Took PD(k) for a loan at month on book a as the default share at a + k times the shares neither defaulting nor closing in each month from a + 1 to a + k - 1, with the 2.4 scalar on stage 2 (3.2).
5. Applied the 70 and 76 per cent LGDs, the re-amortised balance and the contract-rate discount over 12 months or the remaining term if shorter in stage 1 and the remaining term in stage 2 (3.1, 3.3 to 3.5).
6. Weighted the scenarios on the Q1 FY27 sheet of `ifrs9_scenarios_2026Q3.xlsx` into one PD multiplier: 1.06.
7. Summed by stage: AUD 10.6 million in stage 1 and AUD 2.6 million in stage 2.
8. Recommendation: book AUD 13.2 million.

## 4. Deliverable Answers

### ecl_allowance_2026Q3.xlsx

1. Collective ECL allowance at 30 September 2026: AUD 13.2 million
2. Stage 1 allowance: AUD 10.6 million
3. Stage 2 allowance: AUD 2.6 million
4. What the 2023-24 defaults have lost as a share of their balance at default, by product and quarter of default, per cent to one decimal:
   - PL36, July to September 2023: 67.9
   - PL36, October to December 2023: 65.8
   - PL36, January to March 2024: 70.7
   - PL36, April to June 2024: 70.9
   - PL60, July to September 2023: 70.2
   - PL60, October to December 2023: 77.4
   - PL60, January to March 2024: 73.2
   - PL60, April to June 2024: 79.3

### arc_ecl_q3_2026.pptx

1. Slide 1 states the AUD 13.2 million allowance with stage 1 at AUD 10.6 million and stage 2 at AUD 2.6 million.
2. Slide 2 charts where each product's stage 1 and stage 2 loans at 30 June 2026 stand at 30 September 2026, stacked bars with every segment labelled:
   - PL36, stage 1 at 30 June: 14,470 in stage 1, 680 in stage 2, 42 in stage 3, 1,586 closed
   - PL36, stage 2 at 30 June: 468 in stage 1, 658 in stage 2, 115 in stage 3, 123 closed
   - PL60, stage 1 at 30 June: 17,724 in stage 1, 831 in stage 2, 46 in stage 3, 1,180 closed
   - PL60, stage 2 at 30 June: 560 in stage 1, 942 in stage 2, 140 in stage 3, 112 closed
