## Tags

**Domain:** Banking, Credit & Financial Risk (fraud and AML detection).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**The 1 December integrity notice should report that the Q3 2026 sweep expunges 5,900 ratings.**
The sweep suspends 241 accounts in 5 rings, which gave 6,517 Q3 ratings; the holdback keeps 597 for manual review and the sweep expunges 5,920. Not the 2,400 that shared-phone links give, which miss the rings run from one phone per account. Not a scaling of the Q2 notice's count or the transparency report's prevalence, which count another quarter's rings or every inauthentic rating.

## 2. Critical Components

1. Ring accounts, every account on a purchase passed within the hour to an account that tops up the seller it was bought from: **241** in **5** rings
2. Q3 ratings those accounts gave, each once in its latest version: **6,517**
3. Ratings the playbook 3.3 holdback keeps for manual review: **597**
4. Ratings expunged: **5,920**, **5,900** to the nearest hundred

## 3. Step-by-Step Solution

1. Read moderation_playbook_v4.2.pdf: a ring is accounts one person or group controls that trade with one another to rate one another, and the sweep expunges every rating its accounts gave in the quarter (1.2, 3.1) less the holdback of 3.3, which covers suspended accounts too.
2. Resolved the released orders in escrow_orders_2026-07.csv, escrow_orders_2026-08.csv and escrow_orders_2026-09.csv by handle, and the wallet_ledger_2026q3.parquet transfers by wallet number with posted_at converted from Lagos time to UTC, to accounts as at each record through accounts.csv and handle_changes.csv.
3. Kept every released order whose buyer made a wallet transfer within the hour after it to an account that made a wallet transfer to that order's seller in the quarter; the buyers, those accounts and the sellers are 241 ring accounts in 5 connected rings.
4. Counted the ratings those accounts gave in ratings_2026q3.parquet (latest version per rating_id, first version in Q3) and applied the holdback seller by seller: 6,517 given, 597 held, 5,920 expunged.
5. For the disputes, put each case in support_cases_2026q3.xlsx on the order whose coins the escrow held at opened_wat (SD-04 1.2: the cited order_ref when it was open then, otherwise the same two accounts' order open then), counted each order once by its fiat currency, and read U and R against the customer who opened the case.
6. For the withdrawals, summed amount_usdt and network_fee_usdt in custodian_outbound_2026q3.parquet over transfers to addresses outside Calabash, by the UTC month of confirmed_at, leaving out the sweeps whose from_address is a deposit address in the wallet ledger's deposit rows.
7. For the cashback, took each group's treasury as the wallet that funded its desks in each week (four groups in merchant_programme_2026-09-30.xlsx moved theirs in August, the old wallet sending its balance to the new one) and summed its transfers to buyers' accounts in Q3 by the group's market, with the different buyers paid.
8. The notice reports 5,900 ratings expunged.

## 4. Deliverable Answers

### q3_ratings_sweep.xlsx

1. One line per ring (accounts suspended, Q3 ratings given, held for manual review, expunged):
   - musa_danj_swap: 53 accounts, 1,379 given, 131 held, 1,248 expunged
   - kumasiotc64: 39 accounts, 1,263 given, 36 held, 1,227 expunged
   - gwarimpapay15: 50 accounts, 1,355 given, 153 held, 1,202 expunged
   - yusuf.desk: 55 accounts, 1,341 given, 186 held, 1,155 expunged
   - chebetfx: 44 accounts, 1,179 given, 91 held, 1,088 expunged
   - All rings: 241 accounts, 6,517 given, 597 held, 5,920 expunged
2. Notice figure: 5,900 ratings expunged
3. Q3 disputes by market (disputed orders, decided for the buyer):
   - Nigeria (NGN): 978 disputed, 557 decided for the buyer
   - Ghana (GHS): 354 disputed, 209 decided for the buyer
   - Kenya (KES): 367 disputed, 210 decided for the buyer
   - United Kingdom (GBP): 107 disputed, 62 decided for the buyer
4. Users' on-chain withdrawals by the UTC month the custodian's transfer confirmed (USDT withdrawn, network fees):
   - July: 1,361,363 USDT withdrawn, 14,862 USDT in network fees
   - August: 1,429,646 USDT withdrawn, 15,605 USDT in network fees
   - September: 1,421,931 USDT withdrawn, 15,102 USDT in network fees
5. Merchant-group cashback paid in Q3 by market (USDT paid, different buyers):
   - Nigeria (NGN): 1,856 USDT to 815 buyers
   - Ghana (GHS): 191 USDT to 81 buyers
   - Kenya (KES): 613 USDT to 289 buyers
   - United Kingdom (GBP): 130 USDT to 51 buyers

### q3_sweep_chart.png

6. Horizontal stacked bar per ring, expunged and held ratings, rings in descending order of expunged, each bar labelled with both counts and the title giving the 5,900 notice figure
