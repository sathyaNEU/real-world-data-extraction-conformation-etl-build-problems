## Tags

**Domain:** Physical & Environmental Sciences (environmental monitoring and exceedance).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Ituna regular (GB-131) and Canora regular (GB-134) go on the January 2027 tightness-testing work order, having lost 1.2 and 0.9 litres an hour to the ground over October to December 2026.** Canora's 1.0 L/h shortfall moves with its sales, but its meters, calibrated on 2 July 2026, give away only 0.1 L/h of it at the drift the network's own tank books show. Not Ituna alone, which statistical inventory reconciliation files by booking every sales-linked loss to the meters. Not Kamsack regular or Foam Lake diesel, whose 1.7 and 1.5 L/h shortfalls are what their meters' use since calibration gives away.

## 2. Critical Components

1. Canora regular's October to December book shortfall is **1.0 L/h**, of which its meters give away **0.1 L/h**
2. Kamsack regular's **1.7 L/h** and Foam Lake diesel's **1.5 L/h** shortfalls carry meter over-delivery of **1.7 L/h** and **1.6 L/h**
3. The meters drift **6.1 mL per 20 L draft for every 100,000 litres** passed since calibration, one rate across the network
4. Ituna regular loses **1.2 L/h** to the ground and Canora regular **0.9 L/h**

## 3. Step-by-Step Solution

1. Built each gas bar tank system's daily book per PD-07 s.3 from the 05:00 closes in atg_shift_close_inventory_2024_2026.csv, the bills' net litres on the drop's business day in bills_of_lading_2024_2026.csv and the latest export of each hose-day in pos_fuel_sales_by_hose_2024_2026.csv: October to December shortfalls of 1.3 L/h at Ituna regular, 1.0 at Canora regular, 1.7 at Kamsack regular and 1.5 at Foam Lake diesel.
2. Dated each hose's last calibration or replacement from service_work_orders_2024_2026.xlsx, through the dispenser serials in forecourt_controller_config_2027-01-05.json and the dispenser numbers in tpc_site_tank_register.xlsx, and summed each day's hose litres times the litres that hose had passed since: each tank-quarter's exposure.
3. Fitted one drift per litre over the 324 tank-quarters from 2024 Q1 to 2026 Q3 with every hose's reset on record, quarter shortfall on exposure with no constant: 6.1 mL per 20 L for every 100,000 litres.
4. Took each system's October to December exposure times that drift out of its shortfall and divided by the quarter's elapsed hours (2,208 in Saskatchewan, 2,209 in Manitoba): Ituna regular 1.2 L/h and Canora regular 0.9 L/h, every other system near zero.
5. Applied PD-07 s.5: Ituna regular and Canora regular are over 0.75 L/h and go on the January work order.
6. For each cardlock bill in bills_of_lading_2024_2026.csv, took the received litres as the matching report's increase in cardlock_gauge_delivery_reports_q4_2026.csv (one row per delivery number across the pulls) plus the litres drawn from that tank inside the report window in cardlock_transactions_q4_2026.csv (UTC less six hours); the 35 drops with no report were rebuilt from cardlock_gauge_hourly_inventory_q4_2026.csv as the rise between the readings either side plus the fills between them, dated by the rise.
7. Summed bill net less received by carrier and by cardlock in the month each drop arrived, to the nearest 10 litres (block 4).

## 4. Deliverable Answers

### tank_test_workorder_jan2027.pdf

1. Systems going for testing:
   - Ituna regular, GB-131 tank 1: 1.2 litres an hour
   - Canora regular, GB-134 tank 1: 0.9 litres an hour
2. Bar chart on page 2 of every gas bar tank system's loss against the dashed 0.75 line, the two systems going for testing in blue and labelled.

### cardlock_drops_q4_2026.xlsx

1. Litres short of the bills of lading, net of drops that came in over, by carrier:
   - Touchwood Tank Lines: October 20, November 20, December -70
   - Whitesand Tankline: October 1,810, November 3,010, December 2,040
2. Litres short of the bills of lading, net of drops that came in over, by cardlock:
   - CL-401 Wynyard: October 270, November 350, December 360
   - CL-404 Canora: October 790, November 780, December 730
   - CL-407 Kamsack: October 400, November 1,580, December 240
   - CL-412 Russell: October 370, November 330, December 650
