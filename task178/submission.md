## Tags

**Domain:** Physical & Environmental Sciences, hydrology and flood frequency.
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Carry forward Alternative D (14,700 cfs) for the Sauer pipe bridge.** The 1 per cent annual chance peak discharge at TUM-02 is 14,000 cfs, so Alternative C (12,900 cfs) falls short. Not Alternative A, which a single power-law rating through every gauging gives, because that curve runs under every gauging above about 10.3 ft and understates the floodplain peaks.

## 2. Critical Components

1. The station skew of the 46 annual peaks' base-10 logarithms is **-0.2**.
2. The 1 per cent annual chance peak discharge at TUM-02 is **14,000 cfs**.

## 3. Step-by-Step Solution

1. Took water years 1980 to 2015's peaks from tum02_annual_peaks_wy1980-2015.csv and water years 2016 to 2025's maxima from tum02_stage_15min_wy2016-2025.csv, adding 2.00 ft to stages before 1 October 2009 (tum02_station_description.pdf): 46 peak stages on the current datum.
2. Stacked the measurements in tum02_measurement_notes_1980-2004.xlsx and tum02_measurements_wy2005-2025.csv, m3/s converted at 35.3147 and old-datum gage heights raised 2.00 ft: 468 measurements.
3. Fitted the rating as a power law below a break and a floodplain term added above it, the break found by least squares on log discharge at 10.28 ft, and rated every peak stage through it.
4. Fitted log-Pearson Type III by moments of the logs with the station skew weighted with the generalized skew of 0.05 as cpc_engineering_standard_sec4_hydrology.pdf sets out: 14,000 cfs at 1 per cent, so Alternative D.
5. Work windows: dropped every 15-minute reading from arrival to departure of each visit in tum02_site_visits_2016-2025.csv, its times read on the local clock (orifice purges lift the readings inside the visit), and took the 0.47 ft controller offset off from the 11 June 2025 visit to the 27 August 2025 reset; the highest remaining reading in each 15 July to 15 September window gives the stages below.
6. Pipe crests: read scada_sauer_crossing_2019-2025.csv's timestamps as UTC before the 21 June 2022 historian replacement (cmms_work_orders_sauer_2019-2025.csv) and local after, and the level as the sensor face less the distance, 199.34 ft before and 199.84 ft after the 16 November 2022 bracket replacement (tum02_levels_log.txt); read it at TUM-02's crest reading for the levels and falls below.

## 4. Deliverable Answers

### sauer_crossing_design_flow.xlsx

1. Alternative carried forward: Alternative D.
2. 1 per cent annual chance peak discharge at TUM-02: 14,000 cfs.
3. Highest stage the river reached at TUM-02 in each 15 July to 15 September window, ft, with its date:
   - 2016: 3.40 ft on 28 August 2016
   - 2017: 3.37 ft on 26 July 2017
   - 2018: 3.29 ft on 30 July 2018
   - 2019: 3.38 ft on 14 August 2019
   - 2020: 3.30 ft on 13 August 2020
   - 2021: 3.27 ft on 10 August 2021
   - 2022: 3.45 ft on 21 August 2022
   - 2023: 3.47 ft on 18 August 2023
   - 2024: 3.88 ft on 8 August 2024
   - 2025: 3.43 ft on 9 August 2025
4. Water level at the pipe bridge radar at TUM-02's crest reading, ft NAVD88, and the fall from TUM-02, ft:
   - Water year 2020: 191.86 ft, fall 1.14 ft
   - Water year 2021: 189.32 ft, fall 1.11 ft
   - Water year 2022: 189.42 ft, fall 1.09 ft
   - Water year 2023: 193.21 ft, fall 1.25 ft
   - Water year 2024: 192.52 ft, fall 1.21 ft
   - Water year 2025: 193.76 ft, fall 1.28 ft

### sauer_crossing_frequency_curve.svg

1. The 46 annual peak discharges plotted at Weibull exceedance probabilities on a probability axis, the fitted log-Pearson Type III curve, the seven alternatives' capacities as horizontal lines with Alternative D highlighted, the 1 per cent point marked at 14,000 cfs, titled with the alternative carried forward.
