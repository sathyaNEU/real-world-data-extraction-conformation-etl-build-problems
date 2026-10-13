# task448 submission

## Tags

**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (completing HMDA, a register that leaves out whole classes of lenders, from a county recorder file that holds some lenders' mortgages far less often than others').
**Analytical objective:** Data Extraction & Conformation (ETL) (the HMDA loan-level file, three recorder deliveries in two layouts, a mortgagee alias register and a lender register conformed into one lender table and the county figures).

## 1. Final Recommendation

**Recruit Corvane Home Loans, Weyrauch State Bank, Halverd Mortgage, Mennwell Credit Union and Arkhaven Bank first, in that order, with 310, 260, 230, 200 and 180 first-lien home-purchase mortgages on homes in the eight counties closed in 2024 and 2025; Shunga Valley Bank is sixth with 150.**

The deciding figures are Weyrauch's 260 and Mennwell's 200, two lenders that do not report HMDA, counted from the Venridge file over its capture of mortgages recorded after the deed (60 per cent), since every mortgage a lender makes counts, including those the file does not hold. Not Shunga Valley Bank: it is fifth only when the non-reporting lenders are taken at their rows or at the file's pooled capture of 90 per cent, which leaves Mennwell at 130 because the reporters whose mortgages are recorded with the deed, held at 97 per cent, set the pool. Not Heidebrecht State Bank: 43 of its rows are quitclaim refinances into family trusts, and only counting such refinances as purchase mortgages for every lender, in the captures as well, which guidelines 7.3 and 7.4 exclude, lifts it to 200.

## 2. Critical Components

1. The Venridge file holds **1,673** of the HMDA reporters' **1,731** home-purchase mortgages recorded the same day as the deed (**97%**) and **236** of their **395** recorded after it (**60%**).
2. Weyrauch State Bank has **154** and Mennwell Credit Union **121** home-purchase mortgages closed in 2024 and 2025 in the file, all recorded after the deed.
3. Weyrauch State Bank made **260** and Mennwell Credit Union **200**.

## 3. Step-by-Step Solution

