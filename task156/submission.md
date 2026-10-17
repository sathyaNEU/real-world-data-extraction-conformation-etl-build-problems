## Tags

**Domain:** Product Analytics (retention, cohort and lifetime value modeling: a Q&A platform's volunteer reviewers as a retained-user cohort, each site's pool carried forward on its own lapse hazard with almost no new reviewers arriving, times the activity a retained reviewer delivers, seen only where work outran the pool).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The council should request 35 paid moderator FTE for 2027, 9 above finance's 26-FTE envelope: Frontend & Web 5, Mobile Apps 2, Data & ML 7, Databases 5, Infrastructure & DevOps 5, Game Development 2, Security 4, Embedded & Hardware 3 and Scientific Computing 2.**
Items reach the paid team only when the volunteers fall short, so each site's 2027 routed items are the inbox beyond what its shrinking reviewer pool can review at about 40 reviews a reviewer a month, which puts Data & ML, Databases, Infrastructure & DevOps and Game Development short of reviewers after routing almost nothing since January 2024. Not the last twelve months' paid hours per question carried onto the plan, which prices only what those sites routed while their pools still covered the inbox; not a trend in each site's routed share or paid hours, which extends the past and misses the months the pools fall below the inbox; and not a reviewer pace read from 2026 throughput, which on the covered sites measures how little work arrived rather than how much reviewers can do.

## 2. Critical Components

1. A volunteer reviewer completes about **40** reviews a month when the inbox outruns the site's pool, measured in the site-months in which more than 5 per cent of entering items reached the paid team.
2. Every site's reviewer pool loses about **2** per cent of its active reviewers a month, and almost no new reviewers have arrived since late 2024.
3. Data & ML, Databases, Infrastructure & DevOps and Game Development fall short of their inbox in 2027, joining Security, Embedded & Hardware and Scientific Computing; Frontend & Web and Mobile Apps stay covered.

## 3. Step-by-Step Solution

1. Stacked review_queues_monthly_2021-2023.xlsx (old site names through site_register.csv) with review_inbox_daily_2024-01-01_2026-09-30.csv and the active reviewers in reviewer_roster_2026-10-08.csv: over the site-months in which more than 5 per cent of entering items were routed to moderation, volunteer reviews over active reviewers give about 40 reviews a month.
2. In reviewer_roster_2026-10-08.csv, lapses over active reviewer-months from September 2024 to August 2026 give each site's monthly lapse rate, about 2 per cent on every site, and the last twelve months' new reviewers give each site fewer than one a month.
3. Carried each site's September 2026 active reviewers forward month by month at its lapse rate plus its new reviewers, at 40 reviews a reviewer a month, against the inbox of each month in 2027 (the questions in question_plan_2027.xlsx times the site's inbox items per question since January 2024), and routed the items beyond that capacity to the paid team (where a pool has room, the 0.6 per cent no volunteer picks up): Data & ML, Databases, Infrastructure & DevOps and Game Development fall short of their inbox.
4. Priced each site's handled flags per question since January 2024 (modtool_flag_summary_daily_2024-01-01_2026-09-30.csv) times the plan, and its routed items, at handle_time_standards_2027.pdf, and divided by the charter's 1,600 hours, each site to the nearest whole FTE: 35 FTE in all.
5. Against finance_envelope_2027_paid_moderation.pdf the request of 35 FTE is 9 above the 26-FTE envelope.

## 4. Deliverable Answers

### moderation_pool_2027.xlsx

1. 2027 need by site, whole FTE:
   - Frontend & Web: 5
   - Mobile Apps: 2
   - Data & ML: 7
   - Databases: 5
   - Infrastructure & DevOps: 5
   - Game Development: 2
   - Security: 4
   - Embedded & Hardware: 3
   - Scientific Computing: 2
2. Council request for 2027: 35 FTE.
3. Above finance's 26-FTE envelope by 9 FTE.
4. 24-hour flag response by site and month:
   - Frontend & Web: July 2026 97.9%, August 2026 97.0%, September 2026 97.1%
   - Mobile Apps: July 2026 97.2%, August 2026 96.4%, September 2026 96.3%
   - Data & ML: July 2026 97.8%, August 2026 97.3%, September 2026 97.4%
   - Databases: July 2026 97.1%, August 2026 97.5%, September 2026 96.4%
   - Infrastructure & DevOps: July 2026 98.0%, August 2026 96.8%, September 2026 96.7%
   - Game Development: July 2026 97.6%, August 2026 96.8%, September 2026 96.2%
   - Security: July 2026 91.8%, August 2026 89.3%, September 2026 88.1%
   - Embedded & Hardware: July 2026 91.4%, August 2026 87.7%, September 2026 87.1%
   - Scientific Computing: July 2026 85.6%, August 2026 90.0%, September 2026 81.4%
5. Hours each site's paid moderators worked:
   - Frontend & Web: Q1 2026 2,475 hours, Q2 2026 2,893 hours, Q3 2026 2,260 hours
   - Mobile Apps: Q1 2026 879 hours, Q2 2026 827 hours, Q3 2026 540 hours
   - Data & ML: Q1 2026 1,725 hours, Q2 2026 1,719 hours, Q3 2026 1,509 hours
   - Databases: Q1 2026 1,643 hours, Q2 2026 1,631 hours, Q3 2026 1,280 hours
   - Infrastructure & DevOps: Q1 2026 1,624 hours, Q2 2026 1,616 hours, Q3 2026 1,352 hours
   - Game Development: Q1 2026 751 hours, Q2 2026 622 hours, Q3 2026 535 hours
   - Security: Q1 2026 1,220 hours, Q2 2026 1,387 hours, Q3 2026 2,104 hours
   - Embedded & Hardware: Q1 2026 898 hours, Q2 2026 870 hours, Q3 2026 1,531 hours
   - Scientific Computing: Q1 2026 706 hours, Q2 2026 683 hours, Q3 2026 1,382 hours
6. January to September 2026 questions as a percentage of January to September 2022:
   - Frontend & Web: 39.7%
   - Mobile Apps: 42.1%
   - Data & ML: 55.5%
   - Databases: 58.4%
   - Infrastructure & DevOps: 60.2%
   - Game Development: 53.8%
   - Security: 72.0%
   - Embedded & Hardware: 76.0%
   - Scientific Computing: 76.8%

### council_pool_request_2027.pptx

7. Slide 1 states the request: 35 paid moderator FTE for 2027, 9 above the 26-FTE envelope, with each site's need.
8. Slide 2 charts the network's monthly paid review hours, as the operations notes define them, from January 2024 to December 2027, one stacked band per site, the forecast from October 2026 shaded, with finance's envelope drawn across at 3,467 hours a month (26 FTE); the plotted months are on the workbook's Monthly hours sheet.
