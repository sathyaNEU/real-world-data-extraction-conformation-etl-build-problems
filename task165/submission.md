## Tags

**Domain:** Urban & Regional Science (municipal service demand and resource allocation: a city's winter road salt for a change of service level, forecast from the spreader records of the streets that went through the same change before).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Commit 2,200 t of rock salt above the rolled-over 39,100 t contract for November 2026 to March 2027.** The redesign's collectors took 1.6 t a lane-km of Priority 2 salt in a 61.7-point winter, far less than the collectors moved to Priority 1 before them, and read off those earlier moves at each street's own Priority 2 salt the move adds 5.2 t a lane-km over 424.0 lane-km. Not the Priority 1 collectors' rate less these streets' own salt, which carries the higher Priority 1 level of streets with more intersections, hills and curves onto flat ones; not the earlier moves' average gain, which belongs to streets Priority 2 had already salted along much of their length.

## 2. Critical Components

1. The 424.0 lane-km's own Priority 2 rock salt in a winter of 61.7 WSI points: **1.6 t per lane-km**.
2. Their gain on moving to Priority 1 in that winter: **5.2 t per lane-km**.

## 3. Step-by-Step Solution

1. Took the 216 segments route_audit_revision_log.csv moves from priority 2 to 1 on 2026-08-30, 424.0 lane-km in winter_route_register_2026-09-14.csv.
2. Summed each collector segment's rock salt from 1 November to 31 March in each winter, from avl_legacy_segment_shift_2021-11-01_2023-03-31.csv (kilograms, legacy ids through gis_segment_crosswalk_2023.csv) and telematics_segment_passes_2023-10-01_2026-09-23.parquet (UTC to local), per lane-km and per point of the winter's WSI in storm_log_2021-22_to_2025-26.xlsx.
3. For the 202 collectors the revision log moves from priority 2 to 1 on 1 November 2022, 2023, 2024 and 2025, took each street's salt per lane-km per point in its winters before and after the move.
4. Fitted each moved street's gain against its own Priority 2 salt, weighted by lane-km: the gain falls as a street's Priority 2 salt rises.
5. Read the line at the new segments' own Priority 2 salt and scaled to 61.7 WSI points (winter_maintenance_plan_2026-27.pdf, section 4) over their 424.0 lane-km, the additional salt road_salt_procurement_procedure_RO-PR-07.pdf 4.2 commits: 2,200 t to the nearest 100 t.

## 4. Deliverable Answers

### salt_commitment_2026-27.xlsx

1. Seasonal tonnage above the rolled-over contract: 2,200 t.
2. Rock salt in each yard's dome on 1 November 2026 once the October deliveries booked with the supplier have landed, and the tonnes more the dome can then take:
   - Kelvin Road: 7,843.2 t in the dome, 1,356.8 t more
   - Mapleford: 7,142.4 t in the dome, 1,257.6 t more
   - Ridge: 8,447.4 t in the dome, 2,352.6 t more
   - Lakeshore: 6,279.6 t in the dome, 1,320.4 t more
3. Rock salt spread on each yard's Priority 1 arterial circuits:
   - Kelvin Road: 2023-24 4,487.3 t, 2024-25 7,883.9 t, 2025-26 6,158.2 t
   - Mapleford: 2023-24 5,663.7 t, 2024-25 9,845.3 t, 2025-26 7,701.5 t
   - Ridge: 2023-24 5,050.2 t, 2024-25 8,836.6 t, 2025-26 6,896.9 t
   - Lakeshore: 2023-24 7,519.9 t, 2024-25 13,243.7 t, 2025-26 10,252.3 t

### seasonal_salt_commitment_memo.docx

1. One-page report to council stating the seasonal commitment of 2,200 t, with a grouped bar chart of the arterial figures, each yard's three winters as labelled bars.
