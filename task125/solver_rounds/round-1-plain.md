# solver round: round 1, plain

**Proxy score 80.2 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 38.2 of 58). Main call LANDED. 3 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: Order 6,500 routed payments from Fernhollow for April 2027 to March 2028.

solver: Order 6,500 routed payments for April 2027 to March 2028. The working forecast is 6,522, built on the cells flagged by the 2025/26 screen: ASC 14, HS 14, HT 49 and 99, and PF 12. Waste & Environment cell 11 drops out. Adult Social Care carries the largest share at about 3,500 (3,486). The forecast allows for Home First step-down closing, which moves 60 Shared Lives payments per pay date into cell 14, so that cell goes from 102 to 162 per date. It also allows for the 2024-25 Tenancy Sustainment awards running off by November 2027. Fernhollow's indicative figure is 8,100 (8,126 routed in 2025/26 per the run log), so we sit about 1,600 below it.

tokens matched 5 of 5 (6,500, Order, Fernhollow, April, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| examination_calloff_2027-28.docx | 1 | 2 | 4 | 50% |
| examination_calloff_2027-28.docx | 2 | 3 | 3 | 100% |
| examination_calloff_2027-28.docx | 3 | 3 | 3 | 100% |
| examination_calloff_2027-28.docx | 4 | 1 | 1 | 100% |
| examination_calloff_2027-28.docx | 5 | 7 | 11 | 64% |
| examination_calloff_2027-28.xlsx | 1 | 3 | 24 | 12% |
| examination_calloff_2027-28.xlsx | 2 | 20 | 37 | 54% |
| examination_calloff_2027-28.xlsx | 3 | 6 | 13 | 46% |

## Solver's path

1. Rebuilt the 2025/26 screen from the spending file. It uses gross amounts (net + VAT), payments from £1,000 up to £999,999.99, and the first two digits of the gross amount. This reproduces every published payments-tested count and MAD for 2023/24 to 2025/26. Under the methodology the flagged cells are those more than 1.5 times their Benford expected count and at least 30 above it. For 2025/26 that gives ASC 14, HS 14, HT 49, HT 99 and PF 12.
2. Confirmed that 2025/26 is the right screen. It is the latest statement published (July 2026) before the order goes on 12 March 2027 (methodology section 5). The 2025/26 run log used the 2023/24 cells, which included WE 11; that cell no longer qualifies.
3. Assigned each payment to a run month by its BACS submission date, using the payment calendar and run book section 2. Plan-year Shared Lives submissions number 13, with two in December 2027 (one on 6/12 and one on 31/12 for the 5 January payment). Direct payments and Tenancy Sustainment each have 12.
4. ASC cell 14 is made up of 115 direct payments a month plus Shared Lives carer payments. On each carer pay date, 102 payments are £1,464, and 22 + 20 + 18 more are £1,464 plus a step-down rate (£3,044, £3,272, £3,524). When Home First step-down closes on 31 March 2027 those 60 drop to £1,464, so cell 14 has 162 payments per pay date. ASC total: 115 x 12 + 162 x 13 = 3,486.
5. Housing Support: the case extract shows 2024-25 round awards of 18 a month (approved July 2024 to June 2025), each running 30 months. Tenancy Sustainment payments in the plan year are 144, 126, 108, 90, 72, 54, 36 and 18 from April to November 2027, then zero, a total of 648. Adding floating-support block payments of 14 a month gives 816.
6. HT (66 + 36 = 102 a month) and PF (83 a month) are stable monthly creditor streams, giving 1,224 and 996. The plan-year total is 6,522, which rounds to 6,500. December 2027 is the peak month at 638.
7. Fernhollow's indicative figure under clause 4.2 is the 2025/26 run log total of 8,126. This leaves out the replaced Oct-25 scheduled run and adds supplementary run S1. It rounds to 8,100, giving a gap of 1,604 (about 1,600).
8. For 2025/26 examined and charged, matched the run log against the acknowledgement JSON (the 5 withdrawn batches carry no charge). Examined total is 8,039. The 25-examination minimum on the WCC-2601-S1-WE batch lifts charged volume by 14. Invoices net of the credit note and replacement invoice agree batch by batch. The quarters use allocations of 1,900, 1,900, 2,200 and 2,200 (Variation 1) and the unused-volume rate of 0.4 x £18.40 = £7.36.

confidence: high

notes: Wendy's 'nothing has moved' is contradicted by the step-down closure notice, and Pauline's 'nothing for your filter' is contradicted by the case extract. Both are treated as wrong. Shared Lives is paid four-weekly in arrears; the forecast assumes no step-down element remains in the first plan-year payment on 28 April 2027. The scratch scripts were run inline rather than saved, because this agent was in read-only mode.

### examination_calloff_2027-28.docx (solver's answers)
- Order: payments routed Apr 2027-Mar 2028: 6,500 routed payments (6,522 before rounding)
- Largest department and its count: Adult Social Care, 3,500 (3,486 = 1,380 direct payments + 2,106 Shared Lives carer payments). The others are Highways & Transport 1,224, Property & Facilities 996 and Housing Support 816.
- Fernhollow's figure from the latest closed year: 8,100 (2025/26 routed count in the run log: 8,126; the replaced run DF-2510-01 is left out and supplementary run S1 is included)
- Gap between our order and Fernhollow's figure: 1,600 below Fernhollow (8,126 - 6,522 = 1,604)
- Chart reference values: Monthly average of Fernhollow's figure: 677 (8,126 / 12). Busiest plan-year month: December 2027, 638. Chart title should show the order of 6,500.

### examination_calloff_2027-28.xlsx (solver's answers)
- Sheet 1: plan-year routed payments by month: Apr-27 620, May-27 602, Jun-27 584, Jul-27 566, Aug-27 548, Sep-27 530, Oct-27 512, Nov-27 494, Dec-27 638, Jan-28 476, Feb-28 476, Mar-28 476. Total 6,522. ASC is 277 a month, 439 in December. HS: 158, 140, 122, 104, 86, 68, 50, 32, then 14 a month. HT is 102 a month and PF is 83 a month.
- Sheet 2: 2025/26 routed and examined by month: Routed / examined: Apr-25 636/630, May-25 654/645, Jun-25 666/658, Jul-25 670/660, Aug-25 675/668, Sep-25 678/673, Oct-25 683/678, Nov-25 665/657, Dec-25 665/661, Jan-26 687/679, Feb-26 671/663, Mar-26 776/767. Total 8,126 routed and 8,039 examined.
- Sheet 3: 2025/26 quarterly premium examinations and unused-volume charge: Q1: 33 premium examinations (1,933 charged against an allocation of 1,900), unused charge £0. Q2: 101 premium (2,001 against 1,900), £0. Q3: 0 premium (1,996 against 2,200), unused charge £1,501 (204 x £7.36). Q4: 0 premium (2,124 charged, including the 25-examination minimum on batch S1, against 2,200), unused charge £559 (76 x £7.36).
