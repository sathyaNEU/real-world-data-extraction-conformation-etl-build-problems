## Tags

**Domain:** Physical & Environmental Sciences (hydrology and frequency analysis: a season's irrigation requirement read at 24 in 30 from replayed weather years through a daily root-zone water balance).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Kestrel Bend Irrigation District should order 202,700 acre-feet from the Tolan Valley Project for the 2027 season.**
That is the smallest whole hundred covering the headgate requirement in 24 of the 30 replayed weather years, set by the 2012 replay at 202,660 acre-feet, with every replay started from the root-zone depletion each of the 619 requested fields carries at the end of 31 January 2027. Not an order from replays that start every field at field capacity on 1 February, which leaves out the deficit each field has carried since its last 2026 set in September or October through the driest October to January in the weather record; not one that starts each replay from its own weather year's winter, or from the procedure's irrigation rule run through 2026, because the 2027 season starts from the fields' recorded last sets and the winter that has already fallen.

## 2. Critical Components

1. The 2027 fields are the **619** fields on accepted water requests, **39,399** acres.
2. At the end of 31 January 2027 the root zones are **3.39 inches** below field capacity, acre-weighted, and **446** of the 619 fields are at or past their allowable depletion.
3. The 24th smallest of the thirty replayed headgate requirements is the 2012 replay's **202,660 acre-feet**.

## 3. Step-by-Step Solution

1. Took each field's latest accepted version in kbid_water_requests_2027.xlsx (crop, irrigation method, acres) with its lateral and soil unit from kbid_field_register_2027-02-01.csv per WOP 6.2 of KBID_Water_Order_Procedure_rev2025.pdf, and its total available water and allowable depletion from Tables 2 and 3 of KBID_WOP_tables_2027_order.xlsx per WOP 3.3: 619 fields, 39,399 acres.
2. Spliced the weather record per WOP 6.1: station39_daily_1995-2027.csv converted from millimetres to inches up to 30 April 2014, kbid_station_daily_2014-2027.csv from 1 May 2014, and the network station's values on a day the yard station did not record.
3. Dated each field's last irrigation as the day of its last Delivered 2026 set in kbid_irrigation_orders_2023-2026.csv, ended that day at zero depletion per WOP 3.4, and ran the WOP 3.1 daily balance with the Table 1 coefficients to the end of 31 January 2027: 3.39 inches acre-weighted, 446 fields at or past their allowable depletion.
4. Replayed each weather year 1997 to 2026 from that depletion per WOP 2.4 and 3.1 to 3.5 (its 1 February to 31 October weather with 29 February included, an irrigation on any day ending at or past the allowable depletion delivering the depletion over the Table 4 efficiency) and carried the deliveries to the headgate per WOP 4.1: the 2012 replay is the 24th smallest at 202,660 acre-feet.
5. Summed each lateral's 2026 deliveries by differencing each turnout's reads in kbid_meter_book_2026.csv within each meter and across each meter change through the removal and installation registers in kbid_meter_shop_log_2026.xlsx, in acre-feet with register rollovers carried, crediting the Lateral 5 tail turnouts to Lateral 5 through their 15 June 2026 read and to Lateral 6 after (kbid_canal_operations_log_2026.docx), and set each total against the lateral's heading volumes in kbid_lateral_headings_daily_2026.csv, estimated days included: the deliveries and shares in block 4.
6. Applied each tail weir's equation in kbid_canal_structures.xlsx to each morning's gauge in kbid_tail_weir_sheets_2026.csv, held until the next reading, with the crest raised 2 inches for each flashboard the remarks show in place: the spills in block 4.
7. Scheduled the order per WOP 5.1, each month the order times its share of the thirty replays' summed monthly requirements to the nearest 10 acre-feet and October the difference: the nine months in block 4, 13,520 acre-feet in February and 9,970 in October.
8. Ordered the smallest whole number of hundreds of acre-feet covering at least 24 of the 30 replays per WOP 2.3: 202,700 acre-feet.

## 4. Deliverable Answers

### kbid_order_2027.xlsx

1. 2027 order: 202,700 acre-feet
2. Monthly schedule, acre-feet:
   - February: 13,520
   - March: 970
   - April: 10,290
   - May: 27,190
   - June: 37,470
   - July: 42,010
   - August: 37,270
   - September: 24,010
   - October: 9,970
3. Weather year whose replay sets the order: 2012
4. That replay's headgate requirement: 202,660 acre-feet
5. Each lateral's 2026 deliveries, the share of the water put into it that its turnouts did not deliver, and the water over its tail weir:
   - Lateral 1: 17,820 acre-feet delivered, 8.7 per cent not delivered, 580 acre-feet over the tail weir
   - Lateral 2: 19,610 acre-feet delivered, 9.6 per cent not delivered, 630 acre-feet over the tail weir
   - Lateral 3: 12,800 acre-feet delivered, 8.5 per cent not delivered, 440 acre-feet over the tail weir
   - Lateral 4: 16,960 acre-feet delivered, 14.9 per cent not delivered, 270 acre-feet over the tail weir
   - Lateral 5: 16,500 acre-feet delivered, 8.3 per cent not delivered, 550 acre-feet over the tail weir
   - Lateral 6: 17,300 acre-feet delivered, 13.9 per cent not delivered, 650 acre-feet over the tail weir
   - Lateral 7: 13,880 acre-feet delivered, 8.0 per cent not delivered, 510 acre-feet over the tail weir
   - Lateral 8: 14,430 acre-feet delivered, 12.3 per cent not delivered, 420 acre-feet over the tail weir
   - Lateral 9: 18,210 acre-feet delivered, 13.2 per cent not delivered, 360 acre-feet over the tail weir

### kbid_order_2027.svg

1. Chart of the thirty replayed seasons' headgate requirements from smallest (2024) to largest (2002), the 24 the order covers marked apart from the six above it, the order drawn across them at 202,700 acre-feet, and the 2012 replay labelled as the one that sets it at 202,660 acre-feet.
