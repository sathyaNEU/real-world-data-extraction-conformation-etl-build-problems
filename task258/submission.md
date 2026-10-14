## Tags

**Domain:** Product Analytics (metric definition and measurement science: a counterfactual on Largest Contentful Paint built from RUM attribution).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Send the performance squad to Matchday for the quarter starting 5 January 2027: its hero-image playbook would move 4.6 million page loads a month into the good LCP band, 1.40 times Ledger's 3.3 million.**
Each slow page load on a property's own hero image is rebuilt with the image's load delay at 240 ms, the level the squad's eleven engagements settled at whatever it began at, its load time at 0.48 of its own, and its paint no sooner than the page's own first contentful paint, which the playbook leaves where it is. Not Pantry, which leads with the render delay held as it is (6.8 million): most of its slow loads are on pages that first paint about three seconds after their first byte, and it moves 2.9 million. Not Ledger, which the engagements' after-over-before ratios carried part by part (7.4 million) or a preload taken to end the delay (8.4 million) put first: on the image CDN its short delays rise to 240 ms and it moves 3.3 million. Not Hearth, which has the most slow loads on its own images (20.4 million) but whose paint is held by time to first byte, which the playbook leaves alone (3.2 million). Not Tideline, which has the most slow loads of all (36.6 million), most of them painting text, agency photos, ads or video posters.

## 2. Critical Components

1. The image's load delay after the playbook: **240 ms**, the median after-window delay on the engagements' pages (each engagement between 232 and 247 ms, from before-window medians of 129 to 2,991 ms)
2. The image's load time after the playbook: **0.48** of what it was (the engagements' ratio of medians)
3. The paint after the playbook comes no sooner than the load's own first contentful paint: the render delay held on nine engagements and rose at E06 and E10 from **377 and 462 ms** to **2,321 and 2,245 ms**
4. Page loads a month moved into the good band: **Matchday 4.6 million**, Ledger 3.3 million

## 3. Step-by-Step Solution

1. Kept the beacons of rum_lcp_beacons_2026-11.csv fired in November 2026 Sydney time (from 31 October 13:00 UTC to before 30 November 13:00 UTC), one per beacon_id, navigations reporting LCP, each weighted 1 / the sampling rate in force for its origin when its page load started (rum_sampling_config.csv, per rum_extract_field_notes.md).
2. Kept the loads slower than 2,500 ms whose LCP element is an image the property serves itself, from its image host, its legacy alias or its img.brolgacdn.au path in cdn_host_list.csv, the playbook's reach in the squad charter: Hearth has the most, 20.4 million a month.
3. Placed each beacon of squad_engagement_beacons_2024-2026.csv in its engagement's before or after window from squad_change_log_2024-2026.xlsx by Sydney date and compared each part's medians: the load delay settled at 240 ms after every engagement (232 to 247 ms) from before-window medians of 129 to 2,991 ms, the load time fell to 0.48 of its before median, time to first byte and first contentful paint held on every engagement, and the render delay held on nine and rose at E06 and E10 (377 to 2,321 ms and 462 to 2,245 ms), whose pages first paint about three seconds after their first byte and whose after-window paint lands on that first paint.
4. Rebuilt each slow own-image load with its time to first byte and render delay as they are, its load delay at 240 ms and its load time at 0.48 of its own, its paint taken no sooner than its own fcp_ms, and counted the loads at 2,500 ms or less, a load moved as the squad charter defines it: Matchday 4.6 million a month, Ledger 3.3, Hearth 3.2, Tideline 3.1, Pantry 2.9, Trailhead 1.8.
5. With the render delay held and no first-paint floor Pantry leads at 6.8 million; the same loads carried at the after-over-before ratios of medians on both image parts put Ledger first at 7.4 million, and with no load delay at 8.4 million; at the 240 ms level Ledger, whose delays start short, moves 3.3 million.
6. Hero-image egress: the hero slot's requests answered with the image (not the revalidations that send none, per extract_log_2026-12-03.csv) in the same Sydney month, from image_host_logs_2026-11.csv (UTC hours) on each property's image host and img.brolgacdn.au path and from legacy_media_server_log_2026-11.csv (Sydney time) on its legacy alias, times the slot's mean AVIF size in squad_avif_size_table.xlsx, at AUD 0.071 per GB of 1,000,000,000 bytes (image_cdn_contract_schedule_2026.pdf).
7. Live hero images: the assets of dam_image_export_2026-11.csv on the 2 December 2026 crawl (last_used_on), one per asset_id across its renditions, leaving out each library record a DAM record names as its legacy_id, each under the property whose page carries it (last_used_page), the sections moved in March 2025 (domains_runbook.md) being their new property's own hero images in the squad charter's sense, whatever collection they were uploaded to.
8. Sent the squad to Matchday, 1.40 times Ledger's count.

## 4. Deliverable Answers

### performance_squad_q1_2027.md

1. The call: Matchday, 4.6 million page loads a month into the good LCP band.
2. Page loads a month the playbook would move into the good band:
   - Matchday: 4.6 million
   - Ledger: 3.3 million
   - Hearth: 3.2 million
   - Tideline: 3.1 million
   - Pantry: 2.9 million
   - Trailhead: 1.8 million
3. Hero-image egress the group image CDN would serve each month:
   - Matchday: 1,208 GB, $86
   - Ledger: 1,056 GB, $75
   - Hearth: 2,102 GB, $149
   - Tideline: 1,971 GB, $140
   - Pantry: 653 GB, $46
   - Trailhead: 667 GB, $47
4. Live hero images the squad would convert to AVIF:
   - Matchday: 4,210
   - Ledger: 2,044
   - Hearth: 2,777
   - Tideline: 6,362
   - Pantry: 3,543
   - Trailhead: 2,444

### lcp_reach_q1_2027.png

1. One horizontal bar chart of the six properties' page loads a month moved into the good LCP band, largest first and labelled in millions, Matchday's bar coloured and marked "Squad, Q1 2027".
