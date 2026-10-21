## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: each permanent traffic count station's 2027 counting error, a sensitivity, a loss that grows with occupancy in queued traffic and the older controllers' miss on cold days).  
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Flag 7 of the 30 stations in the 2027 report and send them to the spring 2028 recalibration: R02-01, R04-03, R06-01, R08-05, R14-01, R25-01 and R29-03; the other 23 meet the standard.** Each listed station counted more than 6 per cent fewer vehicles than passed it in 2027 once the vehicles its loops lose in queued traffic, and on a TCX-2 controller on cold days, are counted, and no other station is beyond 4.5 per cent. Not the summer validation list (R14-01 and R25-01): the filmed days were July and August weekdays with no hour above 8.2 per cent occupancy and no day below 13 degrees. Not the queue loss alone (R02-01, R04-03, R08-05, R14-01 and R25-01), which leaves R06-01 and R29-03 inside the band; not the cold miss alone (R04-03, R06-01, R14-01 and R25-01), which leaves R02-01, R08-05 and R29-03 inside it.

## 2. Critical Components

1. Each station and direction's sensitivity from its filmed day, with no hour of any filmed day above **8.2 per cent** occupancy and no filmed day's mean temperature below **13 degrees**.
2. The loops' loss in queued traffic, from each bridge's queued approach against its free one: none in free flow, **nearly one in five** vehicles at 40 per cent occupancy.
3. The TCX-2 controllers' miss on cold days, from the bridges whose approaches run one controller of each generation: none above about 2 degrees mean temperature, **about one in ten** vehicles at -10 degrees; the TCX-4s miss none (their occupancy per counted vehicle holds flat through the winter while the TCX-2s' climbs).
4. The margin: every listed station more than **6 per cent** below the vehicles that passed it, every other station within **4.5 per cent**.

## 3. Step-by-Step Solution

1. Read trafficvault_hourly_counts_2027.csv with each renumbered station's hours joined to its current number (count_station_register.xlsx, Code history), each hour placed in UTC by its offset, and took each station and direction's sensitivity as the loops' count over the video count on its filmed day in Northline_validation_counts_2027.xlsx, sites mapped through the register's validation_site.
2. Took each day's controller from the register and its Code history (R08-05 and R19-03 ran a TCX-2 before their replacement dates) and each day's mean temperature from weather_daily_2027.csv (Mean Temp, a missing day the mean of the days either side).
3. Paired each bridge's two stations (regional_road_network_2027.xlsx: five bridges, no junction between their stations) and, on the three bridges whose approaches run one controller of each generation, set each free-flowing day's TCX-2 count against the TCX-4 count, each on its validated sensitivity, against the day's mean temperature: a miss on the TCX-2 that grows below about 2 degrees.
4. With that miss taken out, set in each direction and hour one less the queued approach's count over the far approach's, each on its validated sensitivity, against the queued approach's occupancy: a loss that grows with occupancy above the free-flow range.
5. Divided every hour's count by its sensitivity ratio, by one less the loss at its occupancy and, on a TCX-2, by one less the cold miss at the day's temperature, and took each station's 2027 error as its counted vehicles over the vehicles so estimated, less one, over the hours it counted (TDP-03 section 5): 7 stations beyond 5 per cent.
6. Counted the maintenance visits as the days labour was booked to each station in Carrick_work_orders_2027.xlsx (Labour joined to Orders' stations, one per station and day), less the days at a station then on a TCX-4 whose cabinet door logged nothing that local day in trafficvault_station_events_2027.csv: the controller was reset from the contractor's office; the counts are item 2 below.
7. Counted the power failures as each MAINS_FAIL a TCX-4 logged, once (the log repeats some after a lost poll), and at each TCX-2, which logs nothing and stops, each break in its hourly record, as many as the COMMS_LOST TrafficVault raised inside the break (a feeder that tripped twice) and at least one, leaving out the two controller replacements, quarters by local date; the counts are item 3 below.
8. Flag the 7 stations and send the list for the spring round; the other 23 stay.

## 4. Deliverable Answers

### count_stations_flagged_2027.xlsx

1. The stations whose 2027 count is off by more than 5 per cent, 7 (station, district):
   - R02-01, Marlow
   - R04-03, Kessel
   - R06-01, Kessel
   - R08-05, Kessel
   - R14-01, Marlow
   - R25-01, Kessel
   - R29-03, Kessel
2. Maintenance visits to the stations in 2027, by district and quarter:
   - Ashby: first quarter 2, second 20, third 7, fourth 15
   - Kessel: first quarter 9, second 20, third 6, fourth 14
   - Marlow: first quarter 3, second 11, third 9, fourth 11
3. Power failures at the stations in 2027, by district and quarter:
   - Ashby: first quarter 8, second 15, third 9, fourth 8
   - Kessel: first quarter 20, second 15, third 9, fourth 12
   - Marlow: first quarter 10, second 7, third 7, fourth 10

### count_station_errors_2027.png

4. Each of the 30 stations' 2027 count error against the band from -5 to +5 per cent, the 7 listed stations marked.
