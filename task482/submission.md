## Tags

**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution (a city bike-share programme's archive of its operator's station status feed, the operator's trips, fleet moves and rider fault reports, and its pay-station vendor's sales, work orders, register and alarm log, conformed into each station's Schedule C availability and pay-station figures for the fourth quarter of 2026).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**The City names four priority stations for the first quarter of 2027 under Schedule C: W-02 Queen and Albert, W-12 Maple Grove, W-16 Birch Hill and W-19 Willow Crescent, each under 90 per cent availability in October 2026 (88, 88, 86 and 88 per cent).**
The station that cleared the line by the least is W-09 Science Quad, 91 per cent in October, 0.7 points above 90. Not W-16 Birch Hill alone: the status feed counts a docked bike as available until Northlane marks it out of service, and bikes that broke on rides and were docked unreported stayed listed while renters took the bikes around them, so read as the bikes in working order the feed puts W-02 Queen and Albert, W-12 Maple Grove and W-19 Willow Crescent at 91, 92 and 92 per cent in October.

## 2. Critical Components

1. With each docked bike that broke on a ride counted out of working order from the end of that ride until a van took it to the depot, the lowest month of Q4 2026 puts W-02 at **88** per cent, W-12 at **88** per cent, W-16 at **86** per cent and W-19 at **88** per cent.
2. The feed's available bikes taken as the bikes in working order put them at 91, 92, 87 and 92 per cent and name W-16 Birch Hill alone.
3. The nearest station above the line is W-09 Science Quad at **91** per cent in October, **0.7** points clear.

## 3. Step-by-Step Solution

1. Mapped each feed station ID to its City station in wellhaven_bike_share_station_list.xlsx (W-17 Linden Avenue under 117 until its move on the evening of 8 November and 125 after) and read northlane_trips_2026q4.csv once per trip (its week of 16 November is repeated at the end), its times on Eastern time with a trip in the repeated hour of 1 November placed by its duration, and northlane_fleet_moves_2026q4.csv with the WHB- prefix dropped from its bike numbers.
2. Rebuilt every bike's spells docked at a station from the trips (staff rides too, since they moved bikes) and the fleet moves: from a ride's end or a van's drop to the next ride's start or a van's pickup, a bike first recorded leaving a station counted as docked there from the start of the records.
3. Counted a docked bike out of working order from the end of the ride that left it when renters took other bikes from its station while it stood there and a van then took it to the depot, where it stayed a day or more before it was back on the street, and every other docked bike in working order; a bike counted out this way that a full station's surplus or a storage run took decides no minute, since a bike a rider then took was docked beside it.
4. For each station and each minute of service hours (6:00 to midnight Eastern) from October to December 2026, counted the minute available when a bike in working order was docked at its start (Schedule C, C.1), and divided each month's available minutes by its service minutes (C.2).
5. Listed the stations under 90 per cent in a month (C.3): W-02, W-12, W-16 and W-19; the lowest month above the line is W-09's October, 91 per cent.
6. For pay-station sales, kept paystation_sales_2026q4.csv's sales not voided and sold in the fourth quarter on Eastern time, and placed each at the pay station its terminal was in when it was sold, from the terminal replacements in paystation_work_orders_2026q4.xlsx (the export's pay_station column is each terminal's present pay station in paystation_register_2027-01-08.xlsx).
7. For the hours without card payments, ran each COMMS_LOST and READER_FAULT alarm in paystation_alarm_log_2026q4.csv (the register's codes that stop card payments) from its raise to its clear or to the pay station's next restart, after which a fault still present is raised again in the same second, merged overlapping alarms and summed the service hours of October to December.

## 4. Deliverable Answers

### priority_stations_2027q1.xlsx

1. The priority stations for Q1 2027: W-02 Queen and Albert, W-12 Maple Grove, W-16 Birch Hill and W-19 Willow Crescent.
2. Each station's availability in its lowest month of Q4 2026, whole per cent, and whether it is a priority station:
   - W-01 Market Square: 94, not
   - W-02 Queen and Albert: 88, priority
   - W-03 City Hall: 95, not
   - W-04 Wharf Street: 94, not
   - W-05 Courthouse: 91, not
   - W-06 Library Plaza: 96, not
   - W-07 General Hospital: 95, not
   - W-08 University Commons: 95, not
   - W-09 Science Quad: 91, not
   - W-10 Central Station: 97, not
   - W-11 Eastgate Terminal: 97, not
   - W-12 Maple Grove: 88, priority
   - W-13 Elmwood Park: 92, not
   - W-14 Riverbend: 92, not
   - W-15 Cedar Heights: 95, not
   - W-16 Birch Hill: 86, priority
   - W-17 Linden Avenue: 91, not
   - W-18 Orchard Lane: 93, not
   - W-19 Willow Crescent: 88, priority
   - W-20 Ashdale: 95, not
   - W-21 Fernwood: 92, not
   - W-22 Waterfront Trail: 100, not
   - W-23 Pier Park: 100, not
   - W-24 Lighthouse Point: 99, not
3. The station that cleared the line by the least: W-09 Science Quad, 91 per cent in October, 0.7 points above 90.
4. Each station's Q4 2026 pay-station card sales, dollars to the cent:
   - W-01 Market Square: 1,660.25
   - W-02 Queen and Albert: 1,913.00
   - W-03 City Hall: 1,573.50
   - W-04 Wharf Street: 1,516.50
   - W-05 Courthouse: 1,580.50
   - W-06 Library Plaza: 1,630.75
   - W-07 General Hospital: 1,634.50
   - W-08 University Commons: 1,184.50
   - W-09 Science Quad: 854.50
   - W-10 Central Station: 1,994.00
   - W-11 Eastgate Terminal: 1,897.00
   - W-12 Maple Grove: 1,124.25
   - W-13 Elmwood Park: 967.50
   - W-14 Riverbend: 900.25
   - W-15 Cedar Heights: 736.50
   - W-16 Birch Hill: 1,073.00
   - W-17 Linden Avenue: 791.75
   - W-18 Orchard Lane: 746.00
   - W-19 Willow Crescent: 1,098.00
   - W-20 Ashdale: 613.25
   - W-21 Fernwood: 1,127.75
   - W-22 Waterfront Trail: 866.75
   - W-23 Pier Park: 933.75
   - W-24 Lighthouse Point: 1,025.75
5. Each station's Q4 2026 service hours its pay station could not take a card payment, whole hours:
   - W-01 Market Square: 86
   - W-02 Queen and Albert: 6
   - W-03 City Hall: 67
   - W-04 Wharf Street: 87
   - W-05 Courthouse: 71
   - W-06 Library Plaza: 23
   - W-07 General Hospital: 66
   - W-08 University Commons: 66
   - W-09 Science Quad: 47
   - W-10 Central Station: 46
   - W-11 Eastgate Terminal: 10
   - W-12 Maple Grove: 30
   - W-13 Elmwood Park: 36
   - W-14 Riverbend: 53
   - W-15 Cedar Heights: 99
   - W-16 Birch Hill: 51
   - W-17 Linden Avenue: 37
   - W-18 Orchard Lane: 44
   - W-19 Willow Crescent: 105
   - W-20 Ashdale: 52
   - W-21 Fernwood: 78
   - W-22 Waterfront Trail: 55
   - W-23 Pier Park: 6
   - W-24 Lighthouse Point: 67

### station_availability_2026q4.html

6. A horizontal bar chart of the 24 stations' availability in their lowest month of Q4 2026, lowest first, each bar labelled with its whole per cent and its month, a dashed line at 90 per cent, the 4 priority stations in orange and the rest in grey, with each station's monthly figures in a table beneath.
