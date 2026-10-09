# solver round: round 6, plain

**Proxy score 36.1 / 100** (recommendation 1.7 of 35, instruction 7.0 of 7, asks 27.4 of 58). Main call missed. 1 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.

solver: Put the headline squad on Local·metro (LOC-M) for 2027. It would add about 2,800,000 extra article clicks there. The runner-up is Business·national at 1,750,000, which leaves a gap of 1,050,000 clicks. The other desks are Culture·national 1,350,000, Sport·national 1,300,000, Politics·national 900,000 and Sport·metro 250,000. Neither the dashboard's Politics lift (4.69%) nor Kayla's "where the readers are" test (Politics·national, 3,180,000 monthly readers) picks this desk.

tokens matched 1 of 3 (1,250,000, Place, Culture)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| squad_placement_2027.docx | 1 | 0 | 2 | 0% |
| squad_placement_2027.docx | 2 | 2 | 4 | 50% |
| squad_placement_2027.docx | 3 | 1 | 3 | 33% |
| squad_placement_2027.xlsx | 1 | 26 | 49 | 53% |
| squad_placement_2027.xlsx | 2 | 2 | 2 | 100% |

## Solver's path

1. Read the prompt, placement brief, mail thread, field reference, plan 2027, squad change log and dashboard export. Recomputed the dashboard average winning lift (zero when the control is kept) from headline_tests_archive. It matches exactly, e.g. Politics 4.69% = POL-N 205 + POL-M 210 tests.
2. Archive: one row per package. Joined each variant to its test's control. Lift = CTR_variant/CTR_control - 1, with delta-method variance (r^2*((1-p1)/(n1 p1)+(1-p0)/(n0 p0))). Metro desks run tiny tests (about 2,000 impressions), which inflates their raw winning lifts (SPT-M 10.8%, POL-M 7.9%).
3. Fitted a normal-normal empirical-Bayes prior by maximum likelihood over all 10,111 non-control packages: mean -1.038%, tau^2 0.0020547. Shrank each shipped variant's lift to its posterior mean; a kept control counts 0. Desk lift = mean over all of that desk's tests.
4. Calibrated on headline_squad_change_log: planned_clicks_m x mean shrunk lift for that desk-year's app tests. App desks only have the feed_app, section_app and related_links surfaces, all of which show the live headline. All 7 of 7 land within 2% of realised_incremental_clicks (max deviation 1.2%). Raw lift and significance filters miss badly.
5. From the field reference, the canonical (publication) headline is what RSS/partner feeds, search, social, newsletters and alerts carry, so the tested headline only moves clicks on home_web, section_web, feed_app, section_app and related_links. Summed those from the pageviews parquet per desk; desk totals equal the plan exactly. Extra = own-surface clicks x shrunk desk lift. Results: LOC-M 2,792,947; BUS-N 1,726,554; CUL-N 1,369,906; SPT-N 1,297,878; POL-N 913,383; SPT-M 227,556. Rounded to 50k, the gap is 1,050,000.
6. Panel readers: mapped section codes by the release's taxonomy (old codes for R25-11 to R26-03, 2026 codes for R26-04, R26-04H onward). R26-04H replaces Nov-Feb for Politics and Culture national. R26-07B is used for Apr-Jun; the stale Apr-Jun rows repeated in R26-08 were ignored because the release log scopes R26-08 to Jul only. Took the mean of 12 monthly unique_audience values per desk.
7. CMS revisions: a new correction note is note text that is new or prepended (re-adds after a clear are ignored); it is timed at the first live revision that carries it. Dropped Brisbane-restore recreations (787 docs, originals present), migrated docs (notes carried from the old CMS) and never-live docs. Go-live = earlier of the scheduled publish_at and the first live save. Articles = stories + live blogs live 1 Oct 2025 to 30 Sep 2026 AEST; this matches the pageview article counts exactly.
8. A headline correction is a new note whose publishing revision changes the headline, or whose headline change sits in an adjacent live revision within 15 minutes. For live blogs, a post headline change 0-9 minutes before the blog note also counts (section 7.5). The seven-desk March 2026 total is 11 headline and 22 other corrections, matching the bulletin; a keyword rule gives only 6. Corrections are timed at the revision that publishes the corrected headline. Minutes are measured from the corrected document's go-live (the post's own go-live for live-blog entries), using the first correction per article and taking the median by desk.

