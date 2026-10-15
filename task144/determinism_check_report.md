# Verdict, task144 (Sluis spotlight, October 2026)

- **Verdict:** DETERMINISTIC. (No SOLUTION_WRONG: every golden figure I checked reproduced.)
- **Disposition:** APPROVE. One optional in-house tidy of the memo's tense (see Files/Hygiene). No analytic surface changes, no rerun.

## Why
The memo (s2.1 to 2.4) fixes the estimand: most expected external stars by end of day 90 if spotlighted, every surface counts. The 21-issue lottery log is a randomised draw of 1 of 7, so the drawn repository against its 6 runners-up gives a clean spotlight lift. That lift is not a constant: lift per newsletter star tracks each repository's feed-star rate per follower of its starrers (r = 0.995). The mean-lift route gives tracewire (about 9.8k to 11k). The route the data validates gives slidewell (about 12.0k against tracewire about 9.1k). The pick (slidewell) holds under every rate-based estimator I tried. The call is forced and the main answer is analytical.

## Evidence (recomputed from target/)
| Item | Golden | Mine | Source |
|---|---|---|---|
| External stars to 27 Sep (7 repos) | tracewire 3,876; slidewell 2,709; ferrolog 1,892; shiftgres 1,826; kilnkit 1,245; hullcheck 1,912; timeloom 1,299 | identical, rebuilt from v5+v6 events (crosswalk, bots, membership-at-time, merges, first-star) and equal to the rollup for all 28 repos in the events files | events csvs, accounts parquet, memberships, rollup |
| No-spotlight day-90 baseline | slidewell 3,000; tracewire 6,000 | 3,050; 5,723 (stars to date + 7-day pace x mean runner-up ratio, 119 complete runners-up, ratio about 5.8, sd about 0.9) | rollup |
| Newsletter stars per subscriber | 0.7236% of 433,812 = about 3,000 | pooled 0.72361%; per-issue mean 0.7249%, median 0.7189%; Oct = 3,139 (3,119 to 3,145) | events, lottery log |
| Feed-card stars per follower of starrers | slidewell 1.8%; tracewire 0.1% | 1.801%; 0.098% | events + snapshot followers |
| Mean followers of newsletter / feed starrers | 85 / 10 | 84.98 / about 10.2 | same |
| Cascade check on the 21 lottery lifts | n/a | lift/newsletter-star vs 1+r*85/(1-r*10): corr 0.997, RMSE 0.042 (sd 0.56) | rollup + events |
| Expected 90-day stars if spotlighted | 12k / 9k / 8k / 8k / 7k / 7k / 6k | cascade 12,047 / 9,127 / 8,160 / 7,983 / 7,099 / 7,110 / 5,893; linear regression of lift on rate gives 11,908 / 8,985 / 8,183 / 7,966 / 7,178 / 7,061 / 5,827. Same rounding in all seven cases. | |
| Added by spotlight | slidewell 9k; tracewire 3k | 8,997 / 3,404 (regression 8,858 / 3,262) | |
| Sheet 3: Postwerk Apr / May | 391,299, 1.49% / 399,160, 1.52% | delivered = the two split sends (the 3rd-day resend is not added); unique spotlight + image clickers 5,825 and 6,075, reproduced | postwerk csvs |
| Sheet 3: Relaymark Jun to Sep | 406,891, 1.53% / 429,444, 1.52% / 429,291, 1.44% / 429,949, 1.49% | reproduced. The repo is the `feature` + `feature_cta` tags (URL = drawn repo); tag `spotlight` points to the previous month's repo. | relaymark json + clicks |
| Sheet 4: nominators | 47, 58, 31, 27, 26, 19, 37; outside-org 91.49, 90.32, 81.48, 88.46, 81.08 (slidewell and timeloom user-owned) | reproduced exactly (urls and case normalised, old names via renames, bare names mapped to the shortlist, signed-in and typed-email hashes unified, merged accounts to survivor; membership as at snapshot or nomination gives the same) | nominations, accounts, memberships |
| png values | 3k, 4k, 2k, 2k, 1k, 2k, 1k | match the rounded to-date stars | |

**Competing answers tested.**
- Tracewire via average lift added to each trajectory: wrong. The lottery shows the lift is heterogeneous and tracks rate. Out-of-sample (leave-one-out) RMSE of lift per newsletter star on rate is 0.06, on feed share 0.21, on raw feed stars 0.26. Feed-share lift would give tracewire about 9.3k and slidewell about 6.1k.
- Newsletter stars only (about 3.1k added): contradicted by memo 2.2 ("whichever surface") and by the lottery, whose lifts are 1.1x to 2.6x the newsletter stars.
- First-order cascade without the second term (1+85r): slidewell 11.0k and 7.9k added, RMSE 0.137 against 0.042. The data separates it from the golden, so it is a worse method and not a live fork. A nonparametric 3-NN extrapolation gives about 8.2k added and 11.3k total, but slidewell's rate (0.0180) is above every lottery repository (max 0.0156), so a linear or mechanistic fit is the only sound route.
- Other readings of the rates (pooled, mean or median newsletter rate; mean or median baseline ratio): all keep the rounded figures.

