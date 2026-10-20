## Tags

**Domain:** Survey Research & Official Statistics (official time-series production: an annual model-based poverty series rebuilt on new county-equivalents, its 2020 to 2022 years produced by temporal disaggregation with SNAP recipients benchmarked town by town to the survey's five-year level).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Split the $12,000,000 as follows: Greater Ormsby Council of Governments $1,650,000, Mill River Valley Council of Governments $2,250,000, Tarrow Uplands Council of Governments $330,000, Southern Shore Council of Governments $720,000, Wexport Harbor Council of Governments $2,140,000, Two Rivers Council of Governments $1,860,000, Northern Hills Council of Governments $330,000, Quinnet Valley Council of Governments $1,380,000 and Eastern Bays Council of Governments $1,340,000.**
The split follows the nine regions' 2020-2024 average residents in poverty (together 240,800), with each former county's 2020, 2021 and 2022 estimate divided among its towns by their SNAP recipients that year scaled to each town's own 2020-2024 survey count. Not the split the five-year release's town shares give (Greater Ormsby $1,620,000, Mill River Valley $2,280,000, six of the nine amounts off), because that release is an average over 2020 to 2024 and carries the 2021 relocations out of Ormsby and Wexport into 2020 and 2021; not the split the year's SNAP recipients give (Greater Ormsby $1,750,000, nine off), because recipients per resident in poverty differ by town (the survey count runs from 0.87 to 3.13 times the recipients); not the release read as 2022 and moved by SNAP (Greater Ormsby $1,680,000, four off), because the release describes the whole 60 months.

## 2. Critical Components

1. Average residents in poverty, 2020-2024, nearest hundred: Greater Ormsby **33,100**, Mill River Valley **45,100**, Tarrow Uplands **6,600**, Southern Shore **14,500**, Wexport Harbor **42,900**, Two Rivers **37,400**, Northern Hills **6,700**, Quinnet Valley **27,600** and Eastern Bays **26,900**.
2. The nine averages sum to **240,800**.

## 3. Step-by-Step Solution

1. Took each year's estimate as last published (rule 2.1): the former counties' 2020, 2021 and 2022 from Table 2 of sdc_poverty_estimates_dec2022.pdf, sdc_poverty_estimates_dec2023.pdf and sdc_poverty_estimates_dec2024_transition.pdf, and the planning regions' 2023 (Table 2) and 2024 (Table 1) from sdc_poverty_estimates_2024_planning_regions.xlsx; the former counties total 237,551, 240,214 and 241,527.
2. Matched the towns in dss_snap_participation_by_town_2019_2026.txt to town_county_region_codes.csv (DSS writes them in capitals with abbreviations) and took each town's mean monthly RECIPIENTS in each calendar year 2020 to 2024, the year the methods note defines.
3. Took each town's B17001_002 from acs5_2020_2024_b17001_towns_regions.csv through town_geoid_region_basis (the average over January 2020 to December 2024, per the table notes) and divided it by the town's mean recipients over 2020 to 2024: the ratio runs from 0.87 to 3.13.
4. Estimated each town's residents in poverty in 2020, 2021 and 2022 as its mean recipients that year times its ratio, divided each former county's estimate among its towns in proportion to those figures and summed the towns' parts into regions (rule 2.2), then averaged each region's five years with equal weight (rule 2.3): the averages sum to 240,800.
5. Read rof_client_services_extract_20260930.csv counting Wexmoor's April 2026 upload once (the extract holds it twice), kept service dates from July 1, 2025 to June 30, 2026, matched Corbin's pre-2026 client numbers to its new ones through cca_client_number_conversion_20260101.csv, and placed each client in the town given by the town edits in rof_gds_profile_audit_fy2026.csv for the service date (effective_date), since each row carries its record's town when the extract was cut; counted distinct people per agency and region and shared each agency's Unexpended balance in rof_fy2026_closeout.xlsx by those counts (rule 3.1): $549,981 in all.
6. Counted each energy assistance (EA) payment once per household_no and service_date, since the extract repeats it on the row of every household member, in the town the audit trail gives for the payment date (rule 3.2).
7. Split $12,000,000 in proportion to the unrounded averages and rounded each allocation to the nearest $10,000 (rule 2.4): Greater Ormsby $1,650,000, Mill River Valley $2,250,000, Tarrow Uplands $330,000, Southern Shore $720,000, Wexport Harbor $2,140,000, Two Rivers $1,860,000, Northern Hills $330,000, Quinnet Valley $1,380,000 and Eastern Bays $1,340,000.

## 4. Deliverable Answers

### rof_fy2027_region_poverty.csv

1. Residents in poverty by planning region, nearest hundred, in the file's order:
   - Greater Ormsby: 2020 35,900; 2021 34,300; 2022 31,600; 2020-2024 average 33,100
   - Mill River Valley: 2020 41,600; 2021 44,000; 2022 46,800; 2020-2024 average 45,100
   - Tarrow Uplands: 2020 6,700; 2021 6,700; 2022 6,700; 2020-2024 average 6,600
   - Southern Shore: 2020 12,600; 2021 13,300; 2022 14,600; 2020-2024 average 14,500
   - Wexport Harbor: 2020 44,000; 2021 44,000; 2022 42,800; 2020-2024 average 42,900
   - Two Rivers: 2020 35,800; 2021 36,700; 2022 37,900; 2020-2024 average 37,400
   - Northern Hills: 2020 6,800; 2021 6,700; 2022 6,700; 2020-2024 average 6,700
   - Quinnet Valley: 2020 27,600; 2021 27,600; 2022 27,400; 2020-2024 average 27,600
   - Eastern Bays: 2020 26,600; 2021 26,900; 2022 27,000; 2020-2024 average 26,900

### rof_fy2027_allocation_memo.docx

1. FY2027 allocations, nearest $10,000:
   - Greater Ormsby Council of Governments: $1,650,000
   - Mill River Valley Council of Governments: $2,250,000
   - Tarrow Uplands Council of Governments: $330,000
   - Southern Shore Council of Governments: $720,000
   - Wexport Harbor Council of Governments: $2,140,000
   - Two Rivers Council of Governments: $1,860,000
   - Northern Hills Council of Governments: $330,000
   - Quinnet Valley Council of Governments: $1,380,000
   - Eastern Bays Council of Governments: $1,340,000
2. Bar chart of the nine FY2027 allocations, one bar per council with its amount, below the allocation table.
3. Each council's share of the former county agencies' unexpended FY2026 balances, nearest $100:
   - Greater Ormsby Council of Governments: $68,600
   - Mill River Valley Council of Governments: $98,700
   - Tarrow Uplands Council of Governments: $16,300
   - Southern Shore Council of Governments: $39,600
   - Wexport Harbor Council of Governments: $93,200
   - Two Rivers Council of Governments: $90,000
   - Northern Hills Council of Governments: $18,400
   - Quinnet Valley Council of Governments: $52,700
   - Eastern Bays Council of Governments: $72,500
4. People each share is counted on:
   - Greater Ormsby Council of Governments: 4,080
   - Mill River Valley Council of Governments: 5,677
   - Tarrow Uplands Council of Governments: 802
   - Southern Shore Council of Governments: 2,126
   - Wexport Harbor Council of Governments: 5,210
   - Two Rivers Council of Governments: 5,017
   - Northern Hills Council of Governments: 920
   - Quinnet Valley Council of Governments: 3,934
   - Eastern Bays Council of Governments: 3,237
5. Energy assistance the agencies paid in FY2026 to households in each council's towns, nearest $100:
   - Greater Ormsby Council of Governments: $505,600
   - Mill River Valley Council of Governments: $679,700
   - Tarrow Uplands Council of Governments: $92,200
   - Southern Shore Council of Governments: $262,600
   - Wexport Harbor Council of Governments: $644,800
   - Two Rivers Council of Governments: $685,700
   - Northern Hills Council of Governments: $105,900
   - Quinnet Valley Council of Governments: $487,100
   - Eastern Bays Council of Governments: $439,100
