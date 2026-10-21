## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Designate Annaghvale, Ardcullen, Carrigvore, Dunmarra, Glenaskin, Kilbrannagh and Moyrath as rapid price growth areas for 2027.**
The market value of each one's dwelling stock rose by more than 8 per cent in the year to September 2026 on the year before; no other area's did. Each dwelling type's change is held to constant quality by a hedonic regression with location, and the four are weighted by the census stock's value, because apartments sell far more often than the stock holds them and in some areas rose differently from houses: one year effect for all sales would designate Annaghvale, Ardcullen, Drumshallon, Dunmarra, Glenaskin, Innishrue and Kilbrannagh.

## 2. Critical Components

1. Areas designated: **Annaghvale**, **Ardcullen**, **Carrigvore**, **Dunmarra**, **Glenaskin**, **Kilbrannagh**, **Moyrath**
2. Areas not designated: Ballymarne, Clonteevan, Corlespie, Drumshallon, Innishrue, Knockfeerin, Lisnafeen, Rathgowan, Tullyvane
3. Price change, year to September 2026 (per cent): Glenaskin 12.0; Kilbrannagh 11.2; Annaghvale 10.6; Moyrath 10.4; Dunmarra 10.2; Ardcullen 10.1; Carrigvore 9.5; Rathgowan 5.7; Drumshallon 5.6; Clonteevan 5.3; Ballymarne 5.2; Innishrue 4.8; Corlespie 3.8; Lisnafeen 3.8; Tullyvane 3.6; Knockfeerin 3.4

## 3. Step-by-Step Solution

1. Read both price register extracts: the old layout's day-first dates and euro text prices, its new-dwelling prices grossed up by 13.5 per cent VAT, and the new system's consideration including VAT.
2. Joined each old-layout sale to the valuation register by its normalised eircode, or by its address where no eircode was keyed, and each new-system sale by property number; counted the filings made in both systems from 1 to 10 October 2025 once.
3. Took each dwelling's type, floor area and newness from the valuation register and its electoral division from the address point file through the eircode.
4. Kept sales at full market price dated 1 October 2024 to 30 September 2026 by date of sale.
5. For each area regressed log price on a year-to-September-2026 indicator for each dwelling type, dwelling type, log floor area, new dwelling and electoral division.
6. Weighted each type's exp(year effect) by the census count of that type times its mean first-year price (the stock's value) and took the weighted mean less one as the area's change.
7. Designated the areas over 8 per cent: Annaghvale, Ardcullen, Carrigvore, Dunmarra, Glenaskin, Kilbrannagh, Moyrath.
8. Ask: every residential sale dated 1 October 2025 to 30 September 2026, any market basis; the apartments of a housing body's block share one building, date and consideration (the block's total on each line), so each block is one purchase paid once.

## 4. Deliverable Answers

### bso_area_property_price_change_2026.xlsx

1. Areas designated: Annaghvale, Ardcullen, Carrigvore, Dunmarra, Glenaskin, Kilbrannagh, Moyrath.
2. Chart of every area's price change against the 8 per cent line, the designated areas marked.
3. Price change, year to September 2026 on the year before (per cent, one decimal):
   - Annaghvale: 10.6
   - Ardcullen: 10.1
   - Ballymarne: 5.2
   - Carrigvore: 9.5
   - Clonteevan: 5.3
   - Corlespie: 3.8
   - Drumshallon: 5.6
   - Dunmarra: 10.2
   - Glenaskin: 12.0
   - Innishrue: 4.8
   - Kilbrannagh: 11.2
   - Knockfeerin: 3.4
   - Lisnafeen: 3.8
   - Moyrath: 10.4
   - Rathgowan: 5.7
   - Tullyvane: 3.6
4. Residential purchases in the year to September 2026, number and total paid including VAT (whole euros):
   - Annaghvale: 2,164 purchases, EUR 712,798,500
   - Ardcullen: 2,457 purchases, EUR 843,585,000
   - Ballymarne: 2,368 purchases, EUR 860,503,000
   - Carrigvore: 2,674 purchases, EUR 928,926,000
   - Clonteevan: 1,540 purchases, EUR 400,369,000
   - Corlespie: 1,433 purchases, EUR 366,873,500
   - Drumshallon: 1,973 purchases, EUR 546,154,500
   - Dunmarra: 2,978 purchases, EUR 1,181,753,500
   - Glenaskin: 1,870 purchases, EUR 575,617,000
   - Innishrue: 2,058 purchases, EUR 574,199,000
   - Kilbrannagh: 3,229 purchases, EUR 1,425,305,000
   - Knockfeerin: 1,756 purchases, EUR 502,370,000
   - Lisnafeen: 1,944 purchases, EUR 606,609,500
   - Moyrath: 2,302 purchases, EUR 686,107,000
   - Rathgowan: 2,766 purchases, EUR 1,123,996,000
   - Tullyvane: 1,660 purchases, EUR 460,510,500
