# AD39 — Settlement fails: summing a balance ten times does not make ten times the problem

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Broker-dealer and clearing-firm compliance (Regulation SHO threshold securities, close-out obligations); any monitor built on daily outstanding balances (open tickets, backlog, receivables) |
| Domain | Capital markets compliance |
| Task shape | 10 · Scorecard against thresholds (securities × settlement days → threshold-list status; the firm's close-out escalation list for the review date) |
| Core method | Treat the published fails-to-deliver quantity as an outstanding balance at each settlement date; threshold-security test = balance ≥ 10,000 shares and ≥ 0.5% of shares outstanding for 5 consecutive settlement days; persistence counter (13 consecutive days → close-out) |
| Analytical stump | The fails file reports the aggregate *outstanding* fail position per settlement date, not new fails. Summing it over a month or ranking by monthly totals overstates persistent small fails and misses the consecutive-day structure that the rule actually tests. Gaps (dates with no row) mean the balance fell below the reporting floor, not "unknown" |
| Primary sources | SEC fails-to-deliver data (semi-monthly files); shares outstanding from SEC Financial Statement and Notes (dei:EntityCommonStockSharesOutstanding) |

## 1. The real-world situation

A clearing firm's compliance team escalates securities likely to reach mandatory close-out. An analyst built a "fails leaderboard" by
summing the reported fail quantity per security over the month and flagged the top 50. Several flagged securities never appeared on
exchange threshold lists, while two that did were missing.

## 2. The decision (one deterministic recommendation)

**The set of securities on the firm's close-out escalation list as of the review date: those that have been threshold securities for 13
consecutive settlement days.**

Rules (compliance memo):

* Data: SEC fails-to-deliver files for the six months ending at the review date; one row per CUSIP per settlement date (quantity = total
  outstanding fails).
* Missing CUSIP-date rows = balance below reporting minimum → treated as failing the test that day.
* Shares outstanding: most recent value filed before each settlement date (the memo's lookup rule).
* Threshold day: quantity ≥ 10,000 and quantity ≥ 0.005 × shares outstanding.
* Threshold security on day t: threshold days on t and the 4 previous settlement days (5 consecutive).
* Escalation: threshold security on each of the 13 consecutive settlement days ending at the review date.
* Settlement calendar: business days excluding the memo's holiday list.

## 3. Why capable analysts get it wrong

* Daily quantities look like flows; summing is the default aggregation.
* The rule is about persistence relative to size, not volume.
* Treating missing days as zero or as carry-forward changes runs; the memo states the convention.
* Shares outstanding must be point-in-time; using the latest value misclassifies securities after splits or offerings.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `cnsfails<yyyymm>a.txt`, `cnsfails<yyyymm>b.txt` (6 months) | Pipe-delimited text | ~60–90k each | SEC fails-to-deliver data | U.S. Gov public domain | Fails by CUSIP and date |
| 13 | `fsnds_dei_shares_outstanding.parquet` | Parquet | ~200k | Derived from SEC Financial Statement and Notes data sets | Public domain | Shares outstanding history |
| 14 | `cusip_to_cik_map.csv` | CSV | ~8k | Task author (from SEC filings' cover pages and FTD symbols) | — | Join key |
| 15 | `settlement_holidays.json` | JSON | ~10 | Task author | — | Calendar |
| 16 | `reg_sho_rule_203_excerpt.pdf` | PDF | — | 17 CFR 242.203 (public law) | Public domain | Threshold definition |
| 17 | `compliance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 18 | `analyst_monthly_sum_leaderboard.xlsx` | XLSX | 50 | Task author | — | Naive list |
| 19 | `exchange_threshold_lists_sample.csv` | CSV | ~3k | Nasdaq/NYSE published threshold lists (public pages) | Public (verify terms) | Validation |

## 5. Deterministic solution path

1. Stack fails files; build CUSIP × settlement-date panel with missing = below floor.
2. Join point-in-time shares outstanding.
3. Threshold days; 5-day runs; 13-day persistence at the review date.
4. Escalation list; validate against exchange lists; contrast with the leaderboard.

## 6. Wrong paths (method errors, not misreadings)

**A — monthly sum ranking.** Volume, not persistence.

**B — carry-forward on missing days.** Runs too long.

**C — latest shares outstanding.** Misclassification after capital changes.

**D — calendar days instead of settlement days.** Run lengths wrong.

## 7. Why the stump is analytical, not semantic

The rule and conventions are specified. The trap is treating a stock variable as a flow and losing the run structure.

## 8. Draft task prompt (prose)

> Build our close-out escalation list for the review date from the SEC fails data and the threshold rule in the compliance memo. Provide
> `threshold_scorecard.csv` (CUSIP × settlement day: quantity, shares outstanding, threshold day, threshold security), `persistence_chart.png`
> (run lengths for escalated securities and the leaderboard's top ten), and a one-page `escalation_list.pdf` with validation against exchange
> lists.

## 9. Deliverables

* `threshold_scorecard.csv`, `persistence_chart.png`, `escalation_list.pdf`.

## 10. Where 25+ rubric criteria come from

* Escalated securities (each a criterion); run lengths for 8 securities; validation matches; leaderboard contrast; missing-day handling.

## 11. Golden-output checklist

* Panel with missing convention; point-in-time shares; threshold test; 5-day and 13-day runs; calendar.

## 12. Build notes (scope tuning)

* Choose a review date with 5–15 escalations and at least two leaderboard names that are not threshold securities.
