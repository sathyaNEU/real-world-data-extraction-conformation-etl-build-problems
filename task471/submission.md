## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality: each region's adults on census day estimated from the 2025 Census and its Post-Enumeration Survey by dual-system estimation within the survey's cells, the men aged 18 to 49 brought to the sex ratio that demographic analysis of births, deaths and long-term movements gives, and conformed with the roll at census day and the roll's transaction log into the Commission's enrolment-gap file).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Ardenmere 27, Merriton 20, Westerby 25, Larchfield 26, Glenwhite 29, Hawksridge 5, Fairholme 11, Eastwold 12, Corran Valley 7, Drumlea 5, Orrinvale 4, Inchgarry 8, Strathmuir 6, Rowanlea 3, Kilraven 8 and Nethermoor 4 of the 200 organisers.**
Each region's share is its adults usually resident on census day less its electors with a residential address, the adults estimated by dual-system estimation within the survey's cells with the men aged 18 to 49 raised to the sex ratio demographic analysis gives, because the census and its survey miss the same young men and leave the men's estimates about 4 per cent short of it while the women's agree. Not the dual-system estimates as they stand, which give Ardenmere 26, Westerby 26, Larchfield 28, Glenwhite 31, Hawksridge 4, Corran Valley 6, Drumlea 4 and Nethermoor 3; not the census counts, which leave out everyone the census missed and change 14 regions.

## 2. Critical Components

1. Electors on the roll at the close of census day with a residential address: **3,329,031**.
2. Adults on census day by dual-system estimation within the survey's region, sex and age-group cells: **3,593,178**.
3. Men per woman aged 18 to 24, 25 to 34 and 35 to 49: dual-system estimates **1.01, 0.99 and 0.97**; demographic analysis **1.04, 1.03 and 1.02**.
4. Dual-system estimates of men aged 18 to 49 against demographic analysis: about **4 per cent** short, the women's agreeing with it.
5. Adults on census day after the correction: about **3.63 million**.

## 3. Step-by-Step Solution

1. Took the electors with a residential address (ADDRESS_TYPE R) in roll_at_close_of_census_day_2025.csv to regions through electorates_and_regions.csv (plan 2.2): 3,329,031.
2. In each estimation cell of pes_2025_methods_report.pdf (region by sex by age group) took the count in census_2025_usual_residents_by_region.xlsx less its imputed records, kept the share of the cell's records in pes_2025_census_records.csv with STATUS C and raised that by the cell's people in pes_2025_people.csv over those with MATCH M: dual-system estimates of 3,593,178 adults.
3. Rebuilt the population on census day by sex and single year of age, cohort by cohort, from live_births_by_sex_1925_2025.csv less deaths (deaths_by_year_of_birth_1925_1990.xlsx and deaths_by_year_of_birth_1991_2025.csv) and departures plus arrivals (long_term_movements_by_year_of_birth_1950_2025.csv), the period 2025-01-01/2025-03-03 included: men per woman of 1.04, 1.03 and 1.02 at 18 to 24, 25 to 34 and 35 to 49, against the dual-system estimates' 1.01, 0.99 and 0.97, the women's estimates agreeing with it.
4. Multiplied every region's dual-system estimates of men in each of those age groups by demographic analysis's men per woman over the dual-system estimates' (about 4, 4 and 5 per cent more men), the women and the other ages as estimated: about 3.63 million adults.
5. Subtracted each region's electors and shared the 200 organisers on the differences by largest remainders (plan 3.1; no share falls under two): the organisers above.
6. New electors: read PROCESSED in roll_transactions_2025_2026.csv as the country's time on the old platform (R25- identifiers) and as UTC on the new one from 4 August 2025 (its daily 06:00 transfers of provisional enrolments are stamped 18:00 the day before, 17:00 in daylight saving time), kept the accepted transactions from 5 March 2025 to 30 June 2026 in the country's time, and counted each PERSON_REF whose first such transaction is a NEW at a residential address, so a move on the old platform (a DEL with reason 05 and a NEW the same day) and a re-enrolment after a removal are not new electors: 167,285.
7. Removed because they had died: the accepted DEL rows in the same window with reason 01 on the old platform (deceased, roll_platform_migration_notes.pdf) or 11 or 12 on the new (roll_extract_data_dictionary.xlsx), less those an accepted REI reverses through REF_TXN, by the region of ELECTORATE: 33,225.
8. Wrote enrolment_gap_allocation_2027.csv in the layout of enrolment_gap_file_specification.xlsx and enrolment_gap_allocation_2027.png, a bar chart of each region's organisers.

## 4. Deliverable Answers

### enrolment_gap_allocation_2027.csv

1. Each region's organisers and, between census day and 30 June 2026, the people added to the roll there who had not been on it on census day and the electors removed from it there because they had died, whole numbers:
   - Ardenmere (01): 27 organisers, 23,597 added, 4,706 removed because they had died
   - Merriton (02): 20 organisers, 18,823 added, 3,653 removed because they had died
   - Westerby (03): 25 organisers, 14,943 added, 3,058 removed because they had died
   - Larchfield (04): 26 organisers, 12,952 added, 2,591 removed because they had died
   - Glenwhite (05): 29 organisers, 10,914 added, 2,212 removed because they had died
   - Hawksridge (06): 5 organisers, 11,186 added, 2,246 removed because they had died
   - Fairholme (07): 11 organisers, 9,486 added, 1,789 removed because they had died
   - Eastwold (08): 12 organisers, 9,670 added, 1,901 removed because they had died
   - Corran Valley (09): 7 organisers, 8,901 added, 1,763 removed because they had died
   - Drumlea (10): 5 organisers, 8,457 added, 1,703 removed because they had died
   - Orrinvale (11): 4 organisers, 8,433 added, 1,692 removed because they had died
   - Inchgarry (12): 8 organisers, 6,839 added, 1,335 removed because they had died
   - Strathmuir (13): 6 organisers, 6,014 added, 1,248 removed because they had died
   - Rowanlea (14): 3 organisers, 6,371 added, 1,203 removed because they had died
   - Kilraven (15): 8 organisers, 5,715 added, 1,191 removed because they had died
   - Nethermoor (16): 4 organisers, 4,984 added, 934 removed because they had died

### enrolment_gap_allocation_2027.png

1. Bar chart of the 16 regions' organisers in region code order, each bar labelled with its count.
