## Tags

**Domain:** Product Analytics (metric definition and measurement science: a counterfactual on Largest Contentful Paint built from RUM attribution).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Send the performance squad to Trailhead for the quarter starting 5 January 2027: its hero-image playbook would move 4.9 million page loads a month into the good LCP band, 1.44 times Matchday's 3.4 million.**
Each slow page load on a property's own hero image is rebuilt the way the squad's engagements landed, with the image's load delay at 240 ms only where the preload can reach the hero, which needs the page's server HTML to carry it, and the paint no sooner than the page's own first contentful paint. Not Matchday, which leads with the playbook carried onto every load (6.3 million): its /live/ pages are an app whose server HTML carries no hero, so 2.9 million of its slow loads keep their delay, and it moves 3.4 million. Not Pantry, which leads with the render delay held (8.0 million): most of its slow loads first paint about three seconds after their first byte, and it moves 3.3 million. Not Ledger, which ratios of medians (8.8 million) or a preload taken to end the delay (9.7 million) put first: its short delays rise to 240 ms and it moves 3.0 million. Not Hearth, with the most slow loads on its own images (20.4 million), held by time to first byte (3.2 million). Not Tideline, with the most slow loads of all (37.4 million), most of them painting text, agency photos, ads or video posters (2.6 million).

## 2. Critical Components

1. The image's load delay where the preload reaches the hero: **240 ms**, the median after-window delay on the engagements' pages (each engagement between 232 and 247 ms, from before-window medians of 129 to 2,991 ms)
2. The image's load time after the playbook: **0.48** of what it was (the engagements' ratio of medians)
3. Slow own-image loads a month whose hero the preload cannot reach, their page's crawled server HTML carrying no such image: **Matchday 2.9 million**
4. The paint after the playbook comes no sooner than the load's own first contentful paint: the render delay held on nine engagements and rose at E06 and E10 from **377 and 462 ms** to **2,321 and 2,245 ms**
5. Page loads a month moved into the good band: **Trailhead 4.9 million**, Matchday 3.4 million

## 3. Step-by-Step Solution

1. Kept the beacons of rum_lcp_beacons_2026-11.csv fired in November 2026 Sydney time (from 31 October 13:00 UTC to before 30 November 13:00 UTC), one per beacon_id, navigations reporting LCP, each weighted 1 / the sampling rate in force for its origin when its page load started (rum_sampling_config.csv, as the squad charter counts page loads).
2. Kept the loads slower than 2,500 ms whose LCP element is an image the property serves itself, from its image host, its legacy alias or its img.brolgacdn.au path in cdn_host_list.csv, the playbook's reach in the squad charter: Hearth has the most, 20.4 million a month.
3. Placed each beacon of squad_engagement_beacons_2024-2026.csv in its engagement's before or after window from squad_change_log_2024-2026.xlsx by Sydney date and compared each part's medians: the load delay settled at 240 ms after every engagement, the load time fell to 0.48 of its before median, time to first byte and fcp_ms held on every engagement, and the render delay held on nine and rose at E06 and E10, whose after-window paint lands on the page's first paint.
4. Joined each slow own-image load to site_crawl_2026-12-02.csv by its page (origin and page_path against page_url) and its LCP image (lcp_url against img_src): the preload is written into the document head (the Playbook sheet of the change log) and the squad does no script or render-path work, so a load whose image is not among its page's crawled images keeps its own load delay; Matchday has 2.9 million of them, all on its /live/ pages, whose crawled HTML carries the site logo alone.
5. Rebuilt each slow own-image load with its time to first byte and render delay as they are, its load delay at 240 ms where reached and as it is where not, its load time at 0.48 of its own, its paint no sooner than its own fcp_ms, and counted the loads at 2,500 ms or less: Trailhead 4.9 million, Matchday 3.4 million, Pantry 3.3 million, Hearth 3.2 million, Ledger 3.0 million, Tideline 2.6 million.
6. Hero-image egress: the hero slot's requests answered with the image (a revalidation sends no bytes) in the same Sydney month, from image_host_logs_2026-11.csv (UTC hours) on each property's image host and img.brolgacdn.au path and from legacy_media_server_log_2026-11.csv (its own Sydney-time hours) on its legacy alias, times the slot's mean AVIF size in squad_avif_size_table.xlsx, at AUD 0.071 per GB of 1,000,000,000 bytes (image_cdn_contract_schedule_2026.pdf).
7. Live hero images: the assets of dam_image_export_2026-11.csv last used on 2 December 2026 (last_used_on), one per asset_id across its renditions, leaving out each library record a DAM record names as its legacy_id, each under the property whose page carries it (last_used_page), the sections moved in March 2025 (domains_runbook.md) being their new property's own hero images in the squad charter's sense, whatever collection they were uploaded to.
8. Sent the squad to Trailhead, 1.44 times Matchday's count.

## 4. Deliverable Answers

### performance_squad_q1_2027.md

1. The call: Trailhead, 4.9 million page loads a month into the good LCP band.
2. Page loads a month the playbook would move into the good band:
   - Trailhead: 4.9 million
   - Matchday: 3.4 million
   - Pantry: 3.3 million
   - Hearth: 3.2 million
   - Ledger: 3.0 million
   - Tideline: 2.6 million
3. Hero-image egress the group image CDN would serve each month:
   - Trailhead: 1,259 GB, $89
   - Matchday: 1,217 GB, $86
   - Pantry: 770 GB, $55
   - Hearth: 2,102 GB, $149
   - Ledger: 1,056 GB, $75
   - Tideline: 1,997 GB, $142
4. Live hero images the squad would convert to AVIF:
   - Trailhead: 2,444
   - Matchday: 4,478
   - Pantry: 3,742
   - Hearth: 2,777
   - Ledger: 2,168
   - Tideline: 6,741

### lcp_reach_q1_2027.png

1. One horizontal bar chart of the six properties' page loads a month moved into the good LCP band, largest first and labelled in millions, Trailhead's bar coloured and marked "Squad, Q1 2027".
