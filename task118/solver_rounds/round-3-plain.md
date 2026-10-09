# solver round: round 3, plain

**Proxy score 46.5 / 100** (recommendation 1.7 of 35, instruction 7.0 of 7, asks 37.8 of 58). Main call missed. 1 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.

solver: Place the headline squad with Local·metro (LOC-M) for 2027. It would add about 2,800,000 extra article clicks there. The runner-up is Business·national at about 1,750,000, so Local·metro leads by about 1,050,000. Each figure is the desk's 2027 plan clicks on surfaces that show the tested headline (Local·metro 108.7m of 114.7m; Business·national 86.4m of 309.1m), multiplied by the desk's average winning lift per concluded test after correcting for over-stated winners.

tokens matched 1 of 3 (1,250,000, Place, Culture)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| squad_placement_2027.docx | 1 | 1 | 2 | 50% |
| squad_placement_2027.docx | 2 | 2 | 4 | 50% |
| squad_placement_2027.docx | 3 | 2 | 3 | 67% |
| squad_placement_2027.xlsx | 1 | 29 | 49 | 59% |
| squad_placement_2027.xlsx | 2 | 2 | 2 | 100% |

## Solver's path

1. Read the prompt, the placement brief, the email thread, the field reference, the CMS field notes, the standards section 7 and the April bulletin, the syndication agreement, the plan, the change log, the panel files and the export log.
2. headline_tests_archive (14,131 package rows, 4,020 tests): computed each variant's lift as its click-through rate over the control's, minus one, with a delta-method standard error. Fitting a normal prior by maximum likelihood across all 10,111 variants gave mu -0.0104 and tau 0.0453. Each shipped winner's lift was shrunk to its posterior mean; a kept control counts as 0. The dashboard's raw average winning lift over-states winners, most of all at Sport·metro (10.8%) and Politics·metro (7.9%), whose tests are tiny.
3. Calibration against headline_squad_change_log: for each of the 7 closed app embeddings, planned clicks times the mean shrunk lift over that desk-year's tests reproduces realised incremental clicks. Ratios run 0.988 to 1.009, so all 7 are within 2%. The dashboard method misses all 7, with ratios 0.28 to 0.76.
4. Pageviews parquet (desk totals equal plan_2027_clicks exactly): reachable surfaces are home_web, section_web, feed_app, section_app and related_links. partner_apps, search, discover, social, newsletter and alerts are excluded because they carry the canonical headline. Reachable share is LOC-M 0.947, BUS-N 0.279, CUL-N 0.502, SPT-N 0.288, POL-N 0.190, SPT-M 0.552 and POL-M 0.599.
5. Extra clicks = reachable 2027 clicks x the desk's mean shrunk lift over its web tests from Oct 2025 to Sep 2026. Results: LOC-M 108.69m x 2.570% = 2,792,947; BUS-N 86.35m x 1.999% = 1,726,554; CUL-N 1,369,906; SPT-N 1,297,878; POL-N 913,383; SPT-M 227,556; POL-M 72,833. Local·metro first, Business·national second, gap 1,066,393.
6. Panel: for each period kept only the latest release (R26-04H replaces Nov 2025 to Feb 2026; R26-07B replaces Apr to Jun 2026). Section codes were mapped with the old taxonomy for Oct 2025 (R25-11) and the 2026 taxonomy otherwise, then unique_audience was averaged over 12 months per desk.
7. CMS revisions: dropped 787 restored-copy documents (restored_from_doc) and 1,704 migrated documents. A headline correction is a live revision where a new correction note appears and the headline differs from the last live headline. Also counted 16 live-blog-entry corrections, where an entry's headline changes in the same minute as a new note on its parent live blog. This reconciles exactly to the bulletin's March figures of 11 headline and 22 text corrections.
8. Articles are stories plus live blogs that went live from 1 Oct 2025 to 30 Sep 2026 AEST, excluding withdrawn never-live scheduled documents. These equal the pageview distinct-article counts exactly. Going-live time is the scheduled publish_at when the CMS published before any live save. Timing is the median, per article, of minutes to the first headline correction; for entry corrections it runs from the entry going live.

confidence: High for the main call (Local·metro, about 2.8m clicks, with Business·national second at about 1.75m) and for the 7 of 7 calibration. Medium for the extra-click values to the nearest 50,000, which depend on the fitted prior and the reachable-surface set. Medium for the median minutes, which depend on how live-blog entry corrections are timed.

notes: Live-blog entry corrections are timed from the entry going live; timing them from the live blog would give BUS-N 89, CUL-N 119, LOC-M 87, POL-M 78, POL-N 86, SPT-M 55, SPT-N 47. Politics·metro is reported for completeness but is not on the shortlist. Discover is treated as using the canonical headline.

### squad_placement_2027.docx (solver's answers)
- Recommended desk: Local·metro (LOC-M)
- Extra article clicks at chosen desk in 2027: 2,800,000 extra clicks (nearest 50,000; unrounded 2,792,947)
- Runner-up desk and its extra clicks: Business·national (BUS-N), 1,750,000 extra clicks (nearest 50,000; unrounded 1,726,554)
- Gap between chosen desk and runner-up: 1,050,000 clicks (nearest 50,000; unrounded 1,066,393)
- Chart: each desk's 2027 clicks to extra clicks, ordered by extra clicks: 2027 clicks to extra clicks, nearest 50,000: Local·metro 114,750,000 to 2,800,000; Business·national 309,050,000 to 1,750,000; Culture·national 153,350,000 to 1,350,000; Sport·national 341,000,000 to 1,300,000; Politics·national 376,250,000 to 900,000; Sport·metro 104,650,000 to 250,000; Politics·metro (not on the shortlist) 61,250,000 to 50,000. Local·metro is marked as chosen and Business·national as runner-up, with the 1,050,000 gap labelled. Suggested title: 'Local·metro: the squad adds about 2.8m clicks in 2027'.

### squad_placement_2027.xlsx (solver's answers)
- Extra clicks 2027 per desk (nearest 50,000): LOC-M 2,800,000; BUS-N 1,750,000; CUL-N 1,350,000; SPT-N 1,300,000; POL-N 900,000; SPT-M 250,000; POL-M 50,000
- Average monthly readers, 12 months to Sep 2026 (nearest thousand): POL-N 3,180,000; SPT-N 2,931,000; BUS-N 1,760,000; CUL-N 1,412,000; LOC-M 617,000; SPT-M 470,000; POL-M 331,000
- Extra clicks per reader (1 dp): LOC-M 4.5; BUS-N 1.0; CUL-N 1.0; SPT-M 0.5; SPT-N 0.4; POL-N 0.3; POL-M 0.2
- Headline corrections, 12 months to Sep 2026 (count): POL-N 47; SPT-N 42; BUS-N 39; LOC-M 33; SPT-M 18; CUL-N 14; POL-M 14
- Articles live in the window (denominator): SPT-N 11,043; POL-N 9,007; BUS-N 7,937; LOC-M 6,941; CUL-N 3,883; POL-M 3,186; SPT-M 2,463
- Headline corrections per 1,000 articles (1 dp): SPT-M 7.3; POL-N 5.2; BUS-N 4.9; LOC-M 4.8; POL-M 4.4; SPT-N 3.8; CUL-N 3.6
- Median minutes from going live to first headline correction (whole minutes): BUS-N 79; CUL-N 79; LOC-M 71; POL-N 69; POL-M 66; SPT-M 55; SPT-N 42
- Finished embeddings reproduced within 2 per cent: 7 of 7 (predicted/realised ratios 0.988 to 1.009)
