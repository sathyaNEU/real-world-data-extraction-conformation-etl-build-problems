## Tags

**Domain:** Supply Chain & Logistics (transportation network: tracking a recalled jet fuel batch through an airport hydrant and its refuellers), in General Statistics & Data Science (data integration).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Before fuelling resumes, drain Pier B's far end (6,600 L), the cargo apron beyond its first pit (11,000 L), the remote stands (3,600 L) and refuellers RF-23, RF-24, T-31 and T-35, and notify the operators of the 86 uplifts that took the recalled batch (73 hydrant, 13 refueller).**
Fuel in each hydrant segment moved only when a pit downstream of it drew, so the batch reached these branches late or not at all past their first pits and still stands there. Not the product change reckoning, which files the hydrant clear once one line fill has passed the pump station's meter (18:19) and notifies 64 uplifts; not a branch's turnover against its own line fill, which clears the cargo apron and the remote stands and drains the maintenance base, which never took the batch.

## 2. Critical Components

1. Pier B's HB-06 and HB-07, under the stands closed at 15:00, hold **6,600 L** of the batch at 05:30.
2. The cargo apron's HE-01 to HE-03, beyond its first pit, hold **11,000 L**.
3. The remote stands' HF-01 and HF-02 hold **3,600 L**; every other section holds none.
4. **73** hydrant uplifts took fuel from the batch.

## 3. Step-by-Step Solution

1. Conformed every hydrant draw: corbel_fuel_tickets_2026-10-12_14.csv in local time with the voided ticket dropped, northgarth_tickets_20261012-20261014.xlsx moved from UTC and its stands mapped to pits by hydrant_network_register.xlsx, the idle-pit flushes in both agents' check records and the Monday low point drains in hydrant_maintenance_2026-wk42.xlsx.
2. Took Tank 3's time on the hydrant (06:00 to 15:40) from the valve states in hydrant_scada_2026-09-14_2026-10-14.csv and its time on the rack (06:00 to 12:20) from farm_shift_log_2026-10-12_14.pdf.
3. Traced the batch through the register's segments, each a first-in first-out pipe of its length and bore moved only by the draws downstream of it: at 05:30 it stands in Pier B (6,600 L), cargo apron (11,000 L), remote stands (3,600 L), and 73 hydrant uplifts took it.
4. Checked the tracing against every density in corbel_daily_checks_2026-10.csv, northgarth_qc_checks_oct2026.xlsx and the low point drain record, each read against batch_certificates_register_2026.csv: every sample shows the batch the tracing puts at its pit and time, while one line fill through the meter (clear by 18:19) does not.
5. Rebuilt each refueller tank as one mixed body from its weekly dip of 12 October through rack_loading_log_2026-10-12_14.csv (the rack line's 4,222 L of the tank before ahead of each load), the tickets, the 3,843 L RF-23 put into RF-24 (corbel_equipment_log_2026-10.csv) and Northgarth's tractor tickets keyed to the trailer northgarth_vehicle_log_2026-10.csv shows coupled (T-35 behind N-7 from 11:58): RF-23, RF-24, T-31 and T-35 hold the batch at 05:30.
6. Took each refueller uplift's batch litres as its litres times its tank's batch share when it started: 13 refueller uplifts delivered the batch.
7. Listed the 86 uplifts in the recall notice's fields and drew the plan: drain the three sections' segments and the four refuellers, notify every listed operator.

## 4. Deliverable Answers

### j26-1187_recall_uplifts.csv

1. 86 rows, one per uplift that delivered fuel from the recalled batch, in order of start (UTC): 73 hydrant and 13 refueller.
2. Columns: ticket number, into-plane agent, aircraft operator, flight, registration, uplift start in UTC, pit or refueller, litres delivered at 15 C, litres of the recalled batch at 15 C to the nearest 10 L.
3. Hydrant uplifts, by section of the pit:
   - Pier A, 33: CB418317, CB418318, CB418325, CB418328, CB418329, CB418332, CB418334, CB418335A, CB418336, CB418339, CB418341, CB418342, CB418345, CB418347, CB418348, CB418350, CB418352, CB418357, CB418358, CB418359, CB418361, CB418362, CB418365, CB418367, CB418371, CB418374, CB418377, CB418380, CB418381, CB418385, CB418386, CB418391, CB418393
   - Pier B, 20: CB418319, CB418321, NG2690191, NG2690193, NG2690198, NG2690200, NG2690201, NG2690204, NG2690205, CB418346, NG2690206, NG2690208, CB418354, NG2690210, NG2690214, NG2690215, CB418368, CB418379, NG2690217, NG2690219
   - International apron, 13: CB418322, NG2690192, CB418330, NG2690196, CB418340, CB418351, CB418363, CB418366, CB418373, CB418375, CB418384, NG2690224, NG2690241
   - Cargo apron, 4: NG2690213, NG2690216, NG2690238, NG2690240
   - Remote stands, 3: CB418378, CB418400, CB418417
4. Refueller uplifts (ticket, operator, refueller, litres delivered, batch litres):
   - NG2690190, Northcove Air, T-31 (tractor N-7), 11,209 L, 9,910 L
   - CB418327, Brightwing Airlines, RF-23, 6,313 L, 3,220 L
   - NG2690197, Sablewood Air, T-31 (tractor N-7), 7,724 L, 6,830 L
   - CB418343, Tallowmere Air, RF-23, 4,919 L, 2,510 L
   - CB418353, Brightwing Airlines, RF-24, 3,401 L, 640 L
   - NG2690209, Northcove Air, T-35 (tractor N-7), 6,763 L, 830 L
   - CB418369, Tallowmere Air, RF-24, 2,887 L, 280 L
   - CB418382, Orvelle Airways, RF-24, 3,105 L, 240 L
   - NG2690218, Sablewood Air, T-35 (tractor N-7), 5,859 L, 720 L
   - CB418399, Brightwing Airlines, RF-24, 3,557 L, 270 L
   - NG2690234, Vireo Airlines, T-35 (tractor N-7), 2,694 L, 330 L
   - CB418422, Tallowmere Air, RF-24, 2,817 L, 110 L
   - CB418424, Tallowmere Air, RF-24, 3,279 L, 120 L

### hydrant_resumption_plan.pdf

1. Hydrant sections to drain, batch litres standing to the nearest 100 L:
   - Pier B (HB-06 and HB-07): 6,600 L
   - Cargo apron (HE-01 to HE-03): 11,000 L
   - Remote stands (HF-01 and HF-02): 3,600 L
   - Farm header, hydrant main, Pier A, international apron and maintenance base: none
2. Refuellers to drain, batch litres held to the nearest 10 L:
   - RF-23: 3,070 L
   - RF-24: 310 L
   - T-31: 14,680 L
   - T-35: 2,340 L
   - RF-21, RF-22, T-32 and N-12: none
3. Batch litres the refuellers delivered, by airline, to the nearest 10 L:
   - Brightwing Airlines: 4,130 L
   - Northcove Air: 10,740 L
   - Orvelle Airways: 240 L
   - Sablewood Air: 7,550 L
   - Tallowmere Air: 3,020 L
   - Vireo Airlines: 330 L
4. Schematic of the hydrant on page 2 marking HB-06 and HB-07, HE-01 to HE-03 and HF-01 and HF-02 as holding the batch, each with its section's litres.
