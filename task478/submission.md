## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (an air district's 2026 NOx inventory of fourteen facilities' boilers and process heaters, conformed from continuous monitor hours, two source test databases, monthly emission statements and the gas utility's heat content, each unmonitored low-NOx burner's tests carried to the heat content of each month's gas).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Sign the 2027 NOx reduction agreements with Ashgrove Refining, Valmora Renewable Fuels, Sedge Hollow Creamery, Lindqvist Paperboard and Merriwell Foods.**
Their Rule 4306 units emitted 26, 8, 8, 12 and 9 tons of NOx in 2026, against Tamsett State University's 7 in sixth. Not Tamsett State University, whose boilers' latest source tests were read in May 2026 on rich Westside gas and overstate a winter fired on lean; Merriwell Foods' latest tests were read in August 2025 on lean gas and understate a canning season fired on 2026's rich summer gas.

## 2. Critical Components

1. A low-NOx burner's rate rises about **6** per cent for each per cent rise in its gas's heat content, from the monitored Lindqvist power boiler's 2026 hours against the Westside heat content.
2. Valmora Renewable Fuels' units emitted **8** tons and Sedge Hollow Creamery's **8**, the lowest two of the five, against Tamsett State University's **7** in sixth.

## 3. Step-by-Step Solution

1. Took the 38 Rule 4306 devices in tbapcd_permit_devices.csv, 4 with a CEMS, and summed each monitored device's 2026 nox_mass_lb in tbapcd_cems_hourly_2026.csv, matched by facility_id and unit_id to the permit list's FAC_NO and CEMS_UNIT_ID (guidance section 2): 32 tons.
2. Put the 248 source tests of the other 34 units on lb/MMBtu, the 2022 to 2026 database's own column and the 2018 to 2021 database's NOX_PPMVD at 3 per cent oxygen through Method 19 (guidance section 5), and took each unit's 2026 monthly heat input from tbapcd_emission_statements_2018_2026.csv, MMSCF at the heat content in tvg_monthly_heat_content_2018_2027.csv for the facility's BTU area and month (guidance section 4).
3. Fitted the log of the Lindqvist power boiler's measured 2026 hourly NOx rate (D-1701, nox_rate_modc 01) on its Westside BTU_FACTOR over 1.035 in the hour's month: about 6 per cent a per cent of heat content, the rise the Westside burners' own tests show against their months' heat content.
4. Carried each unmonitored burner's tests from their months' heat content to 1.035 by that rise, took the unit's level as the geometric mean of its carried tests, and summed each 2026 month's heat input at that level carried to the month's heat content, then each facility's units: Ashgrove 26, Lindqvist 12, Merriwell 9, Valmora 8 and Sedge Hollow 8, then Tamsett State 7 and Haskett Ridge 4.
5. For the gas, matched each line of tvg_commercial_billing_extract_2027-02.csv to its facility by service address, took USAGE_THERMS on the lines whose READ_TO falls before 1 July 2026 as corrected CCF times BTU_FACTOR (read as therms they fall below the plan units' own fuel in the emission statements) and as therms from the July reads, took the usage of the combined-billing accounts 7701-2251, 7702-0864, 7706-0423, 7707-1950 and 7710-2804 once a period, not once a meter, then divided by 10 and spread each bill as plan section 4.2 says: 22,372,114 MMBtu in all.
6. For the engines, read every log in tbapcd_rule4702_engine_logs_2026.xlsx as hours and minutes (0.30 is half an hour: no entry's fraction reaches .60, and the hour meters in tbapcd_engine_inspections_2025_2027.csv bear the reading out), took the emergency lines of the engines run in parallel at Ashgrove, Quarry Lane, St. Aldric and Tamsett State at the outage hours the compliance log's OUTAGE entries record, each run of D-3301 and D-4001 before its 2026 replacement at the removed engine's rating and tier in the EQUIPMENT entry, and applied guidance section 6: 9,943 lb in all.
7. Recommended the five highest: Ashgrove Refining, Valmora Renewable Fuels, Sedge Hollow Creamery, Lindqvist Paperboard and Merriwell Foods.

## 4. Deliverable Answers

### tbapcd_cerp_facilities_2027.xlsx

1. The five facilities for the 2027 NOx reduction agreements: Ashgrove Refining, Valmora Renewable Fuels, Sedge Hollow Creamery, Lindqvist Paperboard and Merriwell Foods.
2. Each facility's 2026 NOx from its Rule 4306 units, whole tons:
   - Wexley Point Energy Center: 0
   - Ashgrove Refining: 26
   - Valmora Renewable Fuels: 8
   - Sedge Hollow Creamery: 8
   - Haskett Ridge Poultry: 4
   - St. Aldric Medical Center: 2
   - Lindqvist Paperboard: 12
   - Tamsett State University: 7
   - Briar Flats Water Reclamation: 1
   - Merriwell Foods: 9
   - Harrow Linen Services: 1
   - Orchard Basin Almond Growers: 1
   - Penrose Tire Retreading: 1
   - Quarry Lane Correctional Facility: 1
3. Natural gas Tamsett Valley Gas delivered to each facility in calendar 2026, whole MMBtu:
   - Wexley Point Energy Center: 62,550
   - Ashgrove Refining: 8,373,008
   - Valmora Renewable Fuels: 2,120,819
   - Sedge Hollow Creamery: 2,044,614
   - Haskett Ridge Poultry: 1,585,709
   - St. Aldric Medical Center: 567,144
   - Lindqvist Paperboard: 3,183,064
   - Tamsett State University: 1,233,721
   - Briar Flats Water Reclamation: 244,409
   - Merriwell Foods: 1,893,296
   - Harrow Linen Services: 292,098
   - Orchard Basin Almond Growers: 238,396
   - Penrose Tire Retreading: 285,822
   - Quarry Lane Correctional Facility: 247,463
4. NOx each facility's emergency standby engines emitted in 2026, whole pounds:
   - Wexley Point Energy Center: 474
   - Ashgrove Refining: 811
   - Valmora Renewable Fuels: 265
   - Sedge Hollow Creamery: 202
   - Haskett Ridge Poultry: 235
   - St. Aldric Medical Center: 2,071
   - Lindqvist Paperboard: 349
   - Tamsett State University: 1,263
   - Briar Flats Water Reclamation: 348
   - Merriwell Foods: 371
   - Harrow Linen Services: 92
   - Orchard Basin Almond Growers: 267
   - Penrose Tire Retreading: 90
   - Quarry Lane Correctional Facility: 3,107

### tbapcd_nox_inventory_2026.csv

5. Fourteen rows in Appendix A order, each with the facility number, the facility and its tons as in item 2.

### tbapcd_facility_nox_2026.svg

6. Horizontal bar chart of the fourteen facilities' 2026 NOx from their Rule 4306 units, highest first, each bar labelled with its whole tons, the five agreement facilities in blue and the others in grey.
