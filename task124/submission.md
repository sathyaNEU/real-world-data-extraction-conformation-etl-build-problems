# task124 · Summer 2027 firm-capacity block split

## Tags

**Domain:** Business & Operations Analytics (an energy retailer's summer supply planning: a capped block of summer call options split across eight weather-zone books by forecast peak-hour exposure).
**Analytical objective:** Forecasting & Predictive Modeling (each book's 1-in-10 load in the June to September 2027 system peak hour, replayed from ten closed summers at the book enrolled for 2027).

## 1. Final Recommendation

**Split the 400 MW summer block as Coast 120 MW, East 30, Far West 0, North 0, North Central 210, South Central 25, Southern 15 and West 0.**

North Central carries the largest uncovered exposure, 340 MW against Coast's 251, once its 31 new cold-storage distribution centres are carried at the 0.98 of maximum demand our cold stores draw in an uncalled peak hour as hot as a system peak. Not Coast first, as trading holds: Coast is second once the 2027 book is replayed. Not the centres at the 0.60 our fourteen cold stores drew at the closed peaks, because every one of those peaks fell in a called Business Saver window and the new centres cannot join before a metered summer. Not at the programme baseline, which averages ordinary weekdays.

## 2. Critical Components

1. Each closed summer's settled peak-hour load over that summer's enrolled maximum demand, applied to the 2026 book's maximum demand, reproduces **80 of 80** cells of Table 2 in the 2026 risk report
2. The fourteen Business Saver cold stores and ice plants drew **0.60** of maximum demand at every closed system peak and **0.98** at the same hour on uncalled weekdays as hot as a closed peak
3. North Central's 31 new refrigerated premises carry **186.0 MW** of maximum demand, priced at **0.98** (**182.3 MW**)
4. Uncovered 1-in-10 exposure before the block is **340 MW** for North Central and **251 MW** for Coast
5. The largest uncovered exposure left after the block is **132 MW** (Southern)

## 3. Step-by-Step Solution

1. Divided each book's settled load in each summer's ERCOT peak hour (`zone_settled_load_s17_s26.csv` at the hour in `ercot_summer_system_peaks.csv`) by its enrolled maximum demand on the peak date (`enrollment_extract_20270409.csv`): at the 2026 book this reproduces all 80 cells of Table 2 in `summer_2026_risk_report.pdf`.
2. Built the 2027 book from the enrolment rows open at the 9 April extract, one row per ESI ID with each AMEND row superseding the row it amends (`field_notes.md`), every premise in service from 1 June (risk policy s.3).
3. Joined `premise_register_20270409.csv`: 31 new North Central premises in refrigerated warehousing (NAICS 493120), none with an interval read, carry 186.0 MW of maximum demand.
4. Reached the fourteen Business Saver sites through `bsaver_credits_2017_2026.csv` and `billing_accounts.csv`: in `idr_hourly_reads_summers_2017_2026.parquet` they drew 0.60 of maximum demand at every closed system peak, each of which fell on a credited window.
5. On days with no credit line whose `tmax_f` in the site's zone (`zone_daily_temps_2017_2026.csv`) is at least that zone's lowest `tmax_f` on the ten closed peak days, the fourteen drew 0.98 of maximum demand at the peak hour (summed kWh over summed maximum demand); `business_saver_terms.pdf` s.1 bars the 31 (no metered summer), so the centres go in at 0.98 and every other premise at its book's replayed factor.
6. Took the 90th percentile of the ten replayed summers (inclusive) less the June to September strips in `hedge_positions_20270409.xlsx` (risk policy s.2): North Central 340 MW, Coast 251 MW.
7. Placed 80 lots of 5 MW, each to the largest remaining uncovered exposure (risk policy s.5): the next lot would go to Southern at 132 MW.
8. Recommendation: Coast 120, East 30, Far West 0, North 0, North Central 210, South Central 25, Southern 15, West 0 MW.

## 4. Deliverable Answers

### summer_block_committee.pptx

1. Split on the first slide, MW: Coast 120, East 30, Far West 0, North 0, North Central 210, South Central 25, Southern 15, West 0 (total 400)
2. Bars of uncovered exposure before the block, largest first, whole MW:
   - North Central 340
   - Coast 251
   - East 160
   - South Central 155
   - Southern 147
   - Far West 114
   - West 106
   - North 96
3. Lots shaded on each bar: North Central 210, Coast 120, East 30, South Central 25, Southern 15 MW
4. Line at 132 MW, labelled with its value (Southern, the largest uncovered exposure after the block)
5. Title: 400 MW block: North Central 210, Coast 120, East 30, South Central 25, Southern 15, none elsewhere

### summer_block_split.xlsx

1. Lots and uncovered exposure after the block, whole MW:
   - Coast: 120 lots, 131 uncovered
   - East: 30 lots, 130 uncovered
   - Far West: 0 lots, 114 uncovered
   - North: 0 lots, 96 uncovered
   - North Central: 210 lots, 130 uncovered
   - South Central: 25 lots, 130 uncovered
   - Southern: 15 lots, 132 uncovered
   - West: 0 lots, 106 uncovered
2. Option premium, USD per MW-month, June, July, August, September:
   - Coast: 2,513, 5,319, 8,318, 3,031
   - East: 2,513, 5,319, 8,318, 3,031
   - Far West: 2,971, 6,209, 9,206, 3,859
   - North: 2,971, 6,209, 9,206, 3,859
   - North Central: 2,237, 5,020, 7,765, 3,078
   - South Central: 2,597, 5,369, 9,027, 3,211
   - Southern: 2,597, 5,369, 9,027, 3,211
   - West: 2,971, 6,209, 9,206, 3,859
3. Average fixed price on existing summer hedges, USD/MWh:
   - Coast: 78.92
   - East: 75.91
   - Far West: 75.52
   - North: 75.91
   - North Central: 75.80
   - South Central: 72.74
   - Southern: 77.93
   - West: 76.88
