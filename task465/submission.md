## Tags

**Domain:** General Statistics & Data Science (data integration: each county's dryland grain sorghum yield history conformed from a state statistics service's county and district estimates in two downloads, the years it withheld recovered from the district totals).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Buy the Ardley, Elster and Pallard covers and decline Corvin's and Tresham's.**
Their quoted rates are 1.08, 1.10 and 1.08 times their expected losses of 6.47, 7.46 and 4.73 per cent, under the policy's 1.4; Corvin's runs 1.71 times its 3.30; Tresham's runs 1.84 times its 3.94. Not the published years alone, which leave out the 10 county-years the service withheld and decline all five covers; not filling those years from the district's yield or the county's published years, which still declines all five; not reading them as total failures, which buys Tresham's too.

## 2. Critical Components

1. Withheld years recovered from the district totals, bushels per harvested acre: Ardley **11.4** (2002), **8.6** (2011), **12.5** (2022); Elster **10.4** (2002), **8.0** (2011), **13.2** (2022); Pallard **9.8** (2003), **11.5** (2011); Tresham **24.5** (2006), **22.6** (2011).
2. Expected loss, per cent of liability: Ardley **6.47**; Corvin **3.30**; Elster **7.46**; Pallard **4.73**; Tresham **3.94**.
3. Quoted rate as a multiple of expected loss: Ardley **1.08**; Corvin **1.71**; Elster **1.10**; Pallard **1.08**; Tresham **1.84**.

## 3. Step-by-Step Solution

1. Took non-irrigated grain sorghum harvested acres, production and yield for every county and district from clrs_county_estimates_pull_2024-03.csv and clrs_county_estimates_pull_2026-10.csv, the October 2026 download for the years it holds (methods note 4.1) and the 2008 district recode applied (5.1): 10 county-years of the five counties are withheld (S).
2. Recovered each withheld county-year as its district's harvested acres and production less those of the district's published counties (methods note 2.1), yield their ratio: Ardley 2002 11.4; Ardley 2011 8.6; Ardley 2022 12.5; Elster 2002 10.4; Elster 2011 8.0; Elster 2022 13.2; Pallard 2003 9.8; Pallard 2011 11.5; Tresham 2006 24.5; Tresham 2011 22.6.
3. Brought each crop year's yield, 1991 to 2025, to 2027 by adding the trend in quillfield_re_area_yield_term_sheet_2027.pdf for each year, took each year's indemnity share against 90 per cent of the expected 2027 yield and averaged the 35 shares (risk policy 5.3): expected losses Ardley 6.47, Corvin 3.30, Elster 7.46, Pallard 4.73, Tresham 3.94 per cent.
4. Set each quoted rate in quillfield_re_quote_schedule_2027.xlsx against 1.4 times the expected loss (risk policy 5.2): buy Ardley, Elster and Pallard, decline Corvin and Tresham.
5. Summed the non-irrigated acres in apgc_cover_enrolment_2027.csv submitted before the 5:00 p.m. Central close of 30 October 2026 (22:00 UTC; apgc_cover_enrolment_notice_2027.txt), each field's latest submission, by the field's county: Ardley 3,657.7, Corvin 9,905.6, Elster 3,848.1, Pallard 3,980.0, Tresham 2,943.7 acres; each cover's liability is its acres times its expected yield times 90 per cent times $4.34 a bushel (the term sheet's $7.75 per hundredweight at 56 pounds), its premium the quoted rate times the liability.
6. Converted the grain sorghum tickets in apgc_scale_tickets_2016_2020.csv to bushels at 14 per cent moisture by the conversion in data_dictionary.csv, left out the terminal's tickets written against a transfer in apgc_site_transfers_2016_2020.csv and summed by origin county: Ardley 440,937, Corvin 2,352,717, Elster 449,844, Pallard 381,491, Tresham 399,069 bushels received, divided by each county's 2016 to 2020 all-practices production in the October 2026 download.

## 4. Deliverable Answers

### county_area_yield_quotes_2027.xlsx

1. Buy the Ardley, Elster and Pallard covers; decline Corvin and Tresham.
2. Each cover's expected loss, quoted rate, quoted rate as a multiple of the expected loss, the quoted rate at which its call changes (per cent of liability; the multiple to two decimals) and its call:
   - Ardley: 6.47, 7.00, 1.08, 9.06, buy
   - Corvin: 3.30, 5.65, 1.71, 4.62, decline
   - Elster: 7.46, 8.20, 1.10, 10.45, buy
   - Pallard: 4.73, 5.10, 1.08, 6.62, buy
   - Tresham: 3.94, 7.25, 1.84, 5.52, decline
3. Each cover's 2027 liability and premium, dollars to the nearest hundred:
   - Ardley: 827,200 and 57,900
   - Corvin: 2,681,300 and 151,500
   - Elster: 781,600 and 64,100
   - Pallard: 831,700 and 42,400
   - Tresham: 593,300 and 43,000
4. The cooperative's 2016 to 2020 grain sorghum receipts from each county as a share of the county's production, per cent to one decimal:
   - Ardley: 31.8
   - Corvin: 21.8
   - Elster: 38.8
   - Pallard: 27.5
   - Tresham: 34.8
5. Chart on the Covers sheet: clustered columns of each cover's quoted rate beside the rate at which its call changes, both labelled in per cent of liability.

### conformed_county_dryland_sorghum_yields.csv

1. 175 rows, one per county and crop year 1991 to 2025, with harvested acres, production, yield and source; the withheld county-years recovered from district totals (harvested acres, bushels, bushels per acre):
   - Ardley 2002: 500, 5,700, 11.4
   - Ardley 2011: 500, 4,300, 8.6
   - Ardley 2022: 400, 5,000, 12.5
   - Elster 2002: 500, 5,200, 10.4
   - Elster 2011: 300, 2,400, 8.0
   - Elster 2022: 500, 6,600, 13.2
   - Pallard 2003: 500, 4,900, 9.8
   - Pallard 2011: 600, 6,900, 11.5
   - Tresham 2006: 800, 19,600, 24.5
   - Tresham 2011: 500, 11,300, 22.6
