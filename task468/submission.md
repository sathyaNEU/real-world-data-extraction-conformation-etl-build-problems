## Tags

> **Domain:** Survey Research & Official Statistics (seasonal adjustment and official time series production: a ward house price index compiled from the price paid record and the council's building control register).
> **Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Give the 2027-28 pressured-ward uplift to Calder Bank (GBP 5,638,095), Kestrel Rise (GBP 3,657,143) and Abbots Hollow (GBP 2,704,762).** Their Ward House Price Index rose 7.9, 6.7 and 5.8 per cent from 2025 to 2026, over the 5.0 per cent line, and no other ward's did. Not Pellbury, whose index rises 6.0 per cent on every pair of its sales but 3.1 per cent once the pairs whose dwelling had building work completed between its two sales are set aside.

## 2. Critical Components

1. Calder Bank's, Kestrel Rise's and Abbots Hollow's index rose **7.9%**, **6.7%** and **5.8%** from 2025 to 2026.
2. Pellbury's index rose **3.1%** with the pairs spanning completed building work set aside, against **6.0%** on every pair.
3. The pressured wards have **148**, **96** and **71** homes due to start on site in 2027-28, **315** in all.

## 3. Step-by-Step Solution

1. Read pp-harrowmere-2015-2025.csv and pp-harrowmere-2026.csv and applied pp-monthly-update-2027-01.csv by transaction identifier: A and C rows stand as published, D rows withdraw the entry.
2. Kept standard (category A) entries for property types D, S, T and F and paired each address's consecutive sales (PAON, SAON, street and postcode), per section 3 of hvha_ward_house_price_index_methodology.pdf.
3. Read both sheets of hcc_building_control_completions_2015-2026.xlsx to house number or name, flat and postcode, and set aside every pair whose dwelling has a completion certificate dated between its two sales, the dwelling being of a different quality at the second sale: Pellbury keeps 226 of its 261 pairs ending in 2026.
4. Placed each pair in its May 2023 ward by postcode (wd23cd in harrowmere_postcode_directory_2026-11.csv), fitted each ward's index by ordinary least squares on the year indicators and took the 2025 to 2026 change: Calder Bank 7.9, Kestrel Rise 6.7, Abbots Hollow 5.8, every other ward under 5.0 (Pellbury 3.1).
5. Ask A: register rows certified in 2026, dwellings created less dwellings lost, each application once (a partial completion and its completion certificate carry the same dwellings), in the ward of the site postcode's wd23cd, since the register's Ward column holds the 2019 wards: 348 in all.
6. Ask B: category B entries for dwellings transferred in 2026, after the update; a portfolio transfer's price stands on each of its titles, so a price on three or more entries of one day is counted once: 525 entries, GBP 160,661,830 in all.
7. Ask C: start-on-site claims in hvha_start_on_site_claims_2025-2027.csv dated 2026 and Paid or Approved, each start once (Calderstone's claims for the starts Brackwell Homes was paid for before the merger repeat the postcode, start date and homes): 1540 homes in all.
8. Shared the GBP 12,000,000 among the three in proportion to homes in Approved or In contract schemes due to start from 1 April 2027 to 31 March 2028 in hvha_affordable_pipeline_2027-28.xlsx, per section 3 of the programme rules: Calder Bank GBP 5,638,095, Kestrel Rise GBP 3,657,143 and Abbots Hollow GBP 2,704,762.

## 4. Deliverable Answers

### harrowmere_pressured_wards_2027-28.pdf

1. Pressured wards for 2027-28: Calder Bank, Kestrel Rise and Abbots Hollow.
2. Shares of the GBP 12,000,000 uplift: Calder Bank GBP 5,638,095; Kestrel Rise GBP 3,657,143; Abbots Hollow GBP 2,704,762.
3. Chart on page 1: every ward's 2025 to 2026 index change as a bar, the 5.0 per cent line marked and the three pressured wards highlighted.

### harrowmere_ward_index_2026.xlsx

1. Index change 2025 to 2026, per cent to one decimal:
   - Abbots Hollow: 5.8
   - Brindley Moor: 3.4
   - Calder Bank: 7.9
   - Dunmore: 2.2
   - Eastholme: 3.9
   - Fennick: 3.6
   - Gorsey Hill: 2.6
   - Hollin Edge: 3.7
   - Kestrel Rise: 6.7
   - Moss Brow: 2.4
   - Pellbury: 3.1
   - Wexley: 3.5
2. Share of the uplift, nearest pound:
   - Abbots Hollow: GBP 2,704,762
   - Brindley Moor: GBP 0
   - Calder Bank: GBP 5,638,095
   - Dunmore: GBP 0
   - Eastholme: GBP 0
   - Fennick: GBP 0
   - Gorsey Hill: GBP 0
   - Hollin Edge: GBP 0
   - Kestrel Rise: GBP 3,657,143
   - Moss Brow: GBP 0
   - Pellbury: GBP 0
   - Wexley: GBP 0
3. Net additional dwellings from building work completed in 2026 (May 2023 wards):
   - Abbots Hollow: 21
   - Brindley Moor: 26
   - Calder Bank: 61
   - Dunmore: 19
   - Eastholme: 16
   - Fennick: 11
   - Gorsey Hill: 17
   - Hollin Edge: 22
   - Kestrel Rise: 35
   - Moss Brow: 60
   - Pellbury: 12
   - Wexley: 48
4. Additional price paid entries for dwellings transferred in 2026, count and money paid to the nearest pound:
   - Abbots Hollow: 45 entries, GBP 14,939,138
   - Brindley Moor: 43 entries, GBP 18,514,750
   - Calder Bank: 93 entries, GBP 22,234,280
   - Dunmore: 28 entries, GBP 12,089,585
   - Eastholme: 51 entries, GBP 15,158,172
   - Fennick: 48 entries, GBP 11,033,449
   - Gorsey Hill: 30 entries, GBP 14,047,363
   - Hollin Edge: 45 entries, GBP 13,924,752
   - Kestrel Rise: 27 entries, GBP 7,121,539
   - Moss Brow: 34 entries, GBP 9,947,892
   - Pellbury: 39 entries, GBP 8,806,141
   - Wexley: 42 entries, GBP 12,844,769
5. Affordable homes started on site in 2026:
   - Abbots Hollow: 131
   - Brindley Moor: 138
   - Calder Bank: 89
   - Dunmore: 158
   - Eastholme: 92
   - Fennick: 164
   - Gorsey Hill: 139
   - Hollin Edge: 133
   - Kestrel Rise: 86
   - Moss Brow: 132
   - Pellbury: 63
   - Wexley: 215
