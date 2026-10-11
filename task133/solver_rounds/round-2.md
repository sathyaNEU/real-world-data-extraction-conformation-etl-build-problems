# solver round: round 2

**Proxy score 36.1 / 100** (recommendation 2.5 of 35, instruction 7.0 of 7, asks 26.6 of 58). Main call missed. 1 of 6 ask items cracked (80 per cent of tokens).

## Main call

golden: Book a collective expected credit loss allowance of AUD 13,773,000 on the PL36 and PL60 personal loans at 30 September 2026.

solver: Report a collective ECL allowance of A$13,318,000 at 30 September 2026 on Bellbird's PL36 and PL60 personal loans (stages 1 and 2, 40,554 loans, gross carrying amount A$509,248,000, coverage 2.62%), built under CRM-ECL-04 v4.1 with the PLPD-2026.06 curve, LGD 70% PL36 / 76% PL60, stage-2 PD scalar 2.4, and the Q3 scenarios approved 18 September 2026 (Base 0.55x1.0, Downside 0.30x1.3, Upside 0.15x0.8 = weighted multiplier 1.06), with 343 stage 3 loans excluded.

tokens matched 2 of 4 (13,773,000, 30, Book, September)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| ecl_allowance_2026Q3.xlsx | 1 | 0 | 4 | 0% |
| ecl_allowance_2026Q3.xlsx | 2 | 9 | 17 | 53% |
| ecl_allowance_2026Q3.xlsx | 3 | 2 | 9 | 22% |
| ecl_allowance_2026Q3.xlsx | 4 | 3 | 3 | 100% |
| arc_ecl_q3_2026.pptx | 1 | 1 | 2 | 50% |
| arc_ecl_q3_2026.pptx | 2 | 1 | 2 | 50% |

## Solver's path

1. personal_loan_book_2026-09-30.csv: 40,897 open loans at COB 30 Sep 2026, no duplicates, max DPD 176, latest drawdown 30 Sep 2026
2. Stage 3 = DPD >= 90 (CRM-ECL-04 1.1-1.2): 343 loans excluded (157 PL36, 186 PL60; gross A$5,464,020)
3. hardship_register_2026-09-30.xlsx joined on loan_no; in force = start <= 30 Sep <= end and not Cancelled (all cancelled_date <= 30 Sep): 612 Active arrangements on 612 book loans
4. Score condition: v3 origination converted round(1.12*v3 - 18) (scorecard_v4_migration_note.pdf); drop >= 60 points on v4 flags 2,930 (2,006 without conversion)
5. Stage 2 = DPD 30-89 OR hardship in force OR score drop: 3,265 loans; Stage 1: 37,289
6. Months on book = repayment dates (same day each month from first_repayment_date) on or before 30 Sep 2026; remaining term = term minus that; 28 non-stage-3 past-maturity loans set to remaining 1 month
7. Per loan ECL = sum PD(k)*LGD*EAD(k)*DF(k); PD(k) = C(m+k)-C(m+k-1) from pd_curve_personal_loans_2026-06.csv (x2.4 for stage 2); LGD 0.70 PL36 / 0.76 PL60; EAD level-instalment amortisation of current_balance at contract rate over remaining term; DF=(1+r/12)^-k; horizon min(12, rem) stage 1, full rem stage 2: base ECL A$12,564,378
8. ifrs9_scenarios_2026Q3.xlsx Q1 FY27 sheet: weighted multiplier 0.55*1.0+0.30*1.3+0.15*0.8=1.06; allowance A$13,318,240.78 -> A$13,318,000
9. Grouped by stage and product and by product and drawdown year (2023 and earlier pooled) for the lines and coverage ratios

confidence: Moderate-high on staging, remaining term and scenario weighting; moderate on the PD(k) convention (plain difference of the cumulative curve, not conditioned on survival).

notes: CRM-ECL-04 does not state whether PD(k) is conditioned on the loan not having defaulted by month m; dividing by (1 - C(m)) would give about A$13,773,000 instead of A$13,318,000. The development sample does not reproduce the approved curve from a simple count, so the approved curve was used as given.

### ecl_allowance_2026Q3.xlsx (solver's answers)
- Total collective allowance: Allowance A$13,318,000 (nearest thousand)
- Stage 1 PL36 line: Loans 17,109; gross carrying amount A$138,349,000; allowance A$3,129,000; coverage 2.26%
- Stage 1 PL60 line: Loans 20,180; gross carrying amount A$330,436,000; allowance A$7,466,000; coverage 2.26%
- Stage 2 PL36 line: Loans 1,421; gross carrying amount A$11,728,000; allowance A$660,000; coverage 5.63%
- Stage 2 PL60 line: Loans 1,844; gross carrying amount A$28,735,000; allowance A$2,063,000; coverage 7.18%
- PL36 allowance by drawdown year: 2023 and earlier A$5,000; 2024 A$146,000; 2025 A$886,000; 2026 A$2,753,000 (nearest thousand)
- PL60 allowance by drawdown year: 2023 and earlier A$573,000; 2024 A$981,000; 2025 A$2,269,000; 2026 A$5,706,000 (nearest thousand)
- Loans left out as stage 3: 343 loans (157 PL36, 186 PL60)

### arc_ecl_q3_2026.pptx (solver's answers)
- Slide 1 allowance and stage/product table: Allowance A$13,318,000. S1 PL36: 17,109 loans, A$138,349,000 gross, A$3,129,000 allowance, 2.26%. S1 PL60: 20,180 loans, A$330,436,000, A$7,466,000, 2.26%. S2 PL36: 1,421 loans, A$11,728,000, A$660,000, 5.63%. S2 PL60: 1,844 loans, A$28,735,000, A$2,063,000, 7.18%. Total 40,554 loans, A$509,248,000 gross, 2.62% coverage.
- Slide 2 allowance by drawdown year per product (chart): PL36: 2023 and earlier A$5,000; 2024 A$146,000; 2025 A$886,000; 2026 A$2,753,000. PL60: 2023 and earlier A$573,000; 2024 A$981,000; 2025 A$2,269,000; 2026 A$5,706,000.
