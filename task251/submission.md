## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: each permanent traffic count station's 2027 counting error, a sensitivity and a loss that grows with occupancy in queued traffic).  
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Flag 5 of the 30 stations in the 2027 report and send them to the spring 2028 recalibration: R03-02, R04-03, R05-01, R08-05, R10-03; the other 25 meet the standard.** Each listed station counted more than 6 per cent fewer vehicles than passed it in 2027 once the vehicles its loops lose in queued traffic are counted, and no other station is beyond 4.5 per cent. Not the summer validation list (R03-02, R14-01, R18-01): the filmed days were July and August weekdays with no hour above 8.8 per cent occupancy, so they miss the loss, which the bridges' paired approaches show reaching about one vehicle in five at 40 per cent occupancy; R14-01 and R18-01, at +6 and +8 per cent on their validation days, are inside the band over the year, and R04-03, R05-01, R08-05 and R10-03, inside it on theirs, are beyond it.

## 2. Critical Components

1. Each station and direction's sensitivity from its filmed day: R14-01 and R18-01 at **+6** and **+8 per cent**, and no hour of any filmed day above **8.8 per cent** occupancy.
2. The loops' loss in queued traffic, from each bridge's queued approach against its free one: none in free flow, about **one vehicle in five** at 40 per cent occupancy.
3. The margin: every listed station more than **6 per cent** below the vehicles that passed it, every other station within **4.5 per cent**.

## 3. Step-by-Step Solution

1. Read trafficvault_hourly_counts_2027.csv with each renumbered station's hours joined to its current number (count_station_register.xlsx, Code history), each hour placed in UTC by its offset.
2. Took each station and direction's sensitivity as the loops' count over the video count on its filmed day in Northline_validation_counts_2027.xlsx, sites mapped through the register's validation_site.
3. Paired each bridge's two stations (regional_road_network_2027.xlsx: five bridges, no junction between their stations) and, in each direction and hour, set one less the queued approach's count over the far approach's, each on its validated sensitivity, against the queued approach's occupancy: a loss that grows with occupancy above the free-flow range.
4. Divided every hour's count by its sensitivity ratio and by one less the loss at its occupancy, and took each station's 2027 error as its counted vehicles over the vehicles so estimated, less one, over the hours it counted (TDP-03 section 5): 5 stations beyond 5 per cent.
5. Counted the maintenance visits as the days labour was booked to each station in Carrick_work_orders_2027.xlsx (Labour joined to Orders' stations, one per station and day), less the days at a station then on a TCX-4 (a TCX-2 before its replacement date) whose cabinet door logged nothing that local day in trafficvault_station_events_2027.csv: the controller was reset from the contractor's office; the counts are item 2 below.
6. Counted the power failures as each MAINS_FAIL a TCX-4 logged, once (the log repeats some after a lost poll), and at each TCX-2, which logs nothing and stops, each break in its hourly record, as many as the COMMS_LOST TrafficVault raised inside the break (a feeder that tripped twice) and at least one, leaving out the two controller replacements, quarters by local date; the counts are item 3 below.
7. Flag the 5 stations and send the list for the spring round; the other 25 stay.

## 4. Deliverable Answers

### count_stations_flagged_2027.xlsx

1. The stations whose 2027 count is off by more than 5 per cent, 5 (station, district):
   - R03-02, Ashby
   - R04-03, Kessel
   - R05-01, Kessel
   - R08-05, Kessel
   - R10-03, Marlow
2. Maintenance visits to the stations in 2027, by district and quarter:
   - Ashby: first quarter 3, second 18, third 10, fourth 19
   - Kessel: first quarter 6, second 18, third 1, fourth 19
   - Marlow: first quarter 3, second 10, third 5, fourth 6
3. Power failures at the stations in 2027, by district and quarter:
   - Ashby: first quarter 3, second 2, third 4, fourth 11
   - Kessel: first quarter 12, second 4, third 9, fourth 4
   - Marlow: first quarter 2, second 5, third 4, fourth 4

### count_station_errors_2027.png

4. Each of the 30 stations' 2027 count error against the band from -5 to +5 per cent, the 5 listed stations marked.
