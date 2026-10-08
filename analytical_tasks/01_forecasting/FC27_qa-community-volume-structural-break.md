# FC27 — Planning moderation after an AI shock: forecasting from the new regime, not the old one

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Q&A, homework-help and search-traffic businesses whose demand broke after generative-AI launches |
| Domain | Online communities / trust & safety staffing |
| Task shape | 17 · Periods around a change point (months before/after the break against a committed baseline; longest shortfall run; go/no-go and the staffing amount it frees) |
| Core method | Pre-break seasonal-trend baseline, month-by-month comparison after the break, break confirmation by run length, and a post-break-only re-estimated forecast for the planning year |
| Analytical stump | Year-over-year growth or a model fitted across the break averages two regimes; seasonality estimated with post-break months under-states the new level's seasonal amplitude; a single bad month is not a regime — the run rule matters |
| Primary sources | Stack Exchange data dump (posts), Stack Exchange Data Explorer exports |

## 1. The real-world situation

A developer Q&A community staffs its review queues with paid community managers in proportion to new questions. After late 2022,
question volume fell. Finance proposed cutting staff; the community lead argued the drop was seasonal and temporary. The staffing
model used next year = this year × last year's growth rate.

## 2. The decision (one deterministic recommendation)

**Go / no-go on reducing review staffing for 2025, and the FTE reduction the post-break forecast supports.**

Rules (community operations memo):

* Series: monthly new questions on the main site (non-deleted at dump time and deleted, both counted — the dump's post history
  supplies deleted counts per the memo), January 2015 – December 2024.
* Baseline: OLS on ln(questions) with month effects and a linear trend, fitted on January 2018 – November 2022; projected forward.
* A post-break month is in shortfall if actual < baseline × 0.85. The break is confirmed if the longest run of consecutive shortfall
  months starting from December 2022 is ≥ 6.
* If confirmed: re-fit the same model on December 2022 – December 2024 only (month effects constrained to the pre-break seasonal
  shape, re-estimated level and trend), forecast 2025; FTE = Σ 2025 forecast questions ÷ 1,400 questions per FTE-month ÷ 12,
  compared with the current 2024 FTE level (Σ 2024 actual ÷ 1,400 ÷ 12). Reduction = difference, rounded down to whole FTE.
* If not confirmed: no reduction.

## 3. Why capable analysts get it wrong

* Growth-rate budgeting carries the old regime forward.
* A model fit through the break splits the difference between regimes.
* Seasonal factors from a short post-break window are noisy; constraining shape while re-estimating level is the stated rule.
* One or two weak months can be noise; the run rule protects against overreaction.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `stackoverflow.com-Posts.7z` (subset: questions, 2015–2024) | XML | ~25M questions | Stack Exchange data dump (archive.org) | CC BY-SA 4.0 | Question creation dates |
| 2 | `monthly_questions_2015_2024.csv` | CSV | 120 | Derived | CC BY-SA 4.0 | Monthly series |
| 3 | `sede_deleted_questions_monthly.csv` | CSV | 120 | Stack Exchange Data Explorer export | CC BY-SA 4.0 | Deleted questions (per memo) |
| 4 | `monthly_questions_by_tag_top50.parquet` | Parquet | ~6k | Derived | CC BY-SA 4.0 | Context |
| 5 | `stackexchange_dump_readme.pdf` | PDF | — | Stack Exchange | CC BY-SA | Schema |
| 6 | `event_timeline.json` | JSON | ~10 | Public announcements (dates only) | Public | Break date |
| 7 | `community_operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `finance_growth_rate_plan.xlsx` | XLSX | 12 | Task author | — | Growth-rate staffing plan |
| 9 | `review_queue_productivity.json` | JSON | — | Task author | — | 1,400 questions per FTE-month |
| 10 | `sede_query_definitions.sql` | SQL | — | Task author | — | Queries used for exports |

## 5. Deterministic solution path

1. Build the monthly series; fit the pre-break baseline; compute shortfall flags for December 2022 onward; longest run.
2. If confirmed, re-fit on the post-break window with constrained seasonal shape; forecast 2025; compute FTE reduction.
3. Contrast with growth-rate and through-the-break models.

## 6. Wrong paths (method errors, not misreadings)

**A — growth-rate plan.** Staffing kept at old-regime levels.

**B — model across the break.** Level mid-way between regimes.

**C — unconstrained post-break seasonality.** Noisy monthly forecasts.

**D — reacting to a single month.** Ignores the run rule.

## 7. Why the stump is analytical, not semantic

Series, baseline, shortfall threshold, run rule and productivity are defined. The trap is regime handling in forecasting — which
data window describes the future.

## 8. Draft task prompt (prose)

> Finance wants to cut review staffing for 2025 and the community lead thinks the drop is temporary. Using the question data and
> the operations memo in the folder, test month by month whether volume broke from its pre-2023 pattern, and if it did, forecast 2025
> from the new regime and tell me the FTE reduction. Provide `break_test.csv` (month, actual, baseline, shortfall flag, run length),
> `break_chart.png` with the baseline, the 15% band, actuals and the 2025 forecast, and a one-page `staffing_decision.pdf` with the
> go/no-go and the reduction.

## 9. Deliverables

* `break_test.csv`, `break_chart.png`, `staffing_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 25 post-break monthly flags; run length; 12 monthly 2025 forecasts; decision; FTE reduction; contrasts.

## 11. Golden-output checklist

* Counting rule; baseline window; threshold; run rule; constrained re-fit; FTE arithmetic.

## 12. Build notes (scope tuning)

* Decide and document how deleted questions are counted (dump vs SEDE) and keep it fixed.
* Confirm the growth-rate plan implies ≥ 3 more FTE than the correct forecast.
