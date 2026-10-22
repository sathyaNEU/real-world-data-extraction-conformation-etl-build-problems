# task446 submission

## Tags

**Domain:** Banking, Credit & Financial Risk (early-warning and watch-list monitoring of corporate obligor groups).  
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Set the 2027 watch-list caseload at 78 groups: 78 of the 913 obligor groups in the monitored book at 30 September 2026 are expected to reach the watch list by 30 September 2027.**

The 78 prices each September flag by the member that raised it: over the 2022 to 2025 cohorts a group flagged on a customer we lend to reached the list within the year 50.0% of the time and one flagged only on a parent or sister company we do not lend to 6.25%, and 127 of the 165 groups flagged this September were flagged on a customer. Not one rate for every flagged group, which carries the cohorts' mix of the two kinds of flag onto a book holding far more of the first and misses one closed cohort by 14.4% where the split's largest miss is 3.9%; not the colour or covenant-trigger splits or the latest or most stressed cohort, which do the same; not the screen's capture and false-alarm rates with this year's arrival share backed out of the flagged share, which read a rise in customer flags as a rise in the base rate.

## 2. Critical Components

1. The monitored book at 30 September 2026 is **913** groups; **165** of them are flagged, **127** of those flagged on a customer the bank lends to
2. Over the 2022 to 2025 cohorts taken together a group flagged on a customer reached the watch list within the year **50.0%** of the time, a group flagged only on members the bank does not lend to **6.25%**, and a group not flagged **1.62%**

## 3. Step-by-Step Solution

1. Built the monitored book at each 30 September from credit_group_register_20260930.xlsx and watch_list_history_2020-01_to_2026-09.csv (CRM-07 4.1): 913 groups at 30 September 2026.
2. Carried each September publication in ews_entity_signals_2022-09_to_2026-09.csv to groups through the group register's ultimate parent LEI, the obligor master's LEI and Companies House keys and the GLEIF relationship records in force at the date (CRM-07 2.2, 3.2), and marked each flagged group by whether any of its AMBER or RED members is a customer on credit_obligor_master_20260930.csv opened by the date: 165 flagged, 127 of them on a customer.
3. Matched the 2022 to 2025 cohorts to watch-list placements in the following twelve months (CRM-07 4.2): of 240 groups flagged on a customer 120 reached the list, of 176 flagged only on other members 11, of 3,092 groups not flagged 50.
4. Back-tested the bases on the closed cohorts, each forecast from the other three taken together: the largest miss, as a share of the cohort's actual arrivals, is 3.9% for the split by where the flag was raised and 14.4% for one rate for every flagged group.
5. Gave each group in the 30 September 2026 book the cohorts' share for its kind of flag, or for groups not flagged, over the four cohorts taken together (CRM-07 4.3) and summed: 78.0 expected arrivals, 78 to the nearest whole group (CRM-07 5.3).
6. Built each group's committed exposure under CRM-07 1.3 and 6.1 from facility_obligor_extract_20260930.csv: each facility (booking entity and number) once in every group with a member on it, counting the facility of a company booked to one group and consolidated through GLEIF into another's ultimate parent in both groups and placing customers not yet grouped through GLEIF (2.2), at the limit in facility_limit_history_20261008.csv as at the end of 30 September UK time, in sterling at the units_per_gbp rates.
7. Left out the 22 facilities the ledger booked twice, each undrawn and repeating stamp for stamp, limit for limit and user for user the limit history of the facility numbered just before it for the same customer and terms, kept the same-day tranches whose histories differ, banded the groups under 6.2 and summed each band's groups, flagged groups, probabilities and probability-weighted committed exposure for the workbook and the chart.
8. Recommendation: set the 2027 watch-list caseload at 78 groups.

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
