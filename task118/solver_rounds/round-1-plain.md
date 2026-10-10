# solver round: round 1, plain

**Proxy score 46.0 / 100** (recommendation 0.0 of 35, instruction 7.0 of 7, asks 39.0 of 58). Main call missed. 1 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.

solver: The squad should join Local·metro (LOC-M). It would add about 2,800,000 extra article clicks there in 2027 (2,792,947 before rounding). Business·national is the runner-up at 1,750,000, which puts it 1,050,000 behind.

tokens matched 0 of 3 (1,250,000, Place, Culture)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| squad_placement_2027.docx | 1 | 1 | 2 | 50% |
| squad_placement_2027.docx | 2 | 2 | 4 | 50% |
| squad_placement_2027.docx | 3 | 2 | 3 | 67% |
| squad_placement_2027.xlsx | 1 | 34 | 49 | 69% |
| squad_placement_2027.xlsx | 2 | 2 | 2 | 100% |

## Solver's path

1. headline_tests_archive (14,131 package rows, 4,020 tests): computed each variant's lift against its control (CTR ratio minus 1) and its delta-method standard error. Fitted a normal prior to all 10,111 non-control variants by maximum likelihood: mu = -0.0104, tau = 0.0453. Shrank each shipped variant's lift to its posterior mean, with 0 for tests that kept the control. The dashboard's raw 'winning lift' suffers from winner's curse: Nina's 95% bar is one-sided, tests have 2 to 5 variants, and the Brisbane desks ship at about z >= 0.84.
2. Back-test against headline_squad_change_log: the mean shrunk lift per test times planned_clicks lands within 2% of realised_incremental_clicks for all 7 app embeddings. The worst miss is 1.2%, with no scaling factor. App desks get every click from on-platform surfaces, so the scaling factor is 1. The raw dashboard lift overstates by 30% to 270%.
3. pageviews parquet (12 months to Sep 2026; totals match audience_plan_2027 P2 desk by desk): limited each desk's clicks to the surfaces that show the live, tested headline (home_web, section_web, feed_app, section_app, related_links). Search, discover, partner_apps, social, newsletter and alerts carry the canonical headline from publication, per the field reference. On-platform clicks: LOC-M 108.7m, SPT-N 98.2m, BUS-N 86.4m, CUL-N 76.9m, POL-N 71.4m, SPT-M 57.8m.
4. Extra clicks = on-platform clicks x mean shrunk lift of the desk's own web tests from Oct 2025 to Sep 2026. LOC-M: 0.0257 x 108.7m = 2.79m. BUS-N: 0.0200 x 86.4m = 1.73m. CUL-N 1.37m, SPT-N 1.30m, POL-N 0.91m, SPT-M 0.23m. The plan holds 2027 clicks at the trailing 12 months, so these figures apply to 2027 unchanged. The traps rank differently: dashboard lift x total clicks picks SPT-M or BUS-N, shrunk lift x total clicks picks BUS-N, and readers pick POL-N.
5. Panel: kept the latest release for each period, using R26-07B's restated April to June 2026 in place of the original releases. Mapped section codes to desks through the Section history sheet, because the codes were reshuffled from March 2026. Averaged unique_audience over the 12 months, e.g. LOC-M 616,760 and POL-N 3,180,260.
6. CMS revisions: merged documents recreated by the 14 Nov 2025 Brisbane restore into their originals. Dropped the 1,704 documents migrated from the old CMS. Kept documents first live between 30 Sep 2025 14:00Z and 30 Sep 2026 14:00Z. Story and live-blog counts match the article counts in the pageview data exactly.
7. A headline correction is a revision that adds a new correction note and changes headline_sha1, following standards s7.4. Notes copied forward to later revisions and notes carried onto restored copies were not counted again. This gives 208 corrections. March 2026 (AEST) has 12 headline and 31 text corrections, matching the April standards bulletin exactly. Rates are per 1,000 stories plus live blogs. Times are minutes from a document's first live save to its first headline correction, taking the median per desk.

