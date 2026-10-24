## Tags

**Domain:** Urban and regional science (accessibility, agglomeration and location analysis).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Marrable Foodstores should open S3, Wrentoft, Mill Lane, which will add GBP 0.8 million a year to the chain's contribution once it is trading.**
The guests on Wrentoft Lakes Holiday Park's 1,750 pitches live outside the region, so no census output area holds them, and at GBP 2,440 of in-store grocery spend a pitch for a season they lift the store's sales to GBP 7.1 million. Not S1 Bellingtoft, which leads on the residents' spend alone and adds GBP 0.5 million. Not S2 Eastgate, which adds GBP 0.1 million because over a third of its sales would come from our own stores.

## 2. Critical Components

1. The holiday parks are origins of grocery spend that the census does not count: Wrentoft Lakes Holiday Park, the largest with **1,750** pitches, is nearer S3 than any other site.
2. A pitch's guests spend **GBP 2,440** a season in store, measured from the out-of-region card spend at our ten stores.
3. With the guests carried, S3 sells **GBP 7.1 million** a year and adds **GBP 0.8 million**; on the residents alone it adds **GBP 0.1 million**, second of six, and S1 leads at **GBP 0.5 million**.

## 3. Step-by-Step Solution

1. Shared each output area's grocery spend (its households in census2021_ts041_households_oa.csv, times the weekly spend in grocery_spend_estimates_2026_oa21.csv, times 52 weeks and 88 per cent in store) among the 24 grocery stores of 280 m2 or more in voa_list_entries_2026_lq.txt and voa_summary_valuations_2026_lq.csv, by floor area over exp(-0.22 x 1.25 x straight-line km) from the output area's centroid in oa21_population_weighted_centroids.csv (spend_share_model_2025.pdf): on residents alone S1 adds GBP 0.5 million and S3 GBP 0.1 million.
2. Took each of our stores' guest spend from card_spend_by_home_sector_fy2025_26.csv: cardholders whose home sector is outside the LQ postcode area, March to October, above the store's own November to February monthly level, divided by the store's card share in store_estate_2026.xlsx.
3. Divided our ten stores' guest spend by the pitches of the 6 pitch-measured sites in voa_summary_valuations_2026_lq.csv, each weighted by the model's share of its spend going to our stores from its postcode in onspd_may2026_lq.csv: GBP 2,440 a pitch for a season.
4. Added each park as an origin, its pitches times GBP 2,440 at its postcode, and appraised each site by the model sheet's rule (26 per cent of its sales, less 26 per cent of what it takes from our stores, less the running costs in site_shortlist_2027.xlsx): S3 sells GBP 7.1 million and adds GBP 0.8 million, S1 adds GBP 0.5 million.
5. Cases: summed the cases of the DEL stops in tms_stop_export_20251006_20260329.csv by store for UK arrival dates from 6 October 2025 to 29 March 2026 and divided by 25, counting a load a store turned away once: a stop closed in under 4 minutes plus 0.02 of a minute a case had its cases taken back and delivered to the store the next day on a trip of their own, so it is left out.
6. Paid hours: paired each colleague's clock-ins and clock-outs in ta_punches_20251006_20260329.csv into shifts (a clock-in or clock-out with no partner is a shift whose other punch was forgotten), dated each shift by its clock-in (by its clock-out where there is none) and placed it at the store, in ta_terminals.csv, of that punch's terminal, not the location column; took one of the colleague's lines in wfm_paid_hours_20251006_20260329.csv for each shift starting that date, since the report lists a night shift against both dates it covers at its full paid hours, summed paid_hours by store and divided by 25.
7. Buses: from gtfs_sallowmere_motor_services_20261002.zip and gtfs_wrentoft_district_coaches_20261002.zip, the departures with pickup allowed from stops within 400 m of the site's postcode by the clock on Friday 15 January 2027, which are that day's services up to 24:00 and the previous day's services from 24:00 on (a GTFS service day runs past midnight), each bus once by its block_id: the same block at the same stop and time is one departure (a jointly run route's journey listed in both feeds, and a weekday journey the Friday-late timetable lists again), while a second bus on the same timetable on a block of its own (a school-day duplicate) is another.
8. Recommended S3, Wrentoft, Mill Lane: it adds GBP 0.8 million a year against S1's GBP 0.5 million.

## 4. Deliverable Answers

### marrable_site_appraisal_2027.xlsx

1. The site to open: S3, Wrentoft, Mill Lane.
2. Its addition to the chain's annual contribution: GBP 0.8 million.
3. Cases a week the distribution centre delivered to each store, 6 October 2025 to 29 March 2026:
   - Store 101: 7,456 cases
   - Store 102: 7,085 cases
   - Store 103: 6,968 cases
   - Store 104: 7,290 cases
   - Store 105: 5,954 cases
   - Store 106: 6,734 cases
   - Store 107: 5,710 cases
   - Store 108: 4,658 cases
   - Store 109: 3,890 cases
   - Store 110: 4,429 cases
4. Paid hours a week worked at each store, 6 October 2025 to 29 March 2026:
   - Store 101: 1,903 hours
   - Store 102: 1,533 hours
   - Store 103: 1,476 hours
   - Store 104: 1,368 hours
   - Store 105: 1,207 hours
   - Store 106: 1,318 hours
   - Store 107: 1,241 hours
   - Store 108: 1,073 hours
   - Store 109: 812 hours
   - Store 110: 783 hours
5. Bus departures that pick up passengers from stops within 400 metres on Friday 15 January 2027:
   - S1 Bellingtoft, Fenton Road: 44
   - S2 Darrowfield, Eastgate: 110
   - S3 Wrentoft, Mill Lane: 44
   - S4 Brackenmere, Northfield: 64
   - S5 Quellby, Sutton Road: 72
   - S6 Sallowmere, Westway: 84

### new_store_case_2027.docx

1. The case for opening S3, Wrentoft, Mill Lane, which adds GBP 0.8 million a year.
