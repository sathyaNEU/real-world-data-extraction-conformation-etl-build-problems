## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Designate Annaghvale, Ardcullen, Carrigvore, Dunmarra, Glenaskin and Kilbrannagh as rapid price growth areas for 2027.**
Their residential property prices rose by more than 8 per cent in the year to September 2026 on the year before, for a dwelling of unchanged type, floor area, newness and electoral division; no other area's did. The homes that sold in each year are a shifting slice of each area's stock, so the change is the year effect of a hedonic regression rather than a summary of what sold: by dwelling type against the census stock the areas over 8 per cent would be Annaghvale, Ballymarne, Carrigvore, Glenaskin, Innishrue, Kilbrannagh, Moyrath and Rathgowan.

## 2. Critical Components

1. Areas designated: **Annaghvale**, **Ardcullen**, **Carrigvore**, **Dunmarra**, **Glenaskin**, **Kilbrannagh**
2. Areas not designated: Ballymarne, Clonteevan, Corlespie, Drumshallon, Innishrue, Knockfeerin, Lisnafeen, Moyrath, Rathgowan, Tullyvane
3. Price change, year to September 2026 (per cent): Annaghvale 12.3; Glenaskin 12.1; Kilbrannagh 11.5; Carrigvore 10.7; Dunmarra 10.1; Ardcullen 9.9; Innishrue 6.3; Rathgowan 6.2; Drumshallon 6.1; Clonteevan 5.9; Ballymarne 5.7; Moyrath 5.7; Lisnafeen 3.8; Corlespie 3.5; Tullyvane 3.1; Knockfeerin 2.0

## 3. Step-by-Step Solution

1. Read both price register extracts: the old layout's day-first dates and euro text prices, its new-dwelling prices grossed up by 13.5 per cent VAT, and the new system's consideration including VAT.
2. Joined each old-layout sale to the valuation register by its normalised eircode, or by its address where no eircode was keyed, and each new-system sale by property number; counted the filings made in both systems from 1 to 10 October 2025 once.
3. Took each dwelling's type, floor area and newness from the valuation register and its electoral division from the address point file through the eircode.
4. Kept sales at full market price dated 1 October 2024 to 30 September 2026 by date of sale.
5. For each area regressed log price on a year-to-September-2026 indicator, dwelling type, log floor area, new dwelling and electoral division; the change is exp(year effect) less one.
6. Designated the areas over 8 per cent: Annaghvale, Ardcullen, Carrigvore, Dunmarra, Glenaskin, Kilbrannagh.
7. Ask: every residential sale dated 1 October 2025 to 30 September 2026, any market basis; the apartments of a housing body's block share one building, date and consideration (the block's total on each line), so each block is one purchase paid once.

## 4. Deliverable Answers

### bso_area_property_price_change_2026.xlsx

1. Areas designated: Annaghvale, Ardcullen, Carrigvore, Dunmarra, Glenaskin, Kilbrannagh.
2. Chart of every area's price change against the 8 per cent line, the designated areas marked.
3. Price change, year to September 2026 on the year before (per cent, one decimal):
   - Annaghvale: 12.3
   - Ardcullen: 9.9
   - Ballymarne: 5.7
   - Carrigvore: 10.7
   - Clonteevan: 5.9
   - Corlespie: 3.5
   - Drumshallon: 6.1
   - Dunmarra: 10.1
   - Glenaskin: 12.1
   - Innishrue: 6.3
   - Kilbrannagh: 11.5
   - Knockfeerin: 2.0
   - Lisnafeen: 3.8
   - Moyrath: 5.7
   - Rathgowan: 6.2
   - Tullyvane: 3.1
4. Residential purchases in the year to September 2026, number and total paid including VAT (whole euros):
   - Annaghvale: 2,177 purchases, EUR 696,982,000
   - Ardcullen: 2,460 purchases, EUR 838,392,500
   - Ballymarne: 2,355 purchases, EUR 866,667,000
   - Carrigvore: 2,686 purchases, EUR 963,083,000
   - Clonteevan: 1,539 purchases, EUR 418,911,500
   - Corlespie: 1,425 purchases, EUR 359,074,500
   - Drumshallon: 1,978 purchases, EUR 578,041,000
   - Dunmarra: 2,983 purchases, EUR 1,286,799,000
   - Glenaskin: 1,853 purchases, EUR 569,966,000
   - Innishrue: 2,455 purchases, EUR 868,862,500
   - Kilbrannagh: 3,216 purchases, EUR 1,415,960,000
   - Knockfeerin: 1,750 purchases, EUR 489,289,000
   - Lisnafeen: 1,952 purchases, EUR 590,768,500
   - Moyrath: 2,735 purchases, EUR 1,062,521,000
   - Rathgowan: 2,770 purchases, EUR 1,114,686,500
   - Tullyvane: 1,664 purchases, EUR 453,259,000
