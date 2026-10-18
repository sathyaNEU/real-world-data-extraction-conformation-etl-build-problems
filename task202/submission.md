# task202 submission

## Tags

**Domain:** General statistics and data science (exploratory data analysis and distribution assessment).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Set the 2027/28 referral ceiling for a four-person household at PHP 7,800.**
The schedule it generates refers 5.94 per cent of the awards the scheme resolved in the twelve months to end-March 2027, inside clause 9's 6.0 per cent, and PHP 7,700 refers 6.04 per cent. Not the distribution of the 528 partner-band average awards, which carries no spread within a partner and files PHP 5,800, a schedule that would refer 9.82 per cent. Not the portal's awards pooled or rescaled to the portfolio, which do not reproduce the average award the returns state for each of the other partners. Not a lognormal or a gamma at the portal's coefficient of variation, which the portal's own fit refuses at 16 and 19 times the five per cent critical value.

## 2. Critical Components

1. The twelve months to end-March 2027 hold **49,265** awards in **528** partner-band cells across **88** accredited partners
2. The award shape measured on the window's portal claims has a coefficient of variation of **0.72**
3. At PHP 7,800 the schedule refers **5.94 per cent** of those awards
4. At PHP 7,700 it refers **6.04 per cent**, above the commitment, so PHP 7,800 is the lowest qualifying multiple of PHP 100

## 3. Step-by-Step Solution

1. Took the claim returns for April 2026 to March 2027 from hrg_claim_returns_fy2025-26.xlsx and hrg_claim_returns_fy2026-27.xlsx, the revised return superseding the preliminary one for the two reopened months as the policy requires, and recoveries excluded because the policy counts awards gross: 49,265 awards in 528 partner-band cells.
2. Divided each cell's claimed total by its award count: each partner-band's own average award, the only award-level figure the returns state.
3. Resolved portal_awards_2025-01_2027-03.csv's partner reference to the grants ledger through partner_identifier_crosswalk.csv and kept the awards claimed in those twelve months: 11,788 award rows for 22 partners.
4. Expressed each of those awards as a multiple of its own partner-band average award: the award shape, coefficient of variation 0.72, which a single lognormal and a single gamma at that coefficient of variation fit at 16 and 19 times the five per cent Kolmogorov-Smirnov critical value.
5. Rebuilt each cell's award distribution as the cell's own average award times that shape and weighted each cell by its award count, which is the policy's share of the scheme's awards.
6. Generated each band's ceiling from a candidate reference ceiling by schedule B.2's factor in hrg_operating_policy_2027_edition.pdf, rounded up to the nearest PHP 100 under B.3, and took the lowest candidate whose referred share is at or below 6.0 per cent: PHP 7,800 refers 5.94 per cent and PHP 7,700 refers 6.04 per cent.
7. Cut instead on the distribution of the 528 partner-band averages, the ceiling is PHP 5,800 and the schedule refers 9.82 per cent of the window's awards.
8. Set the 2027/28 referral ceiling for a four-person household at PHP 7,800.

## 4. Deliverable Answers

### relief_referral_ceilings_2027-28.xlsx

1. Each band's 2027/28 referral ceiling in pesos, its referred share of that band's own awards and of that band's own award value to one decimal place, and the scale factor applied to three decimals, in band order:
   - 1 person: ceiling PHP 3,900, refers 6.2 per cent of awards and 22.9 per cent of award value, scale factor 0.500
   - 2 persons: ceiling PHP 5,600, refers 5.8 per cent of awards and 22.1 per cent of award value, scale factor 0.707
   - 3 persons: ceiling PHP 6,800, refers 5.8 per cent of awards and 21.9 per cent of award value, scale factor 0.866
   - 4 persons: ceiling PHP 7,800, refers 6.1 per cent of awards and 22.5 per cent of award value, scale factor 1.000
   - 5 persons: ceiling PHP 8,800, refers 6.0 per cent of awards and 22.4 per cent of award value, scale factor 1.118
   - 6 or more persons: ceiling PHP 9,600, refers 5.7 per cent of awards and 21.8 per cent of award value, scale factor 1.225
2. All bands together: refers 5.9 per cent of awards and 22.2 per cent of award value.

### referral_ceiling_board_paper.pdf

1. The recommendation on page 1: set the 2027/28 referral ceiling for a four-person household at PHP 7,800.
2. The same six ceilings, referred shares of awards and of award value, and scale factors as the workbook, in the schedule table on page 1.
3. The award distribution and the ceilings drawn across household sizes: a histogram of the four-person band's award amounts with the PHP 7,800 ceiling marked and the referred tail shaded, beside the six ceilings stepped across the household-size bands with each band's referred share labelled, on page 1.

### claims_annex.xlsx

1. The pesos the archived payment runs transferred against each closed scheme quarter's claim months, one payment instruction counted once:
   - 2024/25 Q1: PHP 32,135,504
   - 2024/25 Q2: PHP 30,755,712
   - 2024/25 Q3: PHP 24,385,079
   - 2024/25 Q4: PHP 26,754,851
   - 2025/26 Q1: PHP 39,755,121
   - 2025/26 Q2: PHP 39,301,120
2. The pesos the pre-payment claim check held back in each closed scheme quarter, from each month's own hold:
   - 2024/25 Q1: PHP 267,012
   - 2024/25 Q2: PHP 147,874
   - 2024/25 Q3: PHP 270,559
   - 2024/25 Q4: PHP 165,711
   - 2025/26 Q1: PHP 275,978
   - 2025/26 Q2: PHP 228,163
3. The partner claim-months the check held an amount back in, by reason recorded:
   - Receipts incomplete: 73
   - Household record incomplete: 46
   - Duplicate application: 36
   - Component not eligible: 30
   - Arithmetic error on return: 17
   - Not recorded: 76
