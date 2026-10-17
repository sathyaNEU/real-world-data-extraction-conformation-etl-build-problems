## Tags

**Domain:** General Statistics & Data Science (resampling and simulation methods: a trace-driven simulation of six yard islands, each vehicle's recorded duty replayed visit by visit through the island's one-tankful-a-visit limit).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Contract 23 of Overton's loads for 14 September to 8 November (Memphis 2, Jackson 5, Nashville 8, Cookeville 1, Knoxville 4, Blountville 3), saving $17,408 against the same gallons on the card accounts.**
An island fuels a vehicle only at its yard visits, at most the tankful above the reserve its driver keeps, so each yard's draw is built from the fuel each vehicle burns between visits. Not the vehicles' card gallons, which count the fuel Blountville's four-night sleepers and Cookeville's lot-based vans have to buy on the road; not the 2025 islands' share of the same vehicles' fuel, measured on Jackson and Knoxville fleets mostly back every day or between one-night loops; and not a tankful per run between nights at the yard, which misses Nashville's midweek reload.

## 2. Critical Components

1. Nashville's **15** sleepers are in the yard at midday every Wednesday, so each takes two island fills a week and the island keeps nearly all of their fuel.
2. Blountville's **11** sleepers on four-night loops and Cookeville's **32** vans based at the Sparta and Crossville lots are in the yard once a week, so each takes at most one tankful a week.
3. Each load saves **$800** on Delta's Riverbend account (Memphis, Jackson), **$640** on Crossroads (Nashville, Cookeville, its network fee included) and **$864** on SMPM (Knoxville, Blountville).

## 3. Step-by-Step Solution

1. Took the 157 active units, their yards and their models' fuel tanks from fleet_units_2026-08.xlsx, and named each telematics row by its vehicle, through telematics_device_assignments.csv where a new device reported under its serial.
2. Paired each unit's Enter and Exit rows at its own yard's geofence in geofence_events_2026-03-01_2026-08-27.csv into yard visits, and cut its days in vehicle_days_2024-09-01_2026-08-27.csv at them, a day's Fuel Used split by its driving time either side of a midday visit.
3. In fms_island_transactions_2025.csv (each resent row once), the T680 sleepers' own fills show their cap: the 48 over 225 gallons, back off the road, averaged 269.3 of 300 gallons, a 10.2% reserve, which the replay takes off every vehicle's tank.
4. For every yard visit from 29 June to 23 August, took the smaller of the fuel burned since the unit's previous yard visit and its capped tankful, summed by yard and scaled from those weeks' 39 working days to the window's 40: Memphis 21,303, Jackson 44,695, Nashville 69,402, Cookeville 12,898, Knoxville 37,575, Blountville 27,835 gallons.
5. Took each yard's whole 8,000-gallon loads: Memphis 2, Jackson 5, Nashville 8, Cookeville 1, Knoxville 4, Blountville 3, 23 in all.
6. Overton's price term in overton_offer_2026-08-26.pdf puts its $0.019 on the same TriState average the card programmes bill from, so each of a load's 8,000 gallons saves its account's charge over that average in card_programmes_pricing_schedules.pdf (Crossroads' network fee is part of its diesel price) less $0.019: 23 loads save $17,408, so contract 23.

## 4. Deliverable Answers

### overton_loads_sep-nov_2026.xlsx

1. Loads to contract for 14 September to 8 November, by yard: Memphis 2, Jackson 5, Nashville 8, Cookeville 1, Knoxville 4, Blountville 3.
2. Total: 23 loads.
3. Saving against the same gallons on the card accounts at their agreement terms: $17,408.
4. Diesel gallons each card account's vehicles bought, by month:
   - Delta, Riverbend direct bill: May 33,472 gallons, June 36,732 gallons, July 37,170 gallons
   - Keeble, Crossroads Fleet Card: May 46,569 gallons, June 54,781 gallons, July 52,821 gallons
   - Holston, SMPM fleet card: May 46,391 gallons, June 51,215 gallons, July 53,258 gallons
5. Overton's 2025 island programmes, net gallons delivered and the dollars billed over the posted rack value of those gallons after credits, taxes aside:
   - Jackson, March 2025: 31,911 gallons, $891
   - Jackson, April 2025: 24,004 gallons, $811
   - Jackson, May 2025: 7,986 gallons, $254
   - Knoxville, June 2025: 23,977 gallons, $446
   - Knoxville, July 2025: 24,021 gallons, $542
   - Knoxville, August 2025: 8,021 gallons, $191

### yard_island_draw.png

6. Bar chart: each yard's island draw for 14 September to 8 November beside its vehicles' card gallons for 29 June to 23 August, white ticks marking each whole 8,000-gallon load inside the draw bar and each yard's load count labelled above it.
