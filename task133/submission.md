## Tags

**Domain:** Banking, Credit & Financial Risk (stress testing and capital: a regional bank's ICAAP severe-scenario credit loss on its business lending book for the stress year).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The severe scenario puts NZD 11.5 million of stressed credit loss on the business banking book in the stress year to 30 September 2027.**
By reporting segment, in NZD million: Construction 2.5; Manufacturing 1.3; Trade and logistics 2.4; Hospitality, retail and leisure 3.4; Business and property services 1.5; Health, education and personal services 0.4. Not NZD 10.0 million, the result of stressing each borrower at its own division's sales path, which leaves the firms that builders, hotels and tour operators pay at mild multipliers. Not NZD 10.5 million, which averages the payer mix over each division and so understates the borrowers most exposed to the hardest-hit payers on a steep Table 2 curve. Not NZD 12.0 million, which takes the harsher of the own-division and payer readings for every borrower and so stresses builders whose work councils and ministries pay for at the full construction path.

## 2. Critical Components

1. The performing business book is **632 borrowers** with exposure at default of **NZD 496.7 million**.
2. **56 per cent** of those borrowers' trading credits in the year to 30 September 2026 came from payers outside the borrower's own ANZSIC division.

## 3. Step-by-Step Solution

1. Took business_lending_book_2026-09-30.csv, left out the 13 customers in risk grade D (CR-ST-02 section 1.3) and set exposure at default per section 3.4: 632 borrowers, NZD 496.7 million.
2. Read each borrower's ANZSIC division from its BIC code on nzbn_extract_canterbury_otago_southland_2026-10-12.csv by NZBN (section 4.1), not from the book's industry field, which is blank or on the 1993 codes for some borrowers.
3. Classified operating_account_credits_2025-10_to_2026-09.csv: own-account transfers, GST refunds, insurance claims, loan advances and credit interest are not sales; card settlements, branch cash and payments from individuals are household sales at the borrower's own division; every other payer was matched to the NZBN extract's legal or trading name (upper case, LIMITED as LTD, & as AND, first 20 characters): 56 per cent of trading credits came from another division.
4. Weighted each source division's change in ICAAP_2026_severe_scenario_board_approved.xlsx by the borrower's credits to get the change in its own sales, took the Table 2 multiplier on the fall, capped the stressed PD at 100 per cent, applied the Table 3 LGD to each facility and summed: NZD 11.5 million.
5. Net credit losses: summed the Business rows of write_offs_2023-10_to_2026-09.csv by posting half and subtracted the receipts in collections_receipts_FY2026.xlsx dated in the half and on or after the customer's first write-off, keeping the agency's net remittance and dropping its statement upload (Agency collection, the same payment gross of commission), and crediting each guarantor's receipts on its personal case (customer_master_extract_2026-10-09.csv) to the company it guaranteed in guarantees_register_2026-09-30.csv; segment from the customer master's NZBN on the NZBN extract.
6. Default back-test: graded each customer in risk_grade_snapshot_2025-09-30.csv at the grade in force on 30 September 2025 (grade_overrides_2024-2026.xlsx), counted defaults dated 1 October 2025 to 30 September 2026 in default_register_business_FY2026.csv and default_register_rural_FY2026.csv, gave each defaulted facility the lending book holds to the customer that holds it (a connected group's cross-default sits under the group lead's number) and read surviving numbers back through customer_merge_log_2026-03-14.csv.
7. The business banking book's stressed credit loss for the stress year to 30 September 2027 is NZD 11.5 million.

## 4. Deliverable Answers

### orari_icaap_business_stress_2027.xlsx

1. Stressed credit loss, business banking book, stress year to 30 September 2027: NZD 11.5 million.
2. Stressed credit loss by reporting segment, NZD million:
   - Construction: 2.5
   - Manufacturing: 1.3
   - Trade and logistics: 2.4
   - Hospitality, retail and leisure: 3.4
   - Business and property services: 1.5
   - Health, education and personal services: 0.4
3. Borrower-level working: one row per performing borrower with its own division, risk grade, trading credits, sales change through its payers, Table 2 multiplier, stressed PD, EAD and stressed loss.
4. Net credit losses, financial year to 30 September 2026, NZD thousand (H1 October to March, H2 April to September):
   - Construction: H1 187, H2 858
   - Manufacturing: H1 115, H2 380
   - Trade and logistics: H1 200, H2 148
   - Hospitality, retail and leisure: H1 331, H2 699
   - Business and property services: H1 289, H2 292
   - Health, education and personal services: H1 270, H2 280
5. Business borrowers by risk-grade band at 30 September 2025 that defaulted in the following twelve months:
   - Grades 1 to 3: 4 defaulted, 2.1 per cent of the band
   - Grade 4: 9 defaulted, 6.2 per cent of the band
   - Grade 5: 10 defaulted, 6.5 per cent of the band
   - Grade 6: 13 defaulted, 9.9 per cent of the band
   - Grades 7 to 9: 9 defaulted, 12.3 per cent of the band

### board_paper_business_stress_2027.docx

1. Bar chart of stressed credit loss by reporting segment in NZD million (Figure 1), each bar labelled with its segment figure.
2. The paper states the NZD 11.5 million total, the segment losses, the net credit losses by segment and half and the default back-test as in the workbook.
