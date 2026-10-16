## Tags

**Domain:** Banking, Credit & Financial Risk (expected credit loss provisioning).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Book an allowance for credit losses of $10 million at 30 September 2026 on the unguaranteed portions of the SBA 7(a) loans approved in fiscal years 2019 to 2021.**
Each loan is priced at the default of its guarantor group, the first failure among every performing loan its guarantors stand behind, each at its own months on book, which comes to $9.94 million. Not the loan-by-loan lifetime rates, which price each loan as if it stood alone; not a rate scaled by the group's size or loan count, which holds the operators' new units financed in FY2026 at the pool loans' ages; not the group priced at per-loan default rates, which already hold the history's cross-defaults and count them twice.

## 2. Critical Components

1. Relief-era loans on the books at 30 September 2026: **5,110**, with unguaranteed principal of **$197,538,000**.
2. Relief-era loans whose guarantors stand behind another performing loan: **2,036**, in **988** groups that also hold **1,561** performing loans approved outside FY2019 to FY2021, **1,403** of them in FY2026.
3. Charge-off share of resolved defaults: **91.8%**.
4. Allowance by approval fiscal year: FY2019 **$2.0 million**, FY2020 **$3.0 million**, FY2021 **$5.0 million**.

## 3. Step-by-Step Solution

1. Put legacy_loan_history_200910_201710.parquet and servicing_history_2017-10_2026-09.parquet on SBA loan numbers through sba_loan_master.csv, with servicing_status_codes.csv and October 2017 taken once: each loan's months from its disbursement month, a default its first month-end 90 or more days past due or accelerated, as policy CP-SBA-07 defines it.
2. Joined the loans performing at 30 September 2026 through guarantee_register.xlsx on Party No into the groups the loan authorization's cross-default clause (Part B) makes default together: 2,036 relief-era loans in 988 groups of two or more, with 1,561 performing loans outside the pool.
3. Measured monthly failure rates by six-month band of months on book on loans standing alone (the only loan of their guarantors at risk that month), and payoff rates on every loan at risk, October 2009 to September 2026.
4. Took the share of resolved defaults whose status after liquidation is charged off: 91.8%.
5. Priced each performing relief-era loan at the monthly probability that the first failure among its group's performing loans, each at its own months on book with its own payoff and maturity, comes before it pays off or matures, times 91.8% of its unguaranteed principal scheduled for that month-end at its 30 September 2026 note rate, as CP-SBA-07 sets exposure, and each loan in default at 91.8% of its unguaranteed principal.
6. Summed by approval fiscal year: $9.94 million, booked as $10 million.

## 4. Deliverable Answers

### sba_allowance_fy2026.xlsx

1. Allowance: $10 million at 30 September 2026.
2. Split by approval fiscal year:
   - FY2019: $2.0 million
   - FY2020: $3.0 million
   - FY2021: $5.0 million
3. Section 1112 payments SBA made on these loans for the instalments due in each fiscal quarter:
   - FY2020 Q3 (April to June): $76,581,000
   - FY2020 Q4 (July to September): $88,571,000
   - FY2021 Q1 (October to December): $22,362,000
   - FY2021 Q2 (January to March): $56,835,000
   - FY2021 Q3 (April to June): $60,582,000
   - FY2021 Q4 (July to September): $58,183,000
   - FY2022 Q1 (October to December): $24,141,000
4. Net charge-offs on these loans by fiscal year and approval fiscal year:
   - FY2023: FY2019 approvals $12,518,000; FY2020 approvals $19,933,000; FY2021 approvals $13,333,000
   - FY2024: FY2019 approvals $882,000; FY2020 approvals $6,821,000; FY2021 approvals $11,699,000
   - FY2025: FY2019 approvals $1,487,000; FY2020 approvals $2,189,000; FY2021 approvals $4,133,000
   - FY2026: FY2019 approvals $1,161,000; FY2020 approvals $460,000; FY2021 approvals $2,107,000

### allowance_note_fy2026.docx

1. States the allowance: $10 million.
2. Chart of the allowance and the unguaranteed principal by approval fiscal year: unguaranteed principal $55.0 million, $67.9 million and $74.7 million; allowance $2.0 million, $3.0 million and $5.0 million.
