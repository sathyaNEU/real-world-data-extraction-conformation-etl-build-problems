# task285: the 2027 Flood Ready budget

## Tags

**Domain:** Urban & Regional Science (network analysis: road reachability to a hospital under the closures a design flood makes, read through the event).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Share the 2027 Flood Ready budget between the six parishes the design flood would cut off from Hawkesbridge General Hospital: Burnishaw GBP 6,400, Lunnerby GBP 5,786, Hollinside GBP 4,789, Wrennick GBP 4,611, Ravelsby Bridge GBP 4,416 and Cottergill GBP 3,998, 2,093 households in all.**
Each loses every road route at some hour of the event, the three beckside villages while the becks' storage areas are full and the three lower-valley villages while the Quarnell's are. Not Yarrowcote, Hepplewick and Highfold, which the event's deepest water laid on the roads all at once would add (nine parishes, 3,828 households): each loses one route while the becks are high and the other while the Quarnell is, and those closures never fall in the same hour. Not Burnishaw alone, the one parish cut off at hour 43, when the most links are down.

## 2. Critical Components

1. The ridge road's dips in the becks' storage areas are impassable from hour **12** to hour **24** of the design event, and the Quarnell's crossings and river road from hour **30** to hour **57**, so no hour has both closed
2. Cut off at some hour: **Hollinside, Ravelsby Bridge and Lunnerby** (within hours 12 to 24) and **Burnishaw, Wrennick and Cottergill** (within hours 39 to 55); **Yarrowcote, Hepplewick and Highfold** reach the hospital at every hour
3. Households on the council tax valuation list at 1 October 2026 in the six parishes: **2,093**, so after the GBP 3,000 base grants the remaining GBP 12,000 is shared in proportion to them

## 3. Step-by-Step Solution

1. Placed each point of highways_levels_survey_2019.csv on its 2025 link through the chainage ranges of link_reference_crosswalk_2019_2025.csv and in the storage area polygon of storage_areas_QRN25.geojson it falls in.
2. For every hour of storage_area_stages_QRN25_D100CC.csv (guidance section 2), closed each link of highways_network_2025.geojson with a point more than 0.25 m below its storage area's stage: the becks' dips close from hour 12 to 24 and the Quarnell's crossings and river road from hour 30 to 57.
3. Searched the open network from the hospital's node HBN-3224 at each hour and listed every Annex A access point it could not reach at some hour: Hollinside, Ravelsby Bridge, Lunnerby, Burnishaw, Wrennick and Cottergill.
4. Took the households of council_tax_dwellings_by_parish_oct2026.csv and shared the GBP 30,000 as guidance section 3 sets out, GBP 3,000 to each parish and the rest in proportion to households, each grant rounded once: 2,093 households, grants from GBP 3,998 to GBP 6,400.
5. Vouchers (guidance section 4): counted the RD records of address_register_extract_oct2026.csv inside a storage area polygon, parent shells out and flats not among their building's ground floor units in pfr_property_survey_2022.xlsx out, whose storage area's peak stage is above the survey's threshold for the dwelling or its building, else above the register ground level plus 0.15 m, the SURV08 levels raised 0.42 m to Ordnance Datum Newlyn (they sit 0.42 m below the survey's own ground levels at the same UPRNs; model report section 5), old code E04014119 read as Hawkesbridge North.
6. Closures: grouped every row of highways_road_closures_jul2021.csv by its closure site (road and place, not the closure reference, which three re-closures and the B5131 route closure carry from another entry), added the police_road_closures_jul2021.csv closures at the same sites converted from UTC to BST, ran the closure handed to highways to the first barrier at its site, and counted the hours in all, overlapping closures once.
7. Unpaid awards: each 2026 award with its variation in flood_ready_ledger_2026.xlsx less the payments posted to 31 October 2026, the cancelled cheques in bank_cancelled_cheques_2026.csv left unpaid, an instalment under a closed 2025 reference applied to its payee's 2026 award, and one paid under a 2026 reference to the parish's clerk or a village body counted as paid (guidance section 3).
8. Shared the 2027 budget between the six parishes cut off, GBP 30,000 in all.

