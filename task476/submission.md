## Tags

> **Domain:** Survey Research & Official Statistics (census, register and administrative data quality).
> **Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Recommend two of the five candidates, Dunmore Heights and Kestrel Park, for the 2027 round of the Neighborhood Stabilization Fund.**
Each has three listed 2020 tracts at 20 per cent or more in 2019 to 2023 with a rise from 2014 to 2018 significant at 90 per cent; Calloway Flats has one; Linden Row has two; Sorrel Bend has one. Not Linden Row, whose tract 303.01 rises only against its old tract's 17.8 per cent and stood at 28.9 on its own block groups; Kestrel Park qualifies because tract 403.02 stood at 9.5, not the old tract's 19.1.

## 2. Critical Components

1. Tract 403.02's 2014 to 2018 poverty rate on its own block groups is **9.5%** (z **4.29**).
2. Tract 303.01's 2014 to 2018 poverty rate on its own block groups is **28.9%** (z **0.56**).
3. Qualifying tracts: Calloway Flats **1**, Dunmore Heights **3**, Kestrel Park **3**, Linden Row **2**, Sorrel Bend **1**.

## 3. Step-by-Step Solution

1. Read the guidelines (nsf_2027_program_guidelines.pdf) and the candidate list in carrow_nsf_2027_candidate_neighborhoods.xlsx: 28 listed 2020 tracts in five neighborhoods.
2. Took each listed tract's 2019 to 2023 rate from ACSDT5Y2023.B17001-Data-hollis-tracts.csv (B17001_002 over B17001_001) and its margin by the proportion formula (guidelines 3.2).
3. For a tract keeping its 2010 code, took its 2014 to 2018 rate and margin from ACSDT5Y2018.B17001-Data-hollis-tracts.csv the same way.
4. For each tract the 2020 census split, found the 2010 block groups its blocks come from in tab2010_tab2020_st59_hollis.txt (the first digit of each 2010 block) and summed their 2014 to 2018 estimates in ACSDT5Y2018.B17021-Data-hollis-blockgroups.csv, margins as the root sum of squares: tract 403.02 9.5%, 303.01 28.9%.
5. Tested each tract (guidelines 3.1): 2019 to 2023 rate of 20 per cent or more and z over 1.645; counted the qualifying tracts per neighborhood: Calloway Flats 1, Dunmore Heights 3, Kestrel Park 3, Linden Row 2, Sorrel Bend 1.
6. From carrow_code_cases_2019_2027.csv and carrow_code_case_events_2019_2027.csv, took each housing case's status on 31 December 2026 from its event history (a case closed in 2026 and reopened in 2027 was closed that day), residential land uses from carrow_parcels_2027-03.csv through the prior parcel number for older cases, and days from each case's opening: the open properties and average days below.
7. From both fiscal-year sheets of nsf_rehab_payment_register_fy2023_fy2027.xlsx, took checks dated in 2026 that were not reversed, whenever the reversal was posted, so a reissue dated in 2026 counts and a 2026 check voided in 2027 does not: the dollars and properties below.
8. Recommended the neighborhoods with three or more qualifying tracts: Dunmore Heights and Kestrel Park.

## 4. Deliverable Answers

### nsf_2027_tract_poverty_change.xlsx

1. Each listed tract, 2014 to 2018 rate and margin, 2019 to 2023 rate and margin, in per cent, and whether it meets both tests:
   - Calloway Flats 501: 16.5 ± 3.6; 26.6 ± 3.8; qualifies
   - Calloway Flats 502: 22.2 ± 4.6; 23.9 ± 5.3; does not qualify
   - Calloway Flats 503.01: 11.4 ± 3.9; 11.8 ± 3.6; does not qualify
   - Calloway Flats 503.02: 11.8 ± 4.1; 12.2 ± 3.9; does not qualify
   - Calloway Flats 504: 13.9 ± 4.3; 15.0 ± 4.0; does not qualify
   - Dunmore Heights 201: 17.8 ± 3.7; 29.2 ± 4.3; qualifies
   - Dunmore Heights 202: 14.0 ± 3.3; 26.1 ± 3.9; qualifies
   - Dunmore Heights 203: 21.5 ± 4.9; 24.7 ± 4.8; does not qualify
   - Dunmore Heights 204: 17.7 ± 3.8; 29.8 ± 4.5; qualifies
   - Dunmore Heights 205.01: 12.7 ± 4.2; 14.7 ± 4.0; does not qualify
   - Dunmore Heights 205.02: 11.2 ± 3.8; 12.7 ± 3.4; does not qualify
   - Kestrel Park 401: 13.8 ± 3.3; 25.7 ± 3.9; qualifies
   - Kestrel Park 402: 16.9 ± 3.6; 27.1 ± 4.1; qualifies
   - Kestrel Park 403.01: 33.3 ± 5.5; 15.7 ± 3.9; does not qualify
   - Kestrel Park 403.02: 9.5 ± 3.0; 21.4 ± 3.4; qualifies
   - Kestrel Park 404: 22.3 ± 4.9; 22.9 ± 4.5; does not qualify
   - Kestrel Park 405: 11.6 ± 2.9; 11.7 ± 2.8; does not qualify
   - Linden Row 301: 16.3 ± 3.6; 26.3 ± 4.0; qualifies
   - Linden Row 302: 18.2 ± 3.7; 30.1 ± 4.6; qualifies
   - Linden Row 303.01: 28.9 ± 6.0; 31.6 ± 5.4; does not qualify
   - Linden Row 303.02: 7.7 ± 3.3; 7.5 ± 2.9; does not qualify
   - Linden Row 304: 12.1 ± 3.9; 13.4 ± 3.8; does not qualify
   - Linden Row 305: 21.0 ± 4.0; 22.4 ± 3.7; does not qualify
   - Sorrel Bend 601: 7.9 ± 2.7; 9.9 ± 2.8; does not qualify
   - Sorrel Bend 602.01: 22.5 ± 5.6; 19.5 ± 4.7; does not qualify
   - Sorrel Bend 602.02: 21.6 ± 5.5; 34.2 ± 5.6; qualifies
   - Sorrel Bend 603: 10.9 ± 3.7; 14.1 ± 3.9; does not qualify
   - Sorrel Bend 604: 25.4 ± 4.1; 24.0 ± 3.9; does not qualify
2. Each neighborhood, qualifying tracts, residential properties with a housing case open on 31 December 2026, average days open, grant dollars paid in 2026, properties paid:
   - Calloway Flats: 1; 24; 190; $135,908; 8
   - Dunmore Heights: 3; 25; 196; $323,355; 12
   - Kestrel Park: 3; 31; 167; $335,719; 16
   - Linden Row: 2; 27; 140; $474,212; 18
   - Sorrel Bend: 1; 21; 253; $220,471; 9

### nsf_2027_designation_memo.pdf

1. Recommends two of five: Dunmore Heights and Kestrel Park.
2. Chart of each listed tract's change with its 90 per cent interval, qualifying tracts highlighted, on pages 1 and 2; the neighborhood table beside it.
