## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance: a dairy processing site's production bores, the lowest level each reaches through the design drought on the summer bore plan).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Do not adopt the 2026-27 summer bore plan as drafted: it fails the drought test at PB3, whose lowest pumping water level reaches 35.5 m below measuring point in February and in March against a minimum operating level of 35.0 m.** PB9's October 2026 constant-rate test drew PB3 down by 3.0 m at the plan's 4.40 ML/d. Not the plan holding: each bore's own drought curve leaves out PB9's draw on its neighbours. Not PB4 failing: PB4 sits nearer PB9 on the map, but the test moved it 0.5 m.

## 2. Critical Components

1. At its planned 4.40 ML/d PB9 lowers PB3 by **3.0 m** and PB4 by **0.5 m**, the dip its 7 to 14 October 2026 constant-rate test left in their daily levels.
2. PB3's lowest level is **35.5 m** below measuring point in February and **35.5 m** in March, against its minimum operating level of 35.0 m.
3. Every other bore, PB9 included, stays above its minimum operating level in every month.

## 3. Step-by-Step Solution

1. Conformed kaitanga_bores_daily_2014-2026.csv: mapped the KTG-BH tags used before 14 May 2019 to PB1 to PB8, dropped the August 2021 batch the gateway sent twice, and turned each level into a reduced level with the bore register's ground level and measuring-point height.
2. Moved PB9_logger_LT5-2408817_2026-10.csv from UTC to NZDT, summed its discharge into each local day's take, and took PB9's own drawdown and static level from the last day of the constant-rate stage and the hours before the step test.
3. Fitted each existing bore's level less MB1's level (MRC_MB1_groundwater_level_daily.csv) on every bore's daily take, PB9's test days included, by least squares over 2014 to 2026; PB9's coefficient on each bore is its drawdown there per ML/d.
4. Took MB1's lowest level in each month from December 2019 to March 2020 (SWS-03 section 3) and each bore's planned take from kaitanga_summer_bore_plan_2026-27.xlsx, and computed each bore's lowest pumping water level by month, PB9's from its test with its neighbours' takes carried by reciprocity.
5. Compared each with the register's minimum operating level (SWS-03 section 4): PB3 fails in February and March, and nothing else fails.
6. For the permit meters, differenced each meter's 15-minute totaliser in MRC_permit_meter_telemetry_2025-26.csv across its rollovers, moved NZST to NZ local time, and gave each meter to the bore whose SCADA daily take it tracks: WM-30455 reads PB2, WM-30456 PB1, WM-33119 PB6, WM-33120 PB5, and WM-40958 is PB4's meter from 17 February 2026.
7. For electricity, moved pump_icp_interval_data_2025-26.csv from UTC to NZ local time, read the PB2 meter fitted on 11 February 2026 at x40 (kaitanga_icp_meter_register.csv), split switchboards SB-3 and SB-4 between their pumps by daily run hours times motor kW, and divided by the metered megalitres.
8. Recommended not adopting the plan as drafted: PB3 fails the drought test in February and March.

## 4. Deliverable Answers

### kaitanga_summer_test_2026-27.xlsx

1. Result: the plan fails the drought test; PB3 falls below its minimum operating level in February and March.
2. Lowest pumping water level by month, metres below measuring point, nearest 0.5 m:
   - PB1: December 28.0, January 29.5, February 30.0, March 30.0
   - PB2: December 28.5, January 31.5, February 32.0, March 32.0
   - PB3: December 34.0, January 34.5, February 35.5, March 35.5
   - PB4: December 33.0, January 34.0, February 35.0, March 34.0
   - PB5: December 29.5, January 30.5, February 31.5, March 31.0
   - PB6: December 29.5, January 30.0, February 30.5, March 29.0
   - PB7: December 28.5, January 29.0, February 29.5, March 30.0
   - PB8: December 26.5, January 27.0, February 28.0, March 28.0
3. PB9 holds in every month.
4. Pump electricity per megalitre the permit meters measured, whole kWh/ML:
   - PB1: Jul-Sep 2025 294, Oct-Dec 2025 293, Jan-Mar 2026 293, Apr-Jun 2026 296
   - PB2: Jul-Sep 2025 302, Oct-Dec 2025 301, Jan-Mar 2026 300, Apr-Jun 2026 303
   - PB3: Jul-Sep 2025 303, Oct-Dec 2025 305, Jan-Mar 2026 310, Apr-Jun 2026 316
   - PB4: Jul-Sep 2025 337, Oct-Dec 2025 335, Jan-Mar 2026 332, Apr-Jun 2026 329
   - PB5: Jul-Sep 2025 267, Oct-Dec 2025 265, Jan-Mar 2026 264, Apr-Jun 2026 273
   - PB6: Jul-Sep 2025 258, Oct-Dec 2025 253, Jan-Mar 2026 260, Apr-Jun 2026 254
   - PB7: Jul-Sep 2025 261, Oct-Dec 2025 263, Jan-Mar 2026 268, Apr-Jun 2026 258
   - PB8: Jul-Sep 2025 343, Oct-Dec 2025 339, Jan-Mar 2026 333, Apr-Jun 2026 345
5. Volume by bore as the permit meters measured it, ML to one decimal:
   - PB1: Jul-Sep 2025 205.1, Oct-Dec 2025 323.1, Jan-Mar 2026 283.0, Apr-Jun 2026 140.0
   - PB2: Jul-Sep 2025 155.5, Oct-Dec 2025 226.4, Jan-Mar 2026 229.6, Apr-Jun 2026 124.2
   - PB3: Jul-Sep 2025 188.3, Oct-Dec 2025 296.9, Jan-Mar 2026 260.4, Apr-Jun 2026 146.6
   - PB4: Jul-Sep 2025 168.0, Oct-Dec 2025 275.5, Jan-Mar 2026 232.1, Apr-Jun 2026 165.4
   - PB5: Jul-Sep 2025 167.7, Oct-Dec 2025 279.0, Jan-Mar 2026 248.2, Apr-Jun 2026 130.3
   - PB6: Jul-Sep 2025 153.6, Oct-Dec 2025 231.8, Jan-Mar 2026 181.5, Apr-Jun 2026 133.1
   - PB7: Jul-Sep 2025 173.0, Oct-Dec 2025 284.9, Jan-Mar 2026 249.7, Apr-Jun 2026 152.5
   - PB8: Jul-Sep 2025 162.6, Oct-Dec 2025 254.2, Jan-Mar 2026 242.1, Apr-Jun 2026 161.1

### borefield_plan_2026-27.pptx

1. Call: do not adopt the plan as drafted; PB3 falls below its minimum operating level in February and March.
2. Chart on slide 1: each bore's margin over its minimum operating level by month, PB3 below zero in February and March.
