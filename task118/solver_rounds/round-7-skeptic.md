# solver round: round 7, skeptic

**Proxy score 36.3 / 100** (recommendation 0.0 of 35, instruction 7.0 of 7, asks 29.3 of 58). Main call missed. 1 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.

solver: Put the headline squad on Local·metro (LOC-M) for 2027. On my estimate it adds about 2,800,000 extra article clicks there. The runner-up is Business·national at 1,750,000, so Local·metro leads by about 1,050,000. The estimate takes the 108.7M clicks that come from surfaces showing the tested headline (94.7% of LOC-M's 114.7M plan clicks) and multiplies them by a corrected lift of 2.57% per test. That lift is the empirical-Bayes posterior over LOC-M's 1,400 tests, not the 3.44% the dashboard shows. The same method reproduces all 7 closed embeddings within 2%.

tokens matched 0 of 3 (1,250,000, Place, Culture)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| squad_placement_2027.docx | 1 | 0 | 2 | 0% |
| squad_placement_2027.docx | 2 | 2 | 4 | 50% |
| squad_placement_2027.docx | 3 | 1 | 3 | 33% |
| squad_placement_2027.xlsx | 1 | 34 | 49 | 69% |
| squad_placement_2027.xlsx | 2 | 2 | 2 | 100% |

## Solver's path

1. Matched each change-log embedding to the squad's app tests in the archive by desk and calendar year. Test counts came out at 72/54/60/88/66/60/58, the same as tests_run. Average winning lift (zero where the control was kept) matched avg_winning_lift_pct. Realised/planned ratios run 0.70% to 2.55% and do not follow winning lift. They follow test sample size, which points to winner's curse.
2. From all 10,111 variant-vs-control comparisons in the archive I fitted a normal prior on relative lift by maximum likelihood, with SE from binomial CTRs: mu = -0.0104, tau = 0.0453. Each shipped variant's observed lift was replaced by its posterior mean, and a kept control counts as 0.
3. Calibration: planned clicks × mean posterior lift per test, with every app-desk click counted as testable (factor 1), reproduces all 7 realised_incremental_clicks within ±1.2%.
4. From the pageviews parquet (totals equal the 2027 plan, which holds every desk at Oct-25 to Sep-26) I took testable clicks as home_web + section_web + feed_app + section_app + related_links. Search, discover, partner_apps, social, newsletter and alerts were excluded because they carry the canonical headline.
5. Each desk's honest lift is the mean posterior lift over its own web-engine tests (Oct 2025 to Sep 2026). Extra clicks = testable clicks × that lift: LOC-M 2,792,947; BUS-N 1,726,554; CUL-N 1,369,906; SPT-N 1,297,878; POL-N 913,383; SPT-M 227,556. The dashboard-style lift would have favoured the large national desks and the noisy metro desks (SPT-M 10.8% raw against 0.39% shrunk).
6. Panel readers: each period took only the release the release log lists for it. R26-04H (new taxonomy) replaces Politics and Culture national for Nov 2025 to Feb 2026, and R26-07B replaces Apr to Jun 2026. I ignored R26-08's stale reload of Apr to Jun. Old section codes were used before Mar 2026 and new codes after. Then the 12-month average unique_audience per desk.
7. CMS corrections: a correction is a note text not seen before in the document, dated at its first live revision. Restored Brisbane copies were folded into their originals, and migrated documents' carried-over notes were dropped. It counts as a headline correction when the live headline changes within 10 minutes of the note (for a live blog, its post headline, or its own headline on the same save). Notes about a minister's 'title' are text corrections. This reproduces the April standards bulletin exactly: 11 headline and 22 text corrections in March 2026.
8. Articles are stories and live blogs that went live 1 Oct 2025 to 30 Sep 2026 AEST, excluding migrated documents, restored copies and documents withdrawn before publication. Go-live is the earlier of the first live save and the scheduled publish_at. Minutes to first headline correction run from go-live to the live save that published the corrected headline, with the median taken per desk.

confidence: Medium-high on the call: Local·metro leads the runner-up by more than 1M clicks under every prior I tried. Medium on the exact runner-up figure: Business·national at 1,726,554 sits close to the 1,725,000 rounding boundary. Medium on the correction medians, which move by up to 4 minutes depending on whether the correction time is the corrected-headline save or the note save.

notes: Not settled by the files: whether a live-blog post correction should be timed from the live blog's go-live or the post's (I used the live blog as the article). Whether related_links show the live headline is not stated; including them is what makes the app-desk calibration land at factor 1.

### squad_placement_2027.docx (solver's answers)
- Recommended desk and extra 2027 clicks: Local·metro (LOC-M): 2,800,000 extra article clicks in 2027 (nearest 50,000)
- Runner-up and gap: Runner-up Business·national (BUS-N), 1,750,000 extra clicks; gap to Local·metro 1,050,000 clicks (nearest 50,000)
- Chart walk, each desk from 2027 clicks to extra clicks, in order of extra clicks: Each row runs 2027 plan clicks, then clicks on headline-testable surfaces, then extra clicks (all nearest 50,000). LOC-M 114,750,000 / 108,700,000 / 2,800,000 (chosen). BUS-N 309,050,000 / 86,350,000 / 1,750,000 (runner-up). CUL-N 153,350,000 / 76,900,000 / 1,350,000. SPT-N 341,000,000 / 98,200,000 / 1,300,000. POL-N 376,250,000 / 71,400,000 / 900,000. SPT-M 104,650,000 / 57,800,000 / 250,000. The gap label between LOC-M and BUS-N reads 1,050,000. Title: 'Local·metro: squad adds about 2.8M clicks in 2027'

### squad_placement_2027.xlsx (solver's answers)
- Extra clicks 2027 per desk (nearest 50,000): LOC-M 2,800,000; BUS-N 1,750,000; CUL-N 1,350,000; SPT-N 1,300,000; POL-N 900,000; SPT-M 250,000 (POL-M, not shortlisted, 50,000)
- Average monthly readers, Oct 2025 to Sep 2026 (nearest thousand): LOC-M 617,000; BUS-N 1,760,000; CUL-N 1,412,000; SPT-N 2,931,000; POL-N 3,180,000; SPT-M 470,000 (POL-M 331,000)
- Extra clicks per reader (1 dp): LOC-M 4.5; BUS-N 1.0; CUL-N 1.0; SPT-N 0.4; POL-N 0.3; SPT-M 0.5 (POL-M 0.2)
- Headline corrections, 12 months to Sep 2026 (whole number): LOC-M 34; BUS-N 39; CUL-N 14; SPT-N 42; POL-N 47; SPT-M 18 (POL-M 14); 208 across all seven web desks
- Headline corrections per 1,000 articles (1 dp): LOC-M 4.9 (6,941 articles); BUS-N 4.9 (7,937); CUL-N 3.6 (3,883); SPT-N 3.8 (11,043); POL-N 5.2 (9,007); SPT-M 7.3 (2,463) (POL-M 4.4 on 3,186)
- Median minutes from going live to first headline correction (whole number): LOC-M 102; BUS-N 89; CUL-N 119; SPT-N 47; POL-N 86; SPT-M 55 (POL-M 78)
- Embeddings reproduced within 2 per cent: 7 of 7. Errors against realised clicks: +1.16%, +1.06%, +0.19%, +0.55%, -0.27%, -0.71%, -0.85%
