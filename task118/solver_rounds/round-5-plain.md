# solver round: round 5, plain

**Proxy score 43.9 / 100** (recommendation 0.0 of 35, instruction 7.0 of 7, asks 36.9 of 58). Main call missed. 1 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.

solver: Put the headline squad on Local·metro (LOC-M) for 2027. It should add about 2,750,000 extra article clicks there. The runner-up is Business·national at about 1,700,000, so Local·metro leads by about 1,050,000. The dashboard's ranking by vertical points to Politics (4.69%), but that figure is inflated by Politics·metro's small, noisy tests, and the panel's readers measure points to Politics·national. Neither predicts the clicks the squad actually adds.

tokens matched 0 of 3 (1,250,000, Place, Culture)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| squad_placement_2027.docx | 1 | 1 | 2 | 50% |
| squad_placement_2027.docx | 2 | 2 | 4 | 50% |
| squad_placement_2027.docx | 3 | 2 | 3 | 67% |
| squad_placement_2027.xlsx | 1 | 25 | 49 | 51% |
| squad_placement_2027.xlsx | 2 | 2 | 2 | 100% |

## Solver's path

1. Read the brief, the email thread, the field reference, the CMS export field notes, the standards section 7 PDF, the Newsfold agreement, the dashboard export, the change log and the plan. The headline the squad tests appears only on home_web, section_web, feed_app, section_app and related_links. RSS and partner feeds, search, social, newsletters and alerts carry the original headline stored at publication.
2. Grouped the pageviews parquet by desk and source to get each desk's share of clicks from surfaces that show the tested headline: LOC-M 0.947, CUL-N 0.502, SPT-M 0.552, SPT-N 0.288, BUS-N 0.279, POL-N 0.190, app desks 1.00. Partner apps (Newsfold) dominate Politics·national.
3. Built a per-variant lift from the headline test archive (variant CTR divided by control CTR, minus one) with a binomial standard error. The shipped package is always the top variant, so the dashboard's winning lift suffers from the winner's curse. Politics·metro and Sport·metro tests average only about 2,000 impressions, which inflates the Politics and Sport vertical figures.
4. Shrank each variant's lift toward a normal prior, mu = -0.02 and tau^2 = 0.00215. tau^2 is close to the method-of-moments estimate (0.0021 to 0.0022) and to the nonparametric fit's mode near -0.02. The squad's lift per test is the average of the shrunk shipped lifts, counting zero when the control was kept. Times planned clicks and surface share, this reproduces all 7 change-log embeddings within 2% (errors from -1.7% to +1.7%).
5. Applied the same method to each web desk's 12 months of web-engine tests. Extra clicks = 2027 plan clicks × surface share × shrunk lift per test. LOC-M 2.753m (lift 2.53%), BUS-N 1.716m, CUL-N 1.354m, SPT-N 1.288m, POL-N 0.906m, SPT-M 0.118m. Rounded to the nearest 50,000, the gap is 2,750,000 - 1,700,000 = 1,050,000.
6. Panel readers: mapped each panel row to a desk using the section taxonomy of its release (old codes before R26-04, new codes from R26-04 and R26-04H), then kept the latest release for each period and desk (R26-04H for Nov 2025 to Feb 2026 BLN; R26-07B for Apr to Jun 2026 BLB). Averaged unique_audience over Oct 2025 to Sep 2026 to the nearest thousand and divided extra clicks by it.
7. CMS revisions: merged documents recreated in the 14 Nov restore into their originals. Ignored notes that arrived with migration. Took the new text of stacked notes as the prefix added above the earlier note. A note counts as a headline correction if the live headline changes on the revision that publishes it, or if it is a headline-worded note whose headline changed live up to 10 minutes earlier. For a live-blog entry, it counts if the entry's headline changed live within 10 minutes. This gives March 2026 11 headline and 22 text corrections, matching the April bulletin.
8. Articles are stories and live blogs that went live in the window; a scheduled publish_at counts as going live if no other save came before it. Migrated documents are excluded. Per desk: count of headline corrections, rate per 1,000 articles, and median minutes from going live (for live blogs, from the entry going live) to the first headline correction.

confidence: Medium-high on the call: Local·metro leads in every specification I tried by more than 0.9m clicks, and Business·national comes second each time. Medium on exact figures: the 2,750,000 holds across shrinkage settings that fit the change log (2.746m to 2.756m). Sport·metro's extra clicks swing between 50k and 200k depending on the prior.

notes: I calibrated the shrinkage prior to the seven embeddings. Unfitted moment or nonparametric priors over-predict the low-sample embeddings by 3 to 35%, so the 7 of 7 result depends on that calibration. For live-blog entry corrections, I timed the median minutes from the entry going live. Timing from the live blog going live instead gives Local·metro 87, Business·national 85, Sport·national 44 and Politics·national 76. Sport·national's median of 42.5 rounds half-up to 43.

### squad_placement_2027.docx (solver's answers)
- recommended desk: Local·metro (LOC-M)
- extra article clicks in 2027 at chosen desk: 2,750,000 extra clicks (nearest 50,000)
- runner-up desk: Business·national (BUS-N)
- runner-up extra clicks: 1,700,000 extra clicks (nearest 50,000)
- gap between chosen desk and runner-up: 1,050,000 clicks (nearest 50,000)
- chart: 2027 planned clicks for each desk, to the nearest 50,000, in order of extra clicks: Local·metro 114,750,000; Business·national 309,050,000; Culture·national 153,350,000; Sport·national 341,000,000; Politics·national 376,250,000; Sport·metro 104,650,000
- chart title: Local·metro: the squad adds about 2.75m clicks in 2027, 1.05m more than Business·national

### squad_placement_2027.xlsx (solver's answers)
- Local·metro row: extra clicks 2,750,000; average monthly readers 617,000; extra clicks per reader 4.5; headline corrections 33; per 1,000 articles 4.8 (6,941 articles); median minutes to first headline correction 72
- Business·national row: extra clicks 1,700,000; average monthly readers 1,760,000; extra clicks per reader 1.0; headline corrections 37; per 1,000 articles 4.7 (7,937 articles); median minutes 79
- Culture·national row: extra clicks 1,350,000; average monthly readers 1,412,000; extra clicks per reader 1.0; headline corrections 13; per 1,000 articles 3.3 (3,883 articles); median minutes 99
- Sport·national row: extra clicks 1,300,000; average monthly readers 2,931,000; extra clicks per reader 0.4; headline corrections 39; per 1,000 articles 3.5 (11,043 articles); median minutes 43
- Politics·national row: extra clicks 900,000; average monthly readers 3,180,000; extra clicks per reader 0.3; headline corrections 44; per 1,000 articles 4.9 (9,007 articles); median minutes 76
- Sport·metro row: extra clicks 100,000; average monthly readers 470,000; extra clicks per reader 0.3; headline corrections 18; per 1,000 articles 7.3 (2,463 articles); median minutes 55
- finished embeddings reproduced within 2 per cent: 7 of 7 (errors from -1.7% to +1.7%)
