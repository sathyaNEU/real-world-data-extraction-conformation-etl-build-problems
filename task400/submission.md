# task400 submission

## Tags

**Domain:** Human Factors & Ergonomics, safety incident and error analysis (vehicle interaction incidents between haul trucks and other vehicles at an open-pit iron ore mine).  
**Analytical objective:** Root-Cause Analysis (the driver of the 2026 rise in vehicle interaction incidents, and the programme the site's review terms assign to it).

## 1. Final Recommendation

**Mount Bracken should fund programme C, the collision avoidance alerting review on the haul truck units, for 2027.**

Vehicle interaction incidents rose from 22 in July to October 2025 to 86 in July to October 2026 because haul truck operators stopped slowing for critical alerts from units on firmware 5.0.2: while it went on, the same crews slowed for about 85 per cent of critical alerts from units still on 4.3 and about 30 per cent from units already on 5.0.2. Not B: the North ramp junction has the most incidents, but the South pit ore route, which does not use the junction, rose more per truck shift. Not A: the same operators kept slowing on 4.3 units. Not D or E: the fall in slowing came with the firmware on day shifts as on nights, and the crusher pad's incidents barely moved.

## 2. Critical Components

1. Vehicle interaction incidents, July to October 2025: **22**
2. Vehicle interaction incidents, July to October 2026: **86**
3. Firmware 5.0.2 went on the haul truck units between **2 and 23 June 2026**
4. Critical alerts followed by the truck slowing, 2 to 23 June 2026, to the nearest 5 per cent: **85%** on 4.3 units, **30%** on 5.0.2 units

## 3. Step-by-Step Solution

1. Counted the entries in incident_register_2025-01_2026-10.xlsx classified VI-COL or VI-SPI by month of occurrence (vi_review_terms_2026.docx 2.1): 22 in July to October 2025 and 86 in July to October 2026, the rise starting in June 2026.
2. Placed each incident on the dispatch shift its haul truck (the first vehicle named) was working in dispatch_shift_summary_2025-2026.csv: per 1,000 truck shifts in July to October the S-ORE>ROM route went from 2.2 to 11.7 and N-WST>NWD, the route through the North ramp junction, from 8.4 to 15.8, so the junction's extra traffic does not carry the rise.
3. Put each CRIT alert in cas_alert_events_2025-01_2026-10.parquet on its truck through the Devices sheet of cas_device_register_2026-10-31.xlsx (installed and removed dates), took the unit's firmware at onset from the Firmware sheet, moved onset from UTC to Western Australian time (UTC+8) and matched the CAS_CRITICAL window in fms_event_windows_2025-2026.parquet that opened on the same truck within 3 seconds after onset.
4. Counted an alert as acted on where the speed at t_offset_s 6 was at least 6 km/h below the speed at 0 (any drop of 4 to 10 km/h read at 4, 6 or 8 seconds gives the same figures): between 2 and 23 June 2026, with both firmwares running, 85 per cent of critical alerts on 4.3 units against 30 per cent on 5.0.2 units, to the nearest 5 per cent.
5. For the gate figures, read only IN reads in pit_gate_reads_2026-07_2026-10.csv and counted an NG-2 read 2 to 13 seconds after an NG-1 read as the same trip whatever plate each reader returned (the two North gate readers read one vehicle seconds apart, and no two vehicles pass a gate within 16 seconds); a trip with an empty cas_tag is one with no tag detected.
6. For the ramp figures, took each OVERSPEED window on NRP or SRP for a DT truck, merged a window that opens 8 to 12 seconds after the same truck's last one on the same ramp into that time over the limit, took its highest speed, and compared it with the limit in force that day in haul_road_speed_limits.csv.
7. The driver of the rise is the critical alerts on 5.0.2 units, which programme C answers (vi_review_terms_2026.docx section 4): fund C.

## 4. Deliverable Answers

### vi_programme_paper_2027.docx

1. Call: fund programme C, the collision avoidance alerting review on the haul truck units, for 2027
2. Vehicle interaction incidents: 86 in July to October 2026, 22 in July to October 2025
3. Bar chart of vehicle interaction incidents by month from January 2025 to October 2026, each bar labelled with its count

### vi_workings_2026.xlsx

1. Light-vehicle trips into the pits, and trips by vehicles whose collision avoidance tag the gate did not detect:
   - July 2026: 7,517 trips, 192 with no tag detected
   - August 2026: 7,601 trips, 189 with no tag detected
   - September 2026: 7,492 trips, 296 with no tag detected
   - October 2026: 7,620 trips, 171 with no tag detected
2. Haul truck times over the speed limit in force on each pit ramp, and how many peaked more than 5 km/h over it:
   - North pit ramp, July 2026: 44 times, 17 more than 5 km/h over
   - North pit ramp, August 2026: 44 times, 16 more than 5 km/h over
   - North pit ramp, September 2026: 48 times, 23 more than 5 km/h over
   - North pit ramp, October 2026: 49 times, 19 more than 5 km/h over
   - South pit ramp, July 2026: 31 times, 13 more than 5 km/h over
   - South pit ramp, August 2026: 29 times, 11 more than 5 km/h over
   - South pit ramp, September 2026: 38 times, 13 more than 5 km/h over
   - South pit ramp, October 2026: 32 times, 15 more than 5 km/h over
