## Tags

**Domain:** Energy Systems & Utilities (load forecasting: rooftop PV on distribution feeders against hosting capacity).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**YRB27 should get the accelerated hosting capacity augmentation in the FY2027-28 capital works program.**
Its rooftop PV will sit 1.9 MW above its hosting capacity at 31 August 2029, 0.5 MW more than YRB24's 1.4 MW, because the Wattleview bulk-buy will add 1.7 MW to it. Not YRB24, which comes first when the past bulk-buys are carried to the new suburbs per home letterboxed or per owner-occupied house still without PV, because the seven past campaigns installed a steady 1.03 to 1.35 systems for every first application their suburb's owner-occupied houses lodged in the year before sign-ups opened and no steady share of any pool, so Bindarra Waters' slow-moving estate adds only 0.4 MW.

## 2. Critical Components

1. The Wattleview bulk-buy adds **1.7 MW** to YRB27 and the Bindarra Waters bulk-buy **0.4 MW** to YRB24.
2. YRB27's rooftop PV at 31 August 2029 is **25.2 MW**, **1.9 MW** above its spring 2029 minimum-demand hosting capacity.
3. YRB24, the runner-up, sits **1.4 MW** above its hosting capacity, a gap of **0.5 MW**.

## 3. Step-by-Step Solution

1. Summed each NMI's latest connected inverter capacity at 31 August 2026 from eg_connection_applications_20260901.csv (migrated systems' inverters from legacy_inverter_equipment.csv) by its feeder in nmi_network_model_20260831.csv, as NPP-114 defines connected capacity: 17,938 kW on YRB27 and 4,637 kW on YRB24.
2. Took each feeder's trend as NPP-114 sets it, the FY2023-24 to FY2025-26 average yearly increase in connected capacity less the program systems first connected that year, and carried it three years: 1,852 kW a year on YRB27 and 498 kW a year on YRB24.
3. For each campaign in solar_streets_program_summary.xlsx, counted the first applications (each NMI's earliest application other than a withdrawn one) from the suburb's owner-occupied houses (land use 02, rating R1 in merindah_rates_roll_2026-27.csv, through nmi_property_xref_2026.csv) received in the 12 months before sign-ups opened, and the connected systems carrying its program reference: 505 systems on 431 first applications, 1.172 per application, pooled as NPP-114 sets.
4. Applied 1.172 to each 2026 suburb's first applications from 1 September 2025 to 31 August 2026 (209 in Wattleview, 52 in Bindarra Waters): 244.9 and 60.9 systems, at the feeder's FY2025-26 average new inverter (6.97 kW on YRB27, 6.50 kW on YRB24) 1.7 MW and 0.4 MW.
5. Subtracted the spring 2029 minimum-demand hosting capacity in yarrabin_hosting_capacity_assessment_2026.pdf from each forecast and ranked the feeders as NPP-114 assigns a single augmentation: YRB27 1.9 MW above, YRB24 1.4 MW above, a 0.5 MW gap.
6. From der_register_extract_yarrabin_20260901.csv, read each NMI at its first ten characters and a builder's temporary NMI at its replacement in nmi_reallocations_2019-2026.csv, and counted the NMIs with an active AC connection by the feeder the network model shows supplying them, a site first lodged in FY2025-26 when the earliest registration of any of its connections, decommissioned ones included, falls in that year: the counts in block 4.
7. Summed the active connections' inverter ratings, counting once a two-inverter connection lodged before July 2024 whose every row carries the connection's total (the model's nameplate times its rows), and their battery storage, counting once a Sungrow SBR stack whose every module row carries the stack's total: the capacities and storage in block 4.

## 4. Deliverable Answers

### feeder_upgrade_2029.xlsx

1. Feeder to get the augmentation: YRB27
2. YRB27's rooftop PV above its hosting capacity at 31 August 2029: 1.9 MW
3. Runner-up: YRB24, 1.4 MW above its hosting capacity
4. Gap between them: 0.5 MW
5. PV each 2026 bulk-buy will add:
   - Bindarra Waters (YRB24): 0.4 MW
   - Wattleview (YRB27): 1.7 MW
6. Active DER Register sites each feeder supplies, those first lodged in FY2025-26, and their inverter capacity and battery storage:
   - YRB21: 2,323 sites, 82 first lodged in FY2025-26, 14,000 kW, 1,940 kWh
   - YRB22: 3,448 sites, 130 first lodged in FY2025-26, 20,680 kW, 2,410 kWh
   - YRB23: 1,713 sites, 65 first lodged in FY2025-26, 10,860 kW, 1,310 kWh
   - YRB24: 702 sites, 68 first lodged in FY2025-26, 4,730 kW, 750 kWh
   - YRB25: 717 sites, 44 first lodged in FY2025-26, 4,850 kW, 650 kWh
   - YRB26: 1,996 sites, 35 first lodged in FY2025-26, 10,830 kW, 1,710 kWh
   - YRB27: 2,729 sites, 252 first lodged in FY2025-26, 18,040 kW, 2,950 kWh
   - YRB28: 1,781 sites, 62 first lodged in FY2025-26, 10,340 kW, 1,380 kWh

### yarrabin_pv_vs_hosting_2029.png

1. Bar chart with one bar per feeder, YRB21 to YRB28, for its forecast rooftop PV connected at 31 August 2029, each feeder's spring 2029 minimum-demand hosting capacity marked across its bar, YRB27 highlighted and labelled 1.9 MW above its hosting capacity, and YRB24 labelled 1.4 MW above.
