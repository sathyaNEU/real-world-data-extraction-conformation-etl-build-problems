## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (a county air quality program's 2025-26 residential wood combustion inventory for a PM2.5 maintenance area's five burn zones, conformed from its device registry, its 2024-25 household survey, three propane distributors' delivery exports in three layouts, the airport station's temperatures, the state tool and Census block-group files).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Valley Floor South, East Bench and West Bench exceeded their 2025-26 allotments and share the 2026-27 changeout fund, USD 155,000 each; Valley Floor North and Upper Valley did not.**
In every zone the propane homes with a heating appliance took 26 to 32 per cent less propane in 2025-26 while those without one took what they took in 2024-25, and the wood burned in its place puts the East Bench at 98 tons against 89.9 and the West Bench at 83 against 77.6. Not Valley Floor South alone: carrying the 2024-25 survey's wood per appliance into 2025-26 leaves the benches at 78 and 68 tons, under their allotments.

## 2. Critical Components

1. 2025-26 PM2.5 from residential wood combustion: Valley Floor North **59 tons** (allotment 63.9); Valley Floor South **59 tons** (allotment 52.6); East Bench **98 tons** (allotment 89.9); West Bench **83 tons** (allotment 77.6); Upper Valley **54 tons** (allotment 58.6).
2. PM2.5 from the wood burned in place of propane: Valley Floor North **2 tons**; Valley Floor South **3 tons**; East Bench **20 tons**; West Bench **15 tons**; Upper Valley **7 tons**.

## 3. Step-by-Step Solution

1. Counted the registry's devices in use in 2025-26 (installed before 1 October 2025, not removed) by burn zone and device code, 12,100 appliances, and took each zone's wood per appliance by class from the 2024-25 survey responses as its methods note estimates it (face cords at a third of a cord, pickup loads at half, 40-pound bags).
2. Matched every residential propane account in the Wapiti, Coldwater and cooperative files to its parcel (the geocode, or the cooperative's service address against burn_zone_parcels_2025.csv) and to the registry, splitting each zone's propane homes into those with a heating appliance in use in 2024-25 and 2025-26 and those without one (the state tool gives a fireplace no heating efficiency).
3. Summed each account's deliveries in each heating season (1 October to 30 April): the two groups moved alike from 2023-24 to 2024-25 (season ratios within 0.01 of each other in every zone), and in 2025-26 the homes without a heating appliance took 0.996 to 1.002 times their 2024-25 gallons while the homes with one took 26 to 32 per cent less.
4. Took each home's 2024-25 gallons at its zone's ratio less its 2025-26 gallons as the propane its appliance replaced and burned that heat (91,500 Btu a gallon at 85 per cent furnace efficiency, heating_fuel_equivalents.csv) at the appliance's seasonal efficiency, 18.5 million Btu a cord and 16.4 a ton of pellets: PM2.5 of 2 tons in Valley Floor North, 3 tons in Valley Floor South, 20 tons in East Bench, 15 tons in West Bench and 7 tons in Upper Valley.
5. Added that wood to the survey's wood per appliance times the appliances, at the 2023 factors: 59, 59, 98, 83 and 54 tons against Table 4-2's 63.9, 52.6, 89.9, 77.6 and 58.6.
6. Summed each zone's commercial and institutional accounts' 2025-26 season deliveries by delivery date, reading Coldwater's from the ticket reference (its statement accounts' transactions post on the first of the following month), with NOx at 0.142 lb/MMBtu.
7. Outside the maintenance area, took each 2020 block group's 2019-2023 ACS wood-heated households at its share of housing units outside the area, the assessor's 2010 block groups carried to 2020 through the relationship file (3,622 main-heat households), then the tool's 2.2 secondary households for each, its shares and its use.
8. Split the USD 465,000 fund equally among the 3 zones over their allotments: USD 155,000 each to Valley Floor South, East Bench and West Bench.

## 4. Deliverable Answers

### rwc_inventory_2025_26.xlsx

1. The 2025-26 inventory by burn zone and SCC on sheet RWC inventory, each zone's total carried to the determinations.
2. Commercial and institutional propane delivered in the 2025-26 season (sheet Commercial propane):
   - Valley Floor North: 515,500 gallons, 3.35 tons of NOx
   - Valley Floor South: 437,300 gallons, 2.84 tons of NOx
   - East Bench: 323,000 gallons, 2.10 tons of NOx
   - West Bench: 253,000 gallons, 1.64 tons of NOx
   - Upper Valley: 276,900 gallons, 1.80 tons of NOx
3. Halvard County outside the maintenance area on the state tool (sheet Outside the area):
   - Freestanding woodstoves, not EPA certified: 2,753 appliances, 118.6 tons of PM2.5
   - Freestanding woodstoves, EPA certified, non-catalytic: 2,999 appliances, 50.4 tons of PM2.5
   - Freestanding woodstoves, EPA certified, catalytic: 652 appliances, 9.9 tons of PM2.5
   - Pellet stoves: 1,333 appliances, 4.0 tons of PM2.5
   - Fireplaces: 3,347 appliances, 16.1 tons of PM2.5
   - Outdoor hydronic heaters: 507 appliances, 41.0 tons of PM2.5

### zone_determinations_2026_27.csv

1. One row per burn zone:
   - Valley Floor North: 59 tons of PM2.5, did not exceed, USD 0
   - Valley Floor South: 59 tons of PM2.5, exceeded, USD 155,000
   - East Bench: 98 tons of PM2.5, exceeded, USD 155,000
   - West Bench: 83 tons of PM2.5, exceeded, USD 155,000
   - Upper Valley: 54 tons of PM2.5, did not exceed, USD 0
