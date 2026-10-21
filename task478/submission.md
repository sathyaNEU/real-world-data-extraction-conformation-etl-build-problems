## Tags

**Domain:** General Statistics & Data Science (data integration: a state DOT district's camera pilot, Kerbline's detections linked across passes and units, integrated with the fleet's segment traversals, the unit register, the review queue and the road inventory into a completed count of potholes per maintenance section, the potholes no unit recorded estimated from how often a second unit finds what a first one found).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Give dedicated spring patching crews to seven of the fourteen sections: Elmscourt, Norvelle, Thistlebank, Holloway Run, Carrow Point, Kestrelton and Fenwick Gap.**
Their state roadway held 9, 8, 8, 8, 8, 7 and 7 potholes per ten lane-miles in March 2027 against the program's 6.0 line; the highest of the other seven is Rushmead at 5. Not Carrow Point and Elmscourt alone, which counting every pass over a segment as an independent chance gives: a unit that recorded a pothole recorded it again on 99.7 per cent of its later days, so a segment driven many times by one unit had that one unit's chance, and a second unit finds 54.2 per cent of what another found.

## 2. Critical Components

1. The program's roadway is **2,428.9** lane-miles, the 2026 inventory less the five segments turned back on 15 March, holding **1,080** confirmed potholes.
2. Potholes per ten lane-miles, completed over the distinct units that drove each segment: Holloway Run **8**, Fenwick Gap **7**, Carrow Point **8**, Grisholt **4**, Marlpit **4**, Kestrelton **7**, Elmscourt **9**, Halverton **3**, Thistlebank **8**, Oxbrae **4**, Rushmead **5**, Stonebeck **3**, Norvelle **8**, Pyke Hill **2**.

## 3. Step-by-Step Solution

1. Took the roadway from road_inventory_2026.csv less the five segments in route_turnback_notice_2027-03.pdf, lane-miles as length times through lanes (program section 2): 2,428.9 lane-miles.
2. Kept the potholes confirmed in kerbline_qa_review_2027-03.xlsx, folding each defect rejected as a duplicate into the confirmed defect nearest it on its route, and placed each on its 2026 segment from its detections' road_ref and road_mp in kerbline_detections_2027-03.csv through road_inventory_crosswalk_2025_2026.csv: 1,080 potholes.
3. Listed the units that drove each segment in March, district local time, from fleet_camera_traversals_2027-03.csv joined by vehicle to kerbline_unit_register.xlsx on its install and removal dates; every segment had at least one.
4. Read the per-unit find rate from the potholes on segments two or more units drove: of the other units that drove a found pothole's segment, 54.2 per cent found it, against 99.7 per cent of a finding unit's own later days.
5. Counted each confirmed pothole as one over one minus 0.458 to the power of the distinct units that drove its segment, and divided each section's total by its lane-miles over ten.
6. Cold patches from mms_cold_patch_orders_2027-03.csv, COMPLETE orders finished in March: an ext_ref missing from Kerbline's exports, a number from before Kerbline's 17 March renumbering, taken to the confirmed defect at the same route and milepost in the review export, each defect the reviewer rejected as a duplicate taken to the confirmed defect nearest it on its route, so each pothole counts once; a multi-line order carrying one figure on every line counted it once where the figure is more than any single-line order used on a pothole of its lines' severities in the detections (the mobile app's order total), and summed its lines otherwise.
7. Camera miles: dropped each traversal that repeats the same vehicle's traversal of the segment, the same way, exactly five hours later (the provider's re-run of 12 to 13 March, written in district clock time), kept installed units' March passes on the program's roadway and summed inventory lengths.
8. Designated the sections at 6.0 or more: Elmscourt, Norvelle, Thistlebank, Holloway Run, Carrow Point, Kestrelton and Fenwick Gap.

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
3. Potholes cold patched in March, a pothole patched more than once counting once:
   - 401 Holloway Run: 20
   - 402 Fenwick Gap: 27
   - 403 Carrow Point: 70
   - 404 Grisholt: 11
   - 405 Marlpit: 13
   - 406 Kestrelton: 13
   - 407 Elmscourt: 85
   - 408 Halverton: 6
   - 409 Thistlebank: 23
   - 410 Oxbrae: 7
   - 411 Rushmead: 48
   - 412 Stonebeck: 13
   - 413 Norvelle: 10
   - 414 Pyke Hill: 7
4. Pounds of cold mix those patches used:
   - 401 Holloway Run: 1,275
   - 402 Fenwick Gap: 1,535
   - 403 Carrow Point: 3,780
   - 404 Grisholt: 460
   - 405 Marlpit: 765
   - 406 Kestrelton: 1,070
   - 407 Elmscourt: 4,760
   - 408 Halverton: 360
   - 409 Thistlebank: 1,140
   - 410 Oxbrae: 280
   - 411 Rushmead: 2,915
   - 412 Stonebeck: 780
   - 413 Norvelle: 860
   - 414 Pyke Hill: 400
5. Miles the pilot's camera units were driven on the program's roadway in March, each pass at its segment's inventory length:
   - 401 Holloway Run: 2,087
   - 402 Fenwick Gap: 1,789
   - 403 Carrow Point: 7,734
   - 404 Grisholt: 1,774
   - 405 Marlpit: 2,512
   - 406 Kestrelton: 1,659
   - 407 Elmscourt: 6,743
   - 408 Halverton: 1,823
   - 409 Thistlebank: 1,870
   - 410 Oxbrae: 2,052
   - 411 Rushmead: 13,259
   - 412 Stonebeck: 2,257
   - 413 Norvelle: 1,791
   - 414 Pyke Hill: 1,776

### tamsett_spring_patching_task_orders_2027.pdf

1. Bar chart on page 1 of every section's potholes per ten lane-miles against the program's 6.0 line, the seven designated sections in dark blue.
