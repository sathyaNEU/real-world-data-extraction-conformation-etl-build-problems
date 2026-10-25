## Tags

**Domain:** Human factors and ergonomics, human reliability assessment.  
**Analytical objective:** Forecasting and predictive modeling.

## 1. Final Recommendation

**Plan the Phase 4 safety case and its debriefing for about 1,250 train data entry errors recorded against the six Phase 4 depots' drivers in each depot's first twelve months on ETCS, to the nearest 250.**
The figure reads the chance of an error at each Start of Mission at the driver's own count of ETCS starts in the Phase 1 to 3 record, and runs each of the 276 Phase 4 drivers along it at that driver's 2026 cab activations, about 111,000 starts in the twelve months. Not the earlier depots' first-year errors per start, nor a curve on months since go-live: both carry the suburban drivers' pace, and the rural diagrams keep a Phase 4 driver in the record's first weeks for most of the year.

## 2. Critical Components

1. Drivers on the six Phase 4 depots' rosters at 31 October 2026: **276**
2. Their ETCS Starts of Mission in the depots' first twelve months: **111,000** (nearest 1,000)

## 3. Step-by-Step Solution

1. Placed every Phase 1 to 3 driver start in obr_start_of_mission_log_2024-03_2026-10.csv on the driver's own count of ETCS starts, staff numbers chained through staff_number_crosswalk.csv and TST test starts left out: 707,562 starts.
2. Took the train data entry errors from safety_desk_register_2024-2026.xlsx (category TDE, withdrawn reports out, a linked report once): 4,418, each placed at its start by the SoM Ref of its own or a linked report, else at the driver's last start before the report (the register in local time, the recorder in UTC).
3. Read the errors per start in bands of 50 on that count, to 600 and then one band: 0.0315 in a driver's first 50 starts and 0.0049 beyond 600.
4. For each of the 276 drivers on a Phase 4 roster in driver_roster_2026-10-31.xlsx, took the ETCS starts already made (6 drivers transferred in with some) and twelve months at the driver's monthly cab activations on duties worked in phase4_duty_records_2026.csv, latest issue: 111,357.6 starts.
5. Summed each driver's chance along the bands from the starts already made: 1,280.2, about 1,250 to the nearest 250.
6. Units: each unit in fleet_allocation_2027.csv by its two driving vehicles in unit_formations_2026-10-31.csv, accepted for ETCS service by its depot's go-live in the rollout plan when both vehicles' Accepted or Planned Acceptance dates in etcs_fitment_works_records.xlsx fall on or before it; the works records' Unit is the programme's own unit, so vehicles reformed into other units and renumbered units are read through the formation list.
7. Events: the register's LTR and BRK reports received January to October 2026, withdrawn reports out and linked reports once, each recorder download report (stamped in the recorder's UTC) folded into a driver's or signaller's report of the same driver, unit and category up to 30 minutes after it, and a later event the same day kept as its own.

## 4. Deliverable Answers

### phase4_data_entry_forecast.xlsx

1. Train data entry errors the safety desk will record against the six Phase 4 depots' drivers in each depot's first twelve months on ETCS: **1,250** (nearest 250)
2. Drivers covered: **276**; their ETCS starts over those twelve months: **111,000** (nearest 1,000)
3. Class 461 units allocated for the 2027 timetable, accepted for ETCS service by the depot's go-live and not accepted:
   - Glenhallow: **8** accepted, **6** not accepted
   - Drumcarra: **8** accepted, **5** not accepted
   - Kilvane: **7** accepted, **6** not accepted
   - Ardmorrow: **6** accepted, **4** not accepted
   - Mossbeck: **5** accepted, **5** not accepted
   - Fellbrook: **4** accepted, **6** not accepted
4. Level transition errors and ETCS brake interventions of each Phase 1 to 3 depot's drivers, January to October 2026:
   - Brennick: **54** level transition errors, **83** brake interventions
   - Tollmere: **71** level transition errors, **92** brake interventions
   - Ashlow Road: **73** level transition errors, **92** brake interventions
   - Kelderby: **33** level transition errors, **65** brake interventions
   - Marrow Bridge: **51** level transition errors, **70** brake interventions
   - Fennick Junction: **60** level transition errors, **59** brake interventions
   - Stanholt: **76** level transition errors, **83** brake interventions
   - Corran Central: **61** level transition errors, **64** brake interventions

### phase4_depot_readiness.svg

1. One stacked bar per Phase 4 depot, its accepted and not accepted units, each segment labelled with its count as in answer 3 above.
