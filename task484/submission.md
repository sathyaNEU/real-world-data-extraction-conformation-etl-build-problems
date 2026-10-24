## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (a regional clean air agency's periodic inventory of residential wood combustion for six PM2.5 maintenance areas, built from its device registry, its household survey, its stove changeout programme's applications, the maintenance plans' 2014 base year, the state tool, ACS block-group tables and the assessors' housing units).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Quarrow and Wethermoor trigger their contingency measures for the 2026-27 heating season; Brannock, Ivelton, Saddeny and Ellick do not.**
Each area's 2014 base year is rebuilt for the appliances the plan counted then: the non-certified stoves and outdoor boilers changed out since 2015 burned at the survey's rate for their class and the heat status on their applications (the programme funded main-heat households first), the rest of the 2014 stock at the survey's rate for its class. Carrying the survey's class means back to the 2014 count reads the survivors as the 2014 stock and triggers all six areas.

## 2. Critical Components

1. Areas triggering their contingency measure: **Quarrow** (12.2 per cent against 20) and **Wethermoor** (4.9 per cent against 15).
2. Reductions from the recalculated 2014 base year against each commitment: Brannock 48.2 per cent against 25; Ivelton 30.6 per cent against 22; Quarrow 12.2 per cent against 20; Saddeny 21.0 per cent against 13; Wethermoor 4.9 per cent against 15; Ellick 43.3 per cent against 25.
3. PM2.5 from residential wood combustion in tons, the 2014 base year then the 2025-26 season: Brannock 196.6 and 101.9; Ivelton 117.2 and 81.4; Quarrow 205.1 and 180.2; Saddeny 92.1 and 72.8; Wethermoor 141.9 and 135.0; Ellick 87.7 and 49.7.

## 3. Step-by-Step Solution

1. Counted the 2025-26 appliances: the registry's active devices, each area read on the 2020 boundary through the parcel crosswalk, each device type mapped to its SCC.
2. Took wood burned per appliance from each area's survey respondents by class, face cords at a third of a cord, pickup loads at half, pellets in tons (bags of 40 pounds), 1.163 tons per cord, the 2023 PM2.5 factors.
3. Rebuilt the 2014 base year on the plan's 2014 count: the completed changeouts (applications matched to an area by parcel or street address) at the survey's cords for their class and recorded heat status, the rest of each class at the class mean, the certified and pellet stoves at the survey's units installed by 2014.
4. Took each area's reduction from the 2014 base year to 2025-26 and compared it with its commitment in Table 4-1 of the contingency provisions; below the commitment triggers.
5. Counted the registry's appliances in place in the 2014 season on the 2020 boundaries, a record closed on the day a record of the same kind and install year is registered at its address being the same appliance registered again; the items are appliances registered after the plan's extract and parcels that left an area in 2020.
6. Built each county's remainder on the state tool: each 2020 block group's main-heat households from the 2019-2023 release, times its housing units' share outside the areas (the assessors' 2010 block groups carried to 2020 through the relationship file), 2.4 secondary households per main-heat household, the tool's shares and use.

## 4. Deliverable Answers

### contingency_determinations_2026_27.csv

1. Brannock: 2014 base year 196.6 tons, 2025-26 101.9 tons, reduction 48.2 per cent against 25, NOT TRIGGERED.
2. Ivelton: 2014 base year 117.2 tons, 2025-26 81.4 tons, reduction 30.6 per cent against 22, NOT TRIGGERED.
3. Quarrow: 2014 base year 205.1 tons, 2025-26 180.2 tons, reduction 12.2 per cent against 20, TRIGGERED.
4. Saddeny: 2014 base year 92.1 tons, 2025-26 72.8 tons, reduction 21.0 per cent against 13, NOT TRIGGERED.
5. Wethermoor: 2014 base year 141.9 tons, 2025-26 135.0 tons, reduction 4.9 per cent against 15, TRIGGERED.
6. Ellick: 2014 base year 87.7 tons, 2025-26 49.7 tons, reduction 43.3 per cent against 25, NOT TRIGGERED.

