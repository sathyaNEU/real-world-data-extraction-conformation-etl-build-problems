## Tags

**Domain:** Urban and regional science (forecasting).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**Widen Tolland Road (CW1): it will be crowded on more days of summer 2027 than any other cycleway, every one of them at Tolland Bridge between 08:00 and 09:00 on a weekday morning, where an average school-term weekday in summer 2026 already carried 625 riders in that hour against a capacity of 650, a flow growing 11 to 14 per cent a year.** Not Estuary Path, which leads only when each counter's 2025 to 2026 growth in total riders is carried forward, a growth the hot, dry summer of 2026 inflated; not Market Street, which leads only when each cycleway's dashboard counter stands for all of its segments; not Brickfields, whose Gasworks Lane crowds on fewer mornings.

## 2. Critical Components

1. Tolland Bridge (CW1-03) is **2.6 m** at its narrowest, a capacity of **650** cyclists an hour both ways (Table 4.3).
2. With each day's rain and maximum temperature held fixed, Tolland Bridge's 08:00 weekday riders grow by **11 to 14 per cent** a year.
3. Tolland Bridge is the only segment of Tolland Road that crowds, and only in the hour from **08:00**.

## 3. Step-by-Step Solution

1. Put counts_summer2024_legacy.csv (local hours, Ch1 plus Ch2) and counts_summer2025_2026.parquet (UTC to Europe/London, in plus out) on each counted segment's local clock hours through counter_register.xlsx, leaving no_data, estimated and blank hours out (policy 3.3).
2. Took each counted segment's capacity from its minimum width in cycleway_path_inventory_2026.xlsx and Table 4.3 4.3 of cycle_design_guide_2023_section4.pdf: Tolland Bridge carries 650 an hour.
3. Fitted, for each counter, each of weekdays and weekends (with bank holidays) and each clock hour, a line of the log of the hour's riders on year, a wet-day flag (1.0 mm or more) and the day's maximum temperature from weather_station_daily_2024-01-01_2026-09-30.csv over the three summers: Tolland Bridge's 08:00 weekday riders grow 11 to 14 per cent a year.
4. Carried every recorded hour of 2024, 2025 and 2026 to 2027 at its own counter, day group and hour's growth, keeping each day's weather and calendar (policy 3.4), and counted the days any counted segment exceeds its capacity in an hour from 06:00 to 22:00: Tolland Road is crowded on the most days, all of them at Tolland Bridge from 08:00.
5. Tolland Road still leads with school-holiday weekdays as a day group of their own or with the hours grouped into periods.
6. Matched count_week_15min_2026-05-11_15.csv (each quarter stamped at its end, in UTC, except CVC-1112 and CVC-1207, on local time from their laptop restarts to the 29 May clock reset in the maintenance log) to the quarter hours in volunteer_count_may2026.xlsx that both recorded, track riders only.
7. Took each dashboard counter's stoppages from counter_maintenance_log_2024-2026.csv by site, leaving out follow-up visits that repeat their job's downtime and counting a contractor job inside the unit's job once, and summed the real time inside 2025.
8. Recommend widening Tolland Road at Tolland Bridge.

## 4. Deliverable Answers

### cycleway_widening_2027.xlsx

1. Cycleway to widen: Tolland Road (CW1).
2. Segment that crowds it: Tolland Bridge (CW1-03).
3. Hours it crowds: 08:00 to 09:00 on weekday mornings.
4. May 2026 volunteer count, riders the counter recorded over the intervals both counted, and the counter's shortfall against the volunteers' track count:
   - Tolland Rd - Cathedral Green (CVC-1104): 3,082 riders, shortfall 2.9 per cent
   - Corn Exchange (CVC-1207): 2,399 riders, shortfall 5.6 per cent
   - Brickfields - Station Sq (CVC-1108): 2,598 riders, shortfall 3.8 per cent
   - Wardle Park - Exchange St (CVC-1116): 2,800 riders, shortfall 4.7 per cent
   - Quayside (CVC-1112): 2,169 riders, shortfall 1.3 per cent
   - Southgate (CVC-1120): 2,057 riders, shortfall 3.5 per cent
5. Dashboard counters in 2025, hours recording nothing and separate stoppages:
   - CVC-1104 (Tolland Rd - Cathedral Green): 49.3 hours, 4 stoppages
   - CVC-1108 (Brickfields - Station Sq): 30.8 hours, 5 stoppages
   - CVC-1112 (Quayside): 57.3 hours, 5 stoppages
   - CVC-1116 (Wardle Park - Exchange St): 38.2 hours, 4 stoppages
   - CVC-1120 (Southgate): 49.6 hours, 5 stoppages
   - CVC-1207 (Corn Exchange): 40.4 hours, 3 stoppages

### widening_note_2027.pdf

1. One-page note to the Transport and Environment Committee recommending Tolland Road (CW1) at Tolland Bridge, 08:00 to 09:00 on weekday mornings, with a bar chart of each cycleway's forecast crowded days.
