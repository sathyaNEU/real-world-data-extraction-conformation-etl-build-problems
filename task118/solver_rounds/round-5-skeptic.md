# solver round: round 5, skeptic

**Proxy score 33.7 / 100** (recommendation 1.7 of 35, instruction 7.0 of 7, asks 25.1 of 58). Main call missed. 1 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.

solver: Place the headline squad with Local·metro (LOC-M) for 2027, where it would add about 2,800,000 extra article clicks (2,792,947 before rounding). That is 2027 planned clicks of 114,737,642, of which 108,693,347 come from surfaces that show the tested headline, times a shrunk average lift of 2.570% per test over 1,400 tests. The runner-up is Business·national at 1,750,000 (1,726,554), about 1,050,000 behind. The dashboard's lift view and the panel's reader counts both point to the wrong desk.

tokens matched 1 of 3 (1,250,000, Place, Culture)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| squad_placement_2027.docx | 1 | 0 | 2 | 0% |
| squad_placement_2027.docx | 2 | 2 | 4 | 50% |
| squad_placement_2027.docx | 3 | 1 | 3 | 33% |
| squad_placement_2027.xlsx | 1 | 16 | 49 | 33% |
| squad_placement_2027.xlsx | 2 | 2 | 2 | 100% |

## Solver's path

1. Test archive (headline_tests_archive_2019-2026.csv, 4,020 tests): for each test, computed the shipped package's lift over the control (zero when the control was kept). This reproduces the change log's avg_winning_lift_pct and the dashboard's vertical counts, for example Politics 415 = POL-N 205 + POL-M 210.
2. For every non-control package (10,111), computed relative lift and its delta-method variance: p_v(1-p_v)/(n_v p_c^2) + p_v^2(1-p_c)/(n_c p_c^3). Fitted a normal prior by marginal maximum likelihood over the full archive: mean -0.01038, tau 0.04533.
3. Shrunk each shipped winner to its posterior mean m + (lift - m)*tau^2/(tau^2+se^2), with control-kept tests at 0. Embedding estimate = planned_clicks_m x (sum of posterior lifts / tests_run). App desks' clicks all come from app surfaces, so the reach factor is 1. All 7 closed embeddings in headline_squad_change_log.xlsx land within 2% (largest error +1.16%). The dashboard's raw average lift overstates them by 31% to 285%.
4. Reach: per the field reference, the canonical headline (not the tested one) is what feeds partner apps, search, discover, social, newsletters and alerts. So only home_web, section_web, feed_app, section_app and related_links take the uplift. From the pageviews parquet these come to: LOC-M 108.69m of 114.74m clicks; BUS-N 86.35m of 309.05m; SPT-N 98.22m of 340.99m; POL-N 71.40m of 376.24m; CUL-N 76.92m of 153.34m; SPT-M 57.79m of 104.67m. The parquet totals match the clicks in audience_plan_2027.xlsx exactly.
5. 2027 extra clicks = addressable clicks x mean posterior lift per test, taken over each desk's web-engine tests in the 12 months. Mean posterior lifts: LOC-M 2.570% (1,400 tests), BUS-N 1.999%, CUL-N 1.781%, SPT-N 1.321%, POL-N 1.279%, SPT-M 0.394%. That gives LOC-M 2,792,947 > BUS-N 1,726,554 > CUL-N 1,369,906 > SPT-N 1,297,878 > POL-N 913,383 > SPT-M 227,556. SPT-M and POL-M have tiny tests (8,000 to 11,000 impressions), so their 10.8% and 7.9% dashboard lifts shrink almost to nothing.
6. Panel readers (panel_monthly_audience + panel_reference_workbook): sections mapped by the old taxonomy before March 2026 and the new one after. R26-04H supersedes Nov 2025 to Feb 2026 for the sections it restates (POL-N, CUL-N). R26-07B supersedes Apr to Jun 2026 for Brisbane. Took the 12-month mean of unique_audience. Extra per reader = extra clicks / average readers.
7. CMS revisions: merged restored Brisbane copies (restored_from_doc) into their originals. Dropped migrated documents and documents that never went live (534 scheduled then withdrawn). Go-live = earlier of the scheduled publish_at and the first live save. Articles = stories plus live blogs that went live in the window; the per-desk counts match the pageview article counts exactly (e.g. BUS-N 7,937).
8. A headline correction is a new correction note logged on a revision that changes the headline, live or draft (when the change is on a draft, the next live save counts as publishing it). Also counted: notes that name the headline and follow a just-published headline change by 0 to 9 minutes, and live-blog notes paired with an entry whose headline changed. This rule reproduces the April 2026 bulletin's March figures exactly: 11 headline corrections (7 live and 4 draft same-revision) and 22 text corrections. Medians use each article's first correction, timed from the go-live of the item carrying the headline (the entry itself for live-blog entries).

