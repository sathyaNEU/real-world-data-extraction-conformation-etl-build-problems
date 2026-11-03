## Tags

**Domain:** Energy Systems & Utilities, grid reliability and outage analysis (district metered area burst detection on a water distribution network).  
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Send the leak detection crew to Thrushgate in week 46, whose own leakage rose by 0.6 l/s, 0.3 l/s more than Ashworth Fold.** Not Kestle Hill, whose normalised night flow rose 0.9 l/s only because boundary valve BV-0412 passes Moorend Low's supply through its inlet meter; not Calvert Rise, whose rise is the higher pressure its PRV now holds; not Pellow Bridge, whose rise is a new depot's metered night use.

## 2. Critical Components

1. Kestle Hill's normalised net night flow rose **0.9 l/s** while Moorend Low's fell by the same amount, hour for hour across the whole day, so the area boundary on BV-0412 is open.
2. The supply crossing BV-0412 at night is **0.9 l/s**, and netting it leaves Kestle Hill and Moorend Low with an own leakage change of **0.0 l/s** each.
3. Thrushgate's own leakage rose **0.6 l/s**, matched by no neighbour's fall; the runner-up Ashworth Fold rose **0.3 l/s**.

## 3. Step-by-Step Solution

1. Took each area's inlet tags from dma_register_2026-09.xlsx, converted l/s tags to m3/h by its Instrument units sheet, summed two-meter areas and averaged the 03:00 to 04:00 local readings of historian_inlet_flows_20260801_20261102.csv over each night set in LP04 Appendix B.
2. Took off household and unlogged non-household night use at LP04 4.2 and 4.3 and the logged large users' 03:00 hour consumption from amr_large_user_reads_hourly.csv, metered at the register's supply points: Pellow Bridge's rise falls to nothing.
3. Normalised each night set to its baseline AZNP pressure from aznp_pressure_hourly_2026.csv with N1 of 1.15 (LP04 5.1, bar converted to metres): Calvert Rise's rise falls to nothing and Kestle Hill leads at 0.9 l/s.
4. Compared every valve pair in gis_boundary_valves.geojson on its two areas' whole-day volume change: only BV-0412 shows an equal and opposite move, Kestle Hill up and Moorend Low down by the same profile.
5. Took the night crossing as the mean of Kestle Hill's night rise and Moorend Low's night fall, 0.9 l/s, and netted it out of both areas' normalised changes.
6. For the large users, summed hourly register advances per meter (adding 100,000 m3 where a five-digit register rolls over) over October local time for the register's revenue meter at each supply point, the same account's replacement meter and supply points connected since the register issue, leaving out tenants' check meters on bulk supplies.
7. For households, ordered billing_account_events_extract.csv by effective date to 31 October and counted properties with an occupied account whose class, after any CONV event, is HH; for repairs, counted jobs in works_orders_aug_oct_2026.xlsx with a REPAIR MAIN task completed from 1 August to 31 October, a contractor's TC job placed through the job number in its Asset field, areas from mains_asset_list.csv.
8. Ranked the areas on own leakage change: Thrushgate first at 0.6 l/s, Ashworth Fold second at 0.3 l/s.

## 4. Deliverable Answers

### crew_allocation_week46.xlsx

1. Crew area: Thrushgate, 0.6 l/s.
2. Runner-up: Ashworth Fold, 0.3 l/s; gap 0.3 l/s.
3. Change in own leakage by area, l/s, one decimal:
   - Ashworth Fold: 0.3
   - Barrowfold: 0.2
   - Calvert Rise: 0.0
   - Crake Bank: 0.0
   - Gorsey Bank: 0.1
   - Hennick: -0.2
   - Kestle Hill: 0.0
   - Lidden Common: 0.1
   - Moorend Low: 0.0
   - Netherby Road: 0.0
   - Oakshaw: -0.1
   - Pellow Bridge: 0.0
   - Ravensclough: -0.2
   - Stanecroft: 0.0
   - Thrushgate: 0.6
   - Tollbar: -0.1
   - Upper Sowden: 0.0
   - Whinlow Moor: -0.1
4. Metered consumption of logged large users, October 2026, whole m3:
   - Ashworth Fold: 2,756
   - Barrowfold: 4,630
   - Calvert Rise: 2,835
   - Crake Bank: 688
   - Gorsey Bank: 4,437
   - Hennick: 2,867
   - Kestle Hill: 2,121
   - Lidden Common: 2,078
   - Moorend Low: 2,062
   - Netherby Road: 2,800
   - Oakshaw: 2,545
   - Pellow Bridge: 6,346
   - Ravensclough: 1,707
   - Stanecroft: 2,670
   - Thrushgate: 823
   - Tollbar: 2,474
   - Upper Sowden: 4,851
   - Whinlow Moor: 936
5. Occupied household properties at the end of 31 October 2026:
   - Ashworth Fold: 2,135
   - Barrowfold: 3,034
   - Calvert Rise: 3,384
   - Crake Bank: 1,359
   - Gorsey Bank: 1,647
   - Hennick: 3,930
   - Kestle Hill: 2,244
   - Lidden Common: 950
   - Moorend Low: 1,702
   - Netherby Road: 1,993
   - Oakshaw: 1,505
   - Pellow Bridge: 1,802
   - Ravensclough: 1,196
   - Stanecroft: 3,599
   - Thrushgate: 2,564
   - Tollbar: 2,407
   - Upper Sowden: 1,160
   - Whinlow Moor: 2,808
6. Mains repairs completed August to October 2026:
   - Ashworth Fold: 5
   - Barrowfold: 1
   - Calvert Rise: 7
   - Crake Bank: 6
   - Gorsey Bank: 2
   - Hennick: 3
   - Kestle Hill: 4
   - Lidden Common: 5
   - Moorend Low: 6
   - Netherby Road: 5
   - Oakshaw: 3
   - Pellow Bridge: 5
   - Ravensclough: 3
   - Stanecroft: 5
   - Thrushgate: 4
   - Tollbar: 9
   - Upper Sowden: 1
   - Whinlow Moor: 3

### night_flow_changes.pdf

1. One bar per area of the change in own leakage in l/s, Thrushgate's bar marked as the crew's area.
