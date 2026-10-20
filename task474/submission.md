## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: an on-road NOx inventory by roadway link, each link's vehicle-miles by class expanded from short classification counts with continuous count station factors).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Designate four of the fourteen port roadway links for the 2027 Air Corridor Program: L01, L03, L05 and L14.**
Each carried 5.00 tonnes or more of on-road NOx per mile from October 2025 to September 2026 once each link's two-weekday count is expanded to the year class by class: trucks with the monthly and day-of-week factors the classifying stations measure for trucks, cars with those for cars. Trucks run well above their annual average on weekdays and are nearly flat by season, so expanding a weekday count with all-vehicle factors and splitting it by the counted truck share carries too many trucks into the year and designates L01, L03, L04, L05, L06, L09, L10, L11, L13 and L14.

## 2. Critical Components

1. Links at or above 5.00 tonnes of NOx per mile: **4** of 14.

## 3. Step-by-Step Solution

1. Took every link in port_roadway_links_2026.xlsx (rule 2.1) and its two count days, both directions, from the programme and site the register names: dot_short_counts_fy2026.csv (hourly), county_traffic_counts_2025_2026.xlsx (15-minute sheets, one per site) and terminal_access_counts_2026.csv (hourly by lane), as passenger (1-3), single-unit (4-7) and combination (8-13) daily totals.
2. From ccs_hourly_volumes_oct2025_sep2026.csv, each classifying station in count_station_register_2026.xlsx, both directions summed by date and class group, days with no record left out.
3. For each class group, each classifying station's factor for each month and day of week: its average daily volume over the year divided by its average volume on that month's days of that weekday; the group's factor the average over the four classifying stations.
4. Each link's annual average daily volume for each class group: the mean over its two count days of the day's count times the class group's factor for that day's month and weekday.
5. NOx per mile: each class group's annual average daily volume times 365 days times its rate in onroad_nox_emission_rates_2026.csv, summed over the groups, in tonnes (rule 2.2); designated every link at 5.00 or more (rule 2.3): L01, L03, L05 and L14.
6. For the terminal operations review (rule 3.1), from terminal_gate_transactions_oct2025_sep2026.csv: Berth 20's gate_in moved an hour later in the daylight-time months (its in-gate keeps standard time, its out-gate local time); at Pacific Gateway a transaction sharing its container_no and gate_in with a later transaction_id under another tag is the voided first keying and is dropped; at Berth 40 a leg out through the rail ramp gate (out_lane RG1) and the tag's next leg in through it (in_lane RG1) are one stay; then each tag's overlapping transactions at a terminal merged into one visit from its first gate_in to its last gate_out, and visits counted and turn minutes averaged by terminal and the quarter of the gate_in date.

## 4. Deliverable Answers

### air_corridor_links_2027.xlsx

1. Every link, designated or not:
   - L01: designated
   - L02: not designated
   - L03: designated
   - L04: not designated
   - L05: designated
   - L06: not designated
   - L07: not designated
   - L08: not designated
   - L09: not designated
   - L10: not designated
   - L11: not designated
   - L12: not designated
   - L13: not designated
   - L14: designated
2. Every terminal and quarter: truck visits and average turn time (minutes, one decimal):
   - Berth 20 Container Terminal, Oct-Dec 2025: 9,790 visits; 69.1 minutes
   - Berth 20 Container Terminal, Jan-Mar 2026: 9,687 visits; 67.4 minutes
   - Berth 20 Container Terminal, Apr-Jun 2026: 9,601 visits; 65.4 minutes
   - Berth 20 Container Terminal, Jul-Sep 2026: 9,998 visits; 62.8 minutes
   - Pacific Gateway Terminal (Berths 30 to 34), Oct-Dec 2025: 7,799 visits; 84.8 minutes
   - Pacific Gateway Terminal (Berths 30 to 34), Jan-Mar 2026: 7,382 visits; 91.9 minutes
   - Pacific Gateway Terminal (Berths 30 to 34), Apr-Jun 2026: 7,509 visits; 99.1 minutes
   - Pacific Gateway Terminal (Berths 30 to 34), Jul-Sep 2026: 7,553 visits; 104.5 minutes
   - Berth 40 Intermodal Terminal, Oct-Dec 2025: 5,186 visits; 61.5 minutes
   - Berth 40 Intermodal Terminal, Jan-Mar 2026: 4,906 visits; 59.8 minutes
   - Berth 40 Intermodal Terminal, Apr-Jun 2026: 5,012 visits; 58.2 minutes
   - Berth 40 Intermodal Terminal, Jul-Sep 2026: 5,117 visits; 56.1 minutes

### air_corridor_designations_2027.pdf

1. The designated links: L01, L03, L05 and L14.
2. Bar chart of every link's on-road NOx per mile, October 2025 to September 2026, against the 5.00 tonne line, the designated links' bars in orange.
