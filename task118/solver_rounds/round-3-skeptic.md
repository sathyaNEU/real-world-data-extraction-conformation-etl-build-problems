# solver round: round 3, skeptic

**Proxy score 36.8 / 100** (recommendation 0.0 of 35, instruction 7.0 of 7, asks 29.8 of 58). Main call missed. 1 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.

solver: The squad should join Local·metro (LOC-M) in January 2027, where it would add about 2,400,000 extra article clicks in 2027 (unrounded 2,419,628). That is 108,693,347 headline-surface clicks times a shrunk average lift of 2.23% per test. The runner-up is Business·national at about 1,750,000 (unrounded 1,726,554), 700,000 behind (unrounded gap 693,074). Politics·national leads on readers and on the dashboard's raw lift but would add only about 900,000.

tokens matched 0 of 3 (1,250,000, Place, Culture)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| squad_placement_2027.docx | 1 | 0 | 2 | 0% |
| squad_placement_2027.docx | 2 | 2 | 4 | 50% |
| squad_placement_2027.docx | 3 | 1 | 3 | 33% |
| squad_placement_2027.xlsx | 1 | 36 | 49 | 73% |
| squad_placement_2027.xlsx | 2 | 2 | 2 | 100% |

## Solver's path

1. Read the prompt, brief, thread, field reference, CMS field notes, standards s7, the bulletin, the panel workbook, the plan, the change log and the dashboard export. Dashboard average winning lift (Politics 4.69%) and panel readers both point to Politics·national; I treated both as the views being argued against, not as the method.
2. Headline test archive (14,131 packages, 4,020 tests): computed each variant's lift against its control (CTR ratio minus 1) and a delta-method standard error. Fitted a normal prior to all 10,111 variant packages by maximum likelihood: mean -1.038%, SD 4.533%. Each package's posterior-mean (shrunk) lift = mu + tau^2/(tau^2+se^2)*(lift-mu).
3. Found the squad's shipping rule from the archive: the highest-CTR variant with pooled z >= 1.645 against control, otherwise keep the control. This matches 100% of app (squad) tests and all national-desk tests. The metro desks ship non-significant top variants, so I reapplied the squad's rule to every desk's tests.
4. Back-test: for each embedding in the change log, realised = planned_clicks x mean over that calendar year's squad tests of the shrunk lift of the package the rule ships (zero when the control is kept). Calendar-year test counts and average lifts reproduce the log (72/3.0, 54/3.1, 60/2.9, 88/3.7, 66/2.7, 60/2.9, 58/3.2). All 7 predictions land within 2% (max 1.16%). The raw measured lift overstates by 35-75%, and an app-only or method-of-moments prior fails the back-test.
5. Addressable clicks: the canonical headline is the one carried in partner apps, search, discover, social, newsletters and alerts, so only home_web, section_web, feed_app, section_app and related_links carry the tested headline. For app desks that is 100% of clicks, consistent with the back-test multiplier of 1. Applied the shares from the pageviews parquet (desk totals equal audience_plan_2027 P2) to the 2027 plan clicks.
6. 2027 extra clicks = headline-surface clicks x the desk's mean shrunk squad-rule lift over its 12 months of web tests: LOC-M 108.69M x 2.226% = 2,419,628; BUS-N 86.35M x 1.999% = 1,726,554; CUL-N 1,369,906; SPT-N 1,297,878; POL-N 913,383; SPT-M 119,343; POL-M 47,728. Rounded to the nearest 50,000; gap computed on unrounded figures = 693,074, rounded to 700,000.
7. Panel readers: took the latest release per period (R26-04H replaces Nov-Feb; R26-07B replaces Apr-Jun) and mapped section codes by release taxonomy (old 2024 codes only for the R25-11 Oct 2025 release; 2026 codes for R26-04 onward, including the history release). Averaged unique_audience over the 12 months per desk and divided extra clicks by it.
8. CMS revisions: merged restored Brisbane docs into their originals and dropped their copy revision. Built the published sequence (live saves at saved_at; scheduled revisions at publish_at only if no later save came first, which drops 534 withdrawn-before-publish docs and superseded schedules). A headline correction is a published revision that adds new correction-note text and changes headline_sha1 against the previous published revision, plus live-blog entry notes matched to a post headline change in the same minute (16). This reproduces the bulletin's March 2026 figures exactly: 11 headline and 22 text corrections (AEST). Articles = live stories plus live blogs first live in the window, excluding migrated and withdrawn docs, which matches the pageview article counts exactly. Median = minutes from the corrected item's first going live to its first headline correction.

