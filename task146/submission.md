## Tags

**Domain:** Banking, Credit & Financial Risk (deposit and liquidity behaviour: a building society's structural hedge on its instant-access savings).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Set the structural hedge at GBP 165 million in January 2027 and replace the maturing GBP 51 million swap with a new three-year swap of GBP 63 million: Trentmoor will still hold GBP 165 million of the GBP 219 million instant-access savings of 30 November 2026 a year on.**
Run-off measured account by account puts the stable balance at GBP 125 million, because a member who takes up a new Loyalty Saver issue closes one account and opens another the same day with the same amount; that money is still held in instant-access savings.

## 2. Critical Components

1. Each closing payment from an instant-access account that funded an instant-access opening the same local day for the same amount is the same money: the share kept to the first anniversary is **75.4 per cent** across the products, against 57.0 per cent account by account.
2. The Society's stable balance a year on is **GBP 165 million**, two years on **GBP 130 million** and three years on **GBP 104 million**.
3. The swaps outstanding after the January 2027 maturity are **GBP 101.9 million**, so the new swap is **GBP 63 million**.

## 3. Step-by-Step Solution

1. Month-end balances read on their calendar month (the extract dates them on the last business day); product codes mapped on the product register by date (ES02 is Easy Saver Online to 30 June 2025 and Young Saver from 1 July 2025).
2. Account events converted from UTC to UK local time; each CLOSE matched to the instant-access OPEN on the same local day with the same amount in pence.
3. For every account with a balance at each 30 November from 2021, the money followed through its matched openings and its lowest month-end balance taken to each anniversary (a closure with no matched opening ends it).
4. Each product's share kept: the kept balances over the 30 November balances, the start dates taken together, for one, two and three years.
5. Each product's 30 November 2026 balance times its share; summed for the Society.
6. The hedge is the first-anniversary stable balance to the nearest GBP 1 million (policy 7.4); the new swap brings the GBP 101.9 million outstanding after January to it.

## 4. Deliverable Answers

### structural_hedge_reset_2027.pdf

1. Hedge from January 2027: GBP 165 million.
2. Change to the swaps: the maturing GBP 51 million swap replaced by a new three-year swap of GBP 63 million.
3. Chart of the stable balance at each anniversary (GBP 165, 130 and 104 million) against the swaps outstanding at each after the reset.

### stable_balance_ladder_2026-11.xlsx

1. Balance on 30 November 2026, GBP million: Easy Saver 42, Loyalty Saver 133, Easy Access Cash ISA 40, Young Saver 4; total 219.
2. Stable balance 1 year on, GBP million: Easy Saver 29, Loyalty Saver 99, Easy Access Cash ISA 33, Young Saver 4; total 165.
3. Stable balance 2 years on, GBP million: Easy Saver 21, Loyalty Saver 77, Easy Access Cash ISA 28, Young Saver 3; total 130.
4. Stable balance 3 years on, GBP million: Easy Saver 16, Loyalty Saver 61, Easy Access Cash ISA 24, Young Saver 3; total 104.
