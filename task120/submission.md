# task120: the campus water system's added well capacity for 2027

## Tags

**Domain:** Energy Systems & Utilities (generation capacity planning: a campus water system's firm well capacity against its maximum-day demand).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**The university has to add 184 gpm of firm well capacity to its campus water system before June 2027.**

The campus used 4,469,527 gallons on August 20, 2026, 3,103.8 gpm against a firm capacity of 2,920 gpm with Well 1, the largest, out of service. Not none, which takes each day's well production as the water used: the largest production day, August 21, 2026, is the day the wells refilled the tanks, and on August 20 the four tanks gave up 752,881 gallons the wells never pumped. Not a smaller addition from the main zone's two tanks alone or from the historian's UTC days: the hill zone's tanks gave up water the same day, and the state's day runs midnight to midnight, Eastern time.

## 2. Critical Components

1. The day the campus used the most water: **August 20, 2026**
2. The water used on it: **4,469,527 gallons** (3,103.8 gpm)
3. The wells' firm capacity: **2,920 gpm**

## 3. Step-by-Step Solution

1. Differenced each well's midnight totalizers in water_operators_daily_log_2025-10_2026-10.xlsx (Well 3's register rolls over after 99,999,999) for each of the 365 calendar days from October 1, 2025 to September 30, 2026: the wells produced 3,716,646 gallons on August 20, 2026.
2. Took the four tanks' levels at each Eastern midnight from scada_historian_export_2025-10-01_2026-10-01.csv (UTC, per scada_export_readme.txt) at each tank's gallons per foot of level in campus_water_system_facilities_summary_2026.docx: on August 20 the tanks gave up 752,881 gallons.
3. Balanced the whole system over each Eastern calendar day the letter sets, since the wells pump into the tanks and not into the buildings: water used is the day's production less what the four tanks gained (plus what they gave up), and the most was 4,469,527 gallons on August 20, 2026.
4. Took each well's most recent pump test in well_pump_tests_2021-2026.xlsx (1,090, 820, 760, 700 and 640 gpm) less Well 1, the largest, per the letter's firm capacity: 2,920 gpm.
5. Took each month's water used the same way, less the water its buildings' service meters recorded (amr_monthend_reads_2025-10_2026-10.csv, the vault meters' logged reads in cmms_water_work_orders_2025-10-01_2026-10-09.csv, multipliers and change-out reads from meter_inventory_2026-10-08.xlsx; the meters inside a building beyond its service lines in service_line_inventory_2024-10-15.csv not counted twice): 125,629,212 gallons lost, 12.3% of the 1,021,278,949 gallons used.
6. Summed each service meter's year by its building's primary use in space_inventory_buildings_2026-09-30.xlsx, the Science Annex's meter under building 47 taken from the removed-buildings sheet: the residence halls used 280,319,280 gallons.
7. Divided 4,469,527 gallons by 1,440 minutes: 3,103.8 gpm, 183.84 gpm above firm capacity, so the university adds 184 gpm before June 1, 2027.

## 4. Deliverable Answers

### campus_water_capacity_2027.xlsx

1. Well capacity to add before June 2027: 184 gpm
2. The day: August 20, 2026
3. The water used on it: 4,469,527 gallons
4. The wells' firm capacity: 2,920 gpm

### sanitary_survey_response_2026.docx

1. The water the system lost in each month, whole gallons:
   - October 2025: 9,249,728
   - November 2025: 8,692,700
   - December 2025: 8,985,071
   - January 2026: 9,346,726
   - February 2026: 8,267,450
   - March 2026: 9,031,386
   - April 2026: 9,488,916
   - May 2026: 10,095,785
   - June 2026: 12,119,389
   - July 2026: 15,036,717
   - August 2026: 14,447,009
   - September 2026: 10,868,335
2. The water the system lost over the year: 125,629,212 gallons
3. The year's water loss percentage: 12.3%
4. Bar chart under the water audit: one bar per month, October 2025 to September 2026 in order, each labelled with its gallons lost, on a gallons axis, titled with the year's loss and its share.
5. The water each group used over the year, whole gallons:
   - Residence halls: 280,319,280
   - Academic and research buildings: 366,798,732
   - Athletics facilities: 36,193,200
   - Central energy plant: 87,422,200
