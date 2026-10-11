# task133: Bellbird personal loans, the 30 September 2026 ECL allowance

## Tags

**Domain:** Banking, Credit & Financial Risk (expected credit loss provisioning: unsecured personal loans).
**Analytical objective:** Forecasting & Predictive Modeling (12-month and lifetime expected credit losses on the performing book).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Book a collective expected credit loss allowance of AUD 13,773,000 on the PL36 and PL60 personal loans at 30 September 2026.**

Stage 1 carries AUD 10,933,000 and stage 2 AUD 2,840,000, with 343 loans in stage 3 left to CRM-ECL-06. Not the cumulative default curve read from origination for every loan, which charges seasoned loans for defaults in months they have already come through. Not the curve shifted to each loan's months on book without dividing by its survival to date, which understates the probability for a loan that is still performing.

## 2. Critical Components

1. Loans in stage 2 at 30 September 2026: **3,265**
2. Probability-weighted PD multiplier from the approved scenarios: **1.06**
3. Stage 1 allowance **AUD 10,933,000**; stage 2 allowance **AUD 2,840,000**

## 3. Step-by-Step Solution

1. Set aside the loans 90 or more days past due in `personal_loan_book_2026-09-30.csv` as stage 3 (CRM-ECL-04 section 1): 343 loans.
2. Staged the rest under CRM-ECL-04 section 2: 30 or more days past due, a hardship arrangement in force on 30 September in `hardship_register_2026-09-30.xlsx`, or a 60-point score fall after converting v3 origination scores with `scorecard_v4_migration_note.pdf`: 3,265 loans in stage 2.
3. Counted each loan's monthly repayments fallen due by 30 September and its remaining term, one month for a loan past maturity (CRM-ECL-04 3.2).
4. Took PD(k) from `pd_curve_personal_loans_2026-06.csv` as the curve's increment after the loan's months on book divided by its survival to date, because the curve runs from origination and a performing loan has already come through those months, with the 2.4 stage 2 scalar.
5. Applied LGD, the re-amortised balance and the contract-rate discount over 12 months or the remaining term if shorter for stage 1 and the remaining term for stage 2 (CRM-ECL-04 3.3 to 3.5).
6. Weighted the scenarios in the Q1 FY27 sheet of `ifrs9_scenarios_2026Q3.xlsx` into one PD multiplier: 1.06.
7. Summed by stage: AUD 10,933,000 in stage 1 and AUD 2,840,000 in stage 2.
8. Recommendation: book AUD 13,773,000.

## 4. Deliverable Answers

### ecl_allowance_2026Q3.xlsx

1. Collective ECL allowance at 30 September 2026: AUD 13,773,000
2. By stage and product, loans, gross carrying amount and allowance to the nearest thousand dollars, coverage to two decimals:
   - Stage 1, PL36: 17,109 loans; AUD 138,349,000; allowance AUD 3,202,000; coverage 2.31%
   - Stage 1, PL60: 20,180 loans; AUD 330,436,000; allowance AUD 7,731,000; coverage 2.34%
   - Stage 2, PL36: 1,421 loans; AUD 11,728,000; allowance AUD 681,000; coverage 5.81%
   - Stage 2, PL60: 1,844 loans; AUD 28,735,000; allowance AUD 2,159,000; coverage 7.51%
3. Allowance by drawdown year and product, to the nearest thousand dollars:
   - 2023 and earlier: PL36 AUD 5,000; PL60 AUD 641,000
   - 2024: PL36 AUD 159,000; PL60 AUD 1,073,000
   - 2025: PL36 AUD 940,000; PL60 AUD 2,412,000
   - 2026: PL36 AUD 2,779,000; PL60 AUD 5,763,000
4. Loans left out of the collective model as stage 3: 343

### board_ecl_q3_2026.pptx

1. Slide 1 states the AUD 13,773,000 allowance with the stage and product table:
   - Stage 1, PL36: 17,109 loans; AUD 138,349,000; allowance AUD 3,202,000; coverage 2.31%
   - Stage 1, PL60: 20,180 loans; AUD 330,436,000; allowance AUD 7,731,000; coverage 2.34%
   - Stage 2, PL36: 1,421 loans; AUD 11,728,000; allowance AUD 681,000; coverage 5.81%
   - Stage 2, PL60: 1,844 loans; AUD 28,735,000; allowance AUD 2,159,000; coverage 7.51%
2. Slide 2 charts the allowance by drawdown year for each product:
   - PL36: 2023 and earlier AUD 5,000; 2024 AUD 159,000; 2025 AUD 940,000; 2026 AUD 2,779,000
   - PL60: 2023 and earlier AUD 641,000; 2024 AUD 1,073,000; 2025 AUD 2,412,000; 2026 AUD 5,763,000
