## Tags

**Domain:** General Statistics & Data Science (data integration and entity resolution: a state DOT district's camera pilot, Kerbline's raw detections resolved into distinct potholes with a linkage tolerance set by each unit's positional error, measured on the surveyed utility covers, and conformed to the road inventory as at 31 March into potholes per maintenance section).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Give dedicated spring patching crews to seven of the fourteen sections: Elmscourt, Norvelle, Thistlebank, Carrow Point, Holloway Run, Kestrelton and Fenwick Gap.**
Their state roadway held 9, 8, 8, 8, 8, 7 and 7 potholes per ten lane-miles in March 2027 against the program's 6.0 line; the highest of the other seven is Rushmead at 5. Not Holloway Run, Carrow Point, Elmscourt, Thistlebank and Norvelle, which joining every unit's detections at one distance (53 feet) gives: the street sweepers' units place a pothole 52 to 59 feet either way against 2 to 3 feet for every other unit, so no one distance both keeps a sweeper's reports of one pothole together and keeps neighbouring bridge-deck potholes apart.

## 2. Critical Components

1. The program's roadway is **2,428.9** lane-miles, the 2026 inventory less the five segments turned back on 15 March, on which the pilot's units recorded **1,413** distinct potholes in March.
2. Potholes per ten lane-miles: Holloway Run **8**, Fenwick Gap **7**, Carrow Point **8**, Grisholt **4**, Marlpit **4**, Kestrelton **7**, Elmscourt **9**, Halverton **3**, Thistlebank **8**, Oxbrae **4**, Rushmead **5**, Stonebeck **3**, Norvelle **8**, Pyke Hill **2**.

## 3. Step-by-Step Solution

1. Took the roadway from road_inventory_2026.csv less the five segments in route_turnback_notice_2027-03.pdf, lane-miles as length times through lanes (program section 2): 2,428.9 lane-miles.
2. Measured each unit's milepost error from its utility_cover detections in kerbline_detections_2027-03.csv against the nearest surveyed cover on the same route in utility_cover_inventory_2026.csv: the six street sweepers' units 52 to 59 feet, every other unit 2 to 3 feet.
3. Sorted the March pothole detections (district local time) on each route by road_mp and joined each to the one before it when the gap was within three times the root sum of squares of the two units' errors; each run of joined detections is one pothole.
4. Placed each pothole on the 2026 segment holding its median milepost and kept those on the roadway: 1,413 potholes; divided each section's count by its lane-miles over ten.
5. Pounds of cold mix from mms_cold_patch_orders_2027-03.csv, COMPLETE orders finished in March: a multi-line order carrying one figure on every line counted it once where the figure is more than any single-line order used on a pothole of its lines' severities (the severity of the ext_ref detection; the mobile app's order total), and summed its lines otherwise.
6. Designated the sections at 6.0 or more: Elmscourt, Norvelle, Thistlebank, Carrow Point, Holloway Run, Kestrelton and Fenwick Gap.

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
   - 401 Holloway Run: 1,400
   - 402 Fenwick Gap: 1,575
   - 403 Carrow Point: 3,770
   - 404 Grisholt: 495
   - 405 Marlpit: 1,000
   - 406 Kestrelton: 780
   - 407 Elmscourt: 4,380
   - 408 Halverton: 690
   - 409 Thistlebank: 1,710
   - 410 Oxbrae: 655
   - 411 Rushmead: 2,560
   - 412 Stonebeck: 815
   - 413 Norvelle: 1,325
   - 414 Pyke Hill: 325

### tamsett_spring_patching_task_orders_2027.pdf

1. Bar chart on page 1 of every section's potholes per ten lane-miles against the program's 6.0 line, the seven designated sections in dark blue.
