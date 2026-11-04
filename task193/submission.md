## Tags

**Domain:** Physical & Environmental Sciences, environmental monitoring and exceedance (groundwater detection monitoring at a closed municipal solid waste landfill).  
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Yes: the October 2026 event sends MW-6, MW-7 and MW-9 to verification resampling, MW-7 on sodium at 23.5 mg/L against a 20.8 mg/L limit and MW-9 on boron at 79.5 ug/L against 68.3 ug/L.** Not MW-6 alone, which limits built on every background result give (sodium 34.8 mg/L, boron 109 ug/L), because MW-1 and MW-2 sampled water from beneath the waste in the events their heads fell below their boundary piezometers'; not MW-10 as well, which only a background taken from MW-3 alone puts over a limit.

## 2. Critical Components

1. MW-1's head stood below PZ-1's on **10** of the 17 background events and MW-2's below PZ-2's on **6**; MW-3 never stood below PZ-3, so **16** background results are not background.
2. Background results: **34** chloride, **34** sodium, **33** boron.
3. Upper prediction limits: chloride **38.2 mg/L**, sodium **20.8 mg/L**, boron **68.3 ug/L**.

## 3. Step-by-Step Solution

1. Took the primary samples' reportable chloride, dissolved sodium and dissolved boron from tamarack_edd_marten_creek_2018-2021.csv (boron in mg/L, wells coded MW-01) and ridgeline_edd_MCL_2021-2026.txt (boron in ug/L, field duplicates under the parent well's code), with MW-5R in MW-5's place.
2. Took the background window of SAP section 4, April 2018 to April 2026: 50 chloride, 50 sodium and 49 boron results at MW-1, MW-2 and MW-3.
3. Computed each event's heads from mcl_gauging_rounds_2018-2026.csv and the survey in force on the gauging date in mcl_monitoring_points.xlsx, and compared each background well with its boundary piezometer: MW-1 below PZ-1 on 10 events, MW-2 below PZ-2 on 6, MW-3 never below PZ-3.
4. Left out those 16 results, water drawn from beneath the waste and so not groundwater the landfill has not affected (SAP section 4), keeping 34, 34 and 33.
5. Computed SAP section 5's limits from the natural logarithms with t at the 99th percentile: 38.2 mg/L, 20.8 mg/L and 68.3 ug/L.
6. Compared every compliance well's October 2026 result with the unrounded limits (SAP section 6): MW-6 over on chloride, sodium and boron; MW-7 over on sodium; MW-9 over on boron.
7. From fieldlog_purge_entries_2026.csv, read each well's reading set marked sample collected, corrected R-4471's logged conductivity to 25 C at 1.91 per cent a degree (FS-03 section 4), and took the purge volume as the controller counter at the sample less the counter when the pump last stopped that day (a decon rinse or bottles filled entry, zero for the day's first well), in gallons of 3.785 litres.
8. Resample MW-6, MW-7 and MW-9 within 60 days of their October samples.

## 4. Deliverable Answers

### detection_eval_2026-10.xlsx

1. Wells to resample: MW-6, MW-7 and MW-9.
2. Upper prediction limits, with the background results behind each:
   - Chloride: 38.2 mg/L, 34 results
   - Sodium, dissolved: 20.8 mg/L, 34 results
   - Boron, dissolved: 68.3 ug/L, 33 results
3. October 2026 results at the compliance wells against the limits:
   - MW-4: chloride 20.7 mg/L, sodium 12.1 mg/L, boron 41.5 ug/L; under every limit
   - MW-5R: chloride 17.7 mg/L, sodium 11.3 mg/L, boron 34.9 ug/L; under every limit
   - MW-6: chloride 82.6 mg/L, sodium 53.6 mg/L, boron 165 ug/L; over on chloride, sodium and boron
   - MW-7: chloride 33.2 mg/L, sodium 23.5 mg/L, boron 58.2 ug/L; over on sodium
   - MW-8: chloride 19.7 mg/L, sodium 11.0 mg/L, boron 45.5 ug/L; under every limit
   - MW-9: chloride 29.7 mg/L, sodium 16.5 mg/L, boron 79.5 ug/L; over on boron
   - MW-10: chloride 33.8 mg/L, sodium 18.4 mg/L, boron 34.7 ug/L; under every limit
   - MW-11: chloride 22.5 mg/L, sodium 11.5 mg/L, boron 60.1 ug/L; under every limit
4. Specific conductance at sampling, microsiemens per centimetre at 25 C, whole:
   - MW-1: 584
   - MW-2: 670
   - MW-3: 574
   - MW-4: 563
   - MW-5R: 533
   - MW-6: 1096
   - MW-7: 702
   - MW-8: 591
   - MW-9: 625
   - MW-10: 682
   - MW-11: 599
5. Purge volume before the sample, gallons, one decimal:
   - MW-1: 3.5
   - MW-2: 3.0
   - MW-3: 2.5
   - MW-4: 2.1
   - MW-5R: 1.7
   - MW-6: 2.6
   - MW-7: 3.1
   - MW-8: 4.3
   - MW-9: 3.3
   - MW-10: 3.2
   - MW-11: 3.6

### october_results_vs_limits.svg

1. One panel each for chloride, sodium and boron, every compliance well's October 2026 result a point and the upper prediction limit a dashed line labelled at its value, with MW-6, MW-7 and MW-9 marked as over a limit.
