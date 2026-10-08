# FC33 — Triage staffing for a browser: the "season" is the release train, not the calendar

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Software organizations staffing QA, triage and support around release trains (browser, OS and app release cycles) |
| Domain | Software engineering operations |
| Task shape | 02 · Forecast across many periods (13 weekly new-bug forecasts → one committed triage staffing level) |
| Core method | Event-time (days-since-release) inflow profile estimated from recent cycles, projected onto the future release calendar, plus a slow-moving level |
| Analytical stump | Bug inflow spikes after each release; when the release cadence changed (six weeks to four), calendar-based seasonal models (52-week, weekly dummies) place spikes in the wrong weeks. The correct seasonality is aligned to release events |
| Primary sources | Mozilla Bugzilla (bug creation data via REST API), Mozilla Firefox release calendar |

## 1. The real-world situation

A browser team staffs bug triage weekly. The planning model is "same week last year × 1.03". After the release cadence shortened, the
model placed post-release spikes in the wrong weeks: triagers sat idle one week and fell behind the next.

## 2. The decision (one deterministic recommendation)

**The committed triage staffing level for next quarter = staff needed in the busiest forecast week (forecast new bugs ÷ 120 bugs
per triager-week, rounded up).**

Rules (engineering operations memo):

* Series: bugs created per day in product Firefox (all components), excluding bugs marked as duplicates within 7 days and bugs filed
  by automation accounts listed in the memo.
* Release events: Firefox release dates from the public calendar (actual and scheduled).
* Event-time profile: for the last 10 release cycles before the origin, daily inflow ÷ the cycle's mean daily inflow, by day since
  release (0–27); average across cycles → profile p(d).
* Level: mean daily inflow over the last 4 cycles.
* Forecast each future day = level × p(days since the most recent release on the schedule); weekly sums (Mon–Sun) for 13 weeks.
* Staffing = ceil(max weekly forecast ÷ 120).

## 3. Why capable analysts get it wrong

* Seasonal-naive and weekly-dummy models are the default for weekly operational series.
* A cadence change shifts spike positions by weeks; last year's week no longer corresponds to the same release phase.
* Profiles must be built in event time, then mapped to calendar weeks using the future schedule.
* Including automation-filed bugs or duplicates inflates spikes.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–4 | `bugzilla_firefox_bugs_2019.json` … `2022.json` (REST API exports) | JSON | 30k–60k bugs each | bugzilla.mozilla.org | Publicly visible bug metadata (verify reuse terms) | Creation dates, resolution, reporter |
| 5–6 | `bugzilla_firefox_bugs_2023.json`, `2024.json` | JSON | 30k–60k each | Same | Same | Recent cycles |
| 7 | `bugs_daily_firefox.csv` | CSV | ~2.2k days | Derived | Same | Daily inflow |
| 8 | `firefox_release_calendar.csv` | CSV | ~100 | Mozilla release calendar (whattrainisitnow / wiki) | Public | Release dates |
| 9 | `automation_accounts.json` | JSON | ~20 | Task author | — | Exclusions |
| 10 | `engineering_operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 11 | `current_planning_model.xlsx` | XLSX | ~13 | Task author | — | Calendar-week forecast |

## 5. Deterministic solution path

1. Build clean daily inflow; tag days since release.
2. Profile over the last 10 cycles; level over the last 4.
3. Map future days to release phases via the schedule; weekly sums; peak; staffing.
4. Contrast with the calendar-week model.

## 6. Wrong paths (method errors, not misreadings)

**A — same week last year.** Spikes misaligned; peak week wrong.

**B — weekly dummies over multiple years.** Mixes cadences.

**C — duplicates/automation kept.** Inflated profile.

**D — profile in calendar weeks.** Smears spikes.

## 7. Why the stump is analytical, not semantic

Inflow, exclusions and the event-time method are defined. The trap is choosing the wrong seasonal clock.

## 8. Draft task prompt (prose)

> Set next quarter's triage staffing from a forecast of weekly new bugs that follows the release train, as the engineering
> operations memo describes. Using the Bugzilla exports and the release calendar, build the post-release profile, project it onto the
> coming releases and tell me the staffing level. Provide `weekly_bug_forecast.csv` (13 weeks with release phases), `release_profile.png`
> (inflow by days since release, recent cycles overlaid), and a one-page `triage_staffing.pdf` with the level and the misplaced peaks
> in the current model.

## 9. Deliverables

* `weekly_bug_forecast.csv`, `release_profile.png`, `triage_staffing.pdf`.

## 10. Where 25+ rubric criteria come from

* Profile values (28 days, spot-check 8); level; 13 weekly forecasts; peak week; staffing; current-model contrast.

## 11. Golden-output checklist

* Exclusions; event-time profile; level window; schedule mapping; ceiling.

## 12. Build notes (scope tuning)

* Choose an origin within two years after the cadence change so last-year weeks are misaligned; confirm peak weeks differ.
* Record API queries and timestamps; bug metadata can change (e.g. later duplicates).
