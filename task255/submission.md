## Tags

**Domain:** Marketing & Consumer Research (media reach, frequency and audience measurement: a metro advertising concessionaire's screen packages, effective reach over its autumn audience window).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Sell Overstappunten, Oosttak and Zuidtak in Tier G in 2027, at 47, 47 and 46 per cent effective reach against the 40 per cent line; every other package stays in the standard tier.** The nearest package below the line is Eindhaltes at 35 per cent. Not Centraal and Binnenstad: with every change of trains put where the line map puts it they reach 63 and 56 per cent, but on weekday peaks the north and east branches run through Centraal into each other, as do the west and south, so the riders who change there are others than the line map shows, and they reach 34 and 33 per cent.

## 2. Critical Components

1. The audience window holds **1,901** regular riders (passenger cards with a metro journey in each of its calendar weeks).
2. Each journey through Centraal shows from its own duration whether the rider changed trains there, and on weekday peaks the changes fall on north-south and west-east journeys, not on north-east and west-south ones; at every other time riders change where the line map shows.
3. Effective reach is **47 per cent** for Overstappunten, **47 per cent** for Oosttak and **46 per cent** for Zuidtak, and **34 per cent** for Centraal and **33 per cent** for Binnenstad.

## 3. Step-by-Step Solution

1. Kept the passenger cards (card class reiziger in RVB_productcodes.csv) of RVB_metro_ritten_20261001_20261104.csv with a journey checked in during each calendar week from 5 October to 1 November 2026 (rate card 3.2 and 3.3): 1,901 regular riders.
2. Gave each of their journeys its check-in and check-out halls through the Gates sheet of RVB_metronet_planningsmodel_2026.xlsx, old and new gate codes alike, and routed it over the network's lines by the fewest changes, crediting the interchange passage wherever the route changes line.
3. Read each journey through Centraal from its own duration: the minutes it took over its hall walks and run times leave an empty band across the record (a change adds the passage walk and a second wait), and a journey above the band changed trains there; on weekday peaks that is the north-south and west-east riders while the north-east and west-south riders ride through, and at every other time the line map holds.
4. Counted for each package in Annex A of Spoorbeeld_tariefkaart_2027.pdf the regular riders whose journeys passed its halls and passages 3 times or more (rate card 3.4 and 3.5): Overstappunten 47, Oosttak 47 and Zuidtak 46 per cent, every other package under 40.
5. For make-good, took each booked screen's dark hours within the opening hours of terms 6.1 from cms_player_status_20261001_20261104.csv (UTC to Ravelmond time), a player whose first status there is online being offline until then, on the player its Bekabeling rows in schermregister_2026-11-12.xlsx give, except that a screen moved off a player that never came back connects from the receiving player's first report counting it among its displays (terms 6.2); then the dark hours above 0.5 per cent of booked screen-hours, rounded up (terms 6.3).
6. For the 2027 screens, took each asset tag's latest Schermen row hung by 1 January 2027 and not taken down by then, kept one screen to a location and position (the replacement units of 2 to 4 November came on the old units' player outputs, the players' display counts unchanged, under new tags beside rows left open), left out package "-" and counted by package.
7. For net revenue, split the VAT out of facturen_oud_systeem_2026.csv, added the invoices and netted every credit note through its invoice number in billing_export_2026-10-15_2026-11-12.xlsx, and charged each agency's contract rate (its statement in bureaucommissie_najaar_2026.pdf over the value net of the credit notes issued by 31 October: Windroos Media 13.5, Noordlicht Mediaplanning 12.5 and Bureau Overdiep 17.5 per cent) on each booking's value net of all its credit notes (terms 8.2 and 8.3).
8. Recommended Tier G for Overstappunten, Oosttak and Zuidtak.

## 4. Deliverable Answers

### tier_g_2027.xlsx

1. Tier G in 2027: Overstappunten, Oosttak and Zuidtak; every other package in the standard tier.
2. Effective reach, whole per cent, and 2027 tier:
   - Overstappunten (OVP): 47, Tier G
   - Zuidtak (ZDT): 46, Tier G
   - Oosttak (OST): 47, Tier G
   - Eindhaltes (EIN): 35, standard tier
   - Binnenstad (BNS): 33, standard tier
   - Centraal (CEN): 34, standard tier
   - Ringlijn (RNG): 32, standard tier
   - Noordtak (NRD): 32, standard tier
   - Westtak (WST): 24, standard tier
3. Make-good owed per autumn booking, whole hours:
   - SB-26-0411 (Overstappunten): 254
   - SB-26-0414 (Centraal): 161
   - SB-26-0415 (Noordtak): 734
   - SB-26-0419 (Oosttak): 101
   - SB-26-0422 (Binnenstad): 207
   - SB-26-0424 (Zuidtak): 252
   - SB-26-0429 (Centraal): 65
   - SB-26-0430 (Westtak): 91
   - SB-26-0434 (Ringlijn): 342
   - SB-26-0437 (Eindhaltes): 256
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

### tier_g_2027.svg

1. Bar chart of every package's effective reach, highest first, the Tier G line at 40 per cent drawn across it and Overstappunten, Oosttak and Zuidtak shaded as Tier G, titled with the call.