1. Matched the twelve shortlisted lenders to lender_register_2026-09.csv by NMLS ID: seven have LEIs with records in the eight counties in hmda_lar_kansas_2024_2025.csv, five do not.
2. Counted each reporter's originated (action_taken 1), home-purchase (loan_purpose 1), first-lien (lien_status 1) loans in the eight counties in 2024 and 2025: Corvane 311, Halverd 228, Arkhaven 182, Shunga Valley 151, Tessaline 141, Saltfork 138, Ninnescah 133.
3. Stacked the three Venridge deliveries, reading layout v4's RECORDING_DT, DOC_DT, LOAN_AMT, LENDER_NAME, BORROWER_NAME, DEED_RECORDING_DT, SELLER_NAME and REMARKS as v3's MTG_REC_DATE, MTG_INSTR_DATE, MTG_AMT, MORTGAGEE_NAME, MORTGAGOR_NAME, DEED_REC_DATE, GRANTOR_NAME and DOC_REMARKS: 3,770 rows, 2,628 of them closed in 2024 and 2025 by the instrument date (guidelines 7.5). Named each row's lender by its trimmed MORTGAGEE_NAME in mortgagee_alias_register.csv and the lender's LEI through the register. Then left out, in this order, what is not one lender's first-lien mortgage on an arm's-length purchase: 17 re-recordings (a re-recording note in DOC_REMARKS; the original document is already in the file); 81 quitclaim pairings (DEED_TYPE QCD, each a conveyance from the mortgagor to the mortgagor's own trust, not an arm's-length sale under 7.4, so the mortgage is a refinance and not a home-purchase mortgage under 7.3); 10 second mortgages (the smaller of two mortgages against the same DEED_DOC_NO in one county, a subordinate lien under 7.3); 10 land-only records (a record with no SITUS_ADDR of a mortgage with the same lender, mortgagor, amount and instrument date recorded in a second county: one mortgage, counted where the house stands); and 37 seller-carried notes (the mortgagee is the deed's grantor and no lender's alias, 7.2). That leaves 2,473 lender purchase mortgages, among them Weyrauch 154 (166 rows less 3 re-recordings and 9 quitclaim pairings), Mennwell 121 (126 less 2 and 3), Heidebrecht 82 (128 less 1 re-recording, 43 quitclaim pairings and 2 land-only records), Kessinger 80 (81 less 1 quitclaim pairing) and Eisenbrandt 47 (51 less 1, 1 and 2).
4. Every mortgage a lender makes is counted, including any that no report or data file shows (guidelines 7.5), and the Venridge file does not hold every purchase-money mortgage recorded (venridge_pmm_layout_guide_v4.pdf, section 1), so the non-reporters' rows are completed for what the file misses, measured on the lenders in both sources: the 46 HMDA reporters with home-purchase loans in the eight counties, every one in the register and the file. A reporter's lender purchase mortgages in the file over its HMDA count fall in two tight groups set by how its mortgages are recorded (every lender's 2024 and 2025 mortgages are recorded one way): the 42 whose mortgages are recorded the same day as the deed (MTG_REC_DATE equal to DEED_REC_DATE) hold 0.913 to 1.000 of their counts, the 4 that record after the deed 0.593 to 0.607 (reporters with 20 or more loans), wherever they lend. Pooled within each group: 1,673 of 1,731 with the deed (0.9665; 1,701 rows less 5 re-recordings, 12 quitclaim pairings, 10 second mortgages and 1 land-only record) and 236 of 395 after it (0.5975; 248 rows less 4 re-recordings and 8 quitclaim pairings).
5. Divided each non-reporting lender's mortgages by its group's capture (Weyrauch, Mennwell, Heidebrecht and Eisenbrandt record after the deed, Kessinger with it): Weyrauch 154 / 0.5975 = 257.8, Mennwell 121 / 0.5975 = 202.5, Heidebrecht 82 / 0.5975 = 137.2, Kessinger 80 / 0.9665 = 82.8, Eisenbrandt 47 / 0.5975 = 78.7; that is 260, 200, 140, 80 and 80.
6. Ranked the twelve: Corvane 310, Weyrauch 260, Halverd 230, Mennwell 200, Arkhaven 180, then Shunga Valley 150, Tessaline 140, Saltfork 140, Heidebrecht 140, Ninnescah 130, Kessinger 80 and Eisenbrandt 80.
7. For the two-year county figures, placed each home in the county in which the property is recorded (guidelines 2.2; CNTY_NAME): each reporter's HMDA count spread over the counties in proportion to its lender purchase mortgages in the file closed in 2024 and 2025, and every other lender's mortgages in each county divided by its group's capture (the five non-reporters on the shortlist and five more lenders): Saline 1,359.1, McPherson 577.5, Dickinson 361.9, Marion 269.5, Rice, Ottawa, Ellsworth and Lincoln 441.8. The completed lenders at a capture measured within each county and group instead, or the reporters' own mortgages over their group's capture, give the same rounded figures.
8. For the program year, HMDA carries no closing date, so every lender's mortgages come from the file: the 1,387 lender purchase mortgages closed 1 July 2025 to 30 June 2026 (the same exclusions as step 3), each divided by the capture of the way it was recorded, 1,117 the same day as the deed over 0.9665 and 270 after it over 0.5975. From 6 April 2026 the 12 lenders that recorded after the deed in 2024 and 2025 have their closings recorded with the deed (all 201 from 6 April to 30 June 2026, none of their 79 earlier 2026 closings), and their rows for those weeks run 2.05 times the same weeks of 2025 against 0.92 for the other lenders (1.08 and 1.14 from 1 January to 5 April), so each mortgage takes the capture of its own recording. By county: Saline 710.9, McPherson 311.1, Dickinson 191.8, Marion 151.9, Rice, Ottawa, Ellsworth and Lincoln 241.9; all eight 1,607.6, which is 1,600 to the nearest 100. Taking the reporters' July to December 2025 from their 2025 HMDA counts, spread by their recorded mortgages, gives the same rounded figures.
9. Recommendation: recruit Corvane Home Loans, Weyrauch State Bank, Halverd Mortgage, Mennwell Credit Union and Arkhaven Bank first.

## 4. Deliverable Answers

### rural_lender_recruitment_2027.xlsx

1. The five to recruit first, in order, with their first-lien home-purchase mortgages on homes in the eight counties closed in 2024 and 2025:
   - Corvane Home Loans: 310
   - Weyrauch State Bank: 260
   - Halverd Mortgage: 230
   - Mennwell Credit Union: 200
   - Arkhaven Bank: 180
2. The sixth: Shunga Valley Bank, 150.
3. First-lien home-purchase mortgages on homes in each county, closed in 2024 and 2025:
   - Saline: 1,360
   - McPherson: 580
   - Dickinson: 360
   - Marion: 270
   - Rice, Ottawa, Ellsworth and Lincoln together: 440
4. Closed in the July 2025 to June 2026 program year:
   - Saline: 710
   - McPherson: 310
   - Dickinson: 190
   - Marion: 150
   - Rice, Ottawa, Ellsworth and Lincoln together: 240
   - All eight counties: 1,600 (to the nearest 100, from the unrounded county figures)

### rural_lender_recruitment_2027.pptx

5. Bar chart of the twelve shortlisted lenders' counts, the five recruited first in a dark bar:
   - Corvane Home Loans: 310
   - Weyrauch State Bank: 260
   - Halverd Mortgage: 230
   - Mennwell Credit Union: 200
   - Arkhaven Bank: 180
   - Shunga Valley Bank: 150
   - Tessaline Home Lending: 140
   - Saltfork State Bank: 140
   - Heidebrecht State Bank: 140
   - Ninnescah Federal Credit Union: 130
   - Kessinger Federal Credit Union: 80
   - Eisenbrandt State Bank: 80