**Residual fragility (not blocking, Gate C thin-but-clean).**
- Slidewell's 12k/9k rest on a rate from only 160 feed stars (rate sd about 8%). A one-sigma lower rate puts the total at about 11.5k, on the rounding line. The pick is unaffected (tracewire stays below 9.5k). The point-estimate method every validated estimator uses gives 12k and 9k.
- Sheet 4: 173 nominations are in bare or other-owner form. Bare names (`tracewire`, `kiln-ui`, `imagelint`) are mapped to the shortlist; look-alike owners (`jorisprins/shiftgres`, `lottekuip/tracewire`) are treated as other repositories. Without the bare names the counts fall to 44/58/29/22/23/18/37. The shortlist-mapping is the natural reading but is not stated anywhere in the files. Sheet 4 is a supplementary ask and does not touch the main call.

## Files/Hygiene
**PASS.** 19 files; formats parquet, csv (several), json, pdf, xlsx, md. 110k-row click log, 119k-row snapshot and 169k event rows.
- Distractors present: trending, traffic, renames, product-news campaigns.
- Realistic: semicolon, BOM and Amsterdam-time exports, Dutch link labels, test sends, split sends plus resend.
- No README or benchmark disclosure. xlsx and pdf metadata are in-fiction.
- Minor temporal slip, in-house fix: memo dated 15 Sep (s3.1 to 3.3) states the 20 Sep and 23 Sep closings and the 27 Sep extract in the past tense. The lottery log (extracted 24 Sep) notes a pick "locked 30 Sep". Reword to future or planned tense. This changes no number.
- Layer 1 mess is not planted: v5/v6 schemas, ms epoch vs ISO, UTC days, merged accounts, renames.
- Repository names are plausibly synthetic; no contamination (no public canonical answer).
- Not exclusion-level.

## Stump power (Gate F)
Strong. The mean-lift route, the newsletter-only route and the feed-share route each give a specific wrong pick (tracewire, or kilnkit and tracewire). Slidewell looks weakest on every surface figure (low baseline, 59 stars/week, 8,883 follower-views) and its advantage appears only after modelling exposure. A strong model that averages the lottery lift fails. No shipped artifact ranks the seven and gets it wrong. The memo's "whichever surface" sentence is the only pointer and does not name the mechanism.

## Stumping type (Gate G)
`mechanism: method_or_model_selection` (forecasting with heterogeneous treatment effect), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
All reported numbers (rollup, log, lifts) are correct and nothing is a defect to catch. The difficulty is choosing the exposure-based lift model, validated on the randomised lottery. On perfectly clean data the task still stumps.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: audience-growth forecasting and treatment-effect estimation from a randomised promotion with network spillover. This is quantity a growth analyst would estimate, and swapping "stars" for another event does not change the method.
- Layer 1: schema v5/v6 with surface-code crosswalk, ms vs ISO timestamps, bot and membership-at-time exclusion, merged accounts and renames, split sends plus resend, Dutch/UTC times, free-text nomination keys.
- Layer 2: lift heterogeneity by follower exposure, validated on the lottery as a natural experiment, plus a day-90 forecast calibrated on runners-up.
- Easy route: a strong analyst who cleaned everything and read memo 2.2 correctly adds the lottery's average lift (about 4k to 5k) to each baseline. That files tracewire at 10k to 11k.

## Fix
none. Optional (input_files, in-house): reword the memo's section 3 tense. Optional (prompt or sheet 4): if bare-name nominations should be unambiguous, state in the nominations file note that a name without owner refers to the shortlisted repository. Not required for determinism of the main call.

## Repairs after this verdict (2026-10-15, re-judge pending)

The verdict above was given on the pack cut as target.zip 224ba2c1. Its points were repaired in one generator pass:
- Rate evidence: slidewell's launch audience now has about 11 followers per starrer, so its per-view rate rests on 551
  feed stars instead of 160. A one-sigma move in any repository's rate keeps every rounded figure; slidewell moves
  11,669 to 12,283, adding 8,713 to 9,327. At two sigma (slidewell's rate low, every other rate high) slidewell still
  leads, 11,370 against 9,147. Both are asserted in checks.py. The golden is slidewell 11,973, adding 9,017
  (12,000 and 9,000).
- Sheet 4: the nomination form keeps only references that resolve on the host (stated once in the field notes), so no
  reference is a bare name. Every signed-out nominator of the shortlist resolves to an account, and membership when
  nominating equals membership now. All three are asserted, and the counts are unchanged (47, 58, 31, 27, 26, 19, 37).
- Memo: section 3 now gives the 20 and 23 September closings, the 27 September extract and the 30 September meeting
  as planned dates. The lottery log's October note reads as a plan.
- Names: repository, owner, login and rename names were regenerated after the leak reader's realism note. No figure
  depends on a name.
