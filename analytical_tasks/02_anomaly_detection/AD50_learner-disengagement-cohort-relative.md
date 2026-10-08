# AD50 — Disengagement alerts: a quiet week before the exam is normal for everyone

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Customer-health and churn early-warning systems at SaaS and consumer-learning companies (usage drops relative to the customer's cohort and calendar) |
| Domain | Education technology / customer success |
| Task shape | 04 · Setting one dial (the cohort-percentile cut that defines an at-risk week, under the tutors' outreach capacity) |
| Core method | Weekly activity relative to the same module-presentation and week (within-cohort percentile rank); at-risk when ≥ 2 consecutive weeks below percentile q; evaluation against later withdrawal or failure with outreach capacity constraint; contrast with absolute-click thresholds |
| Analytical stump | Absolute activity thresholds fire for whole cohorts in reading weeks and after assessment deadlines and never fire for students whose activity fell from high to merely average. Engagement is meaningful relative to peers in the same course and week; persistence filters out one-off quiet weeks |
| Primary sources | Open University Learning Analytics Dataset (OULAD) |

## 1. The real-world situation

A distance-learning provider sends tutor outreach to students flagged as disengaging. The current alert fires when a student records
fewer than 20 virtual-learning-environment (VLE) clicks in a week. In some weeks it flags a third of a module's students; tutors can contact
at most **8%** of enrolled students per week.

## 2. The decision (one deterministic recommendation)

**The percentile cut q (grid 5–30, step 1) for the cohort-relative alert that maximises the share of eventual withdrawals or failures
flagged by week 10, subject to average weekly flags ≤ 8% of enrolled students.**

Rules (student-success memo):

* Data: OULAD `studentVle`, `studentInfo`, `studentRegistration`, `courses`; all module presentations.
* Week = floor(date ÷ 7) relative to presentation start; weeks 0–9 in scope; students active (registered, not yet unregistered) at the
  start of the week.
* Weekly clicks = Σ `sum_click`; percentile rank within module × presentation × week among active students (ties: average rank).
* Alert in week w: percentile < q in weeks w−1 and w (both active).
* Outcome positive: final_result Withdrawn or Fail.
* Metrics over weeks 1–9: weekly flag share (alerts ÷ active); recall = positives alerted at least once by week 9 ÷ positives.
* Choose q maximising recall with mean weekly flag share ≤ 8%; ties → smaller q.

## 3. Why capable analysts get it wrong

* Absolute thresholds are easy and ignore course design (different modules use the VLE very differently).
* Calendar effects (assessment weeks, breaks) move whole cohorts.
* One quiet week is common among successful students; persistence matters.
* Students who unregister early must leave the denominator.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `studentVle.csv` | CSV | ~10.6M | OULAD (Kuzilek et al., Scientific Data 2017) | CC BY 4.0 | Daily clicks per student and resource |
| 2 | `studentInfo.csv` | CSV | ~32.6k | OULAD | CC BY 4.0 | Outcomes, demographics |
| 3 | `studentRegistration.csv` | CSV | ~32.6k | OULAD | CC BY 4.0 | Registration and unregistration dates |
| 4 | `courses.csv` | CSV | 22 | OULAD | CC BY 4.0 | Presentations |
| 5 | `assessments.csv` | CSV | ~200 | OULAD | CC BY 4.0 | Deadlines (context) |
| 6 | `vle.csv` | CSV | ~6.4k | OULAD | CC BY 4.0 | Resource types (context) |
| 7 | `student_success_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `current_absolute_alerts.parquet` | Parquet | ~150k | Task author | — | Existing alerts |
| 9 | `weekly_clicks.parquet` | Parquet | ~300k | Derived | CC BY 4.0 | Convenience |
| 10 | `oulad_description.pdf` | PDF | — | Kuzilek et al. 2017 (cite) | CC BY 4.0 | Data description |

## 5. Deterministic solution path

1. Weekly clicks per active student; percentile ranks within cohort-week.
2. For each q, alerts with persistence; weekly flag shares; recall by week 9.
3. Choose q under the capacity constraint; contrast with the absolute rule.

## 6. Wrong paths (method errors, not misreadings)

**A — absolute click threshold.** Cohort-wide flags; capacity exceeded.

**B — percentiles across all modules.** Course design differences dominate.

**C — no persistence rule.** Flags exceed capacity.

**D — keeping unregistered students in denominators.** Flag shares understated.

## 7. Why the stump is analytical, not semantic

Weeks, ranks and the selection rule are specified. The trap is absolute versus cohort-relative baselines under a capacity constraint.

## 8. Draft task prompt (prose)

> Set the percentile cut for our cohort-relative disengagement alert following the student-success memo: it must stay within tutor capacity
> and catch as many eventual withdrawals and failures as possible by week 10. Provide `q_sweep.csv` (q: mean flag share, recall),
> `flag_share_by_week.png` (absolute rule vs chosen q by week), and a one-page `alert_setting.pdf`.

## 9. Deliverables

* `q_sweep.csv`, `flag_share_by_week.png`, `alert_setting.pdf`.

## 10. Where 25+ rubric criteria come from

* q; recall and flag share at 6 checkpoints; weekly shares for 9 weeks under the chosen q; absolute-rule shares; constraint check.

## 11. Golden-output checklist

* Week indexing; active denominators; within-cohort ranks; persistence; selection rule.

## 12. Build notes (scope tuning)

* Confirm the absolute rule exceeds 8% in at least four weeks and the constraint binds within the grid.
