# solver round: round 7, plain

**Proxy score 45.5 / 100** (recommendation 1.7 of 35, instruction 7.0 of 7, asks 36.9 of 58). Main call missed. 1 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.

solver: Place the headline squad with Local·metro (LOC-M) for 2027. It should add about 2,800,000 extra article clicks there. The runner-up is Business·national (BUS-N) at about 1,750,000, so Local·metro leads by about 1,050,000 clicks. Politics·national, the desk with the most readers (Kayla Torres's pick), would add only about 900,000.

tokens matched 1 of 3 (1,250,000, Place, Culture)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| squad_placement_2027.docx | 1 | 1 | 2 | 50% |
| squad_placement_2027.docx | 2 | 2 | 4 | 50% |
| squad_placement_2027.docx | 3 | 2 | 3 | 67% |
| squad_placement_2027.xlsx | 1 | 25 | 49 | 51% |
| squad_placement_2027.xlsx | 2 | 2 | 2 | 100% |

## Solver's path

1. Checked audience_plan_2027.xlsx against the pageview parquet. The 2027 plan clicks equal each desk's October 2025 to September 2026 pageview total exactly, so the plan is a flat roll-forward of last year.
2. Joined the headline test archive to itself on test_id to get each package's click-through rate against its control. Shipped lift is the shipped package's CTR over the control's, minus one, and zero when the control is kept. This reproduces the avg_winning_lift_pct in the change log, so the archive matches the log.
3. Raw winning lift overstates the true effect. Its ratio to realised clicks ran from 0.26 to 0.76 across embeddings and fell as test samples shrank. Sport·metro and Politics·metro tests average about 2,200 impressions, which inflates the dashboard's Sport and Politics figures.
4. Corrected for this with empirical Bayes shrinkage. The prior comes from all variants with error variance below 0.001: mean variant lift -1.01%, true-lift variance 0.00203. Each shipped variant's lift is pulled toward that prior in proportion to its noise.
5. Checked the method against the change log: the mean shrunk lift of each embedding's tests times that year's planned clicks lands within 2% of realised_incremental_clicks for 7 of 7 embeddings (largest gap 1.1%).
6. Worked out which clicks a tested headline can reach. The field reference says the canonical headline feeds RSS and partner apps, search, social, discover, newsletters and alerts. So the base is home_web + section_web + feed_app + section_app + related_links. This is 94.7% of Local·metro clicks (it has no Newsfold partner traffic) but only 19 to 29% for the national desks. For the app desks this base is 100% of clicks, which the calibration needs.
7. Extra clicks = the desk's mean shrunk shipped lift from its own web tests over the last 12 months times the plan clicks on those surfaces. Local·metro 2,789,024; Business·national 1,725,051; Culture·national 1,368,398; Sport·national 1,296,754; Politics·national 912,796; Sport·metro 229,246.
8. Panel readers: mapped section codes using the old taxonomy for releases before R26-04 and the 2026 taxonomy from R26-04 and R26-04H on. For each period took the latest release whose log covers it: R26-04H for Politics and Culture November to February, and R26-07B for April to June. Ignored the stale April to June rows that reappear in R26-08. Averaged 12 months of unique_audience: Local·metro 616,760; Politics·national 3,180,260.
9. Articles from the CMS export: stories and live blogs whose go-live (the earlier of publish_at and the first live save) falls in the 12 months, excluding withdrawn-before-publish documents, 1 October migration copies and 14 November Brisbane restore copies. Restore copies were mapped back to their originals. The counts match the pageview article counts exactly (Local·metro 6,941).
10. Headline corrections: a new correction-note segment (ignoring stacked-note carry-over, re-added notes, and notes carried on the first revision of migrated or restored copies) with the document's headline changing within 15 minutes. For live blogs, the test is a child post's headline changing within 10 minutes. This gives 11 headline and 22 text corrections for March 2026, matching standards bulletin issue 31. The correction time is the first live revision publishing the corrected headline, measured from when that headline went live (the post's go-live for live-blog entries). Took the first correction per article and the median per desk.

confidence: The desk ranking and the 2,800,000 figure are solid: every prior variant tried keeps Local·metro first, at 2.78m to 2.85m. The runner-up's rounding is borderline: Business·national is 1,725,051, which sits almost exactly on the 50,000 boundary. The median minutes depend on one judgement call (from the post's go-live, not the live blog's). Counts, rates and readers have been checked against the files.

notes: Business·national's unrounded figure is right on the rounding boundary, so its rounded value and the gap could read 1,700,000 and 1,100,000 under a slightly different prior. If live-blog entry corrections are timed from the live blog's own go-live, the medians become: Business·national 89, Culture·national 119, Local·metro 102, Politics·national 86, Sport·metro 55, Sport·national 47.

### squad_placement_2027.docx (solver's answers)
- Recommended desk: Local·metro (LOC-M)
- Extra article clicks at the chosen desk in 2027: 2,800,000 clicks (nearest 50,000; unrounded 2,789,024)
- Runner-up desk: Business·national (BUS-N), 1,750,000 extra clicks (nearest 50,000; unrounded 1,725,051)
- Gap between chosen desk and runner-up: 1,050,000 clicks (nearest 50,000; unrounded 1,063,973; 2,800,000 minus 1,750,000 also gives 1,050,000)
- Chart: each desk's 2027 clicks and extra clicks, in order of extra clicks: Local·metro: 114,750,000 planned clicks, 2,800,000 extra. Business·national: 309,050,000 planned, 1,750,000 extra. Culture·national: 153,350,000 planned, 1,350,000 extra. Sport·national: 341,000,000 planned, 1,300,000 extra. Politics·national: 376,250,000 planned, 900,000 extra. Sport·metro: 104,650,000 planned, 250,000 extra. Chosen desk is Local·metro and runner-up is Business·national, with the gap labelled 1,050,000. All figures to the nearest 50,000. Title: 'Local·metro: the headline squad adds about 2.8m clicks in 2027'.

### squad_placement_2027.xlsx (solver's answers)
- Local·metro row: Extra clicks 2027: 2,800,000. Average monthly readers: 617,000. Extra clicks per reader: 4.5. Headline corrections: 34. Rate per 1,000 articles: 4.9 (6,941 articles). Median minutes to first headline correction: 71.
- Business·national row: Extra clicks 2027: 1,750,000. Average monthly readers: 1,760,000. Extra clicks per reader: 1.0. Headline corrections: 39. Rate per 1,000 articles: 4.9 (7,937 articles). Median minutes to first headline correction: 79.
- Culture·national row: Extra clicks 2027: 1,350,000. Average monthly readers: 1,412,000. Extra clicks per reader: 1.0. Headline corrections: 14. Rate per 1,000 articles: 3.6 (3,883 articles). Median minutes to first headline correction: 79.
- Sport·national row: Extra clicks 2027: 1,300,000. Average monthly readers: 2,931,000. Extra clicks per reader: 0.4. Headline corrections: 42. Rate per 1,000 articles: 3.8 (11,043 articles). Median minutes to first headline correction: 42.
- Politics·national row: Extra clicks 2027: 900,000. Average monthly readers: 3,180,000. Extra clicks per reader: 0.3. Headline corrections: 47. Rate per 1,000 articles: 5.2 (9,007 articles). Median minutes to first headline correction: 69.
- Sport·metro row: Extra clicks 2027: 250,000. Average monthly readers: 470,000. Extra clicks per reader: 0.5. Headline corrections: 18. Rate per 1,000 articles: 7.3 (2,463 articles). Median minutes to first headline correction: 43.
- Calibration line: finished embeddings within 2 per cent: 7 of 7. Gaps between the method's figure and what each embedding actually added: +0.9%, +0.7%, +0.1%, +0.4%, -0.7%, -1.1%, -1.0%.
