## Tags

**Domain:** General Statistics & Data Science (data integration: a farming company's water year groundwater extraction integrated from the electric utility's interval energy, its wells' pump efficiency tests, their water level loggers and the upper wells' totalizers into the groundwater sustainability agency's extraction return).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Ochre Flats should buy 250 acre-feet of transfer water and have it recorded with the Sallow Plains GSA before the December 15 true-up.**
Its wells pumped 15,583 acre-feet in water year 2026 against 15,358.9 available, 224 over, and the agency records transfers only in whole blocks of 50. Not no purchase, which converting each unmetered well's energy at its pump test's kilowatt-hours per acre-foot gives (15,020 acre-feet, 339 inside), because the deep wells were tested near the confined aquifer's late-summer low and pumped most of their water on higher spring and early-summer levels, where each kilowatt-hour lifted more water; not run hours times the tested flow (14,719 acre-feet), which misses the same change.

## 2. Critical Components

1. The water available for water year 2026 is **15,358.9** acre-feet: the 14,878.9 acre-foot allocation plus 480 carried over.
2. The metered upper wells pumped **3,270** acre-feet by their totalizers.
3. The unmetered wells, each interval's energy converted at that interval's total head, pumped **12,313** acre-feet.
4. The ranch pumped **15,583** acre-feet, **224** over what it had available.

## 3. Step-by-Step Solution

1. Linked each well's service agreements in vrp_usage_export_2025-09-01_2026-03-31.csv (hourly kWh, local prevailing time, both 01:00 rows of 2 November) and vrp_interval_data_2026-04-01_2026-10-31.csv (15-minute Wh, UTC) to its well through the prior and current account columns of ochre_flats_well_register.xlsx, keeping water year 2026, 1 October 2025 to 30 September 2026 local time (notice section 3).
2. Took each pump's August or September 2025 report in pump_tests/ (the 2023 reports predate the 2024 pump replacements the register dates) for its pumping water level, total head and overall plant efficiency.
3. Differenced the W-01 to W-04 reads of 1 October 2025 and 1 October 2026 in totalizer_reads_wy2026.xlsx, through each rollover and W-03's June 17 meter exchange: 3,270 acre-feet.
4. Converted each other well's interval energy at 1.0241 times total head over the test's efficiency (the reports' own definition), the total head being the test's plus the interval's depth to water below ground (the mean logger reading from the interval's start to its end, less the register's MP height) less the test's pumping level: 12,313 acre-feet.
5. Summed the wells' whole-acre-foot volumes (notice section 3), 15,583, set them against the allocation plus carryover (section 2), 224 over, and rounded up to whole blocks of 50 (section 4): 250.
6. Found each well's spring and fall static depth as the first logger reading in each window (section 5) at which the power exports show the pump off for the preceding 24 hours, less the MP height; for the four Levelogger 5 wells the depth is the register's sensor depth less the reading's total pressure head net of the shop barologger at the same instant (its clock on UTC, per logger_download_log.csv), and W-02's and W-04's spring readings come from the loggers the download log places in each well before the June 10 swap.
7. Priced each April to September 2026 interval's kWh at its time-of-use period in local time (vrp_agricultural_tou_schedules_2026.pdf, holidays off-peak), on AG-2T before June 1 for the agreements vrp_rate_change_confirmation_2026-05-14.pdf moves to AG-3T and on the register's schedule otherwise.
8. Recommended buying 250 acre-feet before December 15.

## 4. Deliverable Answers

### wy2026_extraction_return.csv

1. Each well's water year 2026 volume in whole acre-feet and its method (each graded within 1 per cent, the ranch within 0.5 per cent):
   - W-01: 824, METER
   - W-02: 864, METER
   - W-03: 838, METER
   - W-04: 744, METER
   - W-05: 905, CALCULATED
   - W-06: 699, CALCULATED
   - W-07: 1,121, CALCULATED
   - W-08: 1,219, CALCULATED
   - W-09: 1,165, CALCULATED
   - W-10: 1,313, CALCULATED
   - W-11: 1,005, CALCULATED
   - W-12: 1,169, CALCULATED
   - W-13: 1,169, CALCULATED
   - W-14: 1,216, CALCULATED
   - W-15: 1,332, CALCULATED
2. The return carries every well's twelve monthly volumes, October 2025 to September 2026, in whole acre-feet on the agency's template.
3. Each well's spring and fall 2026 static depth to water, feet below ground to one decimal:
   - W-01: spring 139.0, fall 145.1
   - W-02: spring 120.2, fall 126.1
   - W-03: spring 123.9, fall 128.5
   - W-04: spring 124.1, fall 127.2
   - W-05: spring 125.0, fall 129.8
   - W-06: spring 129.1, fall 136.3
   - W-07: spring 258.2, fall 370.7
   - W-08: spring 246.1, fall 359.0
   - W-09: spring 264.2, fall 370.8
   - W-10: spring 258.6, fall 382.1
   - W-11: spring 250.7, fall 365.1
   - W-12: spring 266.8, fall 375.3
   - W-13: spring 244.0, fall 353.8
   - W-14: spring 261.0, fall 367.5
   - W-15: spring 267.7, fall 373.4

### transfer_purchase_memo.docx

1. The purchase: 250 acre-feet of transfer water, recorded before December 15, about USD 296,250 at the agency's posted price.
2. The ranch's water year 2026 total against the water it had available: 15,583 acre-feet against 15,358.9, 224 over.
3. Each well's April to September 2026 energy charge, nearest dollar:
   - W-01: USD 62,185
   - W-02: USD 59,205
   - W-03: USD 62,095
   - W-04: USD 55,271
   - W-05: USD 65,316
   - W-06: USD 49,307
   - W-07: USD 140,560
   - W-08: USD 158,019
   - W-09: USD 153,428
   - W-10: USD 175,837
   - W-11: USD 140,790
   - W-12: USD 154,906
   - W-13: USD 159,362
   - W-14: USD 159,270
   - W-15: USD 172,137
