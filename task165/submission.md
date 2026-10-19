## Tags

**Domain:** Urban & Regional Science (municipal service demand and resource allocation: a city's winter road salt for a change of service level, forecast from the spreader records of the streets that went through the same change before).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Commit 2,200 t of rock salt above the rolled-over 39,100 t contract for November 2026 to March 2027.** The redesign's collectors took under 2 t a lane-km of Priority 2 salt in a 61.7-point winter, far less than the collectors moved to Priority 1 before them, and read off those earlier moves at each street's own Priority 2 salt the move adds about 5 t a lane-km over 424.0 lane-km. Not the Priority 1 collectors' rate less these streets' own salt, which carries the higher Priority 1 level of streets with more intersections, hills and curves onto flat ones; not the earlier moves' average gain, which belongs to streets Priority 2 had already salted along much of their length.

## 2. Critical Components

1. The 424.0 lane-km's own Priority 2 rock salt over the five winters, in a winter of 61.7 WSI points: **about 700 t, under 2 t per lane-km**.
2. Their gain on moving to Priority 1 in that winter: **about 5 t per lane-km**.

## 3. Step-by-Step Solution

1. Took the 216 segments route_audit_revision_log.csv moves from priority 2 to 1 on 2026-08-30, 424.0 lane-km in winter_route_register_2026-09-14.csv.
2. Summed each collector segment's rock salt from 1 November to 31 March in each winter, from avl_legacy_segment_shift_2021-11-01_2023-03-31.csv (kilograms, legacy ids through gis_segment_crosswalk_2023.csv) and telematics_segment_passes_2023-10-01_2026-09-23.parquet (UTC to local), per lane-km and per point of the winter's WSI in storm_log_2021-22_to_2025-26.xlsx.
3. For the 377 collectors the revision log moves from priority 2 to 1 on 1 November 2022, 2023, 2024 and 2025, took each street's salt per lane-km per point in its winters before and after the move.
4. Fitted each moved street's gain against its own Priority 2 salt, weighted by lane-km: the gain falls as a street's Priority 2 salt rises.
5. Read the line at the new segments' own Priority 2 salt and scaled to 61.7 WSI points (winter_maintenance_plan_2026-27.pdf, section 4) over their 424.0 lane-km, the additional salt road_salt_procurement_procedure_RO-PR-07.pdf 4.2 commits: 2,200 t to the nearest 100 t.
6. Brought each dome's stock in dome_stock_survey_2026-09.pdf forward by the loads weighed in to it and out of it after its capture's end (winter_maintenance_plan_2026-27.pdf section 5) in scale_house_log_2026-08-24_to_2026-09-24.xlsx, the flight log's UTC taken to Eastern daylight time and a weighing for another yard counted at the dome its remarks name, and counted each of the five supplier loads also weighed at another yard's scale on its way to its own yard once, on its own yard's ticket, since deliveries for each yard are "weighed at the yard's scale house" (road_salt_procurement_procedure_RO-PR-07.pdf section 2) and the earlier ticket is the same delivery weighed again (the same truck on the same gross, back at a City scale inside its own round trip from the supplier); with the BOOKED October loads in northgrit_dispatch_2026-10_issued_2026-09-21.csv added, the stock in each dome on 1 November is Kelvin Road 7,843.2 t, Mapleford 7,142.4 t, Ridge 8,447.4 t and Lakeshore 6,279.6 t, and each dome's room is its rated capacity in salt_dome_register.csv less that stock.
7. Summed the rock salt on the arterial circuits in telematics_segment_passes_2023-10-01_2026-09-23.parquet from 1 November to 31 March local time, counting each run of the M410 controllers (the units whose segment rows repeat the run's total, salt and brine together, up to each M410 replacement in fleet_work_orders_2023-07_to_2026-09.csv) once, less its pre-wet litres at the brine's weight in winter_maintenance_plan_2026-27.pdf section 2, KLV-A15 and KLV-A16 under Mapleford before their 1 July 2026 entries in route_audit_revision_log.csv, and added Kettlewood's contract circuits under their City circuits' yards from kettlewood_material_returns_2023-24_to_2025-26.xlsx: Kelvin Road 5,100, 10,000 and 8,200 t, Mapleford 7,000, 13,700 and 11,300 t, Ridge 6,650, 13,200 and 10,700 t and Lakeshore 2,750, 5,400 and 4,500 t in 2023-24, 2024-25 and 2025-26.
8. Commit 2,200 t of rock salt above the rolled-over 39,100 t contract for November 2026 to March 2027.

## 4. Deliverable Answers

### salt_commitment_2026-27.xlsx

1. Seasonal tonnage above the rolled-over contract: 2,200 t.
2. Rock salt in each yard's dome on 1 November 2026 once the October deliveries booked with the supplier have landed, and the tonnes more the dome can then take:
   - Kelvin Road: 7,843.2 t in the dome, 1,356.8 t more
   - Mapleford: 7,142.4 t in the dome, 1,257.6 t more
   - Ridge: 8,447.4 t in the dome, 2,352.6 t more
   - Lakeshore: 6,279.6 t in the dome, 1,320.4 t more
3. Rock salt spread on each yard's Priority 1 arterial circuits, each circuit under the yard it belonged to that winter, to the nearest 50 t:
   - Kelvin Road: 2023-24 5,100 t, 2024-25 10,000 t, 2025-26 8,200 t
   - Mapleford: 2023-24 7,000 t, 2024-25 13,700 t, 2025-26 11,300 t
   - Ridge: 2023-24 6,650 t, 2024-25 13,200 t, 2025-26 10,700 t
   - Lakeshore: 2023-24 2,750 t, 2024-25 5,400 t, 2025-26 4,500 t

### seasonal_salt_commitment_council_report.docx

1. One-page report to council stating the seasonal commitment of 2,200 t, with a grouped bar chart of the arterial figures, each yard's three winters as labelled bars.
