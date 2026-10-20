## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: an on-road NOx inventory by roadway link, each link's vehicle-miles by class expanded from short classification counts with continuous count station factors).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Designate three of the fourteen port roadway links for the 2027 Air Corridor Program: L03, L05 and L14.**
Each carried 5.00 tonnes or more of on-road NOx per mile from October 2025 to September 2026. Every link's two-weekday count is expanded to the year class by class with the classifying stations' factors, except the combination trucks on the three terminal access roads (L01, L06 and L14), which are the terminals' own drays and follow the vessel calls: each count is carried to the year by its terminal's gate record, the terminal's average daily trucks over the year against its trucks on the count days. Expanded with the stations' factors, a road counted in a busy week or a quiet one keeps that week's level, and the designation would be L01, L03, L05 and L06.

## 2. Critical Components

1. Links at or above 5.00 tonnes of NOx per mile: **3** of 14.

## 3. Step-by-Step Solution

1. Took every link in port_roadway_links_2026.xlsx (rule 2.1) and its two count days, both directions, from the programme and site the register names: dot_short_counts_fy2026.csv (hourly), county_traffic_counts_2025_2026.xlsx (15-minute sheets, one per site) and terminal_access_counts_2026.csv (hourly by lane), as passenger (1-3), single-unit (4-7) and combination (8-13) daily totals.
2. From ccs_hourly_volumes_oct2025_sep2026.csv, each classifying station in count_station_register_2026.xlsx, both directions summed by date and class group, days with no record left out.
3. For each class group, each classifying station's factor for each month and day of week: its average daily volume over the year divided by its average volume on that month's days of that weekday; the group's factor the average over the four classifying stations.
4. Each link's annual average daily volume for each class group: the mean over its two count days of the day's count times the class group's factor for that day's month and weekday; for the combination trucks on the links port_roadway_links_2026.xlsx names as terminal access roads, the mean over the count days of the day's count times the terminal's average daily trucks_in over the 365 days in terminal_daily_gate_report_fy2026.csv over its trucks_in that day.
5. NOx per mile: each class group's annual average daily volume times 365 days times its rate in onroad_nox_emission_rates_2026.csv, summed over the groups, in tonnes (rule 2.2); designated every link at 5.00 or more (rule 2.3): L03, L05 and L14.
6. For the fleet sizing (rule 3.1), from drayage_truck_registry_2026.csv: on each quarter's last day, the registrations in force (registered_from on or before the day, registered_to blank or on or after it), one truck per vin (an O or I, which a VIN never holds, read as 0 or 1) at its latest registration; each truck's engine model year read from its engine_family in heavy_duty_engine_certifications.xlsx (model_year is the truck's own); counted, with those whose engines are of model year 2009 or older, by quarter and, on 30 September 2026, by motor carrier.

## 4. Deliverable Answers

### air_corridor_links_2027.xlsx

1. The designated links: L03, L05 and L14 (three of fourteen).
2. Drayage trucks registered on each quarter's last day, and those with engines of model year 2009 or older:
   - 31 December 2025: 2,290 trucks; 379 of model year 2009 or older
   - 31 March 2026: 2,333 trucks; 385 of model year 2009 or older
   - 30 June 2026: 2,369 trucks; 392 of model year 2009 or older
   - 30 September 2026: 2,423 trucks; 405 of model year 2009 or older
3. On 30 September 2026, by motor carrier:
   - Atlantic Port Services: 229 trucks; 39 of model year 2009 or older
   - Bay Freight Co: 259 trucks; 49 of model year 2009 or older
   - Coastal Haul LLC: 304 trucks; 42 of model year 2009 or older
   - Harborline Drayage: 413 trucks; 74 of model year 2009 or older
   - Northpoint Logistics: 275 trucks; 48 of model year 2009 or older
   - Rivera Trucking: 237 trucks; 45 of model year 2009 or older
   - Seaboard Intermodal: 323 trucks; 54 of model year 2009 or older
   - Tri-County Cartage: 383 trucks; 54 of model year 2009 or older

### air_corridor_designations_2027.pdf

1. The designated links: L03, L05 and L14.
2. Bar chart of every link's on-road NOx per mile, October 2025 to September 2026, against the 5.00 tonne line, the designated links' bars in orange.
