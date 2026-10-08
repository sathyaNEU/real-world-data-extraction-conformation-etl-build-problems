# AD17 — Paging on error budgets: raw error-rate thresholds page on noise and sleep through slow burns

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Site-reliability alerting on service-level objectives (multi-window burn-rate alerts popularized by SRE practice at large web companies) |
| Domain | Web operations / SRE |
| Task shape | 04 · Setting one dial (the long-window burn-rate threshold, given fixed short-window confirmation) |
| Core method | SLO error-budget burn rate = observed error ratio ÷ (1 − SLO); multi-window confirmation (long and short windows); replay against labelled incident windows; choose the threshold meeting recall and page-budget constraints |
| Analytical stump | Thresholds on 1-minute error ratios fire on low-traffic noise (one failed request out of three) and miss sustained moderate burns that exhaust the budget; burn rate normalizes by the SLO and windows set the sensitivity–speed trade-off. Gaps in logs (no traffic recorded) are outages, not zero errors |
| Primary sources | NASA Kennedy Space Center HTTP access logs (July–August 1995) |

## 1. The real-world situation

An operations team protects a public web service with a 99.5% availability SLO (non-5xx and non-timeout responses). Its alert pages when
the 1-minute error ratio exceeds 5%. Overnight, low traffic produced pages for single failures; during a multi-day degradation the alert
flapped, and during the hurricane-driven shutdown — when no requests were logged — it never fired at all.

## 2. The decision (one deterministic recommendation)

**The long-window burn-rate threshold B (to one decimal) for a 1-hour/5-minute two-window alert that pages on every labelled incident
window while producing at most 6 pages over the two months.**

Rules (SRE memo):

* Logs: NASA KSC access logs, 1 July – 31 August 1995. Bad events: HTTP status ≥ 500, plus every minute in which the service was
  unreachable — defined as gaps of ≥ 10 consecutive minutes with zero log lines during hours when the previous week's same hour had
  ≥ 100 requests; each such minute counts as 100 bad requests (the memo's convention).
* Burn rate over a window = (bad ÷ total) ÷ (1 − 0.995).
* Alert fires when the 1-hour burn rate ≥ B **and** the 5-minute burn rate ≥ B; consecutive firing minutes form one page; a page
  ends after 15 minutes without firing.
* Labelled incident windows: in `incident_windows.json` (outage and degradation periods from documented events and the logs).
* Choose the largest B (grid 1.0 … 20.0 in 0.1 steps) that detects all incident windows with ≤ 6 pages total.

## 3. Why capable analysts get it wrong

* Error-ratio thresholds ignore traffic volume; small denominators create spurious spikes.
* Burn rate expresses how fast the error budget is spent; a threshold on it maps directly to budget risk.
* Two windows trade detection speed against noise; a single short window pages on blips, a single long window is slow to reset.
* Missing log lines are not good minutes; outages must be imputed as bad events.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `NASA_access_log_Jul95.gz` | Text (Common Log Format) | ~1.9M | NASA KSC logs (Internet Traffic Archive) | Public domain (verify) | July requests |
| 2 | `NASA_access_log_Aug95.gz` | Text | ~1.6M | Same | Same | August requests |
| 3 | `requests_per_minute.parquet` | Parquet | ~89k minutes | Derived | Same | Totals and errors per minute |
| 4 | `incident_windows.json` | JSON | ~5 | Task author (documented outages/degradations) | — | Labels |
| 5 | `ita_dataset_notes.html` | HTML | — | Internet Traffic Archive | Public | Log description |
| 6 | `google_sre_workbook_alerting_excerpt.pdf` (citation) | PDF | — | Cite | Cite | Burn-rate alerting concepts |
| 7 | `sre_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `current_alert_replay.csv` | CSV | ~200 | Task author | — | Existing rule's pages |
| 9 | `slo_definition.json` | JSON | — | Task author | — | SLO and event classes |
| 10 | `gap_detection_rules.json` | JSON | — | Task author | — | Outage imputation |

## 5. Deterministic solution path

1. Parse logs; per-minute totals and 5xx counts; detect gaps and impute bad minutes.
2. Compute rolling 1-hour and 5-minute burn rates.
3. Sweep B; compute pages and incident coverage; choose the largest feasible B.
4. Replay the current 5% rule for contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — raw error-ratio threshold.** Pages on noise; misses outages.

**B — gaps ignored.** Outages invisible.

**C — single window.** Either noisy or slow.

**D — choosing B by eye on one incident.** Fails coverage or page budget.

## 7. Why the stump is analytical, not semantic

Events, SLO, windows and constraints are defined. The traps are denominator noise, missing-data semantics turned into analysis, and
window design — analytical alerting choices.

## 8. Draft task prompt (prose)

> Tune our burn-rate alert on the 1995 KSC logs as the SRE memo specifies: count bad events including outage minutes, compute 1-hour and
> 5-minute burn rates, and find the largest threshold that pages on every incident window with no more than six pages in two months.
> Provide `threshold_sweep.csv` (B: pages, incidents detected), `burn_rate_timeline.png` (burn rates with incidents and pages marked), and a
> one-page `alerting_decision.pdf` comparing with the current rule.

## 9. Deliverables

* `threshold_sweep.csv`, `burn_rate_timeline.png`, `alerting_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* B; pages and detection times for each incident (≈ 5 × 2); total pages; sweep values at 5 checkpoints; current-rule page count.

## 11. Golden-output checklist

* Correct parsing and status handling; gap imputation; burn-rate formula; two-window logic; page grouping; sweep rule.

## 12. Build notes (scope tuning)

* Document incident windows from the logs (the early-August hurricane shutdown is a visible gap) and any degradation periods identified by
  elevated 5xx.
* Confirm the current rule produces > 50 pages.
