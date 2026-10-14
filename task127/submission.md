## Tags

**Domain:** Actuarial Science & Insurance (reserving with development triangles: a motor bodily injury loss reserve).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Carry $400 million for unpaid bodily injury losses at 31 December 2026, $55.4 million more than the $344.6 million finance has booked.**
The figure is $399.8 million: the paid triangle developed after its history is restated at the share of ultimate claimant features the latest diagonal had closed at each age, because since the claims platform went live on 1 July 2024 the book has closed a smaller share of its features at every age than before. Not the paid chain ladder on the triangle as recorded ($316.8 million, $325 million carried and a release), which carries the earlier closing pace onto quarters that are closing more slowly; not the latest diagonals' factors ($283.6 million to $314.1 million), lower still; not severity trended from the 2017 to 2019 quarters ($356.5 million), a twelve-quarter trend carried seven years.

## 2. Critical Components

1. Share of ultimate claimant features closed at eight quarters: **74.4 per cent** in the 2018 to 2020 accident quarters, **71.9 per cent** for 2025 Q1; at twelve quarters **84.7 per cent** against **80.6 per cent** for 2024 Q1
2. Paid to date at 31 December 2026 on the 40 accident quarters from 2017 Q1: **$845.4 million**
3. Unpaid by the restated development: **$399.8 million**, carried at **$400 million**; unrestated, **$316.8 million**

## 3. Step-by-Step Solution

1. Read the legacy payment ledger (dollars, US dates) to 30 June 2024 and the platform's payments (cents, UTC timestamps put on Central time) from 1 July 2024, each void on its own date (ninebark_reserving_basis_2026.pdf), each payment on its feature's accident quarter: $845.4 million paid to date.
2. Took claimant features from the legacy archive without its CV and XD rows and from the platform register without its DUPLICATE rows, a legacy feature re-entered on the platform once, each closed or open at every quarter end from its closing and reopening history (archive CLS_DT, platform events).
3. Built quarterly triangles of paid loss, reported features and closed features for accident quarters 2017 Q1 to 2026 Q4 at ages 1 to 40 (the reserving basis), and ultimate features from the reported triangle's volume-weighted factors.
4. Compared each age's share of ultimate features closed on the latest diagonal with the history: lower at every age from seven quarters (at twelve quarters 80.6 per cent for 2024 Q1 against 84.7 per cent).
5. Restated each accident quarter's paid history at the latest diagonal's closed share for each age, linearly between its own quarter ends, took volume-weighted factors over all accident quarters from the restated triangle and projected the paid to date with them: $399.8 million unpaid.
6. Rounded to the nearest $25 million and set against the register's preliminary $344.6 million for bodily injury loss: carry $400 million, $55.4 million more.
7. Tied account 5311 in gl_5311_bi_paid_loss_2026.csv to the platform's payments: a claims feed batch carries the checks of the Central day before its posting, net of that day's voids (a second batch with a day's checks is not a payment); a Treasury journal carries a month's wires by bank value date (released after 15:00, the next business day); the rest is not claims payments.
8. Counted claimant features closed at 31 December 2026 by accident year, with a loss payment when their net payments in both ledgers to that date (a converted feature's legacy payments and a payment on its claim's duplicate feature included) exceed zero.

## 4. Deliverable Answers

### bi_reserve_ye2026.md

1. Carry $400 million for unpaid bodily injury losses at 31 December 2026, $55.4 million more than the $344.6 million booked.
2. Bodily injury loss the ledger booked in each quarter of 2026 that was claims payments issued in an earlier quarter, and that was not claims payments at all:
   - Q1 2026: $2,760,968.56 issued earlier; $96,250.00 not claims payments
   - Q2 2026: $2,727,945.49 issued earlier; -$96,250.00 not claims payments
   - Q3 2026: $3,528,113.29 issued earlier; $344,291.68 not claims payments
   - Q4 2026: $3,821,032.50 issued earlier; -$344,291.68 not claims payments

### bi_claim_counts_ye2026.csv

1. Claimant features closed at 31 December 2026 with a loss payment and without one, by accident year:
   - 2017: 5,164 with, 853 without
   - 2018: 5,078 with, 893 without
   - 2019: 5,225 with, 892 without
   - 2020: 5,214 with, 931 without
   - 2021: 5,241 with, 962 without
   - 2022: 5,043 with, 1,014 without
   - 2023: 4,586 with, 985 without
   - 2024: 4,065 with, 968 without
   - 2025: 3,697 with, 1,011 without
   - 2026: 2,246 with, 707 without

### bi_unpaid_ye2026.png

1. One bar per accident year 2017 to 2026 of the unpaid carried, largest for 2026, with the carried $400 million and the booked $344.6 million noted.
