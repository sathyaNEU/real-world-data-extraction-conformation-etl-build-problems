## Tags

**Domain:** Energy Systems & Utilities (load forecasting: a distribution substation's summer planning peak once conservation voltage reduction runs on every feeder).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Breckwater must transfer 1.0 MW off Dunraith in summer 2027, 2.0 MW in 2028, 3.0 MW in 2029, 4.0 MW in 2030 and 5.0 MW in 2031.** With the voltage cut taking 1.1 per cent off at the planning peak, the planning peaks are 105, 106, 107, 108 and 109 MW against the firm rating. Not the pilot's relief over every hour (2.4 per cent, 0.0 MW in 2027), which carries the night's voltage-sensitive load into the peak; not the relief at each day's peak hour (1.5 per cent, 0.5 MW in 2027), which carries mild days whose peak holds less air conditioning.

## 2. Critical Components

1. The weather-normal peak (criteria 3.2) is **102.9 MW** at the 2024 level, **105.9 MW** in 2027 before the voltage cut.
2. The 3.5 per cent voltage cut takes **1.1 per cent** off the load at the planning peak (**1.1 MW** in 2027), read from the 2025 pilot's afternoons on days at 99 F or more.
3. The planning peaks for 2027 to 2031 are **105, 106, 107, 108 and 109 MW**.

## 3. Step-by-Step Solution

1. Joined DUNRAITH_FDR_KW_2022-2023.csv (kW, each hour labelled at its end) to dunraith_feeder_mw_2024-2026.csv (MW, labelled at its start; Bad hours left out per criteria 5) and took each day's highest hourly sum of the feeders.
2. Took each local day's maximum from mossford_ap_obs_2022-2026.csv (UTC, Celsius) and fitted criteria 3.2's line over the 561 days at 85 F or more: 3.45 MW per F, 102.9 MW at 101 F, carried from 2024 at the BEC_load_forecast_2025.xlsx base case, 0.95 per cent a year compounded: 105.9 MW in 2027.
3. Rebuilt each hour's setting from VR_event_log_DUN_2025.csv and compared the ratio of DUN-2, DUN-5 and DUN-7 to the other feeders in CVR hours and normal hours, 16:00 to 21:00: the relief falls from 2.3 per cent on days under 85 F to 1.1 per cent on days at 99 F or more (65 CVR and 50 normal hours), the conditions of the planning peak.
4. Took 1.1 per cent off each summer's weather-normal peak for the 2027 operating plan's CVR on every feeder (criteria 3.3): planning peaks 105, 106, 107, 108, 109 MW.
5. Rounded each planning peak's excess over the 104.0 MW firm rating up to whole 0.5 MW switching blocks (criteria 4.1): 1.0, 2.0, 3.0, 4.0, 5.0 MW.
6. Ask A: multiplied each day's KWH in mdms_xfmr_daily_kwh_20260601_20260930.csv by METER_MULT in DUN_transformer_register_2026-10.xlsx from the transformer's METER_SET date (the LP-3 services that went onto CT metering in June read whole kWh before it) and counted June on the old feeder for every transformer whose PROTECTIVE_DEVICE lies beyond S-4471, S-6120 or S-1302 in the register's Devices sheet (SO-2026-114_Dunraith.pdf): DUN-1 16,600, DUN-2 16,210, DUN-3 17,670, DUN-4 11,150, DUN-5 16,980, DUN-6 8,990, DUN-7 14,810, DUN-8 15,850 MWh.
7. Ask B: summed recorders 41-2207 and 41-2208 of MV90_DP0417_202606-202609.csv (the transformers' 24.9 kV side in WPC_Exhibit_A_delivery_points.pdf, not the 69 kV line terminal 41-2391), moved the T2 replacement recorder's stamps up 15 minutes from its repeated stamp of 9 June, put the UTC interval ends on CDT and took each of the ten hottest local days' highest 15-minute demand: 2026-06-14 94.7, 2026-06-15 99.1, 2026-06-26 97.3, 2026-07-18 91.0, 2026-08-05 92.9, 2026-08-06 101.3, 2026-08-08 101.0, 2026-08-09 114.1, 2026-08-28 97.1, 2026-09-28 95.7 MW.
8. Transfer 1.0, 2.0, 3.0, 4.0, 5.0 MW off Dunraith in the summers 2027 to 2031.

## 4. Deliverable Answers

### dunraith_planning.xlsx

1. Transfer requirement by summer, MW:
   - 2027: 1.0
   - 2028: 2.0
   - 2029: 3.0
   - 2030: 4.0
   - 2031: 5.0
2. Planning peak by summer, MW to the nearest MW:
   - 2027: 105
   - 2028: 106
   - 2029: 107
   - 2030: 108
   - 2031: 109
3. Energy each feeder delivered to members' meters, June to September 2026, MWh to the nearest 10:
   - DUN-1: 16,600
   - DUN-2: 16,210
   - DUN-3: 17,670
   - DUN-4: 11,150
   - DUN-5: 16,980
   - DUN-6: 8,990
   - DUN-7: 14,810
   - DUN-8: 15,850
4. Peak 15-minute demand of the feeders on the ten hottest days of summer 2026, MW to one decimal:
   - 2026-06-14: 94.7
   - 2026-06-15: 99.1
   - 2026-06-26: 97.3
   - 2026-07-18: 91.0
   - 2026-08-05: 92.9
   - 2026-08-06: 101.3
   - 2026-08-08: 101.0
   - 2026-08-09: 114.1
   - 2026-08-28: 97.1
   - 2026-09-28: 95.7
5. Chart sheet: the planning peak for each summer from 2027 to 2031 in columns against the firm rating line, with the weather-normal peak before the voltage cut as a dashed line.
