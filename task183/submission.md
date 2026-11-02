## Tags

**Domain:** Banking, Credit & Financial Risk (fraud and anti-money-laundering detection).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Refer Crystal Auto Spa (BC-10896) and Polished Nail Studio (BC-10731) to Financial Crime Investigations at the January committee: they lodged EUR 100,000 and EUR 50,000 in 2025-26 beyond what their own trading took, against the EUR 40,000 line.**
Each carried a fixed sum in every lodgement that its own card trade never moved. Not The Abbey Tea Rooms (BC-10444) or Old Town Barber Shop (BC-10643), which lodge 2.6 and 1.9 times their trades' median cash per euro of card trade but whose cash moves with their own card trade, lodgement by lodgement, with no fixed part.

## 2. Critical Components

1. Crystal Auto Spa's 103 lodgements in the year each carry about **EUR 970** that its card trade does not explain.
2. Polished Nail Studio's 103 lodgements in the year each carry about **EUR 485** that its card trade does not explain.
3. No other reviewed customer comes near the line: the highest is **EUR 1,346**.

## 3. Step-by-Step Solution

1. Took each reviewed customer's cash lodgements (type LDG, all its accounts) from the account export de-duplicated on Transaction Ref, dated by the day handed in (the counter date in an AN POST LODGEMENT reference) as BCR-3 dates a lodgement, within BCR-3's review year.
2. Summed each customer's card trade by trading_date (gross less refunds) from the merchant services file, its terminals mapped through the merchant register.
3. Paired each lodgement with the card trade of the days from the customer's previous lodgement to the day before it; on the till customers this window reproduces every lodgement as the till's cash sales less paid-outs, to the cent.
4. Fitted each card customer's lodgements on that card trade by least squares with an intercept and took the cash lodged in the year less the fitted slope times the card trade of the windows those lodgements carry, which is the intercept times the number of lodgements: Crystal Auto Spa EUR 99,899, Polished Nail Studio EUR 49,952, every other card customer EUR 1,346 or less.
5. Took the till customers' figures under BCR-3's till measure as cash lodged in the year less the till's cash sales; every one is negative.
6. An Post: de-duplicated the export on ap_ref and, where notes_eur is not a whole multiple of five euro (the older counter platform writes all the cash there), took notes_eur as the lodgement's cash, else notes_eur plus coin_eur; Schedule 2 fees lodgement by lodgement, rounded as its clause on rounding states; totals by counter month.
7. Till service: placed each Z-report on the latest day, not after its receipt (a morning receipt closes an earlier day), on which its customer's terminal took the same card sales; cash_sales and paid_outs summed by that day's month.
8. Referred every customer over BCR-3's EUR 40,000 line: Crystal Auto Spa at EUR 100,000 and Polished Nail Studio at EUR 50,000, to the nearest five thousand euro.

## 4. Deliverable Answers

### fci_referrals_jan2027.docx

1. Referrals, unexplained cash to the nearest five thousand euro:
   - Crystal Auto Spa, Athlone (BC-10896): EUR 100,000
   - Polished Nail Studio, Tuam (BC-10731): EUR 50,000
2. Bar chart of every reviewed customer's unexplained cash against the EUR 40,000 line, the two referrals marked and labelled, in the memo after the not-referred section.

### cash_review_2026.xlsx

1. Post office counters, cash lodged by business customers and agency fee due, to the cent:
   - October 2025: cash EUR 1,507,545.73, fee EUR 1,876.85
   - November 2025: cash EUR 1,425,294.83, fee EUR 1,778.54
   - December 2025: cash EUR 1,416,027.52, fee EUR 1,778.25
   - January 2026: cash EUR 1,481,013.80, fee EUR 1,851.54
   - February 2026: cash EUR 1,337,503.58, fee EUR 1,653.83
   - March 2026: cash EUR 1,413,914.83, fee EUR 1,770.11
   - April 2026: cash EUR 1,410,976.98, fee EUR 1,785.39
   - May 2026: cash EUR 1,438,140.78, fee EUR 1,796.19
   - June 2026: cash EUR 1,476,062.06, fee EUR 1,819.78
   - July 2026: cash EUR 1,522,007.65, fee EUR 1,909.32
   - August 2026: cash EUR 1,384,580.71, fee EUR 1,753.25
   - September 2026: cash EUR 1,516,109.13, fee EUR 1,890.65
2. Till service, cash sales and paid-outs on each month's trading days, all till-service customers, to the cent:
   - October 2025: cash sales EUR 346,451.75, paid-outs EUR 6,728.64
   - November 2025: cash sales EUR 361,567.45, paid-outs EUR 7,226.25
   - December 2025: cash sales EUR 363,469.60, paid-outs EUR 7,080.51
   - January 2026: cash sales EUR 345,697.45, paid-outs EUR 6,773.76
   - February 2026: cash sales EUR 322,061.01, paid-outs EUR 6,264.91
   - March 2026: cash sales EUR 349,666.76, paid-outs EUR 7,046.34
   - April 2026: cash sales EUR 301,642.38, paid-outs EUR 5,621.91
   - May 2026: cash sales EUR 342,640.37, paid-outs EUR 6,811.74
   - June 2026: cash sales EUR 366,442.65, paid-outs EUR 7,220.53
   - July 2026: cash sales EUR 337,779.51, paid-outs EUR 6,625.73
   - August 2026: cash sales EUR 270,270.49, paid-outs EUR 5,015.02
   - September 2026: cash sales EUR 346,837.40, paid-outs EUR 6,821.63
