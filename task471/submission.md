## Tags

**Domain:** General Statistics & Data Science (data integration and record linkage: a health department links two overlapping lists of private wells, conforms three laboratories' results and estimates each county's wells above the nitrate standard from a survey sampled from both lists).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Six of the sixteen counties qualify for the 2027 Well Water Assistance allocation: Alderwick, Brannock, Farrowdale, Glenmoor, Lindmark and Netherby.**  
Each has an estimated 250 or more wells in its survey population above 10 mg/L nitrate as nitrogen once every tested well counts for the wells it stands for, one over its chance of selection from either list. Not the three that scaling each county's share of tested wells above the standard to its wells gives (Alderwick, Glenmoor and Netherby): the parcel list was sampled at 4.0 per cent against the permit list's 8.3, and its parcel-only wells run higher in nitrate (20.4 per cent of the tested ones above the standard against 6.4 per cent of the tested wells on the permit list), so the pooled share leaves out Brannock, Farrowdale and Lindmark. Nor the ten that weighting each tested well by the sampling rate of the list it was drawn from (that list's target over its wells in Table 2) gives: a well on both lists had two chances of selection, and counting it at one list's rate counts it about twice, which puts Dunmere, Ivyridge, Kestrel Plains and Rushbrook over the line.

## 2. Critical Components

1. Counties at or above 250: **6** of 16.
2. Sampling rates across the sixteen counties: permit list **8.3%** (2,740 of 32,933 wells), parcel list **4.0%** (1,407 of 35,440).
3. Tested wells on both lists: **3,002** of the **3,996** tested; wells on the survey's lists: **42,598**.

## 3. Step-by-Step Solution

1. Built the permit list from DOH_well_construction_permits_extract_2026-08-03.csv (WELL_USE DOMESTIC, WELL_STATUS ACTIVE, DATE_DRILLED from 1986-01-01 to 2025-08-31) and the parcel list from county_assessor_residential_parcels_2025_roll.xlsx (the water code each layout gives for a private well, Codes sheet); both match Table 2 of PWNS_2025-26_survey_design_report.pdf, 32,933 and 35,440 wells.
2. Linked each permit to its parcel by parcel number (digits only) or, on a permit with none, by house number and street name (directions, suffixes and punctuation set aside): a well is on both lists when its permit's parcel carries the private-well code, 42,598 wells in the survey population.
3. Read PWNS_2025-26_draw_manifest.csv: TESTED and TESTED_EARLIER rows count toward each list's target, so the permit list is sampled at f = target over its wells and the parcel list likewise; each tested well's place on the other list comes from the linkage (3,002 of 3,996 tested wells are on both).
4. Took each first-test kit's final nitrate as nitrogen from Halvorsen_PWNS_results_2025-26.csv (RESULT_STATUS FINAL), Cedarline_PWNS_results_2025-26.xlsx (latest Report Date) and Kinsale_PWNS_results_2025-26.csv (highest VERSION, NO3 divided by 4.427): 313 tested wells above 10 mg/L.
5. Summed, over each county's tested wells above the standard, one over the well's chance of selection: f permit, f parcel, or 1 - (1 - f permit)(1 - f parcel) for a well on both lists; six counties at or above 250 (Brannock lowest at 304, Ivyridge highest below at 199), and Hartley's estimator at every split of the wells on both lists and the estimate post-stratified by list membership give the same six.
6. Matched each request in PWNS_retest_kit_requests_2026.csv to its well by ORIGINAL_KIT (portal) or by ship-to house number and street in the request's county (phone), and counted each well in the county the survey tested it in, not the county a border ZIP code routed the request to.
7. Kept retests of wells first tested above 10 mg/L whose retest sample (the laboratories' collection date) was collected on or before June 30, 2026 (WWA-2027-01 4.2); households outside the survey and later retests left out; still above when the retest is above 10 mg/L: 232 retested, 195 still above.
8. Charted the sixteen estimates against the 250-well line, the qualifying counties highlighted.

## 4. Deliverable Answers

### nitrate_assistance_counties_2027.xlsx

1. Counties that qualify: **6**: Alderwick, Brannock, Farrowdale, Glenmoor, Lindmark and Netherby.
2. Each county: private domestic wells on the survey's lists; qualifies; wells first tested above the standard and retested by June 30, 2026; of those, still above:
   - Alderwick: 2,977; yes; 25; 20
   - Brannock: 1,438; yes; 11; 11
   - Corwell: 1,073; no; 5; 5
   - Dunmere: 2,703; no; 14; 13
   - Eskvale: 1,683; no; 9; 6
   - Farrowdale: 2,306; yes; 10; 9
   - Glenmoor: 10,833; yes; 43; 32
   - Hallowcroft: 1,380; no; 7; 5
   - Ivyridge: 3,469; no; 15; 14
   - Kestrel Plains: 3,435; no; 22; 17
   - Lindmark: 2,631; yes; 9; 9
   - Morrowfield: 839; no; 5; 4
   - Netherby: 4,573; yes; 29; 27
   - Oakmere: 866; no; 9; 8
   - Quarrington: 981; no; 8; 6
   - Rushbrook: 1,411; no; 11; 9

### nitrate_assistance_counties_2027.png

3. Bar chart of the sixteen counties' estimated wells above the standard against the 250-well line, the six qualifying counties highlighted.
