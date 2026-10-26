## Tags

**Domain:** Product Analytics (metric definition and measurement science).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Kleerwissel should adopt first purchase within 14 days (first_purchase_d14) as its 2027 proxy for six-month retention.**
Across the 489 past onboarding changes its effects correlate with the same changes' effects on retained_m6 at 0.54, against 0.31 for sessions in days 1 to 14, the runner-up. Not sessions (0.31) or active days (-0.09), whose measured effects move with retention's largely through the sampling error the two effects share on the same users. Not items saved (0.14) or push opens (0.02).

## 2. Critical Components

1. The correlations rest on **489** changes from **399** onboarding experiments.
2. Each candidate's correlation under the standard: first purchase **0.54**, sessions **0.31**, items saved **0.14**, push opens **0.02**, active days **-0.09**.

## 3. Step-by-Step Solution

1. Took from onboarding_experiments_2024_2026.csv the experiments started from 2024 whose six-month read closed by 23 October 2026, completed or stopped early, that passed the sample-ratio check (standard section 2): 399 experiments and 489 changes, each treatment arm against its control.
2. Read experiment_scorecards_2024_2026.csv at each arm and metric's latest computation, the former keys through metric_catalogue.yaml, and took each change's effect on each candidate and on retained_m6 (treatment mean less control mean), the experiment's measurement of the effect the standard correlates, and its sampling variance (each arm's variance over its users, summed).
3. Took each candidate's user-level correlation with retained_m6 among the 31,584 users of global_holdout_users_2025.csv (active days 0.54, sessions 0.46, first purchase 0.06, items saved 0.07, push opens 0.14) and set each change's sampling covariance between its two effects at that correlation times each arm's two standard deviations over its users, summed over the arms.
4. Correlated each candidate's effects with retention's across the 489 changes, each counted once, with the mean sampling covariance taken out of their covariance and the mean sampling variances out of their variances: first purchase 0.54, sessions 0.31, items saved 0.14, push opens 0.02, active days -0.09.
5. Calendar: took each ISO week's figure in new_user_forecast_2027.csv once (the tool writes a week's forecast on each of its days, as the guide's A2 holdout of about 430 a week confirms), set 3 per cent aside for the 2027 holdout, split each layer's users on a platform evenly among its experiments live that week on that platform and each experiment's users evenly among its arms (experimentation_platform_guide.pdf A2 to A4), and took 2.80 times each candidate's holdout standard deviation times the square root of two over the users per arm.
6. Holdout read: took the rows of signup_cohorts_2025.csv for accounts that signed up as consumers, those now business included, at their latest refresh, took the holdout's own users and sums out of each half's totals (the table counts every new consumer), and set each half's mean outside the holdout against the holdout's mean.
7. Named first purchase within 14 days, the highest correlation (0.54 against sessions' 0.31).

## 4. Deliverable Answers

### proxy_metric_scores_2027.xlsx

1. Proxy for 2027: first purchase within 14 days (first_purchase_d14).
2. Correlation with six-month retention under the standard:
   - First purchase within 14 days: 0.54
   - Sessions, days 1 to 14: 0.31
   - Items saved, days 1 to 14: 0.14
   - Push notifications opened, days 1 to 14: 0.02
   - Active days, days 1 to 14: -0.09
3. Past changes the correlations rest on: 489 (399 experiments).
4. First-quarter 2027 calendar, users per arm and the smallest effect a treatment arm can detect against its control:
   - OB-27-001: 24,786 users per arm; active days 0.093, sessions 0.132, first purchase 1.15 pp, items saved 0.051, push opens 0.063
   - OB-27-002: 6,749 users per arm; active days 0.179, sessions 0.253, first purchase 2.21 pp, items saved 0.098, push opens 0.121
   - OB-27-003: 17,353 users per arm; active days 0.112, sessions 0.158, first purchase 1.38 pp, items saved 0.061, push opens 0.075
   - OB-27-004: 30,936 users per arm; active days 0.084, sessions 0.118, first purchase 1.03 pp, items saved 0.046, push opens 0.056
   - OB-27-005: 9,644 users per arm; active days 0.150, sessions 0.212, first purchase 1.85 pp, items saved 0.082, push opens 0.101
   - OB-27-006: 23,571 users per arm; active days 0.096, sessions 0.136, first purchase 1.18 pp, items saved 0.053, push opens 0.065
   - OB-27-007: 10,845 users per arm; active days 0.141, sessions 0.200, first purchase 1.74 pp, items saved 0.078, push opens 0.095
5. 2025 new consumer users outside the global holdout less the holdout's users:
   - January to June: active days 0.040, sessions 0.060, first purchase 0.62 pp, items saved -0.010, push opens 0.034, six-month retention 0.62 pp
   - July to December: active days -0.032, sessions 0.147, first purchase 1.11 pp, items saved -0.032, push opens -0.022, six-month retention 1.69 pp

### proxy_metric_review_2027.pptx

1. Slide 1 names first purchase within 14 days as the 2027 proxy, 0.54 against sessions' 0.31.
2. Slide 2: bar chart of each candidate's correlation under the standard, first purchase highlighted.
3. Slides 4 and 5: the calendar's users per arm and detectable effects, and the 2025 holdout read, as in the workbook.