confidence: Medium-high on the call (LOC-M wins under every shrinkage variant tried, from about 2.78m to 2.86m, with BUS-N second at about 1.72m to 1.75m). Medium on the exact rounded figures. The calibration supports several prior and standard-error variants, and the 2.80m is the one where the full-archive MLE prior hits all 7 embeddings. Medium on the medians, which depend on the live-blog timing basis.

notes: The files leave a few things open. First, whether live-blog entry corrections are timed from the entry's go-live or the blog's; on the blog basis SPT-M comes out at 62.5, LOC-M 102 and POL-N 82. Second, whether 'title'-vocabulary notes posted a few minutes after the headline change count as headline corrections; a strict same-revision rule would give BUS-N 22, CUL-N 9, LOC-M 17, POL-N 26, SPT-M 12, SPT-N 18. Third, no age-band adjustment for clicks that arrive during the test was applied, because the app calibration matches without one.

### squad_placement_2027.docx (solver's answers)
- recommended desk: Local·metro (LOC-M)
- extra article clicks in 2027 at the chosen desk, to the nearest 50,000: 2,800,000 extra clicks (unrounded 2,792,947)
- runner-up desk and its extra clicks: Business·national (BUS-N), 1,750,000 extra clicks (unrounded 1,726,554)
- gap between chosen desk and runner-up, to the nearest 50,000: 1,050,000 clicks (unrounded 1,066,393)
- chart walk, 2027 clicks to addressable (on-site and app) clicks to extra clicks, ordered by extra clicks, nearest 50,000: LOC-M 114,750,000 -> 108,700,000 -> 2,800,000; BUS-N 309,050,000 -> 86,350,000 -> 1,750,000; CUL-N 153,350,000 -> 76,900,000 -> 1,350,000; SPT-N 341,000,000 -> 98,200,000 -> 1,300,000; POL-N 376,250,000 -> 71,400,000 -> 900,000; SPT-M 104,650,000 -> 57,800,000 -> 250,000. Chosen desk is LOC-M, runner-up is BUS-N, gap label is 1,050,000. Suggested title: 'Local·metro: squad adds 2.80m clicks in 2027'

### squad_placement_2027.xlsx (solver's answers)
- extra clicks 2027 per desk, nearest 50,000: LOC-M 2,800,000; BUS-N 1,750,000; CUL-N 1,350,000; SPT-N 1,300,000; POL-N 900,000; SPT-M 250,000
- average monthly readers, 12 months to Sep 2026, nearest thousand: POL-N 3,180,000; SPT-N 2,931,000; BUS-N 1,760,000; CUL-N 1,412,000; LOC-M 617,000; SPT-M 470,000
- extra clicks per reader, 1 dp: LOC-M 4.5; BUS-N 1.0; CUL-N 1.0; SPT-M 0.5; SPT-N 0.4; POL-N 0.3
- headline corrections, 12 months to Sep 2026 (whole number): POL-N 40; BUS-N 35; SPT-N 35; LOC-M 29; SPT-M 17; CUL-N 12
- headline corrections per 1,000 articles, 1 dp: SPT-M 6.9 (17/2,463); POL-N 4.4 (40/9,007); BUS-N 4.4 (35/7,937); LOC-M 4.2 (29/6,941); SPT-N 3.2 (35/11,043); CUL-N 3.1 (12/3,883)
- median minutes from going live to first headline correction (whole minutes): BUS-N 85; CUL-N 79; LOC-M 71; POL-N 69; SPT-M 57; SPT-N 41
- finished embeddings reproduced within 2 per cent: 7 of 7. Errors: Games 2019 +1.16%, Wellness 2020 +1.06%, Puzzles 2021 +0.19%, Recipes 2022 +0.55%, Games 2023 -0.27%, Recipes 2024 -0.71%, Wellness 2025 -0.85%
