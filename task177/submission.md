## Tags

**Domain:** Banking, Credit & Financial Risk (credit scoring and PD modeling).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**About 300 of the pool's 12,880 loans will be 90 or more days past due on 30 June 2027.** Each loan is read off its group: the history's six-month rate for loans whose group was paying for none, one, two or three or more members at its last meeting, applied to the pool's loans in those states, gives 278.1. Not the 100 that reading each member's own payment gives, which treats every carried member as carried and every payer as safe. Not the 200 that flags a group for carrying anyone, which prices a group paying for two at one meeting like a group paying for one.

## 2. Critical Components

1. The pool's loans by how many members their group paid for at its last meeting on or before 31 December 2026: **9,082** none, **3,372** one, **412** two, **14** three or more.
2. Groups paying for two or more members at that meeting: **97**, holding **426** of the pool's loans.

## 3. Step-by-Step Solution

1. Joined collectpro_collections_FY2023-24.csv and collectpro_collections_FY2024-25.csv to kshetra_collections_2025-04_to_2026-12.parquet through kshetra_migration_map_20250401.csv, reading SELF and OWN as paid by the member, GS and GRP_SUPP as paid by another member of her group and NIL and NOT_PAID as unpaid (operating policy section 4): one ledger of 1,554,898 instalment rows.
2. Took each loan's days past due from the due date of its oldest unpaid instalment (operating policy section 6).
3. At each month end from 31 July 2023 to 30 June 2026, took the loans current then and disbursed at least 91 days earlier, counted the instalments other members paid in the loan's group at its last meeting on or before the month end, and read the share of loans 90 or more days past due 181 days later: 0.34, 3.11, 31.15 and 100.00 per cent for none, one, two and three or more.
4. Counted the pool tape's 12,880 loans by the same count at their group's last meeting on or before 31 December 2026: 9,082, 3,372, 412 and 14.
5. Multiplied each count by its rate and added: 278.1 loans, 300 to the nearest 100.
6. For the guardrails, kept active JLG and MFI-IND accounts in cic_portfolio_review_PVM_20261231.csv, counted Salandi's MFI0447 and SFB0029 and Gandhamardan's BNK0102 and BNK0115 as one institution each through the successor_code and parent_code of cic_member_directory_202612.csv (CPN-MF-07 section 3), and counted a loan once where SFB0014 reports the same opening date and sanctioned amount under two account numbers, taking the report later than 13 March 2026: 2,528 borrowers in breach, INR 821.3 lakh of pool principal.
7. Recommendation: about 300 loans 90 or more days past due on 30 June 2027.

## 4. Deliverable Answers

### pool_90dpd_forecast.xlsx

1. Forecast: 300 loans 90 or more days past due on 30 June 2027.
2. Borrowers in breach of the microfinance guardrails on the bureau at the cut-off, and the pool principal outstanding on their loans (INR lakh), by branch:
   - KND Kendrapara: 191 borrowers, INR 63.4 lakh
   - PTM Pattamundai: 164 borrowers, INR 51.8 lakh
   - RJN Rajnagar: 168 borrowers, INR 55.0 lakh
   - JSP Jagatsinghpur: 210 borrowers, INR 69.7 lakh
   - TRT Tirtol: 198 borrowers, INR 64.4 lakh
   - ERS Ersama: 173 borrowers, INR 51.6 lakh
   - BDK Bhadrak: 217 borrowers, INR 67.8 lakh
   - CHB Chandbali: 192 borrowers, INR 66.4 lakh
   - BLS Balasore: 254 borrowers, INR 81.3 lakh
   - BST Basta: 208 borrowers, INR 72.0 lakh
   - JJR Jajpur Road: 143 borrowers, INR 47.3 lakh
   - BNJ Binjharpur: 139 borrowers, INR 46.2 lakh
   - SLP Salepur: 150 borrowers, INR 47.7 lakh
   - NIA Niali: 121 borrowers, INR 36.7 lakh

### pool_purchase_note.docx

1. The forecast: about 300 of the pool's 12,880 loans 90 or more days past due on 30 June 2027.
2. One chart: horizontal bars of the expected loans 90 or more days past due by how many members the group paid for at its last meeting on or before the cut-off, each state labelled with its pool loan count.
