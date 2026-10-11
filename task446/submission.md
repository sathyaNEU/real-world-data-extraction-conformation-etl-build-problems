# task446 submission

## Tags

**Domain:** Banking, Credit & Financial Risk (early-warning and watch-list monitoring of corporate obligor groups).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Put a 2027 caseload of 134 groups to the committee: 134 of the 913 obligor groups in the monitored book at 30 September 2026 are expected to reach the watch list by 30 September 2027.**

The 134 is the 913 groups times 14.7%, the share reaching the list that this year's 18.1% flagged share implies once the early-warning screen's capture and false-alarm rates are taken from the 2022 to 2025 cohorts. Not the hit and miss rates those cohorts report, carried onto this year's flags: the hit rate rises and falls with the share of each year's book that reaches the list, and this year's flagged share is above every closed cohort's. Not the latest or the most stressed cohort on its own: the standard measures the screen on the four closed cohorts taken together.

## 2. Critical Components

1. The monitored book at 30 September 2026 is **913** groups, **165** of them flagged
2. Over the 2022 to 2025 cohorts taken together the capture rate is **78.6%** and the false-alarm rate **7.65%**
3. The flagged share of **18.1%** implies **14.7%** of the book reaches the watch list within the year
4. A flagged group reaches it with probability **63.9%**, a group not flagged with **3.8%**

## 3. Step-by-Step Solution

1. Built the monitored book at each 30 September from credit_group_register_20260930.xlsx and watch_list_history_2020-01_to_2026-09.csv (CRM-07 4.1): 913 groups at 30 September 2026.
2. Carried each September publication in ews_entity_signals_2022-09_to_2026-09.csv to groups through the obligor master's LEI and Companies House keys and the GLEIF relationship records in force at the date (CRM-07 2.2, 2.3, 3.2): 165 of the 913 are flagged.
3. Matched the 2022 to 2025 cohorts to watch-list placements in the following twelve months (CRM-07 4.2) and measured them taken together (4.3): capture rate 78.6%, false-alarm rate 7.65%.
4. Re-ran each closed cohort from the other three: capture and false-alarm rates reproduce its arrivals within 3%, while hit and miss rates miss two of the four by more than a third, because the hit rate moves with the share of each year's book that reaches the list.
5. Solved this year's 18.1% flagged share for the share of the book that will reach the list through those two rates: 14.7%, so a flagged group reaches it with probability 63.9% and a group not flagged with 3.8% (CRM-07 5.2).
6. Summed the probabilities over the 913 groups: 134.1 expected arrivals, 134 to the nearest whole group (CRM-07 5.3).
7. Built each group's committed exposure at 30 September 2026 under CRM-07 6.1 from facility_extract_hbplc_20260930_rerun.csv (the record for 30/09 per reference_data_extract_log_20261008.txt) and facility_extract_hbdac_20260930.csv, counting active facilities that mature after 30 September and dividing non-sterling limits by the per-pound rates in treasury_closing_rates_20260930.csv, then summed probabilities and probability-weighted exposure within each 6.2 band for the workbook.
8. Recommendation: put a 2027 caseload of 134 groups to the committee.

## 4. Deliverable Answers

### watchlist_inflow_2027.xlsx
1. Heading figure: 134 obligor groups expected to reach the watch list by 30 September 2027
2. One row per caseload band, smallest first (expected arrivals from groups flagged in September, expected arrivals from groups not flagged, expected committed exposure arriving):
   - Under £5m: 23.0 flagged, 6.4 not flagged, £73.6m
   - £5m and under £15m: 34.5 flagged, 9.2 not flagged, £450.5m
   - £15m and under £40m: 28.1 flagged, 7.6 not flagged, £969.8m
   - £40m and under £100m: 14.7 flagged, 3.8 not flagged, £1,295.5m
   - £100m and over: 5.1 flagged, 1.7 not flagged, £1,319.0m
3. Total row: 105.4 flagged, 28.7 not flagged, £4,108.4m

### watchlist_inflow_2027.svg
1. One stacked bar per band, smallest first, with the flagged and not-flagged segments labelled with the band figures above
2. The caseload, 134 groups, written on the chart
3. Title: "134 of the 913 groups we monitor are expected on the watch list by 30 September 2027"
