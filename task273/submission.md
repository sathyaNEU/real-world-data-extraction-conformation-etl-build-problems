## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**The programme should cover four of the seven uses: taxicabs, ride-hail, parcel delivery and app-based delivery.**
Their drivers caused crashes at 1.7 to 2.1 times private drivers' rate per mile, parcel delivery nearest the line at 1.7, while paratransit, airport shuttles and limousines all stay under 1.3. Not airport shuttles and paratransit, which the struck vehicles' share of the whole five years puts over the line: their miles run on freeways and in daylight, where crashes per mile are rare, so too few of them are struck for the miles they drive. Not a count of vehicles registered or permitted, which covers six uses because a commercial vehicle drives several times a private car's miles. Not road class or hour alone, each of which leaves ride-hail or both delivery uses under the line.

## 2. Critical Components

1. Crashes caused between moving vehicles, 2021 to 2025: taxicabs **1,564**; ride-hail **6,762**; limousines **558**; airport shuttles **648**; paratransit **865**; parcel delivery **3,317**; app-based delivery **3,282**; private drivers **91,211**.
2. The Department's miles for the five years: **60,420** million on the region's roads, in **288** road class, day type and hour strata.
3. Each use's miles come from the **134,224** vehicles that at-fault drivers struck in crashes with one driver at fault, each stratum's miles shared in proportion to them.
4. Parcel delivery, the nearest use above the line, at **1.7** times private drivers' rate; paratransit, airport shuttles and limousines all under **1.3**.

## 3. Step-by-Step Solution

1. From crash_extract_2021_2025_crashes.csv and crash_extract_2021_2025_units.csv, kept the crashes with two or more vehicles in transport (the coverage rule's crashes): 124,753 crashes.
2. Took each crash's at-fault drivers from the 2023 form's AT_FAULT_UNIT and the 2016 form's contributing circumstance, gave each 2016 vehicle for hire or delivery the use of the operator named on the report (commission_operator_register_2026.xlsx), and left out drivers who fled unidentified, as the rule says: private drivers caused 91,211 crashes.
3. Placed each crash in its road class (2016 crashes by legacy route and milepost through lrs_road_inventory_2025.xlsx), day type and Pacific hour (State Patrol times converted from UTC): 288 strata.
4. Gave each stratum the Department's miles: its road class's 2021 to 2025 VMT (travel_monitoring_report_2025.pdf, Table 1) times the class's share of its count stations' 2025 traffic in that day type and hour (ccs_hourly_volumes_2025.csv): 60,420 million miles in all.
5. Shared each stratum's miles among the uses in proportion to the vehicles struck there by the one at-fault driver of a crash: 134,224 vehicles struck.
6. Divided each use's crashes caused by its miles and set the rate against private drivers': taxicabs, ride-hail, parcel delivery and app-based delivery at 1.9, 2.1, 1.7 and 2.0 times; paratransit, airport shuttles and limousines under 1.3.
7. For the asks, read crash_extract_2021_2025_persons_injury_crashes.csv one person once (a person listed again in the same seat of the same unit taken at the later record), with deaths from road_fatality_register_2021_2025.csv, over every crash of any kind a use's driver caused, and costed each crash once at its most severe final injury (dot_crash_unit_costs_2025.pdf): ride-hail 402 people and USD 1,979.6 million.
8. Recommended covering taxicabs, ride-hail, parcel delivery and app-based delivery.

## 4. Deliverable Answers

### fleet_safety_programme_2027.xlsx

1. The coverage test, every use:
   - Taxicabs: covered
   - Ride-hail: covered
   - Limousines: not covered
   - Airport shuttles: not covered
   - Paratransit: not covered
   - Parcel delivery: covered
   - App-based delivery: covered
2. People killed or seriously injured in all the crashes each use's drivers caused, 2021 to 2025 (whole people):
   - Taxicabs: 74
   - Ride-hail: 402
   - Limousines: 45
   - Airport shuttles: 63
   - Paratransit: 55
   - Parcel delivery: 109
   - App-based delivery: 136
3. Cost of those crashes at the Department's crash unit costs (millions of dollars, one decimal):
   - Taxicabs: 505.9
   - Ride-hail: 1,979.6
   - Limousines: 242.4
   - Airport shuttles: 299.5
   - Paratransit: 279.5
   - Parcel delivery: 641.9
   - App-based delivery: 699.9

### fleet_safety_programme_2027.pptx

1. One chart of each use's rate per mile of causing crashes against private drivers' rate with the line at 1.5, the four covered uses above it and highlighted (slide 2).