confidence: The main call (Local·metro, 2,400,000) holds across every prior that passes the back-test, as do the gap of 700,000 and the per-reader, corrections and readers figures. One figure is fragile: Business·national's unrounded figure (1,726,554) sits just above the 1,725,000 rounding boundary. A rounded prior (-1.0%, 4.5%) gives 1,724,474, which rounds to 1,700,000. Medium-high overall.

notes: The source does not settle whether a live-blog entry's headline correction counts toward the live blog (I counted it, timed from the post going live). March has no such cases, so the bulletin cannot test that choice. Without them the counts are POL-N 44, SPT-N 38, BUS-N 36, LOC-M 32, SPT-M 16, CUL-N 13. Politics·metro is not on the shortlist; its figures are given in brackets only.

### squad_placement_2027.docx (solver's answers)
- Recommended desk: Local·metro (LOC-M)
- Extra article clicks at the chosen desk in 2027: 2,400,000 extra clicks, to the nearest 50,000 (unrounded 2,419,628)
- Runner-up desk and its extra clicks: Business·national (BUS-N), 1,750,000 extra clicks, to the nearest 50,000 (unrounded 1,726,554)
- How far the runner-up sits behind: 700,000 clicks, to the nearest 50,000 (unrounded 693,074)
- Chart walk, 2027 clicks to headline-surface clicks to extra clicks, in order of extra clicks: LOC-M 114,737,642 -> 108,693,347 -> 2,400,000; BUS-N 309,052,180 -> 86,354,201 -> 1,750,000; CUL-N 153,340,236 -> 76,918,315 -> 1,350,000; SPT-N 340,990,504 -> 98,219,774 -> 1,300,000; POL-N 376,236,959 -> 71,403,123 -> 900,000; SPT-M 104,669,888 -> 57,786,909 -> 100,000. Title names Local·metro; gap label 700,000

### squad_placement_2027.xlsx (solver's answers)
- Extra clicks 2027 per desk (nearest 50,000): Local·metro 2,400,000; Business·national 1,750,000; Culture·national 1,350,000; Sport·national 1,300,000; Politics·national 900,000; Sport·metro 100,000 (Politics·metro, not shortlisted: 50,000)
- Average monthly readers, Oct 2025 to Sep 2026 (nearest thousand): Politics·national 3,180,000; Sport·national 2,931,000; Business·national 1,760,000; Culture·national 1,412,000; Local·metro 617,000; Sport·metro 470,000 (Politics·metro 331,000)
- Extra clicks per reader (1 dp): Local·metro 3.9; Business·national 1.0; Culture·national 1.0; Sport·national 0.4; Politics·national 0.3; Sport·metro 0.3 (Politics·metro 0.1)
- Headline corrections, 12 months to Sep 2026 (whole number): Politics·national 47; Sport·national 42; Business·national 39; Local·metro 34; Sport·metro 18; Culture·national 14 (Politics·metro 14)
- Headline corrections per 1,000 articles (1 dp): Sport·metro 7.3; Politics·national 5.2; Business·national 4.9; Local·metro 4.9; Sport·national 3.8; Culture·national 3.6 (Politics·metro 4.4). Article counts: POL-N 9,007; SPT-N 11,043; BUS-N 7,937; LOC-M 6,941; SPT-M 2,463; CUL-N 3,883; POL-M 3,186
- Median minutes from going live to first headline correction (whole minutes): Business·national 79; Culture·national 79; Local·metro 71; Politics·national 69; Sport·metro 55; Sport·national 42 (Politics·metro 66)
- Back-test line: finished embeddings within 2% of what each actually added: 7 of 7 (predicted vs realised: 678,285 vs 670,475 (+1.2%); 328,528 vs 325,071 (+1.1%); 1,066,718 vs 1,064,693 (+0.2%); 1,065,594 vs 1,059,784 (+0.5%); 271,715 vs 272,464 (-0.3%); 528,309 vs 532,067 (-0.7%); 665,181 vs 670,864 (-0.8%))
