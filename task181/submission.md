# task181 submission

## Tags

**Domain:** Human Factors & Ergonomics, safety incident and error analysis (losses of separation between aircraft in an area control centre's en-route sectors).
**Analytical objective:** Anomaly Detection & Diagnostics (which sector's losses of separation will break the unit safety plan's tolerance, diagnosed from what produces them).

## 1. Final Recommendation

**Tarvik will run over the safety plan's tolerance in summer 2027, at about 72 ATM-related losses of separation per 100,000 flight hours against 40.0, and no other sector will.**

Every loss of separation in the record is two aircraft in one sector at once with one climbing or descending through the other's level, and with the new Brekka flights the planning traffic gives Tarvik 48,545 such pairs against 9,682 in summer 2026, on 16,414 flight hours against 14,957. Not "no sector", which is what each sector's summer 2026 rate carried onto its 2027 flight hours gives (Mosby highest at 32.0, Tarvik at 13.4), because Tarvik's losses follow its pairs, not its hours. Not Grendal or Hallin, which only the change from summer 2025 to summer 2026 carried forward puts over, on a single extra loss each. Every other sector stays under 30.

## 2. Critical Components

1. ATM-related losses of separation (SMI, ATM contribution D or I), 1 January 2025 to 30 September 2026: **96** in the eight sectors, every one between two aircraft in the sector at once whose levels changed order
2. **2.45** ATM-related losses per 10,000 such pairs over the record (**96** on **392,294** pairs), between **2.31** and **2.59** in every sector, while losses per 100,000 flight hours run from **13.8** to **24.2**
3. Tarvik in the summer 2027 planning traffic: **48,545** pairs on **16,414** flight hours
4. Summer 2027 forecast: Tarvik about **72** per 100,000 flight hours; every other sector under **30**

## 3. Step-by-Step Solution

1. Kept the SMI occurrences with ATM contribution D or I in `occurrence_export_2025-01_2026-09.csv` (codes in `occurrence_scheme_codes.csv`, as the unit safety plan defines a loss of separation and ATM-related): 96 from 1 January 2025 to 30 September 2026.
2. Found both named aircraft of each loss in `fdps_sector_traversals_2025-01_2026-09.parquet` (sector names to codes through `sector_register.json`): in every one the two were in the sector together and one passed through the other's level, entry to exit levels taken as a straight line.
3. Counted every such pair in the flight data, sector by sector (two traversals of one sector overlapping in time, one strictly above the other where the overlap begins and strictly below it where it ends): 392,294, so 2.45 ATM-related losses per 10,000 pairs, steady across the sectors where losses per 100,000 flight hours are not.
4. Counted the same pairs, and the flight hours from sector entry to exit as the safety plan defines them, in `planning_traffic_summer2027_issue1.csv` (traffic volumes to sectors through the register): Tarvik 48,545 pairs on 16,414 flight hours.
5. Multiplied each sector's 2027 pairs by 2.45 per 10,000 and divided by its planning flight hours: Tarvik about 72 per 100,000 flight hours against the plan's 40.0, every other sector under 30.
6. Recommendation: Tarvik alone runs over the tolerance in summer 2027.
7. For summer 2026 (1 June to 31 August local, UTC times converted): delay per flight from `nm_slot_allocations_2026-05_2026-09.csv`, counted for the flights that operated (the plans whose `ifplid` is in the flight data), each at its most penalising regulation (extract notes), en-route ones charged to the regulation's sector (`nm_regulations_2026-05_2026-09.csv`), over the flights that entered the sector; ACAS encounters from the ACAS RA rows, two reports naming the same two aircraft in the same sector minutes apart counted once.
8. Hours on its own from `sector_configuration_log_2026-05_2026-09.csv` (local time) against the configuration table at revision 8 in `HACC_OM_part3_ch4_sector_configuration.pdf` until the logged entry for revision 9 at 06:00 on 14 July 2026, and `sector_configurations_current.csv` from then.

## 4. Deliverable Answers

### summer2027_safety_forecast.pptx
1. Sectors over the 40.0 tolerance in summer 2027: Tarvik only, at about 72 ATM-related losses of separation per 100,000 flight hours; the other seven are under 30.
2. Chart on slide 1: one bar per sector of the summer 2027 forecast per 100,000 flight hours against a line at the 40.0 tolerance; Tarvik's bar is the only one above the line.

### summer2026_sector_measures.csv
1. En-route ATFM delay per flight, summer 2026, minutes to two decimals:
   - Tarvik: 0.53
   - Mosby: 0.41
   - Grendal: 0.43
   - Linmark: 0.16
   - Karrow: 0.29
   - Lysvik: 0.55
   - Hallin: 0.27
   - Sandvik: 0.10
2. Hours each sector was open as a sector on its own, summer 2026, to one decimal:
   - Tarvik: 1,532.1
   - Mosby: 1,310.5
   - Grendal: 735.3
   - Linmark: 1,202.3
   - Karrow: 771.1
   - Lysvik: 1,410.2
   - Hallin: 971.6
   - Sandvik: 1,301.9
3. Encounters that gave an aircraft an ACAS resolution advisory, summer 2026:
   - Tarvik: 8
   - Mosby: 9
   - Grendal: 10
   - Linmark: 7
   - Karrow: 4
   - Lysvik: 7
   - Hallin: 3
   - Sandvik: 2
