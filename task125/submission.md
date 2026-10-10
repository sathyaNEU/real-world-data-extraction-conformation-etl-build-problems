# task125 · 2027/28 examination call-off for the digit filter's routed payments

## Tags

**Domain:** Accounting, Audit & Forensic Analytics (audit testing and sampling: a council's first-two-digit payment filter and the post-payment examination it buys).
**Analytical objective:** Anomaly Detection & Diagnostics (rebuilding the digit screen against its published statements and diagnosing what each flagged cell holds through the plan year).

## 1. Final Recommendation

**Order 6,500 routed payments from Fernhollow for April 2027 to March 2028.**

The filter routes 6,522 payments in 2027/28 (6,500 to the hundred), 1,600 below the 8,100 Fernhollow sizes on. Not last year's routed count, which ran on the 2023/24 screen's cells and on Tenancy Sustainment instalments that run off before and during the plan year. Not the 2025/26 cells with the instalments run off and Shared Lives carried at today's amounts, which misses the 60 carers whose single four-weekly payment drops into cell 14 once the Home First step-down places close.

## 2. Critical Components

1. The 2025/26 screen flags **5** cells: Adult Social Care 14, Housing Support 14, Highways & Transport 49 and 99, Property & Facilities 12
2. Housing Support's 2024-25 Tenancy Sustainment round pays **648** instalments in 2027/28 on the **30**-instalment term
3. From April 2027 **162** Shared Lives carers are paid in cell 14, **60** more than now, over **13** runs
4. Routed payments in 2027/28 total **6,522**

## 3. Step-by-Step Solution

1. Screened `wealdmoor_spend_over_500_2023-04_to_2027-02.csv` on gross payments (net plus VAT) of 1,000.00 to 999,999.99 with credit notes left out, the only basis that reproduces all 63 figures in `digit_conformity_statements_2023-24_to_2025-26.pdf` (methodology 4), and applied the flag rule (methodology 3) to 2025/26, the latest statement published when the order is placed (methodology 5): 5 cells.
2. Carried every payment stream in those cells other than Tenancy Sustainment instalments and Shared Lives carer payments at its 2025/26 count, the same in every month: 3,768.
3. Ran each household in `tenancy_sustainment_payments_2021-07_to_2027-02.csv` out on 30 monthly instalments from its first payment, the term all 288 households of the 2021 round received: 648 fall in 2027/28, so Housing Support cell 14 routes 816.
4. Decomposed each carer's four-weekly amount (one per `vendor_no`, unchanged through the file) into four weeks of the weekly rates in `shared_lives_carer_rates_2023-24_to_2027-28.pdf`, unique for every amount, dropped the step-down placements closing 31 March 2027 (`home_first_step-down_closure_notice.eml`) and re-binned: 162 carers in cell 14 on the 13 Shared Lives runs in the 2027-28 sheet of `bacs_payment_calendar_2025-26_to_2027-28.xlsx`, so Adult Social Care cell 14 routes 3,486 and the year 6,522 (by payment date or by run month alike).
5. Counted each plan-year payment in its run month, the month its BACS file is submitted (`digit_filter_run_book_2024-06.docx` section 2, submission dates from the calendar): the 5 January 2028 carer run's file goes on 31 December and the 1 March 2028 run's on 28 February, so December 2027 carries two carer runs and every other month one.
6. Summed `digit_filter_run_log_2025-26.xlsx` by run month, October's re-run replacing its scheduled run and January's supplementary run added (run book 3 and 4): 8,126 routed in 2025/26, Fernhollow's indicative volume under clause 4.2 of `pasf_lot2_calloff_terms_clauses_4-8.pdf`, 1,600 above the order to the hundred.
7. Attributed each batch in `fernhollow_batch_acknowledgements_2025-26.json` to its run month through the log's `batch_ref` and reckoned it in that run month's quarter (clause 6.1), charging the payments examined with a 25 minimum per batch and nothing for withdrawn batches (5.2, 5.3), against 1,900 a quarter to September and 2,200 from October (`calloff_WCC-FA-2025-26_order_and_variation_1.pdf`), unused allocation at 40 per cent of the £18.40 base rate on the 2025/26 rate card (6.3), rounded to whole pounds.
8. Recommendation: order 6,500 routed payments for 2027/28.

## 4. Deliverable Answers

### examination_calloff_2027-28.docx

1. Order: 6,500 routed payments, April 2027 to March 2028
2. Department carrying the largest share: Adult Social Care, 3,500
3. Fernhollow's figure from the latest closed year (2025/26): 8,100
4. How far we sit from it: 1,600 below
5. Chart in the note: monthly routed payments April 2025 to March 2028 stacked by department, a dashed line at 677 a month (8,126 / 12), 2027/28 shaded, December 2027 annotated with 638, title "Order for 2027/28: 6,500 routed payments"

### examination_calloff_2027-28.xlsx

1. Plan-year routed payments by month:
   - April 2027: 620
   - May 2027: 602
   - June 2027: 584
   - July 2027: 566
   - August 2027: 548
   - September 2027: 530
   - October 2027: 512
   - November 2027: 494
   - December 2027: 638
   - January 2028: 476
   - February 2028: 476
   - March 2028: 476
2. 2025/26 by month, payments routed and payments Fernhollow examined:
   - April 2025: 636 routed, 630 examined
   - May 2025: 654 routed, 645 examined
   - June 2025: 666 routed, 658 examined
   - July 2025: 670 routed, 660 examined
   - August 2025: 675 routed, 668 examined
   - September 2025: 678 routed, 673 examined
   - October 2025: 683 routed, 678 examined
   - November 2025: 665 routed, 657 examined
   - December 2025: 665 routed, 661 examined
   - January 2026: 687 routed, 679 examined
   - February 2026: 671 routed, 663 examined
   - March 2026: 776 routed, 767 examined
3. 2025/26 by quarter, examinations charged at the premium rate and unused-volume charge:
   - Q1 (April to June 2025): 33 at the premium rate, £0
   - Q2 (July to September 2025): 101 at the premium rate, £0
   - Q3 (October to December 2025): 0 at the premium rate, £1,501
   - Q4 (January to March 2026): 0 at the premium rate, £559
