## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Designate four of Tollard's eight hubs for 2027 under Schedule 4: Carrow Mills, Dunfield, Greyhaven and Kesterbrook.**
Their panel households' connections delivered under 80 per cent of plan for 29, 31, 25 and 22 per cent of the weekday evening peak; Larchmoor, the highest of the rest, for 18 per cent. Not Carrow Mills and Dunfield alone, which the share of the completed tests gives (Carrow Mills 22 per cent; Dunfield 25 per cent; Greyhaven 19 per cent; Kesterbrook 17 per cent): a unit runs no test in an hour while the household's own line stays busy, and the households are busiest on the nights their nodes carry the most traffic, so the tests that ran sat at lighter loads than the peak as a whole (Greyhaven 65.3 against 68.0 per cent average node load; Kesterbrook 64.3 against 67.1 per cent average node load). Weighting each evening hour or each night equally does not remove it; counting every test not run as a failure designates all eight hubs.

## 2. Critical Components

1. Share of the weekday evening peak below 80 per cent of plan: Bellwick **17** per cent; Carrow Mills **29** per cent; Dunfield **31** per cent; Eastholm **10** per cent; Greyhaven **25** per cent; Kesterbrook **22** per cent; Larchmoor **18** per cent; Sedgecombe **14** per cent.
2. Average node utilisation in the hub's tested weekday peak intervals against every weekday peak interval of its panel households: Greyhaven **65.3** against **68.0** per cent; Kesterbrook **64.3** against **67.1** per cent; lighter in every hub.
3. Each household's tests were read against its node's utilisation in the tested interval and carried to every weekday peak interval of the window from the node's filing (per plan, the load above which the connection fell under 80 per cent of plan), each of the **1,137** panel households counted equally.

## 3. Step-by-Step Solution

1. Took Schedule 4, 3.1 and 3.2, with its definitions (1.2 to 1.8): every weekday interval from 7 to 11 pm local time, 14 September to 13 November 2026, of every panel household served from the hub, each household counted equally; designated above 20 per cent.
2. Kept the 1,137 panel households (enrolled before 14 September and still in the panel at 13 November), gave each test to its household through panel_units.csv, and dropped tests received twice.
3. Put each test in its UTC interval from its own offset, and read its node on the day (tollard_address_node_table.csv), the node's utilisation in that interval and the plan in force (tollard_subscription_history.csv, tollard_plan_catalogue.csv).
4. Compared the node loads of the tested intervals with every weekday peak interval: the tests ran at lighter loads in every hub.
5. For each household and plan, found the node load above which its tests fell under 80 per cent of plan and counted its node's weekday peak intervals above it; averaged the households by hub.
6. For credits, merged each node's overlapping unplanned tickets into one outage, kept outages of four hours or more that began in the window (local time), and charged a day for each started 24 hours to the node's subscribers at the end of the month before.
7. For capacity added, summed each hub's register capacity in service on 13 November less 14 September, leaving out the second records of the split nodes (the same children a day later, with no subscribers).

## 4. Deliverable Answers

### hub_peak_congestion_2026.xlsx

1. Share of the weekday evening peak below 80 per cent of plan (whole per cent) and designation:
   - Bellwick: 17 per cent, not designated
   - Carrow Mills: 29 per cent, designated
   - Dunfield: 31 per cent, designated
   - Eastholm: 10 per cent, not designated
   - Greyhaven: 25 per cent, designated
   - Kesterbrook: 22 per cent, designated
   - Larchmoor: 18 per cent, not designated
   - Sedgecombe: 14 per cent, not designated
2. Outage credits owed for unplanned outages that began in the window (subscriber-days):
   - Bellwick: 2,549
   - Carrow Mills: 2,531
   - Dunfield: 2,401
   - Eastholm: 3,149
   - Greyhaven: 1,095
   - Kesterbrook: 2,559
   - Larchmoor: 2,808
   - Sedgecombe: 3,140
3. Downstream capacity added during the window (Mbit/s):
   - Bellwick: 13,200
   - Carrow Mills: 14,960
   - Dunfield: 16,840
   - Eastholm: 11,910
   - Greyhaven: 11,030
   - Kesterbrook: 5,980
   - Larchmoor: 13,670
   - Sedgecombe: 17,840

### hub_peak_congestion_2026.png

1. One bar chart of the eight hubs' shares of the peak below 80 per cent of plan against the 20 per cent line, the four designated hubs (Carrow Mills, Dunfield, Greyhaven and Kesterbrook) highlighted.
