# task183 submission

## Tags

**Domain:** Energy Systems & Utilities, grid reliability and outage analysis (underground distribution cable failures and feeder reliability indices).
**Analytical objective:** Anomaly Detection & Diagnostics (which feeder's cable is in a failing condition that its recent failure count does not show).

## 1. Final Recommendation

**Quarry Hill 21 will have the most failures of the cable itself in 2027, so it is the feeder for the 2027 cable program.**

Quarry Hill 21 is the only feeder with in-service sections that have already failed twice or more (17 sections, all spliced in place under State Route 443), and a section in that state fails again many times as often as one with a single failure. Not Mill Lane 7, which leads the five-year failure count but on first failures of different sections, which seldom fail again, from a run that has eased since 2022. Not Sutter Park 5, which leads on its last two years and on failure rates by insulation and age, but whose recent failures are mostly on the Kessler Avenue loop, over its rating from the warehouse park's expansion until the loop's second feed was energised in September, before the data cut (the annual report and the extract notes). Not Harrow Road 12, which leads only when its removed paper cable is counted.

## 2. Critical Components

1. Cable failures are the INS, SPL and TRM work orders, counted on the sections with status IS in the GIS export of 30 September 2026
2. Quarry Hill 21 has **17** in-service sections with two or more cable failures; every other feeder has **none**
3. Across every section year since January 2012, a section with two failures fails again at **more than ten times** the yearly rate of a section with one
4. Each in-service section carried forward at the rate for its own count of failures puts Quarry Hill 21 **first** in expected 2027 failures

## 3. Step-by-Step Solution

1. Kept the INS, SPL and TRM orders in `ug_cable_fault_work_orders_2012_2026.csv` (codes in `wo_cause_repair_codes.csv`) and joined them to `gis_ug_primary_sections_20260930.xlsx` on `section_id`.
2. Ordered each section's failures by fault date and split its time in service from January 2012 (or installation) to retirement or 30 September 2026 at each failure, so every section year sits under the failures the section had already had.
3. Estimated the failure rate per section year for none, one, two and three or more prior failures: the rate after two failures is more than ten times the rate after one.
4. Counted the in-service sections by feeder and prior failures: only Quarry Hill 21 has sections at two or more, the rest were replaced at their second failure.
5. Summed each in-service section's rate by feeder (the June 2026 lateral on Mill Lane 7, as the register states) for the expected failures of calendar 2027: Quarry Hill 21 is first under every rate split tried (by count alone, with insulation and age, or as a Poisson model), with the Kessler Avenue loop's overload ended by its second feed.
6. Recommendation: Quarry Hill 21 for the 2027 program.
7. For the reliability figures, timed each customer's interruption to its own restoration step (`oms_restoration_steps_2020-10_2026-09.csv`, ADMS times converted from UTC) through the dated rows of `connectivity_meter_points.parquet` and `feeder_device_list.json`, counting a substation outage once per customer rather than at the export's repeated totals.
8. Applied TVE-RS-04: sustained over five minutes, major event days 2026-01-25, 2026-07-28 by the 2.5 beta method (left out of SAIFI and SAIDI, kept in the four-or-more count), customers served from the connectivity model on 30 September 2026.

## 4. Deliverable Answers

### cable_program_2027.xlsx
1. Feeder for the 2027 program: Quarry Hill 21
2. Sustained interruptions per customer served (SAIFI), October 2025 to September 2026, major event days out:
   - Harrow Road 12: 1.40
   - Harrow Road 14: 1.97
   - Mill Lane 3: 1.73
   - Mill Lane 7: 1.31
   - Quarry Hill 21: 1.58
   - Quarry Hill 22: 1.52
   - Sutter Park 5: 2.23
   - Sutter Park 9: 1.53
3. Customer minutes of sustained interruption per customer served (SAIDI), October 2025 to September 2026, major event days out:
   - Harrow Road 12: 71.3
   - Harrow Road 14: 131.4
   - Mill Lane 3: 88.2
   - Mill Lane 7: 85.7
   - Quarry Hill 21: 92.4
   - Quarry Hill 22: 73.5
   - Sutter Park 5: 139.7
   - Sutter Park 9: 125.5
4. Customers with four or more sustained interruptions, October 2025 to September 2026:
   - Harrow Road 12: 108
   - Harrow Road 14: 1,163
   - Mill Lane 3: 445
   - Mill Lane 7: 485
   - Quarry Hill 21: 262
   - Quarry Hill 22: 44
   - Sutter Park 5: 1,812
   - Sutter Park 9: 65

### feeder_failures_2027.png
1. Bar chart of expected 2027 cable failures for all eight feeders, Quarry Hill 21 the tallest bar and highlighted.