confidence: High on the main call: Local·metro at 2,800,000, Business·national the runner-up 1,050,000 behind, and 7 of 7 embeddings within 2%. Readers and correction counts are medium-high. The median minutes are medium, because the go-live anchor for live-blog entries is a judgement call.

notes: If minutes for live-blog entries are timed from the live blog's own go-live instead of the post's, the medians become BUS-N 89, CUL-N 119, LOC-M 87, POL-N 86, SPT-M 55, SPT-N 47. Three live-blog notes that coincide with a change to the blog's own headline are counted as headline corrections, consistent with the story rule. The September 2026 panel month looks low for some sections but is not flagged anywhere in the folder, so it is kept.

### squad_placement_2027.docx (solver's answers)
- Recommended desk and extra 2027 clicks: Local·metro (LOC-M): 2,800,000 extra article clicks in 2027 (nearest 50,000; unrounded 2,792,947)
- Runner-up and gap: Runner-up is Business·national (BUS-N) at 1,750,000 extra clicks (unrounded 1,726,554). It sits 1,050,000 clicks behind Local·metro (nearest 50,000).
- Chart: 2027 clicks to extra clicks per desk, in order of extra clicks: Each desk's 2027 clicks (2027 plan = 12 months to Sep 2026) and extra clicks, nearest 50,000. 1) LOC-M 114,750,000, extra 2,800,000 (chosen). 2) BUS-N 309,050,000, extra 1,750,000 (runner-up; gap 1,050,000 labelled). 3) CUL-N 153,350,000, extra 1,350,000. 4) SPT-N 341,000,000, extra 1,300,000. 5) POL-N 376,250,000, extra 900,000. 6) SPT-M 104,650,000, extra 250,000. Clicks on surfaces that show the live headline (home_web, section_web, feed_app, section_app, related_links): LOC-M 108,700,000, BUS-N 86,350,000, CUL-N 76,900,000, SPT-N 98,200,000, POL-N 71,400,000, SPT-M 57,800,000. Shrunk lift 

### squad_placement_2027.xlsx (solver's answers)
- Extra clicks 2027 per desk (nearest 50,000): LOC-M 2,800,000; BUS-N 1,750,000; CUL-N 1,350,000; SPT-N 1,300,000; POL-N 900,000; SPT-M 250,000
- Average monthly readers, 12 months to Sep 2026 (nearest thousand): POL-N 3,180,000; SPT-N 2,931,000; BUS-N 1,760,000; CUL-N 1,412,000; LOC-M 617,000; SPT-M 470,000 (POL-M, not shortlisted: 331,000)
- Extra clicks per reader (1 dp): LOC-M 4.5; BUS-N 1.0; CUL-N 1.0; SPT-M 0.5; SPT-N 0.4; POL-N 0.3
- Headline corrections (count): POL-N 47; SPT-N 42; BUS-N 39; LOC-M 33; SPT-M 18; CUL-N 14 (POL-M 14). Seven-desk March 2026 total is 11, which matches the April standards bulletin.
- Headline corrections per 1,000 articles (1 dp): SPT-M 7.3 (18/2,463); POL-N 5.2 (47/9,007); BUS-N 4.9 (39/7,937); LOC-M 4.8 (33/6,941); SPT-N 3.8 (42/11,043); CUL-N 3.6 (14/3,883). Articles are stories plus live blogs that went live in the window; these counts equal the pageview article counts.
- Median minutes from going live to first headline correction (whole minutes): BUS-N 79; CUL-N 79; LOC-M 71; POL-N 69; SPT-M 55; SPT-N 42 (POL-M 66)
- Embeddings reproduced within 2%: 7 of 7 finished embeddings are within 2% (largest gap is +1.2%). Predicted vs realised: Games 2019 678,285 vs 670,475; Wellness 2020 328,528 vs 325,071; Puzzles 2021 1,066,718 vs 1,064,693; Recipes 2022 1,065,594 vs 1,059,784; Games 2023 271,715 vs 272,464; Recipes 2024 528,309 vs 532,067; Wellness 2025 665,181 vs 670,864.
