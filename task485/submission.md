## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (a national agriculture department's regional inventory of ammonia from cattle manure for the 2025-26 programme year, conformed from the bovine register's animal and movement exports, its herd register, the June census by farm, the land parcel register's farmed area and the environmental protection office's Tier 2 factors).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**The Minister should designate Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Inner Basin and Lower Basin as Ammonia Action Regions for the 2027 spreading season: on the ammonia from cattle manure arising in each region over 2025-26 these six regions are at or above 26 kilograms a hectare of farmed land, and the other six are under it.**
Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Inner Basin and Lower Basin stand at 31.53, 29.74, 28.48, 34.23, 28.10 and 28.31 kilograms a hectare. Not Lake Uplands, Middle Uplands, Eastern Uplands, Western Seaboard and Atlantic Coast, at 24.23, 23.62, 20.27, 23.92 and 20.10: the cattle on their holdings on 1 June include lowland yearlings out on summer grazing and calves bought in that spring, whose housed months fall in other regions, so the census at the annual factor per head puts them over the line. Not without Inner Basin and Lower Basin, at 28.10 and 28.31: their finishers house stores all winter and send them to slaughter before June, which the census misses.

## 2. Critical Components

1. Ammonia from cattle manure arising in the twelve regions, 1 November 2025 to 31 October 2026: **1,352.2 tonnes**.
2. Farmed land of the twelve regions in the 2026 land parcel register, commonage at each herd's share: **50,930.53 hectares**.

## 3. Step-by-Step Solution

1. Rebuilt each animal's days in nbr_animals_2025-26.csv and nbr_movements_2025-26.csv, from its date of birth or 1 November 2025 to the day before its exit date or 31 October 2026, in HERD_AT_START and then in each destination herd from its arrival date (nbr_export_notes.txt): 37,319,657 animal-days.
2. Put each herd number in the 2024 region of its district in nbr_herd_register_2026-11.xlsx, a reissued number at the record valid on the day (designation rules, section 4).
3. Classed each day by epo_cattle_ammonia_factors_2025.pdf (section 2 and the annex's dairy breeds) and charged Table 3's housed rate on days inside the Table 4 housing season of the region the animal was in that day and its grass rate on the others: 1,352.2 tonnes of ammonia.
4. Divided each region's ammonia by its farmed land in lpr_farmed_area_2026.csv by the herds' regions, a commonage parcel at the herd's SHARE_PCT: 50,930.53 hectares.
5. Tested each region against 26 kilograms a hectare on the unrounded figures (designation rules, section 5): six regions at or above it.
6. For the contractors, took cattle slurry jobs dated 13 January to 30 April 2026 on herds in the herd register from vale_agri_jobs_2026.csv (loads times the tanker's gallons), countrywide_invoice_lines_2026.xlsx (SS- services, thousands of gallons) and basin_agri_job_sheets_2026.xlsx (metered cubic metres), at 0.00454609 cubic metres a gallon, and counted each job once: a Countrywide line whose Reference is a Vale Agri Job No or a Basin Agri Job No bills that contractor's job, so it is left out and the job sheet's volume and spreader are kept; trailing shoe, trailing hose, dribble bar, umbilical dribble bar and shallow injection are low-emission (designation rules, section 6): 243,900 cubic metres, 54.7 per cent low-emission.
7. The Minister designates the six regions at or above the line.

## 4. Deliverable Answers

### ammonia_action_regions_2027.xlsx

1. Ammonia from cattle manure arising in each region over 2025-26, tonnes, kilograms a hectare of farmed land, and whether designated:
   - Northern Vale: 177.4 tonnes, 31.53 kg a hectare, designated
   - Eastern Vale: 191.9 tonnes, 29.74 kg a hectare, designated
   - Southern Vale: 176.1 tonnes, 28.48 kg a hectare, designated
   - Coastal Vale: 177.9 tonnes, 22.91 kg a hectare, not designated
   - Midland Basin: 102.2 tonnes, 34.23 kg a hectare, designated
   - Inner Basin: 82.1 tonnes, 28.10 kg a hectare, designated
   - Lower Basin: 105.0 tonnes, 28.31 kg a hectare, designated
   - Lake Uplands: 57.9 tonnes, 24.23 kg a hectare, not designated
   - Middle Uplands: 62.7 tonnes, 23.62 kg a hectare, not designated
   - Eastern Uplands: 50.5 tonnes, 20.27 kg a hectare, not designated
   - Western Seaboard: 79.3 tonnes, 23.92 kg a hectare, not designated
   - Atlantic Coast: 89.1 tonnes, 20.10 kg a hectare, not designated
2. Cattle slurry spread by contractors on each region's farms from 13 January to 30 April 2026, cubic metres to the nearest hundred, and the share spread by trailing shoe, trailing hose or injection, per cent:
   - Northern Vale: 34,100 cubic metres, 44.5 per cent
   - Eastern Vale: 34,400 cubic metres, 54.7 per cent
   - Southern Vale: 25,900 cubic metres, 65.4 per cent
   - Coastal Vale: 35,900 cubic metres, 77.8 per cent
   - Midland Basin: 19,500 cubic metres, 37.1 per cent
   - Inner Basin: 15,600 cubic metres, 29.5 per cent
   - Lower Basin: 22,600 cubic metres, 72.7 per cent
   - Lake Uplands: 9,600 cubic metres, 19.4 per cent
   - Middle Uplands: 9,900 cubic metres, 53.1 per cent
   - Eastern Uplands: 9,800 cubic metres, 70.9 per cent
   - Western Seaboard: 12,100 cubic metres, 26.1 per cent
   - Atlantic Coast: 14,700 cubic metres, 62.5 per cent

### cattle_ammonia_per_hectare_2025-26.png

1. Horizontal bar chart of each region's kilograms of ammonia a hectare against the 26 kilogram line, the six designated regions (Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Inner Basin and Lower Basin) in orange beyond the line and the other six in grey under it.
