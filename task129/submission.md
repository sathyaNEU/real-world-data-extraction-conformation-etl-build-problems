# task129 submission

## Tags

**Domain:** General Statistics & Data Science (interpretability: splitting one rise in slow mobile page loads between two changes that only ever switched on together, from a news group's page-view beacons).
**Analytical objective:** Root-Cause Analysis (which of five changes shipped since spring the operations squad fixes in Q4).

## 1. Final Recommendation

**The operations squad should fix Bølge's front end in Q4: at August's traffic the fix brings back about 1,460,000 mobile views a month under the line.**

The closest other change, the header-bidding ad stack, would bring back about 610,000. Not the ad stack, which leads only when the two separating groups' effects are carried to the ad-supported views by phone class alone: the front end costs a view mostly on a device's first view after a release-train deploy and the ad stack mostly on its later views, and about three quarters of the ad-supported views are first views against about a quarter of the views the two effects are read on. Not the consent banner, the image pipeline or the brand fonts, whose dated steps bring back 430,000, 330,000 and 270,000.

## 2. Critical Components

1. **About three quarters** of August's ad-supported views of the six Bølge template groups are a device's first view since the latest release-train deploy, against **about a quarter** of the subscriber and puzzles views the two effects are read on
2. The three dated changes would bring back **430,000** (consent banner), **330,000** (image pipeline) and **270,000** (brand fonts) mobile views a month at August's traffic

## 3. Step-by-Step Solution

1. Built the mobile view frame from rum_mobile_views_2026.parquet under the service level and the field guide: phones by device_registry_2026-09.csv, each page view once by pv_id (its first beacon received), a beacon that repeats an earlier beacon of the same device for the same page with the same three timings within ten minutes under another pv_id dropped, every row counted by sample_weight, a scored view over the line by the service level's section 2.
2. Marked each view the device's first since the latest deploy in release_train_log_2026.csv (deployed_at read with its offset) or a later one, with its phone class from the registry's perf_band: about three quarters of August's ad-supported views of the six template groups are first views, against about a quarter of the subscriber and puzzles views in the windows of step 3.
3. Read the ad stack alone on puzzles pages viewed without an active subscription (RT-26-050 on 24 June) and the front end alone on subscribers' views of the six template groups (any subscription active in subscription_register_extract_2026-09-05.csv on the view's Copenhagen day, per section 4 of the paywall terms; the ad-free layout from 30 June in boelge_rollout_log.csv) as the change in the over-line share over the windows of the service level's section 3, within each phone class and first or later view.
4. Valued each cell's effect on all of August's scored views on the pages and layouts the change is live on today (service level section 4: the ad stack on the six template groups' ad-supported views and the puzzles pages, the front end on every view of the six template groups): the front end's fix brings back 1,460,000 mobile views a month and the ad stack's 610,000.
5. Read the consent banner (5 May), the image pipeline (7 April, on the templates its line in change_register_2026.xlsx names) and the brand fonts (3 March) as the change in each title's over-line share over the same windows, titles by their current masthead in edition_register.csv, valued on each title's August scored views the change reaches: 430,000, 330,000 and 270,000 mobile views a month.
6. Image delivery: smartphone rows of browser and app-webview clients in image_cdn_delivery_2026.csv (the app's native CFNetwork and okhttp clients make no page view), edge hits plus origin fills, the fallback vendor's bytes_served converted from kilobytes per the vendor appendix, by the month of log_date, over the month's mobile page views from step 1, scored or not.
7. Recommendation: fix Bølge's front end in Q4, about 1,460,000 mobile views a month; the header-bidding ad stack second at about 610,000.

## 4. Deliverable Answers

### q4_squad_call.pptx

1. Slide 1: "Q4 squad: fix the Bølge front end", about 1,460,000 mobile views a month back under the line at August's traffic, the header-bidding ad stack next at about 610,000.
2. Slide 2, bar chart of what each fix would bring back, mobile views a month at August's traffic:
   - Bølge front end: 1,460,000
   - Header-bidding ad stack: 610,000
   - Consent banner: 430,000
   - Image pipeline: 330,000
   - Brand web fonts: 270,000

### q4_squad_call_workings.xlsx

1. What fixing each dated change would bring back, mobile views a month at August's traffic, nearest ten thousand:
   - Consent banner: Sønderå Tidende 180,000, Lindå Avis 140,000, Kærby Dagblad 110,000
   - Image pipeline: Sønderå Tidende 130,000, Lindå Avis 110,000, Kærby Dagblad 90,000
   - Brand web fonts: Sønderå Tidende 110,000, Lindå Avis 80,000, Kærby Dagblad 80,000
2. Images the CDN served to mobile page views, per mobile page view:
   - March 2026: 11.4 requests, 530 kilobytes
   - April 2026: 12.2 requests, 710 kilobytes
   - May 2026: 12.4 requests, 750 kilobytes
   - June 2026: 12.5 requests, 770 kilobytes
   - July 2026: 12.3 requests, 760 kilobytes
   - August 2026: 12.6 requests, 790 kilobytes
