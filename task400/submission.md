# task400 submission

## Tags

**Domain:** Human Factors & Ergonomics, safety incident and error analysis (vehicle interaction incidents between haul trucks and other vehicles at an open-pit iron ore mine).  
**Analytical objective:** Root-Cause Analysis (the driver of the 2026 rise in vehicle interaction incidents, and the programme the site's review terms assign to it).

## 1. Final Recommendation

**Mount Bracken should fund programme C, the collision avoidance alerting review on the haul truck units, for 2027.**

Vehicle interaction incidents rose from 24 in July to October 2025 to 89 in July to October 2026, and the one change in operator behaviour that the records show is in the response to critical alerts on units running firmware 5.0.2: while it went on, the same crews slowed for about 85 per cent of critical alerts from units still on 4.3 and about 30 per cent from units already on 5.0.2, and from July critical alerts nobody slowed for ran at more than five times their 2025 level. Not B: the North ramp junction has the most incidents, but incidents per truck shift rose about fourfold on the South pit ore route, which never passes the junction. Not A: the same operators kept slowing on 4.3 units. Not D or E: the fall in slowing came with the firmware on day shifts as on nights, and the crusher pad's share of incidents fell.

## 2. Critical Components

1. Vehicle interaction incidents, July to October 2025: **24**
2. Vehicle interaction incidents, July to October 2026: **89**
3. Firmware 5.0.2 went on the haul truck units between **2 and 23 June 2026**
4. Critical alerts followed by the truck slowing, 2 to 23 June 2026, to the nearest 5 per cent: **85%** on 4.3 units, **30%** on 5.0.2 units

## 3. Step-by-Step Solution

1. Counted the entries in incident_register_2025-01_2026-10.xlsx classified VI-COL or VI-SPI by month of occurrence (vi_review_terms_2026.docx 2.1): 24 in July to October 2025 and 89 in July to October 2026, the rise starting in June 2026.
2. Placed each incident on the dispatch shift its haul truck (the first vehicle named) was working in dispatch_shift_summary_2025-2026.csv: per 1,000 truck shifts in July to October the S-ORE>ROM route went from 2.2 to 9.2 and N-WST>NWD, the route through the North ramp junction, from 8.4 to 21.3, so the junction's extra traffic does not carry the rise.
3. Put each CRIT alert in cas_alert_events_2025-01_2026-10.parquet on its truck through the Devices sheet of cas_device_register_2026-10-31.xlsx (installed and removed dates), took the unit's firmware at onset from the Firmware sheet, moved onset from UTC to Western Australian time (UTC+8) and matched the CAS_CRITICAL window in fms_event_windows_2025-2026.parquet that opened on the same truck within 3 seconds after onset.
4. Counted an alert as acted on where the speed at t_offset_s 6 was at least 6 km/h below the speed at 0 (any drop of 4 to 10 km/h read at 4, 6 or 8 seconds gives the same figures): between 2 and 23 June 2026, with both firmwares running, 85 per cent of critical alerts on 4.3 units against 30 per cent on 5.0.2 units, to the nearest 5 per cent.
5. For the gate figures, read only IN reads in pit_gate_reads_2026-07_2026-10.csv and counted an NG-2 read 2 to 13 seconds after an NG-1 read as the same entry whatever plate each reader returned (the two North gate readers read one vehicle seconds apart, and no two vehicles pass a gate within 16 seconds); a trip with an empty cas_tag is one with no tag detected.
6. For the ramp figures, took each OVERSPEED window on NRP or SRP for a DT truck in fms_event_windows_2025-2026.parquet, joined a window to the run before it only where it opens on the sample that closed the same truck's last window on that ramp (ten seconds later) with the truck still over the limit at that sample, took each run's highest speed, and compared it with the limit in force that day in haul_road_speed_limits.csv.
7. The response to critical alerts is the only measured change in operator behaviour, it follows the firmware rather than the crews, and critical alerts nobody slowed for rose more than fivefold in July to October against almost fourfold for the incidents; programme C answers the alerts (vi_review_terms_2026.docx section 4): fund C.

## 4. Deliverable Answers

### vi_programme_paper_2027.docx

1. Call: fund programme C, the collision avoidance alerting review on the haul truck units, for 2027
2. Vehicle interaction incidents: 89 in July to October 2026, 24 in July to October 2025
3. Chart of the monthly count of vehicle interaction incidents from January 2025 to October 2026, each month's count readable

### vi_workings_2026.xlsx

1. Light-vehicle trips into the pits, and trips by vehicles whose collision avoidance tag the gate did not detect:
   - July 2026: 7,517 trips, 192 with no tag detected
   - August 2026: 7,601 trips, 189 with no tag detected
   - September 2026: 7,492 trips, 296 with no tag detected
   - October 2026: 7,620 trips, 171 with no tag detected
2. Haul truck times over the speed limit in force on each pit ramp, and how many peaked more than 5 km/h over it:
   - North pit ramp, July 2026: 53 times, 22 more than 5 km/h over
   - North pit ramp, August 2026: 72 times, 29 more than 5 km/h over
   - North pit ramp, September 2026: 59 times, 23 more than 5 km/h over
   - North pit ramp, October 2026: 43 times, 20 more than 5 km/h over
   - South pit ramp, July 2026: 26 times, 9 more than 5 km/h over
   - South pit ramp, August 2026: 19 times, 7 more than 5 km/h over
   - South pit ramp, September 2026: 34 times, 13 more than 5 km/h over
   - South pit ramp, October 2026: 48 times, 23 more than 5 km/h over
