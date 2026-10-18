# task202 submission

## Tags

**Domain:** General statistics and data science (exploratory data analysis and distribution assessment).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Set the 2027/28 referral ceiling for a four-person household at PHP 8,000.**
The schedule it generates refers 5.59 per cent of the awards the scheme resolved in the twelve months to end-March 2027, inside clause 9's 6.0 per cent, and PHP 7,000 refers 6.85 per cent. Not the distribution of the 528 partner-band average awards, which carries no spread within a partner and files PHP 6,000, a schedule that would refer 8.93 per cent. Not the portal's awards pooled or rescaled to the portfolio, which do not reproduce the average award the returns state for each of the other partners. Not a lognormal or a gamma at the portal's coefficient of variation, which the portal's own fit refuses at 16 and 19 times the five per cent critical value.

## 2. Critical Components

1. The twelve months to end-March 2027 hold **49,265** awards in **528** partner-band cells across **88** accredited partners
2. The award shape measured on the window's portal claims has a coefficient of variation of **0.72**
3. At PHP 8,000 the schedule refers **5.59 per cent** of those awards
4. At PHP 7,000 it refers **6.85 per cent**, above the commitment, so PHP 8,000 is the lowest qualifying amount in Schedule E

## 3. Step-by-Step Solution

1. Took the claim returns for April 2026 to March 2027 from hrg_claim_returns_fy2025-26.xlsx and hrg_claim_returns_fy2026-27.xlsx, the revised return superseding the preliminary one for the two reopened months as the policy requires, and recoveries excluded because the policy counts awards gross: 49,265 awards in 528 partner-band cells.
2. Divided each cell's claimed total by its award count: each partner-band's own average award, the only award-level figure the returns state.
3. Resolved portal_awards_2025-01_2027-03.csv's partner reference to the grants ledger through partner_identifier_crosswalk.csv and kept the awards claimed in those twelve months: 11,788 award rows for 22 partners.
4. Expressed each of those awards as a multiple of its own partner-band average award: the award shape, coefficient of variation 0.72, which a single lognormal and a single gamma at that coefficient of variation fit at 16 and 19 times the five per cent Kolmogorov-Smirnov critical value.
5. Rebuilt each cell's award distribution as the cell's own average award times that shape and weighted each cell by its award count, which is the policy's share of the scheme's awards.
6. Generated each band's ceiling from a candidate reference ceiling by schedule B.2's factor in hrg_operating_policy_2027_edition.pdf, rounded up to the nearest PHP 100 under B.3, and took the lowest candidate whose referred share is at or below 6.0 per cent: PHP 8,000 refers 5.59 per cent and PHP 7,000 refers 6.85 per cent.
7. Cut instead on the distribution of the 528 partner-band averages, the ceiling is PHP 6,000 and the schedule refers 8.93 per cent of the window's awards.
8. Set the 2027/28 referral ceiling for a four-person household at PHP 8,000.

## 4. Deliverable Answers

### relief_referral_ceilings_2027-28.xlsx

1. Each band's 2027/28 referral ceiling in pesos, its referred share of that band's own awards and of that band's own award value to one decimal place, and the scale factor applied to three decimals, in band order:
   - 1 person: ceiling PHP 4,000, refers 5.8 per cent of awards and 22.0 per cent of award value, scale factor 0.500
   - 2 persons: ceiling PHP 5,700, refers 5.5 per cent of awards and 21.3 per cent of award value, scale factor 0.707
   - 3 persons: ceiling PHP 7,000, refers 5.4 per cent of awards and 21.0 per cent of award value, scale factor 0.866
   - 4 persons: ceiling PHP 8,000, refers 5.7 per cent of awards and 21.7 per cent of award value, scale factor 1.000
   - 5 persons: ceiling PHP 9,000, refers 5.7 per cent of awards and 21.7 per cent of award value, scale factor 1.118
   - 6 or more persons: ceiling PHP 9,800, refers 5.4 per cent of awards and 21.1 per cent of award value, scale factor 1.225
2. All bands together: refers 5.6 per cent of awards and 21.4 per cent of award value.

### referral_ceiling_board_paper.pdf

1. The recommendation on page 1: set the 2027/28 referral ceiling for a four-person household at PHP 8,000.
2. The same six ceilings, referred shares of awards and of award value, and scale factors as the workbook, in the schedule table on page 1.
3. The award distribution and the ceilings drawn across household sizes: a histogram of the four-person band's award amounts with the PHP 8,000 ceiling marked and the referred tail shaded, beside the six ceilings stepped across the household-size bands with each band's referred share labelled, on page 1.

### claims_annex.xlsx

1. Of each closed scheme quarter's claims, the pesos the Treasury settled and the payment instructions it settled them on:
   - 2024/25 Q1: PHP 31,571,689 on 486 instructions
   - 2024/25 Q2: PHP 30,216,105 on 483 instructions
   - 2024/25 Q3: PHP 23,957,244 on 493 instructions
   - 2024/25 Q4: PHP 26,285,439 on 481 instructions
   - 2025/26 Q1: PHP 39,057,620 on 488 instructions
   - 2025/26 Q2: PHP 38,611,585 on 484 instructions
2. The pesos the pre-payment claim check passed and the pesos it held back in each closed scheme quarter, from each month's own position:
   - 2024/25 Q1: passed PHP 31,794,406, held PHP 262,327
   - 2024/25 Q2: passed PHP 31,066,751, held PHP 145,280
   - 2024/25 Q3: passed PHP 24,486,170, held PHP 265,812
   - 2024/25 Q4: passed PHP 27,483,702, held PHP 162,803
   - 2025/26 Q1: passed PHP 40,061,966, held PHP 271,136
   - 2025/26 Q2: passed PHP 39,820,548, held PHP 224,160
3. The partner claim-months the check held an amount back in, by reason recorded:
   - Receipts incomplete: 73
   - Household record incomplete: 46
   - Duplicate application: 36
   - Component not eligible: 30
   - Arithmetic error on return: 17
   - Not recorded: 76
