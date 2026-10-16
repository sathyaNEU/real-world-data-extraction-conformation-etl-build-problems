## Tags

**Domain:** Survey Research & Official Statistics (official time-series production: a retail prices index's grocery and household items compiled from three supermarkets' transaction records and set against the published index over a parallel year).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Move 13 of the sixteen items to transaction data from the January 2027 index: Bread, Breakfast cereals, Biscuits, Yoghurt, Butter and spreads, Coffee, Tea, Soft drinks, Bottled water, Fruit juice, Laundry products, Toilet and kitchen rolls and Toiletries. Keep Pasta and rice, Cheese and Chocolate and sweets on the field collection.**
The moving items' 12-month rates to September 2026 from the transaction data sit within 0.8 points of their published rates; Pasta and rice (4.7 against 2.4), Cheese (-0.2 against 2.7) and Chocolate and sweets (-0.3 against 2.5) are 2.3, 2.9 and 2.8 points apart. Not the five that linking the twelve month-on-month comparisons moves (Bread, Pasta and rice, Yoghurt, Butter and spreads and Fruit juice): in the nine items whose goods keep, an offer month's stocked-up buying weights each price cut heavily and the next month's recovery lightly, and the linked index ends below every line's own change.

## 2. Critical Components

1. Breakfast cereals, the moving item nearest the line: **2.6** per cent against a published **1.8**, a difference of **0.8** points.
2. Pasta and rice, the staying item nearest the line: **4.7** per cent against a published **2.4**, a difference of **2.3** points.
3. Items moving: **13** of 16.

## 3. Step-by-Step Solution

1. Put the three feeds into product-months as the plan defines them: wrenfold_weekly_item_sales_2025_2026.csv with each resent week at its latest extract, gorsedale_period_sales_fy2026_fy2027.txt with each fiscal week dated through gorsedale_fiscal_calendar_fy2026_fy2027.csv and its EANs padded to 13 digits, and calderby_pos_daily_2025_2026.sqlite's daily rows through its sku_gtin table with 5 per cent GST added to the net values; a line is a GTIN at one supermarket, a week belongs to the month in which it ends, and a line's monthly price is its sales value with GST over its units, returns netted.
2. Classified each line through statistics_kellesay_product_classification.csv and kept, for each item, the lines each supermarket sold in every month from September 2025 to September 2026: 1,012 lines over the sixteen items.
3. Compiled each item's monthly index over those lines as a Törnqvist comparison of the month with September 2025 (each line weighted by its spending share averaged over the two months compared) and took the 12-month rate as the index's change from September 2025 to September 2026; GEKS and CCDI over the thirteen months and a direct Fisher give the same sixteen rates to one decimal. Linking the twelve month-on-month comparisons was not used: in the nine items whose goods keep, the month after an offer runs well below normal sales, so the linked index ends 4.6 to 8.4 points below the direct comparison and below every line's own change, which no change in the item's prices can do.
4. Set each rate against the item's published 12-month rate to September 2026 (kellesay_rpi_item_indices_2024_2026.xlsx, sheet 12-month rates) and moved the items whose rates, each to one decimal, are within 1.5 points.
5. For each supermarket and month, dated the arrival of the last file in retailer_delivery_log_2025_2026.csv carrying the month's records (a weekly file's weeks in the month they end, Calderby's extracts by their days, resends and second extracts included), converted from UTC to Kellesay time, counted the days after the month's end, and averaged the thirteen months.
6. Placed each category in retailer_annual_returns_2025.xlsx on its RPI item by its name in retailer_category_map.csv (Wrenfold's 2025 codes name other categories in the map), left out Gorsedale's trade rows, added 5 per cent GST to Calderby's net sales, and divided each item's sales by the households' spending in household_spending_estimates_2025.xlsx.

## 4. Deliverable Answers

### kellesay_rpi_transaction_readiness_2027.xlsx

1. Moving to transaction data in January 2027: Bread, Breakfast cereals, Biscuits, Yoghurt, Butter and spreads, Coffee, Tea, Soft drinks, Bottled water, Fruit juice, Laundry products, Toilet and kitchen rolls and Toiletries; staying on the field collection: Pasta and rice, Cheese and Chocolate and sweets.
2. Each item's lines compared, 12-month rate to September 2026 from the transaction data (per cent), published 12-month rate (per cent), difference (points) and January 2027:
   - 1101 Bread: 62, 1.4, 1.1, 0.3, moves
   - 1103 Breakfast cereals: 75, 2.6, 1.8, 0.8, moves
   - 1105 Pasta and rice: 67, 4.7, 2.4, 2.3, stays
   - 1108 Biscuits: 77, 2.7, 2.6, 0.1, moves
   - 1145 Yoghurt: 66, 1.7, 1.4, 0.3, moves
   - 1146 Cheese: 62, -0.2, 2.7, -2.9, stays
   - 1151 Butter and spreads: 43, 1.4, 1.4, 0.0, moves
   - 1182 Chocolate and sweets: 87, -0.3, 2.5, -2.8, stays
   - 1211 Coffee: 60, 5.6, 5.8, -0.2, moves
   - 1212 Tea: 50, 1.7, 1.4, 0.3, moves
   - 1221 Soft drinks: 87, 2.2, 2.3, -0.1, moves
   - 1222 Bottled water: 37, 0.6, 0.7, -0.1, moves
   - 1223 Fruit juice: 41, 1.7, 1.2, 0.5, moves
   - 5611 Laundry products: 56, 2.6, 2.6, 0.0, moves
   - 5613 Toilet and kitchen rolls: 43, 2.6, 2.5, 0.1, moves
   - 6213 Toiletries: 99, 2.5, 2.4, 0.1, moves
3. Each supermarket's average number of calendar days after a month's end until its records for the month were complete, September 2025 to September 2026:
   - Wrenfold Stores: 2.0
   - Gorsedale Co-operative: 8.0
   - Calderby's: 8.6
4. Each item's 2025 coverage, the supermarkets' retail sales with GST as a share of households' spending, whole per cent:
   - 1101 Bread: 68
   - 1103 Breakfast cereals: 58
   - 1105 Pasta and rice: 67
   - 1108 Biscuits: 77
   - 1145 Yoghurt: 55
   - 1146 Cheese: 69
   - 1151 Butter and spreads: 59
   - 1182 Chocolate and sweets: 73
   - 1211 Coffee: 59
   - 1212 Tea: 62
   - 1221 Soft drinks: 57
   - 1222 Bottled water: 60
   - 1223 Fruit juice: 58
   - 5611 Laundry products: 60
   - 5613 Toilet and kitchen rolls: 66
   - 6213 Toiletries: 73

### kellesay_item_indices_parallel_year.png

1. One panel per item: its transaction-data index and its published index by month, September 2025 = 100, each panel titled with whether the item moves and its two 12-month rates; the 13 moving items' transaction-data lines in one colour and the three staying items' in another.

### kellesay_transaction_product_months_2025_2026.csv

1. 14,364 rows, one per supermarket line and month of the sixteen items over the parallel year (1,172 lines), each with the line's units, sales value with GST and unit price; 1,012 of the lines are in the lines compared.
