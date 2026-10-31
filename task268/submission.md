## Tags

**Domain:** Marketing & Consumer Research (segmentation and market structure).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**The 2027 Roastery sampling goes to Oro Rosso's homes.**

Of the 1,857 homes that bought Oro Rosso in 2026, 741 also bought Corcally's Roastery (40%), the lowest share of the rivals and 9 points under Nordhavn (49%). Not Nordhavn, the least overlapped rival read card by card (17%), because its capsule buyers are mostly a home's second card while another member buys the Roastery. Not Westquay, whose homes buy their Roastery through the online shop (79%).

## 2. Critical Components

1. Oro Rosso: **1,857** buying homes, **741** of them also bought the Roastery, **40%**.
2. Runner-up Nordhavn: **1,568** buying homes, **764** also bought the Roastery, **49%**.
3. Gap between them: **9 points**.

## 3. Step-by-Step Solution

1. Mapped each PLU in coffee_till_lines_2026.csv to its brand through product_master_coffee.xlsx (one brand per supplier and range, its spellings folded), kept the 2026 pack lines on Rewards cards, dropped the cards rewards_cards_2026.csv types STORE and folded each REPLACED card into its replaced_by card.
2. Matched every card-paid receipt to its SALE row in faircourt_settlement_2026.parquet on terminal (faircourt_merchant_agreement_2026.pdf, Schedule 2, by installed and removed dates), amount and time (txn_time_utc converted to Irish time, the row up to two minutes before the receipt): 50,047 receipts, one row each.
3. Took each online order in online_orders_2026.json delivered in 2026, its last version's coffee lines, and its card_ref from the settlement row whose merchant_ref is the order number.
4. Joined the Rewards cards and online accounts that share a card_ref into homes (3,802 homes bought coffee), and for each rival counted the homes that bought it and those that also bought Roastery packs: Oro Rosso lowest at 40%, Nordhavn next at 49%.
5. Counter: matched each label in counter_scale_labels_2026.csv to a SALE on terminal 41023121 (labels printed in the 25 minutes before, plus accessories at coffee_counter_price_board_2026.pdf prices) or to a COUNTER COFFEE LOOSE till line of its price; scale 2's labels S2-006398 to S2-006970, printed under January dates, re-dated by the offset that lines them up with those payments; S2 weights read as grams; unpaid labels left out.
6. Funding: each MULTIBUY SAVING line in a deal's dates at the multibuy_deals_2026.xlsx rate in force on the sale day, each reversal netted against the receipt its refund cites, and each MULTIBUY ADJ line added at the date of the receipt its note cites, one multibuy per missed pair on that receipt.
7. The sampling goes to Oro Rosso's homes.

## 4. Deliverable Answers

### roastery_sampling_2027.pptx

1. The 2027 sampling goes to Oro Rosso's homes.
2. Bar chart on slide 2 of every rival's share of buying homes that also bought the Roastery, lowest first, Oro Rosso highlighted.
3. Runner-up Nordhavn at 49%; gap 9 points.
4. Loose coffee the Drumsallagh counter sold, kilograms to one decimal:
   - Glenmore Roasters: Q1 514.0, Q2 503.0, Q3 521.2, Q4 541.9
   - Ardcath Coffee Co.: Q1 441.4, Q2 464.3, Q3 469.5, Q4 470.8
   - Inish Bean: Q1 360.8, Q2 363.1, Q3 374.9, Q4 347.0
5. Multibuy funding owed by each supplier, whole euros:
   - Bellvale Foods Ireland Ltd: Q1 140, Q2 24, Q3 210, Q4 71
   - Cafetto Brands Ireland Ltd: Q1 30, Q2 164, Q3 30, Q4 155
   - Halloran & Sons Coffee Ltd: Q1 259, Q2 139, Q3 174, Q4 388
   - Nordhavn Coffee Ireland Ltd: Q1 259, Q2 43, Q3 233, Q4 53
   - Oro Rosso Caffe Ireland Ltd: Q1 22, Q2 188, Q3 90, Q4 207

### rival_home_overlap_2026.csv

1. One row per rival, lowest share first, whole numbers and whole per cents:
   - Oro Rosso: 1,857 buying homes, 741 also bought the Roastery, 40%
   - Nordhavn: 1,568 buying homes, 764 also bought the Roastery, 49%
   - Halloran's: 2,436 buying homes, 1,244 also bought the Roastery, 51%
   - Cafetto: 1,816 buying homes, 950 also bought the Roastery, 52%
   - Bellvale: 1,696 buying homes, 889 also bought the Roastery, 52%
   - Kinvara Hills: 1,325 buying homes, 744 also bought the Roastery, 56%
   - Westquay: 472 buying homes, 372 also bought the Roastery, 79%
