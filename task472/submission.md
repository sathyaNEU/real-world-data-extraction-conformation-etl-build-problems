## Tags

**Domain:** Supply Chain & Logistics (ports and container terminals, data integration and record linkage: two terminal operating systems, the pilot station's sailings, the Salt Point tide predictions and the vessel register linked into a fiscal year's large-vessel calls, each call's sailing re-allocated under the port's access rules from an earlier ready-to-sail time).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Ternmouth should place the six 2027 replacement cranes at Millrace.**
Its fiscal year 2026 large-vessel calls would have been 887 berth hours shorter with the new cranes, 331 more than Halyard's 556. Not Saltworks, which logged the most cargo work, because its deep-draft ships finish ahead of their tide at Salt Point and a faster finish only lengthens their wait (257 hours). Not Pine Neck or Ore Dock, whose largest ships are worked to sail at first light and gain nothing from finishing earlier in the night (449 and 423 hours).

## 2. Critical Components

1. Fiscal year 2026 large-vessel calls (ships of 10,000 TEU and over, first container move in the year): **784**
2. Millrace's berth hours saved: **887**
3. The runner-up, Halyard: **556**; Millrace's lead: **331** berth hours

## 3. Step-by-Step Solution

1. Linked each visit in tos_vessel_visits_2026.csv and the Calls sheet of srt_tos_export_fy2026.xlsx to vessel_register_extract_2026-10-05.json by IMO number and kept ships of 10,000 TEU and over whose first container move fell in fiscal year 2026, Eastern time (rules 3.2 and 3.3): 784 calls.
2. Took each call's cargo work, first container move to last, from tos_crane_activity_2026.csv and the QC Hours sheet (UTC, converted), and matched each call to its sailing in pilot_station_sailings_fy2026.csv by the ship's name at the time (current or former) or call sign, at the call's berth after its last move.
3. Read when a ship may sail from harbor_masters_general_directions_2025.pdf: a draft of 41 feet or more passes Salt Point from 1 h 30 min before to 30 min after high water (9.2), on the passage times in 9.3, with high waters from salt_point_tide_predictions_2025_2026.txt (standard time, an hour added in daylight saving time); a ship of 1,250 feet or more unberths in the harbor only from 0600 to 2000 (8.1); every sailing in the record is the first such time an hour or more after its notice.
4. For each call, brought its ready-to-sail notice forward by a fifth of its cargo work, gave it the first permitted sailing an hour or more after that, and took the difference from its actual sailing as its berth hours saved (rule 3.6); summed by terminal (rule 3.7): Millrace 887; Halyard 556; Pine Neck 449; Ore Dock 423; Gannet Point 395; Saltworks 257.
5. Ask A: took the out-of-service periods in cmms_asset_status_history_fy2026.csv on orders whose type at the pull is BD (each period of a reopened order) and the BRKDN jobs in srt_maintenance_jobs_2025-26.xlsx, counted February 2026's river stops held in both systems once, placed each stop at the terminal whose calls its crane was working at the time in the TOS crane hours (three cranes moved along the common rail during the year, which the crane register does not show), and summed fiscal year hours: Ore Dock 1,271; Pine Neck 968; Gannet Point 499; Halyard 1,118; Saltworks 701; Millrace 1,715.
6. Ask B: summed cmms_labor_transactions_fy2026.csv on crane orders, the SRT job hours not also in the Authority's system, and the days in crane_maker_service_timesheets_fy2026.xlsx not already keyed into the ledger as CONTRACT on the same order, day and hours, each at the terminal where the crane was working that day, yard equipment left out: Ore Dock 2,759; Pine Neck 3,097; Gannet Point 1,661; Halyard 2,935; Saltworks 2,169; Millrace 3,554.
7. Placed the cranes at the terminal with the most berth hours saved: Millrace, 331 hours ahead of Halyard.

## 4. Deliverable Answers

### ternmouth_2027_crane_placement.xlsx

1. Recommended terminal: Millrace.
2. Berth hours the new cranes would have saved on fiscal year 2026 large-vessel calls, whole hours:
   - Millrace: 887
   - Halyard: 556
   - Pine Neck: 449
   - Ore Dock: 423
   - Gannet Point: 395
   - Saltworks: 257
3. Runner-up: Halyard; Millrace leads by 331 berth hours.
4. Bar chart of the six terminals' berth hours saved on the Berth hours saved sheet, largest first, Millrace highlighted.
5. Hours ship-to-shore cranes stood out of service for breakdowns at each terminal over fiscal year 2026, whole hours:
   - Ore Dock: 1,271
   - Pine Neck: 968
   - Gannet Point: 499
   - Halyard: 1,118
   - Saltworks: 701
   - Millrace: 1,715
6. Maintenance labor hours spent on ship-to-shore cranes at each terminal over fiscal year 2026, the Authority's own staff and contractors alike, whole hours:
   - Ore Dock: 2,759
   - Pine Neck: 3,097
   - Gannet Point: 1,661
   - Halyard: 2,935
   - Saltworks: 2,169
   - Millrace: 3,554

### ternmouth_fy2026_large_vessel_calls.csv

1. The conformed table of the 784 fiscal year 2026 large-vessel calls, one row per call: terminal, visit, ship, IMO number, first and last container move (Eastern time) and berth hours saved to two decimals.
