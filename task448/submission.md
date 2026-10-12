# task448 submission

## Tags

**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (completing HMDA, a register that leaves out whole classes of lenders, from a county recorder file that holds some lenders' mortgages far less often than others').
**Analytical objective:** Data Extraction & Conformation (ETL) (the HMDA loan-level file, three recorder deliveries in two layouts, a mortgagee alias register and a lender register conformed into one lender table and the county figures).

## 1. Final Recommendation

**Recruit Corvane Home Loans, Weyrauch State Bank, Halverd Mortgage, Mennwell Credit Union and Arkhaven Bank first, in that order, with 310, 260, 230, 200 and 180 first-lien home-purchase mortgages on homes in the eight counties closed in 2024 and 2025; Shunga Valley Bank is sixth with 150.**

The deciding figures are Weyrauch's 260 and Mennwell's 200, two lenders that do not report HMDA, counted from the Venridge file over its capture of mortgages recorded after the deed (60 per cent). Not Shunga Valley Bank: it is fifth only when the non-reporting lenders are taken at their rows or at the file's pooled capture of 90 per cent, which leaves Mennwell at 130 because the reporters whose mortgages are recorded with the deed, held at 97 per cent, set the pool. Not Heidebrecht State Bank: 43 of its rows are quitclaim refinances into family trusts, and only counting them, which guidelines 7.3 and 7.4 exclude, lifts it to 200.

## 2. Critical Components

1. The Venridge file holds **1,673** of the HMDA reporters' **1,731** home-purchase mortgages recorded the same day as the deed (**97%**) and **236** of their **395** recorded after it (**60%**).
2. Weyrauch State Bank has **154** and Mennwell Credit Union **121** home-purchase mortgages closed in 2024 and 2025 in the file, all recorded after the deed.
3. Weyrauch State Bank made **260** and Mennwell Credit Union **200**.

## 3. Step-by-Step Solution

1. Matched the twelve shortlisted lenders to lender_register_2026-09.csv by NMLS ID: seven have LEIs with records in the eight counties in hmda_lar_kansas_2024_2025.csv, five do not.
2. Counted each reporter's originated (action_taken 1), home-purchase, first-lien loans in the eight counties in 2024 and 2025: Corvane 311, Halverd 228, Arkhaven 182, Shunga Valley 151, Tessaline 141, Saltfork 138, Ninnescah 133.
3. Stacked the three Venridge deliveries (layouts v3 and v4), named each mortgagee's lender through mortgagee_alias_register.csv, kept mortgages closed (MTG_INSTR_DATE, DOC_DT in v4) in 2024 and 2025, and dropped what is not a lender's arm's-length first lien under guidelines 7.2 to 7.4 (quitclaim refinances into a family trust, seller-carried notes, the smaller mortgage against a shared deed), re-recordings, and the land-only second-county record of a farmstead mortgage: Weyrauch 154, Mennwell 121, Heidebrecht 82, Kessinger 80, Eisenbrandt 47.
4. Split the recorded mortgages by whether each was recorded the same day as its deed or later (every lender records one way in 2024 and 2025) and measured the file against HMDA on the reporters in each group: 1,673 of 1,731 (97 per cent) with the deed, 236 of 395 (60 per cent) after it.
5. Divided each non-reporting lender's rows by its group's capture: Weyrauch 260, Mennwell 200, Heidebrecht 140, Kessinger 80, Eisenbrandt 80.
6. Ranked the twelve: Corvane 310, Weyrauch 260, Halverd 230, Mennwell 200, Arkhaven 180, then Shunga Valley 150, Tessaline 140, Saltfork 140, Heidebrecht 140, Ninnescah 130, Kessinger 80 and Eisenbrandt 80.
7. For the county figures, spread each reporter's HMDA count for 2024 and 2025 over the counties its recorded mortgages stand in and added every other lender's rows over its group's capture; for the program year, divided each recorded mortgage closed 1 July 2025 to 30 June 2026 by the capture of the way that mortgage was recorded (the in-house lenders' closings from 6 April 2026 are recorded with the deed).
8. Recommendation: recruit Corvane Home Loans, Weyrauch State Bank, Halverd Mortgage, Mennwell Credit Union and Arkhaven Bank first.

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
   - All eight counties: 1,610

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
