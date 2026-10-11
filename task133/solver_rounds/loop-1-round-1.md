# solver round: loop 1 round 1

**Proxy score 35.3 / 100** (recommendation 2.5 of 35, instruction 7.0 of 7, asks 25.8 of 58). Main call missed. 1 of 6 ask items cracked (80 per cent of tokens).

## Main call

golden: Book a collective expected credit loss allowance of AUD 13,160,000 on the PL36 and PL60 personal loans at 30 September 2026.

solver: The board should sign off on 23 October a collective (stage 1 and 2) ECL allowance on Bellbird's PL36 and PL60 personal loans at 30 September 2026 of A$11,421 thousand (stage 1 A$9,240k, stage 2 A$2,181k; PL36 A$3,441k, PL60 A$7,980k; 2.24% coverage of A$509,243k gross carrying amount), built under CRM-ECL-04 v4.2 with the ARC-approved Q1 FY27 scenarios (Base 0.55 x1.0, Downside 0.30 x1.3, Upside 0.15 x0.8; weighted multiplier 1.06), the PLPD-2026.06 curves, the 2.4 stage 2 scalar and LGDs of 70% (PL36) and 76% (PL60).

tokens matched 2 of 4 (13,160,000, 30, Book, September)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| ecl_allowance_2026Q3.xlsx | 1 | 0 | 4 | 0% |
| ecl_allowance_2026Q3.xlsx | 2 | 1 | 2 | 50% |
| ecl_allowance_2026Q3.xlsx | 3 | 1 | 2 | 50% |
| ecl_allowance_2026Q3.xlsx | 4 | 9 | 18 | 50% |
| board_ecl_q3_2026.pptx | 1 | 1 | 4 | 25% |
| board_ecl_q3_2026.pptx | 2 | 23 | 25 | 92% |

## Solver's path

1. Read CRM-ECL-04 v4.2, ecl_extract_dictionary.txt, scorecard_v4_migration_note.pdf (v4 = round(1.12 x v3 - 18)) and ifrs9_scenarios_2026Q3.xlsx (current sheet Q1 FY27, weighted multiplier 0.55x1 + 0.30x1.3 + 0.15x0.8 = 1.06; the prior sheet's 1.04 was not used)
2. Checked the curve file: rebuilt the PLPD-2026.06 cumulative curves from pd_model_development_sample.parquet and they match to 5e-7
3. Staged personal_loan_book_2026-09-30.csv (40,897 loans): stage 3 if 90+ days past due (343 loans); stage 2 if 30+ days past due, a hardship arrangement in force by date (start <= 30 Sep <= end and not cancelled on or before 30 Sep: 612 loans, excluding 2 still marked Active that ended 29 Sep), or v4 origination score minus current_score_v4 >= 60; giving stage 1 37,288 and stage 2 3,266
4. Remaining term = term minus repayments fallen due by 30 Sep, counted from first_repayment_date (days 1-28, so the business-day rule moves nothing past either reporting date), floored at 1 for 28 loans at or past maturity; PD(k) = C(m+k) - C(m+k-1) from the product curve, x2.4 for stage 2, x1.06 for the scenarios; EAD from an annuity at contract_rate/12; DF = (1 + r/12)^-k; horizon min(12, n) for stage 1 and n for stage 2; LGD 0.70 or 0.76; summed by loan: AUD 11,421,240
5. Transitions: staged personal_loan_book_2026-06-30.csv the same way at 30 Jun, using the behaviour score run dated 2026-07-01 (the June month-end position; loans not yet at first repayment use their v4 application score) and the hardship register's dates; joined to the September stages on loan_no, with loans missing from the September book counted as closed: 39,677 June stage 1 and 2 loans, of which 3,001 closed
6. LGD back-test: collections_defaults_2023-24.csv (1,148 loans) joined to collections_receipts (dishonours netted; the lump debt-sale receipt replaced by 3.85% x face value per loan from debt_sale_2026-03_schedule.xlsx, received 27 Mar 2026, 591 of these loans sold); each receipt discounted at contract_rate/12 for the whole months from the default month end to the end of its receipt month; Cured loans' loss set to 0; balance-weighted loss / balance at default by product and default quarter

confidence: Medium-high: the staging inputs, the scenario set and the LGD back-test follow the files directly; the main judgement is reading PD(k) as the plain difference in the cumulative curve (the conditional reading gives AUD 11,737k).

notes: CRM-ECL-04 does not say whether the monthly PD should be conditional on the loan not having defaulted by the reporting date, so I used the plain difference in the cumulative curve. The back-test quarters are taken as July 2023 to June 2024 (financial year 2023-24) and are balance-weighted rather than a simple average of loan loss rates.

### board_ecl_q3_2026.pptx (solver's answers)
- Slide 1: collective ECL allowance at 30 Sep 2026: Allowance AUD 11,421 thousand (stage 1 AUD 9,240k; stage 2 AUD 2,181k; PL36 AUD 3,441k; PL60 AUD 7,980k; coverage 2.24% of AUD 509,243k gross carrying amount)
- Slide 2: PL36 stage 1 at 30 Jun, where at 30 Sep: 16,778 loans: stage 1 14,470; stage 2 680; stage 3 42; closed 1,586
- Slide 2: PL36 stage 2 at 30 Jun, where at 30 Sep: 1,364 loans: stage 1 468; stage 2 658; stage 3 115; closed 123
- Slide 2: PL60 stage 1 at 30 Jun, where at 30 Sep: 19,781 loans: stage 1 17,724; stage 2 831; stage 3 46; closed 1,180
- Slide 2: PL60 stage 2 at 30 Jun, where at 30 Sep: 1,754 loans: stage 1 560; stage 2 942; stage 3 140; closed 112

### ecl_allowance_2026Q3.xlsx (solver's answers)
- Total allowance: AUD 11,421 thousand (exact 11,421,239.98); coverage 2.24%
- Stage 1 allowance: AUD 9,240 thousand on 37,288 loans, GCA AUD 468,779k, coverage 1.97% (PL36 AUD 2,859k on 17,108 loans, GCA 138,343k, 2.07%; PL60 AUD 6,381k on 20,180 loans, GCA 330,436k, 1.93%)
- Stage 2 allowance: AUD 2,181 thousand on 3,266 loans, GCA AUD 40,465k, coverage 5.39% (PL36 AUD 582k on 1,422 loans, GCA 11,734k, 4.96%; PL60 AUD 1,599k on 1,844 loans, GCA 28,730k, 5.57%)
- By product: PL36 AUD 3,441k, GCA 150,077k, coverage 2.29%; PL60 AUD 7,980k, GCA 359,166k, coverage 2.22%
- Realised LGD, 2023-24 defaults, PL36 by default quarter: Jul-Sep 2023 67.9%; Oct-Dec 2023 65.8%; Jan-Mar 2024 70.7%; Apr-Jun 2024 70.9% (all-year 68.9%)
- Realised LGD, 2023-24 defaults, PL60 by default quarter: Jul-Sep 2023 70.4%; Oct-Dec 2023 77.3%; Jan-Mar 2024 73.5%; Apr-Jun 2024 79.3% (all-year 75.2%)
