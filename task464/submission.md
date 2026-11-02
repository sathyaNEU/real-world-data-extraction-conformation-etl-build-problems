## Tags

**Domain:** Product Analytics (churn, propensity and uplift modelling).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Drop the restart-your-alerts email from Quaywork's 2027 jobseeker email plan: its thirteen sends would cost about 300,000 sponsored clicks a year.** The pilot's sends brought back 100,000 clicks among the paused pool but cost 250,000 among jobseekers with alerts on at Google, Microsoft and Yahoo addresses. Not the holdout uplift carried forward, which counts only the paused pool and misses the clicks the sends cost everyone else.

## 2. Critical Components

1. The pilot's gain among the paused pool, mailed arm against the holdout, is **100,000** sponsored clicks.
2. The pilot's loss among jobseekers with alerts on, at Google, Microsoft and Yahoo addresses, is **250,000** sponsored clicks.
3. The pilot's net effect is **-150,000** sponsored clicks, and the 2027 series at the average send thirteen times is **-300,000** a year.

## 3. Step-by-Step Solution

1. Counted the 20 to 22 October 2026 reload in sponsored_clicks_by_mailbox_daily.csv once and summed app_ios and app_android into app.
2. Compared restart_pilot_mailed with restart_pilot_holdout clicks per jobseeker over the six 28-day windows from 14 April 2026 (0.178 against 0.034): the mailed arm gained 111,788 clicks.
3. Read each mailbox group's alerts_on clicks per jobseeker in the 14 days after each send against its own fortnight before: gmail, microsoft and yahoo_aol fall after every send, the other six groups do not.
4. Measured gmail, microsoft and yahoo_aol on every channel over days 0 to 13 after each send against the other six groups' pooled rate, at each group's ratio on days 14 to 27 of the window: 255,348 clicks lost.
5. Netted the two (-143,560 over the pilot), divided by six sends and multiplied by thirteen: -311,046 clicks a year in 2027.
6. Left out each restart whose RS-26xx email had four or more links clicked by the subscriber inside ten seconds in postvane_clicks_restart_series_2026.csv (a gateway's pass, 13,256 of 46,756 logged restarts).
7. Tied each logged-out app click in restarted_jobseekers_sponsored_clicks.csv to the one account its app_install_id carries there or in alert_restarts_pilot_pool_2026.csv, then counted restarters with a sponsored click, before or after restarting, dated in the 28 days starting on their send's date.
8. The series stays only if it adds sponsored clicks (jobseeker_email_plan_2027.docx, section 5); it costs them, so it is dropped.

## 4. Deliverable Answers

### restart_series_2027.xlsx

1. Recommendation: drop the restart series; the 2027 series would cost 300,000 sponsored clicks a year.
2. Gain among the paused pool over the pilot: 100,000 sponsored clicks.
3. Loss among jobseekers with alerts on over the pilot: 250,000 sponsored clicks, at Google, Microsoft and Yahoo addresses.
4. Net effect of the pilot: -150,000 sponsored clicks.
5. Each pilot send's restarts by people and, of them, those who clicked a sponsored job in the 28 days starting on the send's date, before or after restarting:
   - Send 1, 14 Apr 2026: 11,383 restarted, 6,180 clicked
   - Send 2, 12 May 2026: 6,758 restarted, 3,607 clicked
   - Send 3, 9 Jun 2026: 4,848 restarted, 2,631 clicked
   - Send 4, 7 Jul 2026: 3,910 restarted, 2,180 clicked
   - Send 5, 4 Aug 2026: 3,451 restarted, 1,865 clicked
   - Send 6, 1 Sep 2026: 3,150 restarted, 1,701 clicked

### restart_series_2027.docx

1. The recommendation to drop the restart series, the 2027 series costing 300,000 sponsored clicks a year.
2. One bar chart of each pilot send's restarts by people beside those who clicked a sponsored job in the 28 days starting on the send's date.
