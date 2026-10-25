## Tags

**Domain:** Energy systems and utilities (generation capacity planning).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Build Kingsley Fields in 2027: it will export about 9,700 MWh in 2028, its first full year.**
Hallam Down receives 4.1 per cent more sun than Kingsley Fields, but its ten planned blocks would lose more than that, at least 4.7 per cent of their output, to the dust of the broiler unit beside them, a loss Wexcombe's fiscal meter averages away and only its inverter blocks show, so it exports no more than 9,600 MWh. Larkhill Common (9,500 MWh) and Marston Vale (9,300 MWh) receive less sun on the same performance.

## 2. Critical Components

1. Knowle Park, the one farm on the frame and modules the build repeats, has a measured performance ratio of **0.83** (its export over its 12.0 MWp and its satellite irradiation from 16 January 2024 to 31 December 2025).
2. Hallam Down's average-year irradiation is **4.1** per cent above Kingsley Fields', the best of the other three.
3. Wexcombe's three blocks nearest its broiler unit, **87** to **141** m from the sheds, produce **1.5** to **4.2** per cent less than its blocks more than **450** m away, while its fiscal meter runs **1.1** per cent above its 2012 to 2014 peers.
4. Carried by block distance to Hallam Down's ten planned blocks (**76** to **269** m from its unit) through its own rain, the deposit takes at least **4.7** per cent of their output on every fit the Wexcombe blocks support, more than the 4.1 per cent lead, so Hallam Down exports no more than **9,600** MWh against Kingsley Fields' **9,700**.

## 3. Step-by-Step Solution

1. Divided Knowle Park's export in fleet_daily_export_2022-2025.csv by its 12.0 MWp (site_register.csv) and its irradiation in site_weather_daily_2016-2025.csv summed over every day it metered, outage days kept: a performance ratio of 0.830; the four bifacial farms' annual ratios, log-linear in age with a level for each farm, give a degradation of 0.15 per cent a year.
2. Multiplied each candidate's ten-year average irradiation in site_weather_daily_2016-2025.csv by 11.0 MWp and that ratio, carried at that degradation from Knowle Park's mean age over its record to the candidate's age at mid-2028 from its energisation date in build_decision_note_2027.docx: Kingsley Fields 9,700 MWh, Larkhill Common 9,500, Marston Vale 9,300, Hallam Down 10,100.
3. Placed the 10-shed broiler units listed beside Wexcombe and Hallam Down in site_environs_2km.csv by distance and bearing from the centroid in site_register.csv, and measured every block in array_layout_blocks.csv from the sheds.
4. Divided each Wexcombe block's daily energy in inverter_daily_energy_2022-2025.parquet by its dc_mwp and by that day's median of the blocks more than 450 m from the sheds, leaving out the block's days in om_event_log_2022-2025.csv: the three nearest run 1.5 to 4.2 per cent low, falling through dry spells and recovering after rain.
5. Fitted each block within 320 m a deposit that builds by a daily step on days under 4 mm of rain, to no more than 25 per cent, keeps 55 per cent of itself on 4 to 10 mm and 8 per cent on 10 mm or more (the thresholds that fit best), with the step falling exponentially with distance, and ran it at each Hallam Down block through Hallam Down's own rain weighted by its irradiation: a loss of 7.4 per cent, 9,300 MWh against Kingsley Fields' 9,700; the fits on the farm's median block or a full wash at one threshold take no less than 4.7 per cent.
6. Pyranometers: met_station_daily_2025.csv carries the logger's sensor setting, which stayed on the sensor that came down in 2025, so each mast's sensor was that one before the installed date in pyranometer_register.csv and the register's from it (the sensor that came down has a certificate sent from that mast dated after it); each recorded day's poa_signal_mvh over the sensitivity of the certificate in force that day in pyranometer_calibration_certificates.xlsx for the sensor then in the mast, summed, over the weather file's irradiation on the same days: 0.971 at Hartsfield to 1.007 at Dunsford Lane.
7. Alarm response: each fault alarm in scada_alarm_log_2025.csv (UTC) joined to its work order in cmms_work_orders_2025.csv, the van its technician had that day in technician_vans_2025.csv and that van's first entry at the farm after the alarm in van_tracker_site_visits_2025.csv, whose times are UK time like the CMMS's (the CMMS attended stamp at a farm without signal is the tablet's sync after the visit, after the alarm cleared): averages from 9.5 hours at Furzedown to 31.3 at Knowle Park.
8. Kingsley Fields exports the most of the four in 2028: build it, 9,700 MWh.

## 4. Deliverable Answers

### fenmore_site_selection_2027.xlsx

1. Site to build in 2027: Kingsley Fields
2. Its export in 2028: 9,700 MWh
3. Each operating farm's 2025 irradiation measured by its met-station pyranometer as a ratio to the site weather file's, over the days the pyranometer recorded:
   - Ashcombe: 0.985
   - Bramble Hill: 0.984
   - Wexcombe: 0.988
   - Coldharbour: 0.991
   - Brindle Moor: 0.985
   - Dunsford Lane: 1.007
   - Elmstead: 0.989
   - Fairoak: 0.987
   - Greystoke Barns: 0.984
   - Hartsfield: 0.971
   - Ivy Cross: 0.989
   - Furzedown: 0.985
   - Jessop's Farm: 0.993
   - Knowle Park: 0.987
4. Each operating farm's average hours in 2025 from an inverter fault alarm to the technician who attended it arriving on site:
   - Ashcombe: 12.9
   - Bramble Hill: 11.9
   - Wexcombe: 19.6
   - Coldharbour: 20.2
   - Brindle Moor: 19.5
   - Dunsford Lane: 15.0
   - Elmstead: 18.6
   - Fairoak: 17.4
   - Greystoke Barns: 21.5
   - Hartsfield: 13.0
   - Ivy Cross: 14.6
   - Furzedown: 9.5
   - Jessop's Farm: 16.1
   - Knowle Park: 31.3

### fenmore_build_paper_2027.docx

5. The case for building Kingsley Fields at 9,700 MWh in 2028, and for passing over Hallam Down, whose broiler-dust loss exceeds its lead in irradiation.
6. Chart of each candidate's expected 2028 export: Kingsley Fields 9,700 MWh, highlighted; Larkhill Common 9,500; Marston Vale 9,300; Hallam Down after broiler dust below Kingsley Fields, no more than 9,600 on any fit, from 10,100 before it.
