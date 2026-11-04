## Tags

**Domain:** Human Factors & Ergonomics (safety incident and error analysis: a streetcar's firm-brake record and its seasonal restricted-speed orders).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Place the four restricted-speed slots for the weekday peaks of 4 January to 26 February 2027 on J4 outbound in the AM peak (Market Square to Harlan Avenue), J5 outbound AM (Harlan Avenue to Sandoval Street), F5 outbound in the PM peak (Tallow Street to Kiln Avenue) and F6 outbound PM (Kiln Avenue to Smelter Row).**
The part of this autumn's rise that moves between rows was the low sun standing ahead of the operator: on the record's logged passes, firm braking climbed on sunny passes with the sun low and close to the line of travel, which in the September and October peaks meant the east- and west-running directions. The class that qualified on 31 August added a smaller lift in its first weeks on every direction alike, and it has faded by January. In the January and February peaks the low sun stands ahead of the south-east-running morning and south-west-running evening directions instead, and J4 and J5 outbound head 125 and 131 degrees, F5 and F6 outbound 231 and 237. Not the rows that rose this autumn, whose excess moved with the sun and has left their line; not a low-sun allowance that ignores direction, which spreads the excess over every row the low sun reaches.

## 2. Critical Components

1. Bearings of travel from the survey's coordinates, outbound in coordinate order and inbound reversed: **J4 125, J5 131, F5 231 and F6 237 degrees outbound**.
2. **The autumn's extra firm braking that moves between rows follows the sun**: on sunny logged passes it rises as the low sun comes onto the bearing of travel; the newly qualified class's smaller first-weeks lift is direction-neutral and gone by January.
3. **Expected rates are taken at the pick's scheduled weekday-peak passes on its 38 weekdays, in the 68 per cent possible sunshine the station normals give January and February.**
4. **In those peaks the low sun stands ahead of the south-east-running morning and south-west-running evening directions**, so J4-O AM, J5-O AM, F5-O PM and F6-O PM carry the four highest expected rates.

## 3. Step-by-Step Solution

1. Converted the recorder export's UTC stamps to Mountain time and attached each FB record to the pass in avl_section_passes_2026.parquet of the car that logged it, the pass whose section lies nearest the recorded position: 95 per cent of the 11,955 FB records fall on a logged pass.
2. Gave each pass the sun's elevation and azimuth at its midpoint (NOAA's solar position at the survey's mean coordinates), its section direction's bearing from streetcar_track_survey_2025.geojson (outbound in coordinate order, inbound reversed) and the sky reported in ash_awos_hourly_obs_2026.csv for its clock hour (sun out under CLR, FEW or SCT): J4 and J5 outbound head 125 and 131 degrees, F5 and F6 outbound 231 and 237.
3. Fitted firm brakes per pass on every logged pass by Poisson regression with a base for each section direction, clock-hour terms, a term for days off the weekday timetable, darkness (sun below the horizon) and a glare factor 1 + G x a x h on sunny passes, a the squared cosine of the sun's offset from the bearing scaled so that 25 degrees off gives none and h one with the sun under 12 degrees up, falling to none at 25: G is 2.5.
4. Built the pick's passes from january_2027_pick_timetable.pdf (its weekday headways and running times on its 38 weekdays, 4 January to 26 February 2027 less the two Monday holidays), kept those entering a section in SRM-07's weekday peaks, set each against the sun and its bearing as in step 2, and averaged each section-direction peak's fitted rate at the 68 per cent possible sunshine of ash_climate_normals_1991-2020.pdf: the four highest are J4-O AM, J5-O AM, F5-O PM and F6-O PM.
5. Ask A: kept the EB records of the recorder export made by a car in service on a block as SRM-07 defines it, the pull-out car or cars on yard_block_sheets_2026.csv from the block's out time until the AVL log first shows another vehicle on that block that day, which is in service from then to the block's in time (a record before 03:00 counts to the day before), dropped the running brake test in the hour after each release in foundry_depot_releases_2026.csv, counted a two-car train's two records on one block within 6 minutes and 80 metres once, and grouped by Mountain-time month: the figures in block 4.
6. Ask B: took the Operator card rows of mms_defect_reports_2026.csv, dated each to the day in the week before it was entered (its entered_at) on which its car ran its block, a car yard_block_sheets_2026.csv names on the block or the car the AVL log shows taking the block over, kept the days run_sheets_2026.csv gives the Weekday schedule from April to October and counted by the car's line and defect group (Brakes, Doors, every other group): the figures in block 4.
7. Placed the four slots on J4-O AM, J5-O AM, F5-O PM and F6-O PM, marked yes in slot_plan_jan_feb_2027.csv among its 52 rows.

## 4. Deliverable Answers

### slot_plan_jan_feb_2027.csv

1. 52 rows, one for each section of track in each direction of travel in each weekday peak, in network order; restricted_speed_slot is yes on four rows (rso_limit_mph 10) and no on the other 48:
   - J1 outbound, Mesa Park to Laurel Street: AM no, PM no
   - J1 inbound, Laurel Street to Mesa Park: AM no, PM no
   - J2 outbound, Laurel Street to Civic Center: AM no, PM no
   - J2 inbound, Civic Center to Laurel Street: AM no, PM no
   - J3 outbound, Civic Center to Market Square: AM no, PM no
   - J3 inbound, Market Square to Civic Center: AM no, PM no
   - J4 outbound, Market Square to Harlan Avenue: AM yes, PM no
   - J4 inbound, Harlan Avenue to Market Square: AM no, PM no
   - J5 outbound, Harlan Avenue to Sandoval Street: AM yes, PM no
   - J5 inbound, Sandoval Street to Harlan Avenue: AM no, PM no
   - J6 outbound, Sandoval Street to Union Yard: AM no, PM no
   - J6 inbound, Union Yard to Sandoval Street: AM no, PM no
   - F1 outbound, Northfield to Garnet Street: AM no, PM no
   - F1 inbound, Garnet Street to Northfield: AM no, PM no
   - F2 outbound, Garnet Street to Pike Street: AM no, PM no
   - F2 inbound, Pike Street to Garnet Street: AM no, PM no
   - F3 outbound, Pike Street to Arsenal Road: AM no, PM no
   - F3 inbound, Arsenal Road to Pike Street: AM no, PM no
   - F4 outbound, Arsenal Road to Tallow Street: AM no, PM no
   - F4 inbound, Tallow Street to Arsenal Road: AM no, PM no
   - F5 outbound, Tallow Street to Kiln Avenue: AM no, PM yes
   - F5 inbound, Kiln Avenue to Tallow Street: AM no, PM no
   - F6 outbound, Kiln Avenue to Smelter Row: AM no, PM yes
   - F6 inbound, Smelter Row to Kiln Avenue: AM no, PM no
   - F7 outbound, Smelter Row to Foundry Loop: AM no, PM no
   - F7 inbound, Foundry Loop to Smelter Row: AM no, PM no

### braking_shift.png

2. Paired horizontal bars for every section direction in network order, an AM panel and a PM panel: each row's September to October 2026 observed firm-braking rate beside its January to February 2027 expected rate, the four slot rows shaded and labelled.

### Emergency brake applications in service (in the response)

3. The streetcar's applications by Mountain-time month, April to October 2026, whole numbers: April 99, May 99, June 99, July 113, August 105, September 97, October 95

### Defect cards operators wrote (in the response)

4. Each line's cards written on days the weekday timetable ran, April to October 2026 as a whole, whole numbers:
   - Juniper Line: brakes 46, doors 55, all other defects 171
   - Foundry Line: brakes 44, doors 34, all other defects 122
