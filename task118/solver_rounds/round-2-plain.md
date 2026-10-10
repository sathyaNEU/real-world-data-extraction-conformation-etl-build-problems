# solver round: round 2, plain

**Proxy score 38.0 / 100** (recommendation 1.7 of 35, instruction 7.0 of 7, asks 29.3 of 58). Main call missed. 1 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.

solver: Place the headline squad with Local·metro (LOC-M) for 2027. It would add about 2,800,000 extra article clicks there. The runner-up is Business·national (BUS-N) at about 1,750,000, so Local·metro leads by about 1,050,000. On the dashboard view Politics looks best (4.69% average winning lift), and on Kayla's 'where the readers are' view Politics·national looks best (about 3,180,000 monthly readers). Once each desk's test lifts are shrunk for noise, and only the surfaces that actually show the tested headline are counted, Politics·national comes out at only about 900,000.

tokens matched 1 of 3 (1,250,000, Place, Culture)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| squad_placement_2027.docx | 1 | 0 | 2 | 0% |
| squad_placement_2027.docx | 2 | 2 | 4 | 50% |
| squad_placement_2027.docx | 3 | 1 | 3 | 33% |
| squad_placement_2027.xlsx | 1 | 34 | 49 | 69% |
| squad_placement_2027.xlsx | 2 | 2 | 2 | 100% |

## Solver's path

1. Read prompt.md, the placement brief, the email thread, the field reference, desk_register, audience_plan_2027 (2027 clicks are held at Oct25-Sep26 pageviews, which match the parquet desk totals exactly), the change log (7 embeddings: realised incremental clicks and planned clicks), the dashboard export and the Newsfold agreement.
2. Test archive: joined owner_staff_id to the staff list. All app tests are squad tests (AUD-HS), one embedding per year. The web tests (Oct 2025-Sep 2026) were all run by desk staff, and their totals match the dashboard counts by vertical (Politics 415 = POL-N 205 + POL-M 210, Sport 950, Business 700, Local 1,400, Culture 50).
3. Calibration: realised/planned divided by the change log's average winning lift ran from 0.26 to 0.77, rising with test size. That is the winner's curse, so the dashboard lift and the raw lift fail. I fitted a normal-normal empirical-Bayes prior on variant lift (CTR ratio minus 1, delta-method variance) by maximum likelihood across all 10,111 variant packages: mu = -0.01038, tau^2 = 0.002055. Each shipped variant's posterior mean = mu + (lift - mu)*tau^2/(tau^2 + se^2); a kept control counts as 0. Expected lift per test = sum of posteriors / tests run. Planned clicks x expected lift reproduces all 7 realised embeddings within 1.2%, so 7 of 7 are within 2% (app desks have only in-app surfaces, so k = 1).
4. Testable share: per the field reference, search, discover, partner_apps, social, newsletter and alerts carry the canonical headline. Testable surfaces are home_web, section_web, feed_app, section_app and related_links. Shares from the parquet: LOC-M 0.947 (no Newsfold feed), BUS-N 0.279, CUL-N 0.502, SPT-N 0.288, POL-N 0.190, SPT-M 0.552, POL-M 0.599.
5. Posterior expected lift per test from each desk's own web tests: LOC-M 2.570%, BUS-N 1.999%, CUL-N 1.781%, SPT-N 1.321%, POL-N 1.279%, SPT-M 0.394%, POL-M 0.198%. SPT-M and POL-M tests are tiny, so their raw lifts of 10.8% and 7.9% shrink almost to zero. Extra clicks = 2027 clicks x testable share x expected lift: LOC-M 2,792,947; BUS-N 1,726,554; CUL-N 1,369,906; SPT-N 1,297,878; POL-N 913,383; SPT-M 227,556; POL-M 72,833.
6. Readers: took the latest release per period from panel_monthly. R26-04H replaces Nov 2025-Feb 2026 and R26-07B replaces Apr-Jun 2026. Section codes are mapped by the taxonomy of the release: the old mapping for R25-11 to R26-03 and the new mapping for R26-04 onward, including R26-04H. Unique_audience is averaged over the 12 months.
7. Corrections: in the CMS export, recreated Brisbane documents are mapped back to their originals via restored_from_doc. The 1,704 migrated documents are excluded from article counts. Article counts then match the parquet's articles published in the window exactly for every desk. Go-live = first live save, or publish_at for a schedule that fired. A headline correction is a live revision whose headline differs from the published headline and which carries a newly added correction note. For live blogs, a note added to the blog in the same minute as a post headline change also counts. This reproduces the April bulletin's March figures exactly (11 headline, 22 text corrections). Rates are per 1,000 articles; the median is taken on the first correction per article.

