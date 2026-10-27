## Tags

**Domain:** Actuarial Science & Insurance, pricing, ratemaking and credibility (the lifetime loss ratio of a vehicle service contract channel's next year of sales, costed per mile of exposure at the odometer, for its renewal election under the obligor's rate manual).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Copperline should renew the Fareline channel on 1 January 2027 with the maximum high-use surcharge.**
A 2027 Fareline contract is forecast to cost about 75 per cent of its price in claims over its cover at current rates, over the rate manual's 70 per cent standard, and about 55 per cent at the price with the 40 per cent surcharge, inside it. Repair claims accrue per mile and climb steeply with the odometer past 70,000 miles; a Fareline driver buys cover on a car at about 75,000 miles and drives about 46,000 miles a year, so the 75,000 covered miles run out in about 21 months at odometers the channel's own six months have not reached, and the cover is costed per mile at each odometer from the whole book, which has driven them.

## 2. Critical Components

1. Claims cost per 1,000 miles driven under cover, whole book 2019 to September 2026: about **USD 4.1** below 70,000 miles on the odometer and climbing past it (the workbook's cost per mile sheet, by 10,000-mile band).
2. A 2027 contract's claims cost over its cover, each 2026 Fareline contract run from its odometer at sale at its own annual mileage to the earlier of 75,000 miles and 60 months: about **USD 3,600** against an average price of about **USD 4,790**, a lifetime loss ratio of **75 per cent** at current rates and **55 per cent** with the surcharge (every banding of the odometer and every treatment of the last reading gives 74.4 to 75.2 per cent at current rates).
3. The forecast rests on the **5,933** 2026 Fareline contracts with a weekly feed reading after their sale date.

## 3. Step-by-Step Solution

1. Joined drive_plus_contract_register.csv, contract_number_crosswalk_2024.csv (contract numbers before 4 March 2024 to their new numbers), claim_lines_2019-01_to_2026-09.csv and odometer_readings_2019-01_to_2026-09.csv (Fareline's weekly feed by VIN to its contract) on the contract.
2. Claims cost per claim: parts and labour lines net of the deductible line and of reversed lines, goodwill left out (rate manual 4), at the repair order's odometer.
3. Miles under cover: each contract's odometer path from the sale through its readings in cover to its last reading, stopped at 75,000 miles from the odometer at sale, split by 10,000-mile odometer band.
4. Cost per mile in each band: the band's claims cost over its miles under cover, whole book.
5. Each 2026 Fareline contract's annual mileage from its weekly feed; its cover runs from its odometer at sale to the earlier of 75,000 miles and 60 months at that mileage, costed band by band; averaged over the contracts and divided by their average price, then by 1.4 for the surcharged price (rate manual 3 and 5).
6. For the cancellations, took each contract's first request received (contract terms 5): a dealer's or owner's by contract number, a lienholder's payoff request as the contract on that VIN showing that lienholder (a VIN resold carries the next owner's contract too), and the refund by the terms' formula with the request's odometer or the latest reading on or before it; a contract showing a lienholder refunds to it.
7. For the dealer premium, read the three bordereau layouts (Brazos in cents, the independents by VIN and day-first sale date), and took as not received each dealer-month payment the bank returned, matched in ach_returns_report_2025-2026.csv on the dealer's name in dealer_directory.csv, the settlement month and the payment's total; a payment re-sent on a later bordereau is received.

## 4. Deliverable Answers

### fareline_channel_renewal_2027.pptx

1. Election for 1 January 2027: renew with the maximum high-use surcharge.
2. Lifetime loss ratio of 2027 Fareline sales: about 75 per cent at current rates, about 55 per cent with the 40 per cent surcharge.
3. Chart: claims cost per 1,000 miles by odometer band, flat at about USD 4.1 to 70,000 miles and climbing past it, the bands a Fareline cover runs through marked.

### drive_plus_channel_review_2027.xlsx

1. Retail contracts cancelled and refunds owed: 2026Q1 191 contracts, USD 225,091, of which USD 120,674 to lienholders; 2026Q2 202 contracts, USD 222,805, of which USD 136,837 to lienholders; 2026Q3 193 contracts, USD 264,816, of which USD 145,907 to lienholders.
2. Retail contracts sold in 2025, premium received from dealers to 30 September 2026 and outstanding: 2025Q1 USD 1,252,537 received, USD 28,963 outstanding; 2025Q2 USD 1,322,803 received, USD 4,174 outstanding; 2025Q3 USD 1,341,549 received, USD 25,274 outstanding; 2025Q4 USD 1,276,743 received, USD 41,758 outstanding.
