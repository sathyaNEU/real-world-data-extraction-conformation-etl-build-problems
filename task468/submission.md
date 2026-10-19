## Tags

**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution: two AVL systems' stop events linked to the timetable's trips, the links the matchers missed propagated into each route's departures through the department's clerical review).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Nominate Routes 2, 4, 6, 17 and 22 to the Frequent Transit Corridors Program for FY2027.**
Seven candidates meet the standard once each stop's departures without a trip are shared by Service Quality's review weighted by its own design: Route 17 is 56 per cent of the Transit Mall's departures without a trip, its lowest hour averages 4.8 departures, and it ranks fourth of the seven by boardings, leaving Route 11 as the first qualifying route left out. Not Routes 2, 4, 6, 22 and 11, which share by the review's unweighted mix (Route 17 at 35 per cent) and leave Route 17 short at 3.6; not Routes 2, 4, 9, 22 and 11, which share in proportion to the departures the matchers tied to trips and give the short-handed Route 9 Oak Street's late buses.

## 2. Critical Components

1. Counting days: **125** (weekdays of January to June 2026, the four state holidays out).
2. Departures in the counting hours that the AVL records tie to no trip: **17,112** of 106,687.
3. Route 17's share of the Transit Mall's departures without a trip, each reviewed event weighted by its bus-day's departures without a trip: **56 per cent** (unweighted, 35).
4. Route 17's lowest hourly average: **4.8** departures, at least four in each of the thirteen hours.

## 3. Step-by-Step Solution

1. Conformed avl_stop_events_2026q1_arbor.csv and avl_stop_events_2026q2_quinnell.csv into one table of departures in Central time at the five designated stops: Arbor's stop ids to stop codes through the January feed's stops.txt, Quinnell's UTC to Central time and its asset tags to fleet numbers through fleet_roster_2026.csv, each event to its service day, Quinnell's rows repeated at the head of each daily file (same bus, stop and second) dropped, and March 31's service taken from Arbor's export.
2. Kept the 125 counting days and the thirteen clock hours from 6 a.m. (guidance 3.3 and 3.4): 106,687 departures, 17,112 with no trip.
3. Weighted each of the 2,400 events in trip_matching_review_2026h1.csv by the departures without a trip its bus-day had at the five stops (the review draws one from each of 400 bus-days a month) and by its month's bus-days listed over drawn: Route 17 is 56 per cent of the Transit Mall's departures without a trip.
4. Shared each stop's departures without a trip in each hour among its routes by the weighted mix, buses out of service left out, added the departures tied to each route's trips, and averaged over the counting days.
5. Took each candidate's lowest hour: Routes 2, 4, 6, 11, 17, 22 and 40 meet four in every hour; Routes 9, 14, 31 and 51 do not.
6. Ranked the qualifying routes by average weekday boardings in ridership_by_route_2026h1.xlsx (guidance 5.1): Routes 2, 4, 6, 17 and 22, with Route 11 the first qualifying route left out.
7. For the shelters, took each candidate's outbound stops from larkhaven_gtfs_20260405.zip (stops.txt, trips.txt with direction 0, stop_times.txt) and joined them to facilities_bus_stop_amenities_20260710.csv by stop code; where a stop's position in the spring feed lies away from where Facilities last inspected it (the spring timetable moved it across its intersection after the inspection), took its shelter only from capital_projects_shelter_work_orders.xlsx work orders completed there between April 5 and June 30; elsewhere took the inventory's shelter, moved forward by work orders completed after the inspection and back by those completed after June 30.
8. Recommended nominating Routes 2, 4, 6, 17 and 22.

## 4. Deliverable Answers

### larkhaven_frequent_corridor_nominations_fy2027.xlsx

1. Verdicts on the program's standard:
   - Route 2 Grand Avenue: meets
   - Route 4 Lincoln Avenue: meets
   - Route 6 Oak Street: meets
   - Route 9 Riverside: does not meet
   - Route 11 University Connector: meets
   - Route 14 Elm Park: does not meet
   - Route 17 Prairie Road: meets
   - Route 22 Fairgrounds: meets
   - Route 31 College Hill: does not meet
   - Route 40 Westgate Crosstown: meets
   - Route 51 Hillcrest: does not meet
2. Nominated: Routes 2, 4, 6, 17 and 22.
3. First qualifying route left out: Route 11.
4. Stops its outbound trips serve in the spring timetable that had no shelter on June 30, 2026:
   - Route 2: 15
   - Route 4: 16
   - Route 6: 8
   - Route 9: 6
   - Route 11: 9
   - Route 14: 10
   - Route 17: 13
   - Route 22: 8
   - Route 31: 7
   - Route 40: 12
   - Route 51: 13
5. Bar chart of each candidate's lowest hourly average against the standard of four, on the Nominations sheet.
