# task446 submission

## Tags

**Domain:** Banking, Credit & Financial Risk (early-warning and watch-list monitoring of corporate obligor groups).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Put a 2027 caseload of 133 groups to the committee: 133 of the 913 obligor groups in the monitored book at 30 September 2026 are expected to reach the watch list by 30 September 2027.**

The 133 comes from the basis CRM-07 5.2's test selects: the early-warning screen's capture and false-alarm rates over the 2022 to 2025 cohorts, with this year's share of the book reaching the list backed out of this year's 18.1% flagged share. Not the hit and miss rates those cohorts report, carried onto this year's flags: the hit rate moves with each year's share of the book reaching the list, and that basis misses a closed cohort by 40.6%. Not the latest or the most stressed cohort on its own, nor rates trended on the flagged share: 5.2 sets the probabilities from the last four closed cohorts taken together, on the basis with the smallest largest miss.

## 2. Critical Components

1. The monitored book at 30 September 2026 is **913** groups, **165** of them flagged
2. On 5.2's test the capture and false-alarm basis misses no closed cohort by more than **1.6%**; the hit and miss rates miss one by **40.6%**
3. Over the 2022 to 2025 cohorts taken together the capture rate is **78.1%** and the false-alarm rate **7.83%**
4. The flagged share of **18.1%** implies **14.6%** of the book reaches the watch list within the year
5. A flagged group reaches it with probability **63.0%**, a group not flagged with **3.9%**

## 3. Step-by-Step Solution

1. Built the monitored book at each 30 September from credit_group_register_20260930.xlsx and watch_list_history_2020-01_to_2026-09.csv (CRM-07 4.1): 913 groups at 30 September 2026.
2. Carried each September publication in ews_entity_signals_2022-09_to_2026-09.csv to groups through the group register's ultimate parent LEI, the obligor master's LEI and Companies House keys and the GLEIF relationship records in force at the date (CRM-07 2.2, 3.2): 165 of the 913 are flagged.
3. Matched the 2022 to 2025 cohorts to watch-list placements in the following twelve months (CRM-07 4.2) and measured them taken together (4.3): capture rate 78.1%, false-alarm rate 7.83%.
4. Ran 5.2's test, each closed cohort predicted from the other three taken together: the capture and false-alarm basis has the smallest largest miss, 1.6%, against 40.6% for the hit and miss rates.
5. Solved this year's 18.1% flagged share for the share of the book that will reach the list through those two rates: 14.6%, so a flagged group reaches it with probability 63.0% and a group not flagged with 3.9%.
6. Summed the probabilities over the 913 groups: 133.0 expected arrivals, 133 to the nearest whole group (CRM-07 5.3).
7. Built each group's committed exposure under CRM-07 1.3 and 6.1 from facility_obligor_extract_20260930.csv, each facility (booking entity and number) once in every group with an obligor on it and customers not yet grouped placed through GLEIF (2.2), at the limit in facility_limit_history_20261008.csv as at the end of 30 September UK time, in sterling at the units_per_gbp rates, then banded it under 6.2 for the workbook.
8. Recommendation: put a 2027 caseload of 133 groups to the committee.

## 4. Deliverable Answers

### watchlist_inflow_2027.xlsx
1. Heading figure: 133 obligor groups expected to reach the watch list by 30 September 2027
2. One row per caseload band, smallest first (groups the band holds, their committed exposure, expected arrivals from groups flagged in September, expected arrivals from groups not flagged, expected committed exposure arriving):
   - Under £5m: 201 groups, £475.8m committed, 21.4 flagged, 6.5 not flagged, £69.6m arriving
   - £5m and under £15m: 306 groups, £3,016.2m committed, 34.0 flagged, 9.8 not flagged, £411.5m arriving
   - £15m and under £40m: 250 groups, £7,153.8m committed, 29.6 flagged, 7.9 not flagged, £1,108.6m arriving
   - £40m and under £100m: 120 groups, £8,213.8m committed, 12.6 flagged, 3.9 not flagged, £1,121.5m arriving
   - £100m and over: 36 groups, £6,640.9m committed, 6.3 flagged, 1.0 not flagged, £1,283.4m arriving
3. Total row: 913 groups, £25,500.5m committed, 103.9 flagged, 29.1 not flagged, £3,994.6m arriving

### watchlist_inflow_2027.svg
1. One stacked bar per band, smallest first, with the flagged and not-flagged segments labelled with the band figures above
2. The caseload, 133 groups, written on the chart
3. Title: "133 of the 913 groups we monitor are expected on the watch list by 30 September 2027"
