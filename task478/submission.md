## Tags

**Domain:** General Statistics & Data Science (data integration: a state DOT district's camera pilot, Kerbline's detections linked into defects and reviewed, integrated with the fleet's segment traversals, the unit register and the road inventory into a completed count of potholes per maintenance section, the potholes no unit recorded estimated with each kind of vehicle, not each unit, as one capture occasion).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Give dedicated spring patching crews to seven of the fourteen sections: Elmscourt, Carrow Point, Norvelle, Holloway Run, Thistlebank, Kestrelton and Fenwick Gap.**
Their state roadway held 9, 9, 8, 8, 8, 7 and 7 potholes per ten lane-miles in March 2027 against the program's 6.0 line; the highest of the other seven is Rushmead at 5. Not Holloway Run, Carrow Point, Elmscourt, Thistlebank and Norvelle, which counting every installed unit as an independent chance gives: two units on the same kind of vehicle record 93.6 per cent of the same potholes against 54.9 per cent across kinds, so a segment's chances are its kinds of vehicle. Not Carrow Point and Elmscourt, which counting every pass gives.

## 2. Critical Components

1. The program's roadway is **2,428.9** lane-miles, the 2026 inventory less the five segments turned back on 15 March, holding **1,034** confirmed potholes.
2. Potholes per ten lane-miles, completed over the distinct fleet groups that drove each segment: Holloway Run **8**, Fenwick Gap **7**, Carrow Point **9**, Grisholt **4**, Marlpit **4**, Kestrelton **7**, Elmscourt **9**, Halverton **3**, Thistlebank **8**, Oxbrae **4**, Rushmead **5**, Stonebeck **3**, Norvelle **8**, Pyke Hill **2**.

## 3. Step-by-Step Solution

1. Took the roadway from road_inventory_2026.csv less the five segments in route_turnback_notice_2027-03.pdf, lane-miles as length times through lanes (program section 2): 2,428.9 lane-miles.
2. Kept the potholes confirmed in kerbline_qa_review_2027-03.xlsx, folding each defect rejected as a duplicate into the confirmed defect nearest it on its route, and placed each on its 2026 segment from its detections' road_ref and road_mp in kerbline_detections_2027-03.csv through road_inventory_crosswalk_2025_2026.csv: 1,034 potholes.
3. Listed the units that drove each segment in March, district local time, from fleet_camera_traversals_2027-03.csv joined by vehicle to kerbline_unit_register.xlsx on its install and removal dates, and their fleet groups.
4. Read the recaptures: where two units drove a segment, the second recorded 93.6 per cent of the first's potholes when both were in one fleet group and 54.9 per cent across groups, so each fleet group that drove a segment is one capture occasion.
5. Read the per-group find rate from the potholes on segments two or more groups drove: 54.4 per cent.
6. Counted each confirmed pothole as one over one minus 0.456 to the power of the distinct fleet groups that drove its segment, and divided each section's total by its lane-miles over ten.
7. Pounds of cold mix from mms_cold_patch_orders_2027-03.csv, COMPLETE orders finished in March: a multi-line order carrying one figure on every line counted it once where the figure is more than any single-line order used on a pothole of its lines' severities in the detections (the mobile app's order total; an ext_ref Kerbline no longer carries taken to the defect at the same route and milepost in the review export), and summed its lines otherwise.
8. Designated the sections at 6.0 or more: Elmscourt, Carrow Point, Norvelle, Holloway Run, Thistlebank, Kestrelton and Fenwick Gap.

## 4. Deliverable Answers

### tamsett_spring_patching_sections_2027.csv

1. Potholes per ten lane-miles of state roadway, March 2027, whole numbers:
   - 401 Holloway Run: 8
   - 402 Fenwick Gap: 7
   - 403 Carrow Point: 9
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
   - 401 Holloway Run: 1,350
   - 402 Fenwick Gap: 1,360
   - 403 Carrow Point: 4,455
   - 404 Grisholt: 585
   - 405 Marlpit: 1,135
   - 406 Kestrelton: 935
   - 407 Elmscourt: 3,400
   - 408 Halverton: 500
   - 409 Thistlebank: 1,110
   - 410 Oxbrae: 180
   - 411 Rushmead: 1,835
   - 412 Stonebeck: 540
   - 413 Norvelle: 940
   - 414 Pyke Hill: 295

### tamsett_spring_patching_task_orders_2027.pdf

1. Bar chart on page 1 of every section's potholes per ten lane-miles against the program's 6.0 line, the seven designated sections in dark blue.
