## Tags

**Domain:** Product Analytics (feature adoption and diffusion modeling: a newsletter spotlight's stars on a code-hosting platform, built from the readers' own stars and the cascade they set off through their followers' home feeds at the rate each repository's feed cards convert once its launch week has passed).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Spotlight kilnkit (kilnworks/kilnkit) in the October 2026 issue of Sluis: it would have about 12,000 external stars in its first 90 days public, about 9,000 of them added by the spotlight.**
From its 8th day public on, about 1.8 per cent of the followers who see a kilnkit star in their feed star it too, against about 0.7 per cent for slidewell and 0.1 per cent for tracewire, so the October readers' stars set off far more feed stars for kilnkit, and slidewell and tracewire follow at about 10,000 each. Not slidewell on the rate its feed cards showed over its whole life, about 2.0 per cent, which spotlights it at about 14,000 by carrying its launch week's feed stars into a cascade that starts a month later: on the lottery's closed spotlights the rate from day 8 reproduces the stars each spotlight added to within a few hundred, where the whole-life rate misses by more than a thousand. Not the lottery's average spotlight lift added to each repository's own trajectory, which spotlights tracewire, the largest organic forecast, although the lottery's lifts follow each spotlighted repository's rate per follower view.

## 2. Critical Components

1. The October issue's own newsletter stars: about **3,000** (**0.71%** of the **433,812** subscribers on the October list).
2. Stars per follower view from the 8th day public: kilnkit about **1.8%**, slidewell about **0.7%** (about **2.0%** over its whole life, its launch week included).
3. Mean followers of the accounts that starred a spotlight from the newsletter about **85**, and of the accounts that starred from a feed card about **10**.
4. Without the spotlight kilnkit would have about **3,000** external stars by day 90; the spotlight adds about **9,000**.

## 3. Step-by-Step Solution

1. Counted each repository's external first stars by UTC day as section 2 of sluis_featuring_memo_2026-09.pdf defines them, from grachtwerk_star_events_2026-03-02_to_2026-09-27.csv with bots excluded by accounts_snapshot_2026-09-27.parquet and members at the time by organization_memberships_2026-09-27.csv, the seven being the October row of the 2026 sheet of sluis_spotlight_lottery_2025-2026.xlsx: kilnkit 1,523 by 27 September, slidewell 4,175, tracewire 4,534.
2. Forecast each repository's stars without the spotlight to day 90 as its stars to date plus its last seven days' daily pace times the ratio of stars still to come to that pace at the same age among the lottery's runners-up with complete windows (repo_daily_external_stars_2024-11-24_to_2026-09-27.csv): kilnkit 3,000.
3. Took the newsletter stars per subscriber over the 21 lottery issues (newsletter-surface external stars of each drawn repository in both event files, v5 codes mapped through star_surface_code_crosswalk_2026-03-02.csv, over the log's subscribers) times the October list: 0.71% of 433,812, about 3,000.
4. Measured each repository's stars per follower view from its 8th day public, its feed-card first stars from that UTC day over the summed followers of every account whose first star of it fell between that day and 27 September, and built its added stars as newsletter stars x (1 + rate x 85 / (1 - rate x 10)) with the mean followers of newsletter starrers over every spotlight (85) and of feed-card starrers over both event files (10): kilnkit 1.8% (356 feed-card stars over 19,548 followers) adding 9,000, slidewell 0.7% where its whole life gives 2.0%.
5. Tested the rate on the lottery spotlights whose 90 days had closed, their added stars (stars by day 90 less the step 2 forecast at the send) against step 4 at the issue's newsletter stars and each one's rate before the send: the rate from day 8 reproduces them to within a few hundred stars in root-mean-square terms, the whole-life rate misses by more than a thousand.
6. Spotlighted the largest total: kilnkit at 12,000 against slidewell and tracewire at 10,000 each.
7. For each issue counted the distinct subscribers whose own click, in any of its sends to the Sluis list, is on a link that reaches its spotlighted repository, by its owner/name address or by the permanent address /repositories/ with its id in repositories_2026-09-27.json that the opening paragraph's links use, leaving out mail gateways' fetches of every link of a message on delivery (four or more links within two seconds in relaymark_link_clicks_2026-06_to_2026-09.csv, one click on every link of the send in postwerk_link_report_2026-04_to_2026-05.csv), over the subscribers its two Tuesday batches were delivered to: April 6,699 of 391,299, September 7,317 of 429,949.
8. Matched each signed-out response in sluis_nominations_2026-10.csv to the account whose primary address it was when made, as accounts_snapshot_2026-09-27.parquet or a signed-in response of that account records it, and took a nominator as outside an organisation when none of their accounts was its member when they nominated, the accounts later merged into the one they nominated from included (merged_into, the spans in organization_memberships_2026-09-27.csv): kilnkit 22 of 27, tracewire 43 of 47.

## 4. Deliverable Answers

### sluis_spotlight_2026-10.xlsx

1. Spotlight: kilnkit (kilnworks/kilnkit), about 12,000 external stars in its first 90 days public, about 9,000 of them added by the spotlight.
2. Each shortlisted repository's expected external stars in its first 90 days public if spotlighted:
   - kilnkit: 12,000
   - slidewell: 10,000
   - tracewire: 10,000
   - shiftgres: 8,000
   - ferrolog: 8,000
   - hullcheck: 7,000
   - timeloom: 6,000
3. Sluis issues, subscribers who clicked through to the issue's spotlighted repository and their share of the subscribers it was delivered to:
   - April 2026 (calware-cloud/bryis): 6,699 subscribers; 1.71%
   - May 2026 (paulaha/awesome-home-automation): 7,031 subscribers; 1.76%
   - June 2026 (otto_kok/zig-toml): 7,169 subscribers; 1.76%
   - July 2026 (dalora-oss/orvum): 7,395 subscribers; 1.72%
   - August 2026 (yusufkuipers/minio-exporter): 7,090 subscribers; 1.65%
   - September 2026 (bruno-murphy29/rust-ratelimit): 7,317 subscribers; 1.70%
4. Shortlisted repositories owned by an organisation, the people who nominated it from outside the organisation when they nominated it and their share of the people who nominated it:
   - kilnkit (kilnworks): 22 people; 81.48%
   - tracewire (meridian-observe): 43 people; 91.49%
   - shiftgres (lindengracht-dev): 28 people; 90.32%
   - ferrolog (ferro-collective): 30 people; 81.08%
   - hullcheck (dokwerf-labs): 23 people; 88.46%

### shortlist_forecast_2026-10.png

5. Horizontal bar chart, one pair of bars per repository: the expected external stars in the first 90 days if spotlighted, split into the stars without the spotlight and those it adds (kilnkit highlighted at 12,000), beside the external stars by 27 September, to the nearest thousand: kilnkit 2,000, slidewell 4,000, tracewire 5,000, shiftgres 2,000, ferrolog 2,000, hullcheck 2,000, timeloom 1,000.
