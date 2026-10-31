## Tags

> **Domain:** Human factors and ergonomics, safety incident and error analysis.
> **Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Run the 2027 Driver-Attention Programme at San Lázaro, and at no other depot.**
San Lázaro's drivers did not brake on 45.2 per cent of their genuine collision warnings in January to October 2026, 2.00 times the fleet's 22.6 per cent. Not Hornacho or Valdeolmos: their high no-brake shares come from four fixed structures that raise a warning on a large share of passes with nothing in the path. La Ribera comes closest at 1.14.

## 2. Critical Components

1. The terms count genuine warnings only (something in the bus's path), one camera event each, by the depot the bus was allocated to that day, in Lorvega local time.
2. Read on every collision warning, the fleet's rate is 38.9 per cent and Hornacho and Valdeolmos reach 1.3 times it; San Lázaro sits at 1.16.
3. Four places fire on a large share of bus passes, from 25.0 to 30.3 per cent; every other place, the Plaza de Abastos included at 2.6 per cent, fires on under 3 per cent. Their 17,968 warnings are not genuine and are set aside.
4. The Plaza de Abastos warnings are genuine: drivers there let 96.9 per cent pass, so dropping the busiest or most ignored places wrongly removes them too.

## 3. Step-by-Step Solution

1. From adas_collision_warnings_2025-10_2026-10.csv kept FCW, PCW, FWD_COLL and PED_COLL, one row per event_id, local dates 1 January to 31 October 2026; not braked on is brake_2s N (firmware 1.x) or brake_reaction_ms blank or over 2,000 (2.x).
2. Gave each warning the depot of its bus that day from fleet_register_2026.xlsx Allocations.
3. Snapped each warning to the nearest stop-to-stop segment of red_paradas_recorridos_2025_2026.xlsx (Red 2026, valid dates) and counted bus passes per segment from service_return_2025-10_2026-10.csv trips operated on every line and direction using it.
4. Grouped warnings in 10 m bins along each segment and set aside the clusters firing on 10 per cent or more of the segment's passes.
5. Took each depot's rate and its ratio to the pooled fleet rate; a depot at 1.3 or more goes in.
6. Hours on service from etm_logons_2026-10.csv: removed repeated rows and lines 000 and ESC, ended a session at the same driver's next log-on, added the hour when clocks went back on 25 October, depot from hr_depot_assignments_2026.csv on the start date, week of the start.
7. At-fault collisions from incident_register_2026.xlsx with the driver's and the inspector's report of one incident (same bus, minutes apart) counted once, codes A and C; claims paid from the October bordereau, plates to buses through the registration history, a reopened claim's chain counted once at its latest claim.
8. Kilometres in service from the return by operating depot (line 25 at Las Tenerías), lines 40 to 46 from July in metres, plus trips operated times each authorised diversion's change for its dates.

## 4. Deliverable Answers

### attention_programme_depots_2027.docx

1. Depots the programme takes: San Lázaro.
2. Fleet's rate of counted warnings not braked on: 22.6 per cent.
3. Depot coming closest without qualifying: La Ribera, ratio 1.14.

### warning_response_by_depot_2026.xlsx

1. Counted warnings, not braked on, rate (per cent, one decimal) and ratio (two decimals):
   - San Lázaro: 8,557, 3,868, 45.2, 2.00
   - Hornacho: 5,700, 889, 15.6, 0.69
   - Valdeolmos: 7,895, 1,273, 16.1, 0.71
   - El Quiñón: 5,913, 981, 16.6, 0.73
   - Las Tenerías: 10,744, 1,877, 17.5, 0.77
   - La Ribera: 8,280, 2,139, 25.8, 1.14
   - Santa Clara: 6,190, 1,008, 16.3, 0.72
2. At-fault collisions, January to October, and claims paid on them (euros):
   - San Lázaro: 20, 24,207
   - Hornacho: 25, 25,850
   - Valdeolmos: 19, 20,517
   - El Quiñón: 19, 33,737
   - Las Tenerías: 25, 29,216
   - La Ribera: 22, 22,579
   - Santa Clara: 21, 17,280
3. Kilometres in service, July, August, September and October (whole kilometres):
   - San Lázaro: 75,127, 72,183, 70,694, 74,009
   - Hornacho: 66,213, 63,634, 60,226, 62,999
   - Valdeolmos: 93,313, 93,247, 90,820, 93,543
   - El Quiñón: 59,390, 55,796, 56,939, 57,969
   - Las Tenerías: 105,247, 101,901, 101,253, 107,135
   - La Ribera: 84,360, 80,946, 79,839, 81,039
   - Santa Clara: 82,443, 80,731, 84,145, 78,799
4. Drivers' hours on service, weeks from Monday 5, 12, 19 and 26 October (whole hours):
   - San Lázaro: 4,493, 4,481, 4,514, 4,501
   - Hornacho: 3,521, 3,493, 3,519, 3,498
   - Valdeolmos: 4,496, 4,507, 4,510, 4,486
   - El Quiñón: 3,398, 3,395, 3,378, 3,381
   - Las Tenerías: 5,621, 5,614, 5,643, 5,617
   - La Ribera: 4,507, 4,516, 4,494, 4,510
   - Santa Clara: 4,502, 4,489, 4,492, 4,513

### warning_response_2026.svg

1. One bar per depot for the rate of counted warnings not braked on, with a dashed line at 1.3 times the fleet's rate (29.4 per cent).
2. San Lázaro marked in red; the title names it.
