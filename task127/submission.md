## Tags

**Domain:** Banking, Credit & Financial Risk (expected credit loss provisioning).  
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**The business support unit should take on Kinloch Engineering and Matai Valley Foods, keeping NZ$3,350,000 of 2027 write-off off Ruahine's book with NZ$5,800,000 of the NZ$6,000,000 envelope.** A package at Matai also keeps out of default the Ruahine borrowers that take most of their receipts from it. Not Kinloch Engineering and Ridgeway Precast, which lead on the two borrowers' own expected write-off but leave Matai's dependants exposed. Not Matai Valley Foods and Ridgeway Precast, the next-best pair inside the envelope, which gives up Kinloch's NZ$1,600,000 for Ridgeway's NZ$1,450,000.

## 2. Critical Components

1. Ruahine borrowers taking most of their 2026 receipts from a watch-list borrower: **8** from Matai Valley Foods, **1** from Ridgeway Precast, none from the others
2. Borrowers taking 30 per cent or more of their receipts from a payer that defaulted in 2022 to 2025 defaulted within twelve months **13** times in **31**; in borrower-years whose such payer was neither in default nor defaulting, **5** times in **211**
3. Matai Valley Foods' package keeps **NZ$1,750,000** off the book against its own expected write-off of **NZ$817,000**

## 3. Step-by-Step Solution

1. Summed twelve-month PD times LGD times EAD over the facilities in ifrs9_facility_run_2026-12-31.csv of each borrower on watch_list_2027-01.pdf: Matai Valley Foods NZ$817,000 of its own.
2. Built each customer's 2026 receipts in business_account_transactions_2021-2026.csv, own-account transfers and Ruahine lending left out and on-us counterparties resolved through customer_master_2026-12.xlsx and account_number_crosswalk_2023.csv: 8 borrowers take most of their receipts from Matai Valley Foods and 1 from Ridgeway Precast.
3. Dated each default by its first trigger in default_register_2021-2026.csv, with cures from default_cures_2021-2026.csv, per the default definition in ifrs9_pd_model_validation_2025.pdf: 13 of 31 borrowers that took 30 per cent or more of their receipts in the twelve months before a payer's first trigger from that payer, and were performing at it, defaulted within twelve months of it, against 5 of 211 borrower-years from 2022 to 2025 in which a borrower performing at the start of the year took 30 per cent or more of the previous year's receipts from a Ruahine borrower neither in default at the start of the year nor defaulting during it (any share from 10 to 45 per cent selects the same borrowers).
4. Added to each watch-list borrower its PD times 0.3957 (13 of 31 less 5 of 211, the rise in a dependant's chance of default when its main payer defaults) times each dependant's LGD times EAD: Matai Valley Foods NZ$1,750,000 and Ridgeway Precast NZ$1,450,000, the others their own figures.
5. Carried each property in security_register_2026-12.xlsx from the quarter in its valuer's reference (the register's 17/06/2023 valuation dates are the core migration's load date) by the latest release in commercial_property_index_2015-2026.csv, dropping mortgages title_instruments_2026-12.csv shows discharged by 31 December 2026: the security values below.
6. Added to each borrower's limits in the 2026 run the guarantees it gave on the Guarantees sheet, matched by NZBN or by its current or former names in companies_register_extract_2026-12.csv, less those the Deed log releases by 31 December 2026: the commitments below.
7. Took the borrowers performing at the end of 2024 in ifrs9_facility_run_2024-12-31.csv and the defaults that started in 2025, keying each register row written against a loan account to the customer whose account repays that loan in business_account_transactions_2021-2026.csv: the sector shares below.
8. Chose, under section 3 of bsu_terms_of_reference_2027.pdf (a NZ$6,000,000 envelope, whole packages), the borrowers whose proposed lines fit with the largest total: Kinloch Engineering and Matai Valley Foods, NZ$3,350,000.

## 4. Deliverable Answers

### bsu_intake_2027.xlsx

1. Take on Kinloch Engineering and Matai Valley Foods; 2027 write-off kept off the book NZ$3,350,000.
2. 2027 write-off each package would keep off, New Zealand dollars to the nearest 50,000:
   - Matai Valley Foods: NZ$1,750,000
   - Kinloch Engineering: NZ$1,600,000
   - Ridgeway Precast: NZ$1,450,000
   - Marlowe Packhouse: NZ$1,050,000
   - Selwyn Joinery: NZ$700,000
   - Brightwater Motor Group: NZ$450,000
   - Coastline Aggregates: NZ$350,000
   - Northgate Print: NZ$250,000
3. Value at 31 December 2026 of the property held as security, New Zealand dollars to the nearest thousand:
   - Matai Valley Foods: NZ$6,321,000
   - Kinloch Engineering: NZ$4,914,000
   - Ridgeway Precast: NZ$794,000
   - Marlowe Packhouse: NZ$7,333,000
   - Selwyn Joinery: NZ$1,431,000
   - Brightwater Motor Group: NZ$3,532,000
   - Coastline Aggregates: NZ$7,549,000
   - Northgate Print: NZ$2,877,000
4. Total commitment at 31 December 2026, New Zealand dollars to the nearest thousand:
   - Matai Valley Foods: NZ$5,250,000
   - Kinloch Engineering: NZ$10,022,000
   - Ridgeway Precast: NZ$6,650,000
   - Marlowe Packhouse: NZ$7,800,000
   - Selwyn Joinery: NZ$4,350,000
   - Brightwater Motor Group: NZ$3,200,000
   - Coastline Aggregates: NZ$2,743,000
   - Northgate Print: NZ$1,750,000
5. Share of business borrowers performing at the end of 2024 that defaulted in 2025, percent to one decimal:
   - A Agriculture, Forestry and Fishing: 6.4%
   - C Manufacturing: 8.2%
   - E Construction: 6.0%
   - F Wholesale Trade: 4.2%
   - G Retail Trade: 8.5%
   - I Transport, Postal and Warehousing: 9.4%
   - N Administrative and Support Services: 6.5%

### bsu_intake_2027.docx

6. A one-page note to the credit committee giving the recommendation and its reasoning.
