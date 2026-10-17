## Tags

**Domain:** General Statistics & Data Science (data integration: a river gauge's record and a water works' reports, kept under different observation mechanisms, combined in one maximum-likelihood fit).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Reserve 0.3 MGD (three blocks) of firm capacity on the Castlewick interconnect for 2027.**
At the Varrow River's 50-year 7-day low flow of 1.55 cfs the permit allows 0.68 MGD, 0.23 MGD short of the 2027 Stage 2 demand of 0.91 MGD, and three blocks cover it. Not 0.4 MGD, from a fit to the gauge's years and the 14 report years with a measured flow alone (1.31 cfs), which drops the 40 report years without a stoppage as if they held no record; not 0.1 MGD, from the gauge alone (1.87 cfs), which leaves out the reports the guidance requires.

## 2. Critical Components

1. The 50-year 7-day low flow at the intake: **1.55 cfs**.
2. The withdrawal the permit allows at it: **0.68 MGD**; the Stage 2 shortfall: **0.23 MGD**.
3. The record fitted: **74** gauged climatic years, **14** report years with a measured flow and **40** report years without a stoppage, each entered as a 7-day low flow above **3.09** cfs.

## 3. Step-by-Step Solution

1. Took each complete climatic year's 7-day low flow (April to March, the lowest mean of seven consecutive daily means) from the approved daily values in varrow_river_at_quillfield_daily_values.txt: 74 years, 1951 to 2024 (climatic year 2025 left out: its winter is provisional).
2. Took each report year from quillfield_water_works_reports_1894_1950.pdf: 14 seasons the pumps stopped, with the lowest seven-day flow converted to cfs (gallons a day before 1921, second-feet after), 40 years with no stoppage, 3 reports not found and left out.
3. Read a year with no stoppage, under the 1893 agreement the transcription quotes, as a 7-day low flow above two million gallons a day (3.09 cfs).
4. Fitted the log-Pearson Type III of swrb_guidance_wr14_design_drought_flows.pdf with the regional skew of -0.30 by maximum likelihood to all of it: the measured years at their flows, the years without a stoppage above 3.09 cfs.
5. Read the 50-year 7-day low flow, 1.55 cfs, and the 10-, 25- and 100-year flows from the fit.
6. Applied quillfield_withdrawal_permit_wd0417.pdf (the flow above the 0.50 cfs passby) and quillfield_drought_management_plan_2024.pdf (2027 Stage 2 demand 0.91 MGD, the smallest 0.1 MGD block covering the shortfall): 0.23 MGD short, 0.3 MGD reserved.
7. For each Stage 2 period in quillfield_drought_notices_2012_2026.csv, summed each day's finished water from quillfield_wtp_scada_daily_2012_2026.csv less Elm Hollow's water from elm_hollow_master_meter_daily_reads.csv, plus the Hollow Road wells (the historian's total until the telemetry failed on 2023-06-14, the operator's readings in hollow_road_operator_log_2023_2026.csv after), and took the period's average and highest day.

## 4. Deliverable Answers

### quillfield_interconnect_reservation_2027.pdf

1. The recommended block: 0.3 MGD (three blocks of 0.1 MGD).
2. The 10-, 25-, 50- and 100-year 7-day low flows at the intake, the withdrawal the permit allows and the Stage 2 shortfall at each:
   - 10 years: 2.54 cfs, withdrawal 1.32 MGD, shortfall none
   - 25 years: 1.89 cfs, withdrawal 0.90 MGD, shortfall 0.01 MGD
   - 50 years: 1.55 cfs, withdrawal 0.68 MGD, shortfall 0.23 MGD
   - 100 years: 1.29 cfs, withdrawal 0.51 MGD, shortfall 0.40 MGD
3. The recommended block stops covering the Stage 2 shortfall beyond the 65-year 7-day low flow (1.44 cfs).
4. A chart of the annual 7-day low flows against recurrence interval: the fitted curve, the 74 gauged years, the 14 measured report years, and the 50-year flow of 1.55 cfs marked with dashed lines.
5. For each Stage 2 period the Select Board declared since 2012, the average and the highest daily water supplied to the town's own distribution system:
   - 2016-08-16 to 2016-10-02: average 0.81 MGD, highest 0.90 MGD
   - 2020-08-04 to 2020-08-26: average 0.86 MGD, highest 0.93 MGD
   - 2020-09-13 to 2020-10-04: average 0.78 MGD, highest 0.86 MGD
   - 2022-08-28 to 2022-09-14: average 0.85 MGD, highest 0.90 MGD
   - 2023-08-13 to 2023-09-29: average 0.84 MGD, highest 0.90 MGD
   - 2024-08-15 to 2024-09-22: average 0.85 MGD, highest 0.93 MGD
   - 2025-08-10 to 2025-09-17: average 0.87 MGD, highest 0.93 MGD
   - 2025-09-23 to 2025-10-11: average 0.79 MGD, highest 0.84 MGD

### varrow_river_annual_low_flows.csv

1. One row for each climatic year from 1894 to 2024 (131 rows): the year, its source, what the record shows and its 7-day low flow where the record gives one.
2. 74 gauged years and 14 measured report years carry a flow; 40 report years without a stoppage and 3 reports not found carry none.