confidence: Medium-high on the desk choice: Local·metro leads every lift-prior variant I tried by more than 1m clicks. Medium on the exact figures. LOC-M's 2.79m rounds to 2.80m under every prior I tried. BUS-N's 1,726,554 sits right on the 1,725,000 rounding line, so 1,750,000 could be 1,700,000 under a slightly different prior. Applying the squad's own 95% shipping bar to LOC-M's tests would give about 2.40m instead of 2.80m.

notes: Two things are still open. The figures use LOC-M's archived tests as shipped, at its roughly 80% bar; re-scoring them at the squad's 95% bar would cut the estimate to about 2.4m, though LOC-M would still be first. I also did not net off the testing the web desks already do themselves.

### squad_placement_2027.docx (solver's answers)
- Chosen desk and extra 2027 clicks: Local·metro (LOC-M): 2,800,000 extra article clicks in 2027 (nearest 50,000)
- Runner-up and gap: Business·national (BUS-N): 1,750,000 extra clicks. Local·metro leads it by 1,050,000 clicks (nearest 50,000).
- Chart: each desk's 2027 clicks and the squad's extra clicks, ordered by extra clicks: Local·metro 114,750,000 -> +2,800,000. Business·national 309,050,000 -> +1,750,000. Culture·national 153,350,000 -> +1,350,000. Sport·national 341,000,000 -> +1,300,000. Politics·national 376,250,000 -> +900,000. Sport·metro 104,650,000 -> +250,000. Local·metro is marked as the chosen desk and Business·national as the runner-up, with the 1,050,000 gap labelled. Title: 'Local·metro: the squad adds about 2.8 million clicks in 2027'. Politics·metro, which is not on the shortlist, would add +50,000 on 61,250,000.

### squad_placement_2027.xlsx (solver's answers)
- Extra clicks 2027 per desk (nearest 50,000): POL-N 900,000; SPT-M 250,000; BUS-N 1,750,000; SPT-N 1,300,000; LOC-M 2,800,000; CUL-N 1,350,000; POL-M (off the shortlist) 50,000
- Average monthly readers, Oct 2025 to Sep 2026 (nearest thousand): POL-N 3,180,000; SPT-M 470,000; BUS-N 1,760,000; SPT-N 2,931,000; LOC-M 617,000; CUL-N 1,412,000; POL-M 331,000
- Extra clicks per reader (1 dp): POL-N 0.3; SPT-M 0.5; BUS-N 1.0; SPT-N 0.4; LOC-M 4.5; CUL-N 1.0; POL-M 0.2
- Headline corrections, 12 months (whole numbers): POL-N 47; SPT-M 18; BUS-N 39; SPT-N 42; LOC-M 34; CUL-N 14; POL-M 14. Total across the 7 web desks is 208, and the March 2026 figure of 12 matches the standards bulletin.
- Headline corrections per 1,000 articles (1 dp): POL-N 5.2 (of 9,007 articles); SPT-M 7.3 (of 2,463); BUS-N 4.9 (of 7,937); SPT-N 3.8 (of 11,043); LOC-M 4.9 (of 6,941); CUL-N 3.6 (of 3,883); POL-M 4.4 (of 3,186)
- Median minutes from going live to first headline correction: POL-N 68; SPT-M 51; BUS-N 97; SPT-N 36; LOC-M 77; CUL-N 139; POL-M 55
- 2027 clicks per desk (nearest 50,000): POL-N 376,250,000; SPT-M 104,650,000; BUS-N 309,050,000; SPT-N 341,000,000; LOC-M 114,750,000; CUL-N 153,350,000
- Back-test: finished embeddings within 2% of actual: 7 of 7. Deviations were +1.2%, +1.1%, +0.2%, +0.6%, -0.3%, -0.7% and -0.9%.
