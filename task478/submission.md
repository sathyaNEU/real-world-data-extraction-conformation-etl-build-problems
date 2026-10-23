## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (an air district's 2026 NOx inventory of fourteen facilities' SCR-controlled combustion units, conformed from continuous monitor hours, two source test databases, monthly emission statements and the compliance log, each unmonitored unit's rate carried along the operating hours on its catalyst).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Sign the 2027 NOx reduction agreements with Wexley Point Energy Center, Ashgrove Refining, Valmora Glass Works, Sedge Hollow Landfill Gas and St. Aldric Medical Center.**
Their Rule 4306 units emitted 24, 21, 22, 8 and 8 tons of NOx in 2026, against Lindqvist Paperboard's 7 in sixth. Not Haskett Ridge Compressor Station, whose 8 tons on its latest source tests rest on two engines tested on worn catalysts it replaced in December 2025; along the hours on the new catalysts its units emitted 6. Not Lindqvist Paperboard, which makes the five on the latest tests only because they read Sedge Hollow's and St. Aldric's engines weeks after new catalysts went in.

## 2. Critical Components

1. St. Aldric Medical Center's units emitted **8** tons and Sedge Hollow Landfill Gas's **8**, the lowest two of the five, against Lindqvist Paperboard's **7** in sixth.
2. Haskett Ridge Compressor Station's units emitted **6** tons.

## 3. Step-by-Step Solution

1. Took the 35 Rule 4306 devices in tbapcd_permit_devices.csv, 9 with a CEMS, and summed each monitored device's 2026 nox_mass_lb in tbapcd_cems_hourly_2026.csv, matched by facility_id and unit_id to the permit list's FAC_NO and CEMS_UNIT_ID (guidance section 2): 74 tons.
2. Put every source test of the other 26 units on lb/MMBtu, the 2022 to 2026 database's own column and the 2018 to 2021 database's NOX_LB_HR over FUEL_FLOW_SCFH times FUEL_HHV (guidance section 5): 172 tests.
3. Spread each unit's monthly heat input (guidance section 4) and operating hours in tbapcd_emission_statements_2017_2026.csv evenly over the month's days, and counted each day's operating hours on the catalyst in service since the unit's last SCR INSTALLED or CATALYST date in tbapcd_compliance_events_2017_2026.csv.
4. Fitted the log of each test's lb/MMBtu on its unit's catalyst hours at the start of the test day, one level for each unit and one climb for all: 0.48 in the log for every 10,000 hours, about 5 per cent for every 1,000 hours.
5. Summed each unit's 2026 heat input day by day at the rate its level and the climb give at the day's mid-day catalyst hours, and each facility's units: Wexley Point 24, Valmora 22, Ashgrove 21, St. Aldric 8 and Sedge Hollow 8, then Lindqvist 7 and Haskett Ridge 6.
6. For the gas, matched each line of tvg_commercial_billing_extract_2027-02.csv to its facility by service address and took USAGE_CCF as therms where it equals the read difference times PRESSURE_MULT times BTU_FACTOR (the 126 lines the utility's new billing system issued, read from July 2026 on) and as CCF times BTU_FACTOR where it equals the read difference times PRESSURE_MULT (the earlier lines), then divided by 10 and spread each bill as plan section 4.2 says: 18,290,110 MMBtu in all.
7. For the engines, read the logs of Wexley Point, Sedge Hollow, Lindqvist, Briar Flats, Harrow, Orchard Basin and Penrose, which sum to their engines' hour meter differences in tbapcd_engine_inspections_2025_2027.csv only as hours and minutes, that way (1.30 is an hour and a half), took each run of D-3201, D-3301, D-3501, D-3602, D-3801, D-4001 and D-4403 before its 2026 replacement date at the removed engine's rating and tier in the compliance log's EQUIPMENT entry, and applied guidance section 6: 10,523 lb in all.
8. Recommended the five highest: Wexley Point Energy Center, Ashgrove Refining, Valmora Glass Works, Sedge Hollow Landfill Gas and St. Aldric Medical Center.

## 4. Deliverable Answers

### tbapcd_cerp_facilities_2027.xlsx

1. The five facilities for the 2027 NOx reduction agreements: Wexley Point Energy Center, Ashgrove Refining, Valmora Glass Works, Sedge Hollow Landfill Gas and St. Aldric Medical Center.
2. Each facility's 2026 NOx from its Rule 4306 units, whole tons:
   - Wexley Point Energy Center: 24
   - Ashgrove Refining: 21
   - Valmora Glass Works: 22
   - Sedge Hollow Landfill Gas: 8
   - Haskett Ridge Compressor Station: 6
   - St. Aldric Medical Center: 8
   - Lindqvist Paperboard: 7
   - Tamsett State University: 4
   - Briar Flats Water Reclamation: 3
   - Merriwell Foods: 3
   - Harrow Peaking Station: 2
   - Orchard Basin Almond Growers: 1
   - Penrose Tire Retreading: 1
   - Quarry Lane Data Center: 1
3. Natural gas Tamsett Valley Gas delivered to each facility in calendar 2026, whole MMBtu:
   - Wexley Point Energy Center: 6,389,903
   - Ashgrove Refining: 4,715,504
   - Valmora Glass Works: 1,486,386
   - Sedge Hollow Landfill Gas: 3,909
   - Haskett Ridge Compressor Station: 498,762
   - St. Aldric Medical Center: 597,323
   - Lindqvist Paperboard: 2,306,679
   - Tamsett State University: 1,000,112
   - Briar Flats Water Reclamation: 3,043
   - Merriwell Foods: 629,912
   - Harrow Peaking Station: 213,011
   - Orchard Basin Almond Growers: 169,003
   - Penrose Tire Retreading: 180,590
   - Quarry Lane Data Center: 95,973
4. NOx each facility's emergency standby engines emitted in 2026, whole pounds:
   - Wexley Point Energy Center: 474
   - Ashgrove Refining: 523
   - Valmora Glass Works: 273
   - Sedge Hollow Landfill Gas: 91
   - Haskett Ridge Compressor Station: 182
   - St. Aldric Medical Center: 2,254
   - Lindqvist Paperboard: 349
   - Tamsett State University: 644
   - Briar Flats Water Reclamation: 348
   - Merriwell Foods: 111
   - Harrow Peaking Station: 89
   - Orchard Basin Almond Growers: 143
   - Penrose Tire Retreading: 90
   - Quarry Lane Data Center: 4,954

### tbapcd_nox_inventory_2026.csv

5. Fourteen rows in Appendix A order, each with the facility number, the facility and its tons as in item 2.

### tbapcd_facility_nox_2026.svg

6. Horizontal bar chart of the fourteen facilities' 2026 NOx from their Rule 4306 units, highest first, each bar labelled with its whole tons, the five agreement facilities in blue and the others in grey.
