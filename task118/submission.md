## Tags

**Domain:** Energy Systems & Utilities (generation capacity planning).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**The USD 3.2 million expansion line should go to the Home Battery Network, which adds 6 MW to the 2027 accredited capacity against 4 MW for Peak Time Rewards, the runner-up.** The deciding figure is each programme's 18:00 reduction on the fourth consecutive event day, where the design year's peak hour falls. Not Cool Credit, which leads on the record's average event at 11 MW but adds 3 MW in that hour; not Business Demand Partners, at 2 MW.

## 2. Critical Components

1. The system peak hour of the design year, the hour beginning 18:00 MST on 23 July 2027, is the **fourth** consecutive weekday OP-7 calls.
2. The budget buys **2,133** batteries, **50,000** rebate customers, **12,307** thermostat premises or **133** commercial sites.
3. Accredited capacity added: Home Battery Network **6 MW**, Peak Time Rewards **4 MW**, Cool Credit **3 MW**, Business Demand Partners **2 MW**.

## 3. Step-by-Step Solution

1. Took the hour of highest forecast load in appendix_b_design_year_2027.csv (the hour beginning 18:00 on 23 July 2027) and applied OP-7's trigger (a weekday whose forecast high reaches 110F) to the design year's daily highs: 20 to 23 July are called, so the peak hour is the fourth event day in a row.
2. Rebuilt each event date's run day from dr_event_log_2024-2026.csv as consecutive calendar days with an event: the record's fourth days are 12 July 2024, 18 July 2025 and 24 July 2026.
3. Read each programme's reduction per enrolled unit in the hour beginning 18:00 MST: holdout less treatment mean kWh in ridgeway_cool_credit_panel_2024-2026.csv (UTC less seven hours), holdout less alerted mean kW in ridgeway_peak_time_rewards_2024-2026.csv, the mean verified site reduction in ridgeway_business_demand_partners_2024-2026.csv, and discharge over enrolled batteries in brightwell_fleet_event_summary_2024-2026.csv under the 3.0 kW setting of schedule 2.
4. Averaged each over its fourth days (0.248 kW a Cool Credit premise, 0.0753 kW a rebate customer, 14.6 kW a site, 2.90 kW a battery) and multiplied by the whole units dr_expansion_costs_2027.xlsx's all-in costs buy: the Home Battery Network 6 MW, Peak Time Rewards 4, Cool Credit 3, Business Demand Partners 2.
5. Counted, for each 2026 event day, the premises in cool_credit_enrolments_cis_2026-10-16.csv enrolled that day with a thermostat ready at 23:00 UTC under OP-7 section 6: the enrolled serial or a device in halvern_device_registry_2026-10-16.json at the same address once both are normalised, registered and not retired by then, its last row in halvern_status_changes_2026.csv ONLINE, or IDLE reported after the firmware 6.0 push of 6 July 2026.
6. Dropped exact repeats from brightwell_dispatch_records_2026.csv, added each battery's record hours for an event (the MST date of the dispatch start), counted a premise in battery_interconnection_register_2026-10-16.csv once per event when any of its batteries reached three hours, and paid USD 15 an event in event order up to USD 255.
7. Kept the latest submitted row per meter and month in arroyo_nominations_2026.csv for the utility's meters, those in cbmu_commercial_meters_2026-10-16.csv, and summed nominated kW by month.
8. Recommended the Home Battery Network, 2 MW ahead of Peak Time Rewards.

## 4. Deliverable Answers

### dr_capacity_note_2027.docx

1. Recommendation: expand the Home Battery Network with the USD 3.2 million.
2. Accredited capacity each programme's expansion adds in the 2027 system peak hour, whole megawatts:
   - Home Battery Network: 6 MW
   - Peak Time Rewards: 4 MW
   - Cool Credit: 3 MW
   - Business Demand Partners: 2 MW
3. Runner-up: Peak Time Rewards.
4. A bar chart of each programme's megawatts sits under the table on page 1 of the note.

### dr_programme_audit_2026.csv

5. Cool Credit enrolled premises with a thermostat online at 16:00, each 2026 event day, whole premises:
   - 17 June 2026: 8,696
   - 23 June 2026: 8,743
   - 30 June 2026: 9,054
   - 7 July 2026: 9,095
   - 8 July 2026: 9,131
   - 13 July 2026: 9,247
   - 15 July 2026: 9,292
   - 21 July 2026: 9,278
   - 22 July 2026: 9,286
   - 23 July 2026: 9,305
   - 24 July 2026: 9,315
   - 31 July 2026: 9,319
   - 4 August 2026: 9,366
   - 5 August 2026: 9,400
   - 6 August 2026: 9,375
   - 17 August 2026: 9,450
   - 26 August 2026: 9,475
   - 31 August 2026: 9,514
   - 9 September 2026: 9,545
6. Home Battery Network incentive owed by 2026 event month, nearest dollar:
   - June: USD 132,735
   - July: USD 399,825
   - August: USD 248,790
   - September: USD 9,480
7. Home Battery Network premises that reached the season cap: 2,939
8. Business Demand Partners nominated capacity by month, whole kilowatts:
   - June 2026: 14,903 kW
   - July 2026: 16,438 kW
   - August 2026: 17,324 kW
   - September 2026: 17,830 kW
