**Domain:** Banking, Credit & Financial Risk, fraud and AML detection.
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Business Services should refer Seaview Specialty Foods and Pacifica Donair & Pizza, in that order, to the financial intelligence unit for enhanced investigation in the first quarter of 2027.**
Seaview paid in CAD 477,000 of cash against about 125,000 its counter trade produced (excess 350,000, 2.91 times
produced) and Pacifica 299,000 against about 75,000 (excess 225,000, 3.17 times). Not Kingsway Pho House and Bright
Spark Car Wash, whose cash only outgrew the expected activity they declared years ago and matches their card trade.
Not a measure on peers or on the account's turnover, which the fronts' network payments inflate and which refers
nobody. Not a measure on card and delivery-platform sales together, which counts platform orders paid in the app as
cash-producing and clears Pacifica.

## 2. Critical Components

1. 2026 cash paid in: Seaview Specialty Foods **CAD 477,000**, Pacifica Donair & Pizza **CAD 299,000**
2. 2026 card acquirer settlements: Seaview **CAD 321,676**, Pacifica **CAD 183,043**
3. Cash their trade produced: Seaview **CAD 125,000**, Pacifica **CAD 75,000**
4. Excess: Seaview **CAD 350,000**, Pacifica **CAD 225,000**; no other member's excess reaches its produced cash

## 3. Step-by-Step Solution

1. Mapped every row of hrcu_business_postings_2026.csv to its member through the Accounts sheet of member_register_2026-12-31.xlsx and summed the cash_portion of DEP, COIN, ATMD and NDEP rows with a 2026 effective_date: Seaview 476,947, Pacifica 299,345.
2. Summed each member's 2026 credits narrated CASCADIA MERCH DEP or NORTHGATE PAY STLMT, the card acquirers' settlements of its counter sales: Seaview 321,676, Pacifica 183,043.
3. Took each business type's median, across the segment's members, of cash paid in per dollar of card settlements (grocery 0.379, quick service 0.392), leaving out delivery-platform payouts, business EFTs and cheques, transfers and the CDD declarations, none of which is cash-producing counter trade.
4. Multiplied each member's card settlements by its type's ratio and subtracted it from its cash: Seaview produced 125,000 and excess 350,000 (2.91 times), Pacifica produced 75,000 and excess 225,000 (3.17 times).
5. Applied programme section 7.3 (an excess of CAD 100,000 or more and at least twice the produced cash): only these two meet it; the largest excess that does not is Sunrise Fresh Market's, at 0.75 times its produced cash.
6. Counted section 6.2's 24-hour windows per member on posted_at_utc across all its accounts, quarter by the window's Pacific opening: 25, 40, 44 and 38 required; counted distinct Original report_reference rows in lctr_submissions_2026.csv whose account_number is a segment account, by transaction_date quarter: 19, 44, 44 and 37 filed; counted as late those submitted more than 15 days after the Pacific day of the account's first cash posting on the report's transaction_date (an evening ATM deposit credits the next business date): 2, 6, 11 and 9.
7. Placed each ATM and night deposit credited on a 2026 business date: an ATM deposit at the transit of the terminal's installation in force on its Pacific deposit day (ATMs sheet of branch_atm_depository_directory.xlsx, which lists HR terminals once per installation), a night deposit at its posting transit, or for transit 19004 at the depository that cit_pickup_manifests_2026.csv lists for that bag number on the pickup_date equal to its effective_date.
8. Referred Seaview Specialty Foods then Pacifica Donair & Pizza to the financial intelligence unit, for the Committee's approval in the first quarter of 2027.

## 4. Deliverable Answers

### fiu_referral_slate_2027q1.docx

1. Referred, in descending order of the excess:
   - Seaview Specialty Foods: cash paid in CAD 477,000, cash its trade produced CAD 125,000, excess CAD 350,000
   - Pacifica Donair & Pizza: cash paid in CAD 299,000, cash its trade produced CAD 75,000, excess CAD 225,000
2. Largest excess among members that do not qualify: Sunrise Fresh Market
3. Large cash transaction reports, 2026:
   - Q1: 25 required, 19 filed, 2 late
   - Q2: 40 required, 44 filed, 6 late
   - Q3: 44 required, 44 filed, 11 late
   - Q4: 38 required, 37 filed, 9 late
4. 2026 segment cash through deposit ATMs and in the night depository, CAD:
   - Newton (10342): ATMs 4,503,000, night depository 1,493,000
   - Guildford (10587): ATMs 4,685,000, night depository 1,832,000
   - Richmond Centre (10611): ATMs 5,117,000, night depository 1,636,000
   - Metrotown (10729): ATMs 4,386,000, night depository 1,208,000
   - Coquitlam Centre (10856): ATMs 4,022,000, night depository 1,566,000
   - Uptown New Westminster (10903): ATMs 1,487,000, night depository 1,001,000
   - Langley City (11021): ATMs 1,278,000, night depository 441,000
   - Ladner Village (11168): ATMs 3,527,000, night depository 1,064,000
   - Willowbrook (11204): ATMs 1,505,000, night depository 487,000

### member_cash_review_2026.xlsx

1. Every segment member's 2026 cash paid in on the Members 2026 sheet, Seaview Specialty Foods and Pacifica Donair & Pizza marked as meeting the test with the figures above; the report counts and branch cash above on their own sheets

### cash_review_2026.png

1. Every member's 2026 cash paid in against its produced cash on log scales, with the section 7.3 test line, Seaview Specialty Foods and Pacifica Donair & Pizza labelled with their cash paid in and produced cash
