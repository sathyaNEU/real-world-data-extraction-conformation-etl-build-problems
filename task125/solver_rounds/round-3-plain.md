# solver round: round 3, plain

**Proxy score 43.3 / 100** (recommendation 2.0 of 35, instruction 7.0 of 7, asks 34.3 of 58). Main call missed. 1 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: Order 6,900 routed payments from Fernhollow for April 2027 to March 2028.

solver: Order 6,700 routed payments for 2027/28, not the 8,100 Fernhollow would size on. The forecast is 6,706: Adult Social Care 3,694, Highways & Transport 1,224, Property & Facilities 972 and Housing Support 816. It applies the cells from the 2025/26 screen (ASC 14, HS 14, HT 49 and 99, PF 12; the Waste & Environment cell 11 drops out). It also allows for two changes: Home First step-down closes, which moves 76 more Shared Lives carer payments into cell 14 on each of 13 runs, and the 2024-25 Tenancy Sustainment awards finish, adding only 648 payments that end by November 2027.

tokens matched 2 of 5 (6,900, Order, Fernhollow, April, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| examination_calloff_2027-28.docx | 1 | 3 | 4 | 75% |
| examination_calloff_2027-28.docx | 2 | 2 | 3 | 67% |
| examination_calloff_2027-28.docx | 3 | 3 | 3 | 100% |
| examination_calloff_2027-28.docx | 4 | 0 | 1 | 0% |
| examination_calloff_2027-28.docx | 5 | 8 | 11 | 73% |
| examination_calloff_2027-28.xlsx | 1 | 12 | 24 | 50% |
| examination_calloff_2027-28.xlsx | 2 | 26 | 37 | 70% |
| examination_calloff_2027-28.xlsx | 3 | 5 | 13 | 38% |

## Solver's path

1. Rebuilt the payment digit screen from the spend file: gross amount (net + VAT), from 1,000 up to but not including 1,000,000 (complete decades), payment-date financial year, by department. This matches every published payments-tested count and MAD for 2023/24, 2024/25 and 2025/26 exactly. Net-only amounts or the 500+ floor do not match.
2. Flag rule (count > 1.5 x expected and at least 30 over): the 2023/24 screen gives ASC 14, HS 14, HT 49 and 99, PF 12, WE 11, the same cells as the 2025/26 run log. The 2025/26 screen (statement published 10/07/2026, the latest published by 12/03/2027) gives ASC 14, HS 14, HT 49 and 99, PF 12. WE 11 drops out.
3. Flagged-cell streams in the spend file: ASC 14 = Direct Payments 115/month plus Shared Lives carers paid 1,464 (102 per four-weekly run). HS 14 = Floating Support 14/month plus Tenancy Sustainment. HT = 66 + 36 per month. PF = 81 per month. Run month is the month of the BACS submission date (from the calendar), which explains the 2025/26 log's March ASC figure of 319.
4. Home First step-down closes on 31/03/2027. Split the Shared Lives carer amounts into weekly rates and removed the step-down parts. 3044, 3272 and 3524 drop to 1,464 (22+20+18). 2388, 2274 and 2514 drop to 1,484 (6+6+4). Both land in cell 14, so the run figure goes from 102 to 178. Other combined amounts fall to 13xx, 16xx, 29xx or below 1,000. There are 13 plan-year SL submissions, two of them in December 2027, giving 2,314.
5. Tenancy Sustainment case extract: every award is 30 monthly payments. The 2024-25 round has 18 awards a month approved Jul-2024 to Jun-2025, and no new round. Payments still due in the plan year: Nov-24 to Jun-25 cohorts give 144, 126, 108, 90, 72, 54, 36 and 18 for Apr to Nov 2027, then 0, for a total of 648.
6. Plan-year total: ASC 3,694 + HS 816 + HT 1,224 + PF 972 = 6,706, so the order is 6,700.
7. Fernhollow's indicative volume (clause 4.2, from the run log): left out the withdrawn DF-2510-01 run (replaced by the re-run) and included the supplementary WE 11, giving 8,102 (8,100). The gap is 1,396, so 1,400.
8. 2025/26 examinations from the batch acknowledgements (examined batches only, grouped by run month from the batch_ref). Charged = max(examined, 25) per batch, under clause 5.2. Allocation was 1,900 for Q1 and Q2 and 2,200 for Q3 and Q4 under Variation 1. Premium examinations: Q1 27, Q2 94. Unused volume at 40% of the 18.40 base rate: Q3 211 = GBP 1,553, Q4 84 = GBP 618. The Q2 service report (1,994 examined) and the invoice quantities agree with these figures.

confidence: Medium-high. The screen rebuild matches every published figure exactly, and the run log, batch acknowledgements and invoices all agree. The main judgement calls are splitting the Shared Lives carer amounts into weekly rates (the 2+2+2-week amounts are read as half-rate shares, which puts them at 1,484 in cell 14) and assuming that the streams with no evidence of change carry on as they are.

notes: The forecast assumes Direct Payments, the HT parish and signal contracts, PF cleaning and HS Floating Support carry on at their current monthly counts, because no document says they will change. If the 16 half-rate Shared Lives carers were left out of cell 14, the ASC count would fall by 208 to 3,486 and the order would come out at 6,500.

### examination_calloff_2027-28.docx (solver's answers)
- Order quantity, April 2027 to March 2028: 6,700 routed payments (forecast 6,706, nearest hundred)
- Department with the largest share and its count: Adult Social Care, 3,700 routed payments (3,694 = 1,380 Direct Payments + 2,314 Shared Lives carers; about 55% of the order)
- Figure Fernhollow would size on (latest closed year 2025/26): 8,100 routed payments (8,102 from the run log, with the withdrawn October 2025 scheduled run left out and the January supplementary run of 11 included; summing every row of the log gives 8,783, which is wrong)
- How far our order sits from Fernhollow's figure: 1,400 routed payments below (8,102 - 6,706 = 1,396)
- Chart: line at monthly average of Fernhollow figure: 675 routed payments per month (8,102 / 12 = 675.2)
- Chart: busiest plan-year month annotation: December 2027, 668 routed payments (two Shared Lives runs: submissions 06/12/2027 and 31/12/2027)
- Chart title order figure: 6,700

### examination_calloff_2027-28.xlsx (solver's answers)
- Sheet 1: plan-year routed payments by month: Apr-27 634; May-27 616; Jun-27 598; Jul-27 580; Aug-27 562; Sep-27 544; Oct-27 526; Nov-27 508; Dec-27 668; Jan-28 490; Feb-28 490; Mar-28 490; total 6,706. By department: ASC 3,694 (DP 115/month, Shared Lives 178 per run x 13 runs), HS 816 (Floating Support 14/month = 168; Tenancy Sustainment 144,126,108,90,72,54,36,18 Apr-Nov then 0 = 648), HT 1,224 (102/month), PF 972 (81/month)
- Sheet 2: 2025/26 monthly payments routed: Apr-25 634; May 652; Jun 664; Jul 668; Aug 673; Sep 676; Oct 681; Nov 663; Dec 663; Jan-26 685; Feb 669; Mar 774; total 8,102
- Sheet 2: 2025/26 monthly payments Fernhollow examined: Apr-25 628; May 643; Jun 656; Jul 658; Aug 667; Sep 669; Oct 675; Nov 656; Dec 658; Jan-26 680; Feb 661; Mar 761; total 8,012
- Sheet 3: examinations charged at premium rate by quarter 2025/26: Q1 27 (1,927 charged vs 1,900 allocation); Q2 94 (1,994 vs 1,900); Q3 0 (1,989 vs 2,200); Q4 0 (2,116 vs 2,200, including the 25-examination minimum on the 11-payment supplementary batch); year 121
- Sheet 3: unused-volume charge by quarter 2025/26: Q1 GBP 0; Q2 GBP 0; Q3 GBP 1,553 (211 x 40% x 18.40); Q4 GBP 618 (84 x 40% x 18.40); year GBP 2,171
