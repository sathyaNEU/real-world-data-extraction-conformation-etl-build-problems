## Tags

**Domain:** Physical & Environmental Sciences, pollution source attribution.  
**Analytical objective:** Root-Cause Analysis.

## 1. Final Recommendation

**Place the 2027 atrazine cost-share program in the Fennick Creek sub-watershed.** Fennick Creek's atrazine was behind all 47 of the 2026 season's days on which the raw water was above the 3.0 ug/L trigger, and no other sub-watershed's was behind any. Not the Tessel River, which carried the most atrazine past its station in every month from April to July but whose warm water spread over the stratified lake's surface layer, above the intake; not Oxley or Dunmore Creek, whose water also entered above the intake's layer; not Ladd Branch, whose water ran to the bottom.

## 2. Critical Components

1. Days in the 15 April to 31 October season with the raw-water result above 3.0 ug/L: **47**.
2. The lake was stratified at the dam from **27 April** to **6 October**, and on every day above the trigger Fennick Creek was the only sub-watershed whose water had entered the lake within the intake's layer.
3. Days above the trigger each sub-watershed's atrazine caused: Fennick Creek **47**; Dunmore Creek **0**; Ladd Branch **0**; Oxley Creek **0**; Tessel River **0**.

## 3. Step-by-Step Solution

1. Took each day's raw-water result from raw_water_log_2026-01-01_to_2026-05-26.csv and LIMS_raw_water_2026-05-20_to_2026-10-31.xlsx as SOP-WQ-07 2.3 sets it (the GC/MS confirmation where one was run, otherwise the ELISA screen) and counted the season's days above 3.0 ug/L (plan 5.2): 47.
2. Built the lake's daily mean temperature profile from MERRIN_BUOY_Hourly_2026.dat (logger clock on CST; sensor depths from buoy_service_log_2026.csv, 0.5 to 15.5 m before the 10 June re-hang and 1 to 16 m after) and the intake's daily depth below the surface from the pool elevation in merrin_dam_daily_log_2026.xlsx (NGVD29) less the intake centreline on intake_tower_record_drawing_S-4.pdf (829.24 ft NAVD88, NGVD29 plus 0.24 ft): stratified from 27 April to 6 October, the intake 10.4 to 11.0 m down in June and July.
3. Placed each tributary's water each day at the depth where that day's profile was as warm as the tributary's daily mean temperature (TR-01, FC-02 and OC-03 exports on local time; the DC-04 and LB-05 loggers on UTC), and on each day above the trigger listed the sub-watersheds whose water had entered within two metres of the intake's depth since the lake stratified, looking back up to 30 days: Fennick Creek alone on all 47 days, so without its atrazine the raw water keeps only the lake's spring residue and each day counts for Fennick Creek and no other sub-watershed (plan 5.1).
4. For the station atrazine, took each bottle's value from SHL_EDD_brennick_source_water_2026.csv (Client_Sample_ID without its hyphens) where the State laboratory ran it and from city_lab_ELISA_tributaries_2026.xlsx otherwise, not detected as zero (plan 3.2); a routine grab's time is its logged time in field_sampling_log_2026.xlsx, and a storm bottle's is its sample time in autosampler_run_logs_2026.csv, each carousel's bottles in number order matched to the positions that drew a sample (NO LIQUID positions hold no bottle).
5. Took DC-04 discharge from gage height through the rating in force in DC-04_LB-05_ratings_and_field_visits.xlsx (rating 2 from 2 June 11:30 CDT), gage height being the logger's level plus the staff-gage offset from the field visits: 1.36 ft until 14:15 on 3 July, when the logger's level steps up 0.25 ft between two readings with no rain, and 1.11 ft after; then summed each 15-minute discharge times the concentration interpolated linearly between the samples either side of it, by local month from 1 April to 31 July: the monthly figures for atrazine_sources_2026.xlsx in section 4, Ladd Branch not sampled.
6. For the carbon, applied each dose setpoint in scada_pac_dose_setpoint_2026.csv (UTC) to the plant day's raw water pumped in daily_operating_report_2026.xlsx (06:00 to 06:00 next day) at 8.34 lb per million gallons per mg/L (SOP-WQ-07 3.2), minute by minute, over the minutes the feeder in scada_alarm_event_history_2026.csv was running with carbon: stopped from a MOTOR OVERLOAD TRIP until its next RUN STATUS ON, and feeding nothing from a HOPPER LEVEL LOW-LOW NO FEED alarm to its return: 3,243 lb in May, 25,024 in June, 23,776 in July and 3,693 in August.
7. Fennick Creek gets the program: 47 days of 47, every other sub-watershed none.

## 4. Deliverable Answers

### cost_share_placement_2027.docx

1. The 2027 cost-share program goes to the Fennick Creek sub-watershed.
2. Days above the trigger each sub-watershed's atrazine caused:
   - Fennick Creek: 47
   - Dunmore Creek: 0
   - Ladd Branch: 0
   - Oxley Creek: 0
   - Tessel River: 0

### atrazine_sources_2026.xlsx

1. Atrazine past each sub-watershed's station by month, 2026, kilograms:
   - Tessel River: April 7, May 155, June 179, July 32
   - Fennick Creek: April 3, May 35, June 41, July 9
   - Oxley Creek: April 6, May 107, June 106, July 17
   - Dunmore Creek: April 4, May 64, June 71, July 14
   - Ladd Branch: not sampled
2. Powdered activated carbon fed, pounds:
   - May: 3,243
   - June: 25,024
   - July: 23,776
   - August: 3,693

### raw_water_atrazine_2026.png

1. The daily raw-water result from 15 April to 31 October 2026 against the 3.0 ug/L trigger line, the 47 days above it marked.
