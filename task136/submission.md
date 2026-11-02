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
6. Fitted each bus section's flow in yarrabin_zs_22kv_check_meters_jun-aug2026.csv (import less export, each interval end closing its half hour) on its four feeder heads in yarrabin_zs_feeder_heads_scada_jun-aug2026.csv: the meter is each feeder head's historian value times its bay's own factor, to within the two systems' measurement error (1.25 on YRB21 and YRB28, 1.6 on YRB22 and YRB27, 1.2 on YRB23 and YRB26, 1.5 on YRB24 and YRB25), which no single factor per bus section reproduces.
7. Multiplied each feeder head's historian values by its factor and summed its reverse flow (from the feeder back into the 22 kV bus) half hour by half hour over June, July and August 2026, with its largest half hour: the energy and peaks in block 4.
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
6. Energy each feeder sent back to the zone substation in June, July and August 2026, and its largest half-hour reverse flow over those months:
   - YRB21: 1,030, 980 and 1,140 MWh; 12.0 MW
   - YRB22: 850, 810 and 960 MWh; 10.8 MW
   - YRB23: 280, 280 and 340 MWh; 5.4 MW
   - YRB24: 660, 620 and 750 MWh; 9.2 MW
   - YRB25: 870, 820 and 980 MWh; 11.2 MW
   - YRB26: 220, 210 and 260 MWh; 4.5 MW
   - YRB27: 130, 150 and 190 MWh; 3.7 MW
   - YRB28: 710, 670 and 820 MWh; 9.0 MW

### yarrabin_pv_vs_hosting_2029.png

1. Bar chart with one bar per feeder, YRB21 to YRB28, for its forecast rooftop PV connected at 31 August 2029, each feeder's spring 2029 minimum-demand hosting capacity marked across its bar, YRB27 highlighted and labelled 1.9 MW above its hosting capacity, and YRB24 labelled 1.7 MW above.
