## Tags

**Domain:** Physical & Environmental Sciences (hydrology and frequency analysis: a season's irrigation requirement read at 24 in 30 from replayed weather years through a daily root-zone water balance).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Kestrel Bend Irrigation District should order 215,000 acre-feet from the Tolan Valley Project for the 2027 season.**
That is the smallest whole number of thousands of acre-feet that covers the 2027 fields' headgate requirement in 24 of the 30 replayed weather years, with every replay started from each field's root zone as it stands at the end of 31 January 2027, rebuilt from the water its 2026 sets delivered. Not an order built from each field's last 2026 set taken as a refill, because the 501 drip, micro-sprinkler and sprinkler fields never returned to field capacity after the spring and their last sets left them short of it; not one from replays that start every field full or from each weather year's own winter, because the 2027 season starts from the state the fields are in after the driest October to January in the weather record.

## 2. Critical Components

1. The 2027 fields are the **631** fields on accepted water requests, **40,309** acres.
2. Run through the daily balance on the water their 2026 sets delivered, the **501** drip, micro-sprinkler and sprinkler fields end their last 2026 sets short of field capacity.
3. The 24th smallest of the thirty replayed headgate requirements, the 2012 replay's, lies between **214,000** and **215,000** acre-feet.

## 3. Step-by-Step Solution

1. Took each field's latest accepted version in kbid_water_requests_2027.xlsx (crop, irrigation method, acres) with its lateral and soil unit from kbid_field_register_2027-02-01.csv per WOP 6.2 of KBID_Water_Order_Procedure_rev2025.pdf, and its total available water and allowable depletion from Tables 2 and 3 of KBID_WOP_tables_2027_order.xlsx per WOP 3.3: 631 fields, 40,309 acres.
2. Spliced the weather record per WOP 6.1: station39_daily_1995-2027.csv converted from millimetres to inches up to 30 April 2014, kbid_station_daily_2014-2027.csv from 1 May 2014, and the network station's values on a day the yard station did not record.
3. Ran each field's root zone through the WOP 3.1 balance from field capacity at the end of 27 January 2026, when the 2025-26 winter's rains had filled every root zone, to the end of 31 January 2027, each Delivered 2026 set in kbid_irrigation_orders_2023-2026.csv putting its ordered flow for the hours it ran on each day into the root zone at the Table 4 efficiency of the field's method: the 501 drip, micro-sprinkler and sprinkler fields end their last 2026 sets short of field capacity.
4. Replayed each weather year 1997 to 2026 from that state per WOP 2.4 and 3.1 to 3.5 (its 1 February to 31 October weather, 29 February included, an irrigation on any day ending at or past the allowable depletion delivering the depletion over the Table 4 efficiency) and carried the deliveries to the headgate per WOP 4.1: the 24th smallest requirement, the 2012 replay's, lies between 214,000 and 215,000 acre-feet.
5. Summed each lateral's 2026 turnout deliveries from kbid_meter_book_2026.csv, each meter's reads differenced in its own register units converted to acre-feet with rollovers carried, each mid-season meter swap chained through the Reg. out and Reg. in of its work order in kbid_meter_shop_log_2026.xlsx, and the west spur turnouts 05-021 to 05-034 credited to Lateral 5 through their 15 June 2026 read and to Lateral 6 after (kbid_canal_operations_log_2026.docx): the deliveries in block 4.
6. Summed each lateral's water put in from the daily totals in kbid_lateral_headings_daily_2026.csv with the Water Master's estimates in kbid_canal_operations_log_2026.docx for the days a heading logger kept no total, and took the share not delivered as the water put in less the deliveries, over the water put in: the water put in and the shares in block 4.
7. Applied each tail weir's equation in kbid_canal_structures.xlsx to each morning's gauge in kbid_tail_weir_sheets_2026.csv, held until the next reading, with the crest raised 2 inches for each flashboard the riders' remarks put in place: the spills in block 4.
8. Ordered the smallest whole number of thousands of acre-feet covering at least 24 of the 30 replays per WOP 2.3: 215,000 acre-feet.

## 4. Deliverable Answers

### kbid_order_2027.xlsx

1. 2027 order: 215,000 acre-feet
2. Each lateral's 2026 turnout deliveries, the water put into it, the share of that water its turnouts did not deliver, and the water over its tail weir:
   - Lateral 1: 17,870 acre-feet delivered, 19,680 acre-feet put in, 9.2 per cent not delivered, 580 acre-feet over the tail weir
   - Lateral 2: 17,530 acre-feet delivered, 19,410 acre-feet put in, 9.7 per cent not delivered, 630 acre-feet over the tail weir
   - Lateral 3: 15,400 acre-feet delivered, 16,880 acre-feet put in, 8.8 per cent not delivered, 440 acre-feet over the tail weir
   - Lateral 4: 17,890 acre-feet delivered, 21,020 acre-feet put in, 14.9 per cent not delivered, 270 acre-feet over the tail weir
   - Lateral 5: 18,160 acre-feet delivered, 19,760 acre-feet put in, 8.1 per cent not delivered, 550 acre-feet over the tail weir
   - Lateral 6: 18,210 acre-feet delivered, 21,060 acre-feet put in, 13.5 per cent not delivered, 650 acre-feet over the tail weir
   - Lateral 7: 15,310 acre-feet delivered, 16,710 acre-feet put in, 8.4 per cent not delivered, 510 acre-feet over the tail weir
   - Lateral 8: 11,490 acre-feet delivered, 13,110 acre-feet put in, 12.4 per cent not delivered, 420 acre-feet over the tail weir
   - Lateral 9: 15,080 acre-feet delivered, 17,370 acre-feet put in, 13.2 per cent not delivered, 360 acre-feet over the tail weir

### kbid_order_2027.svg

1. Chart of the thirty replayed seasons' headgate requirements from smallest (2024) to largest (2002), the 24 the order covers marked apart from the six above it, the order drawn across them at 215,000 acre-feet, and the 2012 replay labelled as the one that sets it.