## 4. Deliverable Answers

### flood_ready_parishes_2027.xlsx

1. Each parish cut off by the design flood or not, with the households (council tax valuation list, 1 October 2026) and the 2027 grant of each one cut off:
   - Hollinside: cut off, 312 households, GBP 4,789
   - Ravelsby Bridge: cut off, 247 households, GBP 4,416
   - Lunnerby: cut off, 486 households, GBP 5,786
   - Whinnerby: not cut off
   - Yarrowcote: not cut off
   - Hepplewick: not cut off
   - Tolmarsh: not cut off
   - Nettlecote: not cut off
   - Burnishaw: cut off, 593 households, GBP 6,400
   - Quernby Moor: not cut off
   - Wrennick: cut off, 281 households, GBP 4,611
   - Cottergill: cut off, 174 households, GBP 3,998
   - Highfold: not cut off
   - Owlthwaite: not cut off
   - Kestlebeck: not cut off
   - Upper Quarnell: not cut off
   - Hawkesbridge North: not cut off
   - Hawkesbridge South: not cut off
   - Six parishes cut off, 2,093 households, the whole budget
2. Dwellings in each parish the design flood would reach at ground floor, whole numbers:
   - Hollinside: 101
   - Ravelsby Bridge: 61
   - Lunnerby: 127
   - Whinnerby: 126
   - Yarrowcote: 123
   - Hepplewick: 124
   - Tolmarsh: 137
   - Nettlecote: 11
   - Burnishaw: 8
   - Quernby Moor: 7
   - Wrennick: 6
   - Cottergill: 60
   - Highfold: 11
   - Owlthwaite: 0
   - Kestlebeck: 0
   - Upper Quarnell: 27
   - Hawkesbridge North: 10
   - Hawkesbridge South: 315
   - All parishes: 1,254
3. Hours in all each closure site in the highways authority's July 2021 duty log was closed by highways or police, to the nearest hour:
   - Hollin Beck, Hollinside, B5131 (first entered as HW21-07-01): 17 hours
   - Ravelsby Brook, Ravelsby Bridge, B5131 (first entered as HW21-07-02): 15 hours
   - Lunnerby Beck, Lunnerby, B5131 (first entered as HW21-07-03): 16 hours
   - Whinnerby Lane ford, C2041 (first entered as HW21-07-04): 5 hours
   - Highfold Road, Cote Bridge, U4108 (first entered as HW21-07-05): 6 hours
   - Hepplewick Road, Mill Bridge, C2045 (first entered as HW21-07-06): 8 hours
   - Yarrowcote Road, Ings Bend, C2043 (first entered as HW21-07-07): 13 hours
   - Tolmarsh Lane, Ford Bridge, C2047 (first entered as HW21-07-08): 3 hours
   - Nettlecote Lane, Nettle Gill, U4105 (first entered as HW21-07-09): 7 hours
4. Each parish's 2026 Flood Ready award still unpaid at 31 October 2026, to the nearest pound:
   - Hollinside (FR26-003): GBP 420
   - Ravelsby Bridge (FR26-005): GBP 770
   - Lunnerby (FR26-007): GBP 5,600
   - Whinnerby (FR26-008): GBP 295
   - Yarrowcote (FR26-010): GBP 1,580
   - Burnishaw (FR26-012): GBP 238
   - Hepplewick (FR26-013): GBP 620
   - Tolmarsh (FR26-015): GBP 400
   - Cottergill (FR26-016): GBP 59
   - Wrennick (FR26-018): GBP 460
   - Upper Quarnell (FR26-019): GBP 132

### flood_ready_parishes_2027.pdf

1. One horizontal bar per cut-off parish of its 2027 grant, split into the base grant and its household share, each labelled with the grant and the parish's households, the largest at the top.
