## Tags

**Domain:** General Statistics & Data Science (data integration and entity resolution: a state DOT district's camera pilot, Kerbline's raw detections resolved into distinct potholes after each detection is moved back along its pass by its unit's GPS latency, fitted on the surveyed utility covers, times the pass's speed, and conformed to the road inventory as at 31 March into potholes per maintenance section).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Give dedicated spring patching crews to seven of the fourteen sections: Elmscourt, Thistlebank, Holloway Run, Carrow Point, Norvelle, Kestrelton and Fenwick Gap.**
Their state roadway held 9, 8, 8, 8, 8, 7 and 7 potholes per ten lane-miles in March 2027 against the program's 6.0 line; the highest of the other seven is Rushmead at 5. Not the five sections (Holloway Run, Carrow Point, Elmscourt, Thistlebank and Norvelle) that joining the detections where Kerbline placed them at one distance of 200 feet designates: every unit places a detection ahead of the pothole along its direction of travel by its GPS latency (0.47 to 1.74 seconds) times its speed, so a distance wide enough to join a pothole's two directions runs the bridge decks' potholes together, and at 100 feet Grisholt and Oxbrae come in instead.

## 2. Critical Components

1. The program's roadway is **2,428.9** lane-miles, the 2026 inventory less the five segments turned back on 15 March, on which the pilot's units recorded **1,427** distinct potholes in March.
2. Potholes per ten lane-miles: Holloway Run **8**, Fenwick Gap **7**, Carrow Point **8**, Grisholt **4**, Marlpit **4**, Kestrelton **7**, Elmscourt **9**, Halverton **3**, Thistlebank **8**, Oxbrae **4**, Rushmead **5**, Stonebeck **3**, Norvelle **8**, Pyke Hill **2**.

## 3. Step-by-Step Solution

1. Took the roadway from road_inventory_2026.csv less the five segments in route_turnback_notice_2027-03.pdf, lane-miles as length times through lanes (program section 2): 2,428.9 lane-miles.
2. Joined every detection in kerbline_detections_2027-03.csv to its pass: the unit's vehicle from kerbline_unit_register.xlsx, captured_local (district local time, across the 14 March change) in UTC, and that vehicle's traversal in fleet_camera_traversals_2027-03.csv running at that moment, which gives the direction of travel (mileposts increase northbound and eastbound) and the speed (the 2026 segment's length over the traversal's duration).
3. Fitted each unit's latency on its utility_cover detections against the nearest surveyed cover on the same route in utility_cover_inventory_2026.csv (within 0.05 mile): the error along the direction of travel regressed through the origin on the pass's speed, 0.47 to 1.74 seconds.
4. Moved each March pothole detection (district local time) back along its pass by its unit's latency times its pass's speed, sorted each route's corrected mileposts and joined a detection to the one before it when the gap was within 10 feet; each run of joined detections is one pothole.
5. Placed each pothole on the 2026 segment holding its median corrected milepost and kept those on the roadway: 1,427 potholes; divided each section's count by its lane-miles over ten.
6. Pounds of cold mix from mms_cold_patch_orders_2027-03.csv, COMPLETE orders finished in March, each line on the section whose 2026 roadway holds its route milepost (program 3, the cold patches on the section's roadway, whichever section's crew made them): an order whose lines all carry one figure and one finished time counted that figure once (the data notes), every other line its own, a pothole patched twice on both of its orders.
7. Designated the sections at 6.0 or more: Elmscourt, Thistlebank, Holloway Run, Carrow Point, Norvelle, Kestrelton and Fenwick Gap.

## 4. Deliverable Answers

### tamsett_spring_patching_sections_2027.csv

1. Potholes per ten lane-miles of state roadway, March 2027, whole numbers:
   - 401 Holloway Run: 8
   - 402 Fenwick Gap: 7
   - 403 Carrow Point: 8
   - 404 Grisholt: 4
   - 405 Marlpit: 4
   - 406 Kestrelton: 7
   - 407 Elmscourt: 9
   - 408 Halverton: 3
   - 409 Thistlebank: 8
   - 410 Oxbrae: 4
   - 411 Rushmead: 5
   - 412 Stonebeck: 3
   - 413 Norvelle: 8
   - 414 Pyke Hill: 2
2. Dedicated crew:
   - 401 Holloway Run: Yes
   - 402 Fenwick Gap: Yes
   - 403 Carrow Point: Yes
   - 404 Grisholt: No
   - 405 Marlpit: No
   - 406 Kestrelton: Yes
   - 407 Elmscourt: Yes
   - 408 Halverton: No
   - 409 Thistlebank: Yes
   - 410 Oxbrae: No
   - 411 Rushmead: No
   - 412 Stonebeck: No
   - 413 Norvelle: Yes
   - 414 Pyke Hill: No
3. Pounds of cold mix the section's March cold patches used:
   - 401 Holloway Run: 1,760
   - 402 Fenwick Gap: 1,495
   - 403 Carrow Point: 4,125
   - 404 Grisholt: 640
   - 405 Marlpit: 1,070
   - 406 Kestrelton: 1,340
   - 407 Elmscourt: 4,495
   - 408 Halverton: 520
   - 409 Thistlebank: 2,005
   - 410 Oxbrae: 380
   - 411 Rushmead: 3,125
   - 412 Stonebeck: 1,060
   - 413 Norvelle: 1,495
   - 414 Pyke Hill: 625

### tamsett_spring_patching_task_orders_2027.pdf

1. Bar chart on page 1 of every section's potholes per ten lane-miles against the program's 6.0 line, the seven designated sections in dark blue.
