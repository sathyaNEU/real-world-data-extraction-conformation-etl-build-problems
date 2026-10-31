## Tags

**Domain:** Economics and econometrics (structural demand: where a product's demand goes when it is unavailable).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Move infant formula onto automated store ordering first: it adds about NZD 60,000 a year to the chain's formula sales.**
Formula's out-of-stock line-days lose their sales outright, because its whole shelf empties when the supplier's weekly delivery is missed. Not bottled water, which has the most out-of-stock line-days (2,714) and the most sales at its lines' own rates, because its shoppers take another water from the same shelf. Not dry pet food, because its shoppers buy the missing bag after the restock. Not gluten-free bakery, which is smaller on every count.

## 2. Critical Components

1. Out-of-stock line-days in 2025-26: bottled water **2,714**, infant formula **1,968**, dry pet food **2,042**, gluten-free bakery **1,900**.
2. Every one of formula's **1,968** out-of-stock line-days falls on the **246** store-days all 8 of its lines were out.
3. Formula adds about **NZD 60,000** a year, the most of the four.

## 3. Step-by-Step Solution

1. Mapped each till code in pos_daily_sales_2024-07_2026-06.parquet to its article with till_item_codes.csv (article numbers to 2 March 2025, GTINs from 3 March, two pack changes) and joined the sales to stock_positions_2024-07_2026-06.csv by store, article and day.
2. Marked each line-day that opened with on_hand_open at zero on a day the store traded (the two refit weeks have no sales and are left out): 2,714, 1,968, 2,042 and 1,900 out-of-stock line-days for water, formula, pet food and gluten-free bakery in 2025-26.
3. Took a line's expected units on a day as its mean on the same weekday within four weeks either side, over days it was on the shelf, outside the fortnight after its own restock and with no other line of its category out (eight weeks either side where four hold fewer than two such days).
4. Took each category's loss as its out lines' expected units on their out days, less its lines' units above expectation on days another of its lines was out and in the fortnight after their own restock, at each line's shelf_price_fy2026_incl_gst in lines.csv, and halved it per store_ordering_2027.docx: formula about NZD 60,000, the most of the four.
5. In cereal_trial_stock_2025-11_2026-05.csv took on_hand as the opening stock up to 1 February 2026 and as the closing stock from 2 February (only from then does a line sell on a day it shows nothing on hand), so a day's opening after go-live is the previous day's close plus that morning's delivery; counted each trial store's line-days that opened with nothing in the 13 weeks either side.
6. In dc_trailer_stops_2025-26.csv counted the stops arriving after the store opened: at 6:30 up to 31 March 2026 and at 7:00 from 1 April, the half hours the first sales in store_trading_days_2025-26.csv start from (stores.csv gives the current 7:00), totalled by island.
7. Joined each delivery_ref in dc_goods_received_2025-26.csv to its appointment in dc_dock_appointments_2025-26.csv and took each appointment's pallets once (the receiving system books a truck's pallets onto every line under every dispatch advice it carried), totalled by category and month of receipt.

## 4. Deliverable Answers

### store_ordering_first_category_2027.pptx

1. Move infant formula onto automated store ordering first: about NZD 60,000 a year.
2. Bar chart of the sales each of the four categories adds a year, infant formula highlighted and labelled about NZD 60,000.

### store_ordering_2027_workbook.xlsx

1. Breakfast cereal out-of-stock line-days after the system went live (2 February to 3 May 2026), and their per cent change from the 13 weeks before, by trial store:
   - Ridgeway Feilding: 26 line-days, -73.7 per cent
   - Ridgeway Levin: 38 line-days, -42.4 per cent
   - Ridgeway Carterton: 40 line-days, -58.8 per cent
2. Distribution centre deliveries that reached a store after it opened, 1 July 2025 to 30 June 2026, by island:
   - North Island: 339
   - South Island: 169
3. Pallets the distribution centre received from each category's suppliers, by month of receipt, July 2025 to June 2026:
   - Bottled water: 188, 185, 262, 205, 223, 249, 247, 221, 178, 259, 221, 200
   - Dry pet food: 277, 224, 228, 290, 214, 240, 209, 176, 258, 198, 193, 207
   - Gluten-free bakery: 33, 34, 37, 44, 35, 41, 35, 33, 38, 31, 46, 29
