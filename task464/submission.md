## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Fund the Kestle reconductoring from the 2027/28 losses programme.**
Its replacement conductor would have removed 74.2 MWh of losses in 2025/26, worth GBP 4,800 at GBP 64.80 per MWh, 26.0 MWh more than Copsewell Town at 48.2 MWh, because the Hob Moor Solar Park's export runs back through Kestle's old overhead line to the Kestle Park estate near Copsewell Cross. Not Oxenford Lane, which leads only when every section is charged with the feeder-head current. Not Copsewell Town, whose replaced sections carry its whole load out of the primary but less current than the solar farm's export.

## 2. Critical Components

1. Kestle's project replaces **3.95 km** of route and removes **0.443 ohm** per phase.
2. Kestle's replaced sections would have lost **74.2 MWh** less in 2025/26.
3. Copsewell Town, the runner-up, would have saved **48.2 MWh**.

## 3. Step-by-Step Solution

1. Built each feeder's normal running arrangement from the closed sections in hv_network_model.xlsx and placed every secondary substation (secondary_substations.csv, by site number) and HV customer (hv_connections.csv, by agreement) on its node.
2. Took each substation's half-hourly kW and kVAr from lv_monitoring_2025-26.parquet, as kVA times power factor before its monitor's vendor change, and each HV customer's import less its export from hv_settlement_2025-26.csv, settlement periods placed on the UTC half-hours.
3. Summed the flows of every connection beyond each section the brief lists to get the section's current each half-hour; Kestle's replaced sections carry the solar farm's export less the load beyond them.
4. Took each replaced section's loss at that current on its existing and its replacement conductor, at 11 kV and the resistances of hv_conductor_data_EDS-02-0310.pdf, per the brief: Kestle saves 74.2 MWh and Copsewell Town 48.2 MWh.
5. Valued each project's year at GBP 64.80 per MWh: GBP 4,800 for Kestle.
6. Counted 2025/26 CI and CML per iis_reporting_definitions_2025-26.pdf from interruptions_2023-2026.csv, dropping the work-management LV jobs at sites already off in an HV incident, ending a site's minutes when generator_hire_2025-26.xlsx shows a generator connected there, leaving out sites a generator kept on supply through a planned outage, and dividing by customers_by_substation_2023-2026.csv at 31 March 2026: the feeders' figures below.
7. Funded Kestle, with Copsewell Town the runner-up.

## 4. Deliverable Answers

### losses_programme_2027.xlsx

1. Saving in 2025/26 in MWh to one decimal place, and its value at the losses value to the nearest GBP 100:
   - Copsewell Town: 48.2 MWh, GBP 3,100
   - Ashlade: 7.7 MWh, GBP 500
   - Oxenford Lane: 8.9 MWh, GBP 600
   - Kestle: 74.2 MWh, GBP 4,800
   - Pennick Hill: 19.9 MWh, GBP 1,300
   - Redburn: 22.6 MWh, GBP 1,500
   - Stowmere: 17.5 MWh, GBP 1,100
   - Ingle Road: 4.2 MWh, GBP 300
2. Fund Kestle.
3. Runner-up: Copsewell Town.

### losses_saving_2027.png

1. Bar chart of the eight projects' 2025/26 savings, each bar labelled with its MWh, Kestle highlighted.

### iis_feeders_2025-26.csv

1. 2025/26 customer interruptions per 100 customers and customer minutes lost per customer, one decimal place:
   - Copsewell Town: CI 18.9, CML 45.8
   - Ashlade: CI 138.7, CML 241.9
   - Oxenford Lane: CI 29.4, CML 95.1
   - Kestle: CI 105.1, CML 55.8
   - Pennick Hill: CI 48.8, CML 81.4
   - Redburn: CI 19.1, CML 30.2
   - Stowmere: CI 251.0, CML 168.8
   - Ingle Road: CI 45.5, CML 94.5
