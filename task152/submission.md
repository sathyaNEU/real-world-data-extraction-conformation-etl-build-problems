## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance: a solar plant's output after its modules are replaced).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Sell 70,000 MWh of Hadley Ranch Solar's 2027 output forward: the one-year P90 of the plant with its new modules, rounded down to the nearest 1,000 MWh.**
The P50 is 73,000 MWh with a standard deviation of 1,900 MWh over the 25 weather years. Not the last twelve months carried onto the new modules with the side-by-side gain, which keeps the original modules' wear that the replacement removes and files 60,000 MWh; not the plant's first year carried with the gain, nor its whole DC-side decline restored, which bring back the inverters' losses or the dust carried between washes that the plant keeps and file 76,000 and 73,000 MWh.

## 2. Critical Components

1. The original modules' own wear since 2016: the DC energy per kWp per unit of plane-of-array irradiation at the inverters' DC input, temperature-corrected, on the days after each block's wash, is **14%** lower after the December 2025 wash than in 2016.
2. The plant's performance ratio over the base period, October 2025 to September 2026: **63.7%**.
3. The repowered plant's performance ratio, the base period's restored by the wear alone and raised by the 14.7% side-by-side gain: **85%**.
4. P50 **73,000 MWh** and standard deviation **1,900 MWh**.

## 3. Step-by-Step Solution

1. Joined hrs_scada_daily_report_2015-11-20_to_2020-03-02.csv (local days, kWh) and hadley_scada_daily_2020-03-03_to_2026-09-30.csv (UTC day starts, MWh) through scada_tag_crosswalk.csv into one daily record per inverter, B2-INV3R continuing inverter 07.
2. Base period (policy section 4.4), October 1, 2025 to September 30, 2026: PLANT-RM E_EXP less E_IMP over H_POA times 40,320 kWp gives a performance ratio of 63.7%.
3. Took each block's washes from the CLN work orders in tresco_work_orders_hadley_ranch_2015-2026.xlsx and, on the inverter-days 1 to 3 days after each wash with full operating hours, E_DC over H_POA times 2,520 kWp corrected to 25 degC with the KS-315P's -0.42 %/degC on T_MOD_IW: the level after the December 2025 wash is 14% below 2016's, the original modules' own wear.
4. On the same record the inverters' AC-to-DC ratio has fallen and the DC energy on every available day has fallen further than on the days after the washes, now one a year under Schedule 2 of the O&M agreement: losses the replacement scope keeps, so the base period carries them into 2027.
5. Divided the base period's performance ratio by the wear and multiplied by the 14.7% gain of corvane_fa-2026-114_hadley_ranch_side_by_side.pdf: 85% on 37,324.8 kWp.
6. Applied it to each full year's plane-of-array irradiation in clearfield_hadley_ranch_poa_hourly_2001-2025.csv (local calendar years 2001 to 2025): P50 73,000 MWh, sample standard deviation 1,900 MWh (policy section 4.2).
7. P50 less 1.2816 standard deviations, rounded down to the nearest 1,000 MWh (policy section 4.1): 70,000 MWh.

## 4. Deliverable Answers

### hedge_volume_2027.xlsx

1. Volume to sell forward for 2027: 70,000 MWh.
2. P50: 73,000 MWh.
3. Standard deviation: 1,900 MWh.
4. Each inverter's 2025 availability under Schedule 4 of the O&M agreement, per cent:
   - B1-INV1: 98.49%
   - B1-INV2: 97.58%
   - B1-INV3: 97.81%
   - B1-INV4: 97.63%
   - B2-INV1: 98.79%
   - B2-INV2: 99.65%
   - B2-INV3R: 98.14%
   - B2-INV4: 96.70%
   - B3-INV1: 98.29%
   - B3-INV2: 99.82%
   - B3-INV3: 99.29%
   - B3-INV4: 97.33%
   - B4-INV1: 99.27%
   - B4-INV2: 98.59%
   - B4-INV3: 97.13%
   - B4-INV4: 97.16%
5. Net energy at the delivery point over (+) or under (-) the volume sold forward, MWh:
   - 2016: +4,020 MWh
   - 2017: +6,582 MWh
   - 2018: +4,815 MWh
   - 2019: +3,964 MWh
   - 2020: -2,923 MWh
   - 2021: +534 MWh
   - 2022: +9,736 MWh
   - 2023: +4,570 MWh
   - 2024: +10,084 MWh
   - 2025: +7,715 MWh

### hedge_note_2027.pdf

1. One-page note to the treasurer recommending the 70,000 MWh sale, with a bar chart of the repowered plant's 2027 output in each weather year 2001 to 2025 and lines marking the P50 (73,000 MWh) and the volume.
