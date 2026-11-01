## Tags

**Domain:** Marketing & Consumer Research (media reach, frequency and audience measurement: a metro advertising concessionaire's screen packages, effective reach over its autumn audience window).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Sell Overstappunten, Zuidtak and Oosttak in Tier G in 2027, at 49, 48 and 47 per cent effective reach against the 40 per cent line; every other package stays in the standard tier.** The nearest package below the line is Eindhaltes at 36 per cent. Not Centraal and Binnenstad: with every change of trains put where the line map puts it they reach 63 and 56 per cent, but on weekday peaks the north and east branches run through Centraal into each other, as do the west and south, so the riders who change there are others than the line map shows and both packages reach 33 per cent.

## 2. Critical Components

1. The audience window holds **1,949** regular riders (passenger cards with a metro journey in each of its calendar weeks).
2. On weekdays the trains passing Centraal from 07:00 to 09:30 and from 16:00 to 18:30 run north with east and west with south; at every other time riders change trains where the line map shows.
3. Effective reach is **49 per cent** for Overstappunten, **48 per cent** for Zuidtak and **47 per cent** for Oosttak, and **33 per cent** for Centraal and for Binnenstad.

## 3. Step-by-Step Solution

1. Kept the passenger cards (card class reiziger in RVB_productcodes.csv) of RVB_metro_ritten_20261001_20261104.csv with a journey checked in during each calendar week from 5 October to 1 November 2026 (rate card 3.2 and 3.3): 1,949 regular riders.
2. Gave each of their journeys its check-in and check-out halls through the Gates sheet of RVB_metronet_planningsmodel_2026.xlsx, old and new gate codes alike, and routed it over the network's lines by the fewest changes, crediting the interchange passage wherever the route changes line.
3. Read each journey through Centraal from its own duration against the network's walking and run times in the hours trains run every 3 minutes (a change adds the passage walk and a second wait): on weekdays from 07:00 to 09:30 and 16:00 to 18:30 north-south and west-east riders change there and north-east and west-south riders ride through, and at every other hour the line map holds.
4. Counted for each package in Annex A of Spoorbeeld_tariefkaart_2027.pdf the regular riders whose journeys passed its halls and passages 3 times or more (rate card 3.4 and 3.5): Overstappunten 49, Zuidtak 48 and Oosttak 47 per cent, every other package under 40.
5. For make-good, took each booked screen's dark hours within the opening hours of terms 6.1 from cms_player_status_20261001_20261104.csv (UTC to Ravelmond time), on the player its Bekabeling rows in schermregister_2026-11-12.xlsx give, except that a move off a player that never came back dates from the receiving player's report of its displays rising by the moved screens, plus Wilgenhof's screens from their take-down; then the dark hours above 0.5 per cent of booked screen-hours, rounded up (terms 6.3).
6. For the 2027 screens, took each asset tag's latest Schermen row hung by 1 January 2027 and not taken down by then, kept one screen to a location and position (the replacement units of 3 to 5 November came in under new tags beside rows left open), left out package "-" and counted by package.
7. For net revenue, split the VAT out of facturen_oud_systeem_2026.csv, added the invoices and netted every credit note through its invoice number in billing_export_2026-10-15_2026-11-12.xlsx, and charged each agency's contract rate (its statement in bureaucommissie_najaar_2026.pdf over the value net of the credit notes issued by 31 October: Windroos Media 13.5, Noordlicht Mediaplanning 12.5 and Bureau Overdiep 17.5 per cent) on each booking's value net of all its credit notes (terms 8.2 and 8.3).
8. Recommended Tier G for Overstappunten, Zuidtak and Oosttak.

## 4. Deliverable Answers

### tier_g_2027.xlsx

1. Tier G in 2027: Overstappunten, Zuidtak and Oosttak; every other package in the standard tier.
2. Effective reach, whole per cent, and 2027 tier:
   - Overstappunten (OVP): 49, Tier G
   - Zuidtak (ZDT): 48, Tier G
   - Oosttak (OST): 47, Tier G
   - Eindhaltes (EIN): 36, standard tier
   - Binnenstad (BNS): 33, standard tier
   - Centraal (CEN): 33, standard tier
   - Ringlijn (RNG): 32, standard tier
   - Noordtak (NRD): 31, standard tier
   - Westtak (WST): 25, standard tier
3. Make-good owed per autumn booking, whole hours:
   - SB-26-0411 (Overstappunten): 113
   - SB-26-0414 (Centraal): 34
   - SB-26-0415 (Noordtak): 591
   - SB-26-0419 (Oosttak): 171
   - SB-26-0422 (Binnenstad): 64
   - SB-26-0424 (Zuidtak): 203
   - SB-26-0429 (Centraal): 195
   - SB-26-0430 (Westtak): 45
   - SB-26-0434 (Ringlijn): 87
   - SB-26-0437 (Eindhaltes): 137
4. Screens on sale on 1 January 2027 by package:
   - Centraal: 10
   - Binnenstad: 9
   - Overstappunten: 10
   - Noordtak: 12
   - Oosttak: 18
   - Westtak: 8
   - Zuidtak: 19
   - Ringlijn: 14
   - Eindhaltes: 14
5. Net revenue from the autumn bookings by package, nearest 10 euros:
   - Centraal: EUR 9,100
   - Binnenstad: EUR 5,050
   - Overstappunten: EUR 8,190
   - Noordtak: EUR 5,530
   - Oosttak: EUR 5,930
   - Westtak: EUR 2,310
   - Zuidtak: EUR 7,260
   - Ringlijn: EUR 4,210
   - Eindhaltes: EUR 4,070

### tier_g_2027.pdf

1. One-page bar chart of every package's effective reach, highest first, with the Tier G line at 40 per cent drawn across it and Overstappunten, Zuidtak and Oosttak shaded as Tier G.
