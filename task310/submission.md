## Tags

**Domain:** Energy systems and utilities (generation capacity planning).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Run the 2027 round in Yarrandale Valley, then Sandhaven Coast in 2028, Eastbrook Metro in 2029 and Tarrock Highlands in 2030: the 2027 round would deliver about 5,900 MWh a year to its homes, 2,450 kWh a battery.**
Not Sandhaven Coast first: it leads only on the readings as recorded, because the Yarrandale Valley estate homes' inverters held their output to the home's use plus the 0.5 kW export limit, and a battery would take the energy they held back.

## 2. Critical Components

1. Energy a programme battery would deliver to a home in a year (kWh): Yarrandale Valley **2,450**; Sandhaven Coast **1,900**; Eastbrook Metro **1,500**; Tarrock Highlands **1,300**.
2. Each round's yearly energy (MWh): Yarrandale Valley **5,900**; Sandhaven Coast **4,600**; Eastbrook Metro **3,600**; Tarrock Highlands **3,100**.
3. Round years: Yarrandale Valley **2027**; Sandhaven Coast **2028**; Eastbrook Metro **2029**; Tarrock Highlands **2030**.

## 3. Step-by-Step Solution

1. Built each panel home's 2025 hours in market time (UTC+10): solar from velkora_portal_hourly_2025.parquet (local hour-beginning with its UTC offset) and ondrava_cloud_counters_2025.csv (lifetime counters at local hour end, differenced, the clock moving at 03:00 on 6 April and 02:00 on 5 October, a replacement inverter's counter from zero), and general-supply use as solar plus E1 less B1 from southmark_meter_halfhours_2025.parquet (reads stamped at the end of the half hour; E2, the controlled load, left out per guideline Appendix A).
2. Read each home's limit in southmark_connection_register_panel.csv: the 28 Yarrandale Valley homes on MEG-CZ05 (0.5 kW) and 8 Eastbrook Metro homes on MEG-L15 (1.5 kW) export no more than their limit and their inverters hold output to use plus the limit, so their recorded solar falls short of what their arrays produced.
3. Rebuilt each limited home's solar hour by hour as its array kWp (hemp_solar_systems_2025.xlsx) times the median output per kWp of its region's unlimited homes that hour, capped at its inverter's AC rating and never below what it recorded.
4. Ran the programme battery (10 kWh usable, 5 kW, 95 per cent stored on charge and 95 per cent delivered on discharge, empty on 1 January) hour by hour on each home's solar and general-supply use, charging only from solar beyond use and discharging only to use; averaged each region's 40 homes, multiplied by 2,400 and ordered the rounds by that value (guideline sections 3 and 4).
5. Eligible homes: residential NMIs in southmark_der_register_2026-09-30.csv with an active PV row and no active battery on 30 September 2026, solar connected by 30 September 2025 dated from the earliest PV row of the NMI and of the NMI it replaced (previous_nmi in southmark_nmi_standing_data_2026-09-30.csv; a reissue re-dates the rows and a replaced system ran until its successor), less premises with a Paid Battery Booster claim, matched by the claim's NMI followed to the current one or, for claims lodged before July 2022 that carry none, by normalised address, suburb and postcode.
6. Pilot energy: dropped re-sent telemetry rows (same serial and date), read each battery's lifetime counter at each quarter end (a replacement unit from zero), and counted the 24 homes whose two units report identical energy and counters every day (one Duo meter) once, while homes with two separately metered units count both.
7. Installations: collapsed module rows to certificates, applied the withdrawals and installer corrections in the amendments, took certificates sharing module serials as one installation (the later lodgement), matched A numbers through previous_no in the accreditation register, kept installers Current with expiry on or after 31 December 2027, and placed each installation by suburb (postcodes 2716 and 2905 span two regions).
8. Recommended Yarrandale Valley for 2027, the largest yearly round energy.

## 4. Deliverable Answers

### battery_rounds_2027_2030.xlsx

1. Round years: 2027 Yarrandale Valley; 2028 Sandhaven Coast; 2029 Eastbrook Metro; 2030 Tarrock Highlands.
2. Energy a programme battery would deliver to a home in a year (kWh, nearest 50):
   - Yarrandale Valley: 2,450
   - Sandhaven Coast: 1,900
   - Eastbrook Metro: 1,500
   - Tarrock Highlands: 1,300
3. Each round's yearly energy (MWh, nearest 100):
   - Yarrandale Valley: 5,900
   - Sandhaven Coast: 4,600
   - Eastbrook Metro: 3,600
   - Tarrock Highlands: 3,100
4. Homes eligible for the 2027 round on 30 September 2026:
   - Sandhaven Coast: 6,591
   - Eastbrook Metro: 8,535
   - Yarrandale Valley: 4,381
   - Tarrock Highlands: 4,539
5. Energy the 2024 pilot batteries delivered to their homes in each quarter of 2025 (MWh, one decimal):
   - Q1 2025: 324.6
   - Q2 2025: 287.8
   - Q3 2025: 271.3
   - Q4 2025: 309.9
6. Batteries installed in 2025 by installers accredited for the whole of 2027:
   - Sandhaven Coast: 410
   - Eastbrook Metro: 456
   - Yarrandale Valley: 292
   - Tarrock Highlands: 161

### round_yield_by_region.png

1. Bar chart of each round's yearly energy in round order, Yarrandale Valley's 2027 bar the tallest and highlighted.

### minister_brief_battery_rounds.pdf

1. Recommendation: run the rounds Yarrandale Valley 2027, Sandhaven Coast 2028, Eastbrook Metro 2029, Tarrock Highlands 2030; the 2027 round about 5,900 MWh a year.
