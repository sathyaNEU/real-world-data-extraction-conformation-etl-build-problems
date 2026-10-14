# task456 submission

## Tags

**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution (three hospital capacity feeds that each record full adult ICU days with error and none of which is a reference, integrated into one hospital-day dataset, each region's share of full days estimated from how the feeds agree).
**Analytical objective:** Data Extraction & Conformation (ETL) (the census survey's two forms and its resubmissions, the bed-status board's event log in UTC across a renumbering of its facility codes, and the transfer center's two call systems across their cut-over conformed to one row per compact hospital and local day).

## 1. Final Recommendation

**The Ridgeline ICU Surge Compact should activate in four regions at its 20 January 2026 review: Northeast, Upper Cumberland, South Central and West.**

Their estimated shares of full adult ICU hospital-days in the 28 days to 18 January are 50, 50, 70 and 80 per cent against the compact's one in three, while East, Southeast, Mid-State and Memphis Delta stand at 20, 10, 10 and 10 per cent. Not all eight regions, which counting a day full whenever any feed shows it gives: the board shows an adult ICU Closed on about a third of ordinary days, when a hospital keeps its last beds for its own patients. Not none, which requiring two feeds to agree gives: the census and the transfer center each miss most full days, so most full days carry the board's flag alone.

## 2. Critical Components

1. The three feeds conform to **2,100 hospital-days**, the 75 compact hospitals each on its own local dates over the 28 days.
2. The census shows **216** of them full at 07:00 and has no report on **82**, the board shows the adult ICU Closed on **1,085**, and the transfer center logged a no-bed decline on **176**.
3. No feed is a record of full days, and their agreement fixes each one's errors: the board shows Closed on about nine in ten full days and about a third of ordinary ones, while the census and the transfer center rarely flag an ordinary day and each miss most full days.
4. Each region's share of full hospital-days is the prevalence of a two-class latent class model of the three feeds, the feeds' rates common to every region and the share free in each, to the nearest ten per cent: Northeast **50%**, East **20%**, Southeast **10%**, Upper Cumberland **50%**, Mid-State **10%**, South Central **70%**, West **80%**, Memphis Delta **10%**.

## 3. Step-by-Step Solution

1. Took each hospital's latest submission for each date in capacity_survey_2025-12-01_2026-01-19.csv (the annex: a later submission replaces the earlier) and flagged the day when adult ICU patients reached staffed adult ICU beds at 07:00: 216 of the 2,100 hospital-days of the 75 hospitals in facility_crosswalk.csv, with no report on 82.
2. Replayed each hospital's adult ICU line (the six unit labels in data_dictionary.xlsx) from bed_status_events_2025-11-01_2026-01-20.jsonl, each status standing until the next event, and flagged the day when the line showed Closed at any time of the hospital's own date in its time zone: 1,085 hospital-days.
3. Flagged the day when a call on an adult ICU request in transfer_center_calls_2025-11-01_2026-01-04.xlsx or transfer_center_calls_2026-01-05_2026-01-19.csv was declined with code CAP (transfer_center_reason_codes.csv) on the called hospital's own date: 176 hospital-days.
4. Fitted a two-class latent class model to the three flags of the 2,100 hospital-days by maximum likelihood, the feeds independent given the day's state, each feed's rates the same in every region (the annex: every hospital reports through the same systems under the same instructions, in every region), the share free in each region of compact_regions_counties.csv (article 1: strain is regional) and a day without a census report entering through its other two feeds: Northeast 52.8, East 17.9, Southeast 10.3, Upper Cumberland 52.1, Mid-State 12.4, South Central 67.9, West 78.9 and Memphis Delta 11.2 per cent.
5. Grouped both call exports by case, a case the new system took in at its 5 January start counting once through its legacy_case, kept adult ICU requests opened on the sending facility's own date in the 28 days (its county and time zone from transfer_center_name_aliases.csv) whose acceptance was not later cancelled, and counted those accepted by a hospital in another region by the sending facility's region: 387 placements.
6. Summed, on each hospital's own dates from 22 December to 18 January, the hours its emergency department line showed Divert or, from 5 January, Advisory with the reason EMS diversion: 698 hours.
7. Summed, on each hospital's own dates from 24 November to 21 December, the hours its adult ICU line showed Closed, reading events logged before the board's system migration of 8 December through board_code_previous: 4,723 hours.
8. Recommendation: activate the compact in the four regions at one in three or more (article 4), Northeast, Upper Cumberland, South Central and West, for 26 January to 22 February 2026.

## 4. Deliverable Answers

### surge_activation_notice_2026-01-26.pdf

1. Regions the compact activates at its 20 January 2026 review, for 26 January to 22 February 2026: Northeast, Upper Cumberland, South Central and West.
2. Each region's share of full adult ICU hospital-days in the window of 22 December 2025 to 18 January 2026, to the nearest ten per cent:
   - Northeast: 50%, activated
   - East: 20%, not activated
   - Southeast: 10%, not activated
   - Upper Cumberland: 50%, activated
   - Mid-State: 10%, not activated
   - South Central: 70%, activated
   - West: 80%, activated
   - Memphis Delta: 10%, not activated
3. Horizontal bar chart on page 1: each region's estimated share of full hospital-days against a dashed line at one in three, the activated regions in red, each bar labelled with its share to the nearest ten per cent.
4. Times the transfer center placed an adult ICU patient in a hospital outside the patient's own region, 22 December to 18 January, by the region the patient left:
   - Northeast: 70
   - East: 40
   - Southeast: 32
   - Upper Cumberland: 45
   - Mid-State: 49
   - South Central: 65
   - West: 58
   - Memphis Delta: 28
   - All regions: 387
5. Hours the region's emergency departments asked ambulances to divert, 22 December to 18 January, added over the region's hospitals, to the nearest whole hour:
   - Northeast: 80
   - East: 133
   - Southeast: 132
   - Upper Cumberland: 27
   - Mid-State: 147
   - South Central: 46
   - West: 64
   - Memphis Delta: 69
   - All regions: 698
6. Hours the region's adult ICUs were shown Closed on the bed-status board, 24 November to 21 December 2025, added over the region's hospitals, to the nearest whole hour:
   - Northeast: 752
   - East: 642
   - Southeast: 475
   - Upper Cumberland: 357
   - Mid-State: 745
   - South Central: 513
   - West: 616
   - Memphis Delta: 623
   - All regions: 4,723

### hospital_days_conformed_2025-12-22_2026-01-18.csv

1. The 2,100 hospital-days, one row per compact hospital and local date from 22 December 2025 to 18 January 2026, each with its region, the census's staffed adult ICU beds and patients at 07:00 and whether they show the unit full (blank on the 82 days with no report), whether the board showed the adult ICU Closed that day, and whether the transfer center logged a no-bed decline of an adult ICU request to the hospital that day.
