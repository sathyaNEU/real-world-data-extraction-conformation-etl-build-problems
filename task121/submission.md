# task121: the source behind the 2026 odor complaints in Harlow Falls

## Tags

**Domain:** Physical & Environmental Sciences (pollution source attribution: residents' odor complaints against a valley's wind record).
**Analytical objective:** Root-Cause Analysis.

## 1. Final Recommendation

**Ridgeway Organics' composting facility is behind the 2026 surge in odor complaints in Harlow Falls, and the district should take it to the hearing board for an order for abatement before the 2027 season.**

It lay upwind of 69 of the season's 499 odor events, 42.6 more than the 26.4 that the wind at the same clock hours on the season's other days would have given (2.6 times); Kestrel Valley Rendering comes closest at 22.5 more (99 against 76.5). Not the Pine Gulch Landfill, upwind of the most events (210) only because the night drainage puts it upwind of the town on most nights, fewer than its 299.1 at those hours. Not the rendering plant on the all-hours comparison (2.69 times), which sets night-only winds against daytime hours when nobody reports an odor.

## 2. Critical Components

1. The season's odor events, May to September 2026: **499**
2. Ridgeway Organics lay upwind of **69** of them
3. Kestrel Valley Rendering lay upwind of **99** of them

## 3. Step-by-Step Solution

1. Formed the odor events in odor_complaints_export_2026-10-02.csv under cp14_odor_complaint_procedure_rev4.pdf (complaints from inside ukvaqmd_boundary.geojson, a report received twice counted once, a household's complaints within two hours of its first): 499 events, May 1 to September 30, 2026.
2. Averaged hfs_met_5min_2026-01-01_2026-09-30.csv into hourly vector winds in standard time (hfs_station_readme.txt), leaving out the held-vane periods in hfs_station_maintenance_log_2026.csv: 60 events fell in calm hours and 2 in hours without a usable wind.
3. Applied the procedure's upwind check from each event's geocoded household to each facility in odor_source_list_2026.xlsx at the event's hour: Pine Gulch Landfill upwind of 210 events, Kestrel Valley Rendering 99, Ridgeway Organics 69, Sutter Bend Mushroom Farms 43, Harlow Falls WPCP 10.
4. Set each event against the same local clock hour on the season's other days with a usable wind at the same household, because complaints come only in the evening, at night and in the early morning while the valley wind turns with the clock: 299.1 expected for the landfill, 76.5 for Kestrel Valley Rendering, 26.4 for Ridgeway Organics.
5. Took the events beyond expectation: Ridgeway Organics 42.6 (2.6 times), Kestrel Valley Rendering 22.5 (1.3 times), Sutter Bend Mushroom Farms 2.7, the landfill and the treatment plant below expectation.
6. Compared against all hours of the season instead: Kestrel Valley Rendering leads at 2.69 times and Ridgeway Organics falls to 0.39, because the up-valley wind puts it upwind of the town all day, when nobody reports.
7. Counted the complaints by the month the odor was noticed (each report once, app times that fall after their receipt converted from UTC, the 38 carried over from ocs_open_complaints_2025-12-31.csv dated to 2025) and the station's usable and calm hours by local month: 632 complaints, 3,607 usable and 202 calm hours.
8. Ridgeway Organics is behind the surge, Kestrel Valley Rendering comes closest.

## 4. Deliverable Answers

### odor_source_determination_2026.docx

1. The facility behind the surge: Ridgeway Organics composting facility
2. The closest rival: Kestrel Valley Rendering
3. The season's odor events each facility lay upwind of:
   - Pine Gulch Landfill: 210
   - Ridgeway Organics composting facility: 69
   - Harlow Falls Water Pollution Control Plant: 10
   - Kestrel Valley Rendering: 99
   - Sutter Bend Mushroom Farms substrate wharf: 43

### odor_events_2026.xlsx

1. Complaints about odors noticed each month, from inside the district:
   - January: 29
   - February: 30
   - March: 28
   - April: 27
   - May: 89
   - June: 90
   - July: 120
   - August: 119
   - September: 100
2. Hours the Harlow Falls station recorded a usable wind:
   - May: 743
   - June: 669
   - July: 740
   - August: 738
   - September: 717
3. Hours the station recorded calm:
   - May: 38
   - June: 35
   - July: 44
   - August: 39
   - September: 46

### odor_events_by_wind_direction_2026.png

1. Polar chart of the season's 437 odor events with a wind direction, by the sixteen compass sectors (N 82, NNE 23, NE 179, ENE 3, E 4, ESE 43, SE 0, SSE 0, S 1, SSW 4, SW 51, WSW 17, W 0, WNW 0, NW 0, NNW 30), each facility's bearing from the station marked, Ridgeway Organics picked out with the sectors within 30 degrees of it shaded, and the determination in the title.
