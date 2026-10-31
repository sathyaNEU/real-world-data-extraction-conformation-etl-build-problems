# task480 submission

## Tags

**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (a state data center's 1 July 2026 municipal population estimates by the housing unit method, which set the municipalities in the road aid formula's urban tier for 2027).
**Analytical objective:** Data Extraction & Conformation (ETL) (the assessor's roll, the certificates of occupancy and demolition permits, the 2020 census block groups, the census history and the boundary register, the group quarters survey and the State Registrar's resident birth and death files conformed into each municipality's residents on 1 July 2026, births and deaths).

## 1. Final Recommendation

**Three municipalities reach 10,000 residents on 1 July 2026 and move into the urban tier for the 2027 aid year: the City of Juniper, the City of Dunmore and the Town of Cedar Run.**

Each dwelling standing on 1 July 2026 carries the persons the 2020 block groups show for dwellings of its type and age, and the group quarters add the 2026 survey's residents: on the eight-band profile the Town of Cedar Run holds 10,787 residents and the Town of Maple Ford 9,611, and every other age profile (bands of three to ten years, with or without an age profile of its own for each type of dwelling, or a fitted curve) puts Cedar Run over the line and Maple Ford under it. Not Maple Ford in place of Cedar Run, which each municipality's 2020 persons per dwelling gives (Maple Ford 10,451, Cedar Run 9,735): a dwelling holds fewer people as it ages, so the 2020 average overstates Maple Ford's subdivisions of 1997 to 2015 and understates Cedar Run's homes built since 2019.

## 2. Critical Components

1. On the eight-band age profile of step 2 the Town of Cedar Run's 1 July 2026 estimate is **10,787** residents, over 10,000, and the Town of Maple Ford's **9,611**, under it; every other age profile puts the two on the same sides of the line.
2. Applied to the dwellings standing at the 2010 and 2000 censuses, by the municipalities they stood in then, the age profile reproduces each municipality's household population more closely than its 2020 persons per dwelling does, and far more closely than persons per dwelling by year built; the 2020 persons per dwelling holds Maple Ford at **10,451** and Cedar Run at **9,735** for July 2026.

## 3. Step-by-Step Solution

1. Built the dwelling stock from tamarack_real_property_roll_2026.csv (living units by parcel: a two-family house or an apartment building one parcel, a townhouse unit its own), the certificates of occupancy in certificates_of_occupancy_2020-01_2026-06.csv (each building once, at its first certificate, temporary or final; the dwellings certified in 2026 on lots the roll holds as vacant land added) and the completed permits in demolition_permits_2000-2026.csv (expired permits left standing), each dwelling dated by its first certificate where it has one and otherwise at mid-year of its year built (the assessor's placeholder 0 taken as 1900), and typed in four by the roll's land use (1010 single-family; 1020 two-family and 1030 condominium unit, attached; 1050 apartments; 1080 manufactured homes; a certificate's use the same way).
2. Placed each dwelling standing on 1 April 2020 in its 2020 block group (the first twelve digits of CENSUS_BLOCK_2020) and regressed each block group's household population (P15_001N in census2020_dhc_tamarack_block_groups.csv), by ordinary least squares without an intercept, on its dwellings of each of the four types and its dwellings by age in bands (0 to 5, 5 to 10, 10 to 15, 15 to 20, 20 to 30, 30 to 40, 40 to 60, 60 years and over, the last the base), giving persons per dwelling by type and age.
3. Checked the profile out of sample: on the dwellings standing at each earlier census, by the municipality they stood in then (municipal_boundary_changes_since_2000.csv: the annexations by tax key, the Towns and the Village of Ivydale together), it reproduces the household population in decennial_census_tamarack_municipalities_2000-2020.xlsx (step 2 of the critical components); the 2020 persons per dwelling and persons per dwelling by year built do not.
4. Applied the profile to every dwelling standing on 1 July 2026 at its age that day, by the municipality on the 2026 roll, and added the residents group_quarters_survey_2026.xlsx records for each municipality's facilities.
5. Compared each estimate with 10,000 unrounded (Municipal Road Aid Act, s. 84.21 (6)): Juniper, Dunmore and Cedar Run reach it, every other municipality falls short.
6. Births: kept the records in births_tamarack_residents_2025-2026.csv with a date of birth from 1 July 2025 to 30 June 2026 (each infant one record) and placed each in the municipality (MCD) of the address point in tamarack_address_points_2026-07.csv with the same house number, street and suffix as the residence; RES_CITY is the post office's city (the address points' POSTAL_CITY), not the municipality.
7. Deaths: the same for deaths_tamarack_residents_2025-2026.csv by date of death, a group quarters resident at the facility's address; RES_MCD_CODE follows the written city on deaths before 1 January 2026 and the address after.
8. Recommendation: the City of Juniper, the City of Dunmore and the Town of Cedar Run are in the urban tier for 2027.

## 4. Deliverable Answers

### tamarack_municipal_estimates_2026.xlsx

1. Whether each municipality is in the urban tier for the 2027 aid year:
   - In: City of Dunmore, City of Juniper, Town of Cedar Run
   - Out: Village of Barrow, Village of Fallon, Village of Ivydale, Village of Lorne, Town of Ashgrove, Town of Elk Prairie, Town of Glenmoor, Town of Harwick, Town of Kessler, Town of Maple Ford, Town of Northfield
2. Each municipality's resident births from 1 July 2025 to 30 June 2026, as whole counts, in the workbook's order:
   - City of Dunmore: 111
   - City of Juniper: 98
   - Village of Barrow: 35
   - Village of Fallon: 86
   - Village of Ivydale: 40
   - Village of Lorne: 22
   - Town of Ashgrove: 57
   - Town of Cedar Run: 167
   - Town of Elk Prairie: 18
   - Town of Glenmoor: 64
   - Town of Harwick: 101
   - Town of Kessler: 26
   - Town of Maple Ford: 84
   - Town of Northfield: 69
3. Each municipality's resident deaths from 1 July 2025 to 30 June 2026, as whole counts, in the workbook's order:
   - City of Dunmore: 244
   - City of Juniper: 182
   - Village of Barrow: 104
   - Village of Fallon: 138
   - Village of Ivydale: 51
   - Village of Lorne: 37
   - Town of Ashgrove: 37
   - Town of Cedar Run: 72
   - Town of Elk Prairie: 24
   - Town of Glenmoor: 29
   - Town of Harwick: 40
   - Town of Kessler: 22
   - Town of Maple Ford: 64
   - Town of Northfield: 26

### urban_tier_estimates_2026.svg

4. Bar chart of each municipality's estimated residents on 1 July 2026 against the 10,000 line.
