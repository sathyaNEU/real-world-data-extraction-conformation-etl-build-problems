# AD30 — Rare incidents: annual counts are too slow, so watch the time between them

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Reliability and safety programmes for rare events: data-centre outages at cloud providers, aviation and rail safety events, pipeline operator incident oversight |
| Domain | Energy infrastructure safety |
| Task shape | 10 · Scorecard against thresholds (10 operators × detection rules → which operators trigger an integrity-management audit this year) |
| Core method | Time-between-events (t-chart) on days between reportable incidents per operator, exponential model with baseline mean from 2015–2019; transformed limits (Nelson's power transformation, y = t^(1/3.6)); run rules; comparison with a Poisson c-chart on annual counts |
| Analytical stump | Rare events produce annual counts of 0–4; a c-chart cannot signal until a year closes, and its limits barely exclude anything. Gaps between events carry the information. The exponential is skewed, so symmetric 3σ limits on raw gaps are wrong |
| Primary sources | PHMSA pipeline incident data (hazardous liquid and gas transmission), PHMSA annual report mileage data |

## 1. The real-world situation

A regulator's integrity office audits operators whose incident frequency has worsened. Its current monitor is a c-chart of incidents per
year per operator: by the time a year closes, a deteriorating operator has had several incidents. The office will audit the operators that
signal on the memo's rare-event monitor by 30 June of the review year.

## 2. The decision (one deterministic recommendation)

**The set of operators (among the 10 in scope) that trigger an audit by 30 June 2023, and the date each triggered.**

Rules (integrity memo):

* Incidents: PHMSA hazardous-liquid incident reports for the 10 operators in `operators_in_scope.csv`, 2015-01-01 to 2023-06-30; one
  incident per report ID (supplemental reports collapsed to the latest).
* Exposure normalisation: gap in days × (operator's pipeline miles in that year ÷ miles in 2019), so gaps are expressed in 2019-mile
  equivalents.
* Baseline 2015–2019: mean normalised gap θ per operator (exponential MLE).
* Transformed gaps y = t^(1/3.6); individuals chart on y with centre and limits from baseline moving ranges; signal when a point falls
  below the lower limit **or** 4 of 5 consecutive points are below centre − 1σ (one-sided, shorter gaps).
* Comparison: c-chart on annual counts with Poisson limits from the baseline mean.
* Audit if the t-chart signals between 2020-01-01 and 2023-06-30.

## 3. Why capable analysts get it wrong

* Counts per period are the default control chart for incidents.
* For rare events, each event's timing is the data; aggregation throws it away.
* Raw exponential gaps are highly skewed; normal-theory limits on them produce absurd negative lower limits.
* Operator growth (more miles) shortens gaps without worse performance; the memo normalises.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `incident_hl_2010_present.xlsx` | XLSX | ~6k | PHMSA Pipeline Incident Flagged Files | U.S. Gov public domain | Hazardous liquid incidents |
| 2 | `incident_gas_transmission_2010_present.xlsx` | XLSX | ~2k | PHMSA | Public domain | Context |
| 3 | `annual_hazardous_liquid_2015_2023.xlsx` | XLSX | ~4k operator-years | PHMSA annual report data | Public domain | Miles by operator |
| 4 | `incident_field_definitions.pdf` | PDF | — | PHMSA | Public domain | Fields, report types |
| 5 | `operators_in_scope.csv` | CSV | 10 | Task author | — | Operators |
| 6 | `operator_id_history.csv` | CSV | ~40 | Task author (mergers/renames) | — | ID continuity |
| 7 | `integrity_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `current_c_chart_results.xlsx` | XLSX | 10 | Task author | — | Existing monitor |
| 9 | `nelson_1994_citation.pdf` | PDF | — | Cite | Cite | Transformation for exponential data |
| 10 | `incident_events.parquet` | Parquet | ~1.5k | Derived | Public domain | Cleaned event list |

## 5. Deterministic solution path

1. Collapse supplemental reports; select operators; order incidents; compute gaps.
2. Normalise gaps by mileage; estimate baseline θ and chart limits on transformed gaps.
3. Apply signal rules from 2020; record first signal dates.
4. Run the c-chart for comparison; list audits.

## 6. Wrong paths (method errors, not misreadings)

**A — annual c-chart.** Signals late or never.

**B — normal limits on raw gaps.** Negative lower limit; no signals.

**C — no mileage normalisation.** Growth flagged as deterioration.

**D — counting supplemental reports as incidents.** Gaps shortened artificially.

## 7. Why the stump is analytical, not semantic

The events, transformation and signal rules are specified. The trap is choosing the wrong monitoring statistic for rare events.

## 8. Draft task prompt (prose)

> Which operators should we audit by mid-2023? Apply the time-between-incidents monitor in the integrity memo to the ten operators and
> compare it with our annual count chart. Provide `operator_scorecard.csv` (operator: baseline θ, limits, first signal date, c-chart signal),
> `t_chart_small_multiples.png`, and a one-page `audit_list.pdf`.

## 9. Deliverables

* `operator_scorecard.csv`, `t_chart_small_multiples.png`, `audit_list.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 operators × (θ, signal date, c-chart result) = 30; audit set; supplemental-collapse count.

## 11. Golden-output checklist

* De-duplication; normalisation; transformation; limits; run rule; dates.

## 12. Build notes (scope tuning)

* Choose operators so that at least two signal on the t-chart in 2021–2022 while the c-chart never signals.
* Freeze the PHMSA file version; records are revised.
