# task125 · 2027/28 examination call-off for the digit filter's routed payments

## Tags

**Domain:** Accounting, Audit & Forensic Analytics (audit testing and sampling: a council's first-two-digit payment filter and the post-payment examination it buys).
**Analytical objective:** Anomaly Detection & Diagnostics (rebuilding the digit screen against its published statements and diagnosing what each flagged cell holds through the plan year).

## 1. Final Recommendation

**Order 6,900 routed payments from Fernhollow for April 2027 to March 2028.**

The filter routes 6,914 payments in 2027/28 (6,900 to the hundred), 1,200 below the 8,100 Fernhollow sizes on. Not last year's routed count, which ran on the 2023/24 screen's cells and on Tenancy Sustainment instalments that run off before and during the plan year. Not the 2025/26 cells with every Shared Lives payment re-summed after the Home First step-down closure as if a joint household were always paid in halves, which leaves the 16 households left with one guest under the filter's floor when each is paid its whole fee in cell 14.

## 2. Critical Components

1. The 2025/26 screen flags **5** cells: Adult Social Care 14, Housing Support 14, Highways & Transport 49 and 99, Property & Facilities 12
2. Housing Support's 2024-25 Tenancy Sustainment round pays **648** instalments in 2027/28 on the **30**-instalment term
3. From April 2027 **194** Shared Lives carer payments a run fall in cell 14 (**102** now): **60** single carers, **16** halves of **8** joint households and **16** joint households left with one guest paid whole, over **13** runs
4. Routed payments in 2027/28 total **6,914**

## 3. Step-by-Step Solution

1. Screened `wealdmoor_spend_over_500_2023-04_to_2027-02.csv` on gross payments (net plus VAT) of 1,000.00 to 999,999.99 with credit notes left out, the only basis that reproduces all 63 figures in `digit_conformity_statements_2023-24_to_2025-26.pdf` (methodology 4), and applied the flag rule (methodology 3) to 2025/26, the latest statement published when the order is placed (methodology 5): 5 cells.
2. Ran each household in `tenancy_sustainment_payments_2021-07_to_2027-02.csv` out on 30 monthly instalments from its first payment, the term all 288 households of the 2021 round received: 648 fall in 2027/28, so Housing Support cell 14 routes 816.
3. Decomposed each carer's latest "Shared Lives carer payments" amount (per `vendor_no`) into four weeks of up to three weekly rates in `shared_lives_carer_rates_2023-24_to_2027-28.pdf`, unique for every amount that decomposes; an amount that decomposes as no rate set is half a joint household's fee, paid identically to two consecutive vendor numbers, and twice it decomposes uniquely.
4. Read the payment rule from the joint pairs whose amount changes inside the file: a household left with two or more guests stays in halves, and one left with one guest (from 15 November 2023, 21 August 2024 and 17 September 2025) is paid its whole fee by the first vendor number and nothing by the second.
5. Dropped the step-down placements closing 31 March 2027 (`home_first_step-down_closure_notice.eml`; each run pays the four weeks ending on its payment date), re-summed each carer's and each household's fee, paid it under that rule over the 13 Shared Lives runs in the 2027-28 sheet of `bacs_payment_calendar_2025-26_to_2027-28.xlsx` (Adult Social Care cell 14 routes 3,902), carried every other stream in the cells at its 2025/26 count, the same each month, and counted each payment in its run month, the month its BACS file is submitted (`digit_filter_run_book_2024-06.docx` section 2), so the 5 January 2028 carer run falls in December 2027: 6,914 routed.
6. Summed `digit_filter_run_log_2025-26.xlsx` by run month, October's re-run replacing its scheduled run and January's supplementary run added (run book 3 and 4): 8,102 routed in 2025/26, Fernhollow's indicative volume under clause 4.2 of `pasf_lot2_calloff_terms_clauses_4-8.pdf`, 1,200 above the order to the hundred.
7. Attributed each batch in `fernhollow_batch_acknowledgements_2025-26.json` to its run through the log's `batch_ref` and reckoned it in that run month's quarter (clause 6.1), charging payments examined with a 25 minimum per batch and nothing for withdrawn batches (5.2, 5.3), against 1,900 a quarter to September and 2,200 from October (`calloff_WCC-FA-2025-26_order_and_variation_1.pdf`), unused allocation at 40 per cent of the £18.40 base rate on the 2025/26 rate card (6.3), in whole pounds.
8. Recommendation: order 6,900 routed payments for 2027/28.

## 4. Deliverable Answers

### examination_calloff_2027-28.docx

1. Order: 6,900 routed payments, April 2027 to March 2028
2. Department carrying the largest share: Adult Social Care, 3,900
3. Fernhollow's figure from the latest closed year (2025/26): 8,100
4. How far we sit from it: 1,200 below
5. Chart in the note: monthly routed payments April 2025 to March 2028 stacked by department, a dashed line at 675 a month (8,102 / 12), 2027/28 shaded, December 2027 annotated with 700, title "Order for 2027/28: 6,900 routed payments"

### examination_calloff_2027-28.xlsx

1. Plan-year routed payments by month:
   - April 2027: 650
   - May 2027: 632
   - June 2027: 614
   - July 2027: 596
   - August 2027: 578
   - September 2027: 560
   - October 2027: 542
   - November 2027: 524
   - December 2027: 700
   - January 2028: 506
   - February 2028: 506
   - March 2028: 506
2. 2025/26 by month, payments routed and payments Fernhollow examined:
   - April 2025: 634 routed, 628 examined
   - May 2025: 652 routed, 643 examined
   - June 2025: 664 routed, 656 examined
   - July 2025: 668 routed, 658 examined
   - August 2025: 673 routed, 667 examined
   - September 2025: 676 routed, 669 examined
   - October 2025: 681 routed, 675 examined
   - November 2025: 663 routed, 656 examined
   - December 2025: 663 routed, 658 examined
   - January 2026: 685 routed, 680 examined
   - February 2026: 669 routed, 661 examined
   - March 2026: 774 routed, 761 examined
3. 2025/26 by quarter, examinations charged at the premium rate and unused-volume charge:
   - Q1 (April to June 2025): 27 at the premium rate, £0
   - Q2 (July to September 2025): 94 at the premium rate, £0
   - Q3 (October to December 2025): 0 at the premium rate, £1,553
   - Q4 (January to March 2026): 0 at the premium rate, £618
