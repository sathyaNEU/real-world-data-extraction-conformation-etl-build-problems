# task129 submission

## Tags

**Domain:** Energy Systems & Utilities (grid reliability and outage analysis: what drove a rural electric cooperative's rise in tree-caused outages on overhead primary).
**Analytical objective:** Root-Cause Analysis (the driver of the 2025 rise in tree-caused outages, and the right-of-way programme the cooperative's policy assigns to it).

## 1. Final Recommendation

**The 2027 right-of-way budget increase should fund hazard-tree removal beyond the right-of-way: the rise in tree-caused outages, from 11.2 per 100 miles of overhead primary on average over 2021 to 2023 to 21.9 in 2025, is mostly ash beyond North's right-of-way falling onto the line.**

North's 2025 rate rose by 18.8 outages per 100 miles on units trimmed within the previous two years, where regrowth seldom reaches the line, about as much as on units late in their cycle, and the rise climbs with the share of ash among the trees within falling distance; that shift is most of the cooperative's rise. Not a re-bid of the trimming contract: North's units fail at North's 2025 rate for their time since trim whoever trimmed them last (Garrity's at 0.98 times, Hollenbeck's at 1.01). Not catch-up trimming: East's units left past the four-year cycle by its April 2025 handover carry a small part of the rise, and North's shift does not fall with time since trim. Not nothing new: South's windier 2025 carries a small part.

## 2. Critical Components

1. The cooperative's tree-caused outages per 100 miles of overhead primary: **21.9** in 2025, **11.2** on average over 2021 to 2023
2. North's tree-caused outages per 100 miles of overhead primary: **30.2** in 2025, **11.1** on average over 2021 to 2023
3. 2025's major event days, taken out of the rates: **18 June** and **9 December**

## 3. Step-by-Step Solution

1. Took each outage in oms_outage_export_2016-2025.csv once: a ticket's restoration-step rows under its outage_id, and a second ticket of a device already open folded into that device's outage, a device being in one outage at a time (ENG-REL-02 2.1), with customer-minutes summed over the restoration steps (3.1).
2. Found each year's major event days by ENG-REL-02 3.2 (IEEE 1366, 2.5 beta, the five prior years' daily SAIDI over the year-end members in member_counts_2015-2025.csv): 2025's are 18 June and 9 December.
3. Counted the sustained TREE outages on overhead primary outside major event days and divided by the miles in service averaged over each year's days from trim_unit_register.csv (2.2): the cooperative's rate is 21.9 in 2025 against 11.2 on average over 2021 to 2023, North's 30.2 against 11.1.
4. Ran each trim unit's regrowth clock from its accepted trims in row_trim_completions_2012-2025.csv, a rebuilt unit's from its in-service date (OPS-ROW-01 3.1, 3.2): North's 2025 rate rose by 18.8 per 100 miles on units within two years of their last trim, about as much as on units late in their cycle.
5. Set each contractor's North units against North's 2025 rate at the same time since trim: the units Garrity last trimmed failed at 0.98 times their expected count and those Hollenbeck last trimmed at 1.01, so the trimming is not the cause.
6. Rated North's units by the share of ash among the trees within falling distance in row_tree_survey_2023-2024.parquet (FRAX in the 2023 survey, ASH in the 2024 re-survey): the rise climbs with the ash share, a gradient absent in 2021 to 2023.
7. Sized the drivers against the cooperative's rise: North's shift at every time since trim is most of it; East's units past the cycle after its April 2025 handover and South's windier 2025 carry the rest.
8. Hazard-tree removal answers trees falling onto the line from beyond the right-of-way (OPS-ROW-01 6.3): the 2027 budget increase funds hazard-tree removal.

## 4. Deliverable Answers

### tree_outage_root_cause_2025.docx

1. Call: fund hazard-tree removal beyond the right-of-way with the 2027 budget increase
2. The cooperative's tree-caused outages per 100 miles of overhead primary: 21.9 in 2025, 11.2 on average over 2021 to 2023

### tree_outage_workings_2025.xlsx

1. Miles of right-of-way billed for trimming done in each quarter of 2025:
   - Hollenbeck Line Clearance, Inc.: Q1 66.5, Q2 80.9, Q3 84.4, Q4 56.6
   - Garrity Vegetation Services, LLC: Q1 94.7, Q2 136.3, Q3 114.9, Q4 178.5
2. Taken out of the reliability figures by 2025's major event days (18 June and 9 December):
   - North: 160 outages, 5,956 members interrupted, 1,821,820 customer-minutes
   - East: 123 outages, 3,559 members interrupted, 1,203,168 customer-minutes
   - South: 112 outages, 3,598 members interrupted, 1,150,972 customer-minutes
3. Miles of overhead primary in service at the end of 2025:
   - North: 1,773.3
   - East: 1,237.8
   - South: 1,138.3
