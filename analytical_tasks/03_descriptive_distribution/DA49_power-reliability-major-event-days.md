# DA49 — Reliability with storms set aside: major event days by the 2.5-beta rule, not by eye

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Availability reporting that separates "normal operations" from major incidents (cloud SLA reporting with exclusions, telecom network availability, data-centre uptime) |
| Domain | Electric utilities |
| Task shape | 10 · Scorecard against thresholds (8 states × years → SAIDI excluding major event days against the regulator's benchmark; which states' utilities face a performance review) |
| Core method | IEEE 1366 major event day (MED) identification: daily SAIDI from customer-minutes interrupted ÷ customers served; α = mean and β = SD of ln(daily SAIDI) over the 5 preceding years (excluding zero days); T_MED = exp(α + 2.5β); MEDs excluded from the annual "normal" SAIDI |
| Analytical stump | Excluding days with large outages "by judgement", using mean + 2.5 SD on the raw (skewed) scale, or computing the threshold on the same year being assessed gives different MED sets and different normal-operations SAIDI. The log-normal fit on a trailing window is the standard |
| Primary sources | ORNL EAGLE-I county-level outage snapshots (15-minute customers out); EIA-861 customers served by state |

## 1. The real-world situation

A multi-state regulator reviews utilities whose normal-operations SAIDI exceeds a benchmark of 120 minutes per customer per year. Staff built
daily outage minutes from the EAGLE-I dataset and excluded "storm days" where more than 5% of customers were out. Utilities in hurricane-prone
states argued that the rule excluded too few days; inland utilities argued the opposite.

## 2. The decision (one deterministic recommendation)

**The states whose normal-operations SAIDI (MEDs excluded by the 2.5β method) exceeds 120 minutes in the assessment year, with MED counts and
thresholds for all eight states.**

Rules (regulator memo):

* Data: EAGLE-I county snapshots (customers out per 15 minutes) for the 8 states, 2015 to the assessment year.
* Customer-minutes interrupted per day = Σ over 15-minute snapshots of customers out × 15 (memo convention; snapshot gaps filled with the last
  value for ≤ 1 hour, else 0).
* Customers served: EIA-861 state totals for the year.
* Daily SAIDI = customer-minutes ÷ customers served.
* T_MED for year Y: α, β from ln(daily SAIDI) for the 5 years before Y, days with SAIDI > 0.
* Normal SAIDI = Σ daily SAIDI on non-MED days in year Y.
* Review: normal SAIDI > 120.

## 3. Why capable analysts get it wrong

* Fixed "percentage out" thresholds feel intuitive but ignore each system's own variability.
* Daily SAIDI is right-skewed; thresholds on the raw scale misbehave.
* The threshold must come from prior years, not the assessed year.
* Snapshot gaps must be handled consistently.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–9 | `eaglei_outages_<yyyy>.csv` (2015–2023) | CSV | ~30–40M rows per year (US) | ORNL EAGLE-I dataset (Figshare, Brelsford et al. 2024) | CC BY 4.0 | County 15-minute customers out |
| 10 | `eaglei_coverage.csv` | CSV | ~3k | Same | CC BY 4.0 | County coverage ratios |
| 11 | `Sales_Ult_Cust_<yyyy>.xlsx` (EIA-861) | XLSX | ~3k per year | EIA | U.S. Gov public domain | Customers served |
| 12 | `ieee_1366_2p5beta_citation.pdf` | PDF | — | IEEE 1366 (cite) | Cite | MED method |
| 13 | `regulator_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 14 | `staff_storm_day_rule_results.xlsx` | XLSX | 8 | Task author | — | Staff exclusion results |
| 15 | `states_in_scope.json` | JSON | 8 | Task author | — | States |
| 16 | `daily_state_cmi.parquet` | Parquet | ~25k | Derived | CC BY 4.0 | Daily customer-minutes |

## 5. Deterministic solution path

1. Aggregate snapshots to daily customer-minutes per state with gap rule.
2. Daily SAIDI; trailing α, β; T_MED; MED days.
3. Normal SAIDI; review list.
4. Contrast with staff rule.

## 6. Wrong paths (method errors, not misreadings)

**A — fixed 5%-out rule.** Inconsistent across systems.

**B — threshold from the assessed year.** Circular.

**C — mean + 2.5 SD on the raw scale.** Skew ignored.

**D — including zero days in the log fit.** Undefined/biased.

## 7. Why the stump is analytical, not semantic

Aggregation and the MED method are specified. The trap is outlier exclusion on a skewed metric with a proper reference window.

## 8. Draft task prompt (prose)

> Which states' utilities face a reliability review this year? Compute normal-operations SAIDI with the 2.5β major-event-day method in the
> regulator memo. Provide `state_reliability.csv` (state: T_MED, MED count, total SAIDI, normal SAIDI, review), `daily_saidi_lognormal.png`, and a
> one-page `review_list.pdf`.

## 9. Deliverables

* `state_reliability.csv`, `daily_saidi_lognormal.png`, `review_list.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 states × (T_MED, MEDs, normal SAIDI, review) = 32; contrast; gap handling.

## 11. Golden-output checklist

* Aggregation; gap fill; customers served; trailing window; log fit; exclusion; review rule.

## 12. Build notes (scope tuning)

* Note EAGLE-I coverage is not 100% of customers; the memo scales by the coverage ratio (document it).
* Confirm the staff rule and the 2.5β method disagree for at least two states.
