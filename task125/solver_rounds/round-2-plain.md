# solver round: round 2, plain

**Proxy score 85.1 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 43.1 of 58). Main call LANDED. 4 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: Order 6,700 routed payments from Fernhollow for April 2027 to March 2028.

solver: Order 6,700 routed payments for 2027/28 (6,706 forecast from the cells flagged on the 2025/26 screen: ASC 14, HS 14, HT 49, HT 99, PF 12). That is 1,400 below the 8,100 Fernhollow would size on from the 2025/26 run log (8,102). Adult Social Care carries the largest share at 3,700 (3,694).

tokens matched 3 of 5 (6,700, Order, Fernhollow, April, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| examination_calloff_2027-28.docx | 1 | 2 | 4 | 50% |
| examination_calloff_2027-28.docx | 2 | 3 | 3 | 100% |
| examination_calloff_2027-28.docx | 3 | 3 | 3 | 100% |
| examination_calloff_2027-28.docx | 4 | 1 | 1 | 100% |
| examination_calloff_2027-28.docx | 5 | 9 | 11 | 82% |
| examination_calloff_2027-28.xlsx | 1 | 13 | 24 | 54% |
| examination_calloff_2027-28.xlsx | 2 | 26 | 37 | 70% |
| examination_calloff_2027-28.xlsx | 3 | 5 | 13 | 38% |

## Solver's path

1. Rebuilt the published 2025/26 digit-conformity statement from wealdmoor_spend_over_500. I used gross amounts (net plus VAT), 1,000 <= amount < 1,000,000 (complete decades only), the fiscal year by payment_date, and the first-two-digit cell. Payments tested and MAD matched for all 10 departments and the council total in 2023/24, 2024/25 and 2025/26. The 2023/24 flagged cells match the cells in the run log (ASC14, HS14, HT49, HT99, WE11, PF12), which confirms the method.
2. Applied the flag rule (count > 1.5 x expected and count - expected >= 30) to 2025/26. Flagged cells for the plan year: ASC 14, HS 14, HT 49, HT 99, PF 12. WE 11 drops out.
3. Cell populations, each stable 2023-2027 per vendor: ASC14 is Direct Payments at 115 a month plus Shared Lives carers at 1,464 (102 a run); HS14 is floating-support block contracts at 14 a month plus Tenancy Sustainment; HT49 is parish contracts at 66 a month; HT99 is traffic signals at 36 a month; PF12 is cleaning at 81 a month.
4. Shared Lives after the Home First step-down closes (31 Mar 2027): I split each carer's constant four-weekly amount using the rate card. Carers whose remaining long-term amount lands in cell 14 are 1,464 (102), L2+S1 3,044 (22), L2+S2 3,272 (20), L2+S3 3,524 (18), and 2,274/2,388/2,514, which leave 1,484 (16). That gives 178 per run. The BACS calendar has 13 carer runs submitted in 2027/28, two of them in December (05/01/2028 is submitted 31/12/2027), so 2,314.
5. Tenancy Sustainment: the case extract shows 30-month awards, 18 a month approved Jul 2024 to Jun 2025, and no new round. Payments in 2027/28 are 144, 126, 108, 90, 72, 54, 36, 18 from Apr to Nov, then 0, for 648. HS = 648 + 168 = 816.
6. Run month is the BACS submission month (run book). Plan-year total: 3,694 + 816 + 1,224 + 972 = 6,706, which rounds to 6,700. December is the peak at 668.
7. Clause 4.2 sizing figure from the 2025/26 run log: routed counts with the scheduled October run DF-2510-01 replaced by re-run DF-2510-02 and supplementary run DF-2601-S1 (11) added = 8,102. This ties batch by batch to payments received in the acknowledgements JSON.
8. Examined: payments_examined on the non-withdrawn batches = 8,012. Charged per clause 5.2 (minimum 25 a batch, so the S1-WE batch is charged 25) = 8,026, which reconciles to net invoice quantities after credit note FC040126 and replacement FA040127, and to the Q2 service report (1,994). Quarterly allocations: 1,900 for Q1 and Q2, 2,200 for Q3 and Q4 (Variation 1). Premium examinations are charged above allocation; unused volume is charged at 40% of the GBP 18.40 base rate.

confidence: Medium-high. The screen reproduces every published figure and the 2025/26 money reconciles. The main residual risk is how the 2,274/2,388/2,514 Shared Lives amounts split. Splitting them as 2 weeks of each rate leaves 1,484, which is cell 14. If they were excluded instead, the total would be 6,498, which rounds to 6,500.

notes: The forecast assumes the cell-14 populations keep their stable per-vendor amounts and no new Tenancy Sustainment round. Premium-rate examinations are given as counts, with GBP values for reference. The rate card in force when the March 2026 batches arrived (31/03/2026) was the 2025/26 card.

### examination_calloff_2027-28.docx (solver's answers)
- Order quantity 2027/28 (routed payments, nearest hundred): 6,700 routed payments (unrounded forecast 6,706)
- Department with largest share and its count: Adult Social Care, 3,700 (3,694: Direct Payments 1,380 plus Shared Lives carers 2,314, which is 13 runs x 178); others: Highways & Transport 1,224, Property & Facilities 972, Housing Support 816, Waste & Environment 0
- Fernhollow's sizing figure from the latest closed year: 8,100 routed payments (2025/26 run log 8,102, counting the October re-run in place of the withdrawn scheduled run and adding the January supplementary run)
- How far the order sits from Fernhollow's figure: 1,400 below (6,706 vs 8,102 = -1,396; 6,700 vs 8,100 = -1,400)
- Chart elements: Monthly average of the closed-year figure is 675 (8,102/12 = 675.2). The plan year is Apr 2027 to Mar 2028. The busiest plan-year month is December 2027 at 668 (two Shared Lives carer runs submitted in the month). The order of 6,700 goes in the title.

### examination_calloff_2027-28.xlsx (solver's answers)
- Sheet 1: plan-year routed payments by run month: Apr-27 634; May-27 616; Jun-27 598; Jul-27 580; Aug-27 562; Sep-27 544; Oct-27 526; Nov-27 508; Dec-27 668; Jan-28 490; Feb-28 490; Mar-28 490; total 6,706. By department: ASC 293 each month (Dec 471); HS 158, 140, 122, 104, 86, 68, 50, 32 from Apr to Nov, then 14 from Dec to Mar; HT 102 every month; PF 81 every month
- Sheet 2: 2025/26 routed by month: Apr 634; May 652; Jun 664; Jul 668; Aug 673; Sep 676; Oct 681; Nov 663; Dec 663; Jan 685; Feb 669; Mar 774; total 8,102
- Sheet 2: 2025/26 examined by Fernhollow by month: Apr 628; May 643; Jun 656; Jul 658; Aug 667; Sep 669; Oct 675; Nov 656; Dec 658; Jan 680; Feb 661; Mar 761; total 8,012
- Sheet 3: premium-rate examinations by quarter 2025/26: Q1 27 (1,927 charged against an allocation of 1,900); Q2 94 (1,994 vs 1,900); Q3 0 (1,989 vs 2,200); Q4 0 (2,116 vs 2,200); total 121. In money that is GBP 745 for Q1 and GBP 2,594 for Q2 at GBP 27.60
- Sheet 3: unused-volume charge by quarter 2025/26: Q1 GBP 0; Q2 GBP 0; Q3 GBP 1,553 (211 unused x 40% x GBP 18.40); Q4 GBP 618 (84 x 40% x 18.40); total GBP 2,171
