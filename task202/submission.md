## Tags

**Domain:** Physical and environmental sciences (pollution source attribution).
**Analytical objective:** Root-cause analysis.

## 1. Final Recommendation

**Back programme C, tertiary filtration at the Hollinsby works: it keeps 222 kg of phosphorus a season out of Selwith Water's surface water, 186 kg more than the runner-up, programme D (the Mill Beck wetland, 36 kg).** Not programme B at the Brathwick works, which carries the largest June-to-September load into the lake, nor programme A on the farms: both act on the River Lenning, which is denser than the surface water on every summer day and enters below the thermocline, so neither keeps any phosphorus out of the surface water.

## 2. Critical Components

1. The Lenning's daily mean water was denser than the buoy's 0 to 5 m water on **122 of 122**, **122 of 122** and **122 of 122** June-to-September days in 2024, 2025 and 2026, so programmes A and B keep out **0 kg**.
2. Hollinsby's effluent is warmer than the surface water in every season month, and programme C keeps out **229**, **221** and **216 kg** (2024 to 2026), **222 kg** on average.
3. Programme D keeps out **36**, **37** and **36 kg**, **36 kg** on average.

## 3. Step-by-Step Solution

1. Read lenning_foot_hourly_validated.csv over lenning_foot_hourly_provisional.csv where both hold an hour, moved the UK clock readings to UTC and took each day's mean water temperature.
2. Averaged the sensors down to 5 m in fellside_buoy_thermistor_daily.csv each day and compared water densities at the two temperatures: the river was denser on every June-to-September day, sinking below the thermocline, where fellside_buoy_sondes_daily.csv shows the 10 m conductivity rising through each summer.
3. Compared Hollinsby's monthly effluent temperature in fellmoor_wwtw_monthly_returns.xlsx with the surface water's monthly mean: warmer in every month June to September.
4. Applied the credited reductions in programme_appraisals_2027.xlsx (C 71%, D 50%) to Hollinsby's June-to-September TP loads in the returns and to the Mill Beck monthly loads, and averaged the seasons: C 222 kg, D 36 kg.
5. For 1 October 2023 to 30 April 2024 added the Brankell Beck at Howe hourly flow from regulator_gauged_flows_hourly.csv to the station's flow (the Lenning Bridge feed until 1 June 2024, above the Brankell Beck's confluence), and multiplied each hour's flow by the bottle that took its sub-sample, the storm bottles for the hours a day bottle's sub-sample count shows it skipped: 51.4 million m3 and 5,200 kg.
6. Took the north basin's 0-5 m results in fellside_lake_lab_results.csv under NB until 31 March 2025 and SWL01 from 1 April 2025 (NB then holds the Hollinsby Bay samples, with no 20 m bottle) and averaged June to September.
7. Counted each block's shared-stack visit in connect_right_visits_export.csv as every flat under that UPRN in hollinsby_address_register_extract.csv and dated each visit by its visit reference: 126 found, 39 fixed by 30 September 2026, 87 not.
8. Ranked the programmes on the fund's measure: C first, D second.

## 4. Deliverable Answers

### selwith_fund_recommendation_2027.pdf

1. Programme C, Hollinsby WwTW tertiary filtration: 222 kg of phosphorus a season.
2. Runner-up: programme D, Mill Beck outfall treatment wetland, 36 kg.
3. Bar chart of every programme's figure for 2024, 2025 and 2026 on page 1.

### selwith_phosphorus_workings.xlsx

1. Each programme's figure for 2024, 2025 and 2026 (kg):
   - A: 0, 0, 0
   - B: 0, 0, 0
   - C: 229, 221, 216
   - D: 36, 37, 36
2. River Lenning into the lake, October 2023 to April 2024: inflow 51.4 million m3, phosphorus load 5,200 kg.
3. North basin June-to-September mean surface water: 2025 total phosphorus 29.9 ug/l and chlorophyll a 8.0 ug/l; 2026 total phosphorus 29.2 ug/l and chlorophyll a 7.9 ug/l.
4. Connect Right: 126 dwellings found draining foul water to the surface-water drains, 39 confirmed fixed by 30 September 2026, 87 not.
