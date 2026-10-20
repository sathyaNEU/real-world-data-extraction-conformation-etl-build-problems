## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data: housing unit method population estimates for cities near a revenue-sharing line, conformed from census, permit, ACS, group quarters and utility account records).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Put two of the twelve cities in the 2027 upper tier: Fairhaven and Linden.**
Each has 50,000 residents or more on 1 April 2026 by the housing unit method once the apartment buildings opened since the 2020 census are counted at the occupancy a building of the same age had reached in the utility's account record, not at the city's ACS occupancy rate: new buildings fill over a year or more, so the overall rate counts households not yet there, and on it the tier would be Ashford, Carver Springs, Eastlake, Fairhaven, Harlow, Juniper Falls and Linden.

## 2. Critical Components

1. Cities at 50,000 residents or more on 1 April 2026: **2** of 12.

## 3. Step-by-Step Solution

1. Took the twelve cities, their 2020 housing units and average household size from census_2020_city_housing_base.xlsx (rule 2.1).
2. From the three permit exports (metro_permits_export.csv, county_building_permits.xlsx, civic_permit_records.csv), the buildings with a certificate of occupancy (FinalDate, C of O Date, co_issued_on) from 2020-04-01 to 2026-03-31, by city, classed single-family or multifamily by building_type_code_table.xlsx (an R3 by its units); less the units in demolition_permits_2020_2026.csv finaled in that time (rule 2.2).
3. From nvp_residential_accounts_monthly.csv, the premises whose first bill month is after January 2021 (buildings opened in the record): for each number of months since the first bill, active_residential_accounts over residential_meters summed over the premises (months with five premises or more; beyond them the mean of the last seven).
4. Occupied units on 1 April 2026: the 2020 units less demolitions plus the single-family completions at the city's occupancy in acs_2020_2024_city_occupancy.xlsx (occupied over total housing units); each multifamily building at the step 3 share for its months from its certificate of occupancy month to April 2026.
5. Population: occupied units times the 2020 average household size, plus the residents in group_quarters_survey_2026.csv; every city at 50,000 or more is in the upper tier (rule 2.3): Fairhaven and Linden.
6. For the housing authorized (rule 3.1): the permits issued in 2025 in the three exports, less any whose parcel and project an earlier permit already carried (an expired permit issued again), units summed by city as single-family or multifamily by building_type_code_table.xlsx.

## 4. Deliverable Answers

### city_population_estimates_2026.xlsx

1. The upper-tier cities: Fairhaven and Linden (two of twelve).
2. Housing units authorized by permits first issued in 2025, single-family and multifamily:
   - Ashford: 85 single-family; 319 multifamily
   - Bellmont: 66 single-family; 823 multifamily
   - Carver Springs: 106 single-family; 0 multifamily
   - Dunmore: 57 single-family; 579 multifamily
   - Eastlake: 91 single-family; 305 multifamily
   - Fairhaven: 58 single-family; 196 multifamily
   - Glenridge: 75 single-family; 340 multifamily
   - Harlow: 93 single-family; 392 multifamily
   - Ironwood: 49 single-family; 288 multifamily
   - Juniper Falls: 91 single-family; 227 multifamily
   - Kestrel Bay: 46 single-family; 0 multifamily
   - Linden: 80 single-family; 859 multifamily

### revenue_sharing_tiers_2027.pdf

1. The upper-tier cities: Fairhaven and Linden.
2. Bar chart of every city's population on 1 April 2026 against the 50,000 line, the upper-tier cities' bars in orange.
