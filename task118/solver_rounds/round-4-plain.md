# solver round: round 4, plain

**Proxy score 34.4 / 100** (recommendation 1.7 of 35, instruction 7.0 of 7, asks 25.8 of 58). Main call missed. 1 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.

solver: Place the headline squad with Local·metro (LOC-M) for 2027. It should add about 2,800,000 extra article clicks there. The runner-up is Business·national at 1,750,000, so Local·metro leads by about 1,050,000. Local·metro has 114.7M planned clicks, 94.7% of them on surfaces that show the tested headline, and a shrunk average true lift of 2.57% per test.

tokens matched 1 of 3 (1,250,000, Place, Culture)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| squad_placement_2027.docx | 1 | 0 | 2 | 0% |
| squad_placement_2027.docx | 2 | 2 | 4 | 50% |
| squad_placement_2027.docx | 3 | 1 | 3 | 33% |
| squad_placement_2027.xlsx | 1 | 19 | 49 | 39% |
| squad_placement_2027.xlsx | 2 | 2 | 2 | 100% |

## Solver's path

1. headline_tests_archive_2019-2026.csv: for each test, computed each package's lift over control (CTR / control CTR - 1) and its sampling variance (delta method). Averaging the shipped packages' lifts, with zero where the control was kept, reproduces the change log's and the dashboard's average winning lift (for example Games 2019 3.0%, Politics vertical 4.69%). That average carries winner's-curse bias, worst on POL-M and SPT-M, where tests average about 2,200 impressions.
2. Fitted a normal prior to every non-control package by maximum likelihood with heteroscedastic noise: mu -1.04%, tau 4.53%. Shrank each shipped variant's lift toward that prior (empirical Bayes) and set kept-control tests to 0.
3. Calibration against headline_squad_change_log.xlsx: planned_clicks × mean shrunk lift of that embedding's tests, with all app surfaces affected, lands within 2% of realised_incremental_clicks for all 7 closed embeddings (largest error +1.16%). The raw dashboard lift overstates realised clicks by 1.3 to 3.8 times.
4. pageviews parquet: the surfaces that show the live, tested headline are home_web, section_web, feed_app, section_app and related_links. Search, discover, social, partner_apps, newsletter and alerts carry the canonical headline, per the field reference. Affected share: LOC-M 94.7%, SPT-M 55.2%, CUL-N 50.2%, SPT-N 28.8%, BUS-N 27.9%, POL-N 19.0%.
5. Extra clicks = plan_2027_clicks (audience_plan_2027.xlsx, held at the twelve months to Sep 2026) × affected share × the desk's mean shrunk lift over its 12 months of web tests. LOC-M 2,792,947; BUS-N 1,726,554; CUL-N 1,369,906; SPT-N 1,297,878; POL-N 913,383; SPT-M 227,556.
6. Panel readers: mapped section codes to desks by release taxonomy, since R26-04 onwards (including history release R26-04H) uses the 2026 codes, then kept the latest release per period and desk, so R26-04H covers Nov–Feb for Politics and Culture and R26-07B covers Apr–Jun for Brisbane. Averaged unique_audience over the 12 periods; per-reader figure = extra / readers.
7. CMS revisions: excluded 1,704 migrated documents (their notes were carried over from the old CMS) and 534 documents that never went live. Merged the 787 documents restored on 14 Nov back into their originals. Going-live time = earliest live save or scheduled publish_at. Articles = stories plus live blogs that first went live from 1 Oct 2025 to 30 Sep 2026 AEST.
8. Headline correction = a newly added correction note where the headline changed on the same revision, or where the note's wording names the headline, heading or title. Wording-only notes lag the headline change by 1 to 12 minutes, so the correction is timed at the live revision that published the new headline. Live-blog entry headline errors are timed at the entry's revision and measured from the entry going live. Check: March 2026 gives 11 headline corrections and 22 text corrections, matching standards bulletin issue 31. Counted per desk; median taken over each article's first correction.

confidence: The main call and the extra-click figures are fairly firm: the calibration holds 7 of 7 and Local·metro leads Business·national by more than 60%. The correction rates and medians are less firm because they depend on judgement calls in the rules.

notes: Three medians came out at a half minute (LOC-M 71.5, POL-N 75.5, SPT-N 41.5) and are rounded up. If live-blog entry corrections are measured from the live blog going live rather than from the entry, the medians move: LOC-M 87, BUS-N 89, SPT-M 63 (62.5), SPT-N 43 (42.5). Lisa Jennings's dashboard view ranks Politics first on average winning lift (4.69%), and the panel puts the most readers on Politics·national; this method rejects both.

### squad_placement_2027.docx (solver's answers)
- recommended desk: Local·metro (LOC-M)
- extra clicks at chosen desk in 2027: 2,800,000 extra article clicks (nearest 50,000)
- runner-up desk and its extra clicks: Business·national (BUS-N), 1,750,000 extra clicks
- gap between chosen desk and runner-up: 1,050,000 clicks (unrounded 1,066,393)
- chart: 2027 clicks to extra clicks per desk, ordered by extra clicks: LOC-M 114,750,000 to 2,800,000; BUS-N 309,050,000 to 1,750,000; CUL-N 153,350,000 to 1,350,000; SPT-N 341,000,000 to 1,300,000; POL-N 376,250,000 to 900,000; SPT-M 104,650,000 to 250,000 (all to nearest 50,000). Title names Local·metro; LOC-M marked chosen, BUS-N marked runner-up, gap labelled 1,050,000

### squad_placement_2027.xlsx (solver's answers)
- extra clicks 2027 per desk (nearest 50,000): LOC-M 2,800,000; BUS-N 1,750,000; CUL-N 1,350,000; SPT-N 1,300,000; POL-N 900,000; SPT-M 250,000
- average monthly readers, Oct 2025 to Sep 2026 (nearest thousand): LOC-M 617,000; BUS-N 1,760,000; CUL-N 1,412,000; SPT-N 2,931,000; POL-N 3,180,000; SPT-M 470,000
- extra clicks per reader (1 dp): LOC-M 4.5; BUS-N 1.0; CUL-N 1.0; SPT-N 0.4; POL-N 0.3; SPT-M 0.5
- headline corrections, 12 months to Sep 2026 (whole number): LOC-M 28; BUS-N 35; CUL-N 12; SPT-N 34; POL-N 39; SPT-M 17 (POL-M, not shortlisted: 13)
- headline corrections per 1,000 articles (1 dp): LOC-M 4.0 (6,941 articles); BUS-N 4.4 (7,937); CUL-N 3.1 (3,883); SPT-N 3.1 (11,043); POL-N 4.3 (9,007); SPT-M 6.9 (2,463)
- median minutes from going live to first headline correction (whole minutes): LOC-M 72 (71.5 before rounding); BUS-N 85; CUL-N 79; SPT-N 42 (41.5); POL-N 76 (75.5); SPT-M 57
- finished embeddings the method gets within 2 per cent: 7 of 7. Errors: Games 2019 +1.16%, Wellness 2020 +1.06%, Puzzles 2021 +0.19%, Recipes 2022 +0.55%, Games 2023 -0.27%, Recipes 2024 -0.71%, Wellness 2025 -0.85%
