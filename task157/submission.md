## Tags

**Domain:** Urban & Regional Science (transport forecasting).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Name routes 27, 41 and 58 in the Thornsby Bridge Disruption Notice: each is forecast below the 80 per cent punctuality floor over the closure, and every other Lot 2 route stays above it.**
Routes 27 and 58 are crewed off route 41: the duty schedule has drivers step off a route 41 arrival at Merchant Row Interchange onto a route 27 departure 3 minutes later and a route 58 departure 4 minutes later, so the diversion's 13 and 10 minutes reach both routes and their buses carry the delay on. Not route 41 alone, the route-level assessment, which forecasts every other route from its own record. Not route 33 as well, whose relieved departures leave 26 minutes or more after the route 41 arrival, which absorbs the delay.

## 2. Critical Components

1. The diversion adds **13 minutes** to route 41's journeys in the weekday peaks and **10 minutes** at other times, with Thornsby Road and Thornsby Quay unserved, and **2 minutes** on the Ring Road crossing for routes 6 and 12 in the weekday peaks.
2. The duty schedule relieves route 41's inbound drivers at Merchant Row onto route 27 departures **3 minutes** and route 58 departures **4 minutes** after their scheduled arrival, and onto route 33 departures **26 minutes** or more after it.
3. Over 1 September to 6 December 2026 every route runs between **82.8** and **88.4 per cent** on time, above the floor.

## 3. Step-by-Step Solution

1. Converted avl_timing_point_events.csv from UTC to local time, kept one event per re-sent message and scored every departure (a journey's last timing point excluded) against clause 7.2 of franchise_lot2_schedule7_performance_regime.pdf: autumn punctuality runs from 82.8 per cent (route 19) to 88.4 per cent (route 6).
2. Imposed thornsby_bridge_closure_tmp_v2.pdf on every recorded day: route 41 diverted between Tenter Street and Ravensholme Road at 13 minutes in the weekday peaks and 10 at other times, its Thornsby Road and Thornsby Quay departures dropped, and 2 minutes added after the Ring Road crossing on routes 6 and 12 in the weekday peaks.
3. Passed each journey's added minutes to its bus's next journey (block numbers in gcr_lot2_timetable_winter2026_txc.xml) beyond the stand time the record shows over 1 minute: route 41 alone falls below the floor.
4. Joined each duty's consecutive pieces in saltmeadow_duty_schedule_winter2026.xlsx to the timetable's journeys by running board and time, and passed a driver's added minutes at a join under 30 minutes to the departure the driver takes over, beyond the slack the record shows at that join: routes 27 and 58 fall below the floor and route 33 stays above it.
5. Lost kilometres: merged the lost and part-lost journeys in control_room_log_sep_dec_2026.csv with the uncovered pieces in saltmeadow_daily_returns_autumn2026.xlsx expanded to journeys through the duty schedule (a piece relieved after midnight running to that time the next morning) and the timetable, each journey once, dropped every returned journey the AVL recorded running, left out the excused causes of clause 7.5 and measured part journeys on the route links not run (clause 7.4): 3,174 km across Lot 2, reliability 99.60 per cent.
6. Boardings: dropped the re-sent uploads in etm_transactions_service41_oct_nov2026.csv, put sales after midnight on the day their journey ran, moved the two machines whose clocks stayed on summer time after 25 October back an hour, placed each sale on the journey its bus was running in the AVL (saltmeadow_fleet_register.csv for the bus, the running board's timetabled journey where the AVL lost it) and counted fare stages 3 and 4 of service41_fare_stages.csv over the 43 weekdays: 488 boardings a day.
7. Named every route whose closure forecast falls below 80 per cent: routes 27, 41 and 58.

## 4. Deliverable Answers

### closure_punctuality_forecast_2027.xlsx

1. Routes the Disruption Notice names: 27, 41 and 58.
2. Each route's punctuality, 1 September to 6 December 2026, and whether its closure forecast falls below the floor:
   - Route 6: 88.4 per cent, above the floor
   - Route 12: 87.7 per cent, above the floor
   - Route 14: 85.1 per cent, above the floor
   - Route 19: 82.8 per cent, above the floor
   - Route 22: 86.9 per cent, above the floor
   - Route 27: 84.0 per cent, below the floor
   - Route 33: 84.3 per cent, above the floor
   - Route 41: 84.6 per cent, below the floor
   - Route 58: 85.4 per cent, below the floor
3. Lost kilometres Schedule 7 does not excuse, and reliability, 1 September to 6 December 2026:
   - Route 6: 598 km, 99.52 per cent
   - Route 12: 281 km, 99.68 per cent
   - Route 14: 279 km, 99.69 per cent
   - Route 19: 264 km, 99.61 per cent
   - Route 22: 364 km, 99.45 per cent
   - Route 27: 412 km, 99.56 per cent
   - Route 33: 269 km, 99.64 per cent
   - Route 41: 452 km, 99.57 per cent
   - Route 58: 255 km, 99.70 per cent
   - Lot 2: 3,174 km, 99.60 per cent
4. Average weekday boardings at the stops the diversion leaves unserved (Thornsby Road, Bridge End and Thornsby Quay), October and November 2026:
   - Towards the city: AM peak 77, PM peak 39, other times 217
   - Towards Ravensholme: AM peak 12, PM peak 38, other times 106
   - Both directions, all day: 488

### closure_punctuality_by_route.svg

1. Each route's autumn 2026 punctuality (circle) and closure forecast (diamond) against a dashed 80 per cent line, with routes 27, 41 and 58 drawn in red below it.
