## Tags

**Domain:** Survey Research & Official Statistics (seasonal adjustment and official time-series production: the airport's monthly taxi trip series restated across a temporary intervention).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Set the 2027 taxi pickup fee at $6.50.**
2025's 74,753 fee-liable pickups, restated to the forecourt rank, are 84,000, and $6.50 is the lowest 25-cent step at which they recover the $535,027 the 2027 budget assigns to the fee (a surplus of about $10,000; $6.25 falls about $10,000 short). Not $5.75, which takes the pickups' whole 22 per cent fall as the rank's although the Airport Line, opened the same day, took part of it for good; not $7.00, which sets all pickups against all drop-offs and finds only 3 per cent, because the drop-offs come mostly from the line's station zones.

## 2. Critical Components

1. 2025's fee-liable pickups as recorded: **74,753**.
2. The share of 2025's restated pickups the temporary rank cost: **11 per cent**, pickups against drop-offs within the Airport Line's station zones and within the other zones.
3. 2025 restated to the forecourt rank: **84,000** budgeted pickups.

## 3. Step-by-Step Solution

1. Counted 2025's trips beginning in zone 1 in vfh_taxi_trips_airport_2025.parquet, the final annual file FP-07 4.4 names (voided trips are not in it): 74,753 fee-liable pickups.
2. Built daily pickups and drop-offs by zone from vfh_od_daily_archive_2023.csv, vfh_taxi_trips_airport_2024.parquet (each voided trip and its reversal taken out) and the 2025 file.
3. Grouped the city zones into the four named for the Airport Line's stations in velmont_transit_airport_line_service_bulletin.pdf (Downtown Central, Midtown, University and Commerce Park in vfh_taxi_zones.csv), the only zones whose drop-offs fell from the twelve months before 4 November 2024 to 2025 (each by about a third), and the rest.
4. In each group, the ratio of pickups to drop-offs was 10.6 per cent lower in 2025 than in the twelve months before the move in the station zones and 11.0 per cent lower in the other zones.
5. Restated 2025 under FP-07 4.3 as each group's 2025 drop-offs at the group's ratio of pickups to drop-offs in the twelve months before the move, summed: 84,000 pickups, of which the rank cost 11 per cent.
6. Applied By-law GT-3 s.4 to the $535,027 on line 12 of vaa_2027_ground_transportation_budget.xlsx: $6.50 is the lowest step that recovers it (a surplus of about $10,000; $6.25 about $10,000 short).
7. For the ledger, billed each pickup once, to the brokerage its taxi belonged to when the trip began, at Schedule A's fee for the trip's year (By-law GT-3 s.3): 2025 from the annual file with the licence's brokerage on the trip date in vfh_vehicle_affiliations.csv (the file's brokerage_id is the licence's brokerage when the file was built), 2026 from the eight monthly files in Velmont local time, each voided trip and its reversal out and each re-sent copy (same licence, minute, zones and amounts as an earlier record) out.
8. Recommended the 2027 fee of $6.50 a pickup.

## 4. Deliverable Answers

### velmont_2027_taxi_pickup_fee.docx

1. The 2027 fee: $6.50 a pickup.
2. 2025's fee-liable pickups: 74,753 as recorded, 84,000 as restated.
3. The share of 2025's restated pickups the temporary rank cost: 11 per cent.
4. Against the $535,027 the 2027 budget assigns to the fee: surplus at $6.50, $10,000; shortfall at $6.25, $10,000.
5. Line chart of monthly fee-liable pickups and airport drop-offs, November 2023 to August 2026, in the memo's Monthly trips section, the temporary rank's months shaded.

### velmont_taxi_fee_ledger_2025_2026.csv

1. One row per brokerage per month, January 2025 to August 2026, 120 rows: fee-liable pickups (whole trips) and fees owed (dollars and cents):
   - 2025-01, Kestrel Cabs: 1,070 pickups, $6,152.50
   - 2025-01, Northgate Taxi: 1,033 pickups, $5,939.75
   - 2025-01, Lakeside Cabs: 921 pickups, $5,295.75
   - 2025-01, Velmont City Cab: 1,319 pickups, $7,584.25
   - 2025-01, Harbour Taxi: 774 pickups, $4,450.50
   - 2025-01, Westbrook Taxi: 583 pickups, $3,352.25
   - 2025-02, Kestrel Cabs: 941 pickups, $5,410.75
   - 2025-02, Northgate Taxi: 863 pickups, $4,962.25
   - 2025-02, Lakeside Cabs: 797 pickups, $4,582.75
   - 2025-02, Velmont City Cab: 1,134 pickups, $6,520.50
   - 2025-02, Harbour Taxi: 633 pickups, $3,639.75
   - 2025-02, Westbrook Taxi: 556 pickups, $3,197.00
   - 2025-03, Kestrel Cabs: 1,148 pickups, $6,601.00
   - 2025-03, Northgate Taxi: 1,142 pickups, $6,566.50
   - 2025-03, Lakeside Cabs: 1,015 pickups, $5,836.25
   - 2025-03, Velmont City Cab: 1,419 pickups, $8,159.25
   - 2025-03, Harbour Taxi: 848 pickups, $4,876.00
   - 2025-03, Westbrook Taxi: 702 pickups, $4,036.50
   - 2025-04, Kestrel Cabs: 1,127 pickups, $6,480.25
   - 2025-04, Northgate Taxi: 1,093 pickups, $6,284.75
   - 2025-04, Lakeside Cabs: 908 pickups, $5,221.00
   - 2025-04, Velmont City Cab: 1,339 pickups, $7,699.25
   - 2025-04, Harbour Taxi: 784 pickups, $4,508.00
   - 2025-04, Westbrook Taxi: 692 pickups, $3,979.00
   - 2025-05, Kestrel Cabs: 1,222 pickups, $7,026.50
   - 2025-05, Northgate Taxi: 1,184 pickups, $6,808.00
   - 2025-05, Lakeside Cabs: 978 pickups, $5,623.50
   - 2025-05, Velmont City Cab: 1,544 pickups, $8,878.00
   - 2025-05, Harbour Taxi: 926 pickups, $5,324.50
   - 2025-05, Westbrook Taxi: 721 pickups, $4,145.75
   - 2025-06, Kestrel Cabs: 1,144 pickups, $6,578.00
   - 2025-06, Northgate Taxi: 1,086 pickups, $6,244.50
   - 2025-06, Lakeside Cabs: 931 pickups, $5,353.25
   - 2025-06, Velmont City Cab: 1,385 pickups, $7,963.75
   - 2025-06, Harbour Taxi: 803 pickups, $4,617.25
   - 2025-06, Westbrook Taxi: 714 pickups, $4,105.50
   - 2025-07, Kestrel Cabs: 1,354 pickups, $7,785.50
   - 2025-07, Northgate Taxi: 1,261 pickups, $7,250.75
   - 2025-07, Lakeside Cabs: 1,098 pickups, $6,313.50
   - 2025-07, Velmont City Cab: 1,612 pickups, $9,269.00
   - 2025-07, Harbour Taxi: 1,005 pickups, $5,778.75
   - 2025-07, Westbrook Taxi: 831 pickups, $4,778.25
   - 2025-08, Kestrel Cabs: 1,388 pickups, $7,981.00
   - 2025-08, Northgate Taxi: 1,347 pickups, $7,745.25
   - 2025-08, Lakeside Cabs: 1,144 pickups, $6,578.00
   - 2025-08, Velmont City Cab: 1,721 pickups, $9,895.75
   - 2025-08, Harbour Taxi: 978 pickups, $5,623.50
   - 2025-08, Westbrook Taxi: 816 pickups, $4,692.00
   - 2025-09, Kestrel Cabs: 1,123 pickups, $6,457.25
   - 2025-09, Northgate Taxi: 1,068 pickups, $6,141.00
   - 2025-09, Lakeside Cabs: 885 pickups, $5,088.75
   - 2025-09, Velmont City Cab: 1,385 pickups, $7,963.75
   - 2025-09, Harbour Taxi: 785 pickups, $4,513.75
   - 2025-09, Westbrook Taxi: 661 pickups, $3,800.75
   - 2025-10, Kestrel Cabs: 1,202 pickups, $6,911.50
   - 2025-10, Northgate Taxi: 1,171 pickups, $6,733.25
   - 2025-10, Lakeside Cabs: 979 pickups, $5,629.25
   - 2025-10, Velmont City Cab: 1,480 pickups, $8,510.00
   - 2025-10, Harbour Taxi: 808 pickups, $4,646.00
   - 2025-10, Westbrook Taxi: 729 pickups, $4,191.75
   - 2025-11, Kestrel Cabs: 1,152 pickups, $6,624.00
   - 2025-11, Northgate Taxi: 1,116 pickups, $6,417.00
   - 2025-11, Lakeside Cabs: 962 pickups, $5,531.50
   - 2025-11, Velmont City Cab: 1,421 pickups, $8,170.75
   - 2025-11, Harbour Taxi: 816 pickups, $4,692.00
   - 2025-11, Westbrook Taxi: 683 pickups, $3,927.25
   - 2025-12, Kestrel Cabs: 1,145 pickups, $6,583.75
   - 2025-12, Northgate Taxi: 1,164 pickups, $6,693.00
   - 2025-12, Lakeside Cabs: 963 pickups, $5,537.25
   - 2025-12, Velmont City Cab: 1,459 pickups, $8,389.25
   - 2025-12, Harbour Taxi: 846 pickups, $4,864.50
   - 2025-12, Westbrook Taxi: 716 pickups, $4,117.00
   - 2026-01, Kestrel Cabs: 1,255 pickups, $8,471.25
   - 2026-01, Northgate Taxi: 1,000 pickups, $6,750.00
   - 2026-01, Lakeside Cabs: 947 pickups, $6,392.25
   - 2026-01, Velmont City Cab: 1,166 pickups, $7,870.50
   - 2026-01, Harbour Taxi: 826 pickups, $5,575.50
   - 2026-01, Westbrook Taxi: 568 pickups, $3,834.00
   - 2026-02, Kestrel Cabs: 1,069 pickups, $7,215.75
   - 2026-02, Northgate Taxi: 861 pickups, $5,811.75
   - 2026-02, Lakeside Cabs: 769 pickups, $5,190.75
   - 2026-02, Velmont City Cab: 974 pickups, $6,574.50
   - 2026-02, Harbour Taxi: 747 pickups, $5,042.25
   - 2026-02, Westbrook Taxi: 480 pickups, $3,240.00
   - 2026-03, Kestrel Cabs: 1,409 pickups, $9,510.75
   - 2026-03, Northgate Taxi: 1,144 pickups, $7,722.00
   - 2026-03, Lakeside Cabs: 1,112 pickups, $7,506.00
   - 2026-03, Velmont City Cab: 1,345 pickups, $9,078.75
   - 2026-03, Harbour Taxi: 954 pickups, $6,439.50
   - 2026-03, Westbrook Taxi: 609 pickups, $4,110.75
   - 2026-04, Kestrel Cabs: 1,356 pickups, $9,153.00
   - 2026-04, Northgate Taxi: 1,120 pickups, $7,560.00
   - 2026-04, Lakeside Cabs: 1,158 pickups, $7,816.50
   - 2026-04, Velmont City Cab: 1,294 pickups, $8,734.50
   - 2026-04, Harbour Taxi: 879 pickups, $5,933.25
   - 2026-04, Westbrook Taxi: 600 pickups, $4,050.00
   - 2026-05, Kestrel Cabs: 1,331 pickups, $8,984.25
   - 2026-05, Northgate Taxi: 1,122 pickups, $7,573.50
   - 2026-05, Lakeside Cabs: 1,191 pickups, $8,039.25
   - 2026-05, Velmont City Cab: 1,297 pickups, $8,754.75
   - 2026-05, Harbour Taxi: 929 pickups, $6,270.75
   - 2026-05, Westbrook Taxi: 630 pickups, $4,252.50
   - 2026-06, Kestrel Cabs: 1,274 pickups, $8,599.50
   - 2026-06, Northgate Taxi: 1,112 pickups, $7,506.00
   - 2026-06, Lakeside Cabs: 1,159 pickups, $7,823.25
   - 2026-06, Velmont City Cab: 1,247 pickups, $8,417.25
   - 2026-06, Harbour Taxi: 968 pickups, $6,534.00
   - 2026-06, Westbrook Taxi: 634 pickups, $4,279.50
   - 2026-07, Kestrel Cabs: 1,511 pickups, $10,199.25
   - 2026-07, Northgate Taxi: 1,257 pickups, $8,484.75
   - 2026-07, Lakeside Cabs: 1,314 pickups, $8,869.50
   - 2026-07, Velmont City Cab: 1,536 pickups, $10,368.00
   - 2026-07, Harbour Taxi: 1,122 pickups, $7,573.50
   - 2026-07, Westbrook Taxi: 737 pickups, $4,974.75
   - 2026-08, Kestrel Cabs: 1,483 pickups, $10,010.25
   - 2026-08, Northgate Taxi: 1,210 pickups, $8,167.50
   - 2026-08, Lakeside Cabs: 1,263 pickups, $8,525.25
   - 2026-08, Velmont City Cab: 1,466 pickups, $9,895.50
   - 2026-08, Harbour Taxi: 1,054 pickups, $7,114.50
   - 2026-08, Westbrook Taxi: 666 pickups, $4,495.50
