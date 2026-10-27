## Tags

**Domain:** Energy systems and utilities (generation capacity planning).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Award the 2027 capacity contract to the 300 MW Red Willow firm import: under RA-3 it removes 7,100 MWh of the 2027 fleet's 9,500 MWh a year of expected unserved energy, a net value of USD 106 million after its USD 35.8 million capacity payment.**
Not Ketchum Ridge, the cheapest capacity at USD 23.2 million: every hour with a shortfall fell while the ten peakers on Northgate's interruptible service were out together on lack of fuel, so a peaker on that service would have been out too and removes 0 MWh (USD -23 million). Not Sandhill Draw (USD 12 million) or Coulee Flats (USD -17 million), whose output is low in those winter hours.

## 2. Critical Components

1. The 2027 fleet's expected unserved energy over the ten weather years is **9,500 MWh** a year.
2. **100** per cent of it falls in hours when all ten Northgate IT peakers were out on lack of fuel (cause 9130), so Ketchum Ridge, on the same service, removes **0 MWh**.
3. The Red Willow import removes **7,100 MWh**, a net value of **USD 106 million**.

## 3. Step-by-Step Solution

1. Put weather_years_2027_hourly.csv on UTC (hour ending in local prevailing time; the starred hour on the autumn change day is the standard-time 01:00) and read 2019's load column, delivered in kW, in MW.
2. Replayed the 2027 fleet in fleet_list_2027.xlsx (Sandoval 1 retires) through the forced outages and derates of outage_event_log_2016_2025.csv at each event's latest revision, a part hour for its part and the least capability governing overlaps (RA-3 sections 4 and 6), with the 200 MW import in every hour the tie is in service (red_willow_tie_outages_2016_2025.csv, CST and CDT stamps): load less wind, solar, units and imports, where positive, averaged over the ten years, is 9,500 MWh.
3. Every one of those shortfall hours fell inside a lack-of-fuel event (cause 9130) that took all ten Elk Prairie, Torrance and Wexford peakers out together; the fleet list puts them on Northgate IT, the service the Ketchum Ridge offer takes its gas on.
4. Counted each offer alone in every replayed hour (RA-3 section 7): Ketchum Ridge at 300 MW times the share of the Northgate IT peakers' capability available in that hour, 0 MWh removed; the Red Willow import at 300 MW whenever the tie is in service, 7,100 MWh; Sandhill Draw and Coulee Flats at their modelled output in offer_profiles_2016_2025.parquet (hours beginning UTC), 2,000 and 400 MWh.
5. Valued each reduction at USD 20,000 per MWh less the 2027 payment the offers sheet quotes (USD 23.2, 35.8, 28.4 and 25.8 million): net USD -23 million, USD 106 million, USD 12 million and USD -17 million; the Red Willow import is the award.
6. Member energy: took the highest version of each interval in mdm_interval_export_2025.parquet, delivered less received, each point's member from the assignment history of delivery_point_register_2025.xlsx; where meter_service_orders_2025.csv records a current transformer replacement, the export kept applying the old multiplier for weeks after it, so each interval from the replacement on is carried at the new multiplier; summed by member in MWh.
7. 12-CP: the same intervals, with the meters the service orders found on standard time moved an hour later from the spring change (2025-03-09 03:00 CDT) up to the first interval after the visit that reset them, and the MDM's estimate for the stamp the reset skipped dropped; each month's peak is the hour with the highest net energy over all points, and a member's 12-CP average is its net energy in those twelve hours averaged.

## 4. Deliverable Answers

### capacity_award_2027.xlsx

1. The 2027 fleet's expected unserved energy: 9,500 MWh a year
2. Each offer's EUE removed, 2027 capacity payment and net value:
   - Ketchum Ridge: 0 MWh removed; payment USD 23.2 million; net value USD -23 million
   - Red Willow import: 7,100 MWh removed; payment USD 35.8 million; net value USD 106 million
   - Sandhill Draw: 2,000 MWh removed; payment USD 28.4 million; net value USD 12 million
   - Coulee Flats: 400 MWh removed; payment USD 25.8 million; net value USD -17 million
3. Award: Red Willow import
4. Each member's 2025 net energy delivered, MWh:
   - Bluestem Valley Electric: 1,881,448
   - Copper Ridge REA: 996,183
   - Lone Elm Cooperative: 1,452,327
   - Marais Electric: 1,309,755
   - Old Mill Power Association: 856,281
   - Sweetgrass Rural Electric: 1,770,626
   - Tamarack Electric Cooperative: 1,433,628
   - Wapsi Prairie Electric: 1,320,285
5. Each member's 2025 12-CP average, MW:
   - Bluestem Valley Electric: 317.2
   - Copper Ridge REA: 167.2
   - Lone Elm Cooperative: 245.6
   - Marais Electric: 224.8
   - Old Mill Power Association: 148.2
   - Sweetgrass Rural Electric: 293.3
   - Tamarack Electric Cooperative: 240.0
   - Wapsi Prairie Electric: 227.5

### capacity_award_2027.docx

1. The committee paper recommends the Red Willow import, with a bar chart of the four offers' net values (the Red Willow import highlighted) and the member allocation table.
