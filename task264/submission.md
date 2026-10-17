## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: which food categories a grocery market-data firm's 2027 scanner price index can publish on their own, when a store's week without a sale of a line is a week its chain's shelf price still held, not a missing price).  
**Analytical objective:** Descriptive & Distribution Analysis (each category's change over the 52 weeks to 28 November 2026 in four store formats against its national change, with the panel's sales, store continuity and promotion shares behind the structure).

## 1. Final Recommendation

**Publish 10 of the 18 food categories as stand-alone sub-indices in 2027: Bread and bakery, Breakfast cereals, Cheese, Yoghurt and desserts, Eggs, Deli and cooked meats, Fresh fruit, Frozen foods, Biscuits and Chips and snacks; the other 8 go into Other food.**
With each line followed at the chain that prices it, every one of the 10 has all four format changes within 1.5 points of its national change (the widest, Yoghurt and desserts online, 1.1 points), and the nearest of the 8 left out misses by 0.8 points (Fresh meat and poultry, 2.3 points in neighbourhood stores). Not the 7 that matching each line store by store publishes, because a convenience store's week without a sale drops a price its chain still charged and the convenience index follows the big sellers. Not the 4 that averaging each line over a format's stores publishes, because the July value chain and shoppers' moves toward the discount chain read as supermarket price falls, nor the 8 left when the July chain is taken out, because the shift between the other chains still does.

## 2. Critical Components

1. The widest format gap among the 10 published: **1.1 points** (Yoghurt and desserts, online); the narrowest largest gap among the 8 left out: **2.3 points** (Fresh meat and poultry, neighbourhood)
2. Convenience gaps of the four categories a store-by-store match drops: Breakfast cereals **-0.2** points; Cheese **-0.8** points; Deli and cooked meats **-0.6** points; Biscuits **-0.5** points
3. Coffee and tea's convenience gap: **2.4 points**, outside the band

## 3. Step-by-Step Solution

1. Kept the accepted loads of gpi_movement_ry2026.csv per feed_delivery_log_ry2026.csv (the April resubmission in place of its four superseded weekly loads), matched item codes to gpi_item_master_2026.csv as GTIN-14 (methodology section 8) and stores to chain and format in panel_store_register.csv.
2. Followed each line at the chain that sets its price (partner_chains.xlsx: one shelf price for a line in all the chain's stores in a format): its price in a week is the chain's dollars over units across its stores, so a store that sold none of it that week costs no comparison.
3. Computed each category's GEKS-Tornqvist index in each format over those line-and-chain prices (gpi_methodology_statement_2026.pdf sections 5 and 6) and its change from the average of the first four weeks to the last four.
4. Combined the four format changes with the committee's 2026 format weights (index_committee_terms_2027_structure.pdf, Table 1) for each national change, took each format's gap to it and applied the 1.5-point test in all four formats (terms section 2): 10 categories pass.
5. Summed store_weekly_sales_ry2026.csv over accepted loads, Sunday week-endings moved to the Saturday before, and weeks inside each store's panel period in the register, counting once a store-week the four chains whose rows all repeat the store's weekly total: sales by format.
6. Linked store codes sharing a trading name, suburb and postcode in panel_store_register.csv into one store and counted, for each chain, the stores with movement data in every week from its data agreement or the window's first week.
7. Took each category's share of spending at catalogue specials (gpi_feed_dictionary.xlsx, Terms; each chain's codes in partner_chains.xlsx), counting chain C2's PC as its special before its first TPR week, ending 8 August 2026, and as a price check after.
8. Publish 10 of the 18 categories on their own in 2027.

## 4. Deliverable Answers

### gpi_2027_structure.xlsx

1. Categories published on their own in 2027: 10: Bread and bakery, Breakfast cereals, Cheese, Yoghurt and desserts, Eggs, Deli and cooked meats, Fresh fruit, Frozen foods, Biscuits and Chips and snacks
2. Each category's national change, per cent to one decimal, and each format's change less it, percentage points to one decimal (supermarket, neighbourhood, convenience, online):
   - Bread and bakery: 5.0; 0.0, 0.1, 0.2, -0.1; own sub-index
   - Breakfast cereals: 5.7; 0.2, -0.3, -0.2, -0.2; own sub-index
   - Milk: 5.1; -0.3, -0.3, 3.2, -0.1; Other food
   - Cheese: 5.8; 0.3, -0.4, -0.8, -0.2; own sub-index
   - Yoghurt and desserts: 3.4; -0.3, -0.1, -0.3, 1.1; own sub-index
   - Butter and spreads: 5.5; 0.6, 0.4, 0.5, -2.7; Other food
   - Eggs: 7.7; 0.0, -0.1, 0.1, 0.0; own sub-index
   - Fresh meat and poultry: 4.6; -0.5, 2.3, -0.1, -0.5; Other food
   - Deli and cooked meats: 6.8; 0.5, -0.9, -0.6, -0.8; own sub-index
   - Seafood: 4.7; 0.3, -0.1, -3.1, 0.2; Other food
   - Fresh fruit: 3.6; -0.1, 0.1, 0.8, 0.1; own sub-index
   - Fresh vegetables: 5.2; 1.3, -0.7, -2.9, -2.9; Other food
   - Frozen foods: 3.7; -0.2, -0.6, 1.0, 0.9; own sub-index
   - Biscuits: 6.3; 0.3, -0.5, -0.5, -0.4; own sub-index
   - Confectionery: 6.8; -0.6, -0.4, -0.4, 2.7; Other food
   - Chips and snacks: 3.2; 0.1, -0.5, -0.4, 0.2; own sub-index
   - Soft drinks: 5.1; -0.3, -0.2, 2.8, 0.0; Other food
   - Coffee and tea: 8.0; -0.2, -0.2, 2.4, -0.2; Other food
3. Each category's spending on promotion, per cent to one decimal:
   - Bread and bakery: 13.4
   - Breakfast cereals: 13.4
   - Milk: 12.9
   - Cheese: 14.2
   - Yoghurt and desserts: 13.9
   - Butter and spreads: 13.0
   - Eggs: 13.7
   - Fresh meat and poultry: 14.4
   - Deli and cooked meats: 14.0
   - Seafood: 13.2
   - Fresh fruit: 13.0
   - Fresh vegetables: 12.4
   - Frozen foods: 13.0
   - Biscuits: 13.7
   - Confectionery: 13.1
   - Chips and snacks: 13.2
   - Soft drinks: 12.8
   - Coffee and tea: 13.9
4. Sales of the panel's stores over the 52 weeks while they were in the panel, A$ million to one decimal:
   - Supermarket: 804.4
   - Neighbourhood: 230.7
   - Convenience: 86.7
   - Online: 466.6
5. Stores of each partner chain that sent data in every week the chain was in the panel:
   - S1 Haskard Fresh: 4
   - S2 Brevane Supermarkets: 3
   - S3 Fremett Foods: 3
   - S4 Pravard Discount: 4
   - S5 Gorvery Warehouse: 3
   - N1 Lumbane Local: 3
   - N2 Ruskett Grocers: 3
   - N3 Skovard Local: 4
   - C1 Quorrix: 12
   - C2 Treskola: 15
   - C3 Jorvery Stop: 11
   - O1 Wiskane Online: 2
   - O2 Pembard Direct: 2
   - O3 Keskary: 2

### gpi_2027_structure_paper.docx

1. A paper for the committee recommending the 10 categories, explaining why each line is followed at the chain that prices it rather than matched store by store or averaged over a format, with a dot chart of every category's four format gaps against the 1.5-point band and the panel's sales, store continuity and promotion figures as in the workbook.
