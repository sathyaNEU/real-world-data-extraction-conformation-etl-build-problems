# DA02 — Which patent examining groups are slowest? Percentiles of waiting times when many cases are still waiting

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Domain | Government operations / intellectual-property administration / workload planning |
| Task shape | 01 · Ranked list under a cap (5 work groups receive new examiner teams) |
| Core method | Kaplan–Meier (product-limit) estimation of time-to-disposition with pending applications right-censored at the data cut-off; percentiles read from the survival curve |
| Analytical stump | Completed-only percentiles drop exactly the slowest cases; treating pending cases as finished at the cut-off truncates them. Both understate pendency most in the slowest groups, reordering the ranking |
| Primary sources | USPTO Patent Examination Research Dataset (PatEx) |

## 1. The real-world situation

A patent office will add **five examiner teams**, one each to the five work groups with the longest 90th-percentile
time from filing to final disposition (patent issued or application abandoned) for applications filed in 2020. The
analyst computed percentiles over applications already disposed of. Two work groups known for multi-year backlogs ranked
in the middle; their completed cases were, by construction, the fast ones.

## 2. The decision (one deterministic recommendation)

**Which five work groups receive teams, and which group is sixth?**

Rules (workload planning memo):

* Cohort: utility applications filed 2020-01-01 to 2020-12-31 (PatEx application table); work group = first three digits of
  the examiner art unit at the data cut-off; groups with ≥ 2,000 cohort applications only.
* Event = disposition: issue date or abandonment date, whichever occurs. Applications without either by the data cut-off
  date (stated in the release notes) are still pending and must be included as **observed to be undisposed up to the
  cut-off**.
* Time in days from filing date; percentiles estimated nonparametrically from the survival function; P90 = the smallest t
  with estimated disposed share ≥ 90%. If a group's curve never reaches 90% before the cut-off, its P90 is "> cut-off" and it
  ranks above all groups with a finite P90 (ties among such groups broken by the disposed share at the cut-off, lower first).
* Rank by P90 descending; teams to the top five.

## 3. Why capable analysts get it wrong

* Descriptive statistics are usually computed on "completed" records; for durations, completion depends on the duration.
* Filling pending cases with the cut-off date treats a lower bound as the value.
* Groups differ in the share still pending, so the bias is uneven and reorders groups.
* Some groups never reach 90% disposed before the cut-off; the ranking rule must handle that explicitly.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `application_data.csv` (PatEx) | CSV | ~12M | USPTO Office of the Chief Economist | U.S. Gov public domain | Filing, art unit, status, issue and abandonment dates |
| 2 | `application_data_2020_cohort.parquet` | Parquet | ~0.6M | Derived | Public domain | Working cohort |
| 3 | `status_codes.csv` | CSV | ~200 | USPTO PatEx | Public domain | Status meanings |
| 4 | `continuity_parents.csv` (PatEx) | CSV | ~10M | USPTO | Public domain | Context (continuations) |
| 5 | `patex_documentation.pdf` + release notes | PDF | — | USPTO | Public domain | Field definitions, cut-off date |
| 6 | `uspto_pendency_definitions.pdf` | PDF | — | USPTO Patents Data at a Glance (methodology) | Public domain | Pendency concepts |
| 7 | `art_unit_to_tc_mapping.csv` | CSV | ~600 | USPTO | Public domain | Work group → technology center |
| 8 | `kaplan_meier_reference.pdf` (citation) | PDF | — | Cite | Cite | Product-limit estimator |
| 9 | `workload_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `analyst_completed_only_ranking.xlsx` | XLSX | ~40 | Task author | — | The biased ranking |

## 5. Deterministic solution path

1. Build the 2020 cohort; assign work groups; compute event indicator and time (event date or cut-off).
2. Kaplan–Meier per work group; read P50 and P90 (or "> cut-off").
3. Rank with the stated rule; top five + sixth.
4. Contrast with completed-only and cut-off-as-event percentiles.

## 6. Wrong paths (method errors, not misreadings)

**A — completed-only percentiles.** Slow groups look fast; ranking changes.

**B — pending set to the cut-off as an event.** P90 capped at the cut-off for slow groups; ties and misordering.

**C — abandonment ignored or censored.** Not the defined event; distorts groups with high abandonment.

**D — mean pendency.** Undefined under censoring; ranking by a different statistic.

## 7. Why the stump is analytical, not semantic

The event, cohort and cut-off are defined, and the memo explicitly says pending applications are observed only up to the
cut-off. The error is choosing an estimator that is biased under right-censoring — a statistical method choice.

## 8. Draft task prompt (prose)

> We're adding five examiner teams to the work groups with the longest 90th-percentile time to final disposition for 2020
> filings, following the workload memo. Using the PatEx files in the folder, estimate each group's percentiles properly —
> including the applications still pending — and tell me the five groups and the sixth. Provide
> `pendency_percentiles.csv` (group, applications, disposed share at cut-off, P50, P90, rank), `survival_curves.png` showing
> disposition curves for the top eight groups with the 90% line, and a one-page `team_allocation.pdf` with the decision and
> how the completed-only ranking differs.

## 9. Deliverables

* `pendency_percentiles.csv`, `survival_curves.png`, `team_allocation.pdf`.

## 10. Where 25+ rubric criteria come from

* Top 5 + 6th; P50/P90 for top 10 groups (20 values); disposed shares; completed-only contrast.

## 11. Golden-output checklist

* Correct cohort and event; censoring at cut-off; KM percentiles; "> cut-off" handling; ranking rule.

## 12. Build notes (scope tuning)

* Choose the cohort year and PatEx release so that some groups have > 15% still pending; confirm the completed-only ranking
  differs in at least two of the five.
* Record the PatEx release and its cut-off date in the memo.
