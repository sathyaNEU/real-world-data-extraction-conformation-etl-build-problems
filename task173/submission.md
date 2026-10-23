## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Enter 3,000 water service leak repairs as the Item 101 estimated quantity for 2027.** The AMI contract exchanges 108,398 meters between February and July 2027, and every 100 exchanges add about 1.0 service leak repairs in the weeks after the new meters are set, on top of about 1,900 repairs the services need without the visits. Not the record's 1,936 repairs a year, which carry only the few exchanges the Meter Shop made each year.

## 2. Critical Components

1. 2027 service leak repairs without exchange visits: **1,900** (nearest 100).
2. Added service leak repairs per 100 meter exchanges: **1.0**.
3. AMI meter exchanges scheduled for 2027: **108,398**.

## 3. Step-by-Step Solution

1. Counted one repair per leak, the CLOSED REP orders of WORK_TYPE SERVICE LEAK in eam_workorders_2021_2026.xlsx and the CLOSED SVC LEAK orders in lwms_workorders_2012_2021.csv (MIGRATED orders are counted in EAM): 1,936 a year from October 2024 to September 2026.
2. Tied each repair to its GIS service (EAM ASSET_ID, legacy ADDRESS) and each meter exchange in cis_meter_events_2012_2026.csv (a REMOVE and the next SET at the premise) to the premise's service in cis_premises_20260930.csv, by SERVICE_ID or address.
3. Counted repairs on a service in the 120 days after its new meter was set, for the 65,620 exchanges whose window closes by 30 September 2026, less the service base rate outside those windows: 1.01 added repairs per 100 exchanges.
4. Took the record's own exchange-visit repairs out of the record rate (4,848 exchanges a year in the window): 1,887.2 repairs in 2027 without exchange visits.
5. Applied the added rate to the 108,398 METER EXCHANGE rows of ami_install_schedule_2027.csv, with the record's delay from exchange to repair, and added the two: 2,977.6 repairs, 3,000 at the nearest 250.
6. Item 201: one break per main ASSET_ID and REPORTED time across its REP and REPC orders in eam_workorders_2021_2026.xlsx, counted at its latest COMPLETED date and by the main's SVC_CENTER in gis_water_mains_20260930.csv: 712 breaks in fiscal 2026.
7. Items 301 to 305: for each estimate in mabry_teague_pay_estimates_fy2025_fy2026.xlsx the revision whose AMOUNT total equals the GROSS_AMOUNT paid in ap_payments_contract_23-0388.csv, QTY summed by surface type and quarter of WORK_COMPLETED.

## 4. Deliverable Answers

### service_leak_forecast_2027.xlsx

1. 2027 water service leak repairs: 3,000 (nearest 250).
2. Fiscal 2026 main break repairs by service centre and month:
   - North: Oct 40, Nov 19, Dec 18, Jan 25, Feb 26, Mar 14, Apr 18, May 12, Jun 10, Jul 26, Aug 32, Sep 48
   - South: Oct 14, Nov 19, Dec 15, Jan 18, Feb 23, Mar 18, Apr 10, May 14, Jun 20, Jul 16, Aug 35, Sep 28
   - West: Oct 15, Nov 13, Dec 8, Jan 8, Feb 19, Mar 17, Apr 9, May 17, Jun 10, Jul 13, Aug 32, Sep 33
3. Fiscal 2026 restoration by surface type and quarter (Q1 October to December, Q2 January to March, Q3 April to June, Q4 July to September), square yards to the nearest 10:
   - Asphalt pavement: Q1 2,910, Q2 2,180, Q3 2,060, Q4 3,740
   - Concrete pavement: Q1 670, Q2 670, Q3 400, Q4 670
   - Sidewalk and driveway: Q1 1,550, Q2 1,530, Q3 1,210, Q4 1,900
   - Sod: Q1 4,660, Q2 3,940, Q3 3,670, Q4 6,000

### service_leaks_by_month.png

1. Monthly service leak repairs January 2021 to September 2026 as a line, and the 2027 forecast by month as stacked bars, without exchange visits and added by the AMI exchanges.
