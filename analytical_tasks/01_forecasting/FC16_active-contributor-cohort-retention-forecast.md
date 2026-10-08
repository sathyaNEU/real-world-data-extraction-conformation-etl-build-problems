# FC16 — Forecasting active users when the newest users churn fastest

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Social platforms forecasting DAU/MAU from acquisition and cohort retention curves (feed products, community platforms) |
| Domain | Consumer internet / community growth |
| Task shape | 02 · Forecast across many periods (12 monthly active-contributor forecasts → one committed annual planning level) |
| Core method | Cohort-component forecasting: monthly new-contributor inflow × cohort-age retention curves (by months since first activity), summed across cohorts |
| Analytical stump | Applying one aggregate month-over-month retention rate to the total treats every user alike. New users churn far faster than tenured ones, so when acquisition changes, the aggregate rate moves even if no cohort's behaviour changed — the aggregate model mis-forecasts |
| Primary sources | Wikimedia MediaWiki history dumps (editor activity), Wikimedia Statistics |

## 1. The real-world situation

A community platform's growth team forecasts **monthly active contributors** (users making ≥ 5 edits in a month) for the next
year to size moderation and support. The analyst applied the trailing 12-month average ratio "active this month ÷ active last
month" to the latest total, plus an assumed inflow of new contributors. The forecast drifted far from reality as a recruitment
campaign brought in many new — and quickly lapsing — contributors.

## 2. The decision (one deterministic recommendation)

**The committed planning level: the average monthly active contributors forecast for the next 12 months on the chosen wiki.**

Rules (growth memo):

* Activity: a user is active in month m if they made ≥ 5 edits (non-bot user accounts, all namespaces) in m. A user's cohort =
  the month of their first edit.
* Retention r(k) = share of a cohort active k months after its cohort month (k = 0…36), pooled over all cohorts from the 36
  months before the forecast origin that have reached age k: r(k) = Σ users active at age k ÷ Σ cohort sizes.
* New-cohort sizes for forecast months = the same calendar month of the previous year × (1 + g), with g in the memo (campaign
  plan).
* Forecast active(m) = Σ over all existing and future cohorts of cohort size × r(age at m); ages beyond 36 use r(36).
* Committed level = mean of the 12 monthly forecasts, rounded to the nearest 10.

## 3. Why capable analysts get it wrong

* Aggregate retention is one number and easy to communicate; it silently depends on the age mix of the user base.
* Recruitment campaigns raise the share of brand-new users and lower aggregate retention without any cohort behaving worse —
  and the next forecast then over-reacts.
* Retention curves must be pooled by age across cohorts, not averaged as unweighted rates of tiny cohorts.
* Bots and the "≥ 5 edits" threshold must be applied consistently to cohort sizes and actives.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–6 | `mediawiki_history_<wiki>_YYYY.tsv.bz2` (6 yearly files) | TSV | 1–20M events each | Wikimedia MediaWiki history dumps | CC BY-SA 4.0 | Edit events with user, timestamp, bot flags |
| 7 | `monthly_user_activity_<wiki>.parquet` | Parquet | ~2–5M user-months | Derived | CC BY-SA 4.0 | User × month edit counts |
| 8 | `wikistats_editors_<wiki>.json` | JSON | ~200 months | Wikimedia Statistics API | CC0 (metrics) | Published active-editor counts (reconciliation) |
| 9 | `mediawiki_history_dump_schema.pdf` | PDF | — | Wikimedia | CC BY-SA | Field definitions, bot groups |
| 10 | `campaign_plan.json` | JSON | — | Task author | — | Growth rate g by month |
| 11 | `growth_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 12 | `analyst_aggregate_forecast.xlsx` | XLSX | ~24 | Task author | — | Aggregate-ratio forecast |

## 5. Deterministic solution path

1. Build user × month activity; exclude bots; assign cohorts; compute actives and cohort sizes; reconcile with Wikistats.
2. Estimate pooled retention r(k) for k = 0…36 over the 36-month window.
3. Project existing cohorts forward; add future cohorts from the campaign plan; sum by month; compute the committed level.
4. Back-test both methods on the previous 12 months (origin shifted one year) for credibility.
5. Contrast with the aggregate-ratio forecast.

## 6. Wrong paths (method errors, not misreadings)

**A — aggregate retention ratio.** Wrong level and trajectory when inflow changes.

**B — unweighted average of cohort retention rates.** Small cohorts distort the curve.

**C — new users added without their steep early churn.** Overstates actives.

**D — bot accounts included.** Inflates tenured retention.

## 7. Why the stump is analytical, not semantic

Activity, cohorts and the projection rule are defined; the error is a compositional one — using an aggregate rate whose value
depends on the population's age mix.

## 8. Draft task prompt (prose)

> We need next year's planning level for monthly active contributors on our wiki, following the growth memo: retention by cohort
> age, new cohorts from the campaign plan, summed month by month. Provide `active_forecast.csv` (12 months: contributions from
> existing cohorts, from new cohorts, total), `retention_curve.png` showing pooled retention by months since first edit with the
> aggregate ratio overlaid, and a one-page `planning_memo.pdf` with the committed level, the back-test errors of both methods, and why
> the aggregate method misleads during campaigns.

## 9. Deliverables

* `active_forecast.csv`, `retention_curve.png`, `planning_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 monthly totals; r(0), r(1), r(3), r(12), r(36); committed level; back-test errors (2 methods); aggregate contrast.

## 11. Golden-output checklist

* Bot exclusion; threshold; pooled retention; cohort projection; campaign inflow; mean of 12 months.

## 12. Build notes (scope tuning)

* Pick a mid-size wiki where a campaign or event changed new-user inflow in the window; confirm the aggregate method's error exceeds
  10% in the back-test.
* State the bot-exclusion rule (user groups and name patterns) explicitly in the memo so cohort sizes are reproducible.
