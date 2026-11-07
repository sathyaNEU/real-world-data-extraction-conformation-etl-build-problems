## Tags

**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution (a waterways charity's summit lockage rebuilt from its lock counters' camera export, the Tilsey lock-keepers' log and its lock register).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Site the 2027/28 back-pumping scheme at Kelsby summit: its two summit locks drew 1,460.8 Ml from the summit pound by filling their chambers between 1 April and 31 October 2026, 274.3 Ml more than Tilsey summit (1,186.5 Ml).**
Not Harnock (1,140.8 Ml), which leads on boats charged a lockful each because its broad chambers hold the largest lockfuls, but whose boats mostly pass two to a chamber, one filling for the pair. Not Tilsey, whose flight carries the most boats but is worked in turn, so most boats going down find the chamber already full.

## 2. Critical Components

1. Kelsby summit's lockage is **1,460.8 Ml**: Kelsby Top Lock **780.5 Ml**, Wharf Lock **680.3 Ml**.
2. Tilsey summit's lockage is **1,186.5 Ml** and Harnock summit's **1,140.8 Ml**.
3. Harnock Top Lock's **7,005** boat movements and Steward's Lock's **6,501** made **4,995** and **4,637** chamber cycles.

## 3. Step-by-Step Solution

1. Read lock_counter_movements_2026.csv through counter_sites_2026.json (the older firmware's rows in UK clock time with UP or DOWN, the June firmware's rows in UTC with A>B from the tail pound into the chamber), leaving out 1,476 unpowered craft and 949 repeat reads of one plate within a minute.
2. Covered Tilsey Top Lock's camera outage from 3 to 23 August with the 1,077 entries in tilsey_lock_keepers_log_2026.xlsx that match no camera record by plate, direction and time, the log's times read as UK clock time.
3. Grouped each lock's records into chamber cycles, same-direction records at one lock being either within about a minute of each other (boats sharing the chamber) or at least fourteen minutes apart: Harnock Top Lock and Steward's Lock ran 4,995 and 4,637 cycles.
4. Replayed each chamber through its cycles from empty on 1 April (navigation_notices_2026.csv, with Steward's Lock left empty on reopening at 17:00 on 29 May): a cycle going up fills the chamber, a cycle going down fills it only when the cycle before went down, each filling charged the 2025 survey lockful in lock_register_2026.xlsx.
5. Summed each summit's two locks: Kelsby 1,460.8 Ml, Tilsey 1,186.5 Ml, Harnock 1,140.8 Ml.
6. Rebuilt reservoir_returns_2026.xlsx from each 09:00 rate and the timed valve remarks over the season's clock hours (Lower Kelsby's keeper books each release on the day the valve is shut), re-rated coldmere_outlet_15min_2026.csv's head on the crest plate in service from 10:30 UTC on 16 June per reservoir_register_extract_2025.pdf, and divided it at Fox Bridge by the pool's level over both notches: Coldmere 6,859.1 Ml, of which 4,462.5 Ml reached Harnock and 2,396.6 Ml Tilsey.
7. Chained abstraction_meter_readings_2026.csv at each abstraction point from the March to the October month-end reading, taking the four exchanged meters' removal and installation readings from works_orders_2026.csv and rolling the trout farm's five-dial meter over.
8. Recommended Kelsby summit, 274.3 Ml ahead of Tilsey.

## 4. Deliverable Answers

### summit_lockage_return_2026.csv

1. One row per summit lock and calendar date of the season, with boats up, boats down, chamber fillings and water drawn in cubic metres.
2. Season water by summit lock, Ml:
   - Kelsby Top Lock: 780.5
   - Wharf Lock: 680.3
   - Harnock Top Lock: 605.4
   - Steward's Lock: 535.4
   - Tilsey Top Lock: 601.6
   - Engine Lock: 584.9
3. Summit totals, Ml: Kelsby 1,460.8; Tilsey 1,186.5; Harnock 1,140.8.
4. Counter records left out: 949 repeat reads of one plate within a minute and 1,476 unpowered craft.

### summit_water_2026.xlsx

5. Reservoir releases over the season, Ml: Upper Kelsby 527.2 (into Lower Kelsby Reservoir), Lower Kelsby 2,246.9, Coldmere 6,859.1, Tilsey 1,090.6.
6. Water received from the reservoirs, Ml: Kelsby summit 2,246.9; Harnock summit 4,462.5; Tilsey summit 3,487.2.
7. Metered take between the March and October month-end readings, cubic metres:
   - KA/014 Hollins Farm: 30,500
   - KA/022 Kelsby Golf Club: 17,790
   - KA/031 Kelsby Wharf Marina: 6,088
   - HA/007 Harnock Mill Trout Farm: 467,827
   - HA/019 Glebe Farm Partnership: 27,299
   - HA/026 Carver's Brewery: 12,904
   - TA/003 Tilsey Hall Estate: 19,398
   - TA/011 Brook Farm: 24,099
   - TA/018 Tilsey Quarry Products: 11,185
8. Summit totals, cubic metres: Kelsby 54,378; Harnock 508,030; Tilsey 54,682.

### backpumping_site_2027.docx

9. A two-page paper recommending Kelsby summit, with the lock-by-lock table and a stacked bar chart of each summit's lockage by lock.