confidence: Medium-high. The 7-of-7 calibration and the exact March bulletin match support the method. The testable-surface split (related_links counted as testable, discover as canonical) is my reading of the field reference. Local·metro stays first under any reasonable variation tested: using all traffic, or raw lifts, would favour Business or Sport·metro instead, but those are the defeated readings.

notes: The files do not say whether a squad embedding adds to or replaces a desk's own testing; I assumed the squad's per-test expected lift equals the posterior lift of the desk's own tests. Migrated documents carried no in-window headline corrections, so excluding them affects only the article denominators.

### squad_placement_2027.docx (solver's answers)
- Recommended desk: Local·metro (LOC-M)
- Extra clicks the squad adds at the chosen desk in 2027: 2,800,000 extra article clicks (unrounded 2,792,947; nearest 50,000)
- Runner-up desk and its extra clicks: Business·national (BUS-N), 1,750,000 extra clicks (unrounded 1,726,554)
- Gap between chosen desk and runner-up: 1,050,000 clicks (unrounded 1,066,393; nearest 50,000)
- Chart order by extra clicks, with each desk's 2027 clicks: LOC-M 2,800,000 extra (2027 clicks 114,750,000); BUS-N 1,750,000 (309,050,000); CUL-N 1,350,000 (153,350,000); SPT-N 1,300,000 (341,000,000); POL-N 900,000 (376,250,000); SPT-M 250,000 (104,650,000). Politics·metro (POL-M, 50,000 extra, 61,250,000 clicks) is not on the shortlist.
- Chart title: Local·metro: the squad adds about 2.8m clicks in 2027, about 1.05m ahead of Business·national

### squad_placement_2027.xlsx (solver's answers)
- Extra clicks 2027 per desk (nearest 50,000): LOC-M 2,800,000; BUS-N 1,750,000; CUL-N 1,350,000; SPT-N 1,300,000; POL-N 900,000; SPT-M 250,000; POL-M 50,000
- Average monthly readers, 12 months to Sep 2026 (nearest thousand): POL-N 3,180,000; SPT-N 2,931,000; BUS-N 1,760,000; CUL-N 1,412,000; LOC-M 617,000; SPT-M 470,000; POL-M 331,000
- Extra clicks per reader (1 dp): LOC-M 4.5; BUS-N 1.0; CUL-N 1.0; SPT-M 0.5; SPT-N 0.4; POL-N 0.3; POL-M 0.2
- Headline corrections, 12 months to Sep 2026 (whole numbers): POL-N 47; SPT-N 42; BUS-N 39; LOC-M 34; SPT-M 18; CUL-N 14; POL-M 14 (208 in total)
- Headline corrections per 1,000 articles (1 dp): SPT-M 7.3 (of 2,463 articles); POL-N 5.2 (of 9,007); BUS-N 4.9 (of 7,937); LOC-M 4.9 (of 6,941); POL-M 4.4 (of 3,186); SPT-N 3.8 (of 11,043); CUL-N 3.6 (of 3,883)
- Median minutes from going live to first headline correction (whole minutes): SPT-N 47; SPT-M 55; POL-M 78; POL-N 86; BUS-N 89; LOC-M 102; CUL-N 119
- Calibration against the seven finished embeddings: 7 of 7 within 2 per cent of the realised incremental clicks (ratios of realised to the method's estimate: 0.989, 0.990, 0.998, 0.995, 1.003, 1.007, 1.009)
