# task446 submission

## Tags

**Domain:** Banking, Credit & Financial Risk (early-warning and watch-list monitoring of corporate obligor groups).  
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Put a 2027 caseload of 78 groups to the committee: 78 of the 913 obligor groups in the monitored book at 30 September 2026 are expected to reach the watch list by 30 September 2027.**

The 78 prices each September flag by where in the group it was raised. Over the 2022 to 2025 cohorts a group whose flag sat on a customer we lend to reached the list within the year 50.0% of the time, and one flagged only through a parent or sister company we do not lend to 6.25%, and this September 127 of the 165 flags sit on customers, a far larger share than in any closed cohort. Predicting each closed cohort from the other three, that basis misses none by more than 3.9%. Not one rate for every flagged group, which gives 64 and misses a closed cohort by 14.4% because it carries the cohorts' mix of the two kinds of flag onto a book that holds far more of the first; nor the colour or covenant-trigger splits, the latest or most stressed cohort, or the screen's capture and false-alarm rates with this year's arrival share backed out of the flagged share, which gives 136.

## 2. Critical Components

1. The monitored book at 30 September 2026 is **913** groups; **165** of them are flagged, **127** of those flags raised on a customer the bank lends to
2. Over the 2022 to 2025 cohorts taken together a flag raised on a customer reached the watch list **50.0%** of the time, a flag raised only on a member the bank does not lend to **6.25%**, and a group not flagged **1.62%**
3. Predicting each closed cohort from the other three, the split by where the flag was raised misses none by more than **3.9%**; one rate for every flagged group misses one by **14.4%**

## 3. Step-by-Step Solution

1. Built the monitored book at each 30 September from credit_group_register_20260930.xlsx and watch_list_history_2020-01_to_2026-09.csv (CRM-07 4.1): 913 groups at 30 September 2026.
2. Carried each September publication in ews_entity_signals_2022-09_to_2026-09.csv to groups through the group register's ultimate parent LEI, the obligor master's LEI and Companies House keys and the GLEIF relationship records in force at the date (CRM-07 2.2, 3.2), and marked each flag by whether an AMBER or RED entity is a customer on credit_obligor_master_20260930.csv opened by the date: 165 flagged, 127 of them on a customer.
3. Matched the 2022 to 2025 cohorts to watch-list placements in the following twelve months (CRM-07 4.2): of 240 flags raised on customers 120 reached the list, of 176 raised only on other members 11, of 3,092 groups not flagged 50.
4. Back-tested the bases on the closed cohorts, each predicted from the other three: the split by where the flag was raised misses by at most 3.9%, one rate for every flagged group by 14.4%.
5. Gave each group in the 30 September 2026 book the share for its kind over the four cohorts taken together (4.3) and summed: 78.0 expected arrivals, 78 to the nearest whole group (CRM-07 5.3).
6. Built each group's committed exposure under CRM-07 1.3 and 6.1 from facility_obligor_extract_20260930.csv, each facility (booking entity and number) once in every group with a member on it, counting the facility of a company booked to one group and consolidated through GLEIF into another's ultimate parent in both groups and placing customers not yet grouped through GLEIF (2.2), at the limit in facility_limit_history_20261008.csv as at the end of 30 September UK time, in sterling at the units_per_gbp rates, and banded it under 6.2.
7. Summed each band's groups, flags, probabilities and probability-weighted committed exposure for the workbook and the chart.
8. Recommendation: put a 2027 caseload of 78 groups to the committee.

## 4. Deliverable Answers

### watchlist_inflow_2027.xlsx
1. Heading figure: 78 obligor groups expected to reach the watch list by 30 September 2027
2. One row per caseload band, smallest first (groups the band holds, their committed exposure, groups flagged in September, expected arrivals, expected committed exposure arriving):
   - Under £5m: 201 groups, £499.9m committed, 34 flagged, 16.2 expected arrivals, £38.5m arriving
   - £5m and under £15m: 304 groups, £3,112.0m committed, 54 flagged, 25.8 expected arrivals, £257.1m arriving
   - £15m and under £40m: 248 groups, £6,936.6m committed, 46 flagged, 21.9 expected arrivals, £596.8m arriving
   - £40m and under £100m: 120 groups, £8,402.7m committed, 20 flagged, 9.0 expected arrivals, £576.3m arriving
   - £100m and over: 40 groups, £6,712.2m committed, 11 flagged, 5.1 expected arrivals, £826.8m arriving
3. Total row: 913 groups, £25,663.4m committed, 165 flagged, 78.0 expected arrivals, £2,295.5m arriving

### watchlist_inflow_2027.svg
1. One bar per band, smallest first, labelled with the band's expected arrivals above
2. The caseload, 78 groups, written on the chart
3. Title: "78 of the 913 groups we monitor are expected on the watch list by 30 September 2027"