### rwc_periodic_inventory_2025_26.xlsx

1. The 2014 base year's PM2.5 by area and SCC, tons:
   - Brannock: non-certified freestanding woodstoves 140.8; certified non-catalytic woodstoves 26.9; certified catalytic woodstoves 5.0; pellet stoves 1.6; fireplaces 5.2; outdoor hydronic heaters 17.0
   - Ivelton: non-certified freestanding woodstoves 79.1; certified non-catalytic woodstoves 18.1; certified catalytic woodstoves 3.8; pellet stoves 1.5; fireplaces 4.2; outdoor hydronic heaters 10.6
   - Quarrow: non-certified freestanding woodstoves 139.2; certified non-catalytic woodstoves 32.6; certified catalytic woodstoves 5.6; pellet stoves 1.8; fireplaces 7.3; outdoor hydronic heaters 18.6
   - Saddeny: non-certified freestanding woodstoves 62.3; certified non-catalytic woodstoves 15.8; certified catalytic woodstoves 2.1; pellet stoves 0.9; fireplaces 2.6; outdoor hydronic heaters 8.3
   - Wethermoor: non-certified freestanding woodstoves 95.3; certified non-catalytic woodstoves 24.9; certified catalytic woodstoves 3.9; pellet stoves 1.5; fireplaces 4.5; outdoor hydronic heaters 11.9
   - Ellick: non-certified freestanding woodstoves 61.9; certified non-catalytic woodstoves 12.3; certified catalytic woodstoves 2.6; pellet stoves 0.9; fireplaces 2.6; outdoor hydronic heaters 7.3
2. The registry's appliances in place in the 2014 season, by area and SCC (2020 boundaries, each appliance once):
   - Brannock: non-certified freestanding woodstoves 2582; certified non-catalytic woodstoves 1485; certified catalytic woodstoves 299; pellet stoves 544; fireplaces 1186; outdoor hydronic heaters 219
   - Ivelton: non-certified freestanding woodstoves 1797; certified non-catalytic woodstoves 1040; certified catalytic woodstoves 207; pellet stoves 382; fireplaces 828; outdoor hydronic heaters 154
   - Quarrow: non-certified freestanding woodstoves 3347; certified non-catalytic woodstoves 1937; certified catalytic woodstoves 386; pellet stoves 709; fireplaces 1542; outdoor hydronic heaters 283
   - Saddeny: non-certified freestanding woodstoves 1292; certified non-catalytic woodstoves 740; certified catalytic woodstoves 148; pellet stoves 274; fireplaces 591; outdoor hydronic heaters 110
   - Wethermoor: non-certified freestanding woodstoves 2309; certified non-catalytic woodstoves 1335; certified catalytic woodstoves 266; pellet stoves 491; fireplaces 1070; outdoor hydronic heaters 198
   - Ellick: non-certified freestanding woodstoves 1548; certified non-catalytic woodstoves 893; certified catalytic woodstoves 175; pellet stoves 323; fireplaces 711; outdoor hydronic heaters 132
3. Each county's remainder outside the maintenance areas, 2025-26 PM2.5 by SCC, tons:
   - Selwick: non-certified freestanding woodstoves 73.9; certified non-catalytic woodstoves 35.8; certified catalytic woodstoves 7.8; pellet stoves 3.1; fireplaces 12.0; outdoor hydronic heaters 19.8
   - Corrin: non-certified freestanding woodstoves 66.8; certified non-catalytic woodstoves 32.4; certified catalytic woodstoves 7.0; pellet stoves 2.8; fireplaces 10.9; outdoor hydronic heaters 17.9
   - Tamsey: non-certified freestanding woodstoves 72.0; certified non-catalytic woodstoves 34.9; certified catalytic woodstoves 7.6; pellet stoves 3.0; fireplaces 11.7; outdoor hydronic heaters 19.3
