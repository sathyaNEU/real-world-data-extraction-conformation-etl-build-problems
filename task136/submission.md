## Tags

**Domain:** Energy Systems & Utilities (load forecasting: rooftop PV on distribution feeders against hosting capacity).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**YRB27 should get the accelerated hosting capacity augmentation in the FY2027-28 capital works program.**
Its rooftop PV will sit 1.9 MW above its hosting capacity at 31 August 2029, 0.2 MW more than YRB24's 1.7 MW. Not YRB24, which comes first when the past bulk-buys' installed systems are carried onto the 2026 suburbs, because more than half of the households the past bulk-buys signed up would have gone solar within three years anyway, so Bindarra Waters adds 1.7 MW by the design point. Not YRB22, which leads only before the bulk-buys are counted.

## 2. Critical Components

1. The Bindarra Waters bulk-buy adds **1.7 MW** to YRB24 by 31 August 2029 and the Wattleview bulk-buy **0.7 MW** to YRB27.
2. YRB27's rooftop PV at 31 August 2029 is **16.1 MW**, **1.9 MW** above its spring 2029 minimum-demand hosting capacity.
3. YRB24, the runner-up, sits **1.7 MW** above its hosting capacity, a gap of **0.2 MW**.

## 3. Step-by-Step Solution

1. Summed each NMI's latest connected inverter capacity at 31 August 2026 from eg_connection_applications_20260901.csv (migrated systems' inverters from legacy_inverter_equipment.csv) by its feeder in nmi_network_model_20260831.csv, as NPP-114 defines connected capacity: 11,645 kW on YRB27 and 17,845 kW on YRB24.
2. Carried each feeder's trend three years as NPP-114 sets it (the FY2023-24 to FY2025-26 average yearly increase in connected capacity less the program systems first connected that year): 1,245 kW a year on YRB27 and 1,935 kW a year on YRB24, base forecasts of 15,380 kW and 23,648 kW.
3. For each campaign in solar_streets_program_summary.xlsx, counted the first applications (each house's earliest application other than a withdrawn one, by received date, program applications included) from the suburb's owner-occupied houses (land use 02, rating R1 in merindah_rates_roll_2026-27.csv, through nmi_property_xref_2026.csv) in the three years from sign-ups opening (to 31 August 2026 for BNR23 and PBG24) and in the year before, and the houses without PV at the opening.
4. Set each campaign suburb's year before against the same months in the suburbs whose own campaign opens after its window: the seven campaigns added 627.8 systems above what their suburbs would have lodged without them, on 15,349 owner-occupied houses without PV at their openings (4.09 per hundred).
5. Carried that rate onto the owner-occupied houses without PV on 1 September 2026 (4,537 in Bindarra Waters, 1,857 in Wattleview): 185.6 and 76.0 systems by 31 August 2029, at the feeder's FY2025-26 average new inverter as NPP-114 sizes them (9.15 kW on YRB24, 9.35 kW on YRB27), 1.7 MW and 0.7 MW.
6. From der_register_extract_yarrabin_20260901.csv, read each NMI at its first ten characters and a builder's temporary NMI at its replacement in nmi_reallocations_2019-2026.csv, and counted the NMIs with an active AC connection by the feeder the network model shows supplying them, a site first lodged in FY2025-26 when the earliest registration of any of its connections, decommissioned ones included, falls in that year: the counts in block 4.
7. Summed the active connections' inverter ratings, counting once a two-inverter connection lodged before July 2024 whose every row carries the connection's total (the model's nameplate times its rows), and their battery storage, counting once a Sungrow SBR stack whose every module row carries the stack's total: the capacities and storage in block 4.
8. Subtracted the spring 2029 minimum-demand hosting capacity in yarrabin_hosting_capacity_assessment_2026.pdf from each feeder's forecast and ranked the feeders: YRB27 16.1 MW, 1.9 MW above its hosting capacity, ahead of YRB24 at 1.7 MW above, a 0.2 MW gap, so YRB27 takes the augmentation.

## 4. Deliverable Answers

### feeder_upgrade_2029.xlsx

1. Feeder to get the augmentation: YRB27
2. YRB27's rooftop PV above its hosting capacity at 31 August 2029: 1.9 MW
3. Runner-up: YRB24, 1.7 MW above its hosting capacity
4. Gap between them: 0.2 MW
5. PV each 2026 bulk-buy will add by 31 August 2029:
   - Bindarra Waters (YRB24): 1.7 MW
   - Wattleview (YRB27): 0.7 MW
6. Active DER Register sites each feeder supplies, those first lodged in FY2025-26, and their inverter capacity and battery storage:
   - YRB21: 3,443 sites, 98 first lodged in FY2025-26, 19,280 kW, 3,260 kWh
   - YRB22: 3,194 sites, 177 first lodged in FY2025-26, 18,950 kW, 2,780 kWh
   - YRB23: 2,128 sites, 91 first lodged in FY2025-26, 12,350 kW, 2,000 kWh
   - YRB24: 2,783 sites, 255 first lodged in FY2025-26, 18,110 kW, 2,560 kWh
   - YRB25: 3,680 sites, 204 first lodged in FY2025-26, 21,770 kW, 3,080 kWh
   - YRB26: 2,180 sites, 75 first lodged in FY2025-26, 12,200 kW, 2,280 kWh
   - YRB27: 1,838 sites, 158 first lodged in FY2025-26, 11,800 kW, 1,560 kWh
   - YRB28: 2,927 sites, 159 first lodged in FY2025-26, 16,980 kW, 2,510 kWh

### yarrabin_pv_vs_hosting_2029.png

1. Bar chart with one bar per feeder, YRB21 to YRB28, for its forecast rooftop PV connected at 31 August 2029, each feeder's spring 2029 minimum-demand hosting capacity marked across its bar, YRB27 highlighted and labelled 1.9 MW above its hosting capacity, and YRB24 labelled 1.7 MW above.
