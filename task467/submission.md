## Tags

**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Wrenfield & Holt should pay GBP 127,785 into the customer goodwill fund for the 8,519 refunds it made late in January to June 2026, and report February, March and April as the months that broke the 95 per cent commitment.**
Each refund's delivery day comes from replaying the goods-in scans and the openings in the order the centre works its hall, the newest parcel waiting opened first, the order every labelled opening shows (181,318 of 181,318). Not GBP 189,330 with February and March only, which pairing the two records in arrival order gives: that order matches 1,759 of the labelled openings and finds none of 2025's late refunds. Not GBP 192,000, which treating every waiting parcel as equally likely gives. Not GBP 0, which reading the opening day as the delivery day gives.

## 2. Critical Components

1. The newest parcel waiting is the one opened on **181,318** of **181,318** labelled openings (every opening to the end of 2025 and the labelled stragglers opened to April 2026); arrival order matches **1,759**.
2. Replayed that way, 2025's labelled late refunds are reproduced: **615** in February and **889** in December, both of which arrival order puts at **0**.
3. Refunds made late, January to June 2026: **0, 1,106, 5,292, 1,935, 151 and 35** (shares **0.0, 7.1, 28.9, 14.5, 1.2 and 0.3** per cent of each month's refunds).

## 3. Step-by-Step Solution

1. Took the return's definitions from paragraphs 2 to 5 of calvermoor_written_assurance_oct2026.pdf: return refunds made in each month, made late on day 15 or later counting calendar days from the goods-in scan day, GBP 15 a late refund, 95 per cent made by day 14 each month.
2. Joined cotterby_goods_in_2025.csv and cotterby_goods_in_2026.parquet into one UK-time record of return parcels delivered, and dated each return refund from wh_refund_ledger_2025_2026.parquet at its PAID row (a failed card refund at its store-credit reissue): 87,641 refunds made in January to June 2026.
3. Tested the pairing of deliveries to openings on the openings in cotterby_returns_processing_2025_2026.csv that carry the parcel's prepaid label (every opening to the end of 2025 and the labelled stragglers opened to April 2026): newest-first matches 181,318 of 181,318, arrival order 1,759.
4. Replayed every delivery and opening from 2 December 2024 in time order, each opening (rejected parcels included) taking the newest parcel waiting, which reproduces 2025's labelled late refunds (615 in February, 889 in December).
5. Counted each 2026 month's refunds made on day 15 or later from their parcel's delivery day: 8,519 in all, with more than 5 per cent late in February, March and April; the payment is 8,519 refunds at GBP 15, GBP 127,785.
6. Valued every voucher in wh_goodwill_vouchers_2026.csv in pounds by its UK issue month, reading each customer's currency from wh_orders_returning_customers.parquet and converting euros at the extract's reporting rate of 0.86 (a euro voucher is redeemed on euro orders in wh_voucher_redemptions_2026.csv).
7. Counted and valued every Refund delay voucher issued in January to June by the main category of the order named in the case it was issued on (wh_customer_cases_2026.csv), not the voucher's own order field, which for some vouchers names a later order of the customer's that was never returned or refunded.
8. Recommendation: pay GBP 127,785 and report February, March and April as breach months.

## 4. Deliverable Answers

### goodwill_fund_return_h1_2026.csv

1. One row per month (refunds made; refunds made late; late share in per cent; met the 95 per cent commitment; goodwill vouchers issued in pounds):
   - 2026-01: 14,103; 0; 0.0; yes; 3,325
   - 2026-02: 15,546; 1,106; 7.1; no; 16,561
   - 2026-03: 18,301; 5,292; 28.9; no; 9,832
   - 2026-04: 13,300; 1,935; 14.5; no; 1,575
   - 2026-05: 12,894; 151; 1.2; yes; 1,229
   - 2026-06: 13,497; 35; 0.3; yes; 1,023

### refund_timeliness_note.pdf

1. Payment into the goodwill fund: GBP 127,785.
2. Months that broke the commitment: February, March and April 2026.
3. A bar chart of each month's late share against a dashed 5 per cent commitment line, the breach months' bars in red and marked missed, on page 1.
4. Vouchers issued in January to June for a refund delay, by the category of the order the refund was on (vouchers; value in pounds):
   - Womenswear: 1,523; 11,117
   - Menswear: 648; 4,693
   - Footwear: 621; 4,537
   - Home: 402; 2,840
   - Kids: 356; 2,608
   - Accessories: 275; 1,922
