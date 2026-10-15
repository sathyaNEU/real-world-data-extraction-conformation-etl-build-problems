## Tags

**Domain:** Product Analytics (feature adoption and diffusion modeling: a newsletter spotlight's stars on a code-hosting platform, built from the readers' own stars and the cascade they set off through their followers' home feeds at each repository's own rate per follower view).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Spotlight slidewell (pjvdlinden/slidewell) in the October 2026 issue of Sluis: it would have about 12,000 external stars in its first 90 days public, about 9,000 of them added by the spotlight.**
About 1.8 per cent of the followers who see a slidewell star in their feed star it too, against 0.1 per cent for tracewire, and each newsletter reader who stars reaches about 85 followers, so slidewell's spotlight sets off far more feed stars than anyone's and leaves tracewire second at about 9,000. Not the lottery's average spotlight lift added to each repository's own trajectory, which spotlights tracewire at about 11,000 with 5,000 added although the lottery's lifts follow each spotlighted repository's rate per follower view; not a lift carried on each repository's own share of stars from feed cards, which carries its own starrers' follower counts instead of the readers'.

## 2. Critical Components

1. The October issue's own newsletter stars: about **3,000** (**0.7236%** of the **433,812** subscribers).
2. Stars per follower view, feed-card stars over the followers of every account that starred the repository: slidewell **1.8%**, tracewire **0.1%**.
3. Mean followers of the accounts that starred a spotlight from the newsletter **85**, and of the accounts that starred from a feed card **10**.
4. Without the spotlight, by day 90: slidewell **3,000**, tracewire **6,000**; the spotlight adds slidewell **9,000** and tracewire **3,000**.

## 3. Step-by-Step Solution

1. Read the estimand in section 2 of sluis_featuring_memo_2026-09.pdf: the shortlisted repository with the most expected external stars in its first 90 days public if it is the issue's spotlight, external stars and the window as that section defines them, stars not yet made counted; the seven are the October row of the 2026 sheet of sluis_spotlight_lottery_2025-2026.xlsx.
2. Counted each repository's external first stars by UTC day from grachtwerk_star_events_2026-03-02_to_2026-09-27.csv, bots excluded by accounts_snapshot_2026-09-27.parquet and members at the time by organization_memberships_2026-09-27.csv: slidewell 2,766 by 27 September, tracewire 3,876.
3. Forecast each repository's stars without the spotlight to day 90 as its stars to date plus its last seven days' daily pace times the ratio of stars still to come to that pace at the same age among the lottery's runners-up with complete windows (repo_daily_external_stars_2024-11-24_to_2026-09-27.csv): slidewell 3,000, tracewire 6,000.
4. Took the newsletter stars per subscriber over the 21 lottery issues (newsletter-surface external stars of each drawn repository in both event files, v5 codes mapped through star_surface_code_crosswalk_2026-03-02.csv, over the log's subscribers) times the October list: 0.7236% of 433,812, about 3,000.
5. Measured each repository's stars per follower view as its feed-card stars over the summed followers of every account that starred it by 27 September: slidewell 1.8%, tracewire 0.1%.
6. Took the mean followers of newsletter starrers over every spotlight (85) and of feed-card starrers over both event files (10), and built each repository's added stars as newsletter stars x (1 + rate x 85 / (1 - rate x 10)), every star shown to its starrer's followers in turn: slidewell 9,000, tracewire 3,000.
7. Spotlighted the largest total: slidewell at 12,000 against tracewire at 9,000.

## 4. Deliverable Answers

### sluis_spotlight_2026-10.xlsx

1. Spotlight: slidewell (pjvdlinden/slidewell), about 12,000 external stars in its first 90 days public, about 9,000 of them added by the spotlight.
2. Each shortlisted repository's expected external stars in its first 90 days public if spotlighted:
   - slidewell: 12,000
   - tracewire: 9,000
   - ferrolog: 8,000
   - shiftgres: 8,000
   - kilnkit: 7,000
   - hullcheck: 7,000
   - timeloom: 6,000
3. Sluis issues, subscribers delivered to and the share of them who clicked through to the issue's spotlighted repository:
   - April 2026 (calware-cloud/bryis): 391,299 subscribers; 1.49%
   - May 2026 (paulaha/awesome-home-automation): 399,160 subscribers; 1.52%
   - June 2026 (otto_kok/zig-toml): 406,891 subscribers; 1.53%
   - July 2026 (dalora-oss/orvum): 429,444 subscribers; 1.52%
   - August 2026 (yusufkuipers/minio-exporter): 429,291 subscribers; 1.44%
   - September 2026 (bruno-murphy29/rust-ratelimit): 429,949 subscribers; 1.49%
4. People who nominated each shortlisted repository and, for those owned by an organisation, the share of them outside it:
   - slidewell: 58 people (owned by a user)
   - tracewire: 47 people; 91.49% outside meridian-observe
   - ferrolog: 37 people; 81.08% outside ferro-collective
   - shiftgres: 31 people; 90.32% outside northbeam
   - kilnkit: 27 people; 81.48% outside kilnworks
   - hullcheck: 26 people; 88.46% outside dokwerf-labs
   - timeloom: 19 people (owned by a user)

### shortlist_forecast_2026-10.png

5. Horizontal bar chart, one pair of bars per repository: the expected external stars in the first 90 days if spotlighted (slidewell highlighted at 12,000) beside the external stars by 27 September, to the nearest thousand: slidewell 3,000, tracewire 4,000, ferrolog 2,000, shiftgres 2,000, kilnkit 1,000, hullcheck 2,000, timeloom 1,000.
