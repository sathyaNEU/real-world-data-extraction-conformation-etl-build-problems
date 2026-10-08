# FC44 — Staffing tax-season support: align seasons by opening day, not by calendar week

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Seasonal support staffing for consumer software and fintech (tax preparation, payroll year-end, retail holiday peaks) |
| Domain | Customer operations / workforce management |
| Task shape | 06 · Sequenced schedule under capacity (four hiring cohorts, training lead time, cohort size limits) |
| Core method | Event-aligned seasonal profiles (weeks since season opening, with the refund-release milestone), forecast of weekly volumes, conversion to agent requirements, cohort scheduling against requirements |
| Analytical stump | The filing season opens on a different date each year; averaging by ISO week blurs and shifts the opening surge and the refund-release surge. The profile must be built in event time and re-anchored to next season's dates |
| Primary sources | IRS Filing Season Statistics (weekly), IRS season-opening announcements |

## 1. The real-world situation

A tax-software company staffs its support centre from a forecast of weekly self-prepared e-filed returns. The workforce team
averaged the past three seasons by calendar week. Last season opened a week later than the year before; the surge arrived after
agents' training had ended and the second (refund-release) wave was under-staffed.

## 2. The decision (one deterministic recommendation)

**Start weeks for four hiring cohorts for the 2026 season (and the resulting weekly coverage).**

Rules (workforce memo):

* Data: IRS weekly cumulative self-prepared e-file receipts for the 2023, 2024 and 2025 seasons; weekly volume = difference of
  cumulative values.
* Event time: week k = 1 is the week containing the season opening date; a second anchor is the week containing the earliest refund
  release date for EITC/ACTC claims (from IRS announcements).
* Profile: for k = 1…14, average weekly volume share (volume ÷ season total through week 14) across the three seasons in event time,
  with weeks around the refund anchor aligned by the memo's two-anchor rule.
* 2026 forecast: profile × 2025 total through week 14 × 1.04, placed on the 2026 calendar using the announced opening date.
* Requirement: agents = ceil(volume × contact rate 0.012 × 9 minutes ÷ (2,400 productive minutes per agent-week)).
* Cohorts: up to 4 cohorts, each ≤ 60 agents, trained 2 weeks before becoming productive, start weeks between week −6 and week 6;
  choose start weeks and sizes to cover every week's requirement with the fewest agent-weeks (agents stay until week 14); ties →
  later start weeks.

## 3. Why capable analysts get it wrong

* Weekly reports are labelled by calendar dates, inviting calendar-week alignment.
* The opening surge and the refund-release surge are tied to IRS dates, which move year to year.
* A blurred profile under-states peaks and mis-times them.
* Training lead time makes cohort timing a scheduling problem, not just a headcount number.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–3 | `filing_season_statistics_2023.html`, `…2024.html`, `…2025.html` (weekly report archives) | HTML | ~15 weekly tables each | IRS newsroom | U.S. Gov public domain | Cumulative weekly statistics |
| 4 | `filing_season_weekly_long.csv` | CSV | ~400 | Derived | Public domain | Long format |
| 5 | `irs_season_opening_announcements.pdf` | PDF | — | IRS newsroom | Public domain | Opening dates, 2026 announcement |
| 6 | `irs_path_act_refund_timing.pdf` | PDF | — | IRS | Public domain | Refund-release timing |
| 7 | `soi_individual_returns_by_week_context.xlsx` | XLSX | ~200 | IRS SOI | Public domain | Context |
| 8 | `workforce_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `calendar_week_forecast.xlsx` | XLSX | ~20 | Task author | — | Calendar-aligned forecast |
| 10 | `cohort_constraints.json` | JSON | — | Task author | — | Cohort rules |

## 5. Deterministic solution path

1. Parse weekly cumulative receipts; compute weekly volumes; anchor each season in event time.
2. Build the aligned profile; forecast 2026 on the announced calendar; compute requirements.
3. Solve the cohort schedule (small integer search); report coverage.
4. Contrast with the calendar-week forecast's coverage.

## 6. Wrong paths (method errors, not misreadings)

**A — calendar-week averaging.** Peaks blurred and shifted; cohorts start late.

**B — single anchor.** Refund wave mis-timed.

**C — requirement from season totals.** Ignores weekly peaks.

**D — ignoring training lead time.** Cohorts not productive in time.

## 7. Why the stump is analytical, not semantic

The volumes, anchors and scheduling rules are explicit. The trap is the time axis used to build seasonality.

## 8. Draft task prompt (prose)

> Plan our four 2026 hiring cohorts for tax-season support as the workforce memo describes: build the weekly volume profile aligned to
> each season's opening and refund-release dates, place it on the 2026 calendar, convert to agents and schedule the cohorts. Provide
> `cohort_plan.csv` (cohort: start week, size), `coverage_chart.png` (weekly requirement vs staffed agents for our plan and the
> calendar-week plan), and a one-page `hiring_plan.pdf`.

## 9. Deliverables

* `cohort_plan.csv`, `coverage_chart.png`, `hiring_plan.pdf`.

## 10. Where 25+ rubric criteria come from

* 14 weekly forecasts and requirements (sampled); 4 cohort start weeks and sizes; agent-weeks total; coverage gaps of the alternative.

## 11. Golden-output checklist

* Event-time profile with two anchors; 2026 dates; requirement formula; optimal cohort plan with ties.

## 12. Build notes (scope tuning)

* Verify the archived weekly tables include self-prepared e-file receipts for all three seasons.
* Confirm the calendar-week plan leaves at least one peak week under-covered by ≥ 10%.
