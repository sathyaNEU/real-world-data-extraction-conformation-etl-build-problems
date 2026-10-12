## Tags

**Domain:** Energy Systems & Utilities (load forecasting: rooftop PV on distribution feeders against hosting capacity).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**YRB24 should get the accelerated hosting capacity augmentation in the FY2027-28 capital works program.**
Its rooftop PV will sit 1.9 MW above its hosting capacity at 31 August 2029, 0.4 MW more than YRB22's 1.5 MW, because the Bindarra Waters bulk-buy will add about 240 systems to a feeder that hosts little. Not YRB22, which comes first when the past bulk-buys are carried to the new suburbs per home letterboxed, per owner-occupied house, per address without PV, per untapped house on the whole feeder or as an average campaign, because the seven past campaigns put systems on the same share of the owner-occupied houses still without PV when sign-ups opened and on no steady share of their letterboxes, owner-occupied houses or addresses without PV.

## 2. Critical Components

1. Each past Solar Streets campaign put systems on between **4.55** and **4.63 per cent** of the owner-occupied houses in its suburb that had no PV when sign-ups opened, **4.58 per cent** pooled.
2. The 2027 bulk-buys will add **240** systems in Bindarra Waters and **30** in Wattleview.
3. YRB24's rooftop PV at 31 August 2029 is **6.1 MW** against a spring 2029 minimum-demand hosting capacity of **4.22 MW**, **1.9 MW** above it.
4. YRB22, the runner-up, sits **1.5 MW** above its hosting capacity, a gap of **0.4 MW**.

## 3. Step-by-Step Solution

1. Summed each NMI's latest connected inverter capacity at 31 August 2026 from eg_connection_applications_20260901.csv (migrated systems' inverters from legacy_inverter_equipment.csv) by its feeder in nmi_network_model_20260831.csv, as NPP-114 defines connected capacity: 3,064 kW on YRB24 and 13,683 kW on YRB22.
2. Took each feeder's trend as NPP-114 sets it, the FY2023-24 to FY2025-26 average yearly increase in connected capacity less the program systems first connected that year, and carried it three years: 432 kW a year on YRB24 and 826 kW a year on YRB22.
3. For each campaign in solar_streets_program_summary.xlsx, counted the suburb's owner-occupied houses (land use 02, rating R1 in merindah_rates_roll_2026-27.csv) none of whose NMIs (nmi_property_xref_2026.csv) had an application, other than a withdrawn one, received before sign-ups opened, and the connected systems carrying its program reference: 4.55 to 4.63 per cent each, 4.58 per cent pooled.
4. Applied the pooled rate to the owner-occupied houses without PV at 31 August 2026 less the suburb's FY2025-26 first applications from such houses (5,275 in Bindarra Waters, 668 in Wattleview): 241.6 and 30.6 systems, at the feeder's FY2025-26 average new inverter (7.25 kW on YRB24, 6.67 kW on YRB27) 1,752 kW and 204 kW.
5. Subtracted the spring 2029 minimum-demand hosting capacity in yarrabin_hosting_capacity_assessment_2026.pdf from each forecast: YRB24 6.1 MW against 4.22 MW, 1.9 MW above; YRB22 1.5 MW above.
6. Matched NMIs connected at 31 August 2026 against active connections in der_register_extract_yarrabin_20260905.csv, reading 11-character NMIs at their first ten characters and builders' temporary NMIs at the permanent NMI in nmi_reallocations_2019-2026.csv: the per-feeder counts in block 4.
7. Summed the storage capacity of each active AC connection with a battery once, since it repeats on every battery module row, by feeder: 2,440 kWh on YRB21 down to 390 kWh on YRB24.
8. Ranked the feeders by forecast PV above hosting capacity, as NPP-114 assigns a single augmentation: YRB24 first by 0.4 MW over YRB22.

## 4. Deliverable Answers

### feeder_upgrade_2029.xlsx

1. Feeder to get the augmentation: YRB24
2. YRB24's rooftop PV above its hosting capacity at 31 August 2029: 1.9 MW
3. Runner-up: YRB22, 1.5 MW above its hosting capacity
4. Gap between them: 0.4 MW
5. Systems each 2027 bulk-buy will add:
   - Bindarra Waters: 240
   - Wattleview: 30
6. Connected systems at 31 August 2026 the DER Register does not show, and active DER Register sites with no connected system:
   - YRB21: 12 not shown, 11 sites with no connected system
   - YRB22: 8 not shown, 12 sites with no connected system
   - YRB23: 11 not shown, 10 sites with no connected system
   - YRB24: 2 not shown, 8 sites with no connected system
   - YRB25: 6 not shown, 5 sites with no connected system
   - YRB26: 14 not shown, 4 sites with no connected system
   - YRB27: 14 not shown, 9 sites with no connected system
   - YRB28: 12 not shown, 4 sites with no connected system
7. Battery storage at active DER Register sites:
   - YRB21: 2,440 kWh
   - YRB22: 1,770 kWh
   - YRB23: 1,800 kWh
   - YRB24: 390 kWh
   - YRB25: 900 kWh
   - YRB26: 1,590 kWh
   - YRB27: 1,740 kWh
   - YRB28: 1,310 kWh

### yarrabin_pv_vs_hosting_2029.png

1. Bar chart with one bar per feeder, YRB21 to YRB28, for its forecast rooftop PV connected at 31 August 2029, each feeder's spring 2029 minimum-demand hosting capacity marked across its bar, YRB24 highlighted and labelled 1.9 MW above its hosting capacity of 4.22 MW, and YRB22 labelled 1.5 MW above.
